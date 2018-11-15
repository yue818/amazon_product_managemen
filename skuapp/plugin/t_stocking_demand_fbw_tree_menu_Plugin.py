#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fbw_tree_menu_Plugin.py
 @time: 2018-10-11
"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_stocking_demand_fbw import t_stocking_demand_fbw
from skuapp.table.t_stocking_demand_fbw_management import t_stocking_demand_fbw_management
from skuapp.table.t_stocking_demand_fbw_all import t_stocking_demand_fbw_all
import json
from django.contrib import messages

class t_stocking_demand_fbw_tree_menu_Plugin(BaseAdminPlugin):
    fbw_tree_menu_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.fbw_tree_menu_flag)

    def validation_url_selected(self, menu_list, new_sourceurl, show_flag):
        flag = 0
        for menu_obj in menu_list:
            to_url = menu_obj['to_url']
            menu_child_obj = menu_obj['child']
            if len(menu_child_obj) > 0:
                new_menu_list, flag, show_flag = self.validation_url_selected(menu_child_obj, new_sourceurl, show_flag)
                if flag == 1:
                    show_flag = 1
                    menu_obj['selected'] = 'selected'
            else:
                if to_url != new_sourceurl:
                    if '?' not in menu_obj['to_url']:
                        to_url = to_url + '?'
                if to_url in new_sourceurl:
                    menu_obj['selected'] = 'selected'
                    flag = 1
                    break
        return menu_list, flag, show_flag

    def block_left_navbar(self, context, nodes):
        try:
            #'未生成清单':'notyet','已生成清单':'genbatch','已生成备货需求':'gendemand','已发货':'deliver','废弃':'nodemand'
            notyet_count = t_stocking_demand_fbw.objects.filter(Status='notyet').count()#
            nodemand_count = t_stocking_demand_fbw.objects.filter(Status='nodemand').count()  #
            genbatch_count = t_stocking_demand_fbw.objects.filter(Status='genbatch').count()  #
            gendemand_count = t_stocking_demand_fbw.objects.filter(Status='gendemand').count()  #
            deliver_count = t_stocking_demand_fbw.objects.filter(Status='deliver').count()  #
            manage_count = t_stocking_demand_fbw_management.objects.filter().count()  #
            allCount = t_stocking_demand_fbw_all.objects.filter().count()  #
            menu_list = [{
                "name": u"FBW发货流程",
                "code": "IPMAIN",
                "icon": "icon-th",
                "selected": "",
                "to_url": "",
                "child": [
                    {
                        "name": u"备发货数据",
                        "code": "DELIVER",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "",
                        "child": [
                            {
                                "name": u"发货列表(" + str(notyet_count) + ")",
                                "icon": "",
                                "code": "DELIVERLIST",
                                "parentCode": "DELIVER",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fbw/?Status=notyet",
                                "child": []
                            },
                            {
                                "name": u"废弃(" + str(nodemand_count) + ")",
                                "icon": "",
                                "code": "DELIVERGIVEUP",
                                "parentCode": "DELIVER",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fbw/?Status=nodemand",
                                "child": []
                            },
                        ]
                    },
                    {
                        "name": u"需备货数据",
                        "code": "DEMAND",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "",
                        "child": [
                            {
                                "name": u"备货列表(" + str(gendemand_count) + ")",
                                "icon": "",
                                "code": "GENDEMAND",
                                "parentCode": "DEMAND",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fbw_demand/?Status=gendemand",
                                "child": []
                            },
                        ]
                    },
                    {
                        "name": u"已生成批次待发货",
                        "code": "WAITDELIVER",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "",
                        "child": [
                            {
                                "name": u"待发货(" + str(genbatch_count) + ")",
                                "icon": "",
                                "code": "WAITDELIVERCODE",
                                "parentCode": "WAITDELIVER",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fbw_deliver/?Status=genbatch",
                                "child": []
                            },
                            {
                                "name": u"已发货(" + str(deliver_count) + ")",
                                "icon": "",
                                "code": "DELIVERCODE",
                                "parentCode": "WAITDELIVER",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fbw_deliver/?Status=deliver",
                                "child": []
                            },
                        ]
                    },
                    {
                        "name": u"发货物流信息",
                        "code": "LOGISTICS",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "",
                        "child": [
                            {
                                "name": u"物流信息(" + str(manage_count) + ")",
                                "icon": "",
                                "code": "LOGISTICSINFO",
                                "parentCode": "LOGISTICS",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fbw_management/?allStatus=all",
                                "child": []
                            },
                        ]
                    },
                    {
                        "name": u"发货全量数据",
                        "code": "ALLDATA",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "",
                        "child": [
                            {
                                "name": u"全量数据(" + str(allCount) + ")",
                                "icon": "",
                                "code": "ALLDATADETAIL",
                                "parentCode": "ALLDATA",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fbw_all/?allStatus=all",
                                "child": []
                            },
                        ]
                    },
                ]
            }]

            sourceURL = str(context['request']).split("'")[1]
            if '?' not in sourceURL:
                sourceURL = "/Project/admin/skuapp/t_stocking_demand_fbw/?Status=notyet"
            new_sourceURL = sourceURL
            if '?p=' in sourceURL:
                new_sourceURL = sourceURL.replace('?p=', '?')
                if '&' in new_sourceURL:
                    new_sourceURL = new_sourceURL.split('?')[0] + '?' + new_sourceURL.split('?')[1].split('&')[1]
                else:
                    new_sourceURL = new_sourceURL.split('?')[0]
            attention_text = ''

            show_flag = 0
            menu_list, flag, show_flag = self.validation_url_selected(menu_list, new_sourceURL, show_flag)
            if show_flag == 1:
                nodes.append(loader.render_to_string('site_left_menu_tree_stocking_fba_Plugin.html',
                                                     {'menu_list': json.dumps(menu_list), 'attention_text': attention_text}))
        except Exception, ex:
            messages.info(self.request,"采购状态加载错误,请联系IT解决:%s"%(str(ex)))