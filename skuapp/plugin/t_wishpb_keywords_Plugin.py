#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wishpb_keywords_Plugin.py
 @time: 2018-06-02 17:03
"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_config_online_amazon import t_config_online_amazon

class t_wishpb_keywords_Plugin(BaseAdminPlugin):
    search_wishpb_keywords = False

    def init_request(self, *args, **kwargs):
        return bool(self.search_wishpb_keywords)

    def block_after_fieldsets(self, context, nodes):
        config_objs = t_config_online_amazon.objects.filter(Name='Wish-0001', K='access_token')
        access_token = ''
        if config_objs.exists():
            access_token = config_objs[0].V

        lastkey = self.request.session.get('lastkey', '')

        nodes.append(loader.render_to_string('t_wishpb_keywords.html', {'access_token': access_token, 'lastkey': lastkey,}))