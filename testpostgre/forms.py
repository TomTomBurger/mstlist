from django import forms
from django.db import models
from django.forms import ModelForm
from .models import Member, Group

# nameをlabelにするModelChoiceField
class ModelNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name

class MemberUpdateForm(ModelForm):
    class Meta:
        model = Member
        fields = ('full_name', 'group', 'auth')

    group = ModelNameChoiceField(Group.objects)