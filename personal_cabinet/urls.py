from django.urls import path

from .views import (
    SummaryTemplateView, ProfileListView, ProfileUpdateView
)


urlpatterns = [
    # summary
    path('', SummaryTemplateView.as_view(), name='cabinet'),

    # profile
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='owner_profile_update'),
    path('profile/', ProfileListView.as_view(), name='owner_profile')
]
