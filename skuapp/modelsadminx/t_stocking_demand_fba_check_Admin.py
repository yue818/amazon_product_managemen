# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fba_check_Admin.py
 @time: 2018-08-14

"""
from xadmin.layout import Fieldset, Row
from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
from django.utils.safestring import mark_safe
from .t_product_Admin import *
from skuapp.table.public import *
from pyapp.models import b_goods as py_b_goods
from datetime import datetime as ddtime
import datetime as tmpDate,random
from Project.settings import *
import oss2
from skuapp.table.t_stocking_demand_fba_detail import t_stocking_demand_fba_detail

class t_stocking_demand_fba_check_Admin(object):
    search_box_flag = True
    fba_tree_menu_flag = True
    hide_page_action = True
    downloadxls = True
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
            rt = u'<strong>店铺SKU:</strong>%s<br><strong>产品性质:</strong>%s<br><strong>商品名称:</strong>%s<br><strong>' \
                 u'计划需求人:</strong>%s<br><strong>供应商:</strong>%s<br><strong>采购人:</strong>%s<br><strong>普元备注:</strong>%s' \
                 u'<br><strong>物流信息:</strong>%s<br><strong>仓库:</strong>%s<br><strong>采购链接:</strong>%s' % (
                obj.ShopSKU, Product_nature_value, obj.ProductName,obj.Demand_people ,obj.Supplier,obj.Buyer,obj.pyRemark,strTmp,Warehouse_value,django_wrap(strSupplierlink, ';', 1))
            return mark_safe(rt)
        except Exception, ex:
            messages.info(self.request,"商品信息加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
    show_goodsInfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">商品信息</p>')

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
            diffDate = 0
            for status in getChoices(ChoiceFBAPlanStatus):
                if status[0] == obj.Status:
                    strStatus = status[1]
                    break
            if (obj.Status == 'check'):
                diffDate = (ddtime.now() - obj.completePurchaseDate).days if obj.completePurchaseDate is not None else 0
                flag = 1 if ((obj.completePurchaseDate is not None) and (str(ddtime.now()) > str(obj.completePurchaseDate + tmpDate.timedelta(days=2)))) else 0
                if flag == 1:
                    rt = '<div class="box" style="width: 150px;height: 80px;background-color: red;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (strStatus,diffDate)
                else:
                    rt = '<div class="box" style="width: 150px;height: 80px;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (
                    strStatus, diffDate)
            elif (obj.checkStatus == 'completecheck'):
                rt = '完成质检'
            else:
                rt = strStatus
        except Exception, ex:
            messages.info(self.request,"质检状态加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_Status.short_description = mark_safe('<p align="center" style="width:120px;color:#428bca;">质检状态</p>')

    def show_opInfo(self, obj):
        try:
            rt = u'<table border="1"><tr><th>操作员</th><th>告警信息</th><th>操作时间</th></tr>'
            if obj.Status == 'check':
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
            elif obj.checkStatus == 'completecheck' or obj.Status == 'abnormalcheck':
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
            rt = rt + "</table>"
        except Exception, ex:
            messages.info(self.request,"操作记录加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_opInfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">操作记录信息</p>')

    def show_infors_number(self,obj) :
        try:
            rt = u'<strong>采购订单号:</strong>%s<br><strong>1688单号:</strong>%s<br><strong>物流单号:</strong>%s' % (
                obj.Single_number, obj.Ali_number,obj.LogisticsNumber )
            return mark_safe(rt)
        except Exception, ex:
            messages.info(self.request,"商品信息加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_infors_number.short_description = mark_safe(u'<p style="width:100px;color:#428bca;" align="center">单号信息</p>')

    def purchaseNum(self,obj) :
        try:
            rt = u'<strong>计划采购数量:</strong>%s<br><strong>实际采购数量:</strong>%s<br><strong>实际到货数量:</strong>%s' % (
                obj.Stocking_quantity, obj.QTY,obj.The_arrival_of_the_number )
            return mark_safe(rt)
        except Exception, ex:
            messages.info(self.request,"采购数量加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    purchaseNum.short_description = mark_safe(u'<p style="width:100px;color:#428bca;" align="center">采购数量</p>')

    def deal_checkData(self,obj) :
        try:
            rt = ""
            input_id = str(obj.id)
            CheckNumber = obj.CheckNumber
            CheckQualified = obj.CheckQualified
            PercentOfPass = obj.PercentOfPass
            if obj.CheckNumber is None:
                CheckNumber = '0'
            if obj.CheckQualified is None:
                CheckQualified = '0'
            if obj.PercentOfPass is None:
                PercentOfPass = '0'
            allCheck = ""
            partCheck = ""
            noCheck = ""
            if obj.isCheck == 0:
                allCheck = "checked='checked'"
            elif obj.isCheck == 1:
                partCheck = "checked='checked'"
            else:
                noCheck = "checked='checked'"
            if obj.Status == 'check':
                rt = '<div id = "checkPurchase_%s">' % (input_id)
                rt = u'%s质检选择:<input name="checkOption_%s" type="radio" %s value="2" />免检&nbsp' \
                     u'<input name="checkOption_%s" type="radio" %s  value="1" />抽检&nbsp' \
                     u'<input name="checkOption_%s" type="radio" %s  value="0" />全检<br>' \
                     u'抽检数量:<input name="checkPart_%s" type="text" style="width:120px;height:25px" id="checkPart_%s" value="%s" onkeyup="jisuanPass_%s()"/><br>' \
                     u'合格数量:<input type="text" style="width:120px;height:25px" id="checkPass_%s" value="%s" onkeyup="jisuanPass_%s()"/><br>' \
                     u'合格率为:<input type="text" readonly= "true" style="width:120px;height:25px;" id="PercentOfPass_%s" value="%s%s" /><br>'\
                     %(rt, input_id,noCheck,input_id,partCheck,input_id,allCheck,input_id,input_id, CheckNumber,input_id, input_id,CheckQualified,input_id,input_id, PercentOfPass,'%')

                rt = u'%s<br><strong>合格总量:</strong><input value="%s" type="text" style="width:120px;height:25px" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba\')" %s title="%s"/><span id="%s"></span><br>' \
                     u'<strong>次品总量:</strong><input value="%s" type="text" style="width:120px;height:25px" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba\')" %s title="%s"/><span id="%s"></span><br>' % \
                     (rt, obj.checkCompleteNum, obj.id, 'checkCompleteNum', '', obj.checkCompleteNum,
                      str(obj.id) + '_checkCompleteNum',
                      obj.checkInferiorNum, obj.id, 'checkInferiorNum', '', obj.checkInferiorNum,
                      str(obj.id) + '_checkInferiorNum')
                rt = u'%s<strong>质检备注:</strong><input value="%s" type="text" style="width:120px;height:25px" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba\')" %s title="%s"/><span id="%s"></span>' %\
                     (rt, obj.Remarks, obj.id, 'Remarks', '', obj.Remarks,str(obj.id) + '_Remarks')
                rt = '%s<input type="button" style="width:60px;height:25px;margin-left:125px" id="btn1_%s" value="确认">' % (
                    rt, obj.id)
                rt = u'%s<br><p id="result1_%s"  style="color:green;"></p></div>' % (rt, input_id)

                tt = """%s<script>
                            $(document).ready(function() {
                                $('input[type=radio][name=checkOption_%s]').change(function() {
                                    $.ajax({url:"/deal_checkReportData/?dealflag=FBA",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",
                                        data:{"id":"%s","ProductSKU":"%s","checkPart_Num":0,"checkPass_Num":0,"empty":0,"selectCheck":this.value},
                                        success:function(data){if(data.result=="NG"){document.getElementById("result1_%s").innerHTML="处理报错,请联系开发人员解决!";}},
                                        error:function(data){document.getElementById("result1_%s").innerHTML="处理报错,请联系开发人员解决!";}
                                    })
                                })
                                
                                $("#btn1_%s").click(function(){                            
                                        $.ajax({url:"/deal_checkReportData/?dealflag=FBA",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",
                                        data:{"id":"%s","ProductSKU":"%s","checkPart_Num":0,"checkPass_Num":0,"empty":0,"selectCheck":"noselect","checkconfirmflag":"checkconfirmflag"},
                                        success:function(data){if(data.result=="OK"){document.getElementById("result1_%s").innerHTML="已确认!";}
                                                               else if(data.result=="NG"){document.getElementById("result1_%s").innerHTML="确认报错,请检查!";}},
                                        error:function(data){document.getElementById("result1_%s").innerHTML="确认报错,请检查!";}
                                })})
                            });
                            function jisuanPass_%s()
                            {
                                var checkPart_Num = document.getElementById("checkPart_%s").value;
                                var checkPass_Num = document.getElementById("checkPass_%s").value;
                                var empty = 0;
                                if(checkPart_Num == "" & checkPass_Num== "" )
                                {
                                    empty = 99999;
                                }
                                if(checkPart_Num == "")
                                {
                                    checkPart_Num = 0;
                                }
                                if(checkPass_Num == "")
                                {
                                    checkPass_Num = 0;
                                }
                                if(isNaN(checkPart_Num) || isNaN(checkPass_Num))
                                {
                                    document.getElementById("result1_%s").innerHTML="数量输入有误，请修正!";
                                    return;
                                }
                                if(Number(checkPart_Num) < Number(checkPass_Num))
                                {
                                    document.getElementById("result1_%s").innerHTML="抽检数量小于合格数量，请修正!";
                                    return;
                                }
                                $.ajax({url:"/deal_checkReportData/?dealflag=FBA",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",
                                        data:{"id":"%s","ProductSKU":"%s","checkPart_Num":checkPart_Num,"checkPass_Num":checkPass_Num,"empty":empty,"selectCheck":"noselect"},
                                        success:function(data){
                                                                   if(data.result=="OK")
                                                                   {
                                                                        document.getElementById("PercentOfPass_%s").value=data.dataContent+'%s';
                                                                        document.getElementById("result1_%s").innerHTML="计算成功";
                                                                    }
                                                                   else if(data.result=="NG")
                                                                   {
                                                                        document.getElementById("PercentOfPass_%s").value='0'+'%s';
                                                                        document.getElementById("result1_%s").innerHTML="数量输入有误,请检查!";
                                                                    }
                                                                },
                                        error:function(data){document.getElementById("PercentOfPass_%s").value='0'+'%s';document.getElementById("result1_%s").innerHTML="数量输入有误,请检查!";}
                                    })
                            }               
                        </script>"""
                rt = tt % (rt, input_id,input_id, obj.ProductSKU,input_id,input_id,
                           input_id, input_id, obj.ProductSKU, input_id, input_id,input_id,
                           input_id,input_id,input_id,input_id,input_id,input_id, obj.ProductSKU, input_id,'%',input_id, input_id, '%',input_id,input_id,'%',input_id)

            elif obj.Status == 'abnormalcheck':
                Check = "全检"
                if obj.isCheck == 0:
                    Check = "全检"
                elif obj.isCheck == 1:
                    Check = "抽检"
                else:
                    Check = "免检"
                rt = u'<strong>质检选择:</strong>%s<br><strong>抽检数量:</strong>%s<br><strong>合格数量:</strong>%s<br><strong>合格率为:</strong>%s%s' % (
                         Check, CheckNumber, CheckQualified, PercentOfPass, '%')
                rt = u'%s<br><strong>合格总量:</strong><input value="%s" type="text" style="width:120px;height:25px" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba\')" %s title="%s"/><span id="%s"></span><br>' \
                     u'<strong>次品总量:</strong><input value="%s" type="text" style="width:120px;height:25px" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba\')" %s title="%s"/><span id="%s"></span><br>' % \
                     (rt, obj.checkCompleteNum, obj.id, 'checkCompleteNum', '', obj.checkCompleteNum,
                      str(obj.id) + '_checkCompleteNum',
                      obj.checkInferiorNum, obj.id, 'checkInferiorNum', '', obj.checkInferiorNum,
                      str(obj.id) + '_checkInferiorNum')
                rt = u'%s<br><strong>转退数量:</strong><input value="%s" type="text" style="width:120px;height:25px" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba\')" %s title="%s"/><span id="%s"></span> ' % \
                     (rt, obj.tranReturnNum, obj.id, 'tranReturnNum', '', obj.tranReturnNum,
                      str(obj.id) + '_tranReturnNum')
                rt = u'%s<br><strong>质检备注:</strong><input value="%s" type="text" style="width:120px;height:25px" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba\')" %s title="%s"/><span id="%s"></span><br>' % \
                     (rt, obj.Remarks, obj.id, 'Remarks', '', obj.Remarks, str(obj.id) + '_Remarks')
                rt = '%s<input type="button" style="width:60px;height:25px;margin-left:125px" id="btn1_%s" value="确认">' % (rt, obj.id)
                rt = u'%s<br><p id="result1_%s"  style="color:green;"></p></div>' % (rt, input_id)

                tt = """%s<script>
                            $(document).ready(function() {
                                $("#btn1_%s").click(function(){                            
                                        $.ajax({url:"/deal_checkReportData/?dealflag=FBA",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",
                                        data:{"id":"%s","ProductSKU":"%s","checkPart_Num":0,"checkPass_Num":0,"empty":0,"selectCheck":"noselect","checkconfirmflag":"checkconfirmflag"},
                                        success:function(data){if(data.result=="OK"){document.getElementById("result1_%s").innerHTML="已确认!";}
                                                               else if(data.result=="NG"){document.getElementById("result1_%s").innerHTML="确认报错,请检查!";}},
                                        error:function(data){document.getElementById("result1_%s").innerHTML="确认报错,请检查!";}
                                })})
                            });             
                        </script>"""
                rt = tt % (rt,input_id, input_id, obj.ProductSKU, input_id, input_id, input_id,)
            else:
                Check = "全检"
                if obj.isCheck == 0:
                    Check = "全检"
                elif obj.isCheck == 1:
                    Check = "抽检"
                else:
                    Check = "免检"
                rt = u'<strong>质检选择:</strong>%s<br><strong>抽检数量:</strong>%s<br><strong>合格数量:</strong>%s<br><strong>合格率为:</strong>%s%s<br><strong>合格总数量:</strong>%s' \
                     u'<br><strong>次品总数量:</strong>%s' % (
                    Check, CheckNumber, CheckQualified,PercentOfPass,'%',obj.checkCompleteNum,obj.checkInferiorNum)

        except Exception as e:
            messages.info(self.request, u'%s,%s,质检合格率加载数据存在问题题，请联系开发人员。' % (obj.ProductSKU, str(e)))
            rt = ""
        return mark_safe(rt)

    deal_checkData.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">质检信息填写</p>')


    list_display = ('Stocking_plan_number','show_Status','ProductSKU','show_ProductImage','Product_nature',   'show_infors_number', 'show_goodsInfo', 'purchaseNum', 'deal_checkData',
                    'level', 'AccountNum','show_opInfo')
    list_editable = ('Single_number', 'Supplierlink', 'Ali_number', 'Arrival_date','Buyer', 'Logistics_costs', 'LogisticsNumber',
                     'pay_method', 'Prepayments', 'QTY', 'Remarks','OplogTime', 'The_arrival_of_the_number')
    fields = ('Single_number', 'Supplier', 'Ali_number', 'Arrival_date','Buyer', 'QTY', 'Remarks','Supplierlink', 'OplogTime')

    actions = [ 'complete_purchased','abnormal_purchased','abnormal_gen','get_excel_to_py','returnNum','tranNum']

    def complete_purchased(self,request,objs):
        try:
            noConfirmList = []
            abnormallist = []
            errorInfo = []
            for obj in objs:
                if obj.checkConfirmFlag is None or str(obj.checkConfirmFlag) != '1':
                    noConfirmList.append(obj.Stocking_plan_number)
                    continue
                if  obj.Status == 'check' and (((str(obj.isCheck) == '0' or str(obj.isCheck) == '1') and obj.PercentOfPass is not None and obj.PercentOfPass != '') or (str(obj.isCheck) == '2') or obj.isCheck is None):
                    PercentOfPass = obj.PercentOfPass if obj.PercentOfPass is not None else 0
                    if float(PercentOfPass) < 93.0 and (str(obj.isCheck) == '0' or str(obj.isCheck) == '1'):
                        obj.Status = 'abnormalcheck'
                        abnormallist.append(obj.Stocking_plan_number)
                        t_stocking_demand_fba_detail.objects.filter(
                            Stocking_plan_number=obj.Stocking_plan_number).update(
                            Status='abnormalcheck')
                    else:
                        obj.Status = 'genbatch'
                        obj.checkStatus = 'completecheck'
                        t_stocking_demand_fba_detail.objects.filter(
                            Stocking_plan_number=obj.Stocking_plan_number).update(
                            Status='genbatch')
                    obj.CheckMan = request.user.first_name
                    obj.CheckTime = ddtime.now()
                    obj.OplogTime = ddtime.now()
                    obj.save()

                else:
                    errorInfo.append(obj.Stocking_plan_number)
            if errorInfo:
                messages.error(request,u"以下计划号不能做完成质检：%s,质检数据未填写成功,请检查。"%(errorInfo))
            if abnormallist:
                messages.info(request, u"以下计划号质检未达标(低于合格率93%s):%s,流转【质检异常数据】,请手动处理。" % ('%',abnormallist))
            if noConfirmList:
                messages.error(request, u"以下计划号不能做完成质检：%s,请确认后再做提交。" % (noConfirmList))
        except Exception, ex:
            messages.info(self.request,"提交完成质检报错,请联系开发人员解决:%s"%(str(ex)))
    complete_purchased.short_description = u'完成质检'

    def abnormal_purchased(self,request,objs):
        try:
            for obj in objs:
                if  obj.Status == 'check':
                    obj.Status = 'abnormalcheck'
                    obj.CheckMan = request.user.first_name
                    obj.CheckTime = ddtime.now()
                    obj.OplogTime = ddtime.now()
                    obj.save()

                    t_stocking_demand_fba_detail.objects.filter(
                        Stocking_plan_number=obj.Stocking_plan_number).update(
                        Status='abnormalcheck')
        except Exception, ex:
            messages.info(self.request,"提交质检异常数据报错,请联系开发人员解决:%s"%(str(ex)))
    abnormal_purchased.short_description = u'质检异常数据'

    def abnormal_gen(self,request,objs):
        try:
            noConfirmList = []
            for obj in objs:
                if obj.checkConfirmFlag is None or str(obj.checkConfirmFlag) != '1':
                    noConfirmList.append(obj.Stocking_plan_number)
                    continue
                if  obj.Status == 'abnormalcheck':
                    obj.checkStatus = 'completecheck'
                    obj.Status = 'genbatch'
                    obj.CheckMan = request.user.first_name
                    obj.CheckTime = ddtime.now()
                    obj.OplogTime = ddtime.now()
                    obj.save()

                    t_stocking_demand_fba_detail.objects.filter(
                        Stocking_plan_number=obj.Stocking_plan_number).update(
                        Status='genbatch')
            if noConfirmList:
                messages.error(request, u"以下计划号不能做转完成质检：%s,请确认后再做提交。" % (noConfirmList))
        except Exception, ex:
            messages.info(self.request,"提交质检异常数据报错,请联系开发人员解决:%s"%(str(ex)))
    abnormal_gen.short_description = u'转完成质检'

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
            sheet = w.add_sheet(u'质检数据')

            sheetlist = [u'备货计划号',u'商品SKU',u'商品名称',u'到货数量',u'质检数量',u'质检合格数量',u'合格总量',u'质检异常总量',]

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
                sheet.write(row, column, qs.ProductSKU) # sku

                column = column + 1
                sheet.write(row, column, qs.ProductName) # 商品名称

                column = column + 1
                sheet.write(row, column, qs.The_arrival_of_the_number) # 到货数量

                column = column + 1
                sheet.write(row, column, qs.CheckNumber) # 质检数量

                column = column + 1
                sheet.write(row, column, qs.CheckQualified)  # 质检合格数量

                column = column + 1
                sheet.write(row, column, qs.checkCompleteNum)  # 合格总量量

                column = column + 1
                sheet.write(row, column, qs.checkInferiorNum)  # 次品总数量

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

    def returnNum(self, request, objs):
        try:
            errorInfo = []
            returnList=[]
            from skuapp.table.t_stocking_rejecting_fba import t_stocking_rejecting_fba
            for obj in objs:
                if obj.Status == 'abnormalcheck' and obj.Single_number is not None:
                    The_arrival_of_the_number = 0 if obj.The_arrival_of_the_number is None else obj.The_arrival_of_the_number
                    tranReturnNum= 0 if obj.tranReturnNum is None else obj.tranReturnNum
                    if tranReturnNum == The_arrival_of_the_number:
                        obj.Status = 'giveup'
                        obj.giveupMan = request.user.first_name
                        obj.giveupDate = ddtime.now()
                        obj.Remarks = u'转退'
                    else:
                        obj.checkStatus = 'completecheck'
                        obj.Status = 'genbatch'
                        obj.CheckMan = request.user.first_name
                        obj.CheckTime = ddtime.now()
                        obj.Remarks = u'部分转退'

                    RejectNumber = ddtime.now().strftime('%Y%m%d%H%M%S') + '_' + str(i)
                    returnList.append(t_stocking_rejecting_fba(
                        RejectNumber=RejectNumber, RejectDate=ddtime.now(),
                        RejectMan=request.user.first_name,
                        ProductSKU=obj.ProductSKU, ProductImage=obj.ProductImage, ProductName=obj.ProductName,
                        PurchaseOrderNum=obj.Single_number,
                        Status='rejecting', RejectStatus='return', RejectNum=tranReturnNum,
                        Remarks='转退', SummbitRejectMan=request.user.first_name, SummbitRejectDate=ddtime.now(),isCheckTranReturn=1,
                    ))
                    obj.checkCompleteNum = The_arrival_of_the_number-tranReturnNum
                    obj.checkInferiorNum = tranReturnNum
                    obj.OplogTime = ddtime.now()
                    obj.save()

                    t_stocking_demand_fba_detail.objects.filter(
                        Stocking_plan_number=obj.Stocking_plan_number).update(
                        Status='genbatch')
                else:
                    errorInfo.append(obj.Stocking_plan_number)
            t_stocking_rejecting_fba.objects.bulk_create(returnList)
            if len(errorInfo) > 0:
                messages.info(self.request, "以下备货计划号:%s,不能转仓操作。" % (str(errorInfo)))
        except Exception, ex:
            messages.info(self.request,"提交退货报错,请联系开发人员解决:%s"%(str(ex)))
    returnNum.short_description = u'退货->转退管理'

    def tranNum(self, request, objs):
        try:
            errorInfo = []
            returnList = []
            from skuapp.table.t_stocking_rejecting_fba import t_stocking_rejecting_fba
            for obj in objs:
                if obj.Status == 'abnormalcheck' and obj.Single_number is not None:
                    The_arrival_of_the_number = 0 if obj.The_arrival_of_the_number is None else obj.The_arrival_of_the_number
                    tranReturnNum= 0 if obj.tranReturnNum is None else obj.tranReturnNum
                    if tranReturnNum == The_arrival_of_the_number:
                        obj.Status = 'giveup'
                        obj.giveupMan = request.user.first_name
                        obj.giveupDate = ddtime.now()
                        obj.Remarks = u'转退'
                    else:
                        obj.checkStatus = 'completecheck'
                        obj.Status = 'genbatch'
                        obj.tranReturnMan = request.user.first_name
                        obj.tranReturnDate = ddtime.now()
                        obj.Remarks = u'部分转退'

                    RejectNumber = ddtime.now().strftime('%Y%m%d%H%M%S') + '_' + str(i)
                    returnList.append(t_stocking_rejecting_fba(
                        RejectNumber=RejectNumber, RejectDate=ddtime.now(),
                        RejectMan=request.user.first_name,
                        ProductSKU=obj.ProductSKU, ProductImage=obj.ProductImage, ProductName=obj.ProductName,
                        PurchaseOrderNum=obj.Single_number,
                        Status='rejecting', RejectStatus='turn', RejectNum=tranReturnNum,
                        Remarks='转退', SummbitRejectMan=request.user.first_name, SummbitRejectDate=ddtime.now(),isCheckTranReturn=1,
                    ))
                    obj.checkCompleteNum = The_arrival_of_the_number-tranReturnNum
                    obj.checkInferiorNum = tranReturnNum
                    obj.OplogTime = ddtime.now()
                    obj.save()

                    t_stocking_demand_fba_detail.objects.filter(
                        Stocking_plan_number=obj.Stocking_plan_number).update(
                        Status='genbatch')
                else:
                    errorInfo.append(obj.Stocking_plan_number)
            t_stocking_rejecting_fba.objects.bulk_create(returnList)
            if len(errorInfo) > 0:
                messages.info(self.request, "以下备货计划号:%s,不能转仓操作。" % (str(errorInfo)))
        except Exception, ex:
            messages.info(self.request,"提交转仓报错,请联系开发人员解决:%s"%(str(ex)))
    tranNum.short_description = u'转仓->转退管理'

    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_demand_fba_check_Admin, self).get_list_queryset()

        from django.contrib.auth.models import User
        userID = [each.id for each in User.objects.filter(groups__id__in=[65])]
        # if request.user.is_superuser or request.user.id in userID:
        if request.user.id in userID:
            qs = qs.filter(Demand_people=request.user.first_name)

        Status = request.GET.get('Status', '')  # 采购状态
        checkStatus = ''
        if Status == 'completecheck':
            checkStatus='completecheck'
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
        OplogTimeStart = request.GET.get('OplogTimeStart', '')  # 记录生成时间
        OplogTimeEnd = request.GET.get('OplogTimeEnd', '')  # 记录生成时间

        isCheck = request.GET.get('isCheck')  # 质检选择 2全检  1抽检 0免检
        LogisticsNumber = request.GET.get('LogisticsNumber')  # 物流单号
        Single_number = request.GET.get('Single_number')  # 采购单号
        Ali_number = request.GET.get('Ali_number')  # 1688单号
        QTYStart = request.GET.get('QTYStart', '')  # 备货计划时间
        QTYEnd = request.GET.get('QTYEnd', '')  # 备货计划时间
        Stocking_quantityStart = request.GET.get('Stocking_quantityStart', '')  # 备货计划时间
        Stocking_quantityEnd = request.GET.get('Stocking_quantityEnd', '')  # 备货计划时间


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
                        'level__exact':level,'isCheck__exact':isCheck,
                        'Buyer__exact':Buyer,
                        'Status__exact':Status,'checkStatus':checkStatus,
                        'OplogTime__gte':OplogTimeStart,'OplogTime__lt':OplogTimeEnd,
                        'neworold__exact': neworold,
                        'QTYStart': QTYStart, 'QTYEnd': QTYEnd,'LogisticsNumber__exact':LogisticsNumber,
                        'Single_number__exact':Single_number,'Ali_number__exact':Ali_number,
                        'Stocking_quantityStart': Stocking_quantityStart, 'Stocking_quantityEnd': Stocking_quantityEnd,
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

