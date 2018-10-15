# -*- coding: utf-8 -*-
"""
 @desc: 用户自定义每页显示条数插件
 @author: fangyu
 @site:
 @software: PyCharm
 @file: show_per_pagePlugin.py
 @time: 2018/5/4 14:40
"""

from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages
from django.template import RequestContext

class show_per_page_Plugin(BaseAdminPlugin):
    show_per_page = False

    def init_request(self, *args, **kwargs):
        return bool(self.show_per_page)

    def block_show_page(self, context, nodes):
        perpage = self.request.GET.get('showperpage',20)
        nodes.append(loader.render_to_string('show_per_page.html',{"perpage":perpage},context_instance=RequestContext(self.request)))