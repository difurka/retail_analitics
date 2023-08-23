"""Классы всех таблиц проекта"""
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete`
#     set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django
#     to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values
#    or field names.
from django.db import models


class Cards(models.Model):
    """Таблица Cards"""
    customer_card_id = models.BigIntegerField(primary_key=True)
    customer = models.ForeignKey(
        'PersonalData', models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return str(self.customer_card_id)

    def get_absolute_url(self):
        return '/data/crud/view_cards'

    class Meta:
        managed = False
        db_table = 'cards'


class Checks(models.Model):
    """Таблица Checks"""
    transaction = models.ForeignKey(
        'Transactions', models.DO_NOTHING, primary_key=True, blank=True)
    sku = models.ForeignKey('Goods', models.DO_NOTHING, blank=True, null=True)
    sku_amount = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True)
    sku_summ = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True)
    sku_summ_paid = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True)
    sku_discount = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return str(self.transaction_id)

    def get_absolute_url(self):
        return '/data/crud/view_checks'

    class Meta:
        managed = False
        db_table = 'checks'


class DateReports(models.Model):
    """Таблица DateReports"""
    analysis_formation = models.DateField(
        primary_key=True, blank=True)

    def __str__(self):
        return str(self.analysis_formation)

    def get_absolute_url(self):
        return '/data/crud/view_date_reports'

    class Meta:
        managed = False
        db_table = 'date_reports'


class Goods(models.Model):
    """Таблица Goods"""
    sku_id = models.BigIntegerField(primary_key=True)
    sku_name = models.CharField(blank=True, null=True)
    group = models.ForeignKey(
        'GroupsOfGoods', models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return str(self.sku_id)

    def get_absolute_url(self):
        return '/data/crud/view_goods'

    class Meta:
        managed = False
        db_table = 'goods'


class GroupsOfGoods(models.Model):
    """Таблица GroupsOfGoods"""
    group_id = models.BigIntegerField(primary_key=True)
    group_name = models.CharField(blank=True, null=True)

    def __str__(self):
        return str(self.group_id)

    def get_absolute_url(self):
        return '/data/crud/view_groups_of_goods'

    class Meta:
        managed = False
        db_table = 'groups_of_goods'


class PersonalData(models.Model):
    """Таблица PersonalData"""
    customer_id = models.BigIntegerField(primary_key=True)
    customer_name = models.CharField(blank=True, null=True)
    customer_surname = models.CharField(blank=True, null=True)
    customer_primary_email = models.CharField(blank=True, null=True)
    customer_primary_phone = models.CharField(blank=True, null=True)

    def __str__(self):
        return str(self.customer_id)

    def get_absolute_url(self):
        return '/data/crud/view_personal_data'

    class Meta:
        managed = False
        db_table = 'personal_data'
        unique_together = (('customer_name',
                            'customer_surname',
                            'customer_primary_email',
                            'customer_primary_phone'),)


class Stores(models.Model):
    """Таблица Stores"""
    transaction_store_id = models.BigIntegerField(
        primary_key=True, blank=True)
    sku = models.ForeignKey(Goods, models.DO_NOTHING, blank=True, null=True)
    sku_purchase_price = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True)
    sku_retail_price = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return str(self.transaction_store_id)

    def get_absolute_url(self):
        return '/data/crud/view_stores'

    class Meta:
        managed = False
        db_table = 'stores'


class Transactions(models.Model):
    """Таблица Transactions"""
    transaction_id = models.BigIntegerField(primary_key=True)
    customer_card = models.ForeignKey(
        Cards, models.DO_NOTHING, blank=True, null=True)
    transaction_summ = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True)
    transaction_date_time = models.DateTimeField(blank=True, null=True)
    transaction_store_id = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.transaction_id)

    def get_absolute_url(self):
        return '/data/crud/view_transactions'

    class Meta:
        managed = False
        db_table = 'transactions'
