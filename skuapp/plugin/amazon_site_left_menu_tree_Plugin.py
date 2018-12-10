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
from skuapp.table.t_templet_amazon_publish_draft_from_ebay import t_templet_amazon_publish_draft_from_ebay
from skuapp.table.t_templet_amazon_follow import t_templet_amazon_follow
from skuapp.table.t_amazon_actionable_order_data import t_amazon_actionable_order_data
from skuapp.table.t_amazon_finance_record import t_amazon_finance_record
from skuapp.table.t_amazon_auto_load import t_amazon_auto_load
from skuapp.table.t_amazon_fba_inventory_age import t_amazon_fba_inventory_age
from django.db.models import Q


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
            actionable_order_cnt = t_amazon_actionable_order_data.objects.filter(shop_name=shopname).values('id').count()
            finance_record_cnt = t_amazon_finance_record.objects.filter(shop_name=shopname).values('id').count()
            can_load_cnt = t_online_info_amazon_listing.objects.filter(ShopName=shopname, shop_status=0, refresh_status=0, is_fba=0, Status='Inactive', product_status=1).values('id').count()
            can_unload_cnt = t_online_info_amazon_listing.objects.filter(ShopName=shopname, shop_status=0, refresh_status=0, is_fba=0, Status='Active', product_status__in=(2,3,4)).values('id').count()
            load_cnt = t_amazon_auto_load.objects.filter(shop_name=shopname, deal_type='load').values('id').count()
            unload_cnt = t_amazon_auto_load.objects.filter(shop_name=shopname, deal_type='unload').values('id').count()
            inventory_age_cnt = t_amazon_fba_inventory_age.objects.filter(shop_name=shopname).filter(Q(qty_to_be_charged_ltsf_6_mo__gt=0)|Q(qty_to_be_charged_ltsf_12_mo__gt=0)).values('id').count()
            tort_cnt_obj = t_online_info_amazon_listing.objects.filter(ShopName=shopname, shop_status=0, refresh_status=0, Status='Active')
            no_ban_cnt = tort_cnt_obj.filter(tortflag=1, RiskGrade__in=[8, 9, 10, 11, 12, 13, 14, 15]).count()
            no_scope_cnt = tort_cnt_obj.filter(tortflag=1, RiskGrade__in=[4, 5, 6, 7, 12, 13, 14, 15]).count()
            no_pot_cnt = tort_cnt_obj.filter(tortflag=1, RiskGrade__in=[2, 3, 6, 7, 10, 11, 14, 15]).count()
            no_other_cnt = tort_cnt_obj.filter(tortflag=1, RiskGrade__in=[1, 3, 5, 7, 9, 11, 13, 15]).count()
            yes_ban_cnt = tort_cnt_obj.filter(tortflag=2, RiskGrade__in=[8, 9, 10, 11, 12, 13, 14, 15]).count()
            yes_scope_cnt = tort_cnt_obj.filter(tortflag=2, RiskGrade__in=[4, 5, 6, 7, 12, 13, 14, 15]).count()
            yes_pot_cnt = tort_cnt_obj.filter(tortflag=2, RiskGrade__in=[2, 3, 6, 7, 10, 11, 14, 15]).count()
            yes_other_cnt = tort_cnt_obj.filter(tortflag=2, RiskGrade__in=[1, 3, 5, 7, 9, 11, 13, 15]).count()
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

            actionable_order_cnt = t_amazon_actionable_order_data.objects.all().values('id').count()
            finance_record_cnt = t_amazon_finance_record.objects.all().values('id').count()
            can_load_cnt = t_online_info_amazon_listing.objects.filter(shop_status=0, refresh_status=0, is_fba=0, Status='Inactive', product_status=1).values('id').count()
            can_unload_cnt = t_online_info_amazon_listing.objects.filter(shop_status=0, refresh_status=0, is_fba=0, Status='Active', product_status__in=(2, 3, 4)).values(
                'id').count()
            load_cnt = t_amazon_auto_load.objects.filter(deal_type='load').values('id').count()
            unload_cnt = t_amazon_auto_load.objects.filter(deal_type='unload').values('id').count()
            inventory_age_cnt = t_amazon_fba_inventory_age.objects.filter(Q(qty_to_be_charged_ltsf_6_mo__gt=0)|Q(qty_to_be_charged_ltsf_12_mo__gt=0)).values('id').count()
            tort_cnt_obj = t_online_info_amazon_listing.objects.filter(shop_status=0, refresh_status=0, Status='Active')
            no_ban_cnt = tort_cnt_obj.filter(tortflag=1, RiskGrade__in=[8, 9, 10, 11, 12, 13, 14, 15]).count()
            no_scope_cnt = tort_cnt_obj.filter(tortflag=1, RiskGrade__in=[4, 5, 6, 7, 12, 13, 14, 15]).count()
            no_pot_cnt = tort_cnt_obj.filter(tortflag=1, RiskGrade__in=[2, 3, 6, 7, 10, 11, 14, 15]).count()
            no_other_cnt = tort_cnt_obj.filter(tortflag=1, RiskGrade__in=[1, 3, 5, 7, 9, 11, 13, 15]).count()
            yes_ban_cnt = tort_cnt_obj.filter(tortflag=2, RiskGrade__in=[8, 9, 10, 11, 12, 13, 14, 15]).count()
            yes_scope_cnt = tort_cnt_obj.filter(tortflag=2, RiskGrade__in=[4, 5, 6, 7, 12, 13, 14, 15]).count()
            yes_pot_cnt = tort_cnt_obj.filter(tortflag=2, RiskGrade__in=[2, 3, 6, 7, 10, 11, 14, 15]).count()
            yes_other_cnt = tort_cnt_obj.filter(tortflag=2, RiskGrade__in=[1, 3, 5, 7, 9, 11, 13, 15]).count()

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

        t_templet_amazon_publish_draft_from_ebay_count = t_templet_amazon_publish_draft_from_ebay.objects.all().values('id').count()

        amazon_upload = {
            "name": u"刊登",
            "code": "12",
            "icon": "icon-minus-sign",
            "parentCode": "01",
            "selected": "",
            "to_url": '',
            "flag": "pub_all",
            "child": [
                {
                    "name": u"eBay待刊登模板(%s)" % t_templet_amazon_publish_draft_from_ebay_count,
                    "code": "128",
                    "icon": "",
                    "parentCode": "12",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_publish_draft_from_ebay/',
                    "flag": "8",
                    "child": []
                },
                {
                    "name": u"草稿箱(%s)" % t_templet_amazon_collection_box_count,
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
                    "code": "124",
                    "icon": "",
                    "parentCode": "12",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_upload_fail/',
                    "flag": "4",
                    "child": []
                },
                {
                    "name": u"发布成功(%s)" % t_templet_amazon_wait_upload_count_success,
                    "code": "125",
                    "icon": "",
                    "parentCode": "12",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_upload_result/?_p_status=SUCCESS',
                    "flag": "5",
                    "child": []
                },
                {
                    "name": u"发布后图片缺失(%s)" % t_templet_amazon_upload_result_lose_pic_count,
                    "code": "126",
                    "icon": "",
                    "parentCode": "12",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_upload_result_lose_pic/',
                    "flag": "6",
                    "child": []
                },
                {
                    "name": u"回收站(%s)" % t_templet_amazon_recycle_bin_count,
                    "code": "127",
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
        if self.request.GET.get('Status'):
            flag = self.request.GET.get('Status')
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
        if 't_templet_amazon_publish_draft_from_ebay' in self.request.get_full_path():
            flag = '8'

        search_str = ''
        inactive_shop_str = ''
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
                        "to_url": '/Project/admin/skuapp/t_online_info_amazon_listing/?Status=Active&_p_refresh_status=0&_p_shop_status=0%s' % search_str,
                        "flag": 'Active',
                        "child": []
                    },

                    {
                        "name": u"未启用(%s)" % inactive_list_cnt,
                        "icon": "",
                        "code": "110102",
                        "parentCode": "1101",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_online_info_amazon_listing/?Status=Inactive&_p_refresh_status=0&_p_shop_status=0%s' % search_str,
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
            "name": u"已关闭店铺",
            "code": "1102",
            "icon": "icon-minus-sign",
            "parentCode": "11",
            "selected": "",
            "to_url": '',
            "flag": "",
            "child":
                [
                    {
                        "name": u"商品列表(%s)" % inactive_shop_cnt,
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
                        "name": u"周转率",
                        "icon": "",
                        "code": "110307",
                        "parentCode": "1103",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_conversion_result/',
                        "flag": 'conversion_result',
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

        if shopname:
            shop_str = '&shopname=%s' % shopname
        else:
            shop_str = ''

        amazon_auto_upload = {
            "name": u"亚马逊上架",
            "code": "1104",
            "icon": "icon-minus-sign",
            "parentCode": "11",
            "selected": "",
            "to_url": '',
            "flag": "",
            "child":
                [
                    {
                        "name": u"可上架(%s)" % can_load_cnt,
                        "icon": "",
                        "code": "110401",
                        "parentCode": "1104",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_online_info_amazon_listing/?_p_Status=Inactive&_p_refresh_status=0&_p_shop_status=0&_p_is_fba=0&_p_product_status=1%s' % shop_str,
                        "flag": 'can_upload',
                        "child": []
                    },

                    {
                        "name": u"上架记录(%s)" % load_cnt,
                        "icon": "",
                        "code": "110402",
                        "parentCode": "1104",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_auto_load/?_p_deal_type=load',
                        "flag": 'upload_log',
                        "child": []
                    },
                ]
        }

        amazon_auto_unload = {
            "name": u"亚马逊下架",
            "code": "1105",
            "icon": "icon-minus-sign",
            "parentCode": "11",
            "selected": "",
            "to_url": '',
            "flag": "",
            "child":
                [
                    {
                        "name": u"可下架(%s)" % can_unload_cnt,
                        "icon": "",
                        "code": "110501",
                        "parentCode": "1105",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_online_info_amazon_listing/?_p_Status=Active&_p_refresh_status=0&_p_shop_status=0&_p_is_fba=0&product_status=2,3,4%s' % shop_str,
                        "flag": 'can_unload',
                        "child": []
                    },

                    {
                        "name": u"下架记录(%s)" % unload_cnt,
                        "icon": "",
                        "code": "110502",
                        "parentCode": "1105",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_auto_load/?_p_deal_type=unload',
                        "flag": 'unload_log',
                        "child": []
                    },
                ]
        }

        qs = t_templet_amazon_follow.objects.exclude(crawl_result__contains=u'删除')
        follow1 = qs.filter(SKU__isnull=True, price__gte=0.0).values('id').count()
        follow2 = qs.filter(ispublish__isnull=True, SKU__isnull=False).values('id').count()
        follow4 = qs.filter(price=0.0).values('id').count()
        follow5 = qs.filter(ispublish__isnull=False).values('id').count()
        amazon_follow = {
            "name": u"亚马逊跟卖",
            "code": "1106",
            "icon": "icon-minus-sign",
            "parentCode": "11",
            "selected": "",
            "to_url": '',
            "flag": "",
            "child": [
                {
                    "name": u"待判定SKU(%s)" % follow1,
                    "icon": "",
                    "code": "110601",
                    "parentCode": "1106",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_follow/?dataflag=1',
                    "flag": 'follow1',
                    "child": []
                },
                {
                    "name": u"待确认刊登(%s)" % follow2,
                    "icon": "",
                    "code": "110602",
                    "parentCode": "1106",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_follow/?dataflag=2',
                    "flag": 'follow2',
                    "child": []
                },
                {
                    "name": u"刊登情况(%s)" % follow5,
                    "icon": "",
                    "code": "110605",
                    "parentCode": "1106",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_follow/?dataflag=5',
                    "flag": 'follow5',
                    "child": []
                },
                {
                    "name": u"采集异常(%s)" % follow4,
                    "icon": "",
                    "code": "110604",
                    "parentCode": "1106",
                    "selected": "",
                    "to_url": '/Project/admin/skuapp/t_templet_amazon_follow/?dataflag=4',
                    "flag": 'follow4',
                    "child": []
                },
            ]

        }
        
        amazon_online_report_data = {
            "name": u"报告数据",
            "code": "1107",
            "icon": "icon-minus-sign",
            "parentCode": "11",
            "selected": "",
            "to_url": '',
            "flag": "",
            "child":
                [

                    {
                        "name": u"已移除订单(%s)" % t_remove_order_cnt,
                        "icon": "",
                        "code": "110701",
                        "parentCode": "1107",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_removal_order_detail/',
                        "flag": 'removal_order',
                        "child": []
                    },

                    {
                        "name": u"订单详情(%s)" % all_orders_cnt,
                        "icon": "",
                        "code": "110702",
                        "parentCode": "1107",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_all_orders_data/',
                        "flag": 'all_orders',
                        "child": []
                    },

                    {
                        "name": u"未发货订单(%s)" % actionable_order_cnt,
                        "icon": "",
                        "code": "110703",
                        "parentCode": "1107",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_actionable_order_data/',
                        "flag": 'actionable_order_data',
                        "child": []
                    },

                    {
                        "name": u"订单交易数据(%s)" % finance_record_cnt,
                        "icon": "",
                        "code": "110704",
                        "parentCode": "1107",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_finance_record/',
                        "flag": 'finance_record',
                        "child": []
                    },

                    {
                        "name": u"库龄数据(%s)" % inventory_age_cnt,
                        "icon": "",
                        "code": "110705",
                        "parentCode": "1107",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_amazon_fba_inventory_age/',
                        "flag": 'inventory_age',
                        "child": []
                    },
                ]
        }

        active_listing_url = '/Project/admin/skuapp/t_online_info_amazon_listing/?Status=Active&_p_shop_status=0&_p_refresh_status=0' + shop_str
        title_tort_word = {
            "name": u"在线链接标题侵权",
            "code": "1108",
            "icon": "icon-minus-sign",
            "parentCode": "11",
            "selected": "",
            "to_url": '',
            "flag": "",
            "child": [
                {
                    "name": u"未处理绝对禁止(%s)" % no_ban_cnt,
                    "icon": "",
                    "code": "110801",
                    "parentCode": "1108",
                    "selected": "",
                    "to_url": active_listing_url + '&_p_tortflag=1&riskgrade=3',
                    "flag": 'no_ban',
                    "child": []
                },

                {
                    "name": u"未处理限定范围(%s)" % no_scope_cnt,
                    "icon": "",
                    "code": "110802",
                    "parentCode": "1108",
                    "selected": "",
                    "to_url": active_listing_url + '&_p_tortflag=1&riskgrade=2',
                    "flag": 'no_scope',
                    "child": []
                },

                {
                    "name": u"未处理潜在风险(%s)" % no_pot_cnt,
                    "icon": "",
                    "code": "110803",
                    "parentCode": "1108",
                    "selected": "",
                    "to_url": active_listing_url + '&_p_tortflag=1&riskgrade=1',
                    "flag": 'no_pot',
                    "child": []
                },

                {
                    "name": u"未处理其他(%s)" % no_other_cnt,
                    "icon": "",
                    "code": "110804",
                    "parentCode": "1108",
                    "selected": "",
                    "to_url": active_listing_url + '&_p_tortflag=1&riskgrade=0',
                    "flag": 'no_other',
                    "child": []
                },

                {
                    "name": u"已处理绝对禁止(%s)" % yes_ban_cnt,
                    "icon": "",
                    "code": "110805",
                    "parentCode": "1108",
                    "selected": "",
                    "to_url": active_listing_url + '&_p_tortflag=2&riskgrade=3',
                    "flag": 'yes_ban',
                    "child": []
                },

                {
                    "name": u"已处理限定范围(%s)" % yes_scope_cnt,
                    "icon": "",
                    "code": "110806",
                    "parentCode": "1108",
                    "selected": "",
                    "to_url": active_listing_url + '&_p_tortflag=2&riskgrade=2',
                    "flag": 'yes_scope',
                    "child": []
                },

                {
                    "name": u"已处理潜在风险(%s)" % yes_pot_cnt,
                    "icon": "",
                    "code": "110807",
                    "parentCode": "1108",
                    "selected": "",
                    "to_url": active_listing_url + '&_p_tortflag=2&riskgrade=1',
                    "flag": 'yes_pot',
                    "child": []
                },

                {
                    "name": u"已处理其他(%s)" % yes_other_cnt,
                    "icon": "",
                    "code": "110808",
                    "parentCode": "1108",
                    "selected": "",
                    "to_url": active_listing_url + '&_p_tortflag=2&riskgrade=0',
                    "flag": 'yes_other',
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
                title_tort_word,
                amazon_auto_upload,
                amazon_auto_unload,
                amazon_follow,
                amazon_online_report_data,
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
                    "name": u"运费模板(%s)" % template_count,
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
        elif 't_templet_amazon_follow' in self.request.get_full_path():
            if 'dataflag=1' in self.request.get_full_path():
                flag = 'follow1'
            elif 'dataflag=2' in self.request.get_full_path():
                flag = 'follow2'
            elif 'dataflag=4' in self.request.get_full_path():
                flag = 'follow4'
            elif 'dataflag=5' in self.request.get_full_path():
                flag = 'follow5'
        elif 't_amazon_finance_record' in self.request.get_full_path():
            flag = 'finance_record'
        elif 't_amazon_fba_inventory_age' in self.request.get_full_path():
            flag = 'inventory_age'
        elif '_p_tortflag=1&riskgrade=3' in self.request.get_full_path():
            flag = 'no_ban'
        elif '_p_tortflag=1&riskgrade=2' in self.request.get_full_path():
            flag = 'no_scope'
        elif '_p_tortflag=1&riskgrade=1' in self.request.get_full_path():
            flag = 'no_pot'
        elif '_p_tortflag=1&riskgrade=0' in self.request.get_full_path():
            flag = 'no_other'
        elif '_p_tortflag=2&riskgrade=3' in self.request.get_full_path():
            flag = 'yes_ban'
        elif '_p_tortflag=2&riskgrade=2' in self.request.get_full_path():
            flag = 'yes_scope'
        elif '_p_tortflag=2&riskgrade=1' in self.request.get_full_path():
            flag = 'yes_pot'
        elif '_p_tortflag=2&riskgrade=0' in self.request.get_full_path():
            flag = 'yes_other'
        elif 't_amazon_conversion_result' in self.request.get_full_path():
            flag = 'conversion_result'

        if '_p_refresh_status=1' in self.request.get_full_path():
            flag = 'remove'

        if '_p_shop_status=1' in self.request.get_full_path():
            flag = 'inactive_shop'

        if self.request.GET.get('_p_Status') == 'Active':
            flag = 'can_unload'

        if self.request.GET.get('_p_Status') == 'Inactive':
            flag = 'can_upload'

        if '_p_deal_type=load' in self.request.get_full_path():
            flag = 'upload_log'

        if '_p_deal_type=unload' in self.request.get_full_path():
            flag = 'unload_log'




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
