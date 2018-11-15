# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_paid_audit_Admin.py
 @time: 2018/4/28 8:53
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.contrib import messages
from datetime import datetime as paidDate
from django.utils.safestring import mark_safe
from skuapp.table.t_cloth_factory_dispatch_paid_audit import t_cloth_factory_dispatch_paid_audit
import os
from Project.settings import *
import oss2
from xlwt import *
from .t_product_Admin import *

class t_cloth_factory_dispatch_paid_audit_Admin(object):
    search_box_flag = True
    t_cloth_factory = True
    downloadxls = True
    actions = ['to_audit','to_no_audit',]

    def setSheetHead(self,sheet):
        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.bottom_colour = 0x3A
        style = XFStyle()
        style1 = XFStyle()
        #sheet.write(0, 0, u'下单日式')
        fnt = Font()  # 创建一个文本格式，包括字体、字号和颜色样式特性
        fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
        fnt.bold = True
        style.font = fnt
        style1.borders = borders
        style.borders = borders
        sheet.write_merge(0, 1, 0, 2, u'下单日期：',style)
        sheet.write_merge(0, 1, 3, 11, u'                                                  面辅料报账单',style)
        sheet.write_merge(0, 1, 12, 14, u'采购员：\n',style)

        sheet.write_merge(2, 3,0,0, u'款号',style1)
        sheet.write_merge(2, 3,1,1 ,u'颜色',style1)
        sheet.write_merge(2, 2,2,9, u'                                                         尺码件数',style1)
        sheet.write(3, 2, u'XS',style1)
        sheet.write(3, 3, u'S', style1)
        sheet.write(3, 4, u'M',style1)
        sheet.write(3, 5, u'L',style1)
        sheet.write(3, 6, u'XL',style1)
        sheet.write(3, 7, u'2XL',style1)
        sheet.write(3, 8, u'3XL',style1)
        sheet.write(3, 9, u'4XL',style1)
        sheet.write_merge(2, 3,10,10, u'借款金额',style1)
        sheet.write_merge(2, 3,11,11, u'实际金额',style1)
        sheet.write_merge(2, 3,12,12, u'外发工厂',style1)
        sheet.write_merge(2, 3,13,13, u'条数',style1)
        sheet.write_merge(2, 3,14,14, u'备注',style1)
        #sheet.write(2, 9, u'下单时间')
        #sheet.write(2, 10, u'采购员')

    def setSheetTail(self,row,sheet,totalLoanMoney,totalActualMoney):
        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.bottom_colour = 0x3A

        style = XFStyle()
        fnt = Font()  # 创建一个文本格式，包括字体、字号和颜色样式特性
        fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
        fnt.bold = True
        style.font = fnt
        style.borders = borders
        nAddRow = row
        for i in range(nAddRow+1,nAddRow+10):
            for j in range(0,15):
                sheet.write(i,j,u'',style)

        sheet.write_merge(nAddRow+10, nAddRow+10, 0, 9, u'                                                                         辅料', style)
        sheet.write(nAddRow+10, 10,u'',style)
        sheet.write(nAddRow + 10, 11, u'', style)
        sheet.write(nAddRow + 10, 12, u'', style)
        sheet.write(nAddRow + 10, 13, u'', style)
        sheet.write(nAddRow + 10, 14, u'', style)

        for i in range(nAddRow+11,nAddRow+15):
            for j in range(0,15):
                sheet.write(i,j,u'',style)

        sheet.write_merge(nAddRow + 15,nAddRow + 16,0,0, u'车费',style)
        sheet.write_merge(nAddRow + 15, nAddRow + 16,1,4, u'',style)
        sheet.write_merge(nAddRow + 15,nAddRow + 15,5,9, u'合计借款金额',style)
        sheet.write(nAddRow + 15, 10, totalLoanMoney,style)
        sheet.write_merge(nAddRow + 16,nAddRow + 16,5,9, u'合计实际金额',style)
        sheet.write(nAddRow + 16, 10, totalActualMoney,style)
        sheet.write(nAddRow + 15, 11, u'', style)
        sheet.write(nAddRow + 16, 11, u'', style)
        sheet.write(nAddRow + 15, 12, u'', style)
        sheet.write(nAddRow + 16, 12, u'', style)
        sheet.write(nAddRow + 15, 13, u'', style)
        sheet.write(nAddRow + 16, 13, u'', style)
        sheet.write(nAddRow + 15, 14, u'', style)
        sheet.write(nAddRow + 16, 14, u'', style)
        sheet.write_merge(nAddRow + 17, nAddRow + 17, 0, 11, u'报账日期:', style)
        sheet.write_merge(nAddRow + 17, nAddRow + 17, 12, 14, u'报账签字:', style)

    def to_audit(self, request, objs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
        # 写入execl
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        # if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))
        w = Workbook()
        row = 0
        sheet = w.add_sheet('SKU')
        # self.setSheetHead(sheet)

        totalLoanMoney = 0.0
        totalActualMoney = 0.0

        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.bottom_colour = 0x3A

        style = XFStyle()
        style.borders = borders

        sheet.write(0, 0, u'款号', style)  # 款号
        sheet.write(0, 1, u'采购数量', style)  # 建议采购数量
        sheet.write(0, 2, u'原材数量', style)  # 建议采购数量
        sheet.write(0, 3, u'原材单位', style)  # 建议采购数量
        sheet.write(0, 4, u'外发工厂', style)  # 外发工厂
        sheet.write(0, 5, u'采购人', style)  # 采购人
        sheet.write(0, 6, u'审核人', style)  # 审核人
        sheet.write(0, 7, u'备注', style)  # 备注

        listSKU = []
        for obj in objs:
            t_cloth_factory_dispatch_plan_objs = t_cloth_factory_dispatch_paid_audit.objects.filter(id=obj.id,SKU=obj.SKU).values(
                'rawNumbers','unit','outFactory')
            if  t_cloth_factory_dispatch_plan_objs[0]['outFactory'] is None or\
                t_cloth_factory_dispatch_plan_objs[0]['outFactory'] is None:
                listSKU.append(obj.SKU)
            else:
                row = row + 1
                sheet.write(row, 0, obj.SKU, style)  # 款号
                sheet.write(row, 1, obj.productNumbers, style)  # 建议采购数量
                sheet.write(row, 2, obj.rawNumbers, style)  # 建议采购数量
                sheet.write(row, 3, obj.unit, style)  # 建议采购数量
                sheet.write(row, 4, obj.outFactory, style)  # 外发工厂
                sheet.write(row, 5, obj.buyer, style)  # 采购人
                sheet.write(row, 6, obj.auditMan, style)  # 审核人
                sheet.write(row, 7, obj.remarkApply, style)  # 备注


                obj.currentState = '20'
                obj.dispatchMan = request.user.first_name
                obj.disPatchDate = paidDate.now()
                obj.save()

        if len(listSKU) > 0:
            messages.info(request, u"商品编码：" + str(listSKU) + u";中排单SKU外派工厂未选择，请填写后再提交-排单生产。")

        filename = request.user.username + '_' + paidDate.now().strftime('%Y%m%d%H%M%S') + '.xls'
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
    to_audit.short_description = u'提交-排单生产/导出execl'

    def to_no_audit(self, request, objs):
        for obj in objs:
            t_cloth_factory_dispatch_audit_obj = t_cloth_factory_dispatch_paid_audit()
            t_cloth_factory_dispatch_audit_obj.__dict__ = obj.__dict__
            obj.dispatchMan = request.user.first_name
            obj.disPatchDate = paidDate.now()
            t_cloth_factory_dispatch_audit_obj.currentState = '14'
            t_cloth_factory_dispatch_audit_obj.save()
            # 修改操作记录
            #t_product_oplog.objects.filter(pid=querysetid.id, StepID='JZL').update(MainSKU='', EndTime=datetime.now())
    to_no_audit.short_description = u'排单审核不通过'

    def ossNum(self, obj):
        rt = ""
        if obj.oosNum > 0:
            rt = u"<font size='4' color='red'>%s</font>"%(obj.oosNum)
        else:
            rt = u"<font size='4' color='red'>0</font>"
        return mark_safe(rt)
    ossNum.short_description = mark_safe(u'<p style="width:100px;color:#428bca;" align="center">缺货及未派单量</p>')

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
        rt = u'<strong>采购数量:</strong>%s <br><strong>采购备注:</strong>%s' % ( obj.productNumbers, obj.remarkApply)
        return mark_safe(rt)
    show_SKUNumbers.short_description = mark_safe('<p align="center" style="width:120px;color:#428bca;">采购数量</p>')

    def show_rawNumbers(self, obj):
        input_id = str(obj.id)
        show_input_res = input_id
        if obj.rawNumbers is None:
            rawNumbers = ''
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
        #messages.info(self.request, str(obj.unit) + "strSelect1:" + strSelect1 + ",strSelect2:" + strSelect2 + ",strSelect3:" + strSelect3)
        rt = u'原料数量:<input type="text" style="width:50px" id="cg_%s" value="%s" />' \
             u'<script>$(document).ready(function(){$("#cg_%s").blur(function(){var newnumber = $("#cg_%s").val();' \
             u'if(newnumber!=""){$.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
             u'dataType: "json",data:{"rawNumbers":newnumber,"unit":"kong01","productNumbers":999999,"remarkApply":"noremarkapply","SKU":"%s","id":"%s"},' \
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
                  u'</select>' \
                  u'<script>  $(document).ready(function(){$("#sel_%s").blur(function(){var selData = $("#sel_%s").val();' \
                  u'if(selData!=""){$.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
                  u'dataType: "json",data:{"rawNumbers":999999,"unit":selData,"productNumbers":999999,"remarkApply":"noremarkapply","SKU":"%s","id":"%s"},' \
                  u'success:function(data, textStatus, jqXHR){if(data == "1"){document.getElementById("sel_%s").text="success";}},' \
                  u'error:function(jqXHR, textStatus, errorThrown){ alert("failed")}});}}); ' \
                  u'var cgcheck =  document.getElementById("sel_%s");  if (cgcheck.checked){document.getElementById("sel_%s").readOnly=true; }' \
                  u'else{document.getElementById("sel_%s").readOnly=false;}}); </script>' % (
                 input_id, strSelect1, strSelect2, strSelect3, input_id, input_id, obj.SKU, input_id, input_id,
                 input_id, input_id, input_id)

        rt = rt + u'<br>排单备注:<input type="text" style="width:140px;height:70px" id="remarkSpeModify_%s" value="%s" />' \
                  u'<script>$(document).ready(function(){$("#remarkSpeModify_%s").blur(function(){var remarkSpeModify = $("#remarkSpeModify_%s").val();' \
                  u'if(remarkSpeModify!=""){$.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
                  u'dataType: "json",data:{"rawNumbers":999999,"unit":"kong01","productNumbers":999999,"remarkApply":"noremarkapply","remarkSpeModify":remarkSpeModify,"SKU":"%s","id":"%s"},' \
                  u'success:function(data, textStatus, jqXHR){if(data == "1"){document.getElementById("remarkSpeModify_%s").text="success";}},' \
                  u'error:function(jqXHR, textStatus, errorThrown){ alert("failed")}});}}); ' \
                  u'var cgcheck =  document.getElementById("remarkSpeModify_%s");  if (cgcheck.checked){document.getElementById("remarkSpeModify_%s").readOnly=true; }' \
                  u'else{document.getElementById("remarkSpeModify_%s").readOnly=false;}}); </script>' % (
                 input_id, obj.remarkSpeModify, input_id, input_id, obj.SKU, input_id, input_id, input_id, input_id,
                 input_id)
        if obj.currentState == '14':
            if obj.remarkDisPatch is not None:
                rt = rt + u"<br><font color='red'>审核未通过:%s</font>" % (obj.remarkDisPatch)
            else:
                rt = rt + u"<br><font color='red'>审核未通过,待修改后重新提交审核</font>"
        return mark_safe(rt)
    show_rawNumbers.short_description = mark_safe('<p style="width:210px;color:#428bca;">原材料数量</p>')

    def GoodsOther(self,obj):
        rt = u'<p style="width:120px;"><strong>商品成本价:</strong>%s <br><strong>7天销量:</strong>%s <br><strong>预计库存量:</strong>%s<br><strong>采购未入库量:</strong>%s</p>' % (obj.goodsCostPrice,obj.sevenSales,obj.ailableNum,obj.PurchaseNotInNum)
        return mark_safe(rt)
    GoodsOther.short_description = mark_safe(u'<p style="width:120px;color:#428bca;" align="center">商品其他信息</p>')

    def GoodsInfo(self,obj):
        rt = u'<p style="width:200px;"><strong>商品名称:</strong>%s <br><strong>供应商名:</strong>%s <br><strong>商品状态:</strong>%s<br><strong>商品类别:</strong>%s<br><strong>上一步处理人员:</strong>%s<br><strong>上一步处理时间:</strong>%s</p>' % (obj.goodsName,obj.Supplier, obj.goodsState,obj.goodsclass,obj.speModifyMan,obj.speModifyDate)
        return mark_safe(rt)
    GoodsInfo.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">商品及流程信息</p>')

    list_display = (
         'SKU', 'show_Picture', 'buyer', 'SalerName2','OSCode','TortInfo', 'GoodsInfo',
        'GoodsOther','ossNum','SuggestNum','show_SKUNumbers','show_rawNumbers','outFactory',)
    list_editable = ('outFactory',)
    fields = (
        'SKU', 'goodsName', 'Supplier', 'goodsState', 'goodsCostPrice', 'oosNum', 'stockNum', 'ailableNum',
        'sevenSales', 'fifteenSales',
        'thirtySales', 'PurchaseNotInNum', 'buyer', 'productNumbers', 'loanMoney',
        'actualMoney', 'outFactory', 'rawNumbers', 'unit',
        'remarkApply', 'remarkApply', 'remarkAudit','remarkApply','remarkAudit',)

    def get_list_queryset(self):
        request = self.request
        qs = super(t_cloth_factory_dispatch_paid_audit_Admin, self).get_list_queryset()

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

        from django.contrib.auth.models import User
        userID = [each.id for each in User.objects.filter(groups__id__in=[48])]
        if request.user.is_superuser or request.user.id in userID:
            return qs.filter(currentState = 16)
        buyer = request.user.first_name
        return qs.filter(currentState = 16,buyer=buyer)
        #return qs.filter(currentState = 16)


