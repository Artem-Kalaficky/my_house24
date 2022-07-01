from django.urls import path

from .views import SummaryTemplateView


urlpatterns = [
    # summary
    path('', SummaryTemplateView.as_view(), name='cabinet'),
]
