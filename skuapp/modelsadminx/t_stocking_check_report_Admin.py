# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_check_report_Admin.py
 @time: 2018-07-31 14:47

"""
from django.contrib import messages
from django.utils.safestring import mark_safe
from datetime import datetime as ddtime

class t_stocking_check_report_Admin(object):
    search_box_flag = True
    check_report_plugin = True
    site_left_menu_stocking_purchase = True
    def show_ProductImage(self,obj) :
        rt =  '<img src="%s"  width="120" height="120"/>  '%(obj.ProductImage)
        return mark_safe(rt)
    show_ProductImage.short_description = u'商品图片'

    def deal_checkData(self,obj) :
        try:
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
                allCheck="checked='checked'"
            elif obj.isCheck == 1:
                partCheck="checked='checked'"
            else:
                noCheck = "checked='checked'"
            rt = '<div id = "checkPurchase_%s">' % (input_id)
            rt = u'%s质检选择:<input name="checkOption_%s" type="radio" %s value="2" />免检&nbsp' \
                 u'<input name="checkOption_%s" type="radio" %s  value="1" />抽检&nbsp' \
                 u'<input name="checkOption_%s" type="radio" %s  value="0" />全检<br><br>' \
                 u'抽检数量:<input name="checkPart_%s" type="text" style="width:150px;height:35px" id="checkPart_%s" value="%s" onkeyup="jisuanPass_%s()"/><br>' \
                 u'合格数量:<input type="text" style="width:150px;height:35px" id="checkPass_%s" value="%s" onkeyup="jisuanPass_%s()"/><br>' \
                 u'合格率为:<input type="text" readonly= "true" style="width:150px;height:35px;" id="PercentOfPass_%s" value="%s%s" /><br>'\
                 %(rt, input_id,noCheck,input_id,partCheck,input_id,allCheck,input_id,input_id, CheckNumber,input_id, input_id,CheckQualified,input_id,input_id, PercentOfPass,'%')

            rt = u'%s<br><p id="result1_%s"  style="color:green;"></p></div>' % (rt, input_id)

            tt = """%s<script>
                        $(document).ready(function() {
                            $('input[type=radio][name=checkOption_%s]').change(function() {
                                $.ajax({url:"/deal_checkReportData/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",
                                    data:{"id":"%s","ProductSKU":"%s","checkPart_Num":0,"checkPass_Num":0,"empty":0,"selectCheck":this.value},
                                    success:function(data){if(data.result=="NG"){document.getElementById("result1_%s").innerHTML="处理报错,请联系开发人员解决!";}},
                                    error:function(data){document.getElementById("result1_%s").innerHTML="处理报错,请联系开发人员解决!";}
                                })
                            })
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
                            $.ajax({url:"/deal_checkReportData/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",
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
                       input_id,input_id,input_id,input_id,input_id,input_id, obj.ProductSKU, input_id,'%',input_id, input_id, '%',input_id,input_id,'%',input_id)
        except Exception as e:
            messages.info(self.request, u'%s,%s,加在数据存在问题题，请联系开发人员。' % (obj.ProductSKU, str(e)))
            rt = ""
        return mark_safe(rt)

    deal_checkData.short_description = u'质检合格率'

    list_per_page = 20
    list_display = ('ProductSKU','Purchaser','SalerName2','Demand_people','Purchase_Order_No','Purchase_date','ProductName','show_ProductImage','ProductPrice','ProductWeight','PurchaseNumber','ArrivalNumber','deal_checkData','Remark')
    list_editable = ('Remark')
    #list_filter = ('ProductSKU')
    actions = ['no_check']

    def no_check(self,request,objs):
        for obj in objs:
            obj.isCheck = 2 # 不需要抽检
            obj.CheckMan = request.user.first_name
            obj.CheckTime=ddtime.now()
            obj.save()
    no_check.short_description = u'免检'

        
    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_check_report_Admin, self).get_list_queryset()
        productsku = request.GET.get('productsku', '')  # 记录生成时间
        productname = request.GET.get('productname', '')  # 记录生成时间
        Purchase_Order_No = request.GET.get('Purchase_Order_No', '')  # 记录生成时间
        isCheck = request.GET.get('isCheck', '')  # 记录生成时间
        Purchase_dateStart = request.GET.get('Purchase_dateStart', '')  # 入库时间
        Purchase_dateEnd = request.GET.get('Purchase_dateEnd', '')  # 入库时间
        SalerName2 = request.GET.get('SalerName2', '')  # 记录生成时间
        Purchaser = request.GET.get('Purchaser', '')  # 记录生成时间
        isFBA = request.GET.get('isFBA', '')  # 记录生成时间
        Demand_people = request.GET.get('Demand_people', '')  # 记录生成时间

        searchList = {
                        'ProductSKU__icontains':productsku,
                        'ProductName__contains':productname,
                        'Purchase_Order_No__exact':Purchase_Order_No,
                        'SalerName2__exact': SalerName2,'Purchaser__exact': Purchaser,
                        'isCheck__exact':isCheck,'Demand_people__exact':Demand_people,
                        'Purchase_date__gte': Purchase_dateStart, 'Purchase_date__lt': Purchase_dateEnd,
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
        if isFBA == '1':
            qs = qs.filter(isFBA__contains="FBA")
        elif isFBA == '0':
            qs = qs.exclude(isFBA__contains="FBA")
        return  qs.order_by("-Purchase_date")

