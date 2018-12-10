# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: amazon_left_menu_tree_plugin.py
 @time: 2018/12/10 10:46
"""
import json

from django.template import RequestContext
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.db.models import Q


class amazon_left_menu_tree_plugin(BaseAdminPlugin):
    amazon_left_menu_tree_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.amazon_left_menu_tree_flag)

    def block_left_navbar(self, context, nodes):

        shop_cfg = {
                "name": u"店铺信息配置",
                "code": "11",
                "parentCode": "01",
                "icon": "icon-th",
                "selected": "",
                "to_url": "",
                "flag": "",
                "child": [
                    {
                        "name": u"发货地址配置",
                        "icon": "",
                        "code": "1101",
                        "parentCode": "11",
                        "selected": "",
                        "to_url": '/Project/admin/amazon_app/t_amazon_fba_inbound_address_cfg',
                        "flag": 'inbound_address_cfg',
                        "child": []
                    },
                ]
        }

        fba_inbound_flow = {
                "name": u"入库流程",
                "code": "12",
                "parentCode": "01",
                "icon": "icon-th",
                "selected": "",
                "to_url": "",
                "flag": "",
                "child": [
                    {
                        "name": u"入库计划",
                        "icon": "",
                        "code": "1201",
                        "parentCode": "12",
                        "selected": "",
                        "to_url": '/Project/admin/amazon_app/t_amazon_fba_inbound_plan',
                        "flag": 'fba_inbound_plan',
                        "child": []
                    },

                    {
                        "name": u"亚马逊规划",
                        "icon": "",
                        "code": "1202",
                        "parentCode": "12",
                        "selected": "",
                        "to_url": '/Project/admin/amazon_app/t_amazon_fba_inbound_plan',
                        "flag": '',
                        "child": []
                    },

                    {
                        "name": u"提交入库",
                        "icon": "",
                        "code": "1203",
                        "parentCode": "12",
                        "selected": "",
                        "to_url": '/Project/admin/amazon_app/t_amazon_fba_inbound_plan',
                        "flag": '',
                        "child": []
                    },



                    {
                        "name": u"货件追踪",
                        "icon": "",
                        "code": "1204",
                        "parentCode": "12",
                        "selected": "",
                        "to_url": '/Project/admin/amazon_app/t_amazon_fba_inbound_plan',
                        "flag": '',
                        "child": []
                    },
                ]
        }

        inbound_check = {
            "name": u"入库稽核",
            "code": "13",
            "parentCode": "01",
            "icon": "icon-th",
            "selected": "",
            "to_url": "",
            "flag": "",
            "child": [
                {
                    "name": u"我方入库",
                    "icon": "",
                    "code": "1301",
                    "parentCode": "13",
                    "selected": "",
                    "to_url": '/Project/admin/amazon_app/t_amazon_fba_inbound_plan',
                    "flag": '',
                    "child": []
                },

                {
                    "name": u"亚马逊接收",
                    "icon": "",
                    "code": "1302",
                    "parentCode": "13",
                    "selected": "",
                    "to_url": '/Project/admin/amazon_app/t_amazon_fba_inbound_plan',
                    "flag": '',
                    "child": []
                },

                {
                    "name": u"入库-接收差异",
                    "icon": "",
                    "code": "1303",
                    "parentCode": "13",
                    "selected": "",
                    "to_url": '/Project/admin/amazon_app/t_amazon_fba_inbound_plan',
                    "flag": '',
                    "child": []
                },


            ]

        }

        menu_list = [
            {
                "name": u"FBA入库",
                "code": "01",
                "icon": "icon-th",
                "selected": "",
                "to_url": "",
                "flag": "",
                "child": [
                        shop_cfg,
                        fba_inbound_flow,
                        inbound_check,
                ]
            },
        ]

        flag = ''
        if 't_amazon_fba_inbound_address_cfg' in self.request.get_full_path():
            flag = 'inbound_address_cfg'
        elif 't_amazon_fba_inbound_plan' in self.request.get_full_path():
            flag = 'fba_inbound_plan'

        show_flag = 0
        for menu_obj in menu_list:
            if menu_obj['flag'] == flag:
                menu_obj['selected'] = 'selected'
                show_flag = 1
            if not menu_obj['child']:
                continue
            for menu_o in menu_obj['child']:
                if not menu_o:
                    continue
                if menu_o['flag'] == flag:
                    menu_o['selected'] = 'selected'
                    show_flag = 1
                if menu_o['child']:
                    for menu_ in menu_o['child']:
                        if not menu_:
                            continue
                        if menu_['flag'] == flag:
                            menu_['selected'] = 'selected'
                            show_flag = 1
                        if menu_['child']:
                            for menu_l in menu_['child']:
                                if not menu_l:
                                    continue
                                if menu_l['flag'] == flag:
                                    menu_l['selected'] = 'selected'
                                    show_flag = 1

        # if show_flag == 1:
        # messages.error(self.request, 'count-------%s' % self.request.result_count)
        nodes.append(loader.render_to_string('site_left_menu_tree_Plugin.html', {'menu_list': json.dumps(menu_list)}, context_instance=RequestContext(self.request)))
