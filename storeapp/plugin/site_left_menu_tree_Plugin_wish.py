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
 @file: site_left_menu_Plugin_wish.py
 @time: 2018/2/28 8:53
"""
from storeapp.models import t_online_info_wish_store
from wishpubapp.table.t_templet_wish_publish_result import t_templet_wish_publish_result
from wishpubapp.table.t_templet_wish_publish_recycle import t_templet_wish_publish_recycle
from wishpubapp.table.t_templet_wish_publish_draft import t_templet_wish_publish_draft
from wishpubapp.table.t_templet_wish_publish_draft_from_ebay import t_templet_wish_publish_draft_from_ebay
from storeapp.table.t_online_info_wish_low_inventory import t_online_info_wish_low_inventory
from wishpubapp.table.t_templet_wish_country_shipping import t_templet_wish_country_shipping
from storeapp.table.t_online_info_wish_fbw_api_low_inventory import t_online_info_wish_fbw_api_low_inventory as fbw_low_inventory


class site_left_menu_tree_Plugin_wish(BaseAdminPlugin):
    site_left_menu_tree_flag_wish = False

    def init_request(self, *args, **kwargs):
        return bool(self.site_left_menu_tree_flag_wish)

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
                if param.split('=')[0] not in ('status', 'ratingStart', 'ratingEnd', 'tortflag', 'riskgrade'):
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
            qs = t_online_info_wish_store.objects.filter(ShopName='Wish-' + shopname.split('-')[-1].zfill(4))
            vflag = 0
        else:
            qs = t_online_info_wish_store.objects.none()
            vflag = 1

        full_path = self.request.get_full_path().replace('EXPRESS=STANDARD', '').replace('EXPRESS=DE', '') \
            .replace('EXPRESS=GB', '').replace('EXPRESS=US', '').replace('?&', '?').replace('&&', '&')
        if full_path[-1:] == '&':
            full_path = full_path[:-1]

        params = None
        if full_path:
            params = full_path.split('?')[-1]

        userID = [each.id for each in User.objects.filter(groups__id__in=[38])]

        if (self.request.user.is_superuser) or (self.request.user.id in userID):
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

                if params == 'ratingStart=1&ratingEnd=3':
                    lNUM = self.request.result_count
                else:
                    lNUM = 0
                if not lNUM:
                    lNUM = t_online_info_wish_store.objects.all().filter(Rating__lt='3', Rating__gte='1',AdStatus='1', SName='0').count()  # 低评分

                if params == 'status=no_ban&tortflag=1&riskgrade=3':
                    NoTTNUM_BAN = self.request.result_count
                else:
                    NoTTNUM_BAN = t_online_info_wish_store.objects.filter(TortFlag__exact=1, Status__exact='Enabled', RiskGrade__in=[8,9,10,11,12,13,14,15]).count()  # 标题侵权

                if params == 'status=no_scope&tortflag=1&riskgrade=2':
                    NoTTNUM_SCOPE = self.request.result_count
                else:
                    NoTTNUM_SCOPE = t_online_info_wish_store.objects.filter(TortFlag__exact=1, Status__exact='Enabled', RiskGrade__in=[4,5,6,7,12,13,14,15]).count()  # 标题侵权

                if params == 'status=no_pot&tortflag=1&riskgrade=1':
                    NoTTNUM_POT = self.request.result_count
                else:
                    NoTTNUM_POT = t_online_info_wish_store.objects.filter(TortFlag__exact=1, Status__exact='Enabled', RiskGrade__in=[2,3,6,7,10,11,14,15]).count()  # 标题侵权

                if params == 'status=no_other&tortflag=1&riskgrade=0':
                    NoTTNUM_OTHER = self.request.result_count
                else:
                    NoTTNUM_OTHER = t_online_info_wish_store.objects.filter(TortFlag__exact=1, Status__exact='Enabled', RiskGrade__in=[1,3,5,7,9,11,13,15]).count()  # 标题侵权


                if params == 'status=yes_ban&tortflag=2&riskgrade=3':
                    YesTTNUM_BAN = self.request.result_count
                else:
                    YesTTNUM_BAN = t_online_info_wish_store.objects.filter(TortFlag__exact=2, Status__exact='Enabled', RiskGrade__in=[8,9,10,11,12,13,14,15]).count()  # 标题侵权

                if params == 'status=yes_scope&tortflag=2&riskgrade=2':
                    YesTTNUM_SCOPE = self.request.result_count
                else:
                    YesTTNUM_SCOPE = t_online_info_wish_store.objects.filter(TortFlag__exact=2, Status__exact='Enabled', RiskGrade__in=[4,5,6,7,12,13,14,15]).count()  # 标题侵权

                if params == 'status=yes_pot&tortflag=2&riskgrade=1':
                    YesTTNUM_POT = self.request.result_count
                else:
                    YesTTNUM_POT = t_online_info_wish_store.objects.filter(TortFlag__exact=2, Status__exact='Enabled', RiskGrade__in=[2,3,6,7,10,11,14,15]).count()  # 标题侵权

                if params == 'status=yes_other&tortflag=2&riskgrade=0':
                    YesTTNUM_OTHER = self.request.result_count
                else:
                    YesTTNUM_OTHER = t_online_info_wish_store.objects.filter(TortFlag__exact=2, Status__exact='Enabled', RiskGrade__in=[1,3,5,7,9,11,13,15]).count()  # 标题侵权


                ENUM = esNUM + eNUM  # 异常链接
            else:
                aNUM = qs.count()  # 全部商品
                oNUM = qs.filter(AdStatus='1', SName='0').count()  # 在线商品
                offNUM = qs.filter(AdStatus='0', SName='0').count() # 不在线商品
                nNUM = oNUM + offNUM  # 正常商品
                esNUM = qs.filter(SName='-1').count()  # 店铺状态异常
                eNUM  = qs.filter(AdStatus__in=['-1', '-2'], SName='0').count()  # 链接异常
                lNUM = qs.filter(Rating__lt='3', Rating__gte='1',AdStatus='1', SName='0').count()  # 低评分
                ENUM = esNUM + eNUM  # 异常链接

                NoTTNUM_BAN = qs.filter(TortFlag=1, Status__exact='Enabled', RiskGrade__in=[8,9,10,11,12,13,14,15]).count()  # 标题侵权
                NoTTNUM_SCOPE = qs.filter(TortFlag=1, Status__exact='Enabled', RiskGrade__in=[4,5,6,7,12,13,14,15]).count()  # 标题侵权
                NoTTNUM_POT = qs.filter(TortFlag=1, Status__exact='Enabled', RiskGrade__in=[2,3,6,7,10,11,14,15]).count()  # 标题侵权
                NoTTNUM_OTHER = qs.filter(TortFlag=1, Status__exact='Enabled', RiskGrade__in=[1,3,5,7,9,11,13,15]).count()  # 标题侵权

                YesTTNUM_BAN = qs.filter(TortFlag=2, Status__exact='Enabled',RiskGrade__in=[8, 9, 10, 11, 12, 13, 14, 15]).count()  # 标题侵权
                YesTTNUM_SCOPE = qs.filter(TortFlag=2, Status__exact='Enabled',RiskGrade__in=[4, 5, 6, 7, 12, 13, 14, 15]).count()  # 标题侵权
                YesTTNUM_POT = qs.filter(TortFlag=2, Status__exact='Enabled',RiskGrade__in=[2, 3, 6, 7, 10, 11, 14, 15]).count()  # 标题侵权
                YesTTNUM_OTHER = qs.filter(TortFlag=2, Status__exact='Enabled',RiskGrade__in=[1, 3, 5, 7, 9, 11, 13, 15]).count()  # 标题侵权
        else:
            shoplist = t_store_configuration_file.objects.filter(Q(Seller=self.request.user.first_name) | Q(Published=self.request.user.first_name) | Q(Operators=self.request.user.first_name)).values_list('ShopName_temp',flat=True)
            if shoplist:
                qs = t_online_info_wish_store.objects.filter(ShopName__in=shoplist)

                aNUM = qs.count() # 全部商品
                oNUM = qs.filter(AdStatus='1',SName='0').count()  # 在线商品
                offNUM = qs.filter(AdStatus='0',SName='0').count()  # 不在线商品
                nNUM = oNUM + offNUM  # 正常商品
                esNUM = qs.filter(SName='-1').count()  # 店铺状态异常
                eNUM = qs.filter(AdStatus__in=['-1', '-2'],SName='0').count()  # 链接异常
                ENUM = esNUM + eNUM  # 异常链接
                lNUM = qs.filter(Rating__lt='3', Rating__gte='1',AdStatus='1', SName='0').count()  # 低评分
                NoTTNUM_BAN = qs.filter(TortFlag=1, Status__exact='Enabled',RiskGrade__in=[8, 9, 10, 11, 12, 13, 14, 15]).count()  # 标题侵权
                NoTTNUM_SCOPE = qs.filter(TortFlag=1, Status__exact='Enabled',RiskGrade__in=[4, 5, 6, 7, 12, 13, 14, 15]).count()  # 标题侵权
                NoTTNUM_POT = qs.filter(TortFlag=1, Status__exact='Enabled',RiskGrade__in=[2, 3, 6, 7, 10, 11, 14, 15]).count()  # 标题侵权
                NoTTNUM_OTHER = qs.filter(TortFlag=1, Status__exact='Enabled',RiskGrade__in=[1, 3, 5, 7, 9, 11, 13, 15]).count()  # 标题侵权

                YesTTNUM_BAN = qs.filter(TortFlag=2, Status__exact='Enabled',RiskGrade__in=[8, 9, 10, 11, 12, 13, 14, 15]).count()  # 标题侵权
                YesTTNUM_SCOPE = qs.filter(TortFlag=2, Status__exact='Enabled',RiskGrade__in=[4, 5, 6, 7, 12, 13, 14, 15]).count()  # 标题侵权
                YesTTNUM_POT = qs.filter(TortFlag=2, Status__exact='Enabled',RiskGrade__in=[2, 3, 6, 7, 10, 11, 14, 15]).count()  # 标题侵权
                YesTTNUM_OTHER = qs.filter(TortFlag=2, Status__exact='Enabled',RiskGrade__in=[1, 3, 5, 7, 9, 11, 13, 15]).count()  # 标题侵权
            else:
                aNUM = 0  # 全部商品
                oNUM = 0  # 在线商品
                offNUM = 0  # 不在线商品
                nNUM = 0  # 正常商品
                esNUM = 0  # 店铺状态异常
                eNUM = 0  # 链接异常
                ENUM = 0  # 异常链接
                lNUM = 0 # 低评分产品
                NoTTNUM_BAN = 0
                NoTTNUM_SCOPE = 0
                NoTTNUM_POT = 0
                NoTTNUM_OTHER = 0

                YesTTNUM_BAN = 0
                YesTTNUM_SCOPE = 0
                YesTTNUM_POT = 0
                YesTTNUM_OTHER = 0

        # TTNUM = NoTTNUM + YesTTNUM

        dNUM = t_templet_wish_publish_draft.objects.all().count()  # 待刊登
        ebay_dNUM = t_templet_wish_publish_draft_from_ebay.objects.all().count()  # ebay待刊登

        rsobjs = t_templet_wish_publish_result.objects.all()

        rsNUM_ing = rsobjs.filter(Status='waiting').count()    # 正在刊登
        rssNUM = rsobjs.filter(Status='success').count()    #  刊登成功
        rseNUM = rsobjs.filter(Status='error').count()    # 刊登失败

        rsNUM = rsNUM_ing + rssNUM + rseNUM   # 刊登结果

        rcNUM = t_templet_wish_publish_recycle.objects.all().count()  #  回收站

        lowNUM = t_online_info_wish_low_inventory.objects.all().count()  #  低库存

        conNUM = t_templet_wish_country_shipping.objects.all().count()  # 运费模板配置

        DFBWNUM = fbw_low_inventory.objects.filter(cansalesdays__lte=15).count() # FBW 低于15库存
        GFBWTTNUM = fbw_low_inventory.objects.filter(cansalesdays__gt=15).count() # FBW 高于15库存

        nowurl_store = "/Project/admin/storeapp/t_online_info_wish_store/?"
        pub_draft = "/Project/admin/wishpubapp/t_templet_wish_publish_draft/?"
        pub_result = "/Project/admin/wishpubapp/t_templet_wish_publish_result/?"
        pub_recycle = "/Project/admin/wishpubapp/t_templet_wish_publish_recycle/?"
        low_inv = "/Project/admin/storeapp/t_online_info_wish_low_inventory/?"
        con_url = "/Project/admin/wishpubapp/t_templet_wish_country_shipping/?"
        ebay_pub_draft = "/Project/admin/wishpubapp/t_templet_wish_publish_draft_from_ebay/?"
        fbw_url = "/Project/admin/storeapp/t_online_info_wish_fbw_api_low_inventory/?"

        if self.model._meta.model_name == 't_online_info_wish_store':
            nowurl_store = self.url_path()

        elif self.model._meta.model_name == 't_templet_wish_publish_draft':
            pub_draft = self.url_path()

        elif self.model._meta.model_name == 't_templet_wish_publish_result':
            pub_result = self.url_path()

        elif self.model._meta.model_name == 't_templet_wish_publish_result':
            pub_recycle = self.url_path()

        elif self.model._meta.model_name == 't_online_info_wish_low_inventory':
            low_inv = self.url_path()

        elif self.model._meta.model_name == 't_templet_wish_country_shipping':
            con_url = self.url_path()

        elif self.model._meta.model_name == 't_templet_wish_publish_draft_from_ebay':
            ebay_pub_draft = self.url_path()

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
                    },
                    {
                        "name": u"低库存产品(%s)" % lowNUM,
                        "code": "03",
                        "icon": "icon-minus-sign",
                        "parentCode": "00",
                        "selected": "",
                        "to_url": low_inv + 'status=low_inv',
                        "flag": "low_inv",
                        "child": []
                    },
                    {
                        "name": u"低评分产品(在线)(%s)" % lNUM,
                        "code": "05",
                        "icon": "icon-minus-sign",
                        "parentCode": "00",
                        "selected": "",
                        "to_url": nowurl_store + 'status=online&ratingStart=1&ratingEnd=3',
                        "flag": "low_score",
                        "child": []
                    },
                    {
                        "name": u"刊登运费模板配置(%s)" % conNUM,
                        "code": "04",
                        "icon": "icon-minus-sign",
                        "parentCode": "00",
                        "selected": "",
                        "to_url": con_url + 'status=con_url',
                        "flag": "con_url",
                        "child": []
                    },
                    {
                        "name": u"在线链接标题侵权",
                        "code": "06",
                        "icon": "icon-minus-sign",
                        "parentCode": "00",
                        "selected": "",
                        "to_url": '',
                        "flag": "TitleTort",
                        "child": [{
                                "name": u"未处理绝对禁止(%s)" % NoTTNUM_BAN,
                                "code": "61",
                                "icon": "icon-minus-sign",
                                "parentCode": "06",
                                "selected": "",
                                "to_url": nowurl_store + 'status=no_ban&tortflag=1&riskgrade=3',
                                "flag": "no_ban",
                                "child": []
                            },
                            {
                                "name": u"未处理限定范围(%s)" % NoTTNUM_SCOPE,
                                "code": "62",
                                "icon": "icon-minus-sign",
                                "parentCode": "06",
                                "selected": "",
                                "to_url": nowurl_store + 'status=no_scope&tortflag=1&riskgrade=2',
                                "flag": "no_scope",
                                "child": []
                            },
                            {
                                "name": u"未处理潜在风险(%s)" % NoTTNUM_POT,
                                "code": "63",
                                "icon": "icon-minus-sign",
                                "parentCode": "06",
                                "selected": "",
                                "to_url": nowurl_store + 'status=no_pot&tortflag=1&riskgrade=1',
                                "flag": "no_pot",
                                "child": []
                            },
                            {
                                "name": u"未处理其他(%s)" % NoTTNUM_OTHER,
                                "code": "64",
                                "icon": "icon-minus-sign",
                                "parentCode": "06",
                                "selected": "",
                                "to_url": nowurl_store + 'status=no_other&tortflag=1&riskgrade=0',
                                "flag": "no_other",
                                "child": []
                            },
                            {
                                "name": u"已处理绝对禁止(%s)" % YesTTNUM_BAN,
                                "code": "65",
                                "icon": "icon-minus-sign",
                                "parentCode": "06",
                                "selected": "",
                                "to_url": nowurl_store + 'status=yes_ban&tortflag=2&riskgrade=3',
                                "flag": "yes_ban",
                                "child": []
                            },
                            {
                                "name": u"已处理限定范围(%s)" % YesTTNUM_SCOPE,
                                "code": "66",
                                "icon": "icon-minus-sign",
                                "parentCode": "06",
                                "selected": "",
                                "to_url": nowurl_store + 'status=yes_scope&tortflag=2&riskgrade=2',
                                "flag": "yes_scope",
                                "child": []
                            },
                            {
                                "name": u"已处理潜在风险(%s)" % YesTTNUM_POT,
                                "code": "67",
                                "icon": "icon-minus-sign",
                                "parentCode": "06",
                                "selected": "",
                                "to_url": nowurl_store + 'status=yes_pot&tortflag=2&riskgrade=1',
                                "flag": "yes_pot",
                                "child": []
                            },
                            {
                                "name": u"已处理其他(%s)" % YesTTNUM_OTHER,
                                "code": "68",
                                "icon": "icon-minus-sign",
                                "parentCode": "06",
                                "selected": "",
                                "to_url": nowurl_store + 'status=yes_other&tortflag=2&riskgrade=0',
                                "flag": "yes_other",
                                "child": []
                            },]
                    },
                    {
                        "name": u"FBW库存预警",
                        "code": "07",
                        "icon": "icon-minus-sign",
                        "parentCode": "00",
                        "selected": "",
                        "to_url": '',
                        "flag": "FBWKC",
                        "child": [{
                                "name": u"可售天数小于15(%s)" % DFBWNUM,
                                "code": "71",
                                "icon": "icon-minus-sign",
                                "parentCode": "07",
                                "selected": "",
                                "to_url": fbw_url + '_p_cansalesdays__lte=15&status=lte',
                                "flag": "lte",
                                "child": []
                            },
                            {
                                "name": u"可售天数大于15(%s)" % GFBWTTNUM,
                                "code": "71",
                                "icon": "icon-minus-sign",
                                "parentCode": "07",
                                "selected": "",
                                "to_url": fbw_url + '_p_cansalesdays__gt=15&status=gt',
                                "flag": "gt",
                                "child": []
                            },]
                    },
                    {
                        "name": u"产品刊登(公测版)",
                        "code": "02",
                        "icon": "icon-minus-sign",
                        "parentCode": "00",
                        "selected": "",
                        "to_url": "",
                        "flag": "all_pub",
                        "child": [
                            {
                                "name": u"eBay待刊登模板(%s)" % ebay_dNUM,
                                "code": "25",
                                "icon": "icon-minus-sign",
                                "parentCode": "02",
                                "selected": "",
                                "to_url": ebay_pub_draft + 'status=ebay_pub_draft',
                                "flag": "ebay_pub_draft",
                                "child": []
                            },
                            {
                                "name": u"草稿箱-待刊登(%s)" % dNUM,
                                "code": "21",
                                "icon": "icon-minus-sign",
                                "parentCode": "02",
                                "selected": "",
                                "to_url": pub_draft + 'status=pub_draft',
                                "flag": "pub_draft",
                                "child": []
                            },
                            {
                                "name": u"正在刊登(%s)" % rsNUM_ing,
                                "code": "22",
                                "icon": "icon-minus-sign",
                                "parentCode": "02",
                                "selected": "",
                                "to_url": pub_result + 'status=waiting',
                                "flag": "waiting",
                                "child": []
                            },
                            {
                                "name": u"刊登结果(%s)" % rsNUM,
                                "code": "23",
                                "icon": "icon-minus-sign",
                                "parentCode": "02",
                                "selected": "",
                                "to_url": "",
                                "flag": "",
                                "child": [
                                    {
                                        "name": u"刊登成功(%s)" % rssNUM,
                                        "icon": "",
                                        "code": "231",
                                        "parentCode": "23",
                                        "selected": "",
                                        "to_url": pub_result + 'status=success',
                                        "flag": 'success',
                                        "child": []
                                    },
                                    {
                                        "name": u"刊登失败(%s)" % rseNUM,
                                        "icon": "",
                                        "code": "232",
                                        "parentCode": "23",
                                        "selected": "",
                                        "to_url": pub_result + 'status=error',
                                        "flag": 'error',
                                        "child": []
                                    }
                                ]
                            },
                            {
                                "name": u"回收站(%s)" % rcNUM,
                                "code": "24",
                                "icon": "icon-minus-sign",
                                "parentCode": "02",
                                "selected": "",
                                "to_url": pub_recycle + 'status=pub_recycle',
                                "flag": "pub_recycle",
                                "child": []
                            },
                        ]
                    },
                ]
            },
        ]

        flag = self.request.GET.get('status')
        score1 = self.request.GET.get('ratingStart','')
        score2 = self.request.GET.get('ratingEnd','')
        if flag == 'online' and score1 == '1' and score2 == '3':
            flag = 'low_score'

        menu_list, show_flag = self.show_select_flag(menu_list, flag)

        nodes.append(loader.render_to_string('site_left_menu_tree_Plugin.html',{'menu_list': json.dumps(menu_list)},context_instance=RequestContext(self.request)))
