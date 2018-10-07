# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: amazon_search_box_plugin.py
 @time: 2018/9/27 15:49
"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from urllib import unquote
from Project.settings import *
from collections import OrderedDict


class AmazonSearchBoxPlugin(BaseAdminPlugin):
    amazon_search_box_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.amazon_search_box_flag)

    def get_param(self, searchKey, searchParams, newUrl):
        searchParam = ''
        for each in searchParams:
            paramf = each.split("=")[0]
            if searchKey == paramf:
                uu = each + '&'
                newUrl = newUrl.replace(uu, '')
                searchParam = unquote(each.split('=')[1])
        paramList = {'newUrl': newUrl, 'searchParam': searchParam}
        return paramList

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]

        model_name_this = self.model._meta.model_name
        ShopNameData = ""
        SupplierData = ""
        cat_Dic = {}
        shopNData = ""
        shopNameOfficialData = ""
        Create_manData = ""

        config_path = STATIC_ROOT + 'search_box_plugin_config.txt'
        cfile = open(config_path)
        lines = cfile.readlines()
        inputs1 = []
        inputs_id1 = []
        inputs2 = []
        inputs_id2 = []

        {'id': '1', 'id_name': 'product_sku', 'descri': '商品SKU', 'urlname1': 'product_sku', 'defult_value1': '可用逗号隔开查询多个', 'value1': '', 'urlname2': '', 'defult_value2': '', 'value2': '',
         'selection': 0, 'isDate': '', 'startNum': 0, 'endNum': 1, 'inputs': '1', 'model_name': 't_amazon_product_order_pend_cost'}

        for line in lines:
            if line is None or line.strip() == '':
                continue
            if '{' not in line:
                continue
            search_dict = eval(line)  # 转换为字典  因为有{ }         [ ] ==> 列表    ( ) ==> 元组
            if search_dict['model_name'] == model_name_this:  # model_name等于访问的网址
                if search_dict['inputs'] == '1':
                    if '{' in search_dict['defult_value1']:
                        search_dict['defult_value1'] = eval(search_dict['defult_value1'])
                        search_dict['defult_value1'] = OrderedDict(sorted(search_dict['defult_value1'].items(), key=lambda item: item[0]))
                    inputs1.append(search_dict)
                    inputs_id1.append(search_dict['id'])
                else:
                    inputs2.append(search_dict)
                    inputs_id2.append(search_dict['id'])

        newUrl = sourceURL
        if "?" in sourceURL:
            newUrl += "&"
            condition = newUrl.split("?")[1]
            conditions = condition.split("&")
            count_params = []
            count_filters = []
            for condition_i in conditions:
                if condition_i is not None and condition_i.strip() != '':
                    count_filters.append(condition_i)
                    count_params.append(condition_i.split("=")[0])

            for input1 in inputs1:
                if input1['urlname1'] in count_params:
                    paramList1 = self.get_param(input1['urlname1'], count_filters, newUrl)
                    newUrl = paramList1['newUrl']
                    input1['value1'] = paramList1['searchParam']
            for input2 in inputs2:
                if input2['urlname1'] in count_params or input2['urlname2'] in count_params:
                    paramList1 = self.get_param(input2['urlname1'], count_filters, newUrl)
                    newUrl = paramList1['newUrl']
                    input2['value1'] = paramList1['searchParam']
                    if input2['urlname2'] is not None and input2['urlname2'].strip() != '':
                        paramList2 = self.get_param(input2['urlname2'], count_filters, newUrl)
                        newUrl = paramList2['newUrl']
                        input2['value2'] = paramList2['searchParam']
                        if input2['isDate'] == 1:
                            import datetime
                            endTime = paramList2['searchParam']
                            if endTime is not None and endTime.strip() != '':
                                date_time = datetime.datetime.strptime(endTime, '%Y-%m-%d')
                                date_time = date_time + datetime.timedelta(days=-1)
                                input2['value2'] = str(date_time).split(' ')[0]
        else:
            newUrl += "?"

        nodes.append(loader.render_to_string('search_box_plugin.html',
                                             {'newUrl': newUrl, 'inputs1': inputs1, 'inputs2': inputs2,
                                              'inputs_id1': inputs_id1, 'inputs_id2': inputs_id2, 'ShopNameData': ShopNameData, 'SupplierData': SupplierData, 'shopNData': shopNData,
                                              'Create_manData': Create_manData, 'model_name_this': model_name_this, 'cat_Dic': cat_Dic, 'shopNameOfficialData': shopNameOfficialData}))
