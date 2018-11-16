from django.urls import path

from . import views

urlpatterns = [
    path('artists', views.index, name='index'),
]
