import sched
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView

from mstlist.forms import ScheduleForm, PlayerForm, SagyoForm

from .models import Member, player, Schedule, Sagyo

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
    return render(request, 'mstlist/schedule_edit.html', {'form': form})

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

#削除
def member_remove(request, pk):
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    return redirect('update_sample')
