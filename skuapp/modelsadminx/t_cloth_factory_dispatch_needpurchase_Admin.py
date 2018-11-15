# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_needpurchase_Admin.py
 @time: 2018/4/28 8:53
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
from datetime import datetime
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.db.models import Q
from skuapp.table.public import *
from django.db import connection
import MySQLdb

class t_cloth_factory_dispatch_needpurchase_Admin(object):
    actions = ['to_generatepurchase','deletenotpurchase'  ]
    search_box_flag = True
    t_cloth_factory = True
    importfile_plugin = True

    def gen_orderno(self,db_cursor):
        try:
            result = {'errorcode': 0, 'errortext': '','OrderNO':''}
            currentDate = datetime.now().strftime('%Y-%m-%d')
            currentDatePre = datetime.now().strftime('%Y%m%d')
            strSelectSql = "select max(PerDayAutoID) from t_cloth_factory_orderno where RecordDate='%s'" % (currentDate)
            db_cursor.execute(strSelectSql)
            selectRecord = db_cursor.fetchone()
            perMaxID = 0
            if selectRecord[0]:  # 存在记录
                perMaxID = selectRecord[0]
                perMaxID = int(perMaxID) + 1
            else:  # 不存在记录
                perMaxID = 100000 + 1
            insertSql = "insert into t_cloth_factory_orderno(IDType,RecordDate,PerDayAutoID,OpMan) values('clothfactory','%s',%s,'%s')" \
                        % (currentDate, perMaxID,self.request.user.first_name)
            db_cursor.execute(insertSql)
            strOrderNo = currentDatePre + str(perMaxID)
            result['OrderNO'] = strOrderNo
        except MySQLdb.Error, e:
            result['errorcode'] = 26666
            result['errortext'] = 'gen_orderno:%s,%s' % (MySQLdb.Error, e)
            result['OrderNO'] = ''
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'gen_orderno:%s,%s' % (Exception, ex)
            result['OrderNO'] = ''
        return result

    def setOrderNo(self,sku):
        db_cursor = connection.cursor()
        try:
            result = {'errorcode': 0, 'errortext': '','OrderNO':''}
            if sku is None:
                result['errorcode'] = 99999
                result['errortext'] = ''
                result['OrderNO'] = ''
                db_cursor.close()
                return result
            strSql_mainSKU = "select MainSKU from t_product_mainsku_sku where ProductSKU='%s'"%(sku)
            db_cursor.execute(strSql_mainSKU)
            selectRecord = db_cursor.fetchone()
            listSKU = []
            if selectRecord:
                strSql_ProductSKU = "select ProductSKU from t_product_mainsku_sku where MainSKU='%s'" % (selectRecord[0])
                db_cursor.execute(strSql_ProductSKU)
                selectProductRecord = db_cursor.fetchall()
                for row in selectProductRecord:
                    listSKU.append(row[0])
            currentStart = datetime.now().strftime('%Y-%m-%d') + " 00:00:00"
            currentEnd = datetime.now().strftime('%Y-%m-%d') + " 23:59:59"
            if len(listSKU) > 0:
                strSql_clothfactory = "select OrderNo from t_cloth_factory_dispatch where SKU in('%s') and OrderNo is not NULL and OrderNo!='' and createDate>'%s' and createDate<'%s' and currentState!='32'"\
                                      %("','".join(listSKU),currentStart,currentEnd)
                db_cursor.execute(strSql_clothfactory)
                selectRecordOrderNo = db_cursor.fetchone()
                if selectRecordOrderNo is not None and len(selectRecordOrderNo)>0:
                    strUpdate = "update t_cloth_factory_dispatch set OrderNo='%s' where SKU in('%s') and createDate>'%s' and createDate<'%s'  and currentState!='32'"\
                                %(selectRecordOrderNo[0],"','".join(listSKU), currentStart, currentEnd)
                    db_cursor.execute(strUpdate)
                    result['errorcode'] = 0
                    result['errortext'] = ''
                    result['OrderNO'] = selectRecordOrderNo[0]
                else:
                    result = self.gen_orderno(db_cursor)
                    if result['errorcode'] == 0:
                        strUpdate = "update t_cloth_factory_dispatch set OrderNo='%s' where SKU in('%s') and createDate>'%s' and createDate<'%s'  and currentState!='32'"\
                                    % (result['OrderNO'], "','".join(listSKU) , currentStart, currentEnd)
                        db_cursor.execute(strUpdate)
                        result['errorcode'] = 0
                        result['errortext'] = ''
                        result['OrderNO'] = result['OrderNO']
            else:
                result = self.gen_orderno(db_cursor)
                if result['errorcode'] == 0:
                    strUpdate = "update t_cloth_factory_dispatch set OrderNo='%s' where SKU='%s' and createDate>'%s' and createDate<'%s'  and currentState!='32'"\
                                %(result['OrderNO'], sku, currentStart, currentEnd)
                    db_cursor.execute(strUpdate)
                    result['errorcode'] = 0
                    result['errortext'] = ''
                    result['OrderNO'] = result['OrderNO']

            if result['errorcode'] != 0:
                db_cursor.close()
                connection.rollback()
            else:
                db_cursor.close()
                connection.commit()
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'setOrderNo:%s,%s' % (Exception, ex)
            result['OrderNO'] = ''
            db_cursor.close()
            connection.rollback()
        return result

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

    def deletenotpurchase(self, request, objs):
        listNo = []
        for obj in objs:
            obj.currentState = '32'
            obj.genPurchaseMan = request.user.first_name
            obj.genPurchaseDate = datetime.now()
            obj.save()
    deletenotpurchase.short_description = u"不需要采购计划"

    def to_generatepurchase(self, request, objs):
        listError = []
        for obj in objs:
            #生成订单号
            result = self.setOrderNo(obj.SKU)
            if result['errorcode'] ==0:
                obj.currentState = '4'
                obj.genPurchaseMan = request.user.first_name
                obj.genPurchaseDate = datetime.now()
                obj.OrderNo = result['OrderNO']
                obj.save()
            else:
                listError.append(obj.SKU)
                messages.error(request,'%s'%(result))
        if len(listError) > 0:
            messages.error(request, '以下SKU:%s,生成采购计划错误，可能由于生成订单号主键冲突，请稍后重试。' % (listError))
    to_generatepurchase.short_description = u"生成采购计划"

    def ossNum(self, obj):
        rt = ""
        if obj.oosNum > 0:
            rt = u"<font size='4' color='red' align='center'>%s</font>"%(obj.oosNum)
        else:
            rt = u"<font size='4' color='red' align='center'>0</font>"
        return mark_safe(rt)
    ossNum.short_description = mark_safe(u'<p style="width:100px;color:#428bca;" align="center">缺货及未派单量</p>')

    def GoodsOther(self,obj):
        try:
            rt = ''
            from skuapp.table.t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
            t_cloth_factory_dispatch_needpurchase_objs = t_cloth_factory_dispatch_needpurchase.objects.filter(
                SKU=obj.SKU).filter( Q(currentState=20) | Q(currentState=22) | Q(currentState=24)).values_list('productNumbers')
            productNumbers = 0
            for rowObj in  t_cloth_factory_dispatch_needpurchase_objs:
                if rowObj[0] is not None:
                    productNumbers += int(rowObj[0])
            ailableNum = 0
            if obj.ailableNum is not None and int(obj.ailableNum) != 0:
                ailableNum = int(obj.ailableNum)
                rt = u'<p style="width:170;"><strong>预计可用库存(%s)</strong>=<br>'%(ailableNum)
                if obj.stockNum is not None and int(obj.stockNum) != 0:
                    rt = rt + u'库存(%s)<br>'%(int(obj.stockNum))
                if obj.occupyNum is not None and int(obj.occupyNum) != 0:
                    rt = rt + u'-占用(%s)<br>'%(int(obj.occupyNum))
                if obj.PurchaseNotInNum is not None and int(obj.PurchaseNotInNum) != 0:
                    rt = rt + u'+(普元采购未入库量<br>+采购计划审核通过量)(%s)<br>'%(int(obj.PurchaseNotInNum))
                if obj.oosNum is not None and int(obj.oosNum) != 0:
                    rt = rt + u'-缺货及未派单量(%s)<br>'%(int(obj.oosNum))

            if obj.AverageNumber is not None and float(obj.AverageNumber) > 0.0:
                rt = rt + u'<strong>预计可卖天数(%s)</strong>=<br>预计可用库存(%s)<br>/日平均销量(%s)<br>'\
                 % (obj.SaleDay,obj.ailableNum, obj.AverageNumber)
            param_num = '4*7'
            if obj.OSCode == 'OS901':
                param_num = '3*7'
            elif obj.OSCode == 'OS903' or obj.OSCode == 'OS904':
                param_num = '5*7'
            elif obj.OSCode == 'OS909':
                param_num = '6*7'
            else:
                param_num = '4*7'
            sevenSales = 0
            if obj.sevenSales is not None :
                sevenSales = int(obj.sevenSales)
            if obj.SuggestNum is not None and obj.SuggestNum != '':
                if obj.SpecialPurchaseFlag is not None and obj.SpecialPurchaseFlag !='':
                    if obj.SpecialPurchaseFlag == 'firstorder':
                        rt = rt + u'<strong>建议采购数量(%s)</strong>=<br>网采转供应链排单-首单(%s)<br>' % (obj.SuggestNum, obj.SuggestNum)
                    elif obj.SpecialPurchaseFlag == 'customermade':
                        rt = rt + u'<strong>建议采购数量(%s)</strong>=<br>客户定做(%s)<br>' % (obj.SuggestNum, obj.SuggestNum)
                    elif obj.SpecialPurchaseFlag == 'other':
                        rt = rt + u'<strong>建议采购数量(%s)</strong>=<br>浦江仓库(%s)<br>' % (obj.SuggestNum, obj.SuggestNum)
                elif obj.OSCode == 'OS906' and obj.Stocking_plan_number is not None and obj.Stocking_plan_number != '':
                    rt = rt + u'<strong>建议采购数量(%s)</strong>=<br>海外仓录入数量(%s)<br>' % (obj.SuggestNum,obj.SuggestNum)
                else:
                    rt = rt + u'<strong>建议采购数量(%s)</strong>=<br>%s天销量(%s)<br>'%(obj.SuggestNum,param_num,sevenSales)
                    if obj.stockNum is not None and int(obj.stockNum) != 0:
                        rt = rt + u'-库存(%s)<br>'%(int(obj.stockNum))
                    if obj.PurchaseNotInNum is not None and int(obj.PurchaseNotInNum) != 0:
                        rt = rt + u'-(普元采购未入库量<br>+采购计划审核通过量)(%s)<br>'%(int(obj.PurchaseNotInNum))
        except Exception as e:
            messages.info(self.request,obj.SKU + str(e))
            rt = ''
        if rt == '':
            rt = u'0'
        return mark_safe(rt)
    GoodsOther.short_description = mark_safe(u'<p style="width:170px;color:#428bca;" align="center">数量信息</p>')

    def GoodsInfo(self,obj):
        rt = u'<p style="width:220px;"><strong>商品名称:</strong>%s <br><strong>商品成本价:</strong>%s <br><strong>供应商名:</strong>%s <br><strong>商品状态:</strong>%s<br><strong>商品类别:</strong>%s<br><strong>侵权站点:</strong>%s<br><strong>创建时间:</strong>%s</p>' % (obj.goodsName,obj.goodsCostPrice,obj.Supplier, obj.goodsState,obj.goodsclass,obj.TortInfo,obj.createDate)
        return mark_safe(rt)
    GoodsInfo.short_description = mark_safe(u'<p style="width:220px;color:#428bca;" align="center">商品信息</p>')

    def SKUNodeInfo(self,obj):
        try:
            rt = ''
            from skuapp.table.t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
            t_cloth_factory_dispatch_needpurchase_objs = t_cloth_factory_dispatch_needpurchase.objects.filter(SKU=obj.SKU).filter(Q(currentState=8)| Q(currentState=16)|Q(currentState=18)|Q(currentState=20)|Q(currentState=22)| Q(currentState=24)).order_by('-currentState').values_list('productNumbers','currentState','genPurchaseDate','applyDate','auditDate','speModifyDate','disPatchDate','confirmDate','closeDate','completeNumbers')
            rt = u'<p style="width:200px;">'
            if len(t_cloth_factory_dispatch_needpurchase_objs) == 0:
                rt = rt + u'<strong>其他流程节点无该商品信息</strong><br>'
            else:
                rt = rt + u'<strong>其他流程信息(采购数量;完成数量;时间):</strong><br>'
                rt_4 = 0
                rt_8 = 0
                rt_16 = 0
                rt_20 = 0
                rt_24 = 0
                dt_4 = ''
                dt_8 = ''
                dt_16 = ''
                dt_20 = ''
                dt_24 = ''
                cm_22 = 0
                cm_24 = 0
                for rowObj in t_cloth_factory_dispatch_needpurchase_objs:
                    ###'productNumbers','currentState','genPurchaseDate','applyDate','auditDate','speModifyDate','disPatchDate','confirmDate','closeDate','completeNumbers'
                    if int(rowObj[1]) == 4 or int(rowObj[1]) == 6 :
                        rt_4 += 1
                    if int(rowObj[1]) == 8 and rowObj[0] is not None and int(rowObj[0]) != 0:
                        rt_8 += rowObj[0]
                        dt_8 = str(rowObj[3])[:10]
                    if (int(rowObj[1]) == 16 or int(rowObj[1]) == 18) and rowObj[0] is not None and int(rowObj[0]) != 0:
                        rt_16 += rowObj[0]
                        dt_16 = str(rowObj[4])[:10] if rowObj[6] is not None else ''
                    if (int(rowObj[1]) == 20 or int(rowObj[1]) == 22)  and rowObj[0] is not None and int(rowObj[0]) != 0:
                        rt_20 += rowObj[0]
                        dt_20 = str(rowObj[6])[:10] if rowObj[6] is not None else ''
                        if rowObj[9] is not None and rowObj[9] != '':
                            cm_22 += int(rowObj[9])
                    if int(rowObj[1]) == 24  and rowObj[0] is not None and int(rowObj[0]) != 0:
                        rt_24 += rowObj[0]
                        dt_24 = str(rowObj[7])[:10] if rowObj[6] is not None else ''
                        if rowObj[9] is not None and rowObj[9] != '':
                            cm_24 += int(rowObj[9])
                if rt_4 > 0:
                    rt = rt + u'<strong>流程节点-采购计划:</strong>存在采购计划<br>'
                if rt_8 > 0:
                    rt = rt + u'<strong>流程节点-采购计划审核:</strong>%s;%s <br>' % (str(rt_8), dt_8)
                if rt_16 > 0:
                    rt = rt + u'<strong>流程节点-转工厂交付系统:</strong>%s;%s <br>' % (str(rt_16), dt_16)
                if rt_20 > 0:
                    rt = rt + u'<strong>流程节点-检验交付数量和单价:</strong>%s;%s;%s<br>' % (str(rt_20),str(cm_22), dt_20)
                if rt_24 > 0:
                    rt = rt + u'<strong>流程节点-生产完成可建普源采购单:</strong>%s;%s;%s<br>' % (str(rt_24),str(cm_24), dt_24)
            rt = rt + u'</p>'
        except Exception as e:
            messages.info(self.request,obj.SKU + str(e))
            rt = ''
        return mark_safe(rt)
    SKUNodeInfo.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">流程节点信息</p>')

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
                  u'</select>'\
                  u'<script>  $(document).ready(function(){$("#sel_%s").blur(function(){var selData = $("#sel_%s").val();' \
                 u'if(selData!=""){$.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
                 u'dataType: "json",data:{"rawNumbers":999999,"unit":selData,"productNumbers":999999,"remarkApply":"noremarkapply","SKU":"%s","id":"%s"},' \
                 u'success:function(data, textStatus, jqXHR){if(data == "1"){document.getElementById("sel_%s").text="success";}},' \
                 u'error:function(jqXHR, textStatus, errorThrown){ alert("failed")}});}}); ' \
                 u'var cgcheck =  document.getElementById("sel_%s");  if (cgcheck.checked){document.getElementById("sel_%s").readOnly=true; }' \
                 u'else{document.getElementById("sel_%s").readOnly=false;}}); </script>' % (
            input_id,strSelect1,strSelect2,strSelect3,input_id,input_id,obj.SKU,input_id,input_id,input_id,input_id,input_id)
        rt = rt + u'<br><br>产出件数:' \
                  u'<input type="text" style="width:180px" id="productNumbers_%s" value="%s" />' \
                  u'<script>$(document).ready(function(){$("#productNumbers_%s").blur(function(){var productNumbers = $("#productNumbers_%s").val();' \
             u'if(productNumbers!=""){$.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
             u'dataType: "json",data:{"rawNumbers":999999,"unit":"kong01","productNumbers":productNumbers,"remarkApply":"noremarkapply","SKU":"%s","id":"%s"},' \
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

    def show_DataFlag(self, obj):
        if obj.flag == 1:
            rt = '<div class="box" style="width: 100px;height: 170px;background-color: #A6FFA6;text-align: center;line-height: 30px;border-radius: 4px">%s<br>建议采购</div>'%(obj.SKU)
        elif obj.flag == 2:
            rt = '<div class="box" style="width: 100px;height: 170px;background-color: #FFF4C1;text-align: center;line-height: 30px;border-radius: 4px">%s<br>联动采购</div>'%(obj.SKU)
        elif obj.flag == 3:
            rt = '<div class="box" style="width: 100px;height: 170px;background-color: #FFECEC;text-align: center;line-height: 30px;border-radius: 4px">%s<br>普源下单</div>'%(obj.SKU)
        else:
            rt = '<div class="box" style="width: 100px;height: 170px;background-color: #C4E1FF;text-align: center;line-height: 30px;border-radius: 4px">%s<br>自主采购</div>'%(obj.SKU)
            #rt = "style="background-color: #FFC1C1"" + obj.SKU
        return mark_safe(rt)
    show_DataFlag.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">商品编码</p>')

    def show_Remark(self, obj):
        choices = getChoices(ChoiceNoNeedPurchaseRemark)
        remarkValue = '' if obj.remarkGenPurchase is None else obj.remarkGenPurchase
        tmpValue = remarkValue
        #rt = '<input type="text" id="box_%s" value="%s" style="width:140px;" readonly="readonly">' % (obj.ID, ipfvalue,)
        rt = '<div id = "selectBox_%s" ><ul>' % (obj.id,)
        for k, v in choices:
            checked = 'checked="checked"' if k in remarkValue else ''
            tmpValue = tmpValue.replace(k,'')
            rt = '%s<li><input type="checkbox" name="ck_%s" value="%s" %s>%s</li>' % (rt, obj.id, k, checked, v)
        while True:
            if tmpValue is not None and len(tmpValue) > 0 and tmpValue[0] == ',':
                tmpValue = tmpValue[1:]
            else:
                break
        rt = '%s</ul><input type="text" style="width:100px" id="input_%s" value="%s"><br><input type="button" id="btn_%s" value="确定" style="width:50px;"> <p id="result_%s" style="color:green;"></p></div>' % (
        rt, obj.id,tmpValue, obj.id, obj.id)

        tt = """%s<script>
            $(document).ready(function(){
                var arr=[];
                $('input:checkbox[name="ck_%s"]').change(function(){
                    if($(this).prop("checked")){
                        arr.push($(this).val());
                    }
                    else{
                        var index=getIndex(arr,$(this).val());
                        arr.splice(index,1);
                    }
                })
                function getIndex(arr,value){
                    for(var i=0;i<arr.length;i++){
                        if(arr[i]==value){
                            return i;
                        }
                    }
                    return -1;
                }

                $('#btn_%s').click(function(){
                    var inputInfo = document.getElementById("input_%s").value;
                    $.ajax({url:"/t_cloth_factory_remark/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",data:{"remarkInfo":arr.join(","),"id":"%s","inputInfo":inputInfo},
                    success:function(data){if(data.result=="OK"){document.getElementById("result_%s").innerHTML="Success!";}},
                    error:function(data){document.getElementById("result_%s").innerHTML="Fail!";}
                })})
            })</script>"""
        rt = tt % (rt, obj.id, obj.id,obj.id, obj.id, obj.id, obj.id)
        return mark_safe(rt)
    show_Remark.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">备注</p>')

    list_per_page = 20
    list_display = ('show_DataFlag','show_Picture', 'buyer','SalerName2', 'OSCode','GoodsInfo','SKUNodeInfo','GoodsOther','ailableNum',
     'SaleDay','SuggestNum','show_Remark')
    list_editable = ('remarkGenPurchase')

    #BmpUrl,SKU,TortInfo,goodsState,buyer,SalerName2,sevenSales,fifteenSales,thirtySales,UseNumber,PurchaseNotInNum,goodsCostPrice,SuggestNum,ailableNum,
    #oosNum,occupyNum,stockNum,goodsName,Supplier,girard,SaleDay,goodsclass,AverageNumber,flag
    #py_db.kc_currentstock_sku
    #通过SKU可以获取的 BmpUrl、TortInfo、goodsState
    fields = (
    'SKU', 'SuggestNum', 'buyer',
    'SpecialPurchaseFlag',
    'remarkGenPurchase',)

    form_layout = (
        Fieldset(u'请认真填写备货需求',
                 Row('SKU', 'SuggestNum', 'buyer', ),
                 Row('SpecialPurchaseFlag', '', '', ),
                 Row('remarkGenPurchase',  ),
                 css_class='unsort '
                 ),)

    def save_models(self,):
        try:
            obj = self.new_obj
            request = self.request

            old_obj = None

            if obj is None or obj.id is None or obj.id <= 0:
                pass
            else:
                old_obj = self.model.objects.get(pk=obj.pk)
            obj.save()

            strSql ='''
                SELECT
                a.BmpUrl, a.SKU, a.TortInfo, a.GoodsStatus, a.Purchaser, a.SalerName2, a.SellCount1, a.SellCount2, a.SellCount3, a.UseNumber,
                a.NotInStore as NotInStore, a.CostPrice,
                4 * a.SellCount1 - a.Number - a.NotInStore as SuggestNum,
                a.hopeUseNum as hopeUseNum, a.UnPaiDNum, a.ReservationNum, a.Number, a.GoodsName, a.SupplierName, a.Model,
                (a.hopeUseNum) / a.AverageNumber as SaleDay, a.CgCategory, a.AverageNumber,
                if (((a.hopeUseNum) / a.AverageNumber) <= 15, 1, 2) as flag,a.SourceOSCode
                FROM py_db.kc_currentstock_sku a  where SKU='%s'  and storeID=1
            ''' % (obj.SKU)
            hqdb_cursor = connection.cursor()
            hqdb_cursor.execute(strSql)
            resultRecord = hqdb_cursor.fetchone()
            #BmpUrl, SKU, TortInfo, goodsState, buyer, SalerName2, sevenSales, fifteenSales, thirtySales,
            #UseNumber, PurchaseNotInNum, goodsCostPrice, SuggestNum, ailableNum, oosNum, occupyNum, stockNum, goodsName, Supplier, girard, SaleDay,
            #goodsclass, AverageNumber, flag
            if resultRecord:
                obj.BmpUrl = resultRecord[0] #图片
                obj.TortInfo = resultRecord[2] #侵权信息
                obj.goodsState = resultRecord[3] #商品状态
                if obj.buyer is None:
                    obj.buyer = resultRecord[4]
                obj.SalerName2 = resultRecord[5]
                obj.sevenSales = resultRecord[6]
                obj.fifteenSales = resultRecord[7]
                obj.thirtySales = resultRecord[8]
                obj.UseNumber = resultRecord[9]

                obj.PurchaseNotInNum = resultRecord[10]
                obj.goodsCostPrice = resultRecord[11]
                obj.ailableNum = resultRecord[13]
                obj.oosNum = resultRecord[14]
                obj.occupyNum = resultRecord[15]
                obj.stockNum = resultRecord[16]
                obj.goodsName = resultRecord[17]
                obj.girard = resultRecord[19]
                obj.SaleDay = resultRecord[20]
                obj.goodsclass = resultRecord[21]
                obj.AverageNumber = resultRecord[22]
                obj.OSCode = resultRecord[24]
                if resultRecord[24] not in ['OS901','OS902','OS903','OS904','OS905','OS906','OS909']:
                    obj.OSCode = 'OS905'
                obj.Supplier = u'广州工厂'
                obj.currentState = '0'
                obj.createDate = datetime.now()
                obj.GenRecordMan = request.user.first_name
                obj.GenRecordDate = datetime.now()
                obj.flag = 9
                obj.save()
            else:
                messages.info(self.request, "库存预警表未关联到数据，请联系IT查看。" )
            hqdb_cursor.close()
        except Exception, ex:
            messages.info(self.request,"保存报错:%s"%(str(ex)))



    def get_list_queryset(self):
        request = self.request
        qs = super(t_cloth_factory_dispatch_needpurchase_Admin, self).get_list_queryset()

        #PurchaseNotInNum = request.GET.get('PurchaseNotInNum', '')
        SKU = request.GET.get('SKU', '')

        Supplier = request.GET.get('Supplier', '')
        buyer = request.GET.get('buyer', '')
        buyer = buyer.split(',')
        if '' in buyer:
            buyer = ''
        oosNumStart = request.GET.get('oosNum_Start', '')
        oosNumEnd = request.GET.get('oosNum_End', '')

        createDateStart = (datetime.now()).strftime('%Y-%m-%d 00:00:01')
        createDateEnd = (datetime.now()).strftime('%Y-%m-%d 23:59:59')

        goodsState = request.GET.get('goodsState', '')
        from skuapp.table.goodsstatus_compare import goodsstatus_compare
        goodsstatus_compare_objs = goodsstatus_compare.objects.filter(py_GoodsStatus=goodsState).values_list(
            "hq_GoodsStatus", flat=True)

        searchList = {'SKU__contains': SKU,
                      'Supplier':Supplier,
                      'buyer__in': buyer,
                      'oosNum__gte': oosNumStart,
                      'oosNum__lt': oosNumEnd,
                      'goodsState__in': list(goodsstatus_compare_objs),
                      'createDate__gte': createDateStart,
                      'createDate__lt': createDateEnd,
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
            return qs.filter(currentState = 0,SuggestNum__gt=0)
        buyer = request.user.first_name
        return qs.filter(currentState = 0,buyer=buyer,SuggestNum__gt=0)

        #qs.filter(Q(CategoryCode=u'001.时尚女装') | Q(CategoryCode=u'002.时尚男装')| Q(CategoryCode=u'025.内衣')| Q(CategoryCode=u'021.泳装')| Q(CategoryCode=u'024.儿童服装')).filter(GoodsStatus='normal')

