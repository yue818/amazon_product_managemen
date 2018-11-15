# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from datetime import datetime


class t_store_status_Admin(object):
    list_display = ('id','DepartmentID','ShopName','Seller','StoreStatus','AccountName','AccountNote','PaymentSituation','PaymentRemarks','AccountNumber','AccountManager','CardNumber','ShopOperationsNote','CreateStaffName','CreateTime',)
    list_filter = ('DepartmentID','ShopName','StoreStatus','AccountName','AccountNote','PaymentSituation','PaymentRemarks','Seller','AccountNumber','AccountManager','CardNumber','ShopOperationsNote','CreateStaffName','CreateTime',)
    search_fields = ('id','DepartmentID','ShopName','StoreStatus','AccountName','AccountNote','PaymentSituation','PaymentRemarks','Seller','AccountNumber','AccountManager','CardNumber','ShopOperationsNote','CreateStaffName',)
    list_editable = ('ShopName','StoreStatus','AccountName','AccountNote','PaymentSituation','PaymentRemarks','Seller','AccountNumber','AccountManager','CardNumber','ShopOperationsNote',)

    
    fields = ('ShopName','Seller','StoreStatus','DepartmentID',
              'AccountName','AccountNote',
              'PaymentSituation','PaymentRemarks',
              'AccountNumber','AccountManager','CardNumber',
              'ShopOperationsNote', 
              )
              
    readonly_fields = ('CreateStaffName','CreateTime',)

    form_layout = (
        Fieldset(u'店铺状态',
                    Row('ShopName','StoreStatus',),
                    Row('Seller','DepartmentID',),
                    Row('AccountName','PaymentSituation',),
                    Row('AccountNote','PaymentRemarks',),
                    Row('AccountNumber',),
                    Row('AccountManager','CardNumber',),
                    Row('ShopOperationsNote'),

                    css_class = 'unsort'
                ),
                  )
    def save_models(self):
        obj = self.new_obj
        request = self.request
        if obj is None or obj.id is None or obj.id <=0:
            obj.CreateStaffName = request.user.first_name
            obj.CreateTime = datetime.now()

        obj.save()