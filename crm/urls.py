from django.urls import path

from .views import StatisticsTemplateView, RoleFormView


urlpatterns = [
    # statistics
    path('', StatisticsTemplateView.as_view(), name='home'),
    path('system-settings/roles', RoleFormView.as_view(), name='roles'),
]
