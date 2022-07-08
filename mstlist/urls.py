from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('sagyolist', views.sagyo_list, name='sagyolist'),
    path('sagyolist/new/', views.sagyo_new, name='sagyo_new'),
    path('sagyolist/<int:pk>/edit/', views.sagyo_edit, name='sagyo_edit'),
    path('sagyolist/<int:pk>/remove/', views.sagyo_remove, name='sagyo_remove'),

    path('playerlist', views.MemberList.as_view(), name='playerlist'),
    path('playerlist/new/', views.player_new, name='player_new'),
    path('playerlist/<int:pk>/edit/', views.player_edit, name='player_edit'),

    path('playerlist/export', views.player_export, name='player_export'),
    path('playerlist/pdf', views.player_pdf, name='player_pdf'),

    path('schedule', views.schedule, name='schedule'),
    path('schedule/new/', views.schedule_new, name='schedule_new'),
    path('schedule/<int:pk>/edit/', views.schedule_edit, name='schedule_edit'),
    path('schedule/<int:pk>/remove/', views.schedule_remove, name='schedule_remove'),
]
