# -*- coding: utf-8 -*-


class t_amazon_ad_serving_status_Admin(object):
    list_display = ('id','ShopName','ShopType','AccountName','ShopSite','AdServingStatus','Remarks',)
    search_fields= ('id','ShopName','ShopType','AccountName','ShopSite','AdServingStatus','Remarks',)
    list_editable= ('ShopName','ShopType','AccountName','ShopSite','AdServingStatus','Remarks',)
    list_filter  = ('ShopName','ShopType','AccountName','ShopSite','AdServingStatus',)
    