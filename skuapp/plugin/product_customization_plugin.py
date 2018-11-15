#-*-coding:utf-8-*-
import json
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages
from django.template import RequestContext
from skuapp.table.v_product_customization_show import v_product_customization_show
from skuapp.table.t_progress_tracking_of_product_customization_table import t_progress_tracking_of_product_customization_table

from datetime import datetime


class product_customization_plugin(BaseAdminPlugin):
    left_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.left_flag)

    def url_path(self):
        url_tmps = self.request.get_full_path().split('?')
        param_list = []
        if len(url_tmps) >= 2 and url_tmps[-1].strip() != '':
            for param in url_tmps[-1].strip().split('&'):
                if param.split('=')[0] != 'status':
                    param_list.append(param)
        if param_list:
            url = url_tmps[0] + '?' + '&'.join(param_list) + '&'
        else:
            url = url_tmps[0] + '?'

        return url


    def show_select_flag(self, m_list, flag):
        show_flag = 0
        for menu in m_list:
            if menu['flag'] == flag:
                menu['selected'] = 'selected'
                show_flag = 1
            if menu['child']:
                menu['child'], show_flag = self.show_select_flag(menu['child'], flag)

        return m_list,show_flag


    def block_left_navbar(self, context, nodes):

        nowurl_store1 = '/'
        nowurl_store2 = '/'
        if self.model._meta.model_name == 't_progress_tracking_of_product_customization_table':
            #nowurl_store1 = self.url_path()
            nowurl_store1 = '/Project/admin/skuapp/t_progress_tracking_of_product_customization_table/?'
            nowurl_store2 = '/Project/admin/skuapp/v_product_customization_show/?'
        elif self.model._meta.model_name == 'v_product_customization_show':
            nowurl_store1 = '/Project/admin/skuapp/t_progress_tracking_of_product_customization_table/?'
            nowurl_store2 = '/Project/admin/skuapp/v_product_customization_show/?'
            #nowurl_store2 = self.url_path()

        isClothes = self.request.GET.get('clothes', '0')
        objs = t_progress_tracking_of_product_customization_table.objects.all()

        if isClothes == '0':
            wNUM = objs.filter(RateOfProgress__exact='0', FromClothes__exact='0', FinishTime__gte=datetime.now()).count()
            iNUM = objs.filter(RateOfProgress__exact='1', FromClothes__exact='0').exclude(FinishTime__lt=datetime.now()).count()
            dNUM = objs.filter(RateOfProgress__exact='2', FromClothes__exact='0').count()
            cNUM = objs.filter(FinishTime__lt=datetime.now(), FromClothes__exact='0').exclude(RateOfProgress__in=['2', '-1']).count()
            nNUM = objs.filter(RateOfProgress__exact='-1', FromClothes__exact='0').count()
            lNUM = v_product_customization_show.objects.filter(FromClothes__exact='0').count()
        else:
            iNUM = objs.filter(RateOfProgress__exact='1', FromClothes__exact='1').exclude(FinishTime__lt=datetime.now()).count()
            dNUM = objs.filter(RateOfProgress__exact='2', FromClothes__exact='1').count()
            cNUM = objs.filter(FinishTime__lt=datetime.now(), FromClothes__exact='1').exclude(RateOfProgress__in=['2', '-1']).count()
            lNUM = v_product_customization_show.objects.filter(FromClothes__exact='1').count()


        if isClothes == '0':

            menu_list = [
                {
                    "name": u"产品定做落地跟踪表",
                    "code": "00",
                    "icon": "icon-th",
                    "selected": "",
                    "to_url": "",
                    "flag": "home",
                    "child": [
                        {
                            "name": u"待审核(%s)" % wNUM,
                            "code": "01",
                            "icon": "icon-minus-sign",
                            "parentCode": "00",
                            "selected": "",
                            "to_url": nowurl_store1 + 'status=pending',
                            "flag": "pending",
                            "child": []
                        },
                        {
                            "name": u"生产中(%s)" % iNUM,
                            "code": "02",
                            "icon": "icon-minus-sign",
                            "parentCode": "00",
                            "selected": "",
                            "to_url": nowurl_store1 + 'status=producing',
                            "flag": "producing",
                            "child": []
                        },
                        {
                            "name": u"已完成(%s)" % dNUM,
                            "code": "03",
                            "icon": "icon-minus-sign",
                            "parentCode": "00",
                            "selected": "",
                            "to_url": nowurl_store1 + 'status=completed',
                            "flag": "completed",
                            "child": []
                        },
                        {
                            "name": u"已超时(%s)" % cNUM,
                            "code": "04",
                            "icon": "icon-minus-sign",
                            "parentCode": "00",
                            "selected": "",
                            "to_url": nowurl_store1 + 'status=time_out',
                            "flag": "time_out",
                            "child": []
                        },
                        {
                            "name": u"被废弃(%s)" % nNUM,
                            "code": "05",
                            "icon": "icon-minus-sign",
                            "parentCode": "00",
                            "selected": "",
                            "to_url": nowurl_store1 + 'status=nullify',
                            "flag": "nullify",
                            "child": []
                        },
                        {
                            "name": u"产品定做落地库存查询(%s)" % lNUM,
                            "code": "06",
                            "icon": "icon-minus-sign",
                            "parentCode": "00",
                            "selected": "",
                            "to_url": nowurl_store2 + 'status=done_show',
                            "flag": "done_show",
                            "child": []
                        },
                    ]
                },
            ]
        else:
            menu_list = [
                {
                    "name": u"服装定做落地跟踪表",
                    "code": "00",
                    "icon": "icon-th",
                    "selected": "",
                    "to_url": "",
                    "flag": "home",
                    "child": [
                        {
                            "name": u"生产中(%s)" % iNUM,
                            "code": "02",
                            "icon": "icon-minus-sign",
                            "parentCode": "00",
                            "selected": "",
                            "to_url": nowurl_store1 + 'status=producing&clothes=1',
                            "flag": "producing",
                            "child": []
                        },
                        {
                            "name": u"已完成(%s)" % dNUM,
                            "code": "03",
                            "icon": "icon-minus-sign",
                            "parentCode": "00",
                            "selected": "",
                            "to_url": nowurl_store1 + 'status=completed&clothes=1',
                            "flag": "completed",
                            "child": []
                        },
                        {
                            "name": u"已超时(%s)" % cNUM,
                            "code": "04",
                            "icon": "icon-minus-sign",
                            "parentCode": "00",
                            "selected": "",
                            "to_url": nowurl_store1 + 'status=time_out&clothes=1',
                            "flag": "time_out",
                            "child": []
                        },
                        {
                            "name": u"服装定做落地库存查询(%s)" % lNUM,
                            "code": "06",
                            "icon": "icon-minus-sign",
                            "parentCode": "00",
                            "selected": "",
                            "to_url": nowurl_store2 + 'status=done_show&clothes=1',
                            "flag": "done_show",
                            "child": []
                        },
                    ]
                },
            ]

        flag = self.request.GET.get('status')

        menu_list, show_flag = self.show_select_flag(menu_list, flag)

        nodes.append(loader.render_to_string('site_left_menu_tree_Plugin.html',{'menu_list': json.dumps(menu_list)},context_instance=RequestContext(self.request)))
