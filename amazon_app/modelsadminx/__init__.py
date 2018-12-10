# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: __init__.py
 @time: 2018/12/10 10:21
"""  
from datetime import datetime


class t_config_shop_alias_Admin(object):
    amazon_site_left_menu_tree_flag = True
    search_box_flag = True
    list_display = ('ShopName', 'ShopAlias', 'ShopType', 'ShopStatus', 'CreateUser', 'CreateTime', 'Remark', )
    # search_fields = ('ShopName', 'ShopAlias',)
    list_editable = ('ShopType', 'ShopStatus')

    def save_models(self):
        obj = self.new_obj
        request = self.request

        if obj is None or obj.id is None or obj.id <= 0:
            obj.CreateUser = request.user.username
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

    def get_list_queryset(self, ):
        request = self.request
        ShopName = request.GET.get('ShopName', '')
        ShopAlias = request.GET.get('ShopAlias', '')
        ShopType = request.GET.get('ShopType', '')
        ShopStatus = request.GET.get('ShopStatus', '')

        qs = super(t_config_shop_alias_Admin, self).get_list_queryset()

        searchList = {'ShopName__icontains': ShopName,
                      'ShopAlias__icontains': ShopAlias,
                      'ShopType__exact': ShopType,
                      'ShopStatus__exact': ShopStatus,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and str(v).strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'Please enter the correct content!')
        return qs