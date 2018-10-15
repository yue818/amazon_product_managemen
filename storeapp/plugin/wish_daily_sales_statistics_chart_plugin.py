#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: wish_daily_sales_statistics_chart_plugin.py
 @time: 2018/9/5 10:06
"""

from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging
import json
from urllib import urlencode
from django.contrib import messages

class wish_daily_sales_statistics_chart_plugin(BaseAdminPlugin):
    daily_sales_chart = False

    def init_request(self, *args, **kwargs):
        return bool(self.daily_sales_chart)

    def block_search_loaction_befor(self, context, nodes):
        request = self.request

        sales_objs = request.list_queryset.order_by('OrderDate')
        datelist,ofsaleslist = [], []
        for sales_obj in sales_objs:
            datelist.append(sales_obj.OrderDate.strftime('%Y-%m-%d'))
            ofsaleslist.append(float(sales_obj.OfSales))

        context_dict={
            'datelist': datelist,
            'ofsaleslist': ofsaleslist
        }

        nodes.append(loader.render_to_string('daily_sales_chart_content.html',context_dict, context_instance=RequestContext(self.request)))















