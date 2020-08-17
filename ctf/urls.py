from django.urls import path

from . import views

app_name = 'ctf'
urlpatterns = [
    path('', views.flag_list, name='index'),
]