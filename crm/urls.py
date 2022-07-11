from django.urls import path

from .views import StatisticsTemplateView, RoleCreateView, UsersListView, UserDetailView, UserCreateView,\
    UserUpdateView, UserDeleteView, ItemsListView, ItemCreateView, ItemUpdateView, ItemDeleteView, RequisiteUpdate, \
    ServiceCreateView


urlpatterns = [
    # statistics page
    path('', StatisticsTemplateView.as_view(), name='home'),


    # SYSTEM-SETTINGS page
    # services
    path('system-settings/services/', ServiceCreateView.as_view(), name='services'),

    # roles
    path('system-settings/roles/', RoleCreateView.as_view(), name='roles'),

    # users
    path('system-settings/users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('system-settings/users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('system-settings/users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('system-settings/users/create/', UserCreateView.as_view(), name='user_create'),
    path('system-settings/users/', UsersListView.as_view(), name='users_list'),

    # requisites
    path('system-settings/requisites/<int:pk>/', RequisiteUpdate.as_view(), name='requisites'),

    # items
    path('system-settings/items/delete/<int:pk>/', ItemDeleteView.as_view(), name='item_delete'),
    path('system-settings/items/update/<int:pk>/', ItemUpdateView.as_view(), name='item_update'),
    path('system-settings/items/create/', ItemCreateView.as_view(), name='item_create'),
    path('system-settings/items/', ItemsListView.as_view(), name='items_list'),
]
