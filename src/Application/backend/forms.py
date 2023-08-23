"""Классы форм"""
from .models import (Cards,
                     Checks,
                     DateReports,
                     Goods,
                     GroupsOfGoods,
                     PersonalData,
                     Stores,
                     Transactions
                     )

from django.contrib.auth.forms import AuthenticationForm
from django.forms import (ModelForm,
                          TextInput,
                          DateInput,
                          DateTimeInput,
                          PasswordInput,
                          CharField
                          )


class LoginUserForm(AuthenticationForm):
    username = CharField(label='Username', widget=TextInput(
        attrs={'class': 'form-input'}))
    password = CharField(label='Password', widget=PasswordInput(
        attrs={'class': 'form-input'}))


class CardsForms(ModelForm):
    class Meta:
        model = Cards
        fields = (
            'customer_card_id',
            'customer'
        )

        widgets = {
            'customer_card_id': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'customer_card_id'
            }),
            'customer': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'customer'
            }),
        }


class ChecksForms(ModelForm):
    """Таблица Checks"""
    class Meta:
        """Поля таблицы"""
        model = Checks
        fields = (
            'transaction',
            'sku',
            'sku_amount',
            'sku_summ',
            'sku_summ_paid',
            'sku_discount'
        )

        widgets = {
            'transaction': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'transaction'
            }),
            'sku': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sku_id'
            }),
            'sku_amount': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sku_amount'
            }),
            'sku_summ': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sku_summ'
            }),
            'sku_summ_paid': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sku_summ_paid'
            }),
            'sku_discount': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sku_discount'
            }),
        }


class DateReportsForms(ModelForm):
    class Meta:
        model = DateReports
        fields = (
            'analysis_formation',
        )

        widgets = {
            'analysis_formation': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'analysis_formation'
            })
        }


class GoodsForms(ModelForm):
    class Meta:
        model = Goods
        fields = (
            'sku_id',
            'sku_name',
            'group'
        )

        widgets = {
            'sku_id': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sku_id'
            }),
            'sku_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sku_name'
            }),
            'group': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'group'
            }),
        }


class GroupsOfGoodsForms(ModelForm):
    class Meta:
        model = GroupsOfGoods
        fields = (
            'group_id',
            'group_name'
        )

        widgets = {
            'group_id': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'group_id'
            }),
            'group_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'group_name'
            })
        }


class PersonalDataForms(ModelForm):
    """Таблица PersonalData"""
    class Meta:
        """Поля таблицы"""
        model = PersonalData
        fields = (
            'customer_id',
            'customer_name',
            'customer_surname',
            'customer_primary_email',
            'customer_primary_phone'
        )

        widgets = {
            'customer_id': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'customer_id'
            }),
            'customer_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'customer_name'
            }),
            'customer_surname': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'customer_surname'
            }),
            'customer_primary_email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'customer_primary_email'
            }),
            'customer_primary_phone': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'customer_primary_phone'
            }),
        }


class StoresForms(ModelForm):
    """Таблица Stores"""
    class Meta:
        """Поля таблицы"""
        model = Stores
        fields = (
            'transaction_store_id',
            'sku',
            'sku_purchase_price',
            'sku_retail_price'
        )

        widgets = {
            'transaction_store_id': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'transaction_store_id'
            }),
            'sku': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sku'
            }),
            'sku_purchase_price': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sku_purchase_price'
            }),
            'sku_retail_price': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sku_retail_price'
            }),
        }


class TransactionsForms(ModelForm):
    """Таблица Transactions"""
    class Meta:
        """Поля таблицы"""
        model = Transactions
        fields = (
            'transaction_id',
            'customer_card',
            'transaction_summ',
            'transaction_date_time',
            'transaction_store_id'
        )

        widgets = {
            'transaction_id': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'transaction_id'
            }),
            'customer_card': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'customer_card'
            }),
            'transaction_summ': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'transaction_summ'
            }),
            'transaction_date_time': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'transaction_date_time'
            }),
            'transaction_store_id': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'transaction_store_id'
            }),
        }
