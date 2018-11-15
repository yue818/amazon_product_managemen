# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fba_all_Admin.py
 @time: 2018-08-20

"""
from xadmin.layout import Fieldset, Row
import datetime as tmpDate,random
from pyapp.models import b_goods as py_b_goods,B_Supplier as py_b_Supplier
from django.contrib import messages
from django.utils.safestring import mark_safe
from datetime import datetime as ddtime
from skuapp.table.public import *

class t_stocking_demand_fba_all_Admin(object):
    search_box_flag = True
    importfile_plugin = False
    fba_tree_menu_flag = True
    hide_page_action = True
    def show_ProductImage(self,obj) :
        from Project.settings import BmpUrl
        # 获取图片的url
        picture_url = obj.ProductImage  # 获取图片的url
        sku = obj.ProductSKU  # 获取商品SKU
        if not picture_url:
            picture_url = BmpUrl + sku + '.jpg'

        rt = """<img src="%s"  width="120" height="120"  title="%s" onerror="this.title=''" />  """ % (picture_url, picture_url)
        return mark_safe(rt)
    show_ProductImage.short_description = mark_safe('<p align="center" style="width:120px;color:#428bca;">商品图片</p>')

    def show_Status(self, obj):
        try:
            rt = ""
            strStatus = ""
            for status in getChoices(ChoiceFBAPlanStatus):
                if status[0] == obj.Status:
                    strStatus = status[1]
                    break
            rt = strStatus
        except Exception, ex:
            messages.info(self.request,"采购状态加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_Status.short_description = mark_safe('<p align="center" style="width:120px;color:#428bca;">采购状态</p>')

    def show_opInfo(self, obj):
        try:
            rt = u'<table border="1"><tr><th>操作员</th><th>告警信息</th><th>操作时间</th></tr>'
            if obj.Status == 'giveup':
                diffDate1 = (obj.giveupDate - obj.Stock_plan_date).days if (obj.Stock_plan_date is not None and obj.giveupDate is not None) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>'%(obj.Demand_people,diffDate1,obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                rt = rt + u'<tr style=""><th>废弃:%s</th><th> </th><th>%s</th></tr>' % (obj.giveupMan, obj.giveupDate)
            elif obj.Status == 'notgenpurchase':
                diffDate1 = (ddtime.now() - obj.Stock_plan_date).days if obj.Stock_plan_date is not None else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
            elif obj.Status == 'notpurchase' or obj.Status == 'purchasing':
                #rt = u'<div style="width:120px"><strong>计划需求人:</strong>%s' % (obj.Demand_people)
                diffDate1 = (obj.genPurchasePlanDate - obj.Stock_plan_date).days if (obj.Stock_plan_date is not None and obj.genPurchasePlanDate is not None) else 0
                diffDate2 = (ddtime.now() - obj.genPurchasePlanDate).days if (obj.genPurchasePlanDate is not None) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>'%(obj.Demand_people,diffDate1,obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                if diffDate2 > 2:
                    rt = rt + u'<tr style="color:red"><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.recordPurchaseCodeMan, diffDate2, obj.genPurchasePlanDate)
                else:
                    rt = rt + u'<tr style=""><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.recordPurchaseCodeMan, diffDate2, obj.genPurchasePlanDate)
            elif obj.Status == 'abnormalpurchase':
                diffDate1 = (obj.genPurchasePlanDate - obj.Stock_plan_date).days if (obj.Stock_plan_date is not None and obj.genPurchasePlanDate is not None) else 0
                diffDate2 = (obj.completePurchaseDate - obj.genPurchasePlanDate).days if (obj.completePurchaseDate is not None and obj.genPurchasePlanDate is not None) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                if diffDate2 > 2:
                    rt = rt + u'<tr style="color:red"><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.recordPurchaseCodeMan, diffDate2, obj.genPurchasePlanDate)
                else:
                    rt = rt + u'<tr style=""><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.recordPurchaseCodeMan, diffDate2, obj.genPurchasePlanDate)
            elif obj.Status == 'check':
                #rt = u'<div style="width:120px"><strong>计划需求人:</strong>%s' % (obj.Demand_people)
                diffDate1 = (obj.genPurchasePlanDate - obj.Stock_plan_date).days if (obj.Stock_plan_date is not None and obj.genPurchasePlanDate is not None) else 0
                diffDate2 = (obj.completePurchaseDate - obj.genPurchasePlanDate).days if (obj.recordPurchaseCodeDate is not None or obj.completePurchaseDate is not None) else 0
                diffDate3 = (ddtime.now() - obj.completePurchaseDate).days if (obj.completePurchaseDate is not None) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>'%(obj.Demand_people,diffDate1,obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                if diffDate2 > 2:
                    rt = rt + u'<tr style="color:red"><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.completePurchaseMan, diffDate2, obj.completePurchaseDate)
                else:
                    rt = rt + u'<tr style=""><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.completePurchaseMan, diffDate2, obj.completePurchaseDate)
                if diffDate3 > 2:
                    rt = rt + u'<tr style="color:red"><th>质检:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.CheckMan, diffDate3, obj.CheckTime)
                else:
                    rt = rt + u'<tr style=""><th>质检:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.CheckMan, diffDate3, obj.CheckTime)
            elif obj.Status == 'abnormalcheck':
                diffDate1 = (obj.genPurchasePlanDate - obj.Stock_plan_date).days if (obj.Stock_plan_date is not None and obj.genPurchasePlanDate is not None) else 0
                diffDate2 = (obj.completePurchaseDate - obj.genPurchasePlanDate).days if (obj.recordPurchaseCodeDate is not None or obj.completePurchaseDate is not None) else 0
                diffDate3 = (obj.CheckTime - obj.completePurchaseDate).days if (obj.completePurchaseDate is not None or obj.CheckTime is not None) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                if diffDate2 > 2:
                    rt = rt + u'<tr style="color:red"><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.completePurchaseMan, diffDate2, obj.completePurchaseDate)
                else:
                    rt = rt + u'<tr style=""><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.completePurchaseMan, diffDate2, obj.completePurchaseDate)
                if diffDate3 > 2:
                    rt = rt + u'<tr style="color:red"><th>质检:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.CheckMan, diffDate3, obj.CheckTime)
                else:
                    rt = rt + u'<tr style=""><th>质检:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.CheckMan, diffDate3, obj.CheckTime)
            elif obj.Status == 'completecheck':
                diffDate1 = (obj.genPurchasePlanDate - obj.Stock_plan_date).days if (
                            obj.Stock_plan_date is not None and obj.genPurchasePlanDate is not None) else 0
                diffDate2 = (obj.completePurchaseDate - obj.genPurchasePlanDate).days if (
                            obj.recordPurchaseCodeDate is not None and obj.completePurchaseDate is not None) else 0
                diffDate3 = (obj.CheckTime - obj.completePurchaseDate).days if (
                            obj.completePurchaseDate is not None and obj.CheckTime is not None) else 0
                diffDate4 = (ddtime.now() - obj.CheckTime).days if (obj.CheckTime is not None) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.Demand_people, diffDate1, obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.Demand_people, diffDate1, obj.Stock_plan_date)
                if diffDate2 > 2:
                    rt = rt + u'<tr style="color:red"><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.completePurchaseMan, diffDate2, obj.completePurchaseDate)
                else:
                    rt = rt + u'<tr style=""><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.completePurchaseMan, diffDate2, obj.completePurchaseDate)
                if diffDate3 > 2:
                    rt = rt + u'<tr style="color:red"><th>质检:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.CheckMan, diffDate3, obj.CheckTime)
                else:
                    rt = rt + u'<tr style=""><th>质检:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.CheckMan, diffDate3, obj.CheckTime)
                if diffDate4 > 2:
                    rt = rt + u'<tr style="color:red"><th>生成批次:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.genBatchMan, diffDate4, obj.genBatchDate)
                else:
                    rt = rt + u'<tr style=""><th>生成批次:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.genBatchMan, diffDate4, obj.genBatchDate)
            elif obj.Status == 'genbatch':
                diffDate1 = (obj.genPurchasePlanDate - obj.Stock_plan_date).days if (
                            obj.Stock_plan_date is not None and obj.genPurchasePlanDate is not None) else 0
                diffDate2 = (obj.completePurchaseDate - obj.genPurchasePlanDate).days if (
                            obj.recordPurchaseCodeDate is not None and obj.completePurchaseDate is not None) else 0
                diffDate3 = (obj.CheckTime - obj.completePurchaseDate).days if (
                            obj.completePurchaseDate is not None and obj.CheckTime is not None) else 0
                diffDate4 = (obj.genBatchDate - obj.CheckTime).days if (
                            obj.CheckTime is not None and obj.genBatchDate is not None) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.Demand_people, diffDate1, obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.Demand_people, diffDate1, obj.Stock_plan_date)
                if diffDate2 > 2:
                    rt = rt + u'<tr style="color:red"><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.completePurchaseMan, diffDate2, obj.completePurchaseDate)
                else:
                    rt = rt + u'<tr style=""><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.completePurchaseMan, diffDate2, obj.completePurchaseDate)
                if diffDate3 > 2:
                    rt = rt + u'<tr style="color:red"><th>质检:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.CheckMan, diffDate3, obj.CheckTime)
                else:
                    rt = rt + u'<tr style=""><th>质检:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.CheckMan, diffDate3, obj.CheckTime)
                if diffDate4 > 2:
                    rt = rt + u'<tr style="color:red"><th>生成批次:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.genBatchMan, diffDate4, obj.genBatchDate)
                else:
                    rt = rt + u'<tr style=""><th>生成批次:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.genBatchMan, diffDate4, obj.genBatchDate)
            elif obj.Status == 'completedeliver':
                diffDate1 = (obj.genPurchasePlanDate - obj.Stock_plan_date).days if (
                            obj.Stock_plan_date is not None and obj.genPurchasePlanDate is not None) else 0
                diffDate2 = (obj.completePurchaseDate - obj.genPurchasePlanDate).days if (
                            obj.recordPurchaseCodeDate is not None and obj.completePurchaseDate is not None) else 0
                diffDate3 = (obj.CheckTime - obj.completePurchaseDate).days if (
                            obj.completePurchaseDate is not None and obj.CheckTime is not None) else 0
                diffDate4 = (obj.genBatchDate - obj.CheckTime).days if (
                            obj.CheckTime is not None and obj.genBatchDate is not None) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.Demand_people, diffDate1, obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.Demand_people, diffDate1, obj.Stock_plan_date)
                if diffDate2 > 2:
                    rt = rt + u'<tr style="color:red"><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.completePurchaseMan, diffDate2, obj.completePurchaseDate)
                else:
                    rt = rt + u'<tr style=""><th>采购:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.completePurchaseMan, diffDate2, obj.completePurchaseDate)
                if diffDate3 > 2:
                    rt = rt + u'<tr style="color:red"><th>质检:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.CheckMan, diffDate3, obj.CheckTime)
                else:
                    rt = rt + u'<tr style=""><th>质检:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.CheckMan, diffDate3, obj.CheckTime)
                if diffDate4 > 2:
                    rt = rt + u'<tr style="color:red"><th>生成批次:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.genBatchMan, diffDate4, obj.genBatchDate)
                else:
                    rt = rt + u'<tr style=""><th>生成批次:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (
                    obj.genBatchMan, diffDate4, obj.genBatchDate)
            rt = rt + "</table>"
        except Exception, ex:
            messages.info(self.request,"操作记录加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_opInfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">操作记录信息</p>')

    list_display = ('Stocking_plan_number','show_Status','Stock_plan_date','Product_nature','ProductSKU','ProductName','Supplier','show_ProductImage','Stocking_quantity','Destination_warehouse','level','Demand_people','AccountNum','neworold','AmazonFactory','show_opInfo')

    actions = ['purchasing_plan_audit','get_excel_product_registration_form','not_demand','againdemand']

    def save_models(self,):
        try:
            pass
        except Exception, ex:
            messages.info(self.request,"保存报错:%s"%(str(ex)))
        
    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_demand_fba_all_Admin, self).get_list_queryset()
        from django.contrib.auth.models import User
        userID = [each.id for each in User.objects.filter(groups__id__in=[65])]
        # if request.user.is_superuser or request.user.id in userID:
        if request.user.id in userID:
            qs = qs.filter(Demand_people=request.user.first_name)
        Status = request.GET.get('Status', '')  # 采购状态
        if Status == 'all':
            Status = ''
        Status1 = request.GET.get('Status1', '')  # 采购状态
        if Status1:
            Status = Status1
        Stocking_plan_number = request.GET.get('Stocking_plan_number', '')   #备货计划号
        Stock_plan_dateStart      = request.GET.get('Stock_plan_dateStart', '')     # 备货计划时间
        Stock_plan_dateEnd      = request.GET.get('Stock_plan_dateEnd', '')     # 备货计划时间
        Demand_people = request.GET.get('Demand_people', '')             # 计划需求人
        Product_nature = request.GET.get('Product_nature', '')            #产品性质
        ProductSKU = request.GET.get('ProductSKU', '')                     #商品sku
        ProductName = request.GET.get('ProductName', '')                    # 商品名称
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
                        'Supplier__exact':Supplier,
                        'AccountNum__exact':AccountNum,
					    'Destination_warehouse__exact': Destination_warehouse,
                        'level__exact':level,
                        'Buyer__exact':Buyer,
                        'Status__exact':Status,
                        'OplogTime__gte':OplogTimeStart,'OplogTime__lt':OplogTimeEnd,
                        'neworold__exact': neworold,'AmazonFactory__exact':AmazonFactory,
                      }

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

