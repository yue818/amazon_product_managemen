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
from django.db import connection
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: wish_listing_readonly_P.py
 @time: 2018/2/28 8:53
"""

class wish_listing_readonly_P(BaseAdminPlugin):
    wish_listing_readonly_f = False

    def init_request(self, *args, **kwargs):
        return bool(self.wish_listing_readonly_f)

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

        shopname = self.request.GET.get('shopname')
        if shopname:
            qs = self.model.objects.filter(ShopName='Wish-' + shopname.split('-')[-1].zfill(4))
            vflag = 0
        else:
            qs = self.model.objects.none()
            vflag = 1

        full_path = self.request.get_full_path().replace('EXPRESS=STANDARD', '').replace('EXPRESS=DE', '') \
            .replace('EXPRESS=GB', '').replace('EXPRESS=US', '').replace('?&', '?').replace('&&', '&')
        if full_path[-1:] == '&':
            full_path = full_path[:-1]

        params = None
        if full_path:
            params = full_path.split('?')[-1]

        if vflag == 1:
            aNUM = self.get_result_count("select * from  tri_db.t_online_info_wish")
            if not aNUM:
                aNUM = self.model.objects.all().count()

            if params == 'status=online':
                oNUM = self.request.result_count
            else:
                oNUM = self.get_result_count("select * from  tri_db.t_online_info_wish_usual_on;")
            if not oNUM:
                oNUM = self.model.objects.all().filter(AdStatus='1', SName='0').count()  # 在线商品

            if params == 'status=offline':
                offNUM = self.request.result_count
            else:
                offNUM = self.get_result_count("select * from  tri_db.t_online_info_wish_usual_off;")
            if not offNUM:
                offNUM = self.model.objects.all().filter(AdStatus='0', SName='0').count()  # 不在线商品

            nNUM = oNUM + offNUM  # 正常商品

            if params == 'status=storeError':
                esNUM = self.request.result_count
            else:
                esNUM = self.get_result_count("select * from  tri_db.t_online_info_wish_unusual;")
            if not esNUM:
                esNUM = self.model.objects.all().filter(SName='-1').count()  # 店铺状态异常

            if params == 'status=doError':
                eNUM = self.request.result_count
            else:
                eNUM = self.get_result_count("select * from  tri_db.t_online_info_wish_op_unusual;")
            if not eNUM:
                eNUM = qs.filter(AdStatus__in=['-1', '-2'], SName='0').count()  # 链接异常

            ENUM = esNUM + eNUM  # 异常链接
        else:
            aNUM = qs.count()  # 全部商品
            oNUM = qs.filter(AdStatus='1', SName='0').count()  # 在线商品
            offNUM = qs.filter(AdStatus='0', SName='0').count() # 不在线商品
            nNUM = oNUM + offNUM  # 正常商品
            esNUM = qs.filter(SName='-1').count()  # 店铺状态异常
            eNUM  = qs.filter(AdStatus__in=['-1', '-2'], SName='0').count()  # 链接异常
            ENUM = esNUM + eNUM  # 异常链接

        nowurl_store = self.url_path()

        menu_list = [
            {
                "name": u"店铺管理",
                "code": "00",
                "icon": "icon-th",
                "selected": "",
                "to_url": "",
                "flag": "gl",
                "child": [
                    {
                        "name": u"全部产品(%s)" % aNUM,
                        "code": "01",
                        "icon": "icon-minus-sign",
                        "parentCode": "00",
                        "selected": "",
                        "to_url": nowurl_store + 'status=all',
                        "flag": "all",
                        "child": [
                            {
                                "name": u"正常产品(%s)" % nNUM,
                                "code": "11",
                                "icon": "icon-minus-sign",
                                "parentCode": "01",
                                "selected": "",
                                "to_url": "",
                                "flag": "",
                                "child": [
                                    {
                                        "name": u"在线(%s)" % oNUM,
                                        "icon": "",
                                        "code": "111",
                                        "parentCode": "11",
                                        "selected": "",
                                        "to_url": nowurl_store + 'status=online',
                                        "flag": 'online',
                                        "child": []
                                    },
                                    {
                                        "name": u"不在线(%s)" % offNUM,
                                        "icon": "",
                                        "code": "112",
                                        "parentCode": "11",
                                        "selected": "",
                                        "to_url": nowurl_store + 'status=offline',
                                        "flag": 'offline',
                                        "child": []
                                    },
                                ]
                            },
                            {
                                "name": u"异常产品(%s)" % ENUM,
                                "code": "12",
                                "icon": "icon-minus-sign",
                                "parentCode": "01",
                                "selected": "",
                                "to_url": "",
                                "flag": "",
                                "child": [
                                    {
                                        "name": u"店铺状态异常(%s)" % esNUM,
                                        "icon": "",
                                        "code": "121",
                                        "parentCode": "12",
                                        "selected": "",
                                        "to_url": nowurl_store + 'status=storeError',
                                        "flag": 'storeError',
                                        "child": []
                                    },
                                    {
                                        "name": u"操作异常及告警(%s)" % eNUM,
                                        "icon": "",
                                        "code": "122",
                                        "parentCode": "12",
                                        "selected": "",
                                        "to_url": nowurl_store + 'status=doError',
                                        "flag": 'doError',
                                        "child": []
                                    }
                                ]
                            },
                        ]
                    }
                ]
            },
        ]

        flag = self.request.GET.get('status')

        menu_list, show_flag = self.show_select_flag(menu_list, flag)

        nodes.append(loader.render_to_string('site_left_menu_tree_Plugin.html',{'menu_list': json.dumps(menu_list)},context_instance=RequestContext(self.request)))
