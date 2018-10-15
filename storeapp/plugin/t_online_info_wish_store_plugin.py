# -*- coding: utf-8 -*-

from xadmin.views import BaseAdminPlugin
from django.template import loader
from brick.table.t_store_configuration_file import t_store_configuration_file
from django.db import connection
from skuapp.table.t_sys_param import t_sys_param
from brick.table.t_config_online_amazon import t_config_online_amazon
# from brick.table.t_config_amazon_shop_status import t_config_amazon_shop_status
from brick.table.t_large_small_corresponding_cate import t_large_small_corresponding_cate
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import logging
import json
from brick.table.get_wish_product_order_updatetime import get_wish_product_order_updatetime
from django.db import connection
from skuapp.table.t_store_configuration_file import t_store_configuration_file

from django.contrib import messages
from django.db.models import Q
from django_redis import get_redis_connection
from brick.classredis.classshopname import classshopname


class t_online_info_wish_store_plugin(BaseAdminPlugin):
    wish_listing_plugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.wish_listing_plugin)

    def block_search_cata_nav(self, context, nodes):
        redis_coon = get_redis_connection(alias='product')

        if self.request.GET.get('shopname', '') != '':
            flag = self.request.GET.get('shopname', '')
        else:
            flag = ''
        if flag.find('Wish-') == -1:
            flag = 'Wish-' + flag.zfill(4)
        lastupdatetime = ''
        if flag != 'Wish-':
            get_wish_product_order_updatetime_obj = get_wish_product_order_updatetime(connection, flag)
            up_obj = get_wish_product_order_updatetime_obj.get_updatetime('Product')
            if up_obj:
                lastupdatetime = up_obj[1]  # 上次增量更新的时间

        classshopname_obj = classshopname(redis_cnxn=redis_coon)
        refreshstatus = classshopname_obj.get_api_status_by_shopname(flag)
        if refreshstatus is None:
            refreshstatus = ''

        synurl = ''
        if flag != 'Wish-0000' and refreshstatus == '':
            synurl = '/syndata_by_wish_api_shopname/?shopname=%s' % flag

        buttonlist = []
        if self.request.user.is_superuser:
            objs = t_store_configuration_file.objects.filter(ShopName__startswith='Wish-').values('ShopName_temp')
        else:
            allobj = User.objects.filter(groups__id__in=[38])
            userID = []
            for each in allobj:
                userID.append(each.id)
            if (self.request.user.id in userID):
                objs = t_store_configuration_file.objects.filter(ShopName__startswith='Wish-').values('ShopName_temp')
            else:
                objs = t_store_configuration_file.objects.filter(
                    Q(Seller=context['user'].first_name) | Q(Published=context['user'].first_name) | Q(
                        Operators=context['user'].first_name)).values('ShopName_temp')
        for obj in objs:
            buttonlist.append(obj['ShopName_temp'])
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
            current_shop = current_shop[:9]
        if current_shop:
            navigation['店铺'] = current_shop

        # 搜索类型配置
        searchType_config = {0: {'productID': '产品ID'}, 1: {'mainSKU': '主SKU'},2: {'MHmainSKU': '主SKU(模糊)'},
                             3: {'shopsku': '店铺SKU'},4: {'Title': 'Title'}, 5: {'Published': '刊登人'},
                             6: {'seller': '店长/销售员'},7: {'MainSKUClaim': '主SKU领取人'}}
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

        # params = [{'config':config, 'parameter':parameter, 'desc':desc},]
        def get_config_result(params):
            config_list = []
            for param in params:
                forms = self.request.GET.get(param['parameter'])
                configuration_Sorted =  sorted(param['config'].items(), key=lambda asd: asd[0], reverse=False)
                configuration = {}
                forms_id = 0
                form = ''
                gcr = 0
                for cfs in configuration_Sorted:
                    configuration[gcr] = cfs[1]
                    if forms == tuple(cfs[1])[0]:
                        forms_id = gcr
                        form = cfs[1][tuple(cfs[1])[0]]  # 显示为中文
                    gcr += 1
                if form:
                    navigation[param['desc']] = form
                config_list.append({'forms_id':forms_id,'configuration':configuration, 'parameter':param['parameter'],'desc':param['desc']})
            return config_list

        params = [{'parameter':'tortInfo', # 页面传值
                  'config':{0: {'': '全部'}, 1: {'WY': 'Wish仿品'}, 2: {'Y': '其他仿品'}, 3:{'N':'非仿品'}},
                  'desc':'侵权状态', },

                  {'parameter': 'dataSources',
                   'config': {0: {'': '全部'}, 1: {'UPLOAD': '铺货'}, 2: {'NORMAL': '非铺货'}, },
                   'desc': '数据来源', },

                  {'parameter': 'Estatus',
                   'config': {0: {'': '全部'}, 1: {'Enabled': '已启用'}, 2: {'Disabled': '已禁用'}, },
                   'desc': '启用状态', },

                  {'parameter': 'reviewState',
                   'config': {0: {'': '全部'}, 1: {'approved': '已批准'}, 2: {'pending': '待审核'}, 3: {'rejected': '被拒绝'}},
                   'desc': 'WISH状态', },
                   
                  {'parameter': 'Band',
                   'config': {0: {'': '全部'}, 1: {'1': '全部绑定'}, 2: {'2': '部分未绑'},3: {'3': '全部未绑'}, },
                   'desc': '是否绑定', },
                  

                  # {'parameter': 'ad',
                  #  'config': {0: {'': '全部'}, 1: {'Y': '是'}, 2: {'N': '否'}, },
                  #  'desc': '是否加广告', },

                  {'parameter': 'skustatus',
                   'config':{0: {'': '全部'}, 1: {'1': '正常'}, 2: {'2': '售完下架'},3: {'3': '临时下架'},4: {'4': '停售'}, },
                   'desc': '商品SKU状态', },

                  {'parameter': 'shopskustatus',
                   'config': {0: {'': '全部'}, 1: {'Enabled': '已启用'}, 2: {'Disabled': '已禁用'}, },
                   'desc': '店铺SKU状态', },
                  
                  
                  ]
        config_list = get_config_result(params)


        # 大类和小类
        large_list = []
        large_list.append({"":'全部'})
        large_hiden = ''
        largeClass = self.request.GET.get('largeClass')
        t_large_small_corresponding_obj = t_large_small_corresponding_cate(connection)
        large_corresponding_objs = t_large_small_corresponding_obj.getLargeClass()
        if large_corresponding_objs['code'] == 0:
            for lco in large_corresponding_objs['data']:
                largeConfig = {}
                largeConfig[lco[0]] = lco[1]
                large_list.append(largeConfig)
                if largeClass == lco[0]:
                    large_hiden = lco[0]
                    navigation['大类名称'] = lco[1]
        else:
            pass

        small_list = []
        small_list.append({"":'全部'})
        small_hiden = ''
        smallClass = self.request.GET.get('smallClass')
        small_corresponding_objs = t_large_small_corresponding_obj.getSmallClass()
        if small_corresponding_objs['code'] == 0:
            for c in small_corresponding_objs['data']:
                smallConfig = {}
                smallConfig[c[0]] = c[1]
                small_list.append(smallConfig)
                if smallClass == c[0]:
                    small_hiden = c[0]
                    navigation['小类名称'] = c[1]
        else:
            pass


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
        timeType_config = {0: {'online刷新时间':{'left': 'refreshTimeStart', 'right':'refreshTimeEnd'}},
                             1: {'上架日期':{'left': 'dateUploadedStart','right':'dateUploadedEnd'}},
                             # 2: {'营销时间':{'left':'market_timeStart','right':'market_timeStart'}},
                             3: {'平台更新日期': {'left': 'lastUpdatedStart', 'right': 'lastUpdatedEnd'}},
                             4: {'建资料时间':{'left':'JZLTimeStart','right':'JZLTimeEnd'}},
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

        nodes.append(loader.render_to_string('products_listing_base_template.html',
                                             {'objs': json.dumps(buttonlist), 'synurl': synurl, 'flag': flag,'lastupdatetime':lastupdatetime,'refreshstatus':refreshstatus,
                                              'current_shop':current_shop,'search_hidden':search_hidden,
                                              'search_hidden_id':search_hidden_id,                        
                                              'timeType_config':timeType_config, 'open_flag':open_flag,'remark_all':remark_all, 'navigation':navigation,
                                              'Typeconfiguration':Typeconfiguration,
                                              'synTypeDict':synTypeDict,'timeType_hiden':timeType_hiden,
                                              'orders7DaysStart':orders7DaysStart,'orders7DaysEnd':orders7DaysEnd,
                                              'OfSalesStart': OfSalesStart, 'OfSalesEnd': OfSalesEnd,
                                              'timeL':timeL, 'timeR':timeR,
                                              'large_hiden':large_hiden,'large_list':large_list,
                                              'small_hiden':small_hiden,'small_list':small_list,                                          
                                              'config_list':config_list,                                             
                                             }))
