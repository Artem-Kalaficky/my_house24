from django.contrib import admin

from .models import MainPage, Seo, Photo, Block


admin.site.register(MainPage)
admin.site.register(Block)
admin.site.register(Photo)
admin.site.register(Seo)

