from django.urls import path

from .views import (
    StatisticsTemplateView, RoleCreateView, UsersListView, UserDetailView, UserCreateView,
    UserUpdateView, UserDeleteView, ItemsListView, ItemCreateView, ItemUpdateView, ItemDeleteView, RequisiteUpdate,
    ServiceCreateView, TariffsListView, TariffDetailView, TariffCreateView, TariffDeleteView, TariffUpdateView,
    MainUpdateView, AboutUpdateView, PhotoDeleteView, ServicePageUpdateView, ContactPageUpdateView, get_units,
    HousesListView, HouseDetailView, HouseCreateView, HouseDeleteView, get_role, HouseUpdateView, OwnersListView,
    OwnerDetailView, OwnerCreateView, OwnerDeleteView, OwnerUpdateView, OwnerInviteView, ApartmentsListView,
    ApartmentDetailView, ApartmentCreateView, ApartmentUpdateView, ApartmentDeleteView, get_section_and_floor,
    PersonalAccountsListView, PersonalAccountDetailView, PersonalAccountCreateView, PersonalAccountDeleteView,
    get_apartment_in_p_a, PersonalAccountUpdateView, MeterReadingsListView, MeterReadingsByApartmentListView,
    MeterReadingDetailView, MeterReadingCreateView, get_apartment_in_m_r, MeterReadingDeleteView,
    MeterReadingUpdateView, ApplicationsListView, ApplicationDetailView, ApplicationCreateView, ApplicationDeleteView,
    get_apartment_by_owner, ApplicationUpdateView, MessagesListView, MessageDetailView, MessageCreateView,
    MessageDeleteView, select_recipients_for_send_message, delete_selected_messages, TransactionsListView,
    TransactionDetailView, TransactionCreateView, create_transaction, TransactionDeleteView, TransactionUpdateView,
    InvoicesListView, InvoiceDetailView, InvoiceCreateView, work_with_invoice, InvoiceDeleteView,
    delete_selected_invoices, InvoiceUpdateView
)


urlpatterns = [
    # statistics page
    path('', StatisticsTemplateView.as_view(), name='home'),

    # transactions
    path('transactions/delete/<int:pk>/', TransactionDeleteView.as_view(), name='transaction_delete'),
    path('transactions/update/<int:pk>/', TransactionUpdateView.as_view(), name='transaction_update'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
    path('transactions/create/', TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/', TransactionsListView.as_view(), name='transactions_list'),
    path('create-transaction-ajax/', create_transaction, name='create_transaction'),

    # invoices
    path('invoices/delete/<int:pk>/', InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('invoices/update/<int:pk>/', InvoiceUpdateView.as_view(), name='invoice_update'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoices/', InvoicesListView.as_view(), name='invoices_list'),
    path('invoices-ajax/', work_with_invoice, name='work_with_invoice'),
    path('invoices-delete-ajax/', delete_selected_invoices, name='delete_selected_invoices'),

    # personal_accounts
    path('personal-accounts/delete/<int:pk>/', PersonalAccountDeleteView.as_view(), name='personal_account_delete'),
    path('personal-accounts/update/<int:pk>/', PersonalAccountUpdateView.as_view(), name='personal_account_update'),
    path('personal-accounts/<int:pk>/', PersonalAccountDetailView.as_view(), name='personal_account_detail'),
    path('personal-accounts/create/', PersonalAccountCreateView.as_view(), name='personal_account_create'),
    path('personal-accounts/', PersonalAccountsListView.as_view(), name='personal_accounts_list'),
    path('get-apartment-in-p_a/', get_apartment_in_p_a, name='get_apartment_in_p_a'),

    # apartments
    path('apartments/delete/<int:pk>/', ApartmentDeleteView.as_view(), name='apartment_delete'),
    path('apartments/update/<int:pk>/', ApartmentUpdateView.as_view(), name='apartment_update'),
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

    # messages
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/', MessagesListView.as_view(), name='messages_list'),
    path('send-messages-ajax/', select_recipients_for_send_message, name='select_recipients_for_send_message'),
    path('delete-messages-ajax/', delete_selected_messages, name='delete_selected_messages'),

    # applications
    path('applications/delete/<int:pk>/', ApplicationDeleteView.as_view(), name='application_delete'),
    path('applications/update/<int:pk>/', ApplicationUpdateView.as_view(), name='application_update'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/create/', ApplicationCreateView.as_view(), name='application_create'),
    path('applications/', ApplicationsListView.as_view(), name='applications_list'),
    path('get-apartment-by-owner/', get_apartment_by_owner, name='get_apartment_by_owner'),

    # meter-readings
    path('meter-readings/delete/<int:pk>/', MeterReadingDeleteView.as_view(), name='meter_reading_delete'),
    path('meter-readings/update/<int:pk>/', MeterReadingUpdateView.as_view(), name='meter_reading_update'),
    path('meter-readings/<int:pk>/', MeterReadingDetailView.as_view(), name='meter_reading_detail'),
    path('meter-readings/create/', MeterReadingCreateView.as_view(), name='meter_reading_create'),
    path('meter-readings/by/', MeterReadingsByApartmentListView.as_view(), name='meter_readings_by_apartment_list'),
    path('meter-readings/', MeterReadingsListView.as_view(), name='meter_readings_list'),
    path('get-apartment-in-m_r/', get_apartment_in_m_r, name='get_apartment_in_m_r'),

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
