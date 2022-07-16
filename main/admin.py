from django.contrib import admin

from .models import MainPage, Seo, Photo, Block, AboutPage, Document


admin.site.register(MainPage)
admin.site.register(Block)
admin.site.register(AboutPage)
admin.site.register(Photo)
admin.site.register(Document)
admin.site.register(Seo)

