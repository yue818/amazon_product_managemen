#-*-coding:utf-8-*-

u"""
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: change_shipping_plugin.py
 @time: 2018-04-08 18:07
"""

from xadmin.views import BaseAdminPlugin
from django.template import loader
from urllib import unquote
import json
from django.template import RequestContext

class change_shipping_plugin(BaseAdminPlugin):
    change_shipping_flage = False

    def init_request(self, *args, **kwargs):
        return bool(self.change_shipping_flage)

    def block_search_cata_nav(self, context, nodes):

        nodes.append(loader.render_to_string('change_shipping_templates.html',{},context_instance=RequestContext(self.request)))


