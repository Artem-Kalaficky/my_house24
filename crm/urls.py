from django.urls import path

from .views import StatisticsTemplateView, RoleCreateView, UsersListView, UserDetailView, UserCreateView


urlpatterns = [
    # statistics page
    path('', StatisticsTemplateView.as_view(), name='home'),


    # SYSTEM-SETTINGS page
    path('system-settings/roles/', RoleCreateView.as_view(), name='roles'),

    # users
    path('system-settings/users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('system-settings/users/create/', UserCreateView.as_view(), name='user_create'),
    path('system-settings/users/', UsersListView.as_view(), name='users_list'),

]
