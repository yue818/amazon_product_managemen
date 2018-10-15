#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_wish_daily_sales_statistics_Admin.py
 @time: 2018/9/5 9:50
"""
from django.contrib import messages
from django.utils.safestring import mark_safe
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import transaction
from skuapp.table.t_online_info import t_online_info

class t_online_info_wish_low_inventory_admin(object):
    site_left_menu_tree_flag_wish = True
    def show_picture(self, obj):
        rt = '<img src="%s"  width="80" height="80"/>  ' % obj.Image
        return mark_safe(rt)
    show_picture.short_description = u'<span style="color: #428bca">图片<span>'

    list_display  = ['id', 'show_picture', 'ShopName', 'ProductID', 'Title', 'SKU', 'ShopSKU', 'Quantity']
    search_fields = ['id', 'Image', 'ShopName', 'ProductID', 'Title', 'SKU', 'ShopSKU', 'Quantity']
    list_filter   = ['Quantity','RefreshTime',]

    actions = ['to_modify_filtervalue',]

    def to_modify_filtervalue(self, request, objs):
        transaction.set_autocommit(False)
        try:
            for obj in objs:
                # 更新 online 信息
                t_online_info.objects.filter(ProductID=obj.ProductID,ShopSKU=obj.ShopSKU).update(filtervalue=-1)
                # 删除 低库存表信息
                obj.delete()
            transaction.commit()
        except Exception as error:
            transaction.rollback()
            messages.error(request, u'清除错误！请将此截图发给IT人员。error: {}'.format(error))

    to_modify_filtervalue.short_description = u'清除营销SKU'



    def get_list_queryset(self,):
        request = self.request
        qs = super(t_online_info_wish_low_inventory_admin, self).get_list_queryset()
        if request.user.is_superuser:
            return qs
        else:
            userID = [each.id for each in User.objects.filter(groups__id__in=[38])]
            if request.user.id in userID:
                return qs
            objs = t_store_configuration_file.objects.filter(
                Q(Seller=request.user.first_name) | Q(Published=request.user.first_name) | Q(
                    Operators=request.user.first_name)).values('ShopName_temp')
            if objs.exists():
                shoplist = []
                for obj in objs:
                    shoplist.append(obj['ShopName_temp'])
                return qs.filter(ShopName__in=shoplist)
            else:
                return qs.none()
