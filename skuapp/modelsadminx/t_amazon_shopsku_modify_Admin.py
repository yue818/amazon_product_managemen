# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_shopsku_modify_Admin.py
 @time: 2018/8/23 17:27
"""  
from datetime import datetime


class t_amazon_shopsku_modify_Admin(object):
    amazon_site_left_menu_tree_flag = True
    list_display = ('shop_name', 'seller_sku', 'sku_modify', 'modify_reason', 'modify_user','modify_time','update_user', 'update_time')
    search_fields = ('shop_name', 'seller_sku', 'sku_modify', 'modify_user','modify_time')
    list_filter = ('shop_name', 'seller_sku', 'sku_modify', 'modify_user','modify_time')

    def save_models(self):
        obj = self.new_obj
        request = self.request

        if obj is None or obj.id is None or obj.id <= 0:
            obj.modify_time = datetime.now()
            obj.modify_user = request.user.first_name
            obj.save()
        else:
            old_obj = self.model.objects.get(pk=obj.pk)
            old_obj.shop_name = obj.shop_name
            old_obj.seller_sku = obj.seller_sku
            old_obj.sku_modify = obj.sku_modify
            old_obj.modify_reason = obj.modify_reason
            old_obj.update_time = datetime.now()
            old_obj.update_user = request.user.first_name
            old_obj.save()