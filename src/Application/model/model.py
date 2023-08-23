"""Модель в MVC"""
import csv

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from logger.logger import _logger


class Model():
    """Основной класс для реализации proposals"""

    def __init__(self):
        self.engine = create_engine(self.get_url())
        self.data = {'table': '',
                     'table_head': ''}

    def get_url(self):
        url = URL.create(
            drivername='postgresql',
            database='postgres',
            username='postgres',
            password='postgres',
            host='s21_retail_db',
            port='5432'
        )
        return url

    def model_proposals(self, request):
        if 'proposals_1' in request.POST:
            self.proposals_1(request)
        if 'proposals_2' in request.POST:
            self.proposals_2(request)
        if 'proposals_3' in request.POST:
            self.proposals_3(request)
        if 'proposals_csv_1' in request.POST:
            self.proposals_1(request)
            self.create_csv('proposals_1')
        if 'proposals_csv_2' in request.POST:
            self.proposals_2(request)
            self.create_csv('proposals_2')
        if 'proposals_csv_3' in request.POST:
            self.proposals_3(request)
            self.create_csv('proposals_3')

    def proposals_1(self, request):
        connection = self.engine.raw_connection()
        cursor_obj = connection.cursor()
        try:
            cursor_obj.callproc('fnc_personal_offers_average_check',
                                [int(request.POST.get('method_1')),
                                 request.POST.get('first_date_1'),
                                 request.POST.get('last_date_1'),
                                 int(request.POST.get('coutn_transaction_1')),
                                 float(request.POST.get('zoom_factor_1')),
                                 int(request.POST.get('outflow_index_1')),
                                 int(request.POST.get('share_transaction_1')),
                                 int(request.POST.get('share_margin_1'))])
            self.data['table_head'] = ['Customer_ID',
                                       'Required_Check_Measure',
                                       'Group_Name',
                                       'Offer_Discount_Depth']
            self.data['table'] = cursor_obj.fetchall()
        except Exception as err:
            _logger.warning(str(err))
        cursor_obj.close()

    def proposals_2(self, request):
        connection = self.engine.raw_connection()
        cursor_obj = connection.cursor()
        try:
            cursor_obj.callproc('fnc_offer_customer_frequency',
                                [request.POST.get('first_date_2'),
                                 request.POST.get('last_date_2'),
                                 int(request.POST.get('coutn_transaction_2')),
                                 float(request.POST.get('outflow_index_2')),
                                 float(request.POST.get(
                                     'share_transaction_2')),
                                 float(request.POST.get('share_margin_2'))])
            self.data['table_head'] = ['Customer_ID',
                                       'Start_Date',
                                       'End_Date',
                                       'Required_Transactions_Count',
                                       'Group_Name',
                                       'Offer_Discount_Depth']
            self.data['table'] = cursor_obj.fetchall()
        except Exception as err:
            _logger.warning(str(err))
        cursor_obj.close()

    def proposals_3(self, request):
        connection = self.engine.raw_connection()
        cursor_obj = connection.cursor()
        try:
            cursor_obj.callproc('fnc_offer_cross_selling',
                                [int(request.POST.get('coutn_group_3')),
                                 float(request.POST.get('outflow_index_3')),
                                 float(request.POST.get('stability_index_3')),
                                 float(request.POST.get('share_sku_3')),
                                 float(request.POST.get('share_margin_3'))])
            self.data['table_head'] = ['Customer_ID',
                                       'SKU_Name',
                                       'Offer_Discount_Depth']
            self.data['table'] = cursor_obj.fetchall()
        except Exception as err:
            _logger.warning(str(err))
        cursor_obj.close()

    def create_csv(self, file_name):
        with open(f'export/{file_name}.csv', 'wt',
                  encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=',',
                                quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(self.data['table_head'])
            for row in self.data['table']:
                writer.writerow(row)

    def model_result(self):
        return self.data
