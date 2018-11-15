# -*- coding: utf-8 -*-

class t_upload_statistics_table_Admin(object):
    upload_statistics = True
    list_display = ('staTime','UplLoad_nub','Upload_suc_nub','Shop_nub','SKU_nub','online_nub','order_nub','order_rate','orderofeday','orders','soldofeay','sold','Integrity_nub',)
    list_filter = ('staTime','UplLoad_nub','Upload_suc_nub','Shop_nub','SKU_nub','online_nub','order_nub','order_rate','orderofeday','orders','soldofeay','sold','Integrity_nub',)
    #search_fields = ('id','UplLoad_nub','Shop_nub','SKU_nub','online_nub','order_nub','order_rate','orderofeday','orders','soldofeay','sold','Integrity_nub',)