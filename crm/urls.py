from django.urls import path

from .views import (
    StatisticsTemplateView, RoleCreateView, UsersListView, UserDetailView, UserCreateView,
    UserUpdateView, UserDeleteView, ItemsListView, ItemCreateView, ItemUpdateView, ItemDeleteView, RequisiteUpdate,
    ServiceCreateView, TariffsListView, TariffDetailView, TariffCreateView, TariffDeleteView, TariffUpdateView,
    MainUpdateView, AboutUpdateView, PhotoDeleteView, ServicePageUpdateView, ContactPageUpdateView, get_units,
    HousesListView, HouseDetailView, HouseCreateView, HouseDeleteView, get_role, HouseUpdateView, OwnersListView,
    OwnerDetailView, OwnerCreateView, OwnerDeleteView, OwnerUpdateView, OwnerInviteView, ApartmentsListView,
    ApartmentDetailView, ApartmentCreateView, ApartmentDeleteView, get_section_and_floor
)


urlpatterns = [
    # statistics page
    path('', StatisticsTemplateView.as_view(), name='home'),

    # apartments
    path('apartments/delete/<int:pk>/', ApartmentDeleteView.as_view(), name='apartment_delete'),
    path('apartments/<int:pk>/', ApartmentDetailView.as_view(), name='apartment_detail'),
    path('apartments/create/', ApartmentCreateView.as_view(), name='apartment_create'),
    path('apartments/', ApartmentsListView.as_view(), name='apartments_list'),
    path('get-section-and-floor/', get_section_and_floor, name='get_section_and_floor'),

    # owners
    path('owners/delete/<int:pk>/', OwnerDeleteView.as_view(), name='owner_delete'),
    path('owners/update/<int:pk>/', OwnerUpdateView.as_view(), name='owner_update'),
    path('owners/<int:pk>/', OwnerDetailView.as_view(), name='owner_detail'),
    path('owners/invite/', OwnerInviteView.as_view(), name='owner_invite'),
    path('owners/create/', OwnerCreateView.as_view(), name='owner_create'),
    path('owners/', OwnersListView.as_view(), name='owners_list'),

    # houses
    path('houses/delete/<int:pk>/', HouseDeleteView.as_view(), name='house_delete'),
    path('houses/update/<int:pk>/', HouseUpdateView.as_view(), name='house_update'),
    path('houses/<int:pk>/', HouseDetailView.as_view(), name='house_detail'),
    path('houses/create/', HouseCreateView.as_view(), name='house_create'),
    path('houses/', HousesListView.as_view(), name='houses_list'),
    path('get-role/', get_role, name='get_role'),

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
    path('get-units/', get_units, name='get_units'),

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
