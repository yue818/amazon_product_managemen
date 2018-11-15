# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: saler_profit_plugin.py
 @time: 2017-12-25 16:27

"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
from django.contrib import messages
import datetime, time


class saler_profit_plugin(BaseAdminPlugin):
    saler_profit = False

    def init_request(self, *args, **kwargs):
        return bool(self.saler_profit)

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]
        selmonth = self.request.GET.get('selmonth')
        if selmonth is None or selmonth == '':
            selmonth =  time.strftime('%Y-%m', time.localtime(time.time()))
        salerman = self.request.GET.get('salerman')
        shopname = self.request.GET.get('shopname')
        shopname = str(shopname)
        shopname = shopname.replace('~~!!','#')

        nodes.append(loader.render_to_string('saler_profit.html',{'selmonth': selmonth,'salerman': salerman,'shopname': shopname},context_instance=RequestContext(self.request)))