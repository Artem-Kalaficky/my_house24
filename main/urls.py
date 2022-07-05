from django.urls import path

from .views import MainTemplateView


urlpatterns = [
    path('', MainTemplateView.as_view(), name='main'),
]
