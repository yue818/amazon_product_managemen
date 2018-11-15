# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: wangzy
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_audit_Admin.py
 @time: 2018-04-20 10:30

"""
from xadmin.layout import Fieldset, Row
import datetime,random
from pyapp.models import b_goods as py_b_goods,B_Supplier as py_b_Supplier
from skuapp.table.t_stocking_purchase_order import t_stocking_purchase_order
from django.contrib import messages
from django.utils.safestring import mark_safe
from datetime import datetime as ddtime
from django.db.models import Q
from skuapp.table.public import *

class t_stocking_demand_audit_Admin(object):
    search_box_flag = True
    importfile_plugin = False
    jump_temp = False
    site_left_menu_stocking_purchase = True
    def show_ProductImage(self,obj) :
        rt =  '<img src="%s"  width="120" height="120"/>  '%(obj.ProductImage)
        return mark_safe(rt)
    show_ProductImage.short_description = u'商品图片'

    def show_Status(self, obj):
        try:
            rt = ""
            strStatus = ""
            for status in getChoices(ChoicePlanStatus):
                if status[0] == obj.Status:
                    strStatus = status[1]
                    break
            if  obj.Status == 'noaudit':
                diffDate = (ddtime.now() - obj.Stock_plan_date).days if obj.Stock_plan_date is not None else 0
                flag = 1 if ((obj.Stock_plan_date is not None) and (str(ddtime.now()) > str(obj.Stock_plan_date + datetime.timedelta(days=2)))) else 0
                if flag == 1:
                    rt = '<div class="box" style="width: 150px;height: 80px;background-color: red;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天' % (strStatus,diffDate)
                else:
                    rt = '<div class="box" style="width: 150px;height: 80px;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (strStatus,diffDate)
            else:
                rt = strStatus
        except Exception, ex:
            messages.info(self.request,"采购状态加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_Status.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">采购状态</p>')

    def show_opInfo(self, obj):
        try:
            rt = u'<table border="1" ><tr><th>操作员</th><th>告警信息</th><th>操作时间</th></tr>'
            diffDate1 = 0
            if obj.AuditTime:
                diffDate1 = (obj.AuditTime - obj.Stock_plan_date).days if (obj.AuditTime is not None and obj.Stock_plan_date is not None) else 0
            else:
                diffDate1 = (datetime.datetime.now() - obj.Stock_plan_date).days if (obj.Stock_plan_date is not None) else 0
            if diffDate1 > 1:
                rt = rt + u'<tr style="color:red"><th>需求:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
            else:
                rt = rt + u'<tr style=""><th>需求:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
            if obj.AuditTime:
                rt = rt + u'<tr style=""><th>审核:%s</th><th></th><th>%s</th></tr>' % (obj.Auditor, obj.AuditTime)
            rt = rt + "</table>"
        except Exception, ex:
            messages.info(self.request,"操作信息加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_opInfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">操作记录信息</p>')

    list_display = ('Stocking_plan_number','show_Status','Product_nature','ProductSKU','ProductName','show_ProductImage','Stocking_quantity','Destination_warehouse','level','Demand_people','AccountNum','neworold','show_opInfo')

    actions = ['audit_purchasing_plan','noaudit_purchasing_plan','giveup_purchasing_plan']

    def audit_purchasing_plan(self,request,objs):
        for obj in objs:
            obj.Auditor = request.user.first_name
            obj.AuditTime = datetime.datetime.now()
            obj.Status = 'audit' # 审核通过
            obj.OplogTime=ddtime.now() #记录生成时间
            obj.save()
    audit_purchasing_plan.short_description = u'审核通过'

    def noaudit_purchasing_plan(self,request,objs):
        for obj in objs:
            obj.Auditor = request.user.first_name
            obj.AuditTime = ddtime.now()
            obj.Status = 'back' # 打回
            obj.save()
    noaudit_purchasing_plan.short_description = u'审核不通过'

    def giveup_purchasing_plan(self,request,objs):
        for obj in objs:
            obj.Auditor = request.user.first_name
            obj.AuditTime = ddtime.now()
            obj.Status = 'giveup' # 废弃
            obj.save()
    giveup_purchasing_plan.short_description = u'废弃'
        
    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_demand_audit_Admin, self).get_list_queryset()
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
        Site = request.GET.get('Site', '')                                  # 站点
        Destination_warehouse = request.GET.get('Destination_warehouse', '')  # 目的地仓库


        level = request.GET.get('level', '')                                # 紧急程度
        Auditor = request.GET.get('Auditor', '')                            #审核人
        AuditTimeStart = request.GET.get('AuditTimeStart', '')                        #审核时间
        AuditTimeEnd = request.GET.get('AuditTimeEnd', '')                        #审核时间
        Buyer = request.GET.get('Buyer', '')                                #采购人

        UpdateTimeStart = request.GET.get('UpdateTimeStart', '')            # 更新时间
        UpdateTimeEnd = request.GET.get('UpdateTimeEnd', '')               # 更新时间
        neworold = request.GET.get('neworold', '')  # 新品备货
        OplogTimeStart = request.GET.get('OplogTimeStart','')  #记录生成时间
        OplogTimeEnd =request.GET.get('OplogTimeEnd','') #记录生成时间


        searchList = {
                        'Stocking_plan_number__exact':Stocking_plan_number,
                        'Stock_plan_date__gte':Stock_plan_dateStart,'Stock_plan_date__lt':Stock_plan_dateEnd,
                        'Demand_people__exact':Demand_people,'Product_nature__exact':Product_nature,
                        'ProductSKU__icontains': ProductSKU,'ProductName__exact':ProductName,
                        'ProductWeight__gte':ProductWeightStart,
                        'ProductWeight__lt':ProductWeightEnd,
                        'Supplier__exact':Supplier,
                        'AccountNum__exact':AccountNum,'Site__exact':Site,
                        'level__exact':level,
                        'Auditor__exact': Auditor,
                        'AuditTime__gte': AuditTimeStart,'AuditTime__lt': AuditTimeEnd,
                        'Buyer__exact':Buyer,
                        'UpdateTime__gte':UpdateTimeStart,'UpdateTime__lt':UpdateTimeEnd,
                        'OplogTime__gte':OplogTimeStart,'OplogTime__lt':OplogTimeEnd,
                        'neworold__exact': neworold,
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

        if Destination_warehouse == "FBA":
            return qs.filter(Status='noaudit').filter(Destination_warehouse__icontains='FBA-').order_by("submitAuditDate")
        elif Destination_warehouse == "NOFBA":
            return qs.filter(Status='noaudit').filter(~Q(Destination_warehouse__icontains='FBA-')).order_by("submitAuditDate")
        else:
            return qs.filter(Status='noaudit').order_by("submitAuditDate")

