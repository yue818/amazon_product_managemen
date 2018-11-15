# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_order_amazon_india import *
from django.contrib import messages

class t_shop_amazon_india_Admin(object):

    def shop_handlers(self,obj):
        shopName = obj.ShopName.replace('/','%2F')
        rt = u'<button id="application1" type="button" style="background-color:#428bca" ' \
             u'onclick="window.location.href=\'/Project/admin/skuapp/t_order_amazon_india/' \
             u'?_p_ShopName__exact=%s&FulfillmentChannel=MFN&applyTracking=0&OrderStatus=Unshipped\'">订单管理</button>'%shopName
        return mark_safe(rt)
    shop_handlers.short_description = '店铺操作'

    list_display = ('id', 'ShopName', 'UserAdress', 'Mobile', 'PostCode', 'Company','CountryCode',
                    'City','UserPhoneTel','ShopUserName', 'shop_handlers',)

    # def save_models(self):
    #     pass
