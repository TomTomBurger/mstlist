from django.urls import path
from . import views

urlpatterns = [
    # path('', views.ListView.as_view(), name='update_sample'),
    path('', views.ListUpdateView.as_view(), name='update_sample'),
    path('member/<str:pk>/remove/', views.member_remove, name='member_remove'),
    path('member/export', views.member_export, name='member_export'),
    path('member/pdf', views.member_pdf, name='member_pdf'),
]
