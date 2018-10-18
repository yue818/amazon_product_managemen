#-*-coding:utf-8-*-
from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_store_configuration_file import t_store_configuration_file
import json, urllib
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: amazon_shop_search_Plugin.py
 @time: 2018/5/29 14:01
"""   
class amazon_shop_search_Plugin(BaseAdminPlugin):
    amazon_shop_search_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.amazon_shop_search_flag)

    def block_search_cata_nav(self, context, nodes):
        accountNames = t_store_configuration_file.objects.filter(ShopName__startswith='AMZ-').values('ShopName')
        buttonlist = []
        for obj in accountNames:
            buttonlist.append(obj['ShopName'])
        buttonlist.sort()

        flag = ''
        if self.request.GET.get('shopname', '') != 'all' and self.request.GET.get('shopname', '') != '':
            flag = self.request.GET.get('shopname', '')

        refreshstatus = t_store_configuration_file.objects.filter(ShopName__exact=flag).values('ShopName')
        if refreshstatus is None:
            refreshstatus = ''

        synurl = ''
        end_url = ''
        count_list = ['_p_advertising_status=ENABLED&_p_advertising_online_status=Selection_ad',
                      '_p_advertising_status=ENABLED&_p_advertising_online_status=Continuous_ad',
                      '_p_advertising_status=PAUSED&_p_advertising_online_status=Stoping_ad']
        if 't_template_amazon_advertising_business_count_report' in self.request.path:
            for count_tt in count_list:
                if count_tt in self.request.get_full_path():
                    end_url += '?' + count_tt

        synurl = self.request.path
        if end_url:
            synurl += end_url
        is_show = self.request.GET.get('is_single', '')
        if is_show == '':
            is_show = self.request.GET.get('is_viewed', '')
        if is_show == '':
            nodes.append(loader.render_to_string('amazon_shop_search_Plugin.html',
                                                 {'shopNames': json.dumps(buttonlist), 'flag': flag, 'synurl': synurl}))
