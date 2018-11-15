#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fba_tree_menu_Plugin.py
 @time: 2018-08-10
"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
from skuapp.table.t_stocking_reject_fba import t_stocking_reject_fba
from skuapp.table.t_stocking_rejecting_fba import t_stocking_rejecting_fba
from skuapp.table.t_stocking_demand_fba_deliver import t_stocking_demand_fba_deliver
import json
from django.contrib import messages

class t_stocking_demand_fba_tree_menu_Plugin(BaseAdminPlugin):
    fba_tree_menu_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.fba_tree_menu_flag)

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
            from django.contrib.auth.models import User
            userID = [each.id for each in User.objects.filter(groups__id__in=[65])]
            # if self.request.user.is_superuser or request.user.id in userID:
            if self.request.user.id in userID:
                notgenpurchase_count = t_stocking_demand_fba.objects.filter(Status='notgenpurchase',Demand_people=self.request.user.first_name).count()  #
                giveup_count = t_stocking_demand_fba.objects.filter(Status='giveup',Demand_people=self.request.user.first_name).count()  #
                reject_count = t_stocking_reject_fba.objects.filter(Status='reject',SummbitRejectMan=self.request.user.first_name).count()  #
                notpurchase_count = t_stocking_demand_fba.objects.filter(Status='notpurchase',Demand_people=self.request.user.first_name).count()
                purchaseing_count = t_stocking_demand_fba.objects.filter(Status='purchasing',Demand_people=self.request.user.first_name).count()
                abnormalpurchase_count = t_stocking_demand_fba.objects.filter(Status='abnormalpurchase',Demand_people=self.request.user.first_name).count()
                completepurchase_count = t_stocking_demand_fba.objects.filter(completeStatus='completepurchase',Demand_people=self.request.user.first_name).count()
                check_count = t_stocking_demand_fba.objects.filter(Status='check',Demand_people=self.request.user.first_name).count()
                completecheck_count = t_stocking_demand_fba.objects.filter(checkStatus='completecheck',Demand_people=self.request.user.first_name).count()
                abnormalcheck_count = t_stocking_demand_fba.objects.filter(Status='abnormalcheck',Demand_people=self.request.user.first_name).count()
                genbatch_count = t_stocking_demand_fba.objects.filter(Status='genbatch',Demand_people=self.request.user.first_name).count()
                completegenbatch_count = t_stocking_demand_fba.objects.filter(genStatus='completegenbatch',Demand_people=self.request.user.first_name).count()
                deliver_count = t_stocking_demand_fba_deliver.objects.filter(Status='deliver').count()
                completedeliver_count = t_stocking_demand_fba_deliver.objects.filter(Status='completedeliver').count()
                fbaall_count = t_stocking_demand_fba.objects.filter(Demand_people=self.request.user.first_name).count()
                turn_count = t_stocking_rejecting_fba.objects.filter(Status='rejecting', RejectStatus='turn',SummbitRejectMan=self.request.user.first_name).count()  #
                return_count = t_stocking_rejecting_fba.objects.filter(Status='rejecting',
                                                                       RejectStatus='return',SummbitRejectMan=self.request.user.first_name).count()  #
                completereject_count = t_stocking_rejecting_fba.objects.filter(Status='completereject',SummbitRejectMan=self.request.user.first_name).count()  #
            else:
                notgenpurchase_count = t_stocking_demand_fba.objects.filter(Status='notgenpurchase').count()#
                giveup_count = t_stocking_demand_fba.objects.filter(Status='giveup').count()  #
                reject_count = t_stocking_reject_fba.objects.filter(Status='reject').count()  #
                notpurchase_count = t_stocking_demand_fba.objects.filter(Status='notpurchase').count()
                purchaseing_count = t_stocking_demand_fba.objects.filter(Status='purchasing').count()
                abnormalpurchase_count = t_stocking_demand_fba.objects.filter(Status='abnormalpurchase').count()
                completepurchase_count = t_stocking_demand_fba.objects.filter(completeStatus='completepurchase').count()
                check_count = t_stocking_demand_fba.objects.filter(Status='check').count()
                completecheck_count = t_stocking_demand_fba.objects.filter(checkStatus='completecheck').count()
                abnormalcheck_count = t_stocking_demand_fba.objects.filter(Status='abnormalcheck').count()
                genbatch_count = t_stocking_demand_fba.objects.filter(Status='genbatch').count()
                completegenbatch_count = t_stocking_demand_fba.objects.filter(genStatus='completegenbatch').count()
                deliver_count = t_stocking_demand_fba_deliver.objects.filter(Status='deliver').count()
                completedeliver_count = t_stocking_demand_fba_deliver.objects.filter(Status='completedeliver').count()
                fbaall_count = t_stocking_demand_fba.objects.filter().count()
                turn_count = t_stocking_rejecting_fba.objects.filter(Status='rejecting',RejectStatus='turn').count()  #
                return_count = t_stocking_rejecting_fba.objects.filter(Status='rejecting', RejectStatus='return').count()  #
                completereject_count = t_stocking_rejecting_fba.objects.filter(Status='completereject').count()  #
            menu_list = [{
                "name": u"FBA备货流程",
                "code": "IPMAIN",
                "icon": "icon-th",
                "selected": "",
                "to_url": "",
                "child": [
                    {
                        "name": u"备货",
                        "code": "DEMAND",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "",
                        "child": [
                            {
                                "name": u"备货需求列表(" + str(notgenpurchase_count) + ")",
                                "icon": "",
                                "code": "NOTPURCHASE",
                                "parentCode": "DEMAND",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba/?Status=notgenpurchase",
                                "child": []
                            },
                            {
                                "name": u"废弃(" + str(giveup_count) + ")",
                                "icon": "",
                                "code": "GIVEUP",
                                "parentCode": "DEMAND",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba/?Status=giveup",
                                "child": []
                            },
                            {
                                "name": u"转退需求列表(" + str(reject_count) + ")",
                                "icon": "",
                                "code": "REJECT",
                                "parentCode": "DEMAND",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_reject_fba/?Status=reject",
                                "child": []
                            },
                        ]
                    },
                    {
                        "name": u"采购",
                        "code": "PURCHASE",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "",
                        "child": [
                            {
                                "name": u"未采购(" + str(notpurchase_count) + ")",
                                "icon": "",
                                "code": "NOTPURCHASE",
                                "parentCode": "PURCHASE",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_purchase/?Status=notpurchase",
                                "child": []
                            },
                            {
                                "name": u"采购中(" + str(purchaseing_count) + ")",
                                "icon": "",
                                "code": "PURCHASEING",
                                "parentCode": "PURCHASE",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_purchase/?Status=purchasing",
                                "child": []
                            },
                            {
                                "name": u"完成采购(" + str(completepurchase_count) + ")",
                                "icon": "",
                                "code": "COMPLETEPURCHASE",
                                "parentCode": "PURCHASE",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_purchase/?Status=completepurchase",
                                "child": []
                            },
                            {
                                "name": u"采购异常数据(" + str(abnormalpurchase_count) + ")",
                                "icon": "",
                                "code": "ABNORMALPURCHASE",
                                "parentCode": "PURCHASE",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_purchase/?Status=abnormalpurchase",
                                "child": []
                            },
                        ]
                    },
                    {
                        "name": u"质检",
                        "code": "CHECK",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "",
                        "child": [
                            {
                                "name": u"质检列表(" + str(check_count) + ")",
                                "icon": "",
                                "code": "CHECKLIST",
                                "parentCode": "CHECK",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_check/?Status=check",
                                "child": []
                            },
                            {
                                "name": u"完成质检(" + str(completecheck_count) + ")",
                                "icon": "",
                                "code": "CHECKCOMPLETE",
                                "parentCode": "CHECK",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_check/?Status=completecheck",
                                "child": []
                            },
                            {
                                "name": u"质检异常数据(" + str(abnormalcheck_count) + ")",
                                "icon": "",
                                "code": "CHECKABNORMAL",
                                "parentCode": "CHECK",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_check/?Status=abnormalcheck",
                                "child": []
                            },
                        ]
                    },
                    {
                        "name": u"集货仓一览",
                        "code": "GENPATCH",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "",
                        "child": [
                            {
                                "name": u"生成批次列表(" + str(genbatch_count) + ")",
                                "icon": "",
                                "code": "GENPATCHLIST",
                                "parentCode": "GENPATCH",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_genbatch/?Status=genbatch",
                                "child": []
                            },
                            {
                                "name": u"完成生成批次(" + str(completegenbatch_count) + ")",
                                "icon": "",
                                "code": "GENPATCHCOMPLETE",
                                "parentCode": "GENPATCH",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_genbatch/?Status=completegenbatch",
                                "child": []
                            },
                        ]
                    },
                    {
                        "name": u"发货管理",
                        "code": "SHIPPINGMANG",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "",
                        "child": [
                            {
                                "name": u"发货列表(" + str(deliver_count) + ")",
                                "icon": "",
                                "code": "SHIPPINGLIST",
                                "parentCode": "SHIPPINGMANG",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_deliver/?Status=deliver",
                                "child": []
                            },
                            {
                                "name": u"完成发货(" + str(completedeliver_count) + ")",
                                "icon": "",
                                "code": "SHIPPPINGCOMPLETE",
                                "parentCode": "SHIPPINGMANG",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_deliver/?Status=completedeliver",
                                "child": []
                            }
                        ]
                    },
                    {
                        "name": u"转退管理",
                        "code": "TRANSFERHOUSE",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "",
                        "child": [
                            {
                                "name": u"退货中(" + str(return_count) + ")",
                                "icon": "",
                                "code": "RETURN",
                                "parentCode": "TRANSFERHOUSE",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_rejecting_fba/?Status=rejecting&RejectStatus=return",
                                "child": []
                            },
                            {
                                "name": u"转仓中(" + str(turn_count) + ")",
                                "icon": "",
                                "code": "TURN",
                                "parentCode": "TRANSFERHOUSE",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_rejecting_fba/?Status=rejecting&RejectStatus=turn",
                                "child": []
                            },
                            {
                                "name": u"转退完成(" + str(completereject_count) + ")",
                                "icon": "",
                                "code": "COMPLETEREJECT",
                                "parentCode": "TRANSFERHOUSE",
                                "selected": "",
                                "to_url": "/Project/admin/skuapp/t_stocking_rejecting_fba/?Status=completereject",
                                "child": []
                            }
                        ]
                    },
                    {
                        "name": u"FBA备货全量数据("+str(fbaall_count)+")",
                        "code": "ALLDEMAND",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_all/?Status=all",
                        "child": []
                    },
                    {
                        "name": u"FBA明细一览",
                        "code": "DETAIL",
                        "icon": "icon-minus-sign",
                        "parentCode": "IPMAIN",
                        "selected": "",
                        "to_url": "/Project/admin/skuapp/t_stocking_demand_fba_detail/?Status=completedeliver",
                        "child": []
                    },
                ]
            }]

            sourceURL = str(context['request']).split("'")[1]
            if '?' not in sourceURL:
                sourceURL = "/Project/admin/skuapp/t_stocking_demand_fba/?Status=notgenpurchase"
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