# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_config_shop_alias_Admin.py
 @time: 2018/8/2 11:38
"""
from datetime import datetime


class t_config_shop_alias_Admin(object):
    amazon_site_left_menu_tree_flag = True
    list_display = ('ShopName', 'ShopAlias', 'CreateUser', 'CreateTime','UpdateUser','UpdateTime')
    search_fields = ('ShopName', 'ShopAlias',)

    def save_models(self):
        obj = self.new_obj
        request = self.request

        if obj is None or obj.id is None or obj.id <= 0:
            obj.CreateTime = datetime.now()
            obj.CreateName = request.user.first_name
            obj.save()
        else:
            old_obj = self.model.objects.get(pk=obj.pk)
            old_obj.ShopName = obj.ShopName
            old_obj.ShopAlias = obj.ShopAlias
            old_obj.UpdateTime = datetime.now()
            old_obj.UpdateUser = request.user.first_name
            old_obj.save()