#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: changyang  
 @site: 
 @software: PyCharm
 @file: t_wishpb_syncdata_Plugin.py
 @time: 2018-08-25 14:37
"""

from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_config_online_amazon import t_config_online_amazon
import json

class t_wishpb_syncdata_Plugin(BaseAdminPlugin):
    t_wishpb_syncdata_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.t_wishpb_syncdata_flag)

    def block_search_cata_nav(self, context, nodes):
        current_shop = self.request.GET.get('Shopname', '')
        if not current_shop:
            current_shop = 'Wish-0000'

        ShopNames = t_config_online_amazon.objects.filter(K='access_token').values('Name')
        buttonlist = [v['Name'] for v in ShopNames]
        buttonlist.sort()

        nodes.append(loader.render_to_string('t_wishpb_syncdata.html', {'objs': json.dumps(buttonlist),
                                                                                  'flag': current_shop, }))