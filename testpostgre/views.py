from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from extra_views import ModelFormSetView

from reportlab.platypus import BaseDocTemplate, PageTemplate
from reportlab.platypus import Paragraph, PageBreak, FrameBreak
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4, mm, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import cidfonts
from reportlab.platypus.frames import Frame
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont

from .models import Member
from .forms import MemberUpdateForm

import csv
import datetime
import unicodedata

class ListUpdateView(ModelFormSetView):
    model = Member
    template_name = 'member_list.html'
    form_class = MemberUpdateForm

    # def get_queryset(self):
    #     try:
    #         q = self.request.GET.get('query')
    #     except:
    #         q = None
    #     return Member.objects.search(query=q)

#削除
def member_remove(request, pk):
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    return redirect('update_sample')

#CSV出力
def member_export(request):
    responese = HttpResponse(content_type='text/csv')
    responese['Content-Disposition'] = 'attachment; filename="member.csv"'

    writer = csv.writer(responese)
    for member in Member.objects.all():
        writer.writerow([member.pk, member.full_name, member.group.name, member.auth])

    return responese

def member_pdf(request):

    LE_ID = 3
    LE_NAME = 20
    LE_GROUP = 12
    LE_AUTH = 8

    response = HttpResponse(content_type='application/pdf')
    pdf_name = 'memberlist.pdf'
    response['Content-Disposition'] = 'filename=' + pdf_name
    # response['Content-Disposition'] = 'attachment; filename=' + pdf_name

    #デプロイするときはこっち
    # font_url = r'/home/sakai/sakai.pythonanywhere.com/mst/static/fonts/MSMincho/msmincho.ttc'

    #localhostはこっち
    font_url = r'./mst/static/fonts/MSMincho/msmincho.ttc'

    pdfmetrics.registerFont(TTFont("msmincho", font_url))
    # pdfmetrics.registerFont(cidfonts.UnicodeCIDFont("HeiseiMin-W3"))
    
    doc = BaseDocTemplate(response, 
        title="memberlist",
        pagesize=portrait(A4),
        )

    #Frameの枠を表示
    show = 1 
    frames = [
            Frame(5*mm, 250*mm, 150*mm, 40*mm, showBoundary=0),
            Frame(5*mm, 255*mm, 200*mm, 15*mm, showBoundary=show),
            Frame(5*mm, 10*mm, 200*mm, 245*mm, showBoundary=show),
        ]
    page_template = PageTemplate("frames", frames=frames)
    doc.addPageTemplates(page_template)

    style_dict ={
        "name":"normal",
        "fontName":"msmincho",
        "fontSize":18,
        "leading":20,
        "firstLineIndent":0,
        }
    # style_dict ={
    #     "name":"normal",
    #     "fontName":"HeiseiMin-W3",
    #     "fontSize":18,
    #     "leading":20,
    #     "firstLineIndent":20,
    #     }

    style = ParagraphStyle(**style_dict)

    style_dict ={
        "name":"normal",
        "fontName":"msmincho",
        "backColor":"paleturquoise",
        "borderColor":"white",
        "borderPadding":(5, 5, 16),
        "fontSize":18,
        "leading":20,
        "firstLineIndent":0,
        "alignment":0,
        "spaceShrinkage":0.05,
        "strikeGap":1,
        "strikeOffset":0.25,
        }
    style2 = ParagraphStyle(**style_dict)

    flowables = []

    space = Spacer(10*mm, 10*mm)

    linecnt = 1
    for member in Member.objects.all():

        if linecnt == 1:
            t_delta = datetime.timedelta(hours=9)
            JST = datetime.timezone(t_delta, 'JST')
            now = datetime.datetime.now(JST)
            today_str = now.date().strftime('%Y/%m/%d')
            para = Paragraph(today_str, style)
            flowables.append(para)
            para = Paragraph("担当者一覧", style)
            flowables.append(para)

            #次のフレームへ
            flowables.append(FrameBreak())

            print_str = settext("ID", LE_ID, 2) + settext("名前", LE_NAME) + settext("グループ", LE_GROUP) + settext("権限", LE_AUTH)
            # print_str = "ID&nbsp;名前&nbsp;&nbsp;&nbsp;グループ&nbsp;権限"
            para = Paragraph(print_str, style2)
            flowables.append(para)

            #次のフレームへ
            flowables.append(FrameBreak())

        detail_str = settext(member.id, LE_ID, 2)
        detail_str += settext(member.full_name, LE_NAME)
        detail_str += settext(member.group.name, LE_GROUP)
        detail_str += settext(member.auth, LE_AUTH)
        para = Paragraph(detail_str, style)
        # para = Paragraph(f"{member.id} {member.full_name} &nbsp; {member.group.name} &nbsp; {member.auth}", style)
        flowables.append(para)
        flowables.append(space)
        linecnt+=1

        if linecnt >= 14:
            #改頁
            flowables.append(PageBreak())
            linecnt=1

    doc.multiBuild(flowables)

    # pdf_size = portrait(A4)
    # pdf_file = canvas.Canvas(response, pagesize=pdf_size, bottomup=False)

    # i=0
    # for member in Member.objects.all():
    #     x = 25
    #     y = 20+20*(i + 1)
    #     # pdf_file.drawString(x*mm, y*mm, member.full_name)
    #     pdf_file.drawString(x*mm, y*mm, f"{i+1}.  {member.full_name}  {member.group}  {member.auth}")
    #     i+=1

    # pdf_file.save()
    
    return response

def settext(text, length, LorR = 1):

    #型変換
    text = str(text)

    #全角調整
    count = 0
    for s in text:
        if unicodedata.east_asian_width(s) in "FWA":
            count += 1

    #全角の数だけ減らす
    length -= count

    if LorR == 1:
        ret_text = text.ljust(length, "|")
    if LorR == 2:
        ret_text = text.rjust(length, "|")

    ret_text += "|"
    return ret_text.replace("|", "&nbsp;")