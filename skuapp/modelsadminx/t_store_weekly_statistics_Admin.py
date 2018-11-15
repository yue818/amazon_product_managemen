# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from datetime import datetime

    
class t_store_weekly_statistics_Admin(object):
    list_display =('id','DepartmentID','ShopName','ShopAccount','InvoiceTime','PromotionCosts','TrafficCosts','SpendSubtotal','RefundAmount','OtherFee','TotalSales','AmountMoney','Remarks','CreateStaffName','CreateTime',)
    search_fields = ('DepartmentID','ShopName','ShopAccount','PromotionCosts','TrafficCosts','SpendSubtotal','RefundAmount','OtherFee','TotalSales','AmountMoney','Remarks','CreateStaffName',)
    list_filter =('DepartmentID','InvoiceTime','PromotionCosts','TrafficCosts','SpendSubtotal','RefundAmount','OtherFee','TotalSales','AmountMoney','Remarks','CreateStaffName','CreateTime',)
    list_display_links = ('id')
    list_editable = ('DepartmentID','ShopName','ShopAccount','InvoiceTime','PromotionCosts','TrafficCosts','SpendSubtotal','RefundAmount','OtherFee','TotalSales','AmountMoney','Remarks',)



    fields = ('ShopName','ShopAccount','DepartmentID',
              'PromotionCosts','TrafficCosts',
              'SpendSubtotal','OtherFee','TotalSales',
              'Remarks',
              )
              
    readonly_fields = ('CreateStaffName','CreateTime','InvoiceTime',)

    form_layout = (
        Fieldset(u'店铺费用周统计表',
                    Row('ShopName','ShopAccount','DepartmentID',),
                    Row('PromotionCosts','TrafficCosts',),
                    Row('OtherFee','SpendSubtotal',),
                    Row('TotalSales',),
                    Row('Remarks',),
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