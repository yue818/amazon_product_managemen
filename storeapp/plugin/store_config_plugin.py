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
 @file: store_config_plugin.py
 @time: 2018/2/28 8:53
"""
from django.db import connection
from brick.table.t_store_configuration_file import t_store_configuration_file
from skuapp.table.t_store_configuration_file import t_store_configuration_file as tt

import copy
from django.contrib import messages

t_store_configuration_file_obj = t_store_configuration_file(connection)
class store_config_plugin(BaseAdminPlugin):
    store_config_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.store_config_flag)

    def get_plat(self,s):
        if s == u'未知平台':
            r = None
        else:
            r = s
        return r

    def get_status(self,s):
        if s == 's':
            r = '0'
        elif s == 'e':
            r = '-1'
        elif s == 'o':
            r = None
        return r

    def get_layerd(self,s):
        if s == 'A':
            r = 'A'
        elif s == 'B':
            r = 'B'
        elif s == 'C':
            r = 'C'
        elif s == 'D':
            r = 'D'
        elif s == u'未知分层':
            r = None
        return r

    def show_select_flag(self, m_list, flag):
        show_flag = 0
        for menu in m_list:
            if menu['flag'] == flag:
                menu['selected'] = 'selected'
                show_flag = 1
            if menu['child']:
                menu['child'], show_flag = self.show_select_flag(menu['child'], flag)

        return m_list,show_flag

    def get_media(self, media):
        media.add_js([self.static('store_config/store_change_status.js')])

        return media

    def block_left_navbar(self, context, nodes):
        sNUM = 0
        eNUM = 0
        oNUM = 0

        menu_list = [
            {
                "name": u"店铺配置文件",
                "code": "00",
                "icon": "icon-th",
                "selected": "",
                "to_url": "",
                "flag": "config",
                "child": []
            },
        ]

        sdict = {}
        nResult = t_store_configuration_file_obj.status_num()
        if nResult['errorcode'] == 1 :
            for obj in nResult['data']:
                PlatformID = obj[1] if obj[1] else u'unknown'

                ndict = copy.deepcopy(sdict[PlatformID]) if sdict.get(PlatformID) else {}

                sdict[PlatformID] = {}
                sdict[PlatformID]['s'] = ndict.get('s', 0)
                sdict[PlatformID]['e'] = ndict.get('e', 0)
                sdict[PlatformID]['o'] = ndict.get('o', 0)

                if obj[2] == '0':
                    sdict[PlatformID]['s'] = obj[0] + ndict.get('s', 0)

                if obj[2] == '-1':
                    sdict[PlatformID]['e'] = obj[0] + ndict.get('e', 0)

                if not obj[2]:
                    sdict[PlatformID]['o'] = obj[0] + ndict.get('o', 0)

        slist = []
        if sdict.get('Wish'):
            slist.append({'Wish':sdict.get('Wish')})
        if sdict.get('eBay'):
            slist.append({'eBay':sdict.get('eBay')})
        if sdict.get('AMZ'):
            slist.append({'AMZ':sdict.get('AMZ')})
        if sdict.get('Ali'):
            slist.append({'Ali':sdict.get('Ali')})
        for i in sdict:
            if i not in ['eBay','Wish','AMZ','Ali'] and i != 'unknown':
                slist.append({i:sdict[i]})
        if sdict.get('unknown'):
            slist.append({'unknown':sdict['unknown']})


        i = 0
        for dict in slist:
            for k, v in dict.items():
                i = i + 1
                cdict = {
                    "name": u"%s" % k,
                    "code": u"%s%s" % (k, i),
                    "icon": "icon-minus-sign",
                    "parentCode": "00",
                    "selected": "",
                    "to_url": '',
                    "flag": "",
                    "child": []
                }
                j = 0
                for ok, ov in v.items():
                    j = j + 1
                    if ok == 's':
                        fname = u'正常'
                    elif ok == 'e':
                        fname = u'异常'
                    else:
                        fname = u'未知状态'
                    codict = {
                        "name": u"%s(%s)" % (fname, ov),
                        "icon": "",
                        "code": u"%s%s%s" % (k, i, j),
                        "parentCode": u"%s%s" % (k, i),
                        "selected": "",
                        "to_url": u'/Project/admin/skuapp/t_store_configuration_file/?status=%s_%s' % (k, ok),
                        "flag": u'%s_%s' % (k, ok),
                        "child": []
                    }
                    m = 0
                    if k in ['Wish', 'eBay', 'AMZ', 'Ali']:
                        if k == u'AMZ':
                            for x in ['A','B','C','D',u'未知分层']:
                                m = m + 1
                                cou = tt.objects.all().filter(PlatformID=self.get_plat(k), Status=self.get_status(ok), ShopLayered=self.get_layerd(x)).count()
                                coodict = {
                                    "name": u"%s(%s)" % (x,cou),
                                    "icon": "",
                                    "code": u"%s%s%s%s" % (k, i, j, m),
                                    "parentCode": u"%s%s%s" % (k, i, j),
                                    "selected": "",
                                    "to_url": u'/Project/admin/skuapp/t_store_configuration_file/?status=%s_%s_%s' % (k, ok, x),
                                    "flag": u'%s_%s_%s' % (k, ok, x),
                                    "child": []
                                }
                                codict['child'].append(coodict)
                        else:
                            for x in ['A','B','C',u'未知分层']:
                                m = m + 1
                                cou = tt.objects.all().filter(PlatformID=self.get_plat(k), Status=self.get_status(ok), ShopLayered=self.get_layerd(x)).count()
                                coodict = {
                                    "name": u"%s(%s)" % (x,cou),
                                    "icon": "",
                                    "code": u"%s%s%s%s" % (k, i, j, m),
                                    "parentCode": u"%s%s%s" % (k, i, j),
                                    "selected": "",
                                    "to_url": u'/Project/admin/skuapp/t_store_configuration_file/?status=%s_%s_%s' % (k, ok, x),
                                    "flag": u'%s_%s_%s' % (k, ok, x),
                                    "child": []
                                }
                                codict['child'].append(coodict)

                    cdict['child'].append(codict)

            menu_list[0]['child'].append(cdict)
        flag = self.request.GET.get('status')

        menu_list, show_flag = self.show_select_flag(menu_list, flag)

        nodes.append(loader.render_to_string('site_left_menu_tree_Plugin.html',{'menu_list': json.dumps(menu_list)},context_instance=RequestContext(self.request)))
