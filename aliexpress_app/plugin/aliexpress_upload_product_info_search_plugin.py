#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import datetime
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.db import connection
from django.db.models import Q
from django_redis import get_redis_connection
from dateutil import tz

from brick.joom.Joom_Get_Products_Server import get_joom_product_order_updatetime
from brick.classredis.classshopname import classshopname
from skuapp.table.t_store_configuration_file import t_store_configuration_file


class aliexpress_upload_product_info_search_plugin(BaseAdminPlugin):
    aliexpress_upload_product_info_plugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.aliexpress_upload_product_info_plugin)

    def block_search_cata_nav(self, context, nodes):
        redis_coon = get_redis_connection(alias='product')

        if self.request.GET.get('shopname', '') != '':
            flag = self.request.GET.get('shopname', '')
        else:
            flag = ''
        if flag.find('Ali-') == -1:
            flag = ''
        lastupdatetime = ''
        if flag != 'Ali-':
            get_joom_product_order_updatetime_obj = get_joom_product_order_updatetime(connection, flag)
            up_obj = get_joom_product_order_updatetime_obj.get_updatetime('Product')
            if up_obj:
                lastupdatetime = up_obj[1]  # 上次增量更新的时间
                utc = datetime.datetime.strptime(lastupdatetime, '%Y-%m-%dT%H:%M:%S')
                from_zone = tz.gettz('UTC')
                # from_zone = tz.tzutc()
                to_zone = tz.gettz('Asia/Shanghai')
                # to_zone = tz.tzlocal()
                utc = utc.replace(tzinfo=from_zone)
                central = utc.astimezone(to_zone)
                lastupdatetime = central.strftime('%Y-%m-%d %H:%M:%S')

        classshopname_obj = classshopname(redis_cnxn=redis_coon)
        refreshstatus = classshopname_obj.get_api_status_by_shopname(flag)
        if refreshstatus is None:
            refreshstatus = ''

        synurl = ''
        if flag and flag != 'Ali-0000' and refreshstatus == '':
            synurl = '/syndata_by_joom_api_shopname/?shopname=%s' % flag

        buttonlist = []
        if self.request.user.is_superuser or (23, u'组长') in self.request.user.groups.values_list():
            objs = t_store_configuration_file.objects.filter(ShopName__startswith='Ali-').values('ShopName')
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

        # 是否导入
        import_flag = {0: {'': '全部'}, 1: {'True': '已导入'}, 2: {'False': '未导入'}, }
        importFlagforms = self.request.GET.get('importFlag')
        importFlag_Sorted = sorted(import_flag.items(), key=lambda asd: asd[0], reverse=False)

        importFlagconfiguration = {}
        importFlagforms_id = 0
        importFlagform = ''
        d = 0
        for dsf in importFlag_Sorted:
            importFlagconfiguration[d] = dsf[1]
            if importFlagforms == tuple(dsf[1])[0]:
                importFlagforms_id = d
                importFlagform = dsf[1][tuple(dsf[1])[0]]  # 显示为中文
            d += 1
        if importFlagforms:
            navigation['数据来源'] = importFlagform

        # 搜索类型配置
        searchType_config = {
            0: {'uploadPerson': '上传人'},
            1: {'importPerson': '导入人'}
        }
        searchType_config_Sorted = sorted(searchType_config.items(), key=lambda asd: asd[0], reverse=False)
        Typeconfiguration = {}
        t = 0
        for type in searchType_config_Sorted:
            Typeconfiguration[t] = type[1]
            searchType = self.request.GET.get(str(tuple(type[1])[0]))
            if searchType:
                # str(tuple(type[1])[0]) # 具体搜索类型
                search_hidden = searchType  # 值
                search_hidden_id = t
                navigation[str(type[1][tuple(type[1])[0]])] = search_hidden
            t += 1

        uploadTimeStart = self.request.GET.get('uploadTimeStart')
        uploadTimeEnd = self.request.GET.get('uploadTimeEnd')
        importTimeStart = self.request.GET.get('importTimeStart')
        importTimeEnd = self.request.GET.get('importTimeEnd')

        if not uploadTimeStart:
            uploadTimeStart = ''
        if not uploadTimeEnd:
            uploadTimeEnd = ''
        if not importTimeStart:
            importTimeStart = ''
        if not importTimeEnd:
            importTimeEnd = ''

        # 类导航栏显示
        # navigation = {}
        if uploadTimeStart or uploadTimeEnd:
            navigation['上传时间'] = uploadTimeStart + ' ~ ' + uploadTimeEnd
        if importTimeStart or importTimeEnd:
            navigation['导入时间'] = importTimeStart + ' ~ ' + importTimeEnd

        synTypeDict = {
            0: {'all': '全量同步'},
            1: {'increment': '增量同步'},
            2: {'synpro': '选中同步'}
        }  # 配置同步类型

        # 时间框
        timeType_hiden = ''
        timeType_config = {
            0: {'上传时间': {'left': 'uploadTimeStart', 'right': 'uploadTimeEnd'}},
            1: {'导入日期': {'left': 'importTimeStart', 'right': 'importTimeEnd'}},
        }
        timeType_config_Sorted = sorted(timeType_config.items(), key=lambda asd: asd[0], reverse=False)
        timeL = ''
        timeR = ''
        for tcs in timeType_config_Sorted:
            timeLeft = self.request.GET.get(str(tcs[1][tuple(tcs[1])[0]]['left']))
            timeRight = self.request.GET.get(str(tcs[1][tuple(tcs[1])[0]]['right']))
            if timeLeft and timeRight:
                navigation[str(tuple(tcs[1])[0])] = timeLeft + ' ~ ' + timeRight
                timeType_hiden = str(tcs[1][tuple(tcs[1])[0]]['left']) + '&' + str(tcs[1][tuple(tcs[1])[0]]['right'])
                open_flag = '(详细)'
                timeL = timeLeft
                timeR = timeRight
            elif timeLeft and not timeRight:
                navigation[str(tuple(tcs[1])[0])] = timeLeft + ' ~ '
                timeType_hiden = str(tcs[1][tuple(tcs[1])[0]]['left']) + '&' + str(tcs[1][tuple(tcs[1])[0]]['right'])
                open_flag = '(详细)'
                timeL = timeLeft
                timeR = timeRight
            elif not timeLeft and timeRight:
                navigation[str(tuple(tcs[1])[0])] = ' ~ ' + timeRight
                timeType_hiden = str(tcs[1][tuple(tcs[1])[0]]['left']) + '&' + str(tcs[1][tuple(tcs[1])[0]]['right'])
                open_flag = '(详细)'
                timeL = timeLeft
                timeR = timeRight

        if uploadTimeStart or uploadTimeEnd or importTimeStart or importTimeEnd:
            open_flag = '(详细)'

        nodes.append(
            loader.render_to_string(
                'aliexpress_upload_product_info_search_plugin_template.html',
                {
                    'objs': json.dumps(buttonlist),
                    'synurl': synurl, 'flag': flag, 'lastupdatetime': lastupdatetime, 'refreshstatus': refreshstatus,
                    'importFlagform': importFlagform, 'importFlagforms_id': importFlagforms_id, 'importFlagconfiguration': importFlagconfiguration,
                    'current_shop': current_shop, 'search_hidden': search_hidden,
                    'search_hidden_id': search_hidden_id,
                    'timeType_config': timeType_config, 'open_flag': open_flag, 'remark_all': remark_all, 'navigation': navigation,
                    'Typeconfiguration': Typeconfiguration,
                    'synTypeDict': synTypeDict, 'timeType_hiden': timeType_hiden,
                    'uploadTimeStart': uploadTimeStart, 'uploadTimeEnd': uploadTimeEnd,
                    'importTimeStart': importTimeStart, 'importTimeEnd': importTimeEnd,
                    'timeL': timeL, 'timeR': timeR,
                }
            )
        )
