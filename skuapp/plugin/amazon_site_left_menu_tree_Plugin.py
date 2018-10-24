# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: amazon_site_left_menu_tree_Plugin.py
 @time: 2018-06-23 13:05
"""  
# -*-coding:utf-8-*-

import json

from django.template import RequestContext
from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_templet_amazon_collection_box import *
from skuapp.table.t_templet_amazon_wait_upload import *
from skuapp.table.t_templet_amazon_upload_result import *
from skuapp.table.t_online_info_amazon_listing import *
from skuapp.table.t_templet_amazon_recycle_bin import *
from skuapp.table.t_templet_amazon_upload_fail import *
from skuapp.table.t_templet_amazon_upload_result_lose_pic import *
from skuapp.table.t_config_amazon_template import *
from skuapp.table.t_config_shop_alias import t_config_shop_alias
from skuapp.table.t_amazon_removal_order_detail import t_amazon_removal_order_detail
from skuapp.table.t_amazon_all_orders_data import t_amazon_all_orders_data

class amazon_site_left_menu_tree_Plugin(BaseAdminPlugin):
    amazon_site_left_menu_tree_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.amazon_site_left_menu_tree_flag)

    def get_result_count(self, sql):
        row_count = None
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            count = cursor.fetchone()
            cursor.close()
            if count:
                row_count = count[0]
        except Exception:
            pass
        return row_count

    def block_left_navbar(self, context, nodes):
        shopname = self.request.GET.get('shopname', '')
        is_fba = self.request.GET.get('_p_is_fba', '')

        if shopname:
            shop_alias_count = t_config_shop_alias.objects.filter(ShopName=shopname).values('id').count()
            # remove_list_cnt = t_online_info_amazon_listing.objects.filter(ShopName=shopname, refresh_status=1, Status__in=('Active', 'Inactive')).values('id').count()
            inactive_shop_cnt = t_online_info_amazon_listing.objects.filter(ShopName=shopname, shop_status=1, Status__in=('Active', 'Inactive')).values('id').count()
            t_remove_order_cnt = t_amazon_removal_order_detail.objects.filter(shop_name=shopname).values('id').count()
            all_orders_cnt = t_amazon_all_orders_data.objects.filter(shop_name=shopname).values('id').count()
            if is_fba:
                try:
                    is_fba = int(is_fba)
                except:
                    is_fba = 0
                active_list_cnt = t_online_info_amazon_listing.objects.filter(ShopName=shopname, Status='Active', refresh_status=0, is_fba=is_fba, shop_status=0).values('id').count()
                inactive_list_cnt = t_online_info_amazon_listing.objects.filter(ShopName=shopname, Status='Inactive', refresh_status=0, is_fba=is_fba, shop_status=0).values('id').count()
                remove_list_cnt = t_online_info_amazon_listing.objects.filter(ShopName=shopname, refresh_status=1, is_fba=is_fba, Status__in=('Active', 'Inactive'), shop_status=0).values('id').count()
                active_shop_cnt = active_list_cnt + inactive_list_cnt + remove_list_cnt
                all_list_cnt = active_shop_cnt + inactive_shop_cnt
                
            else:
                active_list_cnt = t_online_info_amazon_listing.objects.filter(ShopName=shopname,  Status='Active', refresh_status=0, shop_status=0).values('id').count()
                inactive_list_cnt = t_online_info_amazon_listing.objects.filter(ShopName=shopname, Status='Inactive', refresh_status=0, shop_status=0).values('id').count()
                remove_list_cnt = t_online_info_amazon_listing.objects.filter(ShopName=shopname, refresh_status=1, Status__in=('Active', 'Inactive'), shop_status=0).values('id').count()
                active_shop_cnt = active_list_cnt + inactive_list_cnt + remove_list_cnt
                all_list_cnt = active_shop_cnt + inactive_shop_cnt
            if self.request.user.is_superuser:
                t_templet_amazon_collection_box_count = t_templet_amazon_collection_box.objects.filter(status='1', ShopSets=shopname).values(
                    'id').count()
                t_templet_amazon_wait_upload_count_no = t_templet_amazon_wait_upload.objects.filter(status='NO', ShopSets=shopname).values(
                    'id').count()
                t_templet_amazon_upload_result_upload_count = t_templet_amazon_upload_result.objects.filter(
                    status='UPLOAD', ShopSets=shopname).values('id').count()
                t_templet_amazon_wait_upload_count_failed = t_templet_amazon_upload_fail.objects.filter(is_display='1', ShopSets=shopname).values('id').count()
                t_templet_amazon_wait_upload_count_success = t_templet_amazon_upload_result.objects.filter(
                    status='SUCCESS', ShopSets=shopname).values('id').count()
                t_templet_amazon_recycle_bin_count = t_templet_amazon_recycle_bin.objects.filter(status='1', ShopSets=shopname).values('id').count()
                t_templet_amazon_upload_result_lose_pic_count = t_templet_amazon_upload_result_lose_pic.objects.filter(ShopSets=shopname).exclude(is_display='0').values('id').count()
                template_count = t_config_amazon_template.objects.filter(shopName=shopname).values('id').count()

            else:
                t_templet_amazon_collection_box_count = t_templet_amazon_collection_box.objects.filter(status='1', ShopSets=shopname, createUser=self.request.user.username).values(
                    'id').count()
                t_templet_amazon_wait_upload_count_no = t_templet_amazon_wait_upload.objects.filter(status='NO', ShopSets=shopname, createUser=self.request.user.username).values(
                    'id').count()
                t_templet_amazon_upload_result_upload_count = t_templet_amazon_upload_result.objects.filter(
                    status='UPLOAD', createUser=self.request.user.username).values('id').count()
                t_templet_amazon_wait_upload_count_failed = t_templet_amazon_upload_fail.objects.filter(is_display='1', ShopSets=shopname, createUser=self.request.user.username).values('id').count()
                t_templet_amazon_wait_upload_count_success = t_templet_amazon_upload_result.objects.filter(
                    status='SUCCESS', createUser=self.request.user.username).values('id').count()
                t_templet_amazon_recycle_bin_count = t_templet_amazon_recycle_bin.objects.filter(status='1', ShopSets=shopname, createUser=self.request.user.username).values('id').count()
                t_templet_amazon_upload_result_lose_pic_count = t_templet_amazon_upload_result_lose_pic.objects.filter(ShopSets=shopname, createUser=self.request.user.username).exclude(is_display='0').values('id').count()
                template_count = t_config_amazon_template.objects.filter(CreateName=self.request.user.first_name, shopName=shopname).values('id').count()
        else:
            shop_alias_count = t_config_shop_alias.objects.all().values('id').count()
            # remove_list_cnt = t_online_info_amazon_listing.objects.filter(refresh_status=1, Status__in=('Active', 'Inactive')).values('id').count()
            inactive_shop_cnt = t_online_info_amazon_listing.objects.filter(shop_status=1, Status__in=('Active', 'Inactive')).values('id').count()
            shop_name = self.request.GET.get('shop_name', '')
            if shop_name:
                t_remove_order_cnt = t_amazon_removal_order_detail.objects.filter(shop_name=shop_name).values('id').count()
                all_orders_cnt = t_amazon_all_orders_data.objects.filter(shop_name=shop_name).values('id').count()
            else:
                t_remove_order_cnt = t_amazon_removal_order_detail.objects.all().values('id').count()
                all_orders_cnt = t_amazon_all_orders_data.objects.all().values('id').count()
            if is_fba:
                try:
                    is_fba = int(is_fba)
                except:
                    is_fba = 0
                active_list_cnt = t_online_info_amazon_listing.objects.filter(Status='Active', refresh_status=0, is_fba=is_fba, shop_status=0).values('id').count()
                inactive_list_cnt = t_online_info_amazon_listing.objects.filter(Status='Inactive', refresh_status=0, is_fba=is_fba, shop_status=0).values('id').count()
                remove_list_cnt = t_online_info_amazon_listing.objects.filter(refresh_status=1, is_fba=is_fba, Status__in=('Active', 'Inactive'), shop_status=0).values('id').count()
                active_shop_cnt = active_list_cnt + inactive_list_cnt + remove_list_cnt
                all_list_cnt = active_shop_cnt + inactive_shop_cnt
            else:
                active_list_cnt = t_online_info_amazon_listing.objects.filter(Status='Active', refresh_status=0, shop_status=0).values('id').count()
                inactive_list_cnt = t_online_info_amazon_listing.objects.filter(Status='Inactive', refresh_status=0, shop_status=0).values('id').count()
                remove_list_cnt = t_online_info_amazon_listing.objects.filter(refresh_status=1, Status__in=('Active', 'Inactive'), shop_status=0).values('id').count()
                active_shop_cnt = active_list_cnt + inactive_list_cnt + remove_list_cnt
                all_list_cnt = active_shop_cnt + inactive_shop_cnt
            if self.request.user.is_superuser:
                t_templet_amazon_collection_box_count = t_templet_amazon_collection_box.objects.filter(status='1').values(
                    'id').count()
                t_templet_amazon_wait_upload_count_no = t_templet_amazon_wait_upload.objects.filter(status='NO').values(
                    'id').count()
                t_templet_amazon_upload_result_upload_count = t_templet_amazon_upload_result.objects.filter(
                    status='UPLOAD').values('id').count()
                t_templet_amazon_wait_upload_count_failed = t_templet_amazon_upload_fail.objects.filter(is_display='1').values('id').count()
                t_templet_amazon_wait_upload_count_success = t_templet_amazon_upload_result.objects.filter(
                    status='SUCCESS').values('id').count()
                t_templet_amazon_recycle_bin_count = t_templet_amazon_recycle_bin.objects.filter(status='1').values('id').count()
                t_templet_amazon_upload_result_lose_pic_count = t_templet_amazon_upload_result_lose_pic.objects.exclude(is_display='0').values('id').count()
                template_count = t_config_amazon_template.objects.all().values('id').count()
            else:
                t_templet_amazon_collection_box_count = t_templet_amazon_collection_box.objects.filter(status='1', createUser=self.request.user.username).values(
                    'id').count()
                t_templet_amazon_wait_upload_count_no = t_templet_amazon_wait_upload.objects.filter(status='NO', createUser=self.request.user.username).values(
                    'id').count()
                t_templet_amazon_upload_result_upload_count = t_templet_amazon_upload_result.objects.filter(
                    status='UPLOAD', createUser=self.request.user.username).values('id').count()
                t_templet_amazon_wait_upload_count_failed = t_templet_amazon_upload_fail.objects.filter(is_display='1', createUser=self.request.user.username).values('id').count()
                t_templet_amazon_wait_upload_count_success = t_templet_amazon_upload_result.objects.filter(
                    status='SUCCESS', createUser=self.request.user.username).values('id').count()
                t_templet_amazon_recycle_bin_count = t_templet_amazon_recycle_bin.objects.filter(status='1', createUser=self.request.user.username).values('id').count()
                t_templet_amazon_upload_result_lose_pic_count = t_templet_amazon_upload_result_lose_pic.objects.filter(createUser=self.request.user.username).exclude(is_display='0').values(
                    'id').count()
                template_count = t_config_amazon_template.objects.filter(CreateName=self.request.user.first_name).values('id').count()


        amazon_upload = {
            "name": u"刊登" ,
            "code": "12",
            "icon": "icon-minus-sign",
            "parentCode": "01",
            "selected": "",
            "to_url": '',
            "flag": "pub_all",
            "child": [
                {
                    "name": u"草稿箱(%s)" % t_templet_amazon_collection_box_count ,
                    "code": "121",
                    "icon": "",
                    "parentCode": "12",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_collection_box/',
                    "flag": "1",
                    "child": []
                },
                {
                    "name": u"待发布(%s)" % t_templet_amazon_wait_upload_count_no,
                    "code": "122",
                    "icon": "",
                    "parentCode": "12",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_wait_upload/?_p_status=NO',
                    "flag": "2",
                    "child": []
                },
                {
                    "name": u"发布中(%s)" % t_templet_amazon_upload_result_upload_count,
                    "code": "123",
                    "icon": "",
                    "parentCode": "12",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_upload_result/?_p_status=UPLOAD',
                    "flag": "3",
                    "child": []
                },
                {
                    "name": u"发布失败(%s)" % t_templet_amazon_wait_upload_count_failed,
                    "code": "123",
                    "icon": "",
                    "parentCode": "12",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_upload_fail/',
                    "flag": "4",
                    "child": []
                },
                {
                    "name": u"发布成功(%s)" % t_templet_amazon_wait_upload_count_success,
                    "code": "123",
                    "icon": "",
                    "parentCode": "12",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_upload_result/?_p_status=SUCCESS',
                    "flag": "5",
                    "child": []
                },
                {
                    "name": u"发布后图片缺失(%s)" % t_templet_amazon_upload_result_lose_pic_count ,
                    "code": "123",
                    "icon": "",
                    "parentCode": "12",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_upload_result_lose_pic/',
                    "flag": "6",
                    "child": []
                },
                {
                    "name": u"回收站(%s)" % t_templet_amazon_recycle_bin_count,
                    "code": "123",
                    "icon": "",
                    "parentCode": "12",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_recycle_bin/',
                    "flag": "7",
                    "child": []
                },
            ]
        }

        flag = 'info_all'
        if self.request.GET.get('_p_Status'):
            flag = self.request.GET.get('_p_Status')
        if 't_templet_amazon_collection_box' in self.request.get_full_path():
            flag = '1'
        if self.request.GET.get('_p_status') == 'NO':
            flag = '2'
        if self.request.GET.get('_p_status') == 'UPLOAD':
            flag = '3'
        if self.request.GET.get('_p_status') == 'SUCCESS':
            flag = '5'
        if 't_templet_amazon_upload_fail' in self.request.get_full_path():
            flag = '4'
        if 't_templet_amazon_upload_result_lose_pic' in self.request.get_full_path():
            flag = '6'
        if 't_templet_amazon_recycle_bin' in self.request.get_full_path():
            flag = '7'

        search_str = ''
        inactive_shop_str =''
        if str(is_fba):
            search_str += '&_p_is_fba=%s' % is_fba
        else:
            search_str += '&_p_is_fba=0'
        if shopname:
            search_str += '&shopname=%s' % shopname
            inactive_shop_str += '&shopname=%s' % shopname

        '''
        now_url = self.request.get_full_path().replace('_p_Status=Active', '').replace('_p_Status=Inactive', '') \
            .replace('_p_is_fba=1', '').replace('_p_is_fba=0', '') \
            .replace('?&', '?').replace('&&', '&')

        search_opts = now_url.split('?')[-1]
        if search_opts:
            search_list = search_opts.split('&')
            for i in search_list:
                if i.startswith('shopname'):
                    search_list.remove(i)
            search_opts = '&'.join(search_list)
            search_str += search_opts
        '''

        amazon_online_info_active_shop = {
            "name": u"正常店铺(%s)"% active_shop_cnt,
            "code": "1101",
            "icon": "icon-minus-sign",
            "parentCode": "11",
            "selected": "",
            "to_url": '',
            "flag": "active_shop",
            "child":
                [
                    {
                        "name": u"启用(%s)" % active_list_cnt,
                        "icon": "",
                        "code": "110101",
                        "parentCode": "1101",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_online_info_amazon_listing/?_p_Status=Active&_p_refresh_status=0&_p_shop_status=0%s' % search_str,
                        "flag": 'Active',
                        "child": []
                    },

                    {
                        "name": u"未启用(%s)" % inactive_list_cnt,
                        "icon": "",
                        "code": "110102",
                        "parentCode": "1101",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_online_info_amazon_listing/?_p_Status=Inactive&_p_refresh_status=0&_p_shop_status=0%s' % search_str,
                        "flag": 'Inactive',
                        "child": []
                    },

                    {
                        "name": u"已移除(%s)" % remove_list_cnt,
                        "icon": "",
                        "code": "110103",
                        "parentCode": "1101",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_online_info_amazon_listing/?_p_refresh_status=1&_p_shop_status=0%s' % search_str,
                        "flag": 'remove',
                        "child": []
                    },

                    # {
                    #     "name": u"店铺刷新状态",
                    #     "icon": "",
                    #     "code": "110104",
                    #     "parentCode": "1101",
                    #     "selected": "",
                    #     "to_url": '/Project/admin/skuapp/t_perf_amazon_refresh_status',
                    #     "flag": 'refresh_status',
                    #     "child": []
                    # },
                ]
        }

        amazon_online_info_inactive_shop = {
            "name": u"已关闭店铺(%s)" % inactive_shop_cnt,
            "code": "1102",
            "icon": "icon-minus-sign",
            "parentCode": "11",
            "selected": "",
            "to_url": '',
            "flag": "",
            "child":
                [
                    {
                        "name": u"商品列表" ,
                        "icon": "",
                        "code": "110201",
                        "parentCode": "1102",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_online_info_amazon_listing/?_p_shop_status=1%s' % inactive_shop_str,
                        "flag": 'inactive_shop',
                        "child": []
                    },
                ]
        }

        amazon_online_info_analysis = {
            "name": u"统计分析",
            "code": "1103",
            "icon": "icon-minus-sign",
            "parentCode": "11",
            "selected": "",
            "to_url": '',
            "flag": "",
            "child":
                [
                    {
                        "name": u"商品SKU成本统计",
                        "icon": "",
                        "code": "110301",
                        "parentCode": "1103",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_product_inventory_cost/',
                        "flag": 'inventory_cost',
                        "child": []
                    },

                    {
                        "name": u"已移除订单(%s)" % t_remove_order_cnt,
                        "icon": "",
                        "code": "110302",
                        "parentCode": "1103",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_removal_order_detail/',
                        "flag": 'removal_order',
                        "child": []
                    },

                    {
                        "name": u"移除订单统计",
                        "icon": "",
                        "code": "110303",
                        "parentCode": "1103",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_product_remove_cost/',
                        "flag": 'remove_cost',
                        "child": []
                    },

                    {
                        "name": u"订单详情(%s)" % all_orders_cnt,
                        "icon": "",
                        "code": "110304",
                        "parentCode": "1103",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_all_orders_data/',
                        "flag": 'all_orders',
                        "child": []
                    },

                    {
                        "name": u"Pending订单统计",
                        "icon": "",
                        "code": "110305",
                        "parentCode": "1103",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_product_order_pend_cost/',
                        "flag": 'pend_cost',
                        "child": []
                    },

                    {
                        "name": u"激活率",
                        "icon": "",
                        "code": "110306",
                        "parentCode": "1103",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_orders_by_receive_day_total/',
                        "flag": 'orders_by_receive_day',
                        "child": []
                    },

                    {
                        "name": u"未发货订单",
                        "icon": "",
                        "code": "110307",
                        "parentCode": "1103",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_actionable_order_data/',
                        "flag": 'actionable_order_data',
                        "child": []
                    },

                    {
                        "name": u"价格调整记录",
                        "icon": "",
                        "code": "110308",
                        "parentCode": "1103",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_operation_log/',
                        "flag": 'operation_log',
                        "child": []
                    },
                ]
        }

        amazon_online_info = {
            "name": u"全部产品(%s)" % all_list_cnt,
            "code": "11",
            "icon": "icon-minus-sign",
            "parentCode": "01",
            "selected": "",
            "to_url": '/Project/admin/skuapp/t_online_info_amazon_listing',
            "flag": "info_all",
            "child": [
                amazon_online_info_active_shop,
                amazon_online_info_inactive_shop,
                amazon_online_info_analysis,
            ]
        }

        amazon_template = {
            "name": u"店铺管理",
            "code": "10",
            "icon": "icon-minus-sign",
            "parentCode": "01",
            "selected": "",
            # "to_url": '/Project/admin/skuapp/t_online_info_amazon_listing',
            "to_url": '',
            "flag": "shop_all",
            "child": [
                {
                    "name": u"运费模板(%s)" %template_count,
                    "icon": "",
                    "code": "101",
                    "parentCode": "10",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_config_amazon_template/',
                    "flag": 'template_flag',
                    "child": []
                },
                {
                    "name": u"店铺配置(%s)" % shop_alias_count,
                    "icon": "",
                    "code": "102",
                    "parentCode": "10",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_config_shop_alias/',
                    "flag": 'shop_alias_flag',
                    "child": []
                },

                {
                    "name": u"店铺SKU修正",
                    "icon": "",
                    "code": "103",
                    "parentCode": "10",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_amazon_shopsku_modify/',
                    "flag": 'shopsku_modify',
                    "child": []
                },
            ]
        }

        if 't_config_amazon_template' in self.request.get_full_path():
            flag = 'template_flag'
        elif 't_config_shop_alias' in self.request.get_full_path():
            flag = 'shop_alias_flag'
        elif 't_amazon_product_inventory_cost' in self.request.get_full_path():
            flag = 'inventory_cost'
        elif 't_amazon_removal_order_detail' in self.request.get_full_path():
            flag = 'removal_order'
        elif 't_amazon_shopsku_modify' in self.request.get_full_path():
            flag = 'shopsku_modify'
        elif 't_amazon_all_orders_data' in self.request.get_full_path():
            flag = 'all_orders'
        elif 't_amazon_product_remove_cost' in self.request.get_full_path():
            flag = 'remove_cost'
        elif 't_amazon_product_order_pend_cost' in self.request.get_full_path():
            flag = 'pend_cost'
        elif 't_amazon_orders_by_receive_day_total' in self.request.get_full_path():
            flag = 'orders_by_receive_day'
        elif 't_amazon_operation_log' in self.request.get_full_path():
            flag = 'operation_log'
        elif 't_perf_amazon_refresh_status' in self.request.get_full_path():
            flag = 'refresh_status'
        elif 't_amazon_actionable_order_data' in self.request.get_full_path():
            flag = 'actionable_order_data'

        if '_p_refresh_status=1' in self.request.get_full_path():
            flag = 'remove'

        if '_p_shop_status=1' in self.request.get_full_path():
            flag = 'inactive_shop'

        menu_list = [
            {
                "name": u"店铺管理",
                "code": "01",
                "icon": "icon-th",
                "selected": "",
                "to_url": "",
                "flag": "",
                "child": [
                    amazon_template,
                    amazon_upload,
                    amazon_online_info,
                ]
            },
        ]

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
