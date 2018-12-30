from django.urls import path
from . import views

urlpatterns = [
    path('telegram', views.create, name='telegram'),
    path('telegram-webhook', views.callback, name='telegram-webhook'),
    path('notifications/update', views.notification_update, name='notification-update'),
]
