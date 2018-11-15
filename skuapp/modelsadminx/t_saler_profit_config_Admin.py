# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_saler_profit_config_Admin.py
 @time: 2018-08-29

"""
from django.contrib import messages
from django.utils.safestring import mark_safe
from datetime import datetime as ddtime

class t_saler_profit_config_Admin(object):
    search_box_flag = True
    importfile_plugin =True

    list_display = ('Department','PlatformName','ShopName','SalerName','StatisticsMonth')

    actions = ['']

    def save_models(self,):
        pass

    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_saler_profit_config_Admin, self).get_list_queryset()
        '''
        Status = request.GET.get('Status', '')  # 采购状态
        Stocking_plan_number = request.GET.get('Stocking_plan_number', '')   #备货计划号
        Stock_plan_dateStart      = request.GET.get('Stock_plan_dateStart', '')     # 备货计划时间
        Stock_plan_dateEnd      = request.GET.get('Stock_plan_dateEnd', '')     # 备货计划时间
        Demand_people = request.GET.get('Demand_people', '')             # 计划需求人
        Product_nature = request.GET.get('Product_nature', '')            #产品性质
        ProductSKU = request.GET.get('ProductSKU', '')                     #商品sku
        ProductName = request.GET.get('ProductName', '')                    # 商品名称
        ProductWeightStart = request.GET.get('ProductWeightStart', '')
        ProductWeightEnd = request.GET.get('ProductWeightEnd', '')                #商品克重
        Supplier = request.GET.get('Supplier', '')                         # 供应商
        AccountNum = request.GET.get('AccountNum', '')                     # 帐号
        Destination_warehouse = request.GET.get('Destination_warehouse', '')# 目的地仓库
        level = request.GET.get('level', '')                                # 紧急程度
        Buyer = request.GET.get('Buyer', '')                                #采购人

        neworold = request.GET.get('neworold', '')  # 新品备货
        OplogTimeStart = request.GET.get('OplogTimeStart','')  #记录生成时间
        OplogTimeEnd =request.GET.get('OplogTimeEnd','') #记录生成时间
        AmazonFactory = request.GET.get('AmazonFactory', '')  # 是否亚马逊服装


        searchList = {
                        'Stocking_plan_number__exact':Stocking_plan_number,
                        'Stock_plan_date__gte':Stock_plan_dateStart,'Stock_plan_date__lt':Stock_plan_dateEnd,
                        'Demand_people__exact':Demand_people,'Product_nature__exact':Product_nature,
                        'ProductSKU__icontains': ProductSKU,'ProductName__exact':ProductName,
                        'ProductWeight__gte':ProductWeightStart,
                        'ProductWeight__lt':ProductWeightEnd,
                        'Supplier__exact':Supplier,
                        'AccountNum__exact':AccountNum,
					    'Destination_warehouse__exact': Destination_warehouse,
                        'level__exact':level,
                        'Buyer__exact':Buyer,
                        'Status__exact':Status,
                        'OplogTime__gte':OplogTimeStart,'OplogTime__lt':OplogTimeEnd,
                        'neworold__exact': neworold,'AmazonFactory__exact':AmazonFactory,
                      }
        '''
        searchList = {}
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')

        return qs

