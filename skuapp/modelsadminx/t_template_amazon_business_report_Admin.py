#-*-coding:utf-8-*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from django.contrib import messages
import decimal
from skuapp.table.t_template_amazon_business_report import t_template_amazon_business_report


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_template_amazon_business_report_Admin.py
 @time: 2018/8/16 11:01
"""
class t_template_amazon_business_report_Admin(object):
    list_display = ('parent_ASIN', 'child_ASIN', 'ShopSKU', )

    list_display_links = ('id',)

    fields = ('upload_file',)

    def save_models(self):
        from datetime import datetime
        import csv
        obj = self.new_obj

        request = self.request
        user_name = request.user.first_name
        # try:
        i = 0
        for row in csv.reader(obj.upload_file):
            if i < 1:
                i += 1
                continue
            if row:
                obj = t_template_amazon_business_report()
                obj.parent_ASIN = str(row[0])
                obj.child_ASIN = str(row[1])
                obj.item_name = str(row[2])
                obj.ShopSKU = str(row[3])
                obj.visit_count = int(row[4].replace(',', ''))
                obj.visit_percent = str(row[5])
                obj.viewed_count = int(row[6].replace(',', ''))
                obj.viewed_percent = str(row[7])
                obj.buyed_button_percent = str(row[8])
                obj.ordered_count = int(row[9].replace(',', ''))
                obj.ordered_count_Conversion_rate = str(row[10])
                obj.ordered_sales = decimal.Decimal("%.2f" % float(row[11].replace('US$', '')))
                obj.ordered_types = int(row[12].replace(',', ''))
                obj.upload_file = ''
                obj.upload_time = datetime.now()
                obj.upload_user = user_name
                obj.update_user = ''
                obj.update_time = None
                obj.save()
            i += 1
        # except Exception, e:
        #     messages.error(request, u'李杨杨')