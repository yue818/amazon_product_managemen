# -*- coding: utf-8 -*-

import json
from xadmin.views import BaseAdminPlugin
from django.template import loader
from brick.table.t_store_configuration_file import t_store_configuration_file
from skuapp.table.t_store_configuration_file import t_store_configuration_file as store_config_table
from django.db import connection
from skuapp.table.t_sys_param import t_sys_param
from brick.table.t_config_online_amazon import t_config_online_amazon
from brick.table.t_config_amazon_shop_status import t_config_amazon_shop_status
from django.contrib.auth.models import User
from django.db.models import Q


class t_online_info_amazon_listing_plugin(BaseAdminPlugin):
    amazon_listing_plugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.amazon_listing_plugin)

    def block_search_cata_nav(self, context, nodes):
        current_shop = self.request.GET.get('ShopName')

        navigation = {}   # 类导航栏显示

        remark_all = ''
        search_hidden = ''
        search_hidden_id = 0
        if not current_shop:
            current_shop = ''
        elif current_shop:
            current_shop = current_shop[:8]
            # 查询当前店铺状态
            t_config_amazon_shop_status_obj = t_config_amazon_shop_status(connection)
            remark_all = t_config_amazon_shop_status_obj.get_shop_status(current_shop)

        if self.request.GET.get('shopname', '') != '':
            flag = self.request.GET.get('shopname', '')
        else:
            flag = ''
        if flag.find('AMZ-') == -1:
            flag = 'AMZ-' + flag.zfill(4)

        # 搜索类型配置
        searchType_config = {0: {'Title': '标题'}, 1: {'seller_sku': 'seller_sku'}, 2: {'asin1': 'asin1'},}
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

        # 通过配置表t_sys_param    配置站点
        if current_shop:
            t_config_online_amazon_obj = t_config_online_amazon(connection)
            sitesrc = t_config_online_amazon_obj.getSitebyShopName(current_shop)
            if sitesrc['code'] == 0:
                searchSite = self.request.GET.get('searchSite')
                searchSite_id = 0
                Site_conf = {}
                for site in sitesrc['data']:
                    if site[0]:
                        t_sys_param_objs  =  t_sys_param.objects.filter(TypeDesc='ChoiceSiteconfiguration').filter(V=site[0])
                        Site_conf[0] = {'ALL': '全部'}
                        for obj in t_sys_param_objs:
                            Site_conf[obj.Seq] = {obj.V: obj.VDesc}
                Siteconfiguration_Sorted = sorted(Site_conf.items(), key=lambda asd: asd[0], reverse=False)
                k = 0
                Siteconfiguration = {}
                for u in Siteconfiguration_Sorted:
                    Siteconfiguration[k] = u[1]
                    if searchSite == tuple(u[1])[0]:
                        searchSite_id = k
                        searchSite = u[1][tuple(u[1])[0]]  # 显示为中文
                    k += 1
                if not searchSite:
                    searchSite = '全部'
        elif not current_shop:
            searchSite = self.request.GET.get('searchSite')
            searchSite_id = 0
            Site_conf = {}
            t_sys_param_objs = t_sys_param.objects.filter(TypeDesc='ChoiceSiteconfiguration')
            for obj in t_sys_param_objs:
                # Site_conf[obj.Seq] = obj.VDesc
                Site_conf[obj.Seq] = {obj.V:obj.VDesc}
            Siteconfiguration_Sorted = sorted(Site_conf.items(), key=lambda asd: asd[0], reverse=False)
            k = 0
            Siteconfiguration = {}
            for u in Siteconfiguration_Sorted:
                Siteconfiguration[k] = u[1]
                if searchSite == tuple(u[1])[0]:
                    searchSite_id = k
                    searchSite = u[1][tuple(u[1])[0]] #显示为中文
                k += 1
            if not searchSite:
                searchSite = '全部'


        # 配置多属性
        selling_config = {0: {'ALL': '全部'}, 1: {'0': '单品'}, 2: {'1': '多属性'}}
        sellingforms = self.request.GET.get('sellingforms')
        sellingconfiguration_Sorted = sorted(selling_config.items(), key=lambda asd: asd[0], reverse=False)

        sellingconfiguration = {}
        setsellingforms_id = 0
        sellingform = ''
        s = 0
        for sell in sellingconfiguration_Sorted:
            sellingconfiguration[s] = sell[1]
            if sellingforms == tuple(sell[1])[0]:
                setsellingforms_id = s
                # sellingform = sell[1][tuple(sell[1])[0]]  # 显示为中文
            s += 1
        if not sellingforms:
            sellingform = 'ALL'

        priceLift = self.request.GET.get('priceLift')
        priceRight = self.request.GET.get('priceRight')
        quantityLeft = self.request.GET.get('quantityLeft')
        quantityRight = self.request.GET.get('quantityRight')
        brandId = self.request.GET.get('brandId')
        manufacturerId = self.request.GET.get('manufacturerId')

        shipType = self.request.GET.get('shipType')

        if not priceLift:
            priceLift = ''
        if not priceRight:
            priceRight = ''
        if not quantityLeft:
            quantityLeft = ''
        if not quantityRight:
            quantityRight = ''
        if not brandId:
            brandId = ''
        if not manufacturerId:
            manufacturerId = ''
        if not shipType:
            shipType = 'ALL'

        updatetime_str = self.request.GET.get('updatetime_str')
        updatetime_end = self.request.GET.get('updatetime_end')
        createtime_str = self.request.GET.get('createtime_str')
        createtime_end = self.request.GET.get('createtime_end')
        time_type = 0

        timeLift = ''
        timeRight = ''
        if updatetime_str or updatetime_end:
            time_type = 0
            timeLift = updatetime_str
            timeRight = updatetime_end
        if createtime_str or createtime_end:
            time_type = 1
            timeLift = createtime_str
            timeRight = createtime_end
        if not timeLift:
            timeLift = ''
        if not timeRight:
            timeRight = ''
        open_flag = ''
        if priceLift or priceRight or quantityLeft or quantityRight or brandId or manufacturerId or timeLift or timeRight or shipType != 'ALL':
            open_flag = '(详细)'

        t_store_configuration_file_obj = t_store_configuration_file(connection)
        resultdata = ''
        if self.request.user.is_superuser:
            resultdata = t_store_configuration_file_obj.find_shopnames()
        if not self.request.user.is_superuser:
            username = self.request.user.first_name
            resultdata = t_store_configuration_file_obj.find_shopname_by_name(username=username)

        sn_list = []
        if resultdata['code'] == 0:
            for data in resultdata['data']:
                if 'AMZ' in data[0]:
                    sn_list.append(data[0])
        some_sn = sn_list[:3]

        # 类导航栏显示
        # navigation = {}
        if current_shop:
            navigation['店铺'] = current_shop
        if searchSite:
            navigation['站点'] = searchSite
        if sellingforms:
            navigation['售卖形式'] = sellingforms
        if priceLift or priceRight:
            navigation['价格'] = priceLift+' ~ '+priceRight
        if quantityLeft or quantityRight:
            navigation['库存'] = quantityLeft+' ~ '+quantityRight
        if shipType:
            navigation['运输方式'] = shipType
        if brandId:
            navigation['品牌'] = brandId
        if manufacturerId:
            navigation['制造商'] = manufacturerId
        if (timeLift or timeRight) and time_type == 0:
            navigation['更新时间'] = timeLift+' ~ '+timeRight
        elif (timeLift or timeRight) and time_type == 1:
            navigation['创建时间'] = timeLift+' ~ '+timeRight

        createProductURL = '/Project/admin/skuapp/t_templet_amazon_collection_box/add/'  # 创建产品
        currentURL = '/Project/admin/skuapp/t_online_info_amazon_listing/'  #当前URL
        taskURL = '/t_online_info_amazon_listing_syn_shopname/'  #执行任务
        completeURL = '/t_online_info_amazon_listing_complete_shopname/'  #进度URL
        synTypeDict = {0:{'all':'全量同步'},1:{'synpro':'选中同步'} } # 配置同步类型
        platform_flg = 'AMZON'  # 平台
        pdURL = '/load_amazon_products/' # 上下架URL

        isHideSite =  ''
        # isHideSite =  'none' 不显示站点
        # searchSite_id = ''
        # searchSite = ''
        # Siteconfiguration = {'':{'':''}}

        buttonlist = []
        if self.request.user.is_superuser:
            objs = store_config_table.objects.filter(ShopName__startswith='AMZ-').values('ShopName')
        else:
            allobj = User.objects.filter(groups__id__in=[38])
            userID = []
            for each in allobj:
                userID.append(each.id)
            if (self.request.user.id in userID):
                objs = store_config_table.objects.filter(ShopName__startswith='AMZ-').values('ShopName')
            else:
                objs = store_config_table.objects.filter(
                    Q(Seller=context['user'].first_name) | Q(Published=context['user'].first_name) | Q(
                        Operators=context['user'].first_name)).values('ShopName')
        for obj in objs:
            buttonlist.append(obj['ShopName'])
        buttonlist.sort()

        activeflag = self.request.GET.get('_p_is_fba', '')

        nowurl = self.request.get_full_path().replace('_p_is_fba=0', '').replace('_p_is_fba=1', '').replace('?&', '?').replace('&&', '&')
        if nowurl[-1:] in ['?', '&']:
            nowurl = nowurl[:-1]
        if nowurl.find('?') == -1:
            nowurl = nowurl + '?'
        else:
            nowurl = nowurl + '&'

        nodes.append(
            loader.render_to_string(
                't_online_info_amazon_listing_plugin.html',
                {
                    'ShopNames':sn_list,'Some_SNS':some_sn,'current_shop':current_shop,'search_hidden':search_hidden,
                    'search_hidden_id':search_hidden_id,'searchSite_id':searchSite_id,'searchSite':searchSite,'setsellingforms_id':setsellingforms_id,
                    'sellingform':sellingform,'priceLift':priceLift,'priceRight':priceRight,'quantityLeft':quantityLeft,'quantityRight':quantityRight,
                    'brandId':brandId,'manufacturerId':manufacturerId, 'shipType':shipType, 'time_type':time_type, 'timeLift':timeLift, 'timeRight':timeRight,
                    'open_flag':open_flag, 'Siteconfiguration':Siteconfiguration,'remark_all':remark_all, 'navigation':navigation,
                    'Typeconfiguration':Typeconfiguration,'Sellingconfiguration':sellingconfiguration, 'createProductURL':createProductURL,'currentURL':currentURL,
                    'taskURL':taskURL,'completeURL':completeURL,'pdURL':pdURL,'synTypeDict':synTypeDict,'platform_flg':platform_flg,'isHideSite':isHideSite,
                    'objs': json.dumps(buttonlist),
                    'flag': flag,
                    'nowurl': nowurl,
                    'activeflag': activeflag
                }
            )
        )
