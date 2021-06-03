from django.contrib import admin

from apps.user.models.user import User
from apps.user.models.auth import Auth

admin.site.register(User)
admin.site.register(Auth)
