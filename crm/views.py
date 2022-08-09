import datetime
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
from django.db.models import Q, Sum
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from users.tasks import send_invite_letter
from .models import Item, Requisites, Service, Unit, Tariff, ServiceForTariff, House, Section, Floor, Apartment, \
    PersonalAccount, MeterReading, Application, Message, Transaction, Invoice, ServiceForInvoice
from main.models import MainPage, Block, AboutPage, Photo, Document, ServicePage, AboutService, ContactPage
from users.models import UserProfile, Role
from .forms import RoleFormSet, ItemForm, RequisiteForm, ServiceFormSet, UnitFormSet, ServiceForTariffFormSet, \
    TariffForm, ServiceForTariffForm, MainPageForm, SeoForm, BlockFormSet, AboutPageForm, PhotoForm, DocumentFormSet, \
    ServicePageForm, AboutServiceFormSet, ContactPageForm, SectionFormSet, FloorFormSet, UserFormSet, HouseForm, \
    OwnerCreateForm, OwnerUpdateForm, InviteForm, ApartmentForm, PersonalAccountForm, MeterReadingForm, \
    MeterReadingUpdateForm, ApplicationForm, MessageForm, TransactionForm, InvoiceForm, ServiceForInvoiceFormSet, \
    ServiceForInvoiceForm
from users.forms import UserCreateForm, ChangeUserInfoForm
from .serializers import my_serialize


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/admin/login/'

    def test_func(self):
        return self.request.user.is_staff


class StatisticsTemplateView(StaffRequiredMixin, TemplateView):
    template_name = 'crm/pages/statistics.html'


