from django.urls import path
from . import views

urlpatterns = [
    path('releases', views.index, name='index'),
    path('artists/<name>', views.artist, name='artist'),
    path('settings', views.settings, name='settings'),
]
