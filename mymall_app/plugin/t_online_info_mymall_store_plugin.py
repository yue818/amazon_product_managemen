# -*- coding: utf-8 -*-

from brick.table.t_store_configuration_file import t_store_configuration_file
from brick.joom.Joom_Get_Products_Server import get_joom_product_order_updatetime
from brick.classredis.classshopname import classshopname
from skuapp.table.t_sys_param import t_sys_param
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from joom_app.table.t_online_info_joom import t_online_info_joom

from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.db import connection
from django.template import loader
from django.template import RequestContext
from django.db import connection
from django.contrib import messages
from django.db.models import Q
from django_redis import get_redis_connection
from dateutil import tz

import logging
import json
import datetime


class t_online_info_mymall_store_plugin(BaseAdminPlugin):
    mymall_listing_plugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.mymall_listing_plugin)

    def block_search_cata_nav(self, context, nodes):
        redis_coon = get_redis_connection(alias='product')

        if self.request.GET.get('shopname', '') != '':
            flag = self.request.GET.get('shopname', '')
        else:
            flag = ''
        if flag.find('Mall-') == -1:
            flag = ''
        lastupdatetime = ''
        # if flag != 'Mall-':
        #     get_joom_product_order_updatetime_obj = get_joom_product_order_updatetime(connection, flag)
        #     up_obj = get_joom_product_order_updatetime_obj.get_updatetime('Product')
        #     if up_obj:
        #         lastupdatetime = up_obj[1]  # 上次增量更新的时间
        #         utc = datetime.datetime.strptime(lastupdatetime, '%Y-%m-%dT%H:%M:%S')
        #         from_zone = tz.gettz('UTC')
        #         # from_zone = tz.tzutc()
        #         to_zone = tz.gettz('Asia/Shanghai')
        #         # to_zone = tz.tzlocal()
        #         utc = utc.replace(tzinfo=from_zone)
        #         central = utc.astimezone(to_zone)
        #         lastupdatetime = central.strftime('%Y-%m-%d %H:%M:%S')

        classshopname_obj = classshopname(redis_cnxn=redis_coon)
        refreshstatus = classshopname_obj.get_api_status_by_shopname(flag)
        if refreshstatus is None:
            refreshstatus = ''

        synurl = ''
        # if flag and flag != 'Mall-0000' and refreshstatus == '':
        #     synurl = '/syndata_by_joom_api_shopname/?shopname=%s' % flag

        buttonlist = []
        if self.request.user.is_superuser or (23, u'组长') in self.request.user.groups.values_list():
            objs = t_store_configuration_file.objects.filter(ShopName__startswith='Mall-').values('ShopName')
        else:
            objs = t_store_configuration_file.objects.filter(
                Q(Seller=context['user'].first_name) | Q(Published=context['user'].first_name) | Q(
                    Operators=context['user'].first_name)).values('ShopName')
        for obj in objs:
            buttonlist.append(obj['ShopName'])
        buttonlist.sort()
        # -----------------------------------------------------------------

        current_shop = self.request.GET.get('shopname')
        open_flag = ''

        navigation = {}   # 类导航栏显示

        remark_all = ''
        search_hidden = ''
        search_hidden_id = 0
        if not current_shop:
            current_shop = ''
        elif current_shop:
            current_shop = current_shop
        if current_shop:
            navigation['店铺'] = current_shop

        # 搜索类型配置
        searchType_config = {0:{'productID':'产品ID'},1: {'mainSKU': '主SKU'},2: {'shopsku': '店铺SKU'},
                             3:{'Title':'Title'}, 4: {'Published': '刊登人'},5: {'seller': '店长/销售员'},}
        searchType_config_Sorted = sorted(searchType_config.items(), key=lambda asd: asd[0], reverse=False)
        Typeconfiguration = {}
        t = 0
        for type in searchType_config_Sorted:
            Typeconfiguration[t] = type[1]
            searchType = self.request.GET.get(str(tuple(type[1])[0]))
            if searchType:
                # str(tuple(type[1])[0]) # 具体搜索类型
                search_hidden = searchType  #值
                search_hidden_id = t
                navigation[str(type[1][tuple(type[1])[0]])] = search_hidden
            t += 1

        # 侵权状态
        tortInfo_config = {0: {'': '全部'}, 1: {'WY': 'Joom仿品'}, 2: {'Y': '其他仿品'}, 3:{'N':'非仿品'}}
        tortInfoforms = self.request.GET.get('tortInfo')
        tortInfoconfiguration_Sorted = sorted(tortInfo_config.items(), key=lambda asd: asd[0], reverse=False)

        tortInfoconfiguration = {}
        tortInfoforms_id = 0
        tortInfoform = ''
        s = 0
        for tif in tortInfoconfiguration_Sorted:
            tortInfoconfiguration[s] = tif[1]
            if tortInfoforms == tuple(tif[1])[0]:
                tortInfoforms_id = s
                tortInfoform = tif[1][tuple(tif[1])[0]]  # 显示为中文
            s += 1
        if tortInfoforms:
            navigation['侵权状态'] = tortInfoform

        #数据来源
        dataSources_config = {0: {'': '全部'}, 1: {'UPLOAD': '铺货'}, 2: {'NORMAL': '非普货'}, }
        dataSourcesforms = self.request.GET.get('dataSources')
        dataSourcesconfiguration_Sorted = sorted(dataSources_config.items(), key=lambda asd: asd[0], reverse=False)

        dataSourcesconfiguration = {}
        dataSourcesforms_id = 0
        dataSourcesform = ''
        d = 0
        for dsf in dataSourcesconfiguration_Sorted:
            dataSourcesconfiguration[d] = dsf[1]
            if dataSourcesforms == tuple(dsf[1])[0]:
                dataSourcesforms_id = d
                tortInfoform = dsf[1][tuple(dsf[1])[0]]  # 显示为中文
            d += 1
        if dataSourcesforms:
            navigation['数据来源'] = dataSourcesform

        # 启用状态
        Estatus_config = {0: {'': '全部'}, 1: {'True': '已启用'}, 2: {'False': '已禁用'}, }
        Estatusforms = self.request.GET.get('Estatus')
        Estatusconfiguration_Sorted = sorted(Estatus_config.items(), key=lambda asd: asd[0], reverse=False)

        Estatusconfiguration = {}
        Estatusforms_id = 0
        Estatusform = ''
        e = 0
        for ecs in Estatusconfiguration_Sorted:
            Estatusconfiguration[e] = ecs[1]
            if Estatusforms == tuple(ecs[1])[0]:
                Estatusforms_id = e
                Estatusform = ecs[1][tuple(ecs[1])[0]]  # 显示为中文
            e += 1
        if Estatusforms:
            navigation['启用状态'] = Estatusform

        #配置状态
        reviewState_config = {0: {'': '全部'},1: {'approved': '已批准'}, 2: {'pending': '待审核'}, 3: {'rejected': '被拒绝'}}
        reviewStateforms = self.request.GET.get('reviewState')
        reviewStateconfiguration_Sorted = sorted(reviewState_config.items(), key=lambda asd: asd[0], reverse=False)
        reviewStateconfiguration = {}
        reviewStateforms_id = 0
        reviewStateform = ''
        r = 0
        for rscf in reviewStateconfiguration_Sorted:
            reviewStateconfiguration[r] = rscf[1]
            if reviewStateforms == tuple(rscf[1])[0]:
                reviewStateforms_id = r
                reviewStateform = rscf[1][tuple(rscf[1])[0]]  # 显示为中文
            r += 1
        if reviewStateforms:
            navigation['JOOM状态'] = reviewStateform


        orders7DaysStart = self.request.GET.get('orders7DaysStart')
        orders7DaysEnd = self.request.GET.get('orders7DaysEnd')
        OfSalesStart = self.request.GET.get('OfSalesStart')
        OfSalesEnd = self.request.GET.get('OfSalesEnd')

        if not orders7DaysStart:
            orders7DaysStart = ''
        if not orders7DaysEnd:
            orders7DaysEnd = ''
        if not OfSalesStart:
            OfSalesStart = ''
        if not OfSalesEnd:
            OfSalesEnd = ''

        # 类导航栏显示
        # navigation = {}
        if orders7DaysStart or orders7DaysEnd:
            navigation['7天order数'] = orders7DaysStart+' ~ '+orders7DaysEnd
        if OfSalesStart or OfSalesEnd:
            navigation['总销量'] = OfSalesStart+' ~ '+OfSalesEnd


        synTypeDict = {0:{'all':'全量同步'},1:{'increment':'增量同步'},2:{'synpro':'选中同步'} } # 配置同步类型

        # 时间框
        timeType_hiden = ''
        timeType_config = {
            0: {'online刷新时间':{'left': 'refreshTimeStart', 'right':'refreshTimeEnd'}},
            1: {'上架日期':{'left': 'dateUploadedStart','right':'dateUploadedEnd'}},
            # 2: {'营销时间':{'left':'market_timeStart','right':'market_timeStart'}},
            3: {'平台更新日期': {'left': 'lastUpdatedStart', 'right': 'lastUpdatedEnd'}},
        }
        timeType_config_Sorted = sorted(timeType_config.items(), key=lambda asd: asd[0], reverse=False)
        timeL = ''
        timeR = ''
        for tcs in timeType_config_Sorted:
            timeLeft = self.request.GET.get(str(tcs[1][tuple(tcs[1])[0]]['left']))
            timeRight =  self.request.GET.get(str(tcs[1][tuple(tcs[1])[0]]['right']))
            if timeLeft and timeRight:
                navigation[str(tuple(tcs[1])[0])] = timeLeft+' ~ '+timeRight
                timeType_hiden = str(tcs[1][tuple(tcs[1])[0]]['left'])+'&'+str(tcs[1][tuple(tcs[1])[0]]['right'])
                open_flag = '(详细)'
                timeL = timeLeft
                timeR = timeRight
            elif timeLeft and not timeRight:
                navigation[str(tuple(tcs[1])[0])] = timeLeft+' ~ '
                timeType_hiden = str(tcs[1][tuple(tcs[1])[0]]['left']) + '&' + str(tcs[1][tuple(tcs[1])[0]]['right'])
                open_flag = '(详细)'
                timeL = timeLeft
                timeR = timeRight
            elif not timeLeft and timeRight:
                navigation[str(tuple(tcs[1])[0])] = ' ~ '+timeRight
                timeType_hiden = str(tcs[1][tuple(tcs[1])[0]]['left']) + '&' + str(tcs[1][tuple(tcs[1])[0]]['right'])
                open_flag = '(详细)'
                timeL = timeLeft
                timeR = timeRight

        if orders7DaysStart or orders7DaysEnd or OfSalesStart or OfSalesEnd:
            open_flag = '(详细)'

        # MALL CUT PRICE
        cutprice_config = {
            0: {'': '全部'},
            1: {'not_cut_price': '未降价'},
            2: {'cut_price_ing': '降价中'},
            3: {'cut_price_falied': '降价失败'},
            4: {'cut_price_orders': '降价中已产生订单'},
            5: {'recover_price': '降价恢复成功'},
            6: {'recover_price_falied': '降价恢复失败'},
        }
        cutpriceforms = self.request.GET.get('cutprice')
        cutpriceconfiguration_Sorted = sorted(cutprice_config.items(), key=lambda asd: asd[0], reverse=False)

        cutpriceconfiguration = {}
        cutpriceforms_id = 0
        cutpriceform = ''
        e = 0
        for ecs in cutpriceconfiguration_Sorted:
            cutpriceconfiguration[e] = ecs[1]
            if cutpriceforms == tuple(ecs[1])[0]:
                cutpriceforms_id = e
                cutpriceform = ecs[1][tuple(ecs[1])[0]]  # 显示为中文
            e += 1
        if cutpriceforms:
            navigation['JOOM降价'] = cutpriceform

        status = self.request.GET.get('status', '')

        current_url = '/Project/admin/mymall_app/t_mymall_online_info/'
        if self.model._meta.model_name == 't_mymall_template_publish':
            current_url = '/Project/admin/mymall_app/t_mymall_template_publish/'

        nodes.append(
            loader.render_to_string(
                'mymall_products_listing_base_template.html',
                {
                    'objs': json.dumps(buttonlist), 'synurl': synurl, 'flag': flag,'lastupdatetime':lastupdatetime,'refreshstatus':refreshstatus,
                    'current_shop':current_shop,'search_hidden':search_hidden,
                    'search_hidden_id':search_hidden_id,
                    'tortInfoform':tortInfoform,'tortInfoforms_id':tortInfoforms_id,'tortInfoconfiguration':tortInfoconfiguration,
                    'dataSourcesform': dataSourcesform, 'dataSourcesforms_id': dataSourcesforms_id,'dataSourcesconfiguration': dataSourcesconfiguration,
                    'Estatusform': Estatusform, 'Estatusforms_id': Estatusforms_id, 'Estatusconfiguration': Estatusconfiguration,
                    'reviewStateform': reviewStateform, 'reviewStateforms_id': reviewStateforms_id, 'reviewStateconfiguration': reviewStateconfiguration,
                    'cutpriceform': cutpriceform, 'cutpriceforms_id': cutpriceforms_id, 'cutpriceconfiguration': cutpriceconfiguration,
                    'timeType_config':timeType_config, 'open_flag':open_flag,'remark_all':remark_all, 'navigation':navigation,
                    'Typeconfiguration':Typeconfiguration,
                    'synTypeDict':synTypeDict,'timeType_hiden':timeType_hiden,
                    'orders7DaysStart':orders7DaysStart,'orders7DaysEnd':orders7DaysEnd,
                    'OfSalesStart': OfSalesStart, 'OfSalesEnd': OfSalesEnd,
                    'timeL':timeL, 'timeR':timeR, 'status': status, 'current_url': current_url,
                }
            )
        )
