from django.urls import path
from . import views

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('poll/<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('vote/<int:poll_id>/', views.vote, name='vote'),
    path('result/<int:poll_id>/', views.result, name='result'),
    path('login/', views.user_login, name='login'),
]
