from os import scandir
from django.contrib import admin
from .models import Group
from .models import Member
from .models import player
from .models import Septictank
from .models import Schedule
from .models import Sagyo

admin.site.register(Group)
admin.site.register(Member)
admin.site.register(player)
admin.site.register(Septictank)
admin.site.register(Schedule)
admin.site.register(Sagyo)