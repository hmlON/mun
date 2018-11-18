from django.urls import path
from . import views

urlpatterns = [
    path('releases', views.index, name='index'),
]
