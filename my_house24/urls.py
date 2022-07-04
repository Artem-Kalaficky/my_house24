from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('crm/', include('crm.urls')),
    path('cabinet/', include('personal_cabinet.urls')),
    path('', include('users.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('old-admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
