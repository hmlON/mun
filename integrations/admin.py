from django.contrib import admin
from .models import Integration, Artist, Release

admin.site.register(Integration)
admin.site.register(Artist)
admin.site.register(Release)
