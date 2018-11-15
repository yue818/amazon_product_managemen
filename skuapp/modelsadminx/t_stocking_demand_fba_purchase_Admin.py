# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fba_purchase_Admin.py
 @time: 2018-08-11

"""
from xadmin.layout import Fieldset, Row
from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
from django.utils.safestring import mark_safe
from .t_product_Admin import *
from skuapp.table.public import *
from pyapp.models import b_goods as py_b_goods
from datetime import datetime as ddtime
import datetime,random
from Project.settings import *
import oss2
from skuapp.table.t_stocking_demand_fba_detail import t_stocking_demand_fba_detail

class t_stocking_demand_fba_purchase_Admin(object):
    search_box_flag = True
    fba_tree_menu_flag = True
    hide_page_action = True
    downloadxls = True
    purchase_order_plugin = True
    def del_None(self,col):
        rt = col
        if not col:
            rt = ''
        return rt

    def show_goodsInfo(self,obj) :
        try:
            from brick.public.django_wrap import django_wrap
            strTmp = ""
            Product_nature_value = ""
            for status in getChoices(ChoiceProductnature):
                if status[0] == obj.Product_nature:
                    Product_nature_value = status[1]
                    break
            Warehouse_value = ""
            for status in getChoices(ChoiceWarehouse):
                if status[0] == obj.Destination_warehouse:
                    Warehouse_value = status[1]
                    break
            if obj.LogisticsNumber is not None and obj.LogisticsNumber.strip() != '':
                strTmp =  '<a target="_blank" href="https://www.baidu.com/s?wd=%s">查看物流</a>' % obj.LogisticsNumber
            strSupplierlink = obj.Supplierlink if obj.Supplierlink is not None else ""
            TransFactory = '转服装供应链生产' if obj.TransFactory is not None else "非转服装供应链生产"
            rt = u'<strong>商品SKU:</strong>%s<br><strong>店铺SKU:</strong>%s<br><strong>产品性质:</strong>%s<br><strong>商品名称:</strong>%s<br><strong>' \
                 u'计划需求人:</strong>%s<br><strong>供应商:</strong>%s<br><strong>采购人:</strong>%s<br><strong>采购备注:</strong>%s' \
                 u'<br><strong>物流信息:</strong>%s<br><strong>仓库:</strong>%s<br><strong>采购链接:</strong>%s<br><strong>转供应链:</strong>%s' % (
                obj.ProductSKU, obj.ShopSKU, Product_nature_value, obj.ProductName,obj.Demand_people ,obj.Supplier,obj.Buyer,obj.Remarks,strTmp,Warehouse_value,django_wrap(strSupplierlink, ';', 1),TransFactory)
            return mark_safe(rt)
        except Exception, ex:
            messages.info(self.request,"商品信息加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
    show_goodsInfo.short_description = u'商品信息'

    def show_ProductImage(self,obj) :
        from Project.settings import BmpUrl
        # 获取图片的url
        picture_url = obj.ProductImage  # 获取图片的url
        sku = obj.ProductSKU  # 获取商品SKU
        if not picture_url:
            picture_url = BmpUrl + sku + '.jpg'

        rt = """<img src="%s"  width="120" height="120"  title="%s" onerror="this.title=''" />  """ % (picture_url, picture_url)
        return mark_safe(rt)
    show_ProductImage.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">商品图片</p>')

    def show_Status(self, obj):
        try:
            rt = ""
            strStatus = ""
            diffDate = 0
            for status in getChoices(ChoiceFBAPlanStatus):
                if status[0] == obj.Status:
                    strStatus = status[1]
                    break
            if (obj.Status == 'notpurchase' or obj.Status == 'purchasing'):
                diffDate = (ddtime.now() - obj.genPurchasePlanDate).days if obj.genPurchasePlanDate is not None else 0
                flag = 1 if ((obj.genPurchasePlanDate is not None) and (
                        str(ddtime.now()) > str(obj.genPurchasePlanDate + datetime.timedelta(days=2)))) else 0
                if flag == 1:
                    rt = '<div class="box" style="width: 150px;height: 80px;background-color: red;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (strStatus,diffDate)
                else:
                    rt = '<div class="box" style="width: 150px;height: 80px;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (
                    strStatus, diffDate)
            elif obj.Status == 'completedeliver':
                rt = u'已发货'
            elif obj.completeStatus == 'completepurchase':
                rt = u'完成采购'
            else:
                rt = u'异常采购数据'
        except Exception, ex:
            messages.info(self.request,"采购状态加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_Status.short_description = mark_safe('<p align="center" style="width:120px;color:#428bca;">采购状态</p>')

    def show_opInfo(self, obj):
        try:
            rt = u'<table border="1"><tr><th>操作员</th><th>告警信息</th><th>操作时间</th></tr>'
            if obj.Status == 'notpurchase' or obj.Status == 'purchasing':
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
            elif obj.completeStatus == 'completepurchase' or obj.Status == 'completedeliver':
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
                rt = rt + u'<tr style=""><th>完成采购:%s</th><th></th><th>%s</th></tr>' % (obj.completePurchaseMan, obj.completePurchaseDate)
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
            rt = rt + "</table>"
        except Exception, ex:
            messages.info(self.request,"操作记录加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_opInfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">操作记录信息</p>')

    def show_Supplierlink(self,obj) :
        from brick.public.django_wrap import django_wrap
        rt = django_wrap(obj.Supplierlink,';',1)
        if obj.LogisticsNumber is not None and obj.LogisticsNumber.strip() != '':
            rt = rt + '<a target="_blank" href="https://www.baidu.com/s?wd=%s">查看物流</a>'%obj.LogisticsNumber
        return mark_safe(rt)
    show_Supplierlink.short_description = u'采购链接/物流信息'

    def show_infors_number(self,obj) :
        read = ''
        read1 = ''
        if obj.Status != 'notpurchase':
            read = 'readonly'
        if obj.Status == 'notpurchase' or obj.Status == 'purchasing':
            read1 = ''
        else:
            read1 = 'readonly'
        rt = '<table>'
        rt = u'%s<tr><th>采购订单号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
             u'<tr><th>1688单号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt,self.del_None(obj.Single_number),obj.id,'Single_number',read1,self.del_None(obj.Single_number),str(obj.id)+'_Single_number',
              self.del_None(obj.Ali_number),obj.id,'Ali_number',read,self.del_None(obj.Ali_number),str(obj.id)+'_Ali_number',)

        rt = u'%s<tr><th>物流单号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt,self.del_None(obj.LogisticsNumber),obj.id,'LogisticsNumber',read,self.del_None(obj.LogisticsNumber),str(obj.id)+'_LogisticsNumber')

        rt = u'%s<tr><th>供应商：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.Supplier), obj.id, 'Supplier', read,
              self.del_None(obj.Supplier), str(obj.id) + '_Supplier')
        rt = u'%s<tr><th>采购员：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.Buyer), obj.id, 'Buyer', read,
              self.del_None(obj.Buyer), str(obj.id) + '_Buyer')
        rt = u'%s<tr><th>采购链接：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.Supplierlink), obj.id, 'Supplierlink', read,
              self.del_None(obj.Supplierlink), str(obj.id) + '_Supplierlink')

        rt = u'%s<tr><th>普元备注：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.pyRemark), obj.id, 'pyRemark', 'readonly',
              self.del_None(obj.pyRemark), str(obj.id) + '_pyRemark')
        rt = rt + '</table>'

        return mark_safe(rt)
    show_infors_number.short_description = u'填写信息'

    def purchase_number(self,obj) :
        rt = '<table>'
        if obj.Status == 'notpurchase':
            rt = u'%s<tr><th>计划采购数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
                 u'<tr><th>实际采购数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> '% \
                 (rt,self.del_None(obj.Stocking_quantity),obj.id,'Stocking_quantity','readonly',self.del_None(obj.Stocking_quantity),str(obj.id)+'_Stocking_quantity',
                  self.del_None(obj.QTY),obj.id,'QTY','',self.del_None(obj.QTY),str(obj.id)+'_QTY')
            rt = u'%s<tr><th>采购备注：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                 (rt, self.del_None(obj.Remarks), obj.id, 'Remarks', '',
                  self.del_None(obj.Remarks), str(obj.id) + '_Remarks')
        elif obj.Status == 'purchasing':
            rt = u'%s<tr><th>计划采购数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
                 u'<tr><th>实际采购数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' \
                 u'<tr><th>本次到货数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                 (rt, self.del_None(obj.Stocking_quantity), obj.id, 'Stocking_quantity', 'readonly',self.del_None(obj.Stocking_quantity), str(obj.id) + '_Stocking_quantity',
                  self.del_None(obj.QTY), obj.id, 'QTY', 'readonly', self.del_None(obj.QTY), str(obj.id) + '_QTY',
                  self.del_None(obj.The_arrival_of_the_number), obj.id, 'The_arrival_of_the_number', '',self.del_None(obj.The_arrival_of_the_number), str(obj.id) + '_The_arrival_of_the_number',)
            rt = u'%s<tr><th>采购备注：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                 (rt, self.del_None(obj.Remarks), obj.id, 'Remarks', '',
                  self.del_None(obj.Remarks), str(obj.id) + '_Remarks')
        elif obj.completeStatus == 'completepurchase' or obj.Status == 'completedeliver':
            rt = u'%s<tr><th>计划采购数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
                 u'<tr><th>实际采购数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' \
                 u'<tr><th>本次到货数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                 (rt, self.del_None(obj.Stocking_quantity), obj.id, 'Stocking_quantity', 'readonly',self.del_None(obj.Stocking_quantity), str(obj.id) + '_Stocking_quantity',
                  self.del_None(obj.QTY), obj.id, 'QTY', 'readonly', self.del_None(obj.QTY), str(obj.id) + '_QTY',
                  self.del_None(obj.The_arrival_of_the_number), obj.id, 'The_arrival_of_the_number', 'readonly',self.del_None(obj.The_arrival_of_the_number), str(obj.id) + '_The_arrival_of_the_number',)
        elif obj.Status == 'abnormalpurchase':
            rt = u'%s<tr><th>计划采购数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
                 u'<tr><th>实际采购数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' \
                 u'<tr><th>本次到货数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                 (rt, self.del_None(obj.Stocking_quantity), obj.id, 'Stocking_quantity', 'readonly',self.del_None(obj.Stocking_quantity), str(obj.id) + '_Stocking_quantity',
                  self.del_None(obj.QTY), obj.id, 'QTY', 'readonly', self.del_None(obj.QTY), str(obj.id) + '_QTY',
                  self.del_None(obj.The_arrival_of_the_number), obj.id, 'The_arrival_of_the_number', 'readonly',self.del_None(obj.The_arrival_of_the_number), str(obj.id) + '_The_arrival_of_the_number',)
            rt = u'%s<tr><th>采购备注：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_purchase\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                 (rt, self.del_None(obj.Remarks), obj.id, 'Remarks', '',
                  self.del_None(obj.Remarks), str(obj.id) + '_Remarks')
        rt = rt + '</table>'

        return mark_safe(rt)
    purchase_number.short_description = u'采购信息'

    list_display = (
    'Stocking_plan_number', 'show_Status', 'Product_nature','show_infors_number', 'show_goodsInfo', 'show_ProductImage','purchase_number', 'level', 'AccountNum', 'show_opInfo')
    list_editable = ('Single_number', 'Supplierlink', 'Ali_number', 'Arrival_date','Buyer', 'Logistics_costs', 'LogisticsNumber',
                     'pay_method', 'Prepayments', 'QTY', 'Remarks','OplogTime', 'The_arrival_of_the_number')
    fields = ('Single_number', 'Supplier', 'Ali_number', 'Arrival_date','Buyer', 'QTY', 'Remarks','Supplierlink', 'OplogTime')

    actions = [ 'tran_purchase','complete_purchased','not_purchase','abnormal_purchase','tran_return','get_excel_to_py',]

    def tran_purchase(self, request, objs):
        try:
            errorInfo = []
            for obj in objs:
                if obj.Status == 'abnormalpurchase':
                    obj.Status = 'notpurchase'
                    obj.giveupMan = request.user.first_name
                    obj.giveupDate = ddtime.now()
                    obj.OplogTime = ddtime.now()
                    obj.save()
                    t_stocking_demand_fba_detail.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).update(
                        Status='notpurchase')
                else:
                    errorInfo.append(obj.Stocking_plan_number)
            if len(errorInfo)>0:
                messages.info(self.request, "以下备货计划号:%s,非采购异常状态，不允许操作。" % (str(errorInfo)))
        except Exception as e:
            messages.error(self.request,"提交转未采购报错:%s，请联系开发人员"%(str(e)))
    tran_purchase.short_description = u'异常->未采购'

    def complete_purchased(self,request,objs):
        try:
            insertinto = []
            errorInfo = []
            for obj in objs:
                if  obj.Status == 'purchasing' and obj.The_arrival_of_the_number is not None and str(obj.The_arrival_of_the_number) !='' \
                        and int(obj.The_arrival_of_the_number) > 0 and obj.Single_number is not None and str(obj.Single_number) != '':
                    arrNum = obj.The_arrival_of_the_number if obj.The_arrival_of_the_number is not None else 0
                    obj.Status = 'check'
                    obj.completeStatus = 'completepurchase'
                    obj.completePurchaseMan = request.user.first_name
                    obj.completePurchaseDate = ddtime.now()
                    obj.OplogTime = ddtime.now()
                    obj.Stock_plan_unfinished_quantity = obj.QTY - arrNum
                    obj.checkCompleteNum = arrNum
                    obj.checkInferiorNum = 0
                    obj.save()
                    t_stocking_demand_fba_detail.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).update(
                        Status='check')
                else:
                    errorInfo.append(obj.Stocking_plan_number)
            if errorInfo:
                messages.error(request,u"以下不能提交完成备货计划号：%s,可能由于未生成采购订单号或本次到货数量未填写。"%(errorInfo))
        except Exception, ex:
            messages.info(self.request,"完成入库报错,请联系开发人员解决:%s"%(str(ex)))
    complete_purchased.short_description = u'完成采购'

    def abnormal_purchase(self, request, objs):
        try:
            errorInfo = []
            for obj in objs:
                if obj.Status == 'purchasing' or obj.Status == 'notpurchase':
                    obj.Status = 'abnormalpurchase'
                    obj.completePurchaseMan = request.user.first_name
                    obj.completePurchaseDate = ddtime.now()
                    obj.OplogTime = ddtime.now()
                    obj.save()
                    t_stocking_demand_fba_detail.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).update(
                        Status='abnormalpurchase')
                else:
                    errorInfo.append(obj.Stocking_plan_number)
        except Exception as e:
            messages.info(self.request,"提交采购异常数据报错:%s，请联系开发人员"%(str(e)))
    abnormal_purchase.short_description = u'采购异常数据'

    def not_purchase(self, request, objs):
        try:
            errorInfo = []
            for obj in objs:
                if obj.Status == 'notpurchase' and (obj.Single_number is None or obj.Single_number == ''):
                    obj.Status = 'giveup'
                    obj.giveupMan = request.user.first_name
                    obj.giveupDate = ddtime.now()
                    obj.OplogTime = ddtime.now()
                    obj.save()
                    t_stocking_demand_fba_detail.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).update(
                        Status='giveup')
                else:
                    errorInfo.append(obj.Stocking_plan_number)
            if len(errorInfo)>0:
                messages.info(self.request, "以下备货计划号:%s,采购订单非空,不能提交不需要采购，需提交采购异常后进行退单操作。" % (str(errorInfo)))
        except Exception as e:
            messages.error(self.request,"不需采购提交报错:%s，请联系开发人员"%(str(e)))
    not_purchase.short_description = u'不需采购'

    def tran_return(self, request, objs):
        try:
            errorInfo = []
            returnList = []
            from skuapp.table.t_stocking_rejecting_fba import t_stocking_rejecting_fba
            for obj in objs:
                The_arrival_of_the_number = obj.QTY if obj.The_arrival_of_the_number is None else obj.The_arrival_of_the_number
                if obj.Status == 'abnormalpurchase' and obj.Single_number is not None:
                    RejectNumber = ddtime.now().strftime('%Y%m%d%H%M%S') + '_' + str(i)
                    returnList.append(t_stocking_rejecting_fba(
                        RejectNumber=RejectNumber, RejectDate=ddtime.now(),
                        RejectMan=request.user.first_name,
                        ProductSKU=obj.ProductSKU, ProductImage=obj.ProductImage, ProductName=obj.ProductName,
                        PurchaseOrderNum=obj.Single_number,
                        Status='rejecting', RejectStatus='return', RejectNum=The_arrival_of_the_number,
                        Remarks='转退',SummbitRejectMan=request.user.first_name,SummbitRejectDate=ddtime.now(),isCheckTranReturn=0
                    ))
                    obj.Status = 'giveup'
                    obj.giveupMan = request.user.first_name
                    obj.giveupDate = ddtime.now()
                    obj.tranReturnMan = request.user.first_name
                    obj.tranReturnDate = ddtime.now()
                    obj.OplogTime = ddtime.now()
                    obj.Remarks = u'转退'
                    obj.save()
                    t_stocking_demand_fba_detail.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).update(
                        Status='giveup')
                else:
                    errorInfo.append(obj.Stocking_plan_number)
            t_stocking_rejecting_fba.objects.bulk_create(returnList)
            if len(errorInfo)>0:
                messages.info(self.request, "以下备货计划号:%s,采购订单非空,不能提交不需要采购，需提交采购异常后进行退单操作。" % (str(errorInfo)))
        except Exception as e:
            messages.error(self.request,"不需采购提交报错:%s，请联系开发人员"%(str(e)))
    tran_return.short_description = u'退货->转退货管理'

    def get_excel_to_py(self, request, objs):
        try:
            from xlwt import *
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            # if not os.path.exists(path):
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

            mkdir_p(path)
            os.popen('chmod 777 %s' % (path))

            w = Workbook()
            sheet = w.add_sheet(u'采购计划单')

            sheetlist = [u'备货计划号',u'采购订单',u'1688单号',u'商品sku',u'商品名称',u'图片',u'计划采购数量',u'实际采购数量',u'入库数量',
                         u'含税单价',u'仓库',u'供应商',u'采购链接',u'网页URL2',u'预计到货日期',u'采购人',u'备货计划时间',u'采购状态',u'账号',u'备注',]

            for index,item in enumerate(sheetlist):
                sheet.write(0,index,item)

            # 写数据
            idlist = []
            row = 0
            for qs in objs:

                row = row + 1
                column = 0
                sheet.write(row, column, qs.Stocking_plan_number) # 备货计划号

                column = column + 1
                sheet.write(row, column, qs.Single_number) # 采购订单/调拨单号

                column = column + 1
                sheet.write(row, column, qs.Ali_number) # 1688单号

                column = column + 1
                sheet.write(row, column, qs.ProductSKU) # sku

                column = column + 1
                sheet.write(row, column, qs.ProductName) # 商品名称

                column = column + 1
                sheet.write(row, column, qs.ProductImage) # 图片

                column = column + 1
                sheet.write(row, column, qs.Stocking_quantity) # 计划采购数量
                column = column + 1
                sheet.write(row, column, qs.QTY)  # 实际采购数量
                column = column + 1
                sheet.write(row, column, qs.The_arrival_of_the_number)  # 入库数量

                column = column + 1
                sheet.write(row, column, qs.ProductPrice) # 含税单价

                column = column + 1
                Destination_warehouse = ''
                for warehouse in getChoices(ChoiceWarehouse):
                    if warehouse[1] is not None and qs.Destination_warehouse == warehouse[0].strip():
                        Destination_warehouse = warehouse[1].strip()
                sheet.write(row, column, Destination_warehouse) # 仓库

                column = column + 1
                sheet.write(row, column, qs.Supplier) # 供应商

                column = column + 1
                sheet.write(row, column, qs.Supplierlink) # 采购链接

                column = column + 1
                URL2 = ''
                py_b_goods_obj = py_b_goods.objects.filter(SKU = qs.ProductSKU).values('LinkUrl2')
                if py_b_goods_obj.exists():
                    URL2 = py_b_goods_obj[0]['LinkUrl2']
                sheet.write(row, column, URL2)  # 网页URL2

                column = column + 1
                sheet.write(row, column, qs.Arrival_date)  # 预计到货日期

                column = column + 1
                sheet.write(row, column, qs.Buyer) # 采购人

                column = column + 1
                sheet.write(row, column, '%s'%qs.Stock_plan_date) # 备货计划时间

                column = column + 1
                if qs.Status == 'check':
                    sta = u'完成采购'
                elif qs.Status == 'purchasing':
                    sta = u'采购中'
                elif qs.Status == 'abnormalpurchase':
                    sta = u'采购异常数据'
                elif qs.Status == 'completedeliver':
                    sta = u'已发货'
                else:
                    sta = u'未采购'
                sheet.write(row, column, sta) # 采购状态

                column = column + 1
                sheet.write(row, column, qs.AccountNum)  # 账号

                column = column + 1
                sheet.write(row, column, qs.Remarks) # 备注
                idlist.append(qs.id)
            filename = request.user.username + '_' + ddtime.now().strftime('%Y%m%d%H%M%S') + '.xls'
            w.save(path + '/' + filename)
            os.popen(r'chmod 777 %s' % (path + '/' + filename))

            # 上传oss对象
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
            bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
            # 删除现有的
            for object_info in oss2.ObjectIterator(bucket,
                                                   prefix='%s/%s_' % (request.user.username, request.user.username)):
                bucket.delete_object(object_info.key)
            bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))
            #objs.filter(id__in=idlist).update(ExcelStatus='yes')
            messages.success(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                        filename) + u':成功导出,可点击Download下载到本地............................。')
        except Exception as e:
            messages.info(self.request,"导出数据到execl报错:%s，请联系开发人员"%(str(e)))

    get_excel_to_py.short_description = u'导出Excel表格'


    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_demand_fba_purchase_Admin, self).get_list_queryset()
        from django.contrib.auth.models import User
        userID = [each.id for each in User.objects.filter(groups__id__in=[65])]
        # if request.user.is_superuser or request.user.id in userID:
        if request.user.id in userID:
            qs = qs.filter(Demand_people=request.user.first_name)
        Status = request.GET.get('Status', '')  # 采购状态
        completeStatus = ''
        if Status == 'completepurchase':
            completeStatus = 'completepurchase'
            Status = ''
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
        LogisticsNumber = request.GET.get('LogisticsNumber')#物流单号
        Single_number = request.GET.get('Single_number')  # 采购单号
        Ali_number  = request.GET.get('Ali_number')  # 1688单号
        QTYStart = request.GET.get('QTYStart', '')  # 备货计划时间
        QTYEnd = request.GET.get('QTYEnd', '')  # 备货计划时间
        Stocking_quantityStart = request.GET.get('Stocking_quantityStart', '')  # 备货计划时间
        Stocking_quantityEnd = request.GET.get('Stocking_quantityEnd', '')  # 备货计划时间
        The_arrival_of_the_numberStart = request.GET.get('The_arrival_of_the_numberStart', '')  # 备货计划时间
        The_arrival_of_the_numberEnd = request.GET.get('The_arrival_of_the_numberEnd', '')  # 备货计划时间


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
                        'Status__exact':Status,'completeStatus':completeStatus,
                        'QTYStart':QTYStart,'QTYEnd':QTYEnd,
                        'Stocking_quantity__gte': Stocking_quantityStart, 'Stocking_quantity__lt': Stocking_quantityEnd,
                        'The_arrival_of_the_number__gte': The_arrival_of_the_numberStart, 'The_arrival_of_the_number__lt': The_arrival_of_the_numberEnd,
                        'OplogTime__gte':OplogTimeStart,'OplogTime__lt':OplogTimeEnd,
                        'neworold__exact': neworold,'LogisticsNumber__exact':LogisticsNumber,
                        'Single_number__icontains':Single_number,'Ali_number__exact':Ali_number,
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

