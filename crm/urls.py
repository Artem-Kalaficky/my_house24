from django.urls import path

from .views import StatisticsTemplateView, RoleCreateView, UsersListView, UserDetailView, UserCreateView,\
    UserUpdateView, UserDeleteView, ItemsListView, ItemCreateView, ItemUpdateView, ItemDeleteView, RequisiteUpdate, \
    ServiceCreateView, TariffsListView, TariffDetailView, TariffCreateView, TariffDeleteView, TariffUpdateView, \
    MainUpdateView, AboutUpdateView, PhotoDeleteView, ServicePageUpdateView, ContactPageUpdateView


urlpatterns = [
    # statistics page
    path('', StatisticsTemplateView.as_view(), name='home'),


    # SITE-MANAGEMENT pages
    path('site-management/main/', MainUpdateView.as_view(), name='main'),
    path('site-management/about/photo/delete/<int:pk>/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('site-management/about/', AboutUpdateView.as_view(), name='about'),
    path('site-management/about_services/', ServicePageUpdateView.as_view(), name='about_service'),
    path('site-management/contacts/', ContactPageUpdateView.as_view(), name='contact'),

    # SYSTEM-SETTINGS pages
    # services
    path('system-settings/services/', ServiceCreateView.as_view(), name='services'),

    # tariffs
    path('system-settings/tariffs/delete/<int:pk>/', TariffDeleteView.as_view(), name='tariff_delete'),
    path('system-settings/tariffs/update/<int:pk>/', TariffUpdateView.as_view(), name='tariff_update'),
    path('system-settings/tariffs/<int:pk>/', TariffDetailView.as_view(), name='tariff_detail'),
    path('system-settings/tariffs/create/', TariffCreateView.as_view(), name='tariff_create'),
    path('system-settings/tariffs/', TariffsListView.as_view(), name='tariffs_list'),

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
