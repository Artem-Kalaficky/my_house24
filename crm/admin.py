from django.contrib import admin

from users.models import Role
from .models import Item


admin.site.register(Role)
admin.site.register(Item)
