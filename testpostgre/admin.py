from tokenize import group
from django.contrib import admin
from .models import Group
from .models import Member

admin.site.register(Group)
admin.site.register(Member)