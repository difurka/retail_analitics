"""Представления проекта"""
import csv

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import (DetailView,
                                  UpdateView,
                                  DeleteView
                                  )

from controller.controller import Controller
from logger.logger import loggerator
from .models import (Cards,
                     Checks,
                     DateReports,
                     Goods,
                     GroupsOfGoods,
                     PersonalData,
                     Stores,
                     Transactions
                     )
from .forms import (CardsForms,
                    ChecksForms,
                    DateReportsForms,
                    GoodsForms,
                    GroupsOfGoodsForms,
                    PersonalDataForms,
                    StoresForms,
                    TransactionsForms,
                    LoginUserForm
                    )


@loggerator
def index(request):
    data = {}
    return render(request, 'backend/home.html', data)


@loggerator
def logout_user(request):
    logout(request)
    data = {}
    return render(request, 'backend/home.html', data)


@loggerator
def about(request):
    if request.user.username:
        data = {}
        return render(request, 'backend/about.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def developers(request):
    if request.user.username:
        with open('backend/static/backend/text/cshara.txt',
                  'rt', encoding='utf-8') as file:
            text_cshara = file.readlines()
        with open('backend/static/backend/text/ereva.txt',
                  'rt', encoding='utf-8') as file:
            text_ereva = file.readlines()
        with open('backend/static/backend/text/aedie.txt',
                  'rt', encoding='utf-8') as file:
            text_aedie = file.readlines()
        data = {
            'text_cshara': text_cshara,
            'text_ereva': text_ereva,
            'text_aedie': text_aedie,
        }
        return render(request, 'backend/developers.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def data(request):
    if request.user.username:
        data = {}
        return render(request, 'backend/data.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud(request):
    if request.user.username:
        data = {}
        return render(request, 'backend/crud.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_view_cards(request):
    if request.user.username:
        data = {
            'name': 'Cards',
            'table_head': CardsForms.Meta.fields,
            'table': Cards.objects.values_list()
        }
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_view_checks(request):
    if request.user.username:
        data = {
            'name': 'Checks',
            'table_head': ChecksForms.Meta.fields,
            'table': Checks.objects.values_list()
        }
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_view_date_reports(request):
    if request.user.username:
        data = {
            'name': 'DateReports',
            'table_head': DateReportsForms.Meta.fields,
            'table': DateReports.objects.values_list()
        }
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_view_goods(request):
    if request.user.username:
        data = {
            'name': 'Goods',
            'table_head': GoodsForms.Meta.fields,
            'table': Goods.objects.values_list()
        }
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_view_groups_of_goods(request):
    if request.user.username:
        data = {
            'name': 'Groups',
            'table_head': GroupsOfGoodsForms.Meta.fields,
            'table': GroupsOfGoods.objects.values_list()
        }
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_view_personal_data(request):
    if request.user.username:
        data = {
            'name': 'Personal',
            'table_head': PersonalDataForms.Meta.fields,
            'table': PersonalData.objects.values_list()
        }
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_view_stores(request):
    if request.user.username:
        data = {
            'name': 'Stores',
            'table_head': StoresForms.Meta.fields,
            'table': Stores.objects.values_list()
        }
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_view_transactions(request):
    if request.user.username:
        data = {
            'name': 'Transactions',
            'table_head': TransactionsForms.Meta.fields,
            'table': Transactions.objects.values_list()
        }
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_create_cards(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_cards'))
    elif request.user.username == 'admin_retail':
        forms = CardsForms()
        data = {
            'name': 'Cards',
            'forms': forms
        }
        if request.method == 'POST':
            forms = CardsForms(request.POST)
            if forms.is_valid():
                forms.save()
        return render(request, 'backend/crud_create.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_create_checks(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_checks'))
    elif request.user.username == 'admin_retail':
        forms = ChecksForms()
        data = {
            'name': 'Checks',
            'forms': forms
        }
        if request.method == 'POST':
            forms = ChecksForms(request.POST)
            if forms.is_valid():
                forms.save()
        return render(request, 'backend/crud_create.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_create_date_reports(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_date_reports'))
    elif request.user.username == 'admin_retail':
        forms = DateReportsForms()
        data = {
            'name': 'DateReports',
            'forms': forms
        }
        if request.method == 'POST':
            forms = DateReportsForms(request.POST)
            if forms.is_valid():
                forms.save()
        return render(request, 'backend/crud_create.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_create_goods(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_goods'))
    elif request.user.username == 'admin_retail':
        forms = GoodsForms()
        data = {
            'name': 'Goods',
            'forms': forms
        }
        if request.method == 'POST':
            forms = GoodsForms(request.POST)
            if forms.is_valid():
                forms.save()
        return render(request, 'backend/crud_create.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_create_groups_of_goods(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_groups_of_goods'))
    elif request.user.username == 'admin_retail':
        forms = GroupsOfGoodsForms()
        data = {
            'name': 'GroupsOfGoods',
            'forms': forms
        }
        if request.method == 'POST':
            forms = GroupsOfGoodsForms(request.POST)
            if forms.is_valid():
                forms.save()
        return render(request, 'backend/crud_create.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_create_personal_data(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_personal_data'))
    elif request.user.username == 'admin_retail':
        forms = PersonalDataForms()
        data = {
            'name': 'PersonalData',
            'forms': forms
        }
        if request.method == 'POST':
            forms = PersonalDataForms(request.POST)
            if forms.is_valid():
                forms.save()
        return render(request, 'backend/crud_create.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_create_stores(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_stores'))
    elif request.user.username == 'admin_retail':
        forms = StoresForms()
        data = {
            'name': 'Stores',
            'forms': forms
        }
        if request.method == 'POST':
            forms = StoresForms(request.POST)
            if forms.is_valid():
                forms.save()
        return render(request, 'backend/crud_create.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_create_transactions(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_transactions'))
    elif request.user.username == 'admin_retail':
        forms = TransactionsForms()
        data = {
            'name': 'Transactions',
            'forms': forms
        }
        if request.method == 'POST':
            forms = TransactionsForms(request.POST)
            if forms.is_valid():
                forms.save()
        return render(request, 'backend/crud_create.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_update_cards(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_cards'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'Cards',
            'table_head': CardsForms.Meta.fields + ('action',),
            'table': Cards.objects.values_list()
        }
        return render(request, 'backend/crud_update.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_update_checks(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_checks'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'Checks',
            'table_head': ChecksForms.Meta.fields + ('action',),
            'table': Checks.objects.values_list()
        }
        return render(request, 'backend/crud_update.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_update_date_reports(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_date_reports'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'DateReports',
            'table_head': DateReportsForms.Meta.fields + ('action',),
            'table': DateReports.objects.values_list()
        }
        return render(request, 'backend/crud_update.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_update_goods(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_goods'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'Goods',
            'table_head': GoodsForms.Meta.fields + ('action',),
            'table': Goods.objects.values_list()
        }
        return render(request, 'backend/crud_update.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_update_groups_of_goods(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_groups_of_goods'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'GroupsOfGoods',
            'table_head': GroupsOfGoodsForms.Meta.fields + ('action',),
            'table': GroupsOfGoods.objects.values_list()
        }
        return render(request, 'backend/crud_update.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_update_personal_data(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_personal_data'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'PersonalData',
            'table_head': PersonalDataForms.Meta.fields + ('action',),
            'table': PersonalData.objects.values_list()
        }
        return render(request, 'backend/crud_update.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_update_stores(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_stores'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'Stores',
            'table_head': StoresForms.Meta.fields + ('action',),
            'table': Stores.objects.values_list()
        }
        return render(request, 'backend/crud_update.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_update_transactions(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_transactions'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'Transactions',
            'table_head': TransactionsForms.Meta.fields + ('action',),
            'table': Transactions.objects.values_list()
        }
        return render(request, 'backend/crud_update.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_delete_cards(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_cards'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'Cards',
            'table_head': CardsForms.Meta.fields + ('action',),
            'table': Cards.objects.values_list()
        }
        return render(request, 'backend/crud_delete.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_delete_checks(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_checks'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'Checks',
            'table_head': ChecksForms.Meta.fields + ('action',),
            'table': Checks.objects.values_list()
        }
        return render(request, 'backend/crud_delete.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_delete_date_reports(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_date_reports'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'DateReports',
            'table_head': DateReportsForms.Meta.fields + ('action',),
            'table': DateReports.objects.values_list()
        }
        return render(request, 'backend/crud_delete.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_delete_goods(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_goods'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'Goods',
            'table_head': GoodsForms.Meta.fields + ('action',),
            'table': Goods.objects.values_list()
        }
        return render(request, 'backend/crud_delete.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_delete_groups_of_goods(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_groups_of_goods'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'GroupsOfGoods',
            'table_head': GroupsOfGoodsForms.Meta.fields + ('action',),
            'table': GroupsOfGoods.objects.values_list()
        }
        return render(request, 'backend/crud_delete.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_delete_personal_data(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_personal_data'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'PersonalData',
            'table_head': PersonalDataForms.Meta.fields + ('action',),
            'table': PersonalData.objects.values_list()
        }
        return render(request, 'backend/crud_delete.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_delete_stores(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_stores'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'Stores',
            'table_head': StoresForms.Meta.fields + ('action',),
            'table': Stores.objects.values_list()
        }
        return render(request, 'backend/crud_delete.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_delete_transactions(request):
    if request.user.username and request.user.username != 'admin_retail':
        return HttpResponseRedirect(reverse('crud_view_transactions'))
    elif request.user.username == 'admin_retail':
        data = {
            'name': 'Transactions',
            'table_head': TransactionsForms.Meta.fields + ('action',),
            'table': Transactions.objects.values_list()
        }
        return render(request, 'backend/crud_delete.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_import_cards(request):
    if request.user.username:
        data = {'name': 'Cards'}
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split('\n')
            for line in lines:
                fields = line.split(',')
                data_dict = {}
                data_dict['customer_card_id'] = fields[0]
                data_dict['customer'] = fields[1]
                form = CardsForms(data_dict)
                if form.is_valid():
                    form.save()
        return render(request, 'backend/crud_import.html', data)


@loggerator
def crud_import_checks(request):
    if request.user.username:
        data = {'name': 'Checks'}
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split('\n')
            for line in lines:
                fields = line.split(',')
                data_dict = {}
                data_dict['transaction'] = fields[0]
                data_dict['sku'] = fields[1]
                data_dict['sku_amount'] = fields[2]
                data_dict['sku_summ'] = fields[3]
                data_dict['sku_summ_paid'] = fields[4]
                data_dict['sku_discount'] = fields[5]
                form = ChecksForms(data_dict)
                if form.is_valid():
                    form.save()
        return render(request, 'backend/crud_import.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_import_date_reports(request):
    if request.user.username:
        data = {'name': 'DateReports'}
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split('\n')
            for line in lines:
                fields = line.split(',')
                data_dict = {}
                data_dict['analysis_formation'] = fields[0]
                form = DateReportsForms(data_dict)
                if form.is_valid():
                    form.save()
        return render(request, 'backend/crud_import.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_import_goods(request):
    if request.user.username:
        data = {'name': 'Goods'}
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split('\n')
            for line in lines:
                fields = line.split(',')
                data_dict = {}
                data_dict['sku_id'] = fields[0]
                data_dict['sku_name'] = fields[1]
                data_dict['group'] = fields[2]
                form = GoodsForms(data_dict)
                if form.is_valid():
                    form.save()
        return render(request, 'backend/crud_import.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_import_groups_of_goods(request):
    if request.user.username:
        data = {'name': 'GroupsOfGoods'}
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split('\n')
            for line in lines:
                fields = line.split(',')
                data_dict = {}
                data_dict['group_id'] = fields[0]
                data_dict['group_name'] = fields[1]
                form = GroupsOfGoodsForms(data_dict)
                if form.is_valid():
                    form.save()
        return render(request, 'backend/crud_import.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_import_personal_data(request):
    if request.user.username:
        data = {'name': 'PersonalData'}
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split('\n')
            for line in lines:
                fields = line.split(',')
                data_dict = {}
                data_dict['customer_id'] = fields[0]
                data_dict['customer_name'] = fields[1]
                data_dict['customer_surname'] = fields[2]
                data_dict['customer_primary_email'] = fields[3]
                data_dict['customer_primary_phone'] = fields[4]
                form = PersonalDataForms(data_dict)
                if form.is_valid():
                    form.save()
        return render(request, 'backend/crud_import.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_import_stores(request):
    if request.user.username:
        data = {'name': 'Stores'}
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split('\n')
            for line in lines:
                fields = line.split(',')
                data_dict = {}
                data_dict['transaction_store_id'] = fields[0]
                data_dict['sku'] = fields[1]
                data_dict['sku_purchase_price'] = fields[2]
                data_dict['sku_retail_price'] = fields[3]
                form = StoresForms(data_dict)
                if form.is_valid():
                    form.save()
        return render(request, 'backend/crud_import.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_import_transactions(request):
    if request.user.username:
        data = {'name': 'Transactions'}
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split('\n')
            for line in lines:
                fields = line.split(',')
                data_dict = {}
                data_dict['transaction_id'] = fields[0]
                data_dict['customer_card'] = fields[1]
                data_dict['transaction_summ'] = fields[2]
                data_dict['transaction_date_time'] = fields[3]
                data_dict['transaction_store_id'] = fields[4]
                form = TransactionsForms(data_dict)
                if form.is_valid():
                    form.save()
        return render(request, 'backend/crud_import.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def option_write_csv(data):
    with open(f'export/{data["name"]}.csv',
              'wt', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(data['table_head'])
        for row in data['table']:
            writer.writerow(row)


@loggerator
def crud_export_cards(request):
    if request.user.username:
        data = {
            'name': 'Cards',
            'table_head': CardsForms.Meta.fields,
            'table': Cards.objects.values_list()
        }
        option_write_csv(data)
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_export_checks(request):
    if request.user.username:
        data = {
            'name': 'Checks',
            'table_head': ChecksForms.Meta.fields,
            'table': Checks.objects.values_list()
        }
        option_write_csv(data)
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_export_date_reports(request):
    if request.user.username:
        data = {
            'name': 'DateReports',
            'table_head': DateReportsForms.Meta.fields,
            'table': DateReports.objects.values_list()
        }
        option_write_csv(data)
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_export_goods(request):
    if request.user.username:
        data = {
            'name': 'Goods',
            'table_head': GoodsForms.Meta.fields,
            'table': Goods.objects.values_list()
        }
        option_write_csv(data)
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_export_groups_of_goods(request):
    if request.user.username:
        data = {
            'name': 'Groups',
            'table_head': GroupsOfGoodsForms.Meta.fields,
            'table': GroupsOfGoods.objects.values_list()
        }
        option_write_csv(data)
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_export_personal_data(request):
    if request.user.username:
        data = {
            'name': 'Personal',
            'table_head': PersonalDataForms.Meta.fields,
            'table': PersonalData.objects.values_list()
        }
        option_write_csv(data)
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_export_stores(request):
    if request.user.username:
        data = {
            'name': 'Stores',
            'table_head': StoresForms.Meta.fields,
            'table': Stores.objects.values_list()
        }
        option_write_csv(data)
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def crud_export_transactions(request):
    if request.user.username:
        data = {
            'name': 'Transactions',
            'table_head': TransactionsForms.Meta.fields,
            'table': Transactions.objects.values_list()
        }
        option_write_csv(data)
        return render(request, 'backend/crud_view.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def retail(request):
    if request.user.username:
        data = {}
        return render(request, 'backend/retail.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def manual(request):
    if request.user.username:
        with open('backend/static/backend/text/proposals_1.txt',
                  'rt', encoding='utf-8') as file:
            table_1 = file.readlines()
        with open('backend/static/backend/text/proposals_2.txt',
                  'rt', encoding='utf-8') as file:
            table_2 = file.readlines()
        with open('backend/static/backend/text/proposals_3.txt',
                  'rt', encoding='utf-8') as file:
            table_3 = file.readlines()
        table_head = ['Поле',
                      'Название поля в системе',
                      'Формат / возможные значения',
                      'Описание']
        data = {
            'table_head_1': table_head,
            'table_head_2': table_head,
            'table_head_3': table_head,
            'table_1': [tmp_value.split(',') for tmp_value in table_1],
            'table_2': [tmp_value.split(',') for tmp_value in table_2],
            'table_3': [tmp_value.split(',') for tmp_value in table_3],
        }
        return render(request, 'backend/manual.html', data)
    return HttpResponseRedirect(reverse('login'))


@loggerator
def proposals(request):
    if request.user.username:
        controller = Controller()
        if request.method == 'POST':
            controller.controller_proposals(request)
        return render(request, 'backend/proposals.html',
                      controller.controller_result())
    return HttpResponseRedirect(reverse('login'))


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'backend/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class CardsDetailView(DetailView):
    model = Cards
    template_name = 'backend/detail_view.html'
    context_object_name = 'cards'


class ChecksDetailView(DetailView):
    model = Checks
    template_name = 'backend/detail_view.html'
    context_object_name = 'checks'


class DateReportsDetailView(DetailView):
    model = DateReports
    template_name = 'backend/detail_view.html'
    context_object_name = 'datereports'


class GoodsDetailView(DetailView):
    model = Goods
    template_name = 'backend/detail_view.html'
    context_object_name = 'goods'


class GroupsOfGoodsDetailView(DetailView):
    model = GroupsOfGoods
    template_name = 'backend/detail_view.html'
    context_object_name = 'groupsofgoods'


class PersonalDataDetailView(DetailView):
    model = PersonalData
    template_name = 'backend/detail_view.html'
    context_object_name = 'personaldata'


class StoresDetailView(DetailView):
    model = Stores
    template_name = 'backend/detail_view.html'
    context_object_name = 'stores'


class TransactionsDetailView(DetailView):
    model = Transactions
    template_name = 'backend/ditail_view.html'
    context_object_name = 'transactions'


class CardsUpdateView(UpdateView):
    model = Cards
    template_name = 'backend/detail_update.html'
    form_class = CardsForms


class ChecksUpdateView(UpdateView):
    model = Checks
    template_name = 'backend/detail_update.html'
    form_class = ChecksForms


class DateReportsUpdateView(UpdateView):
    model = DateReports
    template_name = 'backend/detail_update.html'
    form_class = DateReportsForms


class GoodsUpdateView(UpdateView):
    model = Goods
    template_name = 'backend/detail_update.html'
    form_class = GoodsForms


class GroupsOfGoodsUpdateView(UpdateView):
    model = GroupsOfGoods
    template_name = 'backend/detail_update.html'
    form_class = GroupsOfGoodsForms


class PersonalDataUpdateView(UpdateView):
    model = PersonalData
    template_name = 'backend/detail_update.html'
    form_class = PersonalDataForms


class StoresUpdateView(UpdateView):
    model = Stores
    template_name = 'backend/detail_update.html'
    slug_field = 'sku_purchase_price'
    form_class = StoresForms


class TransactionsUpdateView(UpdateView):
    model = Transactions
    template_name = 'backend/detail_update.html'
    form_class = TransactionsForms


class CardsDeleteView(DeleteView):
    model = Cards
    success_url = '/data/crud/view_cards'
    template_name = 'backend/detail_delete.html'


class ChecksDeleteView(DeleteView):
    model = Checks
    success_url = '/data/crud/view_checks'
    template_name = 'backend/detail_delete.html'


class DateReportsDeleteView(DeleteView):
    model = DateReports
    success_url = '/data/crud/view_date_reports'
    template_name = 'backend/detail_delete.html'


class GoodsDeleteView(DeleteView):
    model = Goods
    success_url = '/data/crud/view_goods'
    template_name = 'backend/detail_delete.html'


class GroupsOfGoodsDeleteView(DeleteView):
    model = GroupsOfGoods
    success_url = '/data/crud/view_groups_of_goods'
    template_name = 'backend/detail_delete.html'


class PersonalDataDeleteView(DeleteView):
    model = PersonalData
    success_url = '/data/crud/view_personal_data'
    template_name = 'backend/detail_delete.html'


class StoresDeleteView(DeleteView):
    model = Stores
    success_url = '/data/crud/view_stores'
    slug_field = 'sku_purchase_price'
    template_name = 'backend/detail_delete.html'


class TransactionsDeleteView(DeleteView):
    model = Transactions
    success_url = '/data/crud/view_transactions'
    template_name = 'backend/detail_delete.html'
