#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_weekly_collar_and_pub_plugin.py
 @time: 2018-04-19 17:28
"""

from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging

from skuapp.table.public import *

logger = logging.getLogger('sourceDns.webdns.views')
from django.contrib import messages


class t_weekly_collar_and_pub_plugin(BaseAdminPlugin):
    weeklflag = False

    def init_request(self, *args, **kwargs):
        return bool(self.weeklflag)

    def block_search_cata_nav(self, context, nodes):
        Week_NolistTmp = self.model.objects.values_list('Week_No',flat=True)
        weeklist = sorted(set(Week_NolistTmp))
        weeklist.reverse()
        week = self.request.GET.get('_p_Week_No__contains','')
        nodes.append(loader.render_to_string('t_weekly_collar_and_pub_html.html',{'WeeKNo':weeklist,'weekno':week},
                                             context_instance=RequestContext(self.request)))

