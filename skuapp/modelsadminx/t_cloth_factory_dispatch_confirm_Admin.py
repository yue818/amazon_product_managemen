# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_confirm_Admin.py
 @time: 2018/4/28 8:53
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_cloth_factory_dispatch_confirm import *
from django.contrib import messages
from django.db.models import Q
from django.utils.safestring import mark_safe
from datetime import datetime as confirmDate
from Project.settings import *
import oss2
from xlwt import *
from .t_product_Admin import *

class t_cloth_factory_dispatch_confirm_Admin(object):
    actions = ['to_close','to_section_complete','to_import_execl']
    t_cloth_factory = True
    search_box_flag = True
    downloadxls = True

    def to_close(self, request, objs):
        try:
            from skuapp.table.t_cloth_factory_dispatch_confirm import t_cloth_factory_dispatch_confirm
            skulist = []
            for obj in objs:
                #对完成数量为空的处理
                t_cloth_factory_dispatch_confirm_obj_01 = t_cloth_factory_dispatch_confirm.objects.filter(id=obj.id).values_list('completeNumbers', flat=True)
                if t_cloth_factory_dispatch_confirm_obj_01.exists():
                    if t_cloth_factory_dispatch_confirm_obj_01[0] is None or str(t_cloth_factory_dispatch_confirm_obj_01[0]) == '' or str(t_cloth_factory_dispatch_confirm_obj_01[0]) == '0':
                        skulist.append(obj.SKU)
                        continue
                t_cloth_factory_dispatch_confirm_obj = t_cloth_factory_dispatch_confirm()
                t_cloth_factory_dispatch_confirm_obj.__dict__ = obj.__dict__
                t_cloth_factory_dispatch_confirm_obj.confirmMan = request.user.first_name
                t_cloth_factory_dispatch_confirm_obj.confirmDate = confirmDate.now()
                t_cloth_factory_dispatch_confirm_obj.currentState = '24'
                t_cloth_factory_dispatch_confirm_obj.save()

                if obj.Stocking_plan_number is not None and obj.Stocking_plan_number != '':
                    if obj.remarkDisPatch is not None:
                        listTmp = str(obj.remarkDisPatch).split('#@#')
                        from skuapp.table.t_stocking_purchase_order import t_stocking_purchase_order
                        from skuapp.table.t_stocking_demand_list import t_stocking_demand_list
                        from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
                        t_stocking_purchase_order_obj = t_stocking_purchase_order.objects.filter(Stocking_plan_number=obj.Stocking_plan_number,ProductSKU=obj.SKU)
                        t_stocking_demand_fba_obj = t_stocking_demand_fba.objects.filter(Stocking_plan_number=obj.Stocking_plan_number, ProductSKU=obj.SKU)
                        if t_stocking_purchase_order_obj:
                            t_stocking_purchase_order.objects.filter(Stocking_plan_number = obj.Stocking_plan_number,ProductSKU=obj.SKU).update(Single_number=listTmp[0],Status='purchasing',
                                                                                                                                                QTY=t_cloth_factory_dispatch_confirm_obj_01[0],
                                                                                                                                                The_arrival_of_the_number=t_cloth_factory_dispatch_confirm_obj_01[0])
                            t_stocking_demand_list.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).update(Status='already')
                        elif t_stocking_demand_fba_obj:
                            t_stocking_demand_fba.objects.filter(Stocking_plan_number=obj.Stocking_plan_number,ProductSKU=obj.SKU).update(
                                Single_number=listTmp[0], Status='purchasing',recordPurchaseCodeMan=request.user.first_name,recordPurchaseCodeDate=datetime.datetime.now(),
                                QTY=t_cloth_factory_dispatch_confirm_obj_01[0],
                                The_arrival_of_the_number=t_cloth_factory_dispatch_confirm_obj_01[0])


            if len(skulist) > 0:
                messages.info(request,u'以下SKU=%s对应的完成数量不能为空，填写的采购订单号未能获取普元入库数量，请检查后重新填写。'%(skulist))
        except Exception as e:
            messages.info(request, u'商品(%s)保存报错，请联系开发人员查看原因。' % (obj.SKU))
    to_close.short_description = u'全部交付完成'

    def to_section_complete(self, request, objs):
        from skuapp.table.t_cloth_factory_dispatch_confirm import t_cloth_factory_dispatch_confirm
        for obj in objs:
            t_cloth_factory_dispatch_confirm_obj = t_cloth_factory_dispatch_confirm()
            t_cloth_factory_dispatch_confirm_obj.__dict__ = obj.__dict__
            t_cloth_factory_dispatch_confirm_obj.currentState = '22'
            t_cloth_factory_dispatch_confirm_obj.confirmMan = request.user.first_name
            t_cloth_factory_dispatch_confirm_obj.confirmDate = confirmDate.now()
            if t_cloth_factory_dispatch_confirm_obj.remarkConfirm is None:
                t_cloth_factory_dispatch_confirm_obj.remarkConfirm = u'部分完成'
            t_cloth_factory_dispatch_confirm_obj.save()
    to_section_complete.short_description = u'部分交付完成'

    def to_import_execl(self, request, objs):
        try:
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
            sheet = w.add_sheet(u'校验交付数据')
            style = XFStyle()

            sheet.write(0, 0, u'日期', style)  # 日期
            sheet.write(0, 1, u'SKU', style)  # SKU
            sheet.write(0, 2, u'采购员', style)  # 采购员
            sheet.write(0, 3, u'商品名称', style)  # 商品名称
            sheet.write(0, 4, u'建议采购数量', style)  # 建议采购数量
            sheet.write(0, 5, u'采购数量', style)  # 采购数量
            sheet.write(0, 6, u'完成数量', style)  # 完成数量
            sheet.write(0, 7, u'采购备注', style)  # 采购备注
            sheet.write(0, 8, u'派发工厂', style)  # 派发工厂
            sheet.write(0, 9, u'排单备注', style)  # 排单备注
            sheet.write(0, 10, u'生产天数', style)  # 生产天数
            sheet.write(0, 11, u'采购等级', style)  # 采购等级

            for obj in objs:
                row = row + 1
                if obj.createDate is not None:
                    sheet.write(row, 0, str(obj.createDate), style)  # 日期
                else:
                    sheet.write(row, 0, '', style)  # 日期
                sheet.write(row, 1, obj.SKU, style)  # SKU
                if obj.buyer is not None:
                    sheet.write(row, 2, obj.buyer, style)  # 采购员
                else:
                    sheet.write(row, 2, '', style)  # 采购员
                if obj.goodsName is not None:
                    sheet.write(row, 3, obj.goodsName, style)  # 商品名称
                else:
                    sheet.write(row, 3, '', style)  # 商品名称
                if obj.SuggestNum is not None:
                    sheet.write(row, 4, obj.SuggestNum, style)  # 建议采购数量
                else:
                    sheet.write(row, 4, 0, style)  # 建议采购数量
                if obj.productNumbers is not None:
                    sheet.write(row, 5, obj.productNumbers, style)  # 采购数量
                else:
                    sheet.write(row, 5, 0, style)  # 采购数量
                if obj.completeNumbers is not None:
                    sheet.write(row, 6, obj.completeNumbers, style)  # 完成数量
                else:
                    sheet.write(row, 6, 0, style)  # 完成数量
                strRemark = ''
                if obj.remarkApply is not None:
                    strRemark = obj.remarkApply
                    if obj.remarkSpeModify is not None:
                        strRemark = strRemark + "," +obj.remarkSpeModify
                        if obj.remarkConfirm is not None:
                            strRemark = strRemark + "," + obj.remarkConfirm
                    else:
                        if obj.remarkConfirm is not None:
                            strRemark = strRemark + "," + obj.remarkConfirm
                else:
                    if obj.remarkSpeModify is not None:
                        strRemark = strRemark + "," + obj.remarkSpeModify
                        if obj.remarkConfirm is not None:
                            strRemark = strRemark + "," + obj.remarkConfirm
                    else:
                        if obj.remarkConfirm is not None:
                            strRemark = strRemark + "," + obj.remarkConfirm
                sheet.write(row, 7, strRemark, style)  # 采购备注
                sheet.write(row, 8, obj.outFactory, style)  # 派发工厂
                if obj.remarkDisPatch is not None:
                    sheet.write(row, 9, (obj.remarkDisPatch).replace("#@#",';'), style)  # 排单备注
                else:
                    sheet.write(row, 9, '', style)  # 排单备注

                diffDay = 0
                if obj.auditDate is not None:
                    diffDay = (confirmDate.now() - obj.auditDate).days
                sheet.write(row, 10, str(diffDay), style)  # 生产天数

                if obj.OSCode is None or obj.OSCode == 'OS905': # 采购等级
                    sheet.write(row, 11, u'OS905:工期5天(建议采购15天量、联动采购16~17天量)', style)
                elif obj.OSCode == 'OS901': # 采购等级
                    sheet.write(row, 11, u'OS901:工期3天(建议采购10天量、联动采购11~14天量)', style)
                elif obj.OSCode == 'OS902': # 采购等级
                    sheet.write(row, 11, u'OS902:工期5天(建议采购15天量、联动采购16~17天量)', style)
                elif obj.OSCode == 'OS903': # 采购等级
                    sheet.write(row, 11, u'OS903:工期7天(建议采购15天量、联动采购16~19天量)', style)
                elif obj.OSCode == 'OS904': # 采购等级
                    sheet.write(row, 11, u'OS904:工期15天(建议采购20天)', style)
                elif obj.OSCode == 'OS906': # 采购等级
                    sheet.write(row, 11, u'OS906:工期5天(Amazon服装采购)', style)
                elif obj.OSCode == 'OS909': # 采购等级
                    sheet.write(row, 11, u'OS909:工期5天(建议采购20天量)', style)
                else:
                    sheet.write(row, 11, u'OS905:工期5天(建议采购15天量、联动采购16~17天量)', style)

            filename = request.user.username + '_' + confirmDate.now().strftime('%Y%m%d%H%M%S') + '.xls'
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
        except Exception as e:
            messages.info(self.request,"导出数据到execl报错:%s，请联系开发人员"%(str(e)))
    to_import_execl.short_description = u'导出数据到execl'

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

        rt = """<img src="%s"  width="120" height="120"  title="%s" onerror="this.title=''" />  """ % (picture_url,picture_url)
        return mark_safe(rt)
    show_Picture.short_description = mark_safe(u'<p style="width:120px;color:#428bca;" align="center">图片</p>')

    def show_rawNumbers(self, obj):
        rt = u'<strong>原材料数量:</strong>%s(%s) <br><strong>采购数量:</strong>%s<br><strong>外派工厂:</strong>%s<br><strong>采购备注:</strong>%s<br>' \
             u'<strong>审核备注:</strong>%s<br><strong>服装生产备注:</strong>%s' % (
        obj.rawNumbers, obj.unit, obj.productNumbers, obj.outFactory, obj.remarkApply, obj.remarkAudit, obj.FactoryRemark)

        return mark_safe(rt)
    show_rawNumbers.short_description = mark_safe('<p align="center" style="width:150px;color:#428bca;">排单信息</p>')

    def show_confirmRemark(self, obj):
        diffDay = 0
        if obj.disPatchDate is not None:
           diffDay = (confirmDate.now() - obj.disPatchDate).days
        else:
           if obj.auditDate is not None:
                diffDay = (confirmDate.now() - obj.auditDate).days
        rt = u"<div align='center'><font color='black'>%s天</font></div><br>" % (diffDay)
        if obj.OSCode == 'OS901' or not obj.OSCode:
            if diffDay > 7:
                rt = u"<div align='center'><font style='font-weight:bold;' color='red'>%s天</font></div><br>" % (diffDay)
        elif obj.OSCode == 'OS902' or obj.OSCode == 'OS905':
            if diffDay > 8:
                rt = u"<div align='center'><font style='font-weight:bold;' color='red'>%s天</font></div><br>" % (diffDay)
        elif obj.OSCode == 'OS903' or obj.OSCode == 'OS906':
            if diffDay > 10:
                rt = u"<div align='center'><font style='font-weight:bold;' color='red'>%s天</font></div><br>" % (diffDay)
        elif obj.OSCode == 'OS904':
            if diffDay > 15:
                rt = u"<div align='center'><font style='font-weight:bold;' color='red'>%s天</font></div><br>" % (diffDay)
        elif obj.OSCode == 'OS909':
            if diffDay > 6:
                rt = u"<div align='center'><font style='font-weight:bold;' color='red'>%s天</font></div><br>" % (diffDay)
        else:
            rt = rt
        return mark_safe(rt)
    show_confirmRemark.short_description = mark_safe('<p align="center" style="width:150px;color:#428bca;">生产天数</p>')

    def show_complete(self, obj):
        try:
            input_id = str(obj.id)
            show_input_res = input_id
            if obj.completeNumbers is None:
                completeNumbers = '0'
            else:
                completeNumbers = str(obj.completeNumbers)
            #messages.info(self.request, str(obj.unit) + "strSelect1:" + strSelect1 + ",strSelect2:" + strSelect2 + ",strSelect3:" + strSelect3)

            rt = '<div id = "planPurchase_%s">' % (input_id,)
            rt = u'%s完成数量:<input type="text" style="width:150px;height:35px" id="completeNum_%s" value="%s" />' \
                 u'<input type="button" style="width:50px;height:35;margin-left:5px" id="btn1_%s" value="录入">' % (
                 rt, input_id, completeNumbers, input_id)

            if obj.remarkConfirm is not None:
                rt = u'%s<br><p style="color:red;">%s</p>' % (rt, obj.remarkConfirm,)

            rt = u'%s<br><p id="result1_%s"  style="color:green;"></p></div>' % (rt,input_id)

            tt = """%s<script>                        
                    $(document).ready(function(){
                        $("#btn1_%s").click(function(){
                            var completeNum_Num = document.getElementById("completeNum_%s").value;
                            $.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",
                            data:{"id":"%s","SKU":"%s","productNumbers_Num":"%s","rawNum_Num":"99999","selData":"kong","remarkApply":"","remarkAudit":"",'completeNumber':completeNum_Num},
                            success:function(data){if(data.result=="OK"){document.getElementById("result1_%s").innerHTML="录入成功!";}
                                                   else if(data.result=="NG"){document.getElementById("result1_%s").innerHTML="录入失败(完成数量输入有误),请检查!";}
                                                   else if(data.result=="RP"){document.getElementById("result1_%s").innerHTML="录入失败，完成数量超出采购数量(完成数量最大值只能填写采购数量)，请在备注填写超出部分!";}},
                            error:function(data){document.getElementById("result1_%s").innerHTML="录入失败(完成数量输入有误),请检查!";}
                        })})
                    })</script>"""
            rt = tt % (
            rt, input_id, input_id, input_id, obj.SKU,obj.productNumbers, input_id,input_id,input_id,input_id)
        except Exception as e:
            messages.info(self.request, u'%s,%s,加在数据存在问题题，请联系开发人员。' % (obj.SKU,str(e)))
            rt = ""
        return mark_safe(rt)

    show_complete.short_description = u'完成采购数量'

    def show_complete1(self, obj):
        try:
            input_id = str(obj.id)
            if obj.completeNumbers is None:
                completeNumbers = '0'
            else:
                completeNumbers = str(obj.completeNumbers)
            rt = u'<div><p id="completeNumbers_%s"  style="color:green;">%s</p></div>' % (input_id,completeNumbers)
        except Exception as e:
            messages.info(self.request, u'%s,%s,加在数据存在问题题，请联系开发人员。' % (obj.SKU,str(e)))
            rt = ""
        return mark_safe(rt)

    show_complete1.short_description = u'完成数量'

    def completeRemark(self, obj):
        try:
            input_id = str(obj.id)
            show_input_res = input_id
            OrderNum = ''
            BeyondNum = ''
            strOther = ''
            if obj.remarkDisPatch is None or str(obj.remarkDisPatch) == '':
                OrderNum = ''
                BeyondNum = ''
                strOther = ''
            else:
                listTmp = str(obj.remarkDisPatch).split('#@#')
                flag = 0
                for ele in listTmp:
                    if flag == 0:
                        OrderNum = listTmp[flag]
                    if flag == 1:
                        BeyondNum = listTmp[flag]
                    if flag == 2:
                        strOther = listTmp[flag]
                    flag += 1

            #messages.info(self.request, str(obj.unit) + "strSelect1:" + strSelect1 + ",strSelect2:" + strSelect2 + ",strSelect3:" + strSelect3)
            rt = '<font style="color:red">采购单号多个用英文(,)逗号分开</font><br><div id = "remarkDisPatch_%s" >' % (input_id,)
            #u'超出数量:<input type="text" style="width:150px" id="BeyondNum_%s" value="%s" /><br>' \
            rt = u'%s采购单号:<input type="text" style="width:150px" id="OrderNum_%s" value="%s" /><br>' \
                 u'其他信息:<input type="text" style="width:150px" id="Other_%s" value="%s" /><br>' \
                 u'<input type="button" id="btn_%s" value="确定" style="width:50px;">'\
                 u'<p id="result_%s" style="color:green;"></p></div>'%(rt,input_id,OrderNum,input_id,strOther,input_id,input_id,)

            tt = """%s<script>
                $(document).ready(function(){
                    $('#btn_%s').click(function(){
                        var OrderNum = document.getElementById("OrderNum_%s").value;
                        var strOther = document.getElementById("Other_%s").value;
                        $.ajax({url:"/BeyondNum/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",
                        data:{"id":"%s","SKU":"%s","OrderNum":OrderNum,"BeyondNum":0,"OtherInfo":strOther},
                        success:function(data){if(data.errorcode==0){ var strInfo = "Success,完成数量更新为:"+String(data.count);
                                                                      if(String(data.count) == "0"){strInfo="填写的采购单号从普元未获取到";}
                                                                      document.getElementById("result_%s").innerHTML=strInfo;
                                                                      document.getElementById("completeNumbers_%s").innerHTML=data.count;}
                                               else{var strInfo = "Fail,"+data.errortext; document.getElementById("result_%s").innerHTML=data.errorcode;}},
                        error:function(data){var strInfo = "Fail,"+data.errortext; document.getElementById("result_%s").innerHTML=strInfo;}
                    })})
                })</script>"""
            rt = tt % (rt,input_id,input_id,input_id,input_id,obj.SKU,input_id,input_id,input_id,input_id)
        except Exception as e:
            messages.info(self.request, u'商品(%s)读取存在问题，请联系开发人员查看原因。' % (obj.SKU))
            rt = ''
        return mark_safe(rt)
    completeRemark.short_description = u'填写信息'

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
        dispatchMan = obj.dispatchMan
        disPatchDate = obj.disPatchDate
        if obj.dispatchMan is None:
            dispatchMan = obj.auditMan
        if obj.disPatchDate is None:
            disPatchDate = obj.auditDate
        rt = u'<p style="width:200px;"><strong>商品名称:</strong>%s <br><strong>供应商名:</strong>%s <br><strong>商品状态:</strong>%s<br><strong>商品类别:</strong>%s<br>' \
             u'<strong>侵权站点:</strong>%s<br><strong>上一步处理人员:</strong>%s<br><strong>上一步处理时间:</strong>%s</p>' \
             % (obj.goodsName,obj.Supplier, obj.goodsState,obj.goodsclass,obj.TortInfo,dispatchMan,disPatchDate)
        return mark_safe(rt)
    GoodsInfo.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">商品及流程信息</p>')

    list_per_page = 20
    list_display = (
         'SKU','show_Picture', 'buyer', 'SalerName2','OSCode','GoodsInfo',
        'GoodsOther','ossNum', 'show_rawNumbers','show_complete1','completeRemark','show_confirmRemark')
    list_editable = ('remarkConfirm')

    fields = (
        'SKU', 'goodsName', 'Supplier', 'goodsState', 'OSCode','goodsCostPrice', 'oosNum', 'stockNum', 'ailableNum',
        'sevenSales', 'fifteenSales',
        'thirtySales', 'PurchaseNotInNum', 'buyer', 'productNumbers', 'loanMoney',
        'actualMoney', 'outFactory', 'rawNumbers', 'unit',
        'remarkApply', 'remarkApply', 'applyMan','auditMan','remarkAudit', )

    def get_list_queryset(self):
        request = self.request
        qs = super(t_cloth_factory_dispatch_confirm_Admin, self).get_list_queryset()
        ordertype = request.GET.get('ordertype', '')
        if ordertype == 'firstorder':
            qs = qs.filter(SpecialPurchaseFlag='firstorder')
        elif ordertype == 'customermade':
            qs = qs.filter(SpecialPurchaseFlag='customermade')
        elif ordertype == 'other':
            qs = qs.filter(SpecialPurchaseFlag='other')
        elif ordertype=='stockdemand':#obj.OSCode == 'OS906' and obj.Stocking_plan_number is not None and obj.Stocking_plan_number != '':
            qs = qs.filter(OSCode='OS906',Stocking_plan_number__isnull=False)
        elif ordertype=='otherall':
            qs = qs.filter(SpecialPurchaseFlag__isnull=True).filter(Stocking_plan_number__isnull=True)

        SKU = request.GET.get('SKU', '')
        Supplier = request.GET.get('Supplier', '')
        buyer = request.GET.get('buyer', '')
        buyer = buyer.split(',')
        if '' in buyer:
            buyer = ''
        oosNumStart = request.GET.get('oosNum_Start', '')
        oosNumEnd = request.GET.get('oosNum_End', '')

        goodsState = request.GET.get('goodsState', '')
        outFactory = request.GET.get('outFactory', '')
        from skuapp.table.goodsstatus_compare import goodsstatus_compare
        goodsstatus_compare_objs = goodsstatus_compare.objects.filter(py_GoodsStatus=goodsState).values_list(
            "hq_GoodsStatus", flat=True)

        createDateStart = request.GET.get('createDate_Start', '')
        createDateEnd = request.GET.get('createDate_End', '')

        searchList = {'SKU__contains': SKU,
                      'Supplier':Supplier,
                      'buyer__in': buyer,
                      'oosNum__gte': oosNumStart,
                      'oosNum__lt': oosNumEnd,
                      'goodsState__in':list(goodsstatus_compare_objs),
                      'createDate__gte': createDateStart,
                      'createDate__lt': createDateEnd,
                      'outFactory__contains':outFactory,
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
            return qs.filter(Q(currentState = 20)|Q(currentState = 22))
        buyer = request.user.first_name
        return qs.filter(Q(currentState = 20)|Q(currentState = 22),buyer=buyer)
        #return qs.filter(Q(currentState = 20)|Q(currentState = 22))


