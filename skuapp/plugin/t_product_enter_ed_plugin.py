#-*-coding:utf-8-*-

"""
 @desc:
 @author: songguowu
 @site:
 @software: PyCharm
 @file: t_saler_profit_report_menu_Plugin.py
 @time: 2018-10-19 16:58
"""
import json
from xadmin.views import BaseAdminPlugin
from django.template import loader
class t_product_enter_ed_menu_Plugin(BaseAdminPlugin):
    t_product_enter_ed_menu_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.t_product_enter_ed_menu_flag)

    def block_search_cata_nav(self, context, nodes):

        t = self.request.GET.get('datetype', '')

        activeflag = t if t else '0'

        nodes.append(loader.render_to_string('t_product_enter_ed_menu.html',
                                             {'activeflag': activeflag}))