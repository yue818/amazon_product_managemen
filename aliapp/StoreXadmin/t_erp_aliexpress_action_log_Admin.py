#-*-coding:utf-8-*-
from django.utils.safestring import mark_safe
from django.contrib import messages
from django_redis import get_redis_connection
from django.db import connection
import logging,json, re
import xadmin
from aliapp.models import *

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_erp_aliexpress_action_log_Admin.py
 @time: 2018/6/6 8:44
"""
class t_erp_aliexpress_action_log_Admin(object):
    site_left_menu_tree_flag_ali = True
    list_per_page = 20
    action_type_dict = {'synall': u'店铺商品全量同步', 'syn': u'商品信息同步', 'enable': u'商品上架',
                        'disable': u'商品下架', 'enableSKU': u'SKU上架', 'disableSKU': u'SKU下架',
                        'editStock': u'库存修改', 'editPrice': u'价格修改'}

    def show_action_type(self,obj):
        rt = ''
        for k,v in self.action_type_dict.items():
            if obj.action_type == k:
                rt = v
        return mark_safe(rt)

    show_action_type.short_description = mark_safe(u'<p align="center"style="color:#428bca;">操作类型</p>')

    def show_action_param(self,obj):
        rt = ''
        if obj.action_type == 'synall':
            pass
        else:
            if obj.action_param:
                action_param = json.loads(obj.action_param)
                product_id = ''
                if action_param.has_key('product_id'):
                    product_id = action_param['product_id']
                if product_id == '':
                    if obj.action_id and obj.action_id != 0:
                        t_erp_aliexpress_online_info_obj = t_erp_aliexpress_online_info.objects.filter(id=obj.action_id)
                        if t_erp_aliexpress_online_info_obj.exists():
                            product_id = t_erp_aliexpress_online_info_obj[0].product_id
                id_index = 0
                rt = ''
                count = len(str(product_id))/72
                if len(str(product_id))%72 != 0:
                    count += 1
                for i in range(0,count):
                    rt += str(product_id)[id_index:id_index+72] + "<br/>"
                    id_index = id_index + 72
        return mark_safe(rt)

    show_action_param.short_description = mark_safe(u'<p align="center"style="color:#428bca;">操作商品ID</p>')

    def show_action_userinfo(self,obj):
        rt = u'开始时间：' + obj.action_time.strftime("%Y-%m-%d %H:%M:%S")
        rt += u'<br/>完成时间：'
        if obj.done_time:
            rt += obj.done_time.strftime("%Y-%m-%d %H:%M:%S")
        rt += u'<br/>操作人：' + obj.action_user
        return mark_safe(rt)

    show_action_userinfo.short_description = mark_safe(u'<p align="center"style="color:#428bca;">操作详情</p>')

    def show_error_info(self,obj):
        rt = ''
        if bool(re.search('success', obj.action_result, re.IGNORECASE)) or u'成功' in obj.action_result:
            pass
        else:
            remark = obj.remark
            id_index = 0
            rt = ''
            count = len(str(remark)) / 72
            if len(str(remark)) % 72 != 0:
                count += 1
            for i in range(0, count):
                rt += str(remark)[id_index:id_index + 72] + "<br/>"
                id_index = id_index + 72
        return mark_safe(rt)

    show_error_info.short_description = mark_safe(u'<p align="center"style="color:#428bca;">错误详情</p>')

    list_display = ('show_action_type', 'accountName', 'show_action_param', 'action_result', 'show_error_info', 'show_action_userinfo',)
    # list_editable = ('Remarks')
    list_display_links = ('',)


    def get_list_queryset(self,):
        """显示可显示的，自己本人的"""
        request = self.request
        qs = super(t_erp_aliexpress_action_log_Admin, self).get_list_queryset()

        if self.request.user.is_superuser:
            pass
        else:
            print self.request.user.first_name
            qs = qs.filter(action_user=self.request.user.first_name)

        action_type = request.GET.get('action_type', '')
        if action_type:
            qs = qs.filter(action_type=action_type)

        return qs
