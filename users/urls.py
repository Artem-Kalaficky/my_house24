from django.urls import path

from .views import AdminLoginView, OwnerLoginView


urlpatterns = [
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('cabinet/login/', OwnerLoginView.as_view(), name='owner_login'),
]