# region Transactions
class TransactionsListView(StaffRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'crm/pages/transactions/transactions_list.html'
    context_object_name = 'transactions'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.all()
        context['owners'] = UserProfile.objects.filter(is_staff=False)
        context['personal_accounts'] = PersonalAccount.objects.filter(status='active')
        context['income'] = self.get_queryset().aggregate(sum=Sum('amount', filter=Q(completed=True,
                                                                                     amount__gte=0)))['sum']
        expense = self.get_queryset().aggregate(sum=Sum('amount', filter=Q(completed=True, amount__lt=0)))['sum']
        context['expense'] = abs(expense) if expense else None
        context['balance'] = PersonalAccount.objects.aggregate(sum=Sum('balance', filter=Q(status='active',
                                                                                           balance__gte=0)))['sum']
        debt_balance = PersonalAccount.objects.aggregate(sum=Sum('balance', filter=Q(status='active',
                                                                                     balance__lt=0)))['sum']
        context['debt_balance'] = abs(debt_balance) if debt_balance else None
        context['cashbox'] = Transaction.objects.aggregate(sum=Sum('amount', filter=Q(completed=True)))['sum']
        return context

    def get_queryset(self):
        queryset = Transaction.objects.select_related('item', 'owner', 'personal_account').all()
        if self.request.GET.get('number'):
            queryset = queryset.filter(number__contains=self.request.GET.get('number'))
        if self.request.GET.get('input_date'):
            input_date = self.request.GET.get('input_date').split(' - ')
            date_range = [datetime.datetime.strptime(x, '%d.%m.%Y').strftime('%Y-%m-%d') for x in input_date]
            queryset = queryset.filter(date__range=date_range)
        if self.request.GET.get('filter-date') == '1':
            queryset = queryset.order_by('date')
        if self.request.GET.get('filter-date') == '0':
            queryset = queryset.order_by('-date')
        if self.request.GET.get('status'):
            queryset = queryset.filter(completed=(True if self.request.GET.get('status') == 'yes' else False))
        if self.request.GET.get('type'):
            queryset = queryset.filter(item=self.request.GET.get('type'))
        if self.request.GET.get('owner'):
            queryset = queryset.filter(owner=self.request.GET.get('owner'))
        if self.request.GET.get('personal_account'):
            queryset = queryset.filter(
                personal_account__personal_number__contains=self.request.GET.get('personal_account'))
        if self.request.GET.get('income'):
            queryset = queryset.filter(is_income=(True if self.request.GET.get('income') == 'true' else False))
        return queryset


class TransactionDetailView(StaffRequiredMixin, DetailView):
    queryset = Transaction.objects.select_related('item', 'owner', 'personal_account', 'manager')
    template_name = 'crm/pages/transactions/transaction_detail.html'


class TransactionCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/transactions/transaction_create.html'
    success_url = reverse_lazy('transactions_list')
    success_message = 'Ведомость успешно создана!'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['income_items'] = Item.objects.filter(income_expense='income')
        context['expense_items'] = Item.objects.filter(income_expense='expense')
        context['cashbox'] = int(Transaction.objects.aggregate(sum=Sum('amount', filter=Q(completed=True)))['sum'])
        return context

    def get_form(self, form_class=None):
        if self.request.GET.get('type') == 'income':
            form_class = TransactionForm(self.request.POST or None)
            if self.request.GET.get('personal_account_id'):
                personal_account = get_object_or_404(PersonalAccount, pk=self.request.GET.get('personal_account_id'))
                owner = personal_account.apartment.owner.id if (personal_account.apartment and
                                                                personal_account.apartment.owner) else None
                form_class = TransactionForm(self.request.POST or None,
                                             initial={'personal_account': personal_account.id,
                                                      'owner': owner})
            if self.request.GET.get('transaction_id'):
                transaction = get_object_or_404(Transaction, pk=self.request.GET.get('transaction_id'))
                owner_id = transaction.owner_id if transaction.owner else None
                personal_account = transaction.personal_account_id if transaction.personal_account else None
                manager_id = transaction.manager_id if transaction.manager else None
                item_id = transaction.item_id if transaction.item else None
                form_class = TransactionForm(self.request.POST or None, initial={'item': item_id,
                                                                                 'completed': transaction.completed,
                                                                                 'owner': owner_id,
                                                                                 'personal_account': personal_account,
                                                                                 'amount': transaction.amount,
                                                                                 'manager': manager_id,
                                                                                 'comment': transaction.comment})
        if self.request.GET.get('type') == 'expense':
            form_class = TransactionForm(self.request.POST or None, initial={'is_income': False})
            if self.request.GET.get('transaction_id'):
                transaction = get_object_or_404(Transaction, pk=self.request.GET.get('transaction_id'))
                manager_id = transaction.manager_id if transaction.manager else None
                item_id = transaction.item_id if transaction.item else None
                form_class = TransactionForm(self.request.POST or None, initial={'item': item_id,
                                                                                 'completed': transaction.completed,
                                                                                 'is_income': False,
                                                                                 'amount': abs(transaction.amount),
                                                                                 'manager': manager_id,
                                                                                 'comment': transaction.comment})
        return form_class

    def form_valid(self, form):
        if self.request.GET.get('type') == 'expense':
            transaction = form.save(commit=False)
            transaction.amount = -transaction.amount
            transaction.save()
        else:
            transaction = form.save(commit=False)
            if transaction.personal_account:
                personal_account = get_object_or_404(PersonalAccount, pk=transaction.personal_account.id)
                personal_account.balance += transaction.amount
                personal_account.save()
                transaction.save()
        return super().form_valid(form)


class TransactionUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    queryset = Transaction.objects.select_related('item', 'owner', 'manager', 'personal_account')
    template_name = 'crm/pages/transactions/transaction_update.html'
    success_url = reverse_lazy('transactions_list')
    success_message = 'Данные о ведомости обновлены!'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cashbox'] = int(Transaction.objects.aggregate(sum=Sum('amount', filter=Q(completed=True)))['sum'])
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = TransactionForm(self.request.POST or None, instance=self.object,
                                         initial={'date': self.object.date.strftime('%d.%m.%Y'),
                                                  'number': str(self.object.number).zfill(10),
                                                  'amount': abs(self.object.amount)})
        return form_class

    def form_valid(self, form):
        if self.request.GET.get('type') == 'expense':
            transaction = form.save(commit=False)
            transaction.amount = -transaction.amount
            transaction.save()
        else:
            transaction = form.save(commit=False)
            old_amount = get_object_or_404(Transaction, pk=transaction.id).amount
            if transaction.personal_account:
                personal_account = get_object_or_404(PersonalAccount, pk=transaction.personal_account.id)
                personal_account.balance = (personal_account.balance - old_amount) + transaction.amount
                personal_account.save()
                transaction.save()
        return super().form_valid(form)


class TransactionDeleteView(DeleteView):
    model = Transaction
    success_url = reverse_lazy('transactions_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.personal_account:
            personal_account = get_object_or_404(PersonalAccount, pk=self.object.personal_account.id)
            personal_account.balance -= self.object.amount
            personal_account.save()
        self.object.delete()
        return HttpResponseRedirect(success_url)


def create_transaction(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            personal_accounts = PersonalAccount.objects.filter(status='active').values('id', 'personal_number')
            response = {'personal_accounts': json.loads(json.dumps(list(personal_accounts), cls=DjangoJSONEncoder))}
            if request.GET.get('owner_id'):
                personal_accounts = PersonalAccount.objects.filter(status='active',
                                                                   apartment__owner__id=request.GET.get('owner_id'))
                p_a_json = json.loads(json.dumps(list(personal_accounts.values('id', 'personal_number')),
                                                 cls=DjangoJSONEncoder))
                response = {'personal_accounts': p_a_json}
            for d in response['personal_accounts']:
                d['personal_number'] = str(d['personal_number']).zfill(10)
            if request.GET.get('personal_account_id'):
                personal_account = PersonalAccount.objects.get(pk=request.GET.get('personal_account_id'))
                if personal_account.apartment and personal_account.apartment.owner:
                    response = {'owner': personal_account.apartment.owner.id}
                else:
                    response = {'owner': None}
            return JsonResponse(response, status=200)
# endregion Transactions


# region Invoices
class InvoicesListView(StaffRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'crm/pages/invoices/invoices_list.html'
    context_object_name = 'invoices'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owners'] = UserProfile.objects.filter(is_staff=False)
        context['apartments'] = Apartment.objects.select_related('section').all()
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        context['cashbox'] = Transaction.objects.aggregate(sum=Sum('amount', filter=Q(completed=True)))['sum']
        context['balance'] = PersonalAccount.objects.aggregate(sum=Sum('balance', filter=Q(status='active',
                                                                                           balance__gte=0)))['sum']
        debt_balance = PersonalAccount.objects.aggregate(sum=Sum('balance', filter=Q(status='active',
                                                                                     balance__lt=0)))['sum']
        context['debt_balance'] = abs(debt_balance) if debt_balance else None
        return context

    def get_queryset(self):
        queryset = Invoice.objects.select_related('apartment', 'apartment__owner', 'apartment__section').all()
        if self.request.GET.get('number'):
            queryset = queryset.filter(number__contains=self.request.GET.get('number'))
        if self.request.GET.get('status'):
            queryset = queryset.filter(status=self.request.GET.get('status'))
        if self.request.GET.get('input_date'):
            input_date = self.request.GET.get('input_date').split(' - ')
            date_range = [datetime.datetime.strptime(x, '%d.%m.%Y').strftime('%Y-%m-%d') for x in input_date]
            queryset = queryset.filter(date__range=date_range)
        if self.request.GET.get('filter-date') == '1':
            queryset = queryset.order_by('date')
        if self.request.GET.get('filter-date') == '0':
            queryset = queryset.order_by('-date')
        if self.request.GET.get('apartment'):
            queryset = queryset.filter(apartment__id=self.request.GET.get('apartment'))
        if self.request.GET.get('owner'):
            queryset = queryset.filter(apartment__owner__id=self.request.GET.get('owner'))
        if self.request.GET.get('is_held'):
            queryset = queryset.filter(is_held=True if self.request.GET.get('is_held') == 'true' else False)
        return queryset


class InvoiceDetailView(StaffRequiredMixin, DetailView):
    queryset = Invoice.objects.select_related('apartment', 'apartment__owner', 'apartment__section')
    template_name = 'crm/pages/invoices/invoice_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        context['services'] = ServiceForInvoice.objects.select_related('service',
                                                                       'service__unit').filter(invoice=self.object)
        return context


class InvoiceCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/invoices/invoice_create.html'
    success_url = reverse_lazy('invoices_list')
    success_message = 'Общая квитанция успешно создана!'
    id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meter_readings'] = MeterReading.objects.select_related('apartment', 'apartment__section',
                                                                        'meter', 'meter__unit').all()
        context['houses'] = House.objects.prefetch_related('sections').all()
        context['formset'] = ServiceForInvoiceFormSet(self.request.POST or None, prefix='formset',
                                                      queryset=ServiceForInvoice.objects.none())
        if self.request.GET.get('invoice_id'):
            services_for_invoice = ServiceForInvoice.objects.select_related('service', 'service__unit').filter(
                invoice_id=self.request.GET.get('invoice_id'))
            formset = modelformset_factory(ServiceForInvoice, form=ServiceForInvoiceForm, can_delete=True,
                                           extra=len(services_for_invoice))
            context['formset'] = formset(self.request.POST or None, queryset=ServiceForInvoice.objects.none(),
                                         prefix='formset', initial=[{'service': x.service,
                                                                     'cost_for_unit': x.cost_for_unit,
                                                                     'expense': x.expense,
                                                                     'unit': x.service.unit.id,
                                                                     'full_cost': x.full_cost}
                                                                    for x in services_for_invoice])
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = InvoiceForm(self.request.POST or None)
            if self.request.GET.get('personal_account_id'):
                p_a = get_object_or_404(PersonalAccount, pk=self.request.GET.get('personal_account_id')).personal_number
                form_class = InvoiceForm(self.request.POST or None, initial={'personal_account': str(p_a).zfill(10)})
            if self.request.GET.get('invoice_id'):
                largest = Invoice.objects.all().order_by('number').last()
                invoice = get_object_or_404(Invoice, pk=self.request.GET.get('invoice_id'))
                personal_account = str(invoice.apartment.personal_account.personal_number).zfill(10)
                form_class = InvoiceForm(self.request.POST or None,
                                         initial={'personal_account': personal_account,
                                                  'number': str(largest.number + 1).zfill(10),
                                                  'status': invoice.status,
                                                  'is_held': invoice.is_held,
                                                  'date': invoice.date.strftime('%d.%m.%Y'),
                                                  'date_with': invoice.date_with.strftime('%d.%m.%Y'),
                                                  'date_before': invoice.date_before.strftime('%d.%m.%Y')})
        return form_class

    def form_valid(self, form):
        invoice = form.save()
        self.id = invoice.id
        formset = self.get_context_data()['formset']
        for obj in formset:
            if obj.is_valid():
                service_for_invoice = obj.save(commit=False)
                if obj.cleaned_data and not obj.cleaned_data['DELETE']:
                    service_for_invoice.invoice = invoice
                    try:
                        service_for_invoice.save()
                    except IntegrityError:
                        pass
        return super().form_valid(form)

    def get_success_url(self):
        ready_invoice = get_object_or_404(Invoice, pk=self.id)
        amount = ServiceForInvoice.objects.aggregate(sum=Sum('full_cost', filter=Q(invoice=ready_invoice)))['sum']
        ready_invoice.amount = ready_invoice.amount + amount
        ready_invoice.save()
        if ready_invoice.is_held and (ready_invoice.status == 'unpaid' or ready_invoice.status == 'p_paid'):
            personal_account = get_object_or_404(PersonalAccount, apartment=ready_invoice.apartment)
            personal_account.balance = personal_account.balance - ready_invoice.amount
            personal_account.save()
        return self.success_url


class InvoiceUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    queryset = Invoice.objects.select_related('apartment')
    template_name = 'crm/pages/invoices/invoice_update.html'
    success_url = reverse_lazy('invoices_list')
    success_message = 'Данные о квитанции обновлены!'
    is_held = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = ServiceForInvoice.objects.select_related('service', 'service__unit').filter(invoice=self.object)
        context['formset'] = ServiceForInvoiceFormSet(self.request.POST or None, queryset=queryset, prefix='formset')
        self.is_held.append(True if self.object.is_held else False)
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = InvoiceForm(self.request.POST or None, instance=self.object,
                                     initial={'number': str(self.object.number).zfill(10),
                                              'date': self.object.date.strftime('%d.%m.%Y'),
                                              'date_with': self.object.date_with.strftime('%d.%m.%Y'),
                                              'date_before': self.object.date_before.strftime('%d.%m.%Y'),
                                              'personal_account': str(self.object.apartment.personal_account.personal_number).zfill(10)})
        return form_class

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        form.save()
        if formset.is_valid():
            for obj in formset:
                if obj.cleaned_data and not obj.cleaned_data['DELETE']:
                    obj.instance.invoice = form.instance
                    try:
                        obj.save()
                    except IntegrityError:
                        pass
        return super().form_valid(form)

    def get_success_url(self):
        print(self.is_held)
        invoice = get_object_or_404(Invoice, pk=self.object.id)
        amount = ServiceForInvoice.objects.aggregate(sum=Sum('full_cost', filter=Q(invoice=invoice)))['sum']
        old_amount = invoice.amount
        invoice.amount = amount
        invoice.save()
        print(self.is_held)
        if invoice.status == 'unpaid' or invoice.status == 'p_paid':
            personal_account = get_object_or_404(PersonalAccount, apartment=invoice.apartment)
            print(self.is_held[-1], invoice.is_held)
            if self.is_held[-1] != invoice.is_held:
                print('в смысле?')
                if invoice.is_held:
                    personal_account.balance = personal_account.balance - invoice.amount
                else:
                    personal_account.balance = personal_account.balance + invoice.amount
            else:
                personal_account.balance = (personal_account.balance + old_amount) - invoice.amount
            personal_account.save()
        return self.success_url







class InvoiceDeleteView(DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoices_list')


def delete_selected_invoices(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            if request.GET.get('idx'):
                idx = [int(x) for x in request.GET.get('idx').split(' ')[:-1]]
                Invoice.objects.filter(pk__in=idx).delete()
                messages.add_message(request, messages.SUCCESS, 'Выбранные квитанции успешно удалены!')
            return JsonResponse({}, status=200)


def work_with_invoice(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            response = {}
            houses = House.objects.prefetch_related('sections').all()
            meter_readings = MeterReading.objects.select_related('apartment', 'apartment__section', 'meter',
                                                                 'meter__unit').all()
            if request.GET.get('house_id'):
                sections = get_object_or_404(House, pk=request.GET.get('house_id')).sections.all().values('id', 'name')
                response = {'sections': json.loads(json.dumps(list(sections), cls=DjangoJSONEncoder))}
            if request.GET.get('section_id'):
                idx = []
                for x in Apartment.objects.select_related('personal_account').filter(
                        section_id=request.GET.get('section_id')):
                    try:
                        if x.personal_account.status == 'active':
                            idx.append(x.id)
                    except:
                        pass
                apartments = Apartment.objects.filter(pk__in=idx).values('id', 'number')
                response = {'apartments': json.loads(json.dumps(list(apartments), cls=DjangoJSONEncoder))}
            if request.GET.get('apartment_id'):
                apartment = get_object_or_404(Apartment, pk=request.GET.get('apartment_id'))
                meter_readings = meter_readings.filter(apartment_id=request.GET.get('apartment_id'))
                personal_account = apartment.personal_account.personal_number
                response = {'number': str(personal_account).zfill(10),
                            'owner': f'{apartment.owner.last_name} '
                                     f'{apartment.owner.first_name} '
                                     f'{apartment.owner.patronymic}' if apartment.owner else '(не задано)',
                            'telephone': apartment.owner.telephone if apartment.owner else '(не задано)',
                            'tariff': apartment.tariff.id if apartment.tariff else None}
            if request.GET.get('personal_number'):
                try:
                    personal_account = get_object_or_404(PersonalAccount,
                                                         personal_number=int(request.GET.get('personal_number')))
                    if personal_account.status == 'active':
                        house = [x for x in houses if personal_account.apartment.section in x.sections.all()][0]
                        sections = house.sections.all().values('id', 'name')
                        apartments = Apartment.objects.filter(pk=personal_account.apartment.id).values('id', 'number')
                        meter_readings = meter_readings.filter(apartment_id=personal_account.apartment.id)
                        response['house_id'] = house.id
                        response['sections'] = json.loads(json.dumps(list(sections), cls=DjangoJSONEncoder))
                        response['section_id'] = personal_account.apartment.section.id
                        response['apartments'] = json.loads(json.dumps(list(apartments), cls=DjangoJSONEncoder))
                        response['apartment_id'] = personal_account.apartment.id
                        response['tariff_id'] = personal_account.apartment.tariff.id \
                            if personal_account.apartment.tariff else None
                        response['owner'] = f'{personal_account.apartment.owner.last_name} ' \
                                            f'{personal_account.apartment.owner.first_name} ' \
                                            f'{personal_account.apartment.owner.patronymic}' \
                                            if personal_account.apartment.owner else '(не задано)'
                        response['telephone'] = personal_account.apartment.owner.telephone \
                            if personal_account.apartment.owner else '(не задано)'
                except:
                    pass
            response['meter_readings'] = my_serialize(meter_readings)
            if request.GET.get('tariff_id'):
                services = ServiceForTariff.objects.filter(tariff_id=request.GET.get('tariff_id'))
                response['count'] = len(services)
                response['services'] = json.loads(json.dumps(
                    list(services.values('service_id', 'service__unit_id', 'cost_for_unit')), cls=DjangoJSONEncoder))
            if request.GET.get('meters_by_apartment_id'):
                meter_readings = MeterReading.objects.filter(apartment_id=request.GET.get('meters_by_apartment_id'))
                response['meters'] = json.loads(json.dumps(
                    list(meter_readings.values('meter_id', 'expense')), cls=DjangoJSONEncoder))
            if request.GET.get('service_id'):
                response = {'unit_id': get_object_or_404(Service, pk=request.GET.get('service_id')).unit.id}
            return JsonResponse(response, status=200)
# endregion Invoices


# region PersonalAccounts
class PersonalAccountsListView(StaffRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'crm/pages/personal_accounts/personal_accounts_list.html'
    context_object_name = 'personal_accounts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        if self.request.GET.get('house'):
            for house in context['houses']:
                if house.id == int(self.request.GET.get('house')):
                    context['sections'] = house.sections.all()
        context['owners'] = UserProfile.objects.filter(is_staff=False)
        context['cashbox'] = Transaction.objects.aggregate(sum=Sum('amount', filter=Q(completed=True)))['sum']
        context['balance'] = PersonalAccount.objects.aggregate(sum=Sum('balance', filter=Q(status='active',
                                                                                           balance__gte=0)))['sum']
        debt_balance = PersonalAccount.objects.aggregate(sum=Sum('balance', filter=Q(status='active',
                                                                                     balance__lt=0)))['sum']
        context['debt_balance'] = abs(debt_balance) if debt_balance else None
        return context

    def get_queryset(self):
        queryset = PersonalAccount.objects.select_related('apartment', 'apartment__owner', 'apartment__section').all()
        if self.request.GET.get('number'):
            queryset = queryset.filter(personal_number__contains=self.request.GET.get('number'))
        if self.request.GET.get('status'):
            queryset = queryset.filter(status=self.request.GET.get('status'))
        if self.request.GET.get('apartment'):
            queryset = queryset.filter(apartment__number__contains=self.request.GET.get('apartment'))
        if self.request.GET.get('house'):
            sections = get_object_or_404(House, pk=self.request.GET.get('house')).sections.all()
            queryset = queryset.filter(apartment__section__in=sections)
        if self.request.GET.get('section'):
            queryset = queryset.filter(apartment__section__name=self.request.GET.get('section'))
        if self.request.GET.get('owner'):
            queryset = queryset.filter(apartment__owner_id=self.request.GET.get('owner'))
        if self.request.GET.get('debt'):
            if self.request.GET.get('debt') == 'yes':
                queryset = queryset.filter(balance__lt=0)
            else:
                queryset = queryset.filter(balance__gte=0)
        return queryset


class PersonalAccountDetailView(StaffRequiredMixin, DetailView):
    queryset = PersonalAccount.objects.select_related('apartment', 'apartment__owner', 'apartment__section')
    template_name = 'crm/pages/personal_accounts/personal_account_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        return context


class PersonalAccountCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = PersonalAccountForm
    template_name = 'crm/pages/personal_accounts/personal_account_create.html'
    success_url = reverse_lazy('personal_accounts_list')
    success_message = 'Лицевой счет успешно добавлен!'


class PersonalAccountUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PersonalAccount
    form_class = PersonalAccountForm
    template_name = 'crm/pages/personal_accounts/personal_account_update.html'
    success_url = reverse_lazy('personal_accounts_list')
    success_message = 'Данные о лицевом счете обновлены!'


class PersonalAccountDeleteView(SuccessMessageMixin, DeleteView):
    model = PersonalAccount
    success_url = reverse_lazy('personal_accounts_list')
    success_message = 'Лицевой счет успешно удален!'


def get_apartment_in_p_a(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            response = {}
            if request.GET.get('house_id'):
                house = get_object_or_404(House, pk=request.GET.get('house_id'))
                sections = house.sections.all().values('id', 'name')
                json_sections = json.loads(json.dumps(list(sections), cls=DjangoJSONEncoder))
                response = {'sections': json_sections}
            if request.GET.get('section_id'):
                personal_accounts = PersonalAccount.objects.select_related('apartment').all()
                apartment_idx = [x.apartment.id for x in personal_accounts if x.apartment]
                free_apartments = Apartment.objects.exclude(pk__in=apartment_idx)
                apartments = free_apartments.filter(section__id=request.GET.get('section_id')).values('id', 'number')
                json_apartments = json.loads(json.dumps(list(apartments), cls=DjangoJSONEncoder))
                response = {'apartments': json_apartments}
            if request.GET.get('apartment_id'):
                apartment = get_object_or_404(Apartment, pk=request.GET.get('apartment_id'))
                if apartment.owner:
                    response = {'owner': f'{apartment.owner.last_name} '
                                         f'{apartment.owner.first_name} '
                                         f'{apartment.owner.patronymic} ',
                                'telephone': apartment.owner.telephone}
            return JsonResponse(response, status=200)
# endregion PersonalAccounts


# region Apartments
class ApartmentsListView(StaffRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'crm/pages/apartments/apartments_list.html'
    context_object_name = 'apartments'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        houses = House.objects.prefetch_related('sections__apartment_set').all()
        if self.request.GET.get('input_house'):
            for house in houses:
                if house.id == int(self.request.GET.get('input_house')):
                    context['sections'] = house.sections.all()
                    context['floors'] = house.floors.all()
        context['houses'] = houses
        context['owners'] = UserProfile.objects.filter(is_staff=False)
        personal_accounts = PersonalAccount.objects.select_related('apartment').all()
        context['personal_accounts'] = personal_accounts
        context['idx'] = [x.apartment.id for x in personal_accounts if x.apartment]
        return context

    def get_queryset(self):
        queryset = Apartment.objects.select_related('section', 'floor', 'owner').all()
        if self.request.GET.get('filter-number') == '1':
            queryset = queryset.order_by('-number')
        if self.request.GET.get('filter-number') == '0':
            queryset = queryset.order_by('number')
        if self.request.GET.get('filter-house') == '1':
            queryset = queryset.order_by('-id')
        if self.request.GET.get('filter-house') == '0':
            queryset = queryset.order_by('id')
        if self.request.GET.get('filter-section') == '1':
            queryset = queryset.order_by('-section')
        if self.request.GET.get('filter-section') == '0':
            queryset = queryset.order_by('section')
        if self.request.GET.get('filter-floor') == '1':
            queryset = queryset.order_by('-floor')
        if self.request.GET.get('filter-floor') == '0':
            queryset = queryset.order_by('floor')
        if self.request.GET.get('filter-owner') == '0':
            queryset = queryset.order_by('-owner__last_name')
        if self.request.GET.get('filter-owner') == '1':
            queryset = queryset.order_by('owner__last_name')
        if self.request.GET.get('input_number'):
            queryset = queryset.filter(number__icontains=self.request.GET.get('input_number'))
        if self.request.GET.get('input_house'):
            house = get_object_or_404(House, pk=self.request.GET.get('input_house'))
            idx = [x.id for x in house.sections.all()]
            queryset = queryset.filter(section__in=idx)
        if self.request.GET.get('input_section'):
            queryset = queryset.filter(section__name=self.request.GET.get('input_section'))
        if self.request.GET.get('input_floor'):
            queryset = queryset.filter(floor__name=self.request.GET.get('input_floor'))
        if self.request.GET.get('input_owner'):
            queryset = queryset.filter(owner=self.request.GET.get('input_owner'))
        if self.request.GET.get('debt'):
            if self.request.GET.get('debt') == 'yes':
                p_a = PersonalAccount.objects.select_related('apartment').filter(balance__lt=0)
                idx = [x.apartment.id for x in p_a if x.apartment]
            else:
                p_a = PersonalAccount.objects.select_related('apartment').filter(balance__gte=0)
                idx = [x.apartment.id for x in p_a if x.apartment]
            queryset = queryset.filter(pk__in=idx)
        return queryset


class ApartmentDetailView(StaffRequiredMixin, DetailView):
    queryset = Apartment.objects.select_related('section', 'floor', 'owner')
    template_name = 'crm/pages/apartments/apartment_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        context['owners'] = UserProfile.objects.filter(is_staff=False)
        personal_accounts = PersonalAccount.objects.select_related('apartment').all()
        context['personal_accounts'] = personal_accounts
        context['idx'] = [x.apartment.id for x in personal_accounts if x.apartment]
        return context


class ApartmentCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/apartments/apartment_create.html'
    success_message = 'Квартира успешно добавлена!'
    apartment_id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personal_accounts'] = PersonalAccount.objects.filter(status='active', apartment=None)
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            if self.request.GET.get('id'):
                apartment = get_object_or_404(Apartment, pk=self.request.GET.get('id'))
                form_class = ApartmentForm(self.request.POST or None, initial={'number': apartment.number + 1})
            else:
                form_class = ApartmentForm(self.request.POST or None)
        return form_class

    def form_valid(self, form):
        personal_number = form.cleaned_data['personal_number'] if form.cleaned_data['personal_number'] else None
        apartment = form.save()
        self.apartment_id = apartment.id
        if personal_number:
            try:
                personal_account = PersonalAccount.objects.get(personal_number=personal_number)
                if personal_account.apartment:
                    raise ValidationError('Введенный лицевой счет занят')
                else:
                    personal_account.apartment = apartment
                    personal_account.save()
            except ObjectDoesNotExist:
                PersonalAccount.objects.create(personal_number=personal_number, apartment=apartment)
        return super().form_valid(form)

    def get_success_url(self):
        success_url = reverse('apartments_list')
        try:
            if self.request.POST['save_and_add']:
                success_url = reverse('apartment_create') + f'?id={self.apartment_id}'
        except:
            pass
        return success_url


class ApartmentUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    queryset = Apartment.objects.select_related('section', 'floor', 'owner')
    template_name = 'crm/pages/apartments/apartment_update.html'
    success_message = 'Данные о квартире обновлены!'
    apartment_id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        context['personal_accounts'] = PersonalAccount.objects.select_related('apartment').filter(status='active',
                                                                                                  apartment=None)
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = ApartmentForm(self.request.POST or None, instance=self.object)
        return form_class

    def form_valid(self, form):
        personal_number = form.cleaned_data['personal_number'] if form.cleaned_data['personal_number'] else None
        apartment = form.save()
        self.apartment_id = apartment.id
        try:
            personal_account = PersonalAccount.objects.get(apartment=apartment)
        except ObjectDoesNotExist:
            personal_account = None
        if personal_account:
            if personal_number:
                if personal_account.personal_number == personal_number:
                    pass
                else:
                    try:
                        personal_account = PersonalAccount.objects.get(personal_number=personal_number)
                        if personal_account.apartment:
                            raise ValidationError('Введенный лицевой счет занят')
                        else:
                            PersonalAccount.objects.filter(apartment=apartment).update(apartment=None)
                            personal_account.apartment = apartment
                            personal_account.save()
                    except ObjectDoesNotExist:
                        PersonalAccount.objects.filter(apartment=apartment).update(apartment=None)
                        PersonalAccount.objects.create(personal_number=personal_number, apartment=apartment)
            else:
                PersonalAccount.objects.filter(apartment=apartment).update(apartment=None)
        else:
            if personal_number:
                try:
                    personal_account = PersonalAccount.objects.get(personal_number=personal_number)
                    if personal_account.apartment:
                        raise ValidationError('Введенный лицевой счет занят')
                    else:
                        personal_account.apartment = apartment
                        personal_account.save()
                except ObjectDoesNotExist:
                    PersonalAccount.objects.create(personal_number=personal_number, apartment=apartment)
        return super().form_valid(form)

    def get_success_url(self):
        success_url = reverse('apartments_list')
        try:
            if self.request.POST['save_and_add']:
                success_url = reverse('apartment_create') + f'?id={self.apartment_id}'
        except:
            pass
        return success_url


class ApartmentDeleteView(SuccessMessageMixin, DeleteView):
    model = Apartment
    success_url = reverse_lazy('apartments_list')
    success_message = 'Квартира успешно удалена!'


def get_section_and_floor(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            if request.GET.get('house_id'):
                house = get_object_or_404(House, pk=request.GET.get('house_id'))
                sections = house.sections.all().values('id', 'name')
                floors = house.floors.all().values('id', 'name')
                json_sections = json.loads(json.dumps(list(sections), cls=DjangoJSONEncoder))
                json_floors = json.loads(json.dumps(list(floors), cls=DjangoJSONEncoder))
                response = {'sections': json_sections,
                            'floors': json_floors}
            else:
                response = {}
            return JsonResponse(response, status=200)
# endregion Apartments


# region Owners
class OwnersListView(StaffRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'crm/pages/owners/owners_list.html'
    context_object_name = 'owners'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apartments'] = Apartment.objects.select_related('section', 'owner')
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        context['personal_accounts'] = PersonalAccount.objects.select_related('apartment', 'apartment__owner').all()
        return context

    def get_queryset(self):
        queryset = UserProfile.objects.filter(is_staff=False)
        if self.request.GET.get('filter-name') == '1':
            queryset = queryset.order_by('last_name')
        if self.request.GET.get('filter-name') == '0':
            queryset = queryset.order_by('-last_name')
        if self.request.GET.get('filter-date') == '1':
            queryset = queryset.order_by('date_joined')
        if self.request.GET.get('filter-date') == '0':
            queryset = queryset.order_by('-date_joined')
        if self.request.GET.get('id'):
            queryset = queryset.filter(user_id__icontains=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(Q(last_name__icontains=self.request.GET.get('name')) |
                                       Q(first_name__icontains=self.request.GET.get('name')) |
                                       Q(patronymic__icontains=self.request.GET.get('name')))
        if self.request.GET.get('email'):
            queryset = queryset.filter(email__icontains=self.request.GET.get('email'))
        if self.request.GET.get('telephone'):
            queryset = queryset.filter(telephone__icontains=self.request.GET.get('telephone'))
        if self.request.GET.get('date'):
            queryset = queryset.filter(date_joined=self.request.GET.get('date'))
        if self.request.GET.get('status'):
            queryset = queryset.filter(status=self.request.GET.get('status'))
        if self.request.GET.get('house'):
            sections_idx = get_object_or_404(House, pk=self.request.GET.get('house')).sections.all()
            apartments = Apartment.objects.select_related('section', 'owner').filter(section__in=sections_idx)
            owners_idx = [x.owner.id for x in apartments if x.owner]
            queryset = queryset.filter(pk__in=owners_idx)
        if self.request.GET.get('apartment'):
            apartments = Apartment.objects.select_related('owner').filter(
                number__icontains=self.request.GET.get('apartment')
            )
            owners_idx = [x.owner.id for x in apartments if x.owner]
            queryset = queryset.filter(pk__in=owners_idx)
        if self.request.GET.get('debt'):
            if self.request.GET.get('debt') == 'yes':
                personal_accounts = PersonalAccount.objects.select_related('apartment',
                                                                           'apartment__owner').filter(balance__lt=0)
                owners_idx = [x.apartment.owner.id for x in personal_accounts if x.apartment and x.apartment.owner]
                queryset = queryset.filter(pk__in=owners_idx)
            else:
                personal_accounts = PersonalAccount.objects.select_related('apartment',
                                                                           'apartment__owner').filter(balance__gte=0)
                owners_idx = [x.apartment.owner.id for x in personal_accounts if x.apartment and x.apartment.owner]
                queryset = queryset.filter(pk__in=owners_idx)
        return queryset


class OwnerDetailView(StaffRequiredMixin, DetailView):
    queryset = UserProfile.objects.select_related('role')
    template_name = 'crm/pages/owners/owner_detail.html'


class OwnerCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = UserProfile
    template_name = 'crm/pages/owners/owner_create.html'
    form_class = OwnerCreateForm
    success_url = reverse_lazy('owners_list')
    success_message = 'Владелец квартиры успешно добавлен!'


class OwnerUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    queryset = UserProfile.objects.select_related('role')
    form_class = OwnerUpdateForm
    template_name = 'crm/pages/owners/owner_update.html'
    success_url = reverse_lazy('owners_list')
    success_message = 'Данные о владельце успешно обновлены!'


class OwnerDeleteView(SuccessMessageMixin, DeleteView):
    model = UserProfile
    success_url = reverse_lazy('owners_list')
    success_message = 'Владелец квартиры успешно удалён!'


class OwnerInviteView(StaffRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'crm/pages/owners/owner_invite.html'
    form_class = InviteForm
    success_message = 'Приглашение владельцу успешно отправлено!'
    success_url = reverse_lazy('owners_list')

    def form_valid(self, form):
        body_text = render_to_string('crm/elements/invite.txt')
        send_invite_letter.delay(form.cleaned_data['email'], body_text)
        return super().form_valid(form)
# endregion Owners


# region Houses
class HousesListView(StaffRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'crm/pages/houses/houses_list.html'
    context_object_name = 'houses'

    def get_queryset(self):
        queryset = House.objects.all()
        if self.request.GET.get('filter-address') == '1':
            queryset = queryset.order_by('address')
        if self.request.GET.get('filter-address') == '0':
            queryset = queryset.order_by('-address')
        if self.request.GET.get('filter-name') == '1':
            queryset = queryset.order_by('name')
        if self.request.GET.get('filter-name') == '0':
            queryset = queryset.order_by('-name')
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('address'):
            queryset = queryset.filter(address__icontains=self.request.GET.get('address'))
        return queryset


class HouseDetailView(StaffRequiredMixin, DetailView):
    queryset = House.objects.prefetch_related('users__role')
    template_name = 'crm/pages/houses/house_detail.html'


class HouseCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/houses/house_create.html'
    success_message = 'Дом успешно добавлен!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_formset'] = SectionFormSet(self.request.POST or None,
                                                    queryset=Section.objects.none(), prefix='section_formset')
        context['floor_formset'] = FloorFormSet(self.request.POST or None,
                                                queryset=Floor.objects.none(), prefix='floor_formset')
        context['user_formset'] = UserFormSet(self.request.POST or None)
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = HouseForm(self.request.POST or None, self.request.FILES or None)
        return form_class

    def form_valid(self, form):
        section_formset = self.get_context_data()['section_formset']
        floor_formset = self.get_context_data()['floor_formset']
        user_formset = self.get_context_data()['user_formset']
        house = form.save(commit=False)
        house.save()
        for obj in section_formset:
            if obj.is_valid() and obj.cleaned_data and not obj.cleaned_data['DELETE']:
                section = obj.save()
                house.sections.add(section)
        for obj in floor_formset:
            if obj.is_valid() and obj.cleaned_data and not obj.cleaned_data['DELETE']:
                floor = obj.save()
                house.floors.add(floor)

        if user_formset.is_valid():
            for obj in user_formset:
                if obj.cleaned_data and not obj.cleaned_data['DELETE']:
                    user = obj.cleaned_data['user']
                    house.users.add(user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('houses_list')


class HouseUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    queryset = House.objects.prefetch_related('users__role')
    template_name = 'crm/pages/houses/house_update.html'
    success_url = reverse_lazy('houses_list')
    success_message = 'Данные о доме обновлены!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_formset'] = SectionFormSet(self.request.POST or None,
                                                    queryset=self.object.sections.all(), prefix='section_formset')
        context['floor_formset'] = FloorFormSet(self.request.POST or None,
                                                queryset=self.object.floors.all(), prefix='floor_formset')
        users = self.object.users.all()
        context['user_formset'] = UserFormSet(self.request.POST or None,
                                              initial=[{'user': x.id,
                                                        'role': x.role.get_role_display()} for x in users])
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = HouseForm(self.request.POST or None, self.request.FILES or None, instance=self.object)
        return form_class

    def form_valid(self, form):
        section_formset = self.get_context_data()['section_formset']
        floor_formset = self.get_context_data()['floor_formset']
        user_formset = self.get_context_data()['user_formset']
        house = form.save(commit=False)
        house.users.clear()
        for obj in section_formset:
            if obj.is_valid() and obj.cleaned_data and not obj.cleaned_data['DELETE']:
                section = obj.save()
                house.sections.add(section)
        section_formset.save()
        for obj in floor_formset:
            if obj.is_valid() and obj.cleaned_data and not obj.cleaned_data['DELETE']:
                floor = obj.save()
                house.floors.add(floor)
        floor_formset.save()
        for obj in user_formset:
            if obj.is_valid() and obj.cleaned_data and not obj.cleaned_data['DELETE']:
                user = obj.cleaned_data['user']
                house.users.add(user)
        house.save()
        return super().form_valid(form)


class HouseDeleteView(SuccessMessageMixin, DeleteView):
    model = House
    success_url = reverse_lazy('houses_list')
    success_message = 'Дом успешно удалён!'


def get_role(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            if request.GET.get('user'):
                role = UserProfile.objects.get(pk=request.GET.get('user')).role.get_role_display()
                response = {'role': role}
            else:
                response = {'role': None}
            return JsonResponse(response, status=200)
# endregion Houses


# region Messages
class MessagesListView(StaffRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'crm/pages/messages/messages_list.html'
    context_object_name = 'messagess'

    def get_queryset(self):
        queryset = Message.objects.select_related('message_for_owner').all()
        return queryset


class MessageDetailView(StaffRequiredMixin, DetailView):
    queryset = Message.objects.select_related('sender')
    template_name = 'crm/pages/messages/message_detail.html'


class MessageCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/messages/message_create.html'
    success_message = 'Сообщение успешно отправлено!'

    def get_form(self, form_class=None):
        form_class = MessageForm(self.request.POST or None)
        if self.request.GET.get('owner_id'):
            form_class = MessageForm(self.request.POST or None,
                                     initial={'message_for_owner': self.request.GET.get('owner_id')})
        return form_class

    def form_valid(self, form):
        sender = get_object_or_404(UserProfile, pk=self.request.user.id)
        message = form.save(commit=False)
        message.sender = sender
        message.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('messages_list')


class MessageDeleteView(SuccessMessageMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('messages_list')
    success_message = 'Сообщение успешно удалено!'


def select_recipients_for_send_message(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            response = {}
            if request.GET.get('house_id'):
                house = get_object_or_404(House, pk=request.GET.get('house_id'))
                sections = json.loads(json.dumps(list(house.sections.all().values('id', 'name')),
                                                 cls=DjangoJSONEncoder))
                floors = json.loads(json.dumps(list(house.floors.all().values('id', 'name')), cls=DjangoJSONEncoder))
                response = {'sections': sections,
                            'floors': floors}
            if request.GET.get('section_id') and request.GET.get('floor_id'):
                apartments = Apartment.objects.filter(section_id=request.GET.get('section_id'),
                                                      floor_id=request.GET.get('floor_id')).values('id', 'number')
                response = {'apartments': json.loads(json.dumps(list(apartments), cls=DjangoJSONEncoder))}
            return JsonResponse(response, status=200)


def delete_selected_messages(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            if request.GET.get('idx'):
                idx = [int(x) for x in request.GET.get('idx').split(' ')[:-1]]
                Message.objects.filter(pk__in=idx).delete()
                messages.add_message(request, messages.SUCCESS, 'Выбранные сообщения успешно удалены!')
            return JsonResponse({}, status=200)
# endregion Messages


# region Application
class ApplicationsListView(StaffRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'crm/pages/applications/applications_list.html'
    context_object_name = 'applications'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        users = UserProfile.objects.select_related('role').all()
        context['owners'] = users.filter(is_staff=False)
        context['masters'] = users.filter(Q(role__role='plumber') | Q(role__role='electric'))
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        return context

    def get_queryset(self):
        queryset = Application.objects.select_related('apartment', 'apartment__owner',
                                                      'apartment__section', 'master').all()
        if self.request.GET.get('input_number'):
            queryset = queryset.filter(pk__contains=self.request.GET.get('input_number'))
        if self.request.GET.get('filter-number') == '1':
            queryset = queryset.order_by('-pk')
        if self.request.GET.get('filter-number') == '0':
            queryset = queryset.order_by('pk')
        if self.request.GET.get('input_date'):
            input_date = self.request.GET.get('input_date').split(' - ')
            date_range = [datetime.datetime.strptime(x, '%d.%m.%Y').strftime('%Y-%m-%d') for x in input_date]
            queryset = queryset.filter(date__range=date_range)
        if self.request.GET.get('filter-date') == '1':
            queryset = queryset.order_by('date')
        if self.request.GET.get('filter-date') == '0':
            queryset = queryset.order_by('-date')
        if self.request.GET.get('input_type'):
            queryset = queryset.filter(type_master=self.request.GET.get('input_type'))
        if self.request.GET.get('filter-master') == '1':
            queryset = queryset.order_by('type_master')
        if self.request.GET.get('filter-master') == '0':
            queryset = queryset.order_by('-type_master')
        if self.request.GET.get('description'):
            queryset = queryset.filter(description__icontains=self.request.GET.get('description'))
        if self.request.GET.get('apartment'):
            queryset = queryset.filter(apartment__number__contains=self.request.GET.get('apartment'))
        if self.request.GET.get('owner'):
            queryset = queryset.filter(apartment__owner_id=self.request.GET.get('owner'))
        if self.request.GET.get('telephone'):
            queryset = queryset.filter(apartment__owner__telephone__contains=self.request.GET.get('telephone'))
        if self.request.GET.get('master'):
            queryset = queryset.filter(master=self.request.GET.get('master'))
        if self.request.GET.get('status'):
            queryset = queryset.filter(status=self.request.GET.get('status'))
        return queryset


class ApplicationDetailView(StaffRequiredMixin, DetailView):
    queryset = Application.objects.select_related('apartment', 'apartment__owner', 'apartment__section', 'master').all()
    template_name = 'crm/pages/applications/application_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        return context


class ApplicationCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ApplicationForm
    template_name = 'crm/pages/applications/application_create.html'
    success_url = reverse_lazy('applications_list')
    success_message = 'Новая заявка успешно добавленa!'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        context['apartments'] = Apartment.objects.select_related('section').all()
        context['masters'] = UserProfile.objects.select_related('role').filter(Q(role__role='plumber') |
                                                                               Q(role__role='electric'))
        return context


class ApplicationUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    queryset = Application.objects.select_related('apartment', 'apartment__owner', 'master', 'apartment__section')
    template_name = 'crm/pages/applications/application_update.html'
    success_url = reverse_lazy('applications_list')
    success_message = 'Заявка вызова мастера успешно обновлена!'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.prefetch_related('sections').all()
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = ApplicationForm(self.request.POST or None, instance=self.object,
                                         initial={'date': self.object.date.strftime('%d.%m.%Y')})
        return form_class


class ApplicationDeleteView(SuccessMessageMixin, DeleteView):
    model = Application
    success_url = reverse_lazy('applications_list')
    success_message = 'Заявка вызова мастера успешно удалена!'


def get_apartment_by_owner(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            if request.GET.get('owner_id'):
                apartments = Apartment.objects.filter(owner_id=request.GET.get('owner_id')).values('id', 'number',
                                                                                                   'section')
                response = {'apartments': json.loads(json.dumps(list(apartments), cls=DjangoJSONEncoder))}
            else:
                apartments = Apartment.objects.all().values('id', 'number', 'section')
                response = {'apartments': json.loads(json.dumps(list(apartments), cls=DjangoJSONEncoder))}
            houses = House.objects.prefetch_related('sections__apartment_set').all()
            for d in response['apartments']:
                for house in houses:
                    for section in house.sections.all():
                        try:
                            if d['section'] == section.id:
                                d['house'] = house.name
                        except:
                            pass
            if request.GET.get('apartment_id'):
                apartment = get_object_or_404(Apartment, pk=request.GET.get('apartment_id'))
                response = {'telephone': apartment.owner.telephone if apartment.owner else None,
                            'house': str([house.name for house in houses if apartment.section in
                                          house.sections.all()][0]),
                            'section_name': str(apartment.section),
                            'floor': str(apartment.floor),
                            'owner_id': apartment.owner.id if apartment.owner else None}
            return JsonResponse(response, status=200)
# endregion Application


# region MeterReading
class MeterReadingsListView(StaffRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'crm/pages/meter_readings/meter_readings_list.html'
    context_object_name = 'meter_readings'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        if self.request.GET.get('house'):
            for house in context['houses']:
                if house.id == int(self.request.GET.get('house')):
                    context['sections'] = house.sections.all()
        context['meters'] = Service.objects.select_related('unit').all()
        return context

    def get_queryset(self):
        queryset = MeterReading.objects.select_related('apartment', 'apartment__section', 'meter', 'meter__unit').all()
        if self.request.GET.get('house'):
            sections = get_object_or_404(House, pk=self.request.GET.get('house')).sections.all()
            queryset = queryset.filter(apartment__section__in=sections)
        if self.request.GET.get('section'):
            queryset = queryset.filter(apartment__section__name=self.request.GET.get('section'))
        if self.request.GET.get('input_number'):
            queryset = queryset.filter(apartment__number__contains=self.request.GET.get('input_number'))
        if self.request.GET.get('filter-number') == '1':
            queryset = queryset.order_by('-apartment__number')
        if self.request.GET.get('filter-number') == '0':
            queryset = queryset.order_by('apartment__number')
        if self.request.GET.get('meter'):
            queryset = queryset.filter(meter__id=self.request.GET.get('meter'))
        return queryset


class MeterReadingsByApartmentListView(StaffRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'crm/pages/meter_readings/meter_readings_by_apartment_list.html'
    context_object_name = 'meter_readings'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apartment'] = get_object_or_404(Apartment, pk=self.request.GET.get('apartment_id'))
        context['meters'] = Service.objects.select_related('unit').all()
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        return context

    def get_queryset(self):
        queryset = MeterReading.objects.select_related(
            'apartment', 'meter', 'meter__unit'
        ).filter(apartment=self.request.GET.get('apartment_id'))
        if self.request.GET.get('number'):
            queryset = queryset.filter(number__contains=self.request.GET.get('number'))
        if self.request.GET.get('status'):
            queryset = queryset.filter(status=self.request.GET.get('status'))
        if self.request.GET.get('input_date'):
            input_date = self.request.GET.get('input_date').split(' - ')
            date_range = [datetime.datetime.strptime(x, '%d.%m.%Y').strftime('%Y-%m-%d') for x in input_date]
            queryset = queryset.filter(date__range=date_range)
        if self.request.GET.get('filter-date') == '0':
            queryset = queryset.order_by('date')
        if self.request.GET.get('filter-date') == '1':
            queryset = queryset.order_by('-date')
        if self.request.GET.get('meter'):
            queryset = queryset.filter(meter__id=self.request.GET.get('meter'))
        return queryset


class MeterReadingDetailView(StaffRequiredMixin, DetailView):
    queryset = MeterReading.objects.select_related(
        'apartment', 'apartment__section', 'meter', 'meter__unit', 'apartment__owner'
    ).all()
    template_name = 'crm/pages/meter_readings/meter_reading_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.prefetch_related('sections__apartment_set').all()
        return context


class MeterReadingCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/meter_readings/meter_reading_create.html'
    success_message = 'Показания счетчика успешно добавлены!'

    def get_form(self, form_class=None):
        if form_class is None:
            if self.request.GET.get('apartment_id'):
                apartment = get_object_or_404(Apartment, pk=self.request.GET.get('apartment_id'))
                house = get_object_or_404(House, sections__id=apartment.section.id)
                form_class = MeterReadingForm(self.request.POST or None, initial={'apartment': apartment.id,
                                                                                  'section': apartment.section.id,
                                                                                  'house': house.id})
            else:
                form_class = MeterReadingForm(self.request.POST or None)
        return form_class

    def get_success_url(self):
        success_url = reverse('meter_readings_by_apartment_list') + f'?apartment_id={self.object.apartment.id}'
        try:
            if self.request.POST['save_and_add']:
                success_url = reverse('meter_reading_create')
        except:
            pass
        return success_url


class MeterReadingUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MeterReading
    form_class = MeterReadingUpdateForm
    template_name = 'crm/pages/meter_readings/meter_reading_update.html'
    success_message = 'Показания успешно обновлены!'

    def get_success_url(self):
        success_url = reverse('meter_readings_by_apartment_list') + f'?apartment_id={self.object.apartment.id}'
        try:
            if self.request.POST['save_and_add']:
                success_url = reverse('meter_reading_create')
        except:
            pass
        return success_url


class MeterReadingDeleteView(SuccessMessageMixin, DeleteView):
    model = MeterReading
    success_url = reverse_lazy('meter_readings_list')
    success_message = 'Показания счетчика успешно удалены!'


def get_apartment_in_m_r(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            response = {}
            if request.GET.get('house_id'):
                house = get_object_or_404(House, pk=request.GET.get('house_id'))
                sections = house.sections.all().values('id', 'name')
                json_sections = json.loads(json.dumps(list(sections), cls=DjangoJSONEncoder))
                response = {'sections': json_sections}
            if request.GET.get('section_id'):
                personal_accounts = PersonalAccount.objects.select_related('apartment').all()
                apartment_idx = [x.apartment.id for x in personal_accounts if x.apartment]
                apartments = Apartment.objects.filter(pk__in=apartment_idx,
                                                      section_id=request.GET.get('section_id')).values('id', 'number')
                json_apartments = json.loads(json.dumps(list(apartments), cls=DjangoJSONEncoder))
                response = {'apartments': json_apartments}
            return JsonResponse(response, status=200)
# endregion MeterReading


# region SITE-MANAGEMENT
class MainUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'crm/pages/site-management/main.html'
    success_url = reverse_lazy('main')
    success_message = 'Данные о странице обновлены!'

    def get_object(self, queryset=None):
        obj = get_object_or_404(MainPage, pk=1)
        return obj

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = MainPageForm(self.request.POST or None, self.request.FILES or None, instance=self.object)
        return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo_block'] = SeoForm(self.request.POST or None, instance=self.object.seo, prefix='seo_block')
        context['formset'] = BlockFormSet(self.request.POST or None, self.request.FILES or None,
                                          queryset=Block.objects.all(), prefix='formset')
        return context

    def form_valid(self, form):
        seo_block = self.get_context_data()['seo_block']
        formset = self.get_context_data()['formset']
        if seo_block.is_valid():
            seo_block.save()
        for obj in formset:
            if obj.is_valid():
                obj.save()
        form.save(commit=False)
        form.seo = seo_block.instance
        form.save()
        return super().form_valid(form)


class AboutUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'crm/pages/site-management/about.html'
    success_url = reverse_lazy('about')
    success_message = 'Данные о странице обновлены!'

    def get_object(self, queryset=None):
        obj = get_object_or_404(AboutPage, pk=1)
        return obj

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = AboutPageForm(self.request.POST or None, self.request.FILES or None, instance=self.object)
        return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo_form'] = PhotoForm(self.request.POST or None, self.request.FILES or None, prefix='photo_form')
        context['add_photo_form'] = PhotoForm(self.request.POST or None, self.request.FILES or None,
                                              prefix='add_photo_form')
        context['formset'] = DocumentFormSet(self.request.POST or None, self.request.FILES or None,
                                             queryset=Document.objects.all(), prefix='formset')
        context['seo_block'] = SeoForm(self.request.POST or None, instance=self.object.seo, prefix='seo_block')
        context['gallery'] = Photo.objects.all()
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        photo_form = self.get_context_data()['photo_form']
        add_photo_form = self.get_context_data()['add_photo_form']
        seo_block = self.get_context_data()['seo_block']
        if photo_form.is_valid():
            if photo_form.cleaned_data['photo']:
                photo_form.save()
        if add_photo_form.is_valid():
            if add_photo_form.cleaned_data['photo']:
                add_photo_form.save()
        if formset.is_valid():
            formset.save()
        if seo_block.is_valid():
            seo_block.save()
        form.save(commit=False)
        form.seo = seo_block.instance
        form.save()
        return super().form_valid(form)


class PhotoDeleteView(DeleteView):
    model = Photo
    success_url = reverse_lazy('about')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ServicePageUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'crm/pages/site-management/about_service.html'
    success_url = reverse_lazy('about_service')
    success_message = 'Данные о странице обновлены!'

    def get_object(self, queryset=None):
        obj = get_object_or_404(ServicePage, pk=1)
        return obj

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = ServicePageForm(self.request.POST or None, instance=self.object)
        return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = AboutServiceFormSet(self.request.POST or None, self.request.FILES or None,
                                                 queryset=AboutService.objects.all(), prefix='formset')
        context['seo_block'] = SeoForm(self.request.POST or None, instance=self.object.seo, prefix='seo_block')
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        seo_block = self.get_context_data()['seo_block']
        formset.save(commit=False)
        for obj in formset:
            if obj.is_valid() and obj.cleaned_data and not obj.cleaned_data['DELETE']:
                obj.save()
        for obj in formset.deleted_objects:
            obj.delete()
        if seo_block.is_valid():
            seo_block.save()
        form.save(commit=False)
        form.seo = seo_block.instance
        form.save()
        return super().form_valid(form)


class ContactPageUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'crm/pages/site-management/contacts.html'
    success_url = reverse_lazy('contact')
    success_message = 'Данные о странице обновлены!'

    def get_object(self, queryset=None):
        obj = get_object_or_404(ContactPage, pk=1)
        return obj

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = ContactPageForm(self.request.POST or None, instance=self.object)
        return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo_block'] = SeoForm(self.request.POST or None, instance=self.object.seo, prefix='seo_block')
        return context

    def form_valid(self, form):
        seo_block = self.get_context_data()['seo_block']
        if seo_block.is_valid():
            seo_block.save()
        form.save(commit=False)
        form.seo = seo_block.instance
        form.save()
        return super().form_valid(form)
# endregion SITE-MANAGEMENT


# region SYSTEM-SETTINGS
# region services page
class ServiceCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/system_settings/services.html'
    success_message = 'Услуги успешно отредактированны!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.select_related('unit')
        idx = []
        for service in services:
            idx.append(service.unit.id)
        context['idx'] = idx
        context['unit_formset'] = UnitFormSet(self.request.POST or None, queryset=Unit.objects.all(),
                                              prefix='unit_formset')
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = ServiceFormSet(self.request.POST or None, queryset=Service.objects.all())
        return form_class

    def form_valid(self, form):
        unit_formset = self.get_context_data()['unit_formset']
        unit_formset.save(commit=False)
        for unit in unit_formset.deleted_objects:
            unit.delete()
        for unit in unit_formset:
            if unit.is_valid() and unit.cleaned_data:
                unit.save()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('services')
# endregion services page


# region tariffs page
class TariffsListView(StaffRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'crm/pages/system_settings/tariffs/tariffs_list.html'
    context_object_name = 'tariffs'

    def get_queryset(self):
        queryset = Tariff.objects.all()
        if self.request.GET.get('filter') == '1':
            queryset = queryset.order_by('name')
        if self.request.GET.get('filter') == '0':
            queryset = queryset.order_by('-name')
        return queryset


class TariffDetailView(StaffRequiredMixin, DetailView):
    queryset = Tariff.objects.prefetch_related('servicefortariff_set__service__unit')
    template_name = 'crm/pages/system_settings/tariffs/tariff_detail.html'


class TariffCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/system_settings/tariffs/tariff_create.html'
    success_message = 'Тариф успешно создан!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('id'):
            serv_for_tar = ServiceForTariff.objects.filter(tariff_id=self.request.GET.get('id'))
            formset = modelformset_factory(ServiceForTariff, form=ServiceForTariffForm, extra=len(serv_for_tar),
                                           can_delete=True)
            context['formset'] = formset(self.request.POST or None, queryset=ServiceForTariff.objects.none(),
                                         prefix='formset', initial=[{'service': x.service,
                                                                     'cost_for_unit': x.cost_for_unit,
                                                                     'units': x.service.unit.id} for x in serv_for_tar])
        else:
            formset = modelformset_factory(ServiceForTariff, form=ServiceForTariffForm, extra=0, can_delete=True)
            context['formset'] = formset(self.request.POST or None,
                                         queryset=ServiceForTariff.objects.none(), prefix='formset')
        context['units'] = Unit.objects.all()
        context['services'] = Service.objects.select_related('unit')
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            if self.request.GET.get('id'):
                tariff = get_object_or_404(Tariff, pk=self.request.GET.get('id'))
                form_class = TariffForm(self.request.POST or None,
                                        initial={'name': tariff.name, 'description': tariff.description})
            else:
                form_class = TariffForm(self.request.POST or None)
        return form_class

    def form_valid(self, form):
        form.save()
        formset = self.get_context_data()['formset']
        for obj in formset:
            if obj.is_valid():
                serv_for_tar = obj.save(commit=False)
                if obj.cleaned_data:
                    serv_for_tar.tariff = form.instance
                    try:
                        serv_for_tar.save()
                    except IntegrityError:
                        pass
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tariffs_list')


class TariffUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tariff
    template_name = 'crm/pages/system_settings/tariffs/tariff_update.html'
    success_url = reverse_lazy('tariffs_list')
    success_message = 'Данные о тарифе обновлены!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = ServiceForTariffFormSet(self.request.POST or None,
                                                     queryset=ServiceForTariff.objects.filter(tariff_id=self.object.id),
                                                     prefix='formset')
        context['services'] = Service.objects.select_related('unit')
        context['units'] = Unit.objects.all()
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = TariffForm(self.request.POST or None, instance=self.object)
        return form_class

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        form.save()
        formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for obj in formset:
            if obj.is_valid() and obj.cleaned_data:
                obj.instance.tariff = form.instance
                try:
                    obj.save()
                except IntegrityError:
                    pass
        return super().form_valid(form)


class TariffDeleteView(SuccessMessageMixin, DeleteView):
    model = Tariff
    success_url = reverse_lazy('tariffs_list')
    success_message = 'Тариф успешно удалён!'


def get_units(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            if request.GET.get('test'):
                unit_id = Service.objects.get(pk=request.GET.get('test')).unit_id
                response = {'unit_id': unit_id}
            else:
                response = {'unit_id': None}
            return JsonResponse(response, status=200)
# endregion tariffs page


# region roles page
class RoleCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/system_settings/roles.html'
    success_message = 'Роли успешно изменены!'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = RoleFormSet(self.request.POST or None, queryset=Role.objects.all())
        return form_class

    def get_success_url(self):
        return reverse('roles')
# endregion roles page


# region users page
class UsersListView(SuccessMessageMixin, StaffRequiredMixin, ListView):
    template_name = 'crm/pages/system_settings/users/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = UserProfile.objects.filter(is_staff=True).select_related('role').order_by('pk')
        if self.request.GET.get('user_id'):
            user = get_object_or_404(UserProfile, pk=self.request.GET.get('user_id'))
            context = {'user': user}
            body_text = render_to_string('crm/elements/invite_for_admin.txt', context)
            send_invite_letter.delay(user.email, body_text)
            messages.add_message(self.request, messages.SUCCESS, 'Приглашение успешно отправлено')
        if self.request.GET.get('user'):
            queryset = queryset.filter(Q(last_name__icontains=self.request.GET.get('user')) |
                                       Q(first_name__icontains=self.request.GET.get('user')))
        if self.request.GET.get('role'):
            queryset = queryset.filter(role__role=self.request.GET.get('role'))
        if self.request.GET.get('telephone'):
            queryset = queryset.filter(telephone__icontains=self.request.GET.get('telephone'))
        if self.request.GET.get('email'):
            queryset = queryset.filter(email__icontains=self.request.GET.get('email'))
        if self.request.GET.get('status'):
            queryset = queryset.filter(status=self.request.GET.get('status'))
        return queryset


class UserCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/system_settings/users/user_create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно создан!'


class UserDetailView(StaffRequiredMixin, DetailView):
    queryset = UserProfile.objects.select_related('role')
    template_name = 'crm/pages/system_settings/users/user_detail.html'


class UserUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ChangeUserInfoForm
    queryset = UserProfile.objects.select_related('role')
    template_name = 'crm/pages/system_settings/users/user_update.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Данные о пользователе обновлены!'


class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = UserProfile
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно удалён!'
# endregion users page


# region requisites
class RequisiteUpdate(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = RequisiteForm
    model = Requisites
    template_name = 'crm/pages/system_settings/requisites.html'
    success_url = reverse_lazy('requisites', kwargs={'pk': 1})
    success_message = 'Реквизиты обновлены!'
# endregion requisites


# region items page
class ItemsListView(StaffRequiredMixin, ListView):
    template_name = 'crm/pages/system_settings/items/items_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = Item.objects.all()
        if self.request.GET.get('filter') == '0':
            queryset = queryset.order_by('income_expense')
        if self.request.GET.get('filter') == '1':
            queryset = queryset.order_by('-income_expense')
        return queryset


class ItemCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/system_settings/items/item_create.html'
    form_class = ItemForm
    success_url = reverse_lazy('items_list')
    success_message = 'Статья успешно добавлена!'


class ItemUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'crm/pages/system_settings/items/item_update.html'
    success_url = reverse_lazy('items_list')
    success_message = 'Данные о статье успешно обновлены!'


class ItemDeleteView(SuccessMessageMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('items_list')
    success_message = 'Статья успешно удалёна!'
# endregion items page
# endregion SYSTEM-SETTINGS
