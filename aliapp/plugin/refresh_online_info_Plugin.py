#-*-coding:utf-8-*-
from xadmin.views import BaseAdminPlugin
from django.template import loader
from aliapp.models import t_erp_aliexpress_shop_info, t_erp_aliexpress_config_category
import json, urllib
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: refresh_online_info_Plugin.py
 @time: 2018/5/29 14:01
"""
import inspect

def check_permission_legality(self):
    """
    :param self:
    :return:
    """
    funcName = inspect.stack()[1][3]
    permname = '{}.Can_{}_{}'.format(self.model._meta.app_label, self.model._meta.model_name, funcName)
    if self.request.user.is_superuser or self.request.user.has_perm(permname):
        return True
    return False



class refresh_online_info_Plugin(BaseAdminPlugin):
    refresh_online_info_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.refresh_online_info_flag)


    def shopsku_operation(self):
        if check_permission_legality(self):
            return '1'
        else:
            return '0'

    def block_search_cata_nav(self, context, nodes):
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=self.request.user.username,
                                                   urltable="t_config_mstsc").count()
        except:
            pass
        t_erp_aliexpress_shop_info_obj = t_erp_aliexpress_shop_info.objects.filter(shop_status='online').values('seller_zh', 'shopName')
        if self.request.user.is_superuser or flag != 0:
            pass
        else:
            print self.request.user.first_name
            t_erp_aliexpress_shop_info_obj = t_erp_aliexpress_shop_info_obj.filter(seller_zh=self.request.user.first_name)
        accountNames = t_erp_aliexpress_shop_info_obj.values('shopName')
        buttonlist = []
        for obj in accountNames:
            buttonlist.append(obj['shopName'])
        buttonlist.sort()

        flag = ''
        # accountName = ''
        if self.request.GET.get('shopname', '') != 'all' and self.request.GET.get('shopname', '') != '':
            flag = self.request.GET.get('shopname', '')
        #     accountNames = t_erp_aliexpress_shop_info.objects.filter(shopName=flag).values('accountName')
        #     if accountNames.exists():
        #         accountName = accountNames[0]['accountName']
        # elif self.request.GET.get('accountName', '') != 'all' and self.request.GET.get('accountName', '') != '':
        #     accountName = self.request.GET.get('accountName', '')
        #     shopnames = t_erp_aliexpress_shop_info.objects.filter(accountName=accountName).values('shopName')
        #     if shopnames.exists():
        #         flag = shopnames[0]['shopName']

        refreshstatus = t_erp_aliexpress_shop_info.objects.filter(shopName=flag).values('shopName')
        if refreshstatus is None:
            refreshstatus = ''

        synurl = ''
        if flag and refreshstatus:
            synurl = self.request.path + 'refresh_ali_online_info_by_shopname/?shopname=%s' % flag
        else:
            flag = 'all'

        category = ''
        category_id = ''
        synurl_cata = self.request.get_full_path()
        if self.request.GET.get('category', '') != '':
            category_id = urllib.unquote(self.request.GET.get('category', ''))
            category = t_erp_aliexpress_config_category.objects.filter(category_id=category_id).values('full_path_en')
            if category.exists():
                category = category[0]['full_path_en']
            else:
                category = ''
            params = synurl_cata.split('/?')[1].split('&')
            param_temp = ''
            for param_each in params:
                if 'category' in param_each:
                    pass
                else:
                    param_temp += param_each + '&'
            synurl_cata = self.request.path + '?' + param_temp[:-1]
        category_list = {}
        t_erp_aliexpress_config_category_obj = t_erp_aliexpress_config_category.objects.filter(is_leaf=1).values('category_id','full_path_en')
        for category_obj in t_erp_aliexpress_config_category_obj:
            if category_obj:
                category_list[category_obj['category_id']] = category_obj['full_path_en'].replace("'","`")

        off_shelf_flag = 0
        if synurl_cata.find('t_erp_aliexpress_online_info_shelf') >= 0:
            off_shelf_flag = 1

        nodes.append(loader.render_to_string('refresh_online_info_plugin.html',
                                             {'shopNames': json.dumps(buttonlist), 'flag': flag, 'synurl': synurl,
                                              'category_list': json.dumps(category_list), 'category_id': category_id,
                                              'category': category, 'synurl_cata': synurl_cata,'Permission':self.shopsku_operation(),
                                              'off_shelf_flag': off_shelf_flag
                                              }))
