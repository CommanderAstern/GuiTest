from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('select', views.select, name='select'),
    path('scan', views.scan, name='scan'),
    path('battery', views.battery, name='battery'),
    path('batteries', views.batteries, name='batteries'),
]
