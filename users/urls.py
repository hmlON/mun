from django.urls import path
from . import views

urlpatterns = [
    path('user/delete', views.delete, name='delete'),
]
