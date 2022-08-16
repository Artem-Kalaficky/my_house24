from django.urls import path

from crm.views import delete_selected_messages
from .views import (
    OwnerApartmentDetailView, ProfileListView, ProfileUpdateView, OwnerApplicationsListView, OwnerApplicationCreateView,
    OwnerApplicationDeleteView, OwnerMessagesListView, OwnerMessageDetailView, OwnerMessageDeleteView,
    OwnerInvoicesListView,
)


urlpatterns = [
    # summary
    path('apartment/<int:pk>/', OwnerApartmentDetailView.as_view(), name='owner_apartment_detail'),

    # invoices
    path('invoices/', OwnerInvoicesListView.as_view(), name='owner_invoices_list'),

    # messages
    path('messages/<int:pk>/delete/', OwnerMessageDeleteView.as_view(), name='owner_message_delete'),
    path('messages/<int:pk>/', OwnerMessageDetailView.as_view(), name='owner_message_detail'),
    path('messages/', OwnerMessagesListView.as_view(), name='owner_messages_list'),
    path('delete-messages-ajax/', delete_selected_messages, name='delete_selected_messages'),

    # applications
    path('applications/<int:pk>/delete/', OwnerApplicationDeleteView.as_view(), name='owner_application_delete'),
    path('applications/create/', OwnerApplicationCreateView.as_view(), name='owner_application_create'),
    path('applications/', OwnerApplicationsListView.as_view(), name='owner_applications_list'),

    # profile
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='owner_profile_update'),
    path('profile/', ProfileListView.as_view(), name='owner_profile')
]
