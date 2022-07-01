from django.urls import path

from .views import StatisticsTemplateView


urlpatterns = [
    # statistics
    path('', StatisticsTemplateView.as_view(), name='home'),
]
