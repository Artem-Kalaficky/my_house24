from django.contrib import admin

from users.models import Role
from .models import Item, Requisites, Unit, Service, Tariff, ServiceForTariff


admin.site.register(Role)
admin.site.register(Item)
admin.site.register(Requisites)
admin.site.register(Unit)
admin.site.register(Service)
admin.site.register(Tariff)
admin.site.register(ServiceForTariff)




