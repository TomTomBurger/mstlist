from django import forms

from .models import Schedule, player, Sagyo

class PlayerForm(forms.ModelForm):

    class Meta:
        model = player
        fields = ('age', 'name','position','team',)

class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ('cd', 'sagyoCd','yDate',)

class SagyoForm(forms.ModelForm):

    class Meta:
        model = Sagyo
        fields = ('cd', 'name',)