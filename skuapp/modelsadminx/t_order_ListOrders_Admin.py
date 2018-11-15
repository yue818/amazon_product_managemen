# -*- coding: utf-8 -*-
class t_order_ListOrders_Admin(object):

    list_display =('id', 'ShopName','RequestId','LastUpdatedAfter','LastUpdatedBefore','AmazonOrderId','Orders','UpdateTime')
    list_filter = ('ShopName','LastUpdatedAfter','LastUpdatedBefore','UpdateTime')
    search_fields = ('id', 'ShopName','RequestId','AmazonOrderId','Orders')