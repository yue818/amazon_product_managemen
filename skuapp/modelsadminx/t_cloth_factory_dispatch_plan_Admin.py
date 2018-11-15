# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_plan_Admin.py
 @time: 2018/4/28 8:53
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_cloth_factory_dispatch_plan import t_cloth_factory_dispatch_plan
from datetime import datetime
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.db.models import Q

class t_cloth_factory_dispatch_plan_Admin(object):
    actions = ['to_applyPaid','show_auditInfo',  ]
    search_box_flag = True
    t_cloth_factory = True
    '''
    def updateApplyInfo(self, obj):
        rt = ''
        from skuapp.table.t_cloth_factory_dispatch_audit import t_cloth_factory_dispatch_audit
        t_cloth_factory_dispatch_audit_objs = t_cloth_factory_dispatch_audit.objects.filter(SKU=obj.SKU,
                                                                                                currentState='2')
        from skuapp.table.t_cloth_factory_dispatch_no_audit import t_cloth_factory_dispatch_no_audit
        t_cloth_factory_dispatch_no_audit_objs = t_cloth_factory_dispatch_no_audit.objects.filter(SKU=obj.SKU,
                                                                                            currentState='1')
        if t_cloth_factory_dispatch_audit_objs.count() != 0:
            rt = u"<font color:#3C3C3C>已申请</font> \t\t<a href='/Project/admin/skuapp/t_cloth_factory_dispatch_audit'>跳转至审核</a>"
            return mark_safe(rt)
        elif t_cloth_factory_dispatch_no_audit_objs.count() != 0:
            rt = u"<font color:#3C3C3C>已申请</font> \t\t<a href='/Project/admin/skuapp/t_cloth_factory_dispatch_no_audit'>跳转至审核未通过</a>"
            return mark_safe(rt)
        else:
            rt = u"<a id=update_applyInfo%s>新增派单信息</a><script>$('#update_applyInfo%s').on('click',function(){layer.open(" \
                 u"{type:2,skin:'layui-layer-lan',title:'申请编辑',fix:false,shadeClose: true,maxmin:true," \
                 u"area:['1200px','800px'],content:'/t_cloth_factor_eidt/update_applyInfo/?sku=%s',end: function(){ location.reload(); }});});</script>" % (
                obj.id, obj.id, obj.SKU)

        return mark_safe(rt)

    updateApplyInfo.short_description = mark_safe(u'<p style="width:160px;color:#428bca;" align="center">申请编辑信息</p>')
    '''

    def to_applyPaid(self, request, objs):
        try:
            listSKU = []
            listFactory = []
            for obj in objs:
                t_cloth_factory_dispatch_plan_objs = t_cloth_factory_dispatch_plan.objects.filter(id=obj.id,SKU=obj.SKU).values('productNumbers','outFactory')
                if t_cloth_factory_dispatch_plan_objs[0]['productNumbers'] is None or t_cloth_factory_dispatch_plan_objs[0]['productNumbers'] == "" or str(t_cloth_factory_dispatch_plan_objs[0]['productNumbers']) == "0":
                    listSKU.append(obj.SKU)
                elif t_cloth_factory_dispatch_plan_objs[0]['outFactory'] is None or t_cloth_factory_dispatch_plan_objs[0]['outFactory'] == "":
                    listFactory.append(obj.SKU)
                else:
                    obj.currentState = '8'
                    obj.applyMan = request.user.first_name
                    obj.applyDate = datetime.now()
                    obj.save()
            if len(listSKU) > 0:
                messages.info(request,u"商品编码：" + str(listSKU) + u";中采购SKU数量 未填写，请填写后再提交-采购计划审核。")
            if len(listFactory) > 0:
                messages.info(request,u"商品编码：" + str(listFactory) + u";中排单SKU外派工厂未选择，请填写后再提交-采购计划审核。")
        except Exception as e:
            messages.info(self.request, u'%s,%s,提交审核报错，请联系开发人员。' % (obj.SKU,str(e)))
    to_applyPaid.short_description = u"提交-采购计划审核"

    def ossNum(self, obj):
        rt = ""
        if obj.oosNum > 0:
            rt = u"<font size='4' color='red'>%s</font>"%(obj.oosNum)
        else:
            rt = u"<font size='4' color='red'>0</font>"
        return mark_safe(rt)
    ossNum.short_description = mark_safe(u'<p style="width:100px;color:#428bca;" align="center">缺货及未派单量</p>')

    def GoodsOther(self,obj):
        rt = u'<p style="width:120px;"><strong>商品成本价:</strong>%s <br><strong>7天销量:</strong>%s <br><strong>预计库存量:</strong>%s<br><strong>采购未入库量:</strong>%s</p>' % (obj.goodsCostPrice,obj.sevenSales,obj.ailableNum,obj.PurchaseNotInNum)
        if obj.SpecialPurchaseFlag is not None and obj.SpecialPurchaseFlag != '':
            if obj.SpecialPurchaseFlag == 'firstorder':
                rt = rt + u'<br><strong>注:手动新增-网采转供应链排单(首单)</strong>'
            elif obj.SpecialPurchaseFlag == 'customermade':
                rt = rt + u'<br><strong>注:手动新增-客户定做</strong>'
            elif obj.SpecialPurchaseFlag == 'other':
                rt = rt + u'<br><strong>注:手动新增-浦江仓库</strong>'
        elif obj.OSCode == 'OS906' and obj.Stocking_plan_number is not None and obj.Stocking_plan_number != '':
            rt = rt + u'<br><strong>注:海外仓备货转服装排单</strong>'
        else:
            rt = rt + u'<br><strong>注:系统自动生成采购</strong>'
        return mark_safe(rt)
    GoodsOther.short_description = mark_safe(u'<p style="width:120px;color:#428bca;" align="center">商品其他信息</p>')

    def GoodsInfo(self,obj):
        rt = u'<p style="width:200px;"><strong>商品名称:</strong>%s <br><strong>供应商名:</strong>%s <br><strong>商品状态:</strong>%s<br><strong>商品类别:</strong>%s<br><strong>侵权站点:</strong>%s<br><strong>上一步处理人员:</strong>%s<br><strong>上一步处理时间:</strong>%s</p>' % (obj.goodsName,obj.Supplier, obj.goodsState,obj.goodsclass,obj.TortInfo,obj.genPurchaseMan,obj.genPurchaseDate)
        return mark_safe(rt)
    GoodsInfo.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">商品及流程信息</p>')

    def show_Picture(self,obj) :
        # self.update_status(obj)
        from Project.settings import BmpUrl
        # 获取图片的url
        picture_url = obj.BmpUrl  # 获取图片的url
        sku = obj.SKU  # 获取商品SKU
        if not picture_url:
            picture_url = BmpUrl + sku + '.jpg'

        rt = """<img src="%s"  width="120" height="120"  title="%s" onerror="this.title=''" />  """ % (picture_url, picture_url)
        return mark_safe(rt)
    show_Picture.short_description = mark_safe(u'<p style="width:120px;color:#428bca;" align="center">图片</p>')

    def show_SKUNumbers(self, obj):
        try:
            input_id = str(obj.id)
            if obj.productNumbers is None:
                productNumbers = '0'
            else:
                productNumbers = str(obj.productNumbers)

            if obj.remarkApply is None:
                remarkApply = ''
            else:
                remarkApply = str(obj.remarkApply)
            if obj.rawNumbers is None:
                rawNumbers = '0'
            else:
                rawNumbers = str(obj.rawNumbers)
            strSelect1 = ""
            strSelect2 = ""
            strSelect3 = ""
            if obj.unit is None or obj.unit == u"":
                strSelect1 = "selected"
            elif obj.unit == u"条":
                strSelect2 = "selected"
            else:
                strSelect3 = "selected"
            # rt = u'采购数量:' \
            #           u'<input type="text" style="width:180px" id="productNumbers_%s" value="%s" />' \
            #           u'<script>$(document).ready(function(){$("#productNumbers_%s").blur(function(){var productNumbers = $("#productNumbers_%s").val();' \
            #      u'if(productNumbers!=""){$.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
            #      u'dataType: "json",data:{"rawNumbers":999999,"unit":"kong01","productNumbers":productNumbers,"remarkApply":"noremarkapply","remarkSpeModify":"noremarkSpeModify","SKU":"%s","id":"%s"},' \
            #      u'success:function(data, textStatus, jqXHR){if(data == "1"){document.getElementById("productNumbers_%s").text="success";}},' \
            #      u'error:function(jqXHR, textStatus, errorThrown){ alert("failed")}});}}); ' \
            #      u'var cgcheck =  document.getElementById("productNumbers_%s");  if (cgcheck.checked){document.getElementById("productNumbers_%s").readOnly=true; }' \
            #      u'else{document.getElementById("productNumbers_%s").readOnly=false;}}); </script>' % (
            #      input_id, productNumbers, input_id, input_id, obj.SKU, input_id, input_id, input_id, input_id, input_id)
            # rt = rt + u'<br>采购备注:' \
            #           u'<input type="text" style="width:180px;height:70px" id="remarkApply_%s" value="%s" />' \
            #           u'<script>$(document).ready(function(){$("#remarkApply_%s").blur(function(){var remarkApply = $("#remarkApply_%s").val();' \
            #           u'if(remarkApply!=""){$.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
            #           u'dataType: "json",data:{"rawNumbers":999999,"unit":"kong01","productNumbers":999999,"remarkApply":remarkApply,"remarkSpeModify":"noremarkSpeModify","SKU":"%s","id":"%s"},' \
            #           u'success:function(data, textStatus, jqXHR){if(data == "1"){document.getElementById("remarkApply_%s").text="success";}},' \
            #           u'error:function(jqXHR, textStatus, errorThrown){ alert("failed")}});}}); ' \
            #           u'var cgcheck =  document.getElementById("remarkApply_%s");  if (cgcheck.checked){document.getElementById("remarkApply_%s").readOnly=true; }' \
            #           u'else{document.getElementById("remarkApply_%s").readOnly=false;}}); </script>' % (
            #          input_id, obj.remarkApply, input_id, input_id, obj.SKU, input_id, input_id, input_id, input_id,
            #          input_id)

            rt = '<div id = "planPurchase_%s">' % (input_id,)
            rt = u'%s采购数量:<input type="text" style="width:200px;height:35px" id="productNumbers_%s" value="%s" /><br>' \
                 u'原料数量:<input type="text" style="width:110px;height:35px" id="rawNum_%s" value="%s" />' \
                 u' 单位:'\
                 u'<select id="sel_%s" style="width:50px;height:35px">' \
                 u'<option value ="kong" %s >---</option>' \
                 u'<option value ="条" %s>条</option>' \
                 u'<option value ="米" %s>米</option>' \
                 u'</select>' \
                 u'<br>采购备注:<input type="text" style="width:200px;height:60px" id="remarkApply_%s" value="%s" /><br>' \
                 u'<input type="button" style="width:50px;margin-left:215px" id="btn_%s" value="录入">' \
                 u'<p id="result_%s"  style="color:green;"></p></div>' % (
                 rt, input_id, productNumbers, input_id, rawNumbers, input_id,strSelect1,strSelect2,strSelect3, input_id,remarkApply, input_id,input_id)

            tt = """%s<script>                        
                            $(document).ready(function(){
                                var cgcheck =  document.getElementById("sel_%s");  
                                if (cgcheck.checked){
                                    document.getElementById("sel_%s").readOnly=true; 
                                }
                                else{
                                    document.getElementById("sel_%s").readOnly=false;
                                }
                                $("#btn_%s").click(function(){
                                    var productNumbers_Num = document.getElementById("productNumbers_%s").value;
                                    var rawNum_Num = document.getElementById("rawNum_%s").value;
                                    var selData = $("#sel_%s").val();
                                    var remarkApply = document.getElementById("remarkApply_%s").value;
                                    var remarkAudit = "";
                                    $.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",
                                    data:{"id":"%s","SKU":"%s","productNumbers_Num":productNumbers_Num,"rawNum_Num":rawNum_Num,"selData":selData,"remarkApply":remarkApply,"remarkAudit":remarkAudit,'completeNumber':"111229999"},
                                    success:function(data){if(data.result=="OK"){document.getElementById("result_%s").innerHTML="录入成功!";}
                                                           else if(data.result=="NG"){document.getElementById("result_%s").innerHTML="录入失败(采购数量=0或其他数据存在问题),请检查!";}},
                                    error:function(data){document.getElementById("result_%s").innerHTML="录入失败(采购数量=0或其他数据存在问题),请检查!";}
                                })})
                            })</script>"""
            rt = tt % (rt, input_id,input_id,input_id,input_id, input_id, input_id, input_id, input_id,input_id, obj.SKU, input_id,input_id, input_id)

            if obj.currentState == '6':
                if obj.remarkAudit is not None and obj.remarkAudit != '':
                    rt = rt + u"<br><font color='red'>审核未通过:%s</font>"%(obj.remarkAudit)
                else:
                    rt = rt +  u"<br><font color='red'>审核未通过,待修改后重新提交审核</font>"
        except Exception as e:
            messages.info(self.request, u'%s,%s,加在数据存在问题，请联系开发人员。' % (obj.SKU,str(e)))
            rt = ""
        return mark_safe(rt)

    show_SKUNumbers.short_description = mark_safe('<p align="center" style="width:250px;color:#428bca;">采购数据录入</p>')

    list_per_page = 20
    list_display = ('SKU','show_Picture', 'buyer','SalerName2', 'OSCode','GoodsInfo', 'GoodsOther',
     'ossNum','SuggestNum','SaleDay','show_SKUNumbers','outFactory',)
    list_editable = ('outFactory',)

    fields = (
    'SKU', 'goodsName', 'Supplier', 'goodsState', 'goodsCostPrice', 'oosNum', 'stockNum', 'ailableNum',
    'sevenSales', 'fifteenSales',
    'thirtySales', 'PurchaseNotInNum', 'buyer',  'productNumbers', 'loanMoney',
    'actualMoney', 'outFactory', 'unit','rawNumbers',
    'remarkApply','productNumbers',)


    def get_list_queryset(self):
        request = self.request
        qs = super(t_cloth_factory_dispatch_plan_Admin, self).get_list_queryset()

        #PurchaseNotInNum = request.GET.get('PurchaseNotInNum', '')
        SKU = request.GET.get('SKU', '')

        Supplier = request.GET.get('Supplier', '')
        buyer = request.GET.get('buyer', '')
        buyer = buyer.split(',')
        if '' in buyer:
            buyer = ''
        oosNumStart = request.GET.get('oosNum_Start', '')
        oosNumEnd = request.GET.get('oosNum_End', '')

        goodsState = request.GET.get('goodsState', '')
        from skuapp.table.goodsstatus_compare import goodsstatus_compare
        goodsstatus_compare_objs = goodsstatus_compare.objects.filter(py_GoodsStatus=goodsState).values_list(
            "hq_GoodsStatus", flat=True)

        searchList = {'SKU__contains': SKU,
                      'Supplier':Supplier,
                      'buyer__in': buyer,
                      'oosNum__gte': oosNumStart,
                      'oosNum__lt': oosNumEnd,
                      'goodsState__in':list(goodsstatus_compare_objs),
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v

        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        from django.contrib.auth.models import User
        userID = [each.id for each in User.objects.filter(groups__id__in=[48])]
        if request.user.is_superuser or request.user.id in userID:
            return qs.filter(Q(currentState = 4)|Q(currentState = 6))
        buyer = request.user.first_name
        return qs.filter(Q(currentState = 4)|Q(currentState = 6),buyer=buyer)
        #qs.filter(Q(CategoryCode=u'001.时尚女装') | Q(CategoryCode=u'002.时尚男装')| Q(CategoryCode=u'025.内衣')| Q(CategoryCode=u'021.泳装')| Q(CategoryCode=u'024.儿童服装')).filter(GoodsStatus='normal')
        #return qs.filter(Q(currentState = 4)|Q(currentState = 6))

