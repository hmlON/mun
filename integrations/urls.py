from django.urls import path
from . import views

urlpatterns = [
    path('latest', views.latest, name='latest'),
    path('releases', views.releases, name='releases'),
    path('artists/<name>', views.artist, name='artist'),
    path('settings', views.settings, name='settings'),
    path('admin/dashboard', views.admin_dashboard, name='dashboard')
]
