from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView

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

from mstlist.forms import ScheduleForm, PlayerForm, SagyoForm

from .models import Member, player, Schedule, Sagyo

import csv
import datetime
import unicodedata

# Create your views here.
def index(request):
    return render(request, 'mstlist/index.html')

def sagyo_list(request):
    model = Sagyo.objects.all()
    return render(request, 'mstlist/sagyo_list.html', {'sagyo_list':model})

#新規
def sagyo_new(request):
    if request.method == 'POST':
        form = SagyoForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.save()
            return redirect('sagyolist')
    else:
        form = SagyoForm
        return render(request, 'mstlist/sagyo_Edit.html', {'form':form})

#編集
def sagyo_edit(request, pk):
    sagyo = get_object_or_404(Sagyo, pk=pk)
    if request.method == "POST":
        form = SagyoForm(request.POST, instance=sagyo)
        if form.is_valid():
            sagyo = form.save(commit=False)
            sagyo.save()
            return redirect('sagyolist')
    else:
        form = SagyoForm(instance=sagyo)
    return render(request, 'mstlist/sagyo_Edit.html', {'form': form})

#削除
def sagyo_remove(request, pk):
    sagyo = get_object_or_404(Sagyo, pk=pk)
    sagyo.delete()
    return redirect('sagyolist')

def schedule(request):
    model = Schedule.objects.all().order_by('yDate')
    return render(request, 'mstlist/Schedule.html', {'schedules':model})

def schedule_new(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.yId = Schedule.get_MaxId(schedule)
            schedule.save()
            return redirect('schedule')
    else:
        form = ScheduleForm
        return render(request, 'mstlist/Schedule_Edit.html', {'form':form})

def schedule_edit(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.save()
            return redirect('schedule')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'mstlist/Schedule_Edit.html', {'form': form})

#削除
def schedule_remove(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    schedule.delete()
    return redirect('schedule')

class MemberList(ListView):
    model = player
    template_name = 'player_list.html'
    context_object_name = 'player_list'

def player_new(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.save()
            return redirect('playerlist')
    else:
        form = PlayerForm
        return render(request, 'mstlist/player_Edit.html', {'form':form})

def player_edit(request, pk):
    playermodel = get_object_or_404(player, pk=pk)
    if request.method == "POST":
        form = PlayerForm(request.POST, instance=playermodel)
        if form.is_valid():
            playermodel = form.save(commit=False)
            playermodel.save()
            return redirect('playerlist')
    else:
        form = PlayerForm(instance=playermodel)
    return render(request, 'mstlist/player_Edit.html', {'form': form})

#CSV出力
def player_export(request):
    responese = HttpResponse(content_type='text/csv')
    responese['Content-Disposition'] = 'attachment; filename="player.csv"'

    writer = csv.writer(responese)
    for playerModel in player.objects.all():
        writer.writerow([playerModel.pk, playerModel.age, playerModel.name, playerModel.position, playerModel.team])

    return responese

def player_pdf(request):

    LE_ID = 3
    LE_AGE = 3
    LE_NAME = 20
    LE_POSITION = 12
    LE_TEAM = 8

    response = HttpResponse(content_type='application/pdf')
    pdf_name = 'playerlist.pdf'
    response['Content-Disposition'] = 'filename=' + pdf_name

    #デプロイするときはこっち
    font_url = r'/home/sakai/sakai.pythonanywhere.com/mstlist/static/fonts/MSMincho/msmincho.ttc'

    #localhostはこっち
    # font_url = r'./mstlist/static/fonts/MSMincho/msmincho.ttc'

    pdfmetrics.registerFont(TTFont("msmincho", font_url))

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
    for playerModel in player.objects.all():

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

            print_str = settext("ID", LE_ID, 2) + settext("年齢", LE_AGE, 2) + settext("名前", LE_NAME) + settext("ポジション", LE_POSITION) + settext("チーム", LE_TEAM)
            # print_str = "ID&nbsp;名前&nbsp;&nbsp;&nbsp;グループ&nbsp;権限"
            para = Paragraph(print_str, style2)
            flowables.append(para)

            #次のフレームへ
            flowables.append(FrameBreak())

        detail_str = settext(playerModel.id, LE_ID, 2)
        detail_str += settext(playerModel.age, LE_AGE, 2)
        detail_str += settext(playerModel.name, LE_NAME)
        detail_str += settext(playerModel.position, LE_POSITION)
        detail_str += settext(playerModel.team, LE_TEAM)
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






#削除
def member_remove(request, pk):
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    return redirect('update_sample')
