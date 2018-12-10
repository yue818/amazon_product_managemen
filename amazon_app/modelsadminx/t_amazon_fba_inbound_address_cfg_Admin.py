# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_fba_inbound_address_cfg_Admin.py
 @time: 2018/12/10 10:23
"""  
from datetime import datetime


class t_amazon_fba_inbound_address_cfg_Admin(object):
    amazon_left_menu_tree_flag = True
    search_box_flag = True
    list_display = ('id', 'shop_name', 'country', 'province', 'city', 'name', 'postal_code', 'address1', 'address2', 'insert_time', 'insert_user')
    # list_editable = ()

    def save_models(self):
        obj = self.new_obj
        request = self.request

        if obj is None or obj.id is None or obj.id <= 0:
            obj.insert_user = request.user.username
            obj.insert_time = datetime.now()
            obj.save()
        else:
            old_obj = self.model.objects.get(pk=obj.pk)
            old_obj.country = obj.country
            old_obj.province = obj.province
            old_obj.city = obj.city
            old_obj.name = obj.name
            old_obj.postal_code = obj.postal_code
            old_obj.address1 = obj.address1
            old_obj.address2 = obj.address2
            old_obj.update_time = datetime.now()
            old_obj.update_user = request.user.first_name
            old_obj.save()

