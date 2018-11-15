# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_no_audit_Admin.py
 @time: 2018/4/28 8:53
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_cloth_factory_dispatch_no_audit import *
from django.contrib import messages
from datetime import datetime
from django.utils.safestring import mark_safe

class t_cloth_factory_dispatch_no_audit_Admin(object):
    t_cloth_factory = True
    search_box_flag = True

    actions = ['to_apply', ]
    t_cloth_factory = True

    def to_apply(self, request, objs):
        from skuapp.table.t_cloth_factory_dispatch_audit import t_cloth_factory_dispatch_audit
        listSKU = []
        for obj in objs:
            if obj.rawNumbers is None or obj.outFactory is None or obj.unit is None or obj.productNumbers is None :
                listSKU.append(obj.SKU)
            else:
                obj.auditMan = ''
                obj.auditDate = None
                obj.applyMan = request.user.first_name
                obj.applyDate = datetime.now()
                obj.currentState = '3'
                obj.save()
        if len(listSKU) > 0:
            messages.info(request, u"商品编码：" + str(listSKU) + u";中涉及的原材料数量、产出件数、外派工厂或原材料单位字段 未填写，请填写完整后再提交。")

    to_apply.short_description = u'未通过排单-重新提交审核'

    def show_Picture(self,obj) :
       # self.update_status(obj)
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(obj.BmpUrl,obj.BmpUrl,obj.BmpUrl)
        return mark_safe(rt)
    show_Picture.short_description = u'图片'

    def show_rawNumbers(self, obj):
        input_id = str(obj.id)
        show_input_res = input_id
        if obj.rawNumbers is None:
            rawNumbers = ''
        else:
            rawNumbers = str(obj.rawNumbers)

        if obj.productNumbers is None:
            productNumbers = ''
        else:
            productNumbers = str(obj.productNumbers)

        strSelect1 = ""
        strSelect2 = ""
        strSelect3 = ""

        if obj.unit is None or obj.unit == u"":
            strSelect1 = "selected"
        elif obj.unit == u"条":
            strSelect2 = "selected"
        else:
            strSelect3 = "selected"
        #messages.info(self.request, str(obj.unit) + "strSelect1:" + strSelect1 + ",strSelect2:" + strSelect2 + ",strSelect3:" + strSelect3)
        rt = u'原料数量:<input type="text" style="width:80px" id="cg_%s" value="%s" />' \
             u'<script>$(document).ready(function(){$("#cg_%s").blur(function(){var newnumber = $("#cg_%s").val();' \
             u'if(newnumber!=""){$.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
             u'dataType: "json",data:{"rawNumbers":newnumber,"unit":"kong01","productNumbers":999999,"SKU":"%s","id":"%s"},' \
             u'success:function(data, textStatus, jqXHR){if(data == "1"){document.getElementById("cg_%s").text="success";}},' \
             u'error:function(jqXHR, textStatus, errorThrown){ alert("failed")}});}}); ' \
             u'var cgcheck =  document.getElementById("cg_%s");  if (cgcheck.checked){document.getElementById("cg_%s").readOnly=true; }' \
             u'else{document.getElementById("cg_%s").readOnly=false;}}); </script>' % (
             input_id, rawNumbers, input_id, input_id, obj.SKU, input_id, input_id, input_id, input_id, input_id)

        rt = rt + u'单位:' \
                u'<select id="sel_%s" style="width:50px">' \
                  u'<option value ="kong" %s >---</option>' \
                  u'<option value ="tiao" %s>条</option>' \
                  u'<option value ="mi"  %s>米</option>' \
                  u'</select>'\
                  u'<script>  $(document).ready(function(){$("#sel_%s").blur(function(){var selData = $("#sel_%s").val();' \
                 u'if(selData!=""){$.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
                 u'dataType: "json",data:{"rawNumbers":999999,"unit":selData,"productNumbers":999999,"SKU":"%s","id":"%s"},' \
                 u'success:function(data, textStatus, jqXHR){if(data == "1"){document.getElementById("sel_%s").text="success";}},' \
                 u'error:function(jqXHR, textStatus, errorThrown){ alert("failed")}});}}); ' \
                 u'var cgcheck =  document.getElementById("sel_%s");  if (cgcheck.checked){document.getElementById("sel_%s").readOnly=true; }' \
                 u'else{document.getElementById("sel_%s").readOnly=false;}}); </script>' % (
            input_id,strSelect1,strSelect2,strSelect3,input_id,input_id,obj.SKU,input_id,input_id,input_id,input_id,input_id)
        rt = rt + u'<br><br>产出件数:' \
                  u'<input type="text" style="width:180px" id="productNumbers_%s" value="%s" />' \
                  u'<script>$(document).ready(function(){$("#productNumbers_%s").blur(function(){var productNumbers = $("#productNumbers_%s").val();' \
             u'if(productNumbers!=""){$.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
             u'dataType: "json",data:{"rawNumbers":999999,"unit":"kong01","productNumbers":productNumbers,"SKU":"%s","id":"%s"},' \
             u'success:function(data, textStatus, jqXHR){if(data == "1"){document.getElementById("productNumbers_%s").text="success";}},' \
             u'error:function(jqXHR, textStatus, errorThrown){ alert("failed")}});}}); ' \
             u'var cgcheck =  document.getElementById("productNumbers_%s");  if (cgcheck.checked){document.getElementById("productNumbers_%s").readOnly=true; }' \
             u'else{document.getElementById("productNumbers_%s").readOnly=false;}}); </script>' % (
             input_id, productNumbers, input_id, input_id, obj.SKU, input_id, input_id, input_id, input_id, input_id)

        rt = rt + u'<br>采购备注:' \
                  u'<input type="text" style="width:180px;height:50px" id="remarkApply_%s" value="%s" />' \
                  u'<script>$(document).ready(function(){$("#remarkApply_%s").blur(function(){var remarkApply = $("#remarkApply_%s").val();' \
                  u'if(remarkApply!=""){$.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
                  u'dataType: "json",data:{"rawNumbers":999999,"unit":"kong01","productNumbers":999999,"remarkApply":remarkApply,"SKU":"%s","id":"%s"},' \
                  u'success:function(data, textStatus, jqXHR){if(data == "1"){document.getElementById("remarkApply_%s").text="success";}},' \
                  u'error:function(jqXHR, textStatus, errorThrown){ alert("failed")}});}}); ' \
                  u'var cgcheck =  document.getElementById("remarkApply_%s");  if (cgcheck.checked){document.getElementById("remarkApply_%s").readOnly=true; }' \
                  u'else{document.getElementById("remarkApply_%s").readOnly=false;}}); </script>' % (
                 input_id, obj.remarkApply, input_id, input_id, obj.SKU, input_id, input_id, input_id, input_id,
                 input_id)
        return mark_safe(rt)

    show_rawNumbers.short_description = mark_safe('<p style="width:250px;color:#428bca;">原材料数量\单位\产出件数\备注</p>')

    list_per_page = 20

    list_display = (
    'id', 'show_Picture', 'SKU', 'goodsName', 'goodsstate', 'OSCode','Supplier', 'buyer', 'SalerName2',
    'sevenSales', 'goodsCostPrice', 'ailableNum', 'PurchaseNotInNum',
    'oosNum','goodsclass','TortInfo', 'show_rawNumbers', 'outFactory','remarkDisPatch',)
    list_editable = ( 'outFactory', )

    fields = (
        'SKU', 'goodsName', 'Supplier', 'goodsstate', 'goodsCostPrice', 'oosNum', 'stockNum', 'ailableNum',
        'sevenSales', 'fifteenSales',
        'thirtySales', 'PurchaseNotInNum', 'buyer', 'productNumbers', 'loanMoney',
        'actualMoney', 'outFactory', 'rawNumbers', 'unit',
        'remarkApply','remarkApply','remarkAudit',)


    # 判断主SKU是否合法
    def is_valid(self, request, obj):
        # 主SKU不存在
        if obj.SKU is None or obj.SKU.strip() == '':
            messages.error(request, u'错误:SKU(%s)为空!!!' % obj.SKU)
            return False

        # 包装规格
        if obj.girard is None or obj.girard.strip() == '':
            messages.error(request, u'款号必填!!!')
            return False

    def get_list_queryset(self):
        request = self.request
        qs = super(t_cloth_factory_dispatch_no_audit_Admin, self).get_list_queryset()
        SKU = request.GET.get('SKU', '')

        Supplier = request.GET.get('Supplier', '')
        buyer = request.GET.get('buyer', '')
        buyer = buyer.split(',')
        if '' in buyer:
            buyer = ''
        oosNumStart = request.GET.get('oosNum_Start', '')
        oosNumEnd = request.GET.get('oosNum_End', '')

        searchList = {'SKU__contains': SKU,
                      'Supplier__contains': Supplier,
                      'buyer__in': buyer,
                      'oosNum__gte': oosNumStart,
                      'oosNum__lt': oosNumEnd,
                      }

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    # v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs.filter(currentState = 1)


