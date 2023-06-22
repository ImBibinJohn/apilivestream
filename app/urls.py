from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index,name='index'),
    path('save_form/', views.save_form, name='save_form'),
    path('redirection/', views.redirection, name='redirection'),
    path('show_video/', views.show_video, name='show_video'),
    path('extract_rtmp_data/', views.extract_rtmp_data, name='extract_rtmp_data'),


]

