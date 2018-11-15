# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from datetime import datetime
        
        
class t_store_summary_of_sales_profit_data_Admin(object):
    list_display =('id','DepartmentID','ShopName','ShopAccount','StartTime','EndTime','Seller','Sales','PaidProfits','ProfitMargins','PreviouSales','Increase','GrowthRate','Remarks','CreateStaffName','CreateTime',)
    search_fields = ('DepartmentID','ShopName','ShopAccount','Seller','Sales','PaidProfits','ProfitMargins','PreviouSales','Increase','GrowthRate','Remarks','CreateStaffName',)
    list_filter =('DepartmentID','ShopName','ShopAccount','StartTime','EndTime','Seller','Sales','PaidProfits','ProfitMargins','PreviouSales','Increase','GrowthRate','CreateStaffName','CreateTime',)
    list_display_links = ('id')
    list_editable = ('DepartmentID','ShopName','ShopAccount','StartTime','EndTime','Seller','Sales','PaidProfits','ProfitMargins','PreviouSales','Increase','GrowthRate','Remarks',)



    fields = ('ShopName','ShopAccount','DepartmentID',
              'Seller','Sales','PaidProfits',
              'ProfitMargins','PreviouSales',
              'Increase','GrowthRate',
              'Remarks',
              )
              
    readonly_fields = ('StartTime','EndTime','CreateStaffName','CreateTime',)

    form_layout = (
        Fieldset(u'销售额利润数据汇总',
                    Row('ShopName','ShopAccount',),
                    Row('Seller','DepartmentID',),
                    Row('Sales','PaidProfits',),
                    Row('ProfitMargins','PreviouSales',),
                    Row('Increase','GrowthRate',),
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