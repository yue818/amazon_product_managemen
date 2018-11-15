#-*-coding:utf-8-*-

from django.template import loader
from xadmin.views import BaseAdminPlugin
from django.contrib import messages
import datetime
import urlparse
from django.db.models import Q
from django.db import connection
from skuapp.table.t_stocking_demand_list import t_stocking_demand_list
from skuapp.table.t_stocking_demand_audit import t_stocking_demand_audit
from skuapp.table.t_stocking_demand_passaudit import t_stocking_demand_passaudit
from skuapp.table.t_stocking_purchase_order import t_stocking_purchase_order
from skuapp.table.t_set_warehouse_storage_situation_list import t_set_warehouse_storage_situation_list
from skuapp.table.t_shipping_management import t_shipping_management
from skuapp.table.t_stocking_check_report import t_stocking_check_report
class site_left_menu_stocking_purchase_Plugin(BaseAdminPlugin):
    site_left_menu_stocking_purchase = False

    def init_request(self, *args, **kwargs):
        return bool(self.site_left_menu_stocking_purchase)

    def block_left_navbar(self, context, nodes):
        try:
            t_stocking_demand_list_count = t_stocking_demand_list.objects.values('id').count()
            t_stocking_demand_audit_count = t_stocking_demand_audit.objects.filter(Status='noaudit').values('id').count()
            t_stocking_demand_passaudit_count = t_stocking_demand_passaudit.objects.filter(Status='audit').values('id').count()
            t_stocking_purchase_order_count = t_stocking_purchase_order.objects.values('id').count()
            t_set_warehouse_storage_situation_list_count = t_set_warehouse_storage_situation_list.objects.values('id').count()
            t_shipping_management_count = t_shipping_management.objects.values('id').count()
            t_stocking_check_report_count = t_stocking_check_report.objects.values('id').count()

            sourceURL = str(context['request']).split("'")[1]
            title_list = [{'title': u'海外仓备货流程', 'selected': '0'}]
            test_list = [{'url': '/Project/admin/skuapp/t_stocking_demand_list/?Status=notgenerated', 'value': u'1-备货需求列表('+str(t_stocking_demand_list_count)+')',
                          'title': u'海外仓备货流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_stocking_demand_audit/','value': u'2-未生成采购计划审核(' + str(t_stocking_demand_audit_count) + ')',
                          'title': u'海外仓备货流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_stocking_demand_passaudit/','value': u'3-生成采购计划(' + str(t_stocking_demand_passaudit_count) + ')',
                          'title': u'海外仓备货流程', 'selected': '0'},
                        {'url': '/Project/admin/skuapp/t_stocking_purchase_order/?Status=notyet', 'value': u'4-采购计划('+str(t_stocking_purchase_order_count)+')',
                          'title': u'海外仓备货流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_set_warehouse_storage_situation_list/?Delivery_status=notyet', 'value': u'5-集货仓入库一览('+str(t_set_warehouse_storage_situation_list_count)+')',
                          'title': u'海外仓备货流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_shipping_management/?Status=notyet', 'value': u'6-发货管理('+str(t_shipping_management_count)+')',
                          'title': u'海外仓备货流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_stocking_check_report/', 'value': u'7-质检报告('+str(t_stocking_check_report_count)+')',
                          'title': u'海外仓备货流程', 'selected': '0'},]
            title = ''
            flag = 0
            for tl in test_list:
                to_url = tl['url']
                if to_url != sourceURL:
                    if '?' not in tl['url']:
                        to_url = to_url + '?'
                    else:
                        to_url = to_url.split('?')[0]
                if to_url in sourceURL:
                    title = tl['title']
                    tl['selected'] = '1'
                    flag = 1
            if title:
                for titleout in title_list:
                    if titleout['title'] == title:
                        titleout['selected'] = '1'
            if flag == 1:
                nodes.append(loader.render_to_string('site_left_menu_stocking_purchase.html',
                                                     {'title_list': title_list, 'test_list': test_list, 'sourceURL': sourceURL}))
        except Exception as e:
            messages.info(self.request,u'error:%s,加载左侧树形菜单栏存在问题，请联系开发人员。'% ( str(e)))
