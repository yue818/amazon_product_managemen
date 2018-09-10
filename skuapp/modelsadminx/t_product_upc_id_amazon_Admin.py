#-*-coding:utf-8-*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_product_upc_id_amazon import *
from datetime import datetime
from django.utils.safestring import mark_safe
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_product_upc_id_amazon_Admin.py
 @time: 2018/3/26 17:34
"""   
class t_product_upc_id_amazon_Admin(object):
    product_upc_amazon_flag = True

    def show_status(self, obj):
        if obj.use_status == '1':
            rt = u'未使用'
        else:
            rt = u'已使用'
        return mark_safe(rt)
    show_status.short_description = u'使用状态'

    list_display = ('id', 'external_product_id', 'external_product_id_type', 'show_status')
    fields = ('id', 'external_product_id',)

    def save_models(self):
        import xlrd
        request = self.request
        external_product_id_file = request.FILES.get('external_product_id_file','')
        wb = xlrd.open_workbook(
            filename=None, file_contents=external_product_id_file.read())
        table = wb.sheets()[0]
        nrows = table.nrows
        insert_values = []
        for rownum in xrange(1, nrows):
            row = table.row_values(rownum)
            if row[0]:
                external_product_id = str(row[0])
                if '.' in external_product_id:
                    external_product_id = external_product_id.split('.')[0]
                insert_values.append(t_product_upc_id_amazon(external_product_id = external_product_id, external_product_id_type = row[1], use_status='1',
                                                             createTime=datetime.now(), createUser=request.user.first_name))
        t_product_upc_id_amazon.objects.bulk_create(insert_values)






