from django.urls import path

from .views import AdminLoginView, OwnerLoginView, UserLogoutView, RegisterUserView, RegisterDoneView, user_activate


urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('cabinet/login/', OwnerLoginView.as_view(), name='owner_login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout')
]
