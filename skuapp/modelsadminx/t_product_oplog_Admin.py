# -*- coding: utf-8 -*-
class t_product_oplog_Admin(object):
    list_per_page=50
    list_display=('id','MainSKU','Name2','OpID','OpName','StepID','StepName','BeginTime','EndTime','pid',)
    #list_display_links=('id','MainSKU','Name2','OpID','OpName','StepID','StepName','BeginTime','EndTime','pid',)
    readonly_fields = ('id','MainSKU','Name2','OpID','OpName','StepID','StepName','BeginTime','EndTime','pid',)
    search_fields=('id','MainSKU','Name2','OpID','OpName','StepID','StepName','pid',)
    list_filter = ('BeginTime','EndTime',)