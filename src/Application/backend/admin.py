"""Регистрация модели в админ панели"""
from django.contrib import admin
from .models import (Cards,
                     Checks,
                     DateReports,
                     Goods,
                     GroupsOfGoods,
                     PersonalData,
                     Stores,
                     Transactions
                     )

admin.site.register(Cards)
admin.site.register(Checks)
admin.site.register(DateReports)
admin.site.register(Goods)
admin.site.register(GroupsOfGoods)
admin.site.register(PersonalData)
admin.site.register(Stores)
admin.site.register(Transactions)
