from django.urls import path
from . import views

urlpatterns = [
    path('telegram', views.create, name='telegram'),
    path('telegram-webhook', views.callback, name='telegram-webhook'),
]
