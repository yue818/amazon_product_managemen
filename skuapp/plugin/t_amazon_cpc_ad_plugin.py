# -*- coding: utf-8 -*-

from xadmin.views import BaseAdminPlugin
from django.template import loader
from brick.table.t_store_configuration_file import t_store_configuration_file
from django.db import connection
from skuapp.table.t_sys_param import t_sys_param
from brick.table.t_config_online_amazon import t_config_online_amazon
from brick.table.t_config_amazon_shop_status import t_config_amazon_shop_status

class t_amazon_cpc_ad_plugin(BaseAdminPlugin):
    amazon_cpc_ad = False

    def init_request(self, *args, **kwargs):
        return bool(self.amazon_cpc_ad)

    def block_search_cata_nav(self, context, nodes):
        current_shop = self.request.GET.get('ShopName')

        navigation = {}   # 类导航栏显示

        remark_all = ''
        search_hidden = ''
        search_hidden_id = 0
        if not current_shop:
            current_shop = '全部'
        elif current_shop:
            current_shop = current_shop[:8]
            # 查询当前店铺状态
            t_config_amazon_shop_status_obj = t_config_amazon_shop_status(connection)
            remark_all = t_config_amazon_shop_status_obj.get_shop_status(current_shop)


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

        def get_config_result(params):
            config_list = []
            for param in params:
                forms = self.request.GET.get(param['parameter'])
                configuration_Sorted = sorted(param['config'].items(), key=lambda asd: asd[0], reverse=False)
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
                config_list.append(
                    {'forms_id': forms_id, 'configuration': configuration, 'parameter': param['parameter'],
                     'desc': param['desc']})
            return config_list

        params = [{'parameter': 'status3333333333',
                   'config': {0: {'': '全部'}, 1: {'Active': 'Active'}, 2: {'Completed': 'Completed'}, },
                   'desc': '商品状态', },
                  ]
        config_list = get_config_result(params)

        t_store_configuration_file_obj = t_store_configuration_file(connection)
        resultdata = ''
        if self.request.user.is_superuser:
            resultdata = t_store_configuration_file_obj.find_shopnames()
        if not self.request.user.is_superuser:
            username = self.request.user.first_name
            resultdata = t_store_configuration_file_obj.find_shopname_by_name(username=username)

        sn_list = ['全部']
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
        synTypeDict = {0: {'all': '广告同步'}, }  # 配置同步类型

        nodes.append(loader.render_to_string('t_amazon_cpc_ad_plugin.html',
                                             {'ShopNames':sn_list,'Some_SNS':some_sn,'current_shop':current_shop,'search_hidden':search_hidden,
                                               'search_hidden_id':search_hidden_id,'searchSite_id':searchSite_id,'searchSite':searchSite,
                                              'Siteconfiguration':Siteconfiguration,'navigation':navigation,'synTypeDict':synTypeDict,
                                              }))
