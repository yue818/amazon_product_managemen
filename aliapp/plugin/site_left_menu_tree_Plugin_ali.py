#-*-coding:utf-8-*-
import json
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages
from django.template import RequestContext

from skuapp.table.t_store_configuration_file import t_store_configuration_file
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime as timetime
from aliapp.models import *
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: site_left_menu_Plugin_wish.py
 @time: 2018/2/28 8:53
"""   
class site_left_menu_tree_Plugin_ali(BaseAdminPlugin):
    site_left_menu_tree_flag_ali = False

    def init_request(self, *args, **kwargs):
        return bool(self.site_left_menu_tree_flag_ali)

    def validation_url_selected(self, menu_list, new_sourceURL, show_flag):
        for menu_obj in menu_list:
            to_url = menu_obj['to_url']
            menu_child_obj = menu_obj['child']
            if len(menu_child_obj) > 0:
                if to_url == new_sourceURL:
                    menu_obj['selected'] = 'selected'
                    show_flag = 1
                    break
                menu_child_obj, show_flag = self.validation_url_selected(menu_child_obj, new_sourceURL, show_flag)
            else:
                if to_url != new_sourceURL:
                    if '?' not in menu_obj['to_url']:
                        to_url = to_url + '?'
                if to_url == new_sourceURL:
                    menu_obj['selected'] = 'selected'
                    show_flag = 1
                    break
        # messages.error(self.request, 'code: %s' % menu_obj['code'])
        return menu_list, show_flag

    def block_left_navbar(self, context, nodes):
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=self.request.user.username,
                                                   urltable="t_erp_aliexpress_online_info").count()
        except:
            pass
        shop_list = t_erp_aliexpress_shop_info.objects
        online_list = t_erp_aliexpress_online_info.objects.all()

        onSelling_list = t_erp_aliexpress_online_info.objects.filter(product_status_type='onSelling',revoked=0)
        offline_list = t_erp_aliexpress_online_info.objects.filter(product_status_type='offline',revoked=0)
        auditing_list = t_erp_aliexpress_online_info.objects.filter(product_status_type='auditing',revoked=0)
        editingRequired_list = t_erp_aliexpress_online_info.objects.filter(product_status_type='editingRequired',revoked=0)
        service_delete=t_erp_aliexpress_online_info.objects.filter(revoked=0,product_status_type='service-delete')
        # delete_list = t_erp_aliexpress_online_info_delete.objects
        revoked_list=t_erp_aliexpress_online_info.objects.filter(revoked=1)
        log_list = t_erp_aliexpress_action_log.objects
        if self.request.user.is_superuser or flag != 0:
            pass
        else:
            t_erp_aliexpress_shop_info_obj = t_erp_aliexpress_shop_info.objects.filter(shop_status='online').values(
                'seller_zh', 'accountName')
            t_erp_aliexpress_shop_info_obj = t_erp_aliexpress_shop_info_obj.filter(
                seller_zh__exact=self.request.user.first_name)
            accountNames = t_erp_aliexpress_shop_info_obj.values('accountName')
            buttonlist = []
            for obj in accountNames:
                buttonlist.append(obj['accountName'])
            buttonlist.sort()
            shop_list = shop_list.filter(seller_zh__exact=self.request.user.first_name)
            online_list = online_list.filter(owner_member_id__in=buttonlist)
            onSelling_list = onSelling_list.filter(owner_member_id__in=buttonlist)
            offline_list = offline_list.filter(owner_member_id__in=buttonlist)
            auditing_list = auditing_list.filter(owner_member_id__in=buttonlist)
            editingRequired_list = editingRequired_list.filter(owner_member_id__in=buttonlist)
            # delete_list = delete_list.filter(owner_member_id__in=buttonlist)
            revoked_list=revoked_list.filter(owner_member_id__in=buttonlist)
            log_list = log_list.filter(action_user__exact=self.request.user.first_name)
        shop_count = shop_list.values('id').count()
        online_count = online_list.values('id').count()
        onSelling_count = onSelling_list.values('id').count()
        offline_count = offline_list.values('id').count()
        auditing_count = auditing_list.values('id').count()
        editingRequired_count = editingRequired_list.values('id').count()
        service_delete_count = service_delete.values('id').count()
        revoked_count=revoked_list.values('id').count()+service_delete_count
        log_count = log_list.values('id').count()
        fullStopSales_count=t_erp_aliexpress_online_info.objects.filter(StopSales=100).count()
        partStopSales_count=t_erp_aliexpress_online_info.objects.filter(StopSales__range=[1,99]).count()
        StopSales_count=partStopSales_count+fullStopSales_count

        # GoodsFlag__in = stop_sell,
        stop_sell = [1, 1001, 101, 11, 1101, 111, 1011, 1111]
        if self.request.user.is_superuser:
            CanOffShelfCount = t_erp_aliexpress_online_info.objects.filter(product_status_type='onSelling',  skustatus4_stock__in=[1,10], revoked='0').count()
        else:
            from skuapp.table.t_store_configuration_file import t_store_configuration_file
            shop_list = []
            store_conf_objs = t_store_configuration_file.objects.filter(Seller=self.request.user.first_name).values('ShopName_temp')
            for store_conf_obj in store_conf_objs:
                shop_list.append(store_conf_obj['ShopName_temp'])
            CanOffShelfCount = t_erp_aliexpress_online_info.objects.filter(
                product_status_type='onSelling', skustatus4_stock__in=[1, 10], revoked='0', shopName__in=shop_list).count()
        # / Project / admin / aliapp / t_erp_aliexpress_shop_info /
        menu_list = [{
            "name": u"AliExpress在线管理",
            "code": "ALIZXGL",
            "icon": "icon-th",
            "selected": "",
            "to_url": "",
            "child": [{
                    "name": u"店铺授权("+str(shop_count)+")",
                    "code": "DPGL",
                    "icon": "icon-minus-sign",
                    "parentCode": "ALIZXGL",
                    "selected": "",
                    "to_url": "/Project/admin/aliapp/t_erp_aliexpress_shop_info/",
                    "child": []
                },{
                    "name": u"草稿箱",
                    "code": "CGX",
                    "icon": "icon-minus-sign",
                    "parentCode": "ALIZXGL",
                    "selected": "",
                    "to_url": "",
                    "child": [
                        {
                            "name": u"AliExpress草稿箱",
                            "icon": "",
                            "code": "ALICGX",
                            "parentCode": "CGX",
                            "selected": "",
                            "to_url": "",
                            # "to_url": "/Project/admin/aliapp/t_erp_aliexpress_product_draft_box/",
                            "child": []
                        },
                    ]
                },{
                    "name": u"待发布产品",
                    "code": "DFUCP",
                    "icon": "icon-minus-sign",
                    "parentCode": "ALIZXGL",
                    "selected": "",
                    "to_url": "",
                    "child": [
                        {
                            "name": u"待发布",
                            "icon": "",
                            "code": "ALIDFB",
                            "parentCode": "DFUCP",
                            "selected": "",
                            "to_url": "",
                            # "to_url": "/Project/admin/aliapp/t_erp_aliexpress_product_released/",
                            "child": []
                        },
                        {
                            "name": u"发布中",
                            "icon": "",
                            "code": "ALIFBZ",
                            "parentCode": "DFUCP",
                            "selected": "",
                            "to_url": "",
                            # "to_url": "/Project/admin/aliapp/t_erp_aliexpress_product_announcing/",
                            "child": []
                        },
                        {
                            "name": u"发布失败",
                            "icon": "",
                            "code": "ALIFBSB",
                            "parentCode": "DFUCP",
                            "selected": "",
                            "to_url": "",
                            # "to_url": "/Project/admin/aliapp/t_erp_aliexpress_product_upload_result/?online_status=FAILED",
                            "child": []
                        },
                        {
                            "name": u"发布成功",
                            "icon": "",
                            "code": "ALIFBCG",
                            "parentCode": "DFUCP",
                            "selected": "",
                            "to_url": "",
                            # "to_url": "/Project/admin/aliapp/t_erp_aliexpress_product_upload_result/?online_status=SUCCESS",
                            "child": []
                        },
                    ]
                }, {
                    "name": u"回收站",
                    "code": "HSZ",
                    "icon": "icon-minus-sign",
                    "parentCode": "ALIZXGL",
                    "selected": "",
                    "to_url": "",
                    "child": [
                        {
                            "name": u"回收站",
                            "icon": "",
                            "code": "ALIHSZ",
                            "parentCode": "HSZ",
                            "selected": "",
                            "to_url": "",
                            # "to_url": "/Project/admin/aliapp/t_erp_aliexpress_product_recycle_bin/",
                            "child": []
                        },
                    ]
                }, {
                    "name": u"所有分类("+str(online_count)+")",
                    "code": "SYFL",
                    "icon": "icon-minus-sign",
                    "parentCode": "ALIZXGL",
                    "selected": "",
                    "to_url": "/Project/admin/aliapp/t_erp_aliexpress_online_info/",
                    "child": [{
                            "name": u"在售("+str(onSelling_count)+")",
                            "code": "ALIZS",
                            "icon": "",
                            "parentCode": "SYFL",
                            "selected": "",
                            "to_url": "/Project/admin/aliapp/t_erp_aliexpress_online_info/?_p_product_status_type=onSelling&revoked=0",
                            "child": []
                        },{
                            "name": u"已下架("+str(offline_count)+")",
                            "code": "ALIYXJ",
                            "icon": "",
                            "parentCode": "SYFL",
                            "selected": "",
                            "to_url": "/Project/admin/aliapp/t_erp_aliexpress_online_info/?_p_product_status_type=offline&revoked=0",
                            "child": []
                        },{
                            "name": u"审核中("+str(auditing_count)+")",
                            "code": "ALISHZ",
                            "icon": "",
                            "parentCode": "SYFL",
                            "selected": "",
                            "to_url": "/Project/admin/aliapp/t_erp_aliexpress_online_info/?_p_product_status_type=auditing&revoked=0",
                            "child": []
                        },{
                            "name": u"审核不通过("+str(editingRequired_count)+")",
                            "code": "ALISHBTG",
                            "icon": "",
                            "parentCode": "SYFL",
                            "selected": "",
                            "to_url": "/Project/admin/aliapp/t_erp_aliexpress_online_info/?_p_product_status_type=editingRequired&revoked=0",
                            "child": []
                        },{
                            "name": u"已移除("+str(revoked_count)+")",
                            "code": "ALIYSC",
                            "icon": "",
                            "parentCode": "SYFL",
                            "selected": "",
                            "to_url": "/Project/admin/aliapp/t_erp_aliexpress_online_info/?revoked=1",
                            "child": []
                        },
                    ]
                },{
                    "name": u"操作结果("+str(log_count)+")",
                    "code": "CZJG",
                    "icon": "icon-minus-sign",
                    "parentCode": "ALIZXGL",
                    "selected": "",
                    "to_url": "/Project/admin/aliapp/t_erp_aliexpress_action_log/",
                    "child": []
                },
                {
                    "name": u"速卖通下架",
                    "code": "SMTXJ",
                    "icon": "icon-minus-sign",
                    "parentCode": "ALIZXGL",
                    "selected": "",
                    "to_url": "",
                    "child": [
                        {
                            "name": u"可下架("+str(CanOffShelfCount)+")",
                            "icon": "",
                            "code": "KXJ",
                            "parentCode": "SMTXJ",
                            "selected": "",
                            "to_url": "",
                            "to_url": "/Project/admin/aliapp/t_erp_aliexpress_online_info_shelf/?_p_product_status_type=onSelling&skustatus=4&skustock_isempty=0&revoked=0",
                            "child": []
                        },
                        {
                            "name": u"下架记录",
                            "icon": "",
                            "code": "XJJL",
                            "parentCode": "SMTXJ",
                            "selected": "",
                            "to_url": "",
                            "to_url": "/Project/admin/aliapp/t_erp_aliexpress_action_log/?action_type=disableSKU",
                            "child": []
                        },
                    ]
                }
                # {
                # "name": u"停售统计(" + str(StopSales_count) + ")",
                # "code": "TSTJ",
                # "icon": "icon-minus-sign",
                # "parentCode": "ALIZXGL",
                # "selected": "",
                # "to_url": "/Project/admin/aliapp/t_erp_aliexpress_online_info/?_p_StopSalesFlag=1&StopSales=101",
                # "child": [
                #     {
                #         "name": u"完全停售(" + str(fullStopSales_count) + ")",
                #         "code": "ALIWQTS",
                #         "icon": "",
                #         "parentCode": "TSTJ",
                #         "selected": "",
                #         "to_url": "/Project/admin/aliapp/t_erp_aliexpress_online_info/?_p_StopSalesFlag=1&StopSales=100",
                #         "child": []
                #
                #     }, {
                #         "name": u"部分停售(" + str(partStopSales_count) + ")",
                #         "code": "ALIBFTS",
                #         "icon": "",
                #         "parentCode": "TSTJ",
                #         "selected": "",
                #         "to_url": "/Project/admin/aliapp/t_erp_aliexpress_online_info/?StopSales=99&o=-StopSales&_p_StopSalesFlag=1",
                #         "child": []
                #     },]
                # }
            ]
            }]
        url_dict = {"/Project/admin/aliapp/t_erp_aliexpress_shop_info/": [],
                    "/Project/admin/aliapp/t_erp_aliexpress_online_info/": ["_p_product_status_type=onSelling&revoked=0",
                    "_p_product_status_type=offline&revoked=0","_p_product_status_type=auditing&revoked=0","_p_product_status_type=editingRequired&revoked=0",
                    '_p_StopSalesFlag=1&StopSales=101','_p_StopSalesFlag=1&StopSales=100','StopSales=99&o=-StopSales&_p_StopSalesFlag=1','revoked=1'],
                    "/Project/admin/aliapp/t_erp_aliexpress_action_log/": ['action_type=disableSKU'],
                    "/Project/admin/aliapp/t_erp_aliexpress_online_info_shelf/": ['_p_product_status_type=onSelling&skustatus=4&skustock_isempty=0&revoked=0']
                    }
        sourceURL = str(context['request']).split("'")[1]
        # new_sourceURL = sourceURL
        from_url = sourceURL.split('?')[0]
        new_sourceURL = from_url
        for k, v in url_dict.items():
            if from_url == k:
                for param_value in v:
                    if param_value in sourceURL:
                        new_sourceURL += '?' + param_value

        show_flag = 0
        menu_list, show_flag = self.validation_url_selected(menu_list, new_sourceURL, show_flag)
        if show_flag == 1:
            import json
            attention_text = ''
            # # 左侧栏文字
            # attention_text = u'<span style="height: 50px;width: 240px;font-size: 20px; color:red;">' \
            #                  u'1.此页面的数据每6小时刷新一次' \
            #                  u'<br>' \
            #                  u'2.一次分页显示数据越多越慢，因为会有大量的图片下载' \
            #                  u'<//span><br//>'
            # # 左侧栏图片
            # attention_text += '<br//><br//><img id="img_left" class="x" src="http:////fancyqube-tort.oss-cn-shanghai.aliyuncs.com/aliexpress/1/IPflowchart.png">'
            nodes.append(loader.render_to_string('site_left_menu_tree_Plugin.html',
                                                 {'menu_list': json.dumps(menu_list),
                                                  'attention_text': attention_text}))