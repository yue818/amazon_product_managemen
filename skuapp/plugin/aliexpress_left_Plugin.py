#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2018-08-20 10:45
@Author  : chenchen
@Site    : aliexpress_left_Plugin
@File    : aliexpress_left_Plugin.py
@Software: PyCharm
'''
# -*-coding:utf-8-*-

import json

from xadmin.views import BaseAdminPlugin
from django.db.models import Q
from django.db import connection
from django.template import loader
from django.contrib import messages
from django.template import RequestContext
from skuapp.table.t_product_enter_ed_aliexpress import t_product_enter_ed_aliexpress
import datetime

# from lzd_app.table.t_online_info_lazada import t_online_info_lazada
# from lzd_app.table.t_online_info_lazada_detail import t_online_info_lazada_detail


class aliexpress_left_Plugin(BaseAdminPlugin):
    aliexpress_left_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.aliexpress_left_flag)

    def block_left_navbar(self, context, nodes):
        from skuapp.table.t_sys_department_staff import t_sys_department_staff
        from aliapp.models import t_erp_aliexpress_shop_info
        request = self.request
        qs = t_product_enter_ed_aliexpress.objects.all()
        qs=qs.filter(MGProcess__in=[2,3,6])
        All_permissions = ['duanxiaodi', 'liucuixian']
        t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)
        if request.user.is_superuser or request.user.username in All_permissions:
            pass
        else:
            if t_sys_department_staff_objs.count() > 0:
                q_l = None
                cata_zh_objs = t_erp_aliexpress_shop_info.objects.filter(seller_zh=request.user.first_name).values('cata_zh').distinct()
                for cata_zh_obj in cata_zh_objs:
                    if not q_l:
                        q_l = Q(Aliexpress_PL__contains=cata_zh_obj['cata_zh'])
                    else:
                        q_l = q_l|Q(Aliexpress_PL__contains=cata_zh_obj['cata_zh'])
                if q_l:
                    qs = qs.filter(q_l)
            else:
                qs = qs.none()
        flagcloth = request.GET.get('classCloth', '')
        Cate1 = request.GET.get('cate1','')
        Cate2 = request.GET.get('cate2','')
        Cate3 = request.GET.get('cate3','')
        ContrabandAttribute = request.GET.get('ContrabandAttribute', '')
        Storehouse = request.GET.get('Storehouse','')
        LargeCategory = request.GET.get('LargeCategory','')
        MainSKU = request.GET.get('MainSKU','')
        MainSKU = MainSKU.split(',')
        if '' in MainSKU:
            MainSKU=''

        YNphoto = request.GET.get('YNphoto','') # 图片处理 0实拍 1制作 
        MGProcess = request.GET.get('MGProcess','')#图片状态 0待实拍 1待制作 2完成实拍 3完成制作 4错误
        
        DYStaffName = request.GET.get('DYStaffName','')#调研员
        DYSHStaffName = request.GET.get('DYSHStaffName','')#调研审核员
        XJStaffName = request.GET.get('XJStaffName','')#询价员
        KFStaffName = request.GET.get('KFStaffName','')#开发员
        MGStaffName = request.GET.get('MGStaffName','')#美工员 
        Buyer = request.GET.get('Buyer','')#采购员
        CreateStaffName = request.GET.get('CreateStaffName','')#创建人
        LRStaffName = request.GET.get('LRStaffName','')#录入员
        PlatformName = request.GET.get('PlatformName','')#反向链接平台
        SourceURL   =   request.GET.get('SourceURL','')#反向链接平台
        KFTimeStart = request.GET.get('KFTimeStart','')#开发时间
        KFTimeEnd = request.GET.get('KFTimeEnd','')
        
        JZLTimeStart = request.GET.get('JZLTimeStart','')#建资料时间
        JZLTimeEnd = request.GET.get('JZLTimeEnd','')

        MGTimeStart = request.GET.get('MGTimeStart','')#图片完成时间
        MGTimeEnd = request.GET.get('MGTimeEnd','')
        
        WeightStart = request.GET.get('WeightStart','')#克重
        WeightEnd = request.GET.get('WeightEnd','')

        keywords = request.GET.get('keywords', '')  # 关键词EN
        keywords2 = request.GET.get('keywords2', '')  # 关键词CH

        jZLStaffName = request.GET.get('jZLStaffName', '')  # 建资料员
        MainSKUPrefix = request.GET.get('MainSKUPrefix','') # 主SKU前缀搜索

        LRTimeStart = request.GET.get('LRTimeStart','') # 录入时间
        LRTimeEnd = request.GET.get('LRTimeEnd','') # 录入时间
        BJP_FLAG        = request.GET.get('BJP_FLAG','')
        Back_Aliexpress_PL = request.GET.get('Back_Aliexpress_PL', '').replace(',', '&') # 反向速卖通大类

        searchList = {'ContrabandAttribute__exact':ContrabandAttribute, 'Storehouse__exact':Storehouse,'MainSKU__in':MainSKU, 'LargeCategory__exact': LargeCategory,
                      'YNphoto__exact': YNphoto,'MGProcess__exact': MGProcess,'DYStaffName__exact': DYStaffName,'DYSHStaffName__exact': DYSHStaffName,
                      'XJStaffName__exact': XJStaffName,'KFStaffName__exact': KFStaffName,'MGStaffName__exact': MGStaffName,'Buyer__exact': Buyer,
                      'CreateStaffName__exact': CreateStaffName,'LRStaffName__exact': LRStaffName, 'JZLStaffName__exact':jZLStaffName,
                      'KFTime__gte': KFTimeStart, 'KFTime__lt': KFTimeEnd,'JZLTime__gte': JZLTimeStart, 'JZLTime__lt': JZLTimeEnd,
                      'MGTime__gte': MGTimeStart, 'MGTime__lt': MGTimeEnd,'Weight__gte': WeightStart, 'Weight__lt': WeightEnd,
                      'ClothingSystem1__exact':Cate1,'ClothingSystem2__exact': Cate2,'ClothingSystem3__exact':Cate3,
                      'PlatformName__exact':PlatformName, 'MainSKU__startswith':MainSKUPrefix,'BJP_FLAG':BJP_FLAG,
                      'LRTime__gte': LRTimeStart, 'LRTime__lt': LRTimeEnd,'SourceURL__icontains':SourceURL,'Back_Aliexpress_PL__icontains':Back_Aliexpress_PL,
                      }
        searchexclude = {}
        AI_FLAG = request.GET.get('AI_FLAG', '')
        if AI_FLAG == '1':
            searchList['AI_FLAG'] = '1'
        elif AI_FLAG == '0':
            searchexclude['AI_FLAG'] = '1'

        IP_FLAG = request.GET.get('IP_FLAG', '')
        if IP_FLAG == '1':
            searchList['IP_FLAG'] = '1'
        elif IP_FLAG == '0':
            searchexclude['IP_FLAG'] = '1'

        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    #if k == 'ShopName__exact':
                        #v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl).exclude(**searchexclude)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')      
        if keywords:
            qs = qs.filter(Q(Name__icontains=keywords) | Q(Keywords__icontains=keywords))
        if keywords2:
            qs = qs.filter(Q(Name2__icontains=keywords2) | Q(Keywords2__icontains=keywords2))

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']
        
        if flagcloth == '1':
            qs = qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            qs = qs.exclude(LargeCategory__in=catelist)

        publish_url = '/Project/admin/skuapp/t_product_enter_ed_aliexpress?'
        count_all = qs.count()
        count_0 = qs.filter(publish_count__exact=0).exclude(twobuOperation__exact=2).count()
        tt = datetime.datetime.today() - datetime.timedelta(days = 30)
        count_0_month = qs.filter(publish_count__exact=0,MGTime__gte=tt).count()
        count_1 = qs.filter(publish_count__exact=1).count()
        count_2 = qs.filter(publish_count__exact=2).count()
        count_3 = qs.filter(publish_count__exact=3).count()
        count_4 = qs.filter(publish_count__gte=4).count()
        count_5 = qs.filter(twobuOperation__exact=2).count()

        nowurl = self.request.get_full_path().replace('pub=0', '').replace('pub=1', '') \
            .replace('pub=2', '').replace('pub=3', '').replace('pub=4', '').replace('pub=5', '').replace('?&', '?').replace('&&', '&')

        if nowurl[-1:] in ['?', '&']:
            nowurl = nowurl[:-1]
        if nowurl.find('?') == -1:
            nowurl = nowurl + '?'
        else:
            nowurl = nowurl + '&'
        
        if count_0_month != 0:
            publish_url0 = nowurl + 'pub=0'
            publish_url1 = ''
            publish_url2 = ''
            publish_url3 = ''
            publish_url4 = ''
            publish_url5 = nowurl + 'pub=5'
        else:
            publish_url0 = nowurl + 'pub=0'
            publish_url1 = nowurl + 'pub=1'
            publish_url2 = nowurl + 'pub=2'
            publish_url3 = nowurl + 'pub=3'
            publish_url4 = nowurl + 'pub=4'
            publish_url5 = nowurl + 'pub=5'
        
        publish_count = self.request.GET.get('pub')
        if publish_count == '0':
            flag = '0'
        elif publish_count == '1':
            flag = '1'
        elif publish_count == '2':
            flag = '2'
        elif publish_count == '3':
            flag = '3'
        elif publish_count == '4':
            flag = '4'
        elif publish_count == '5':
            flag = '5'
        else:
            flag = 'info_all'

        menu_list = [{
            "name": u"全部刊登信息(%s)"%count_all,
            "code": "011",
            "icon": "icon-th",
            "parentCode": "",
            "selected": "",
            "to_url": nowurl,
            "flag": "info_all",
            "child": [
                {
                    "name": u"刊登0次产品(%s)"%count_0,
                    "code": "0111",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url0,
                    "flag": "0",
                    "child": []
                },
                {
                    "name": u"刊登1次产品(%s)"%count_1,
                    "code": "0112",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url1,
                    "flag": "1",
                    "child": []
                },
                {
                    "name": u"刊登2次产品(%s)"%count_2,
                    "code": "0113",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url2,
                    "flag": "2",
                    "child": []
                },
                {
                    "name": u"刊登3次产品(%s)"%count_3,
                    "code": "0114",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url3,
                    "flag": "3",
                    "child": []
                },
                {
                    "name": u"刊登3次以上产品(%s)"%count_4,
                    "code": "0115",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url4,
                    "flag": "4",
                    "child": []
                },
                {
                    "name": u"本部门弃用(%s)"%count_5,
                    "code": "0116",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url5,
                    "flag": "5",
                    "child": []
                },
            ]
        }]

        show_flag = 0
        for menu_obj in menu_list:
            if menu_obj['flag'] == flag:
                menu_obj['selected'] = 'selected'
                show_flag = 1
            for menu_c in menu_obj['child']:
                if menu_c['flag'] == flag:
                    menu_c['selected'] = 'selected'
                    show_flag = 1   

        if show_flag == 1:
            nodes.append(loader.render_to_string('site_left_menu_tree_Plugin.html', {'menu_list': json.dumps(menu_list)}, context_instance=RequestContext(self.request)))
