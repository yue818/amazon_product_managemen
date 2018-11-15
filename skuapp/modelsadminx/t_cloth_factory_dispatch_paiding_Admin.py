# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_paiding_Admin.py
 @time: 2018/4/28 8:53
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_cloth_factory_dispatch_confirm import *
from django.contrib import messages
from django.db.models import Q
from django.utils.safestring import mark_safe
from datetime import datetime as paidDate
from Project.settings import *
import oss2
from xlwt import *
from .t_product_Admin import *
from django.db import connection

class t_cloth_factory_dispatch_paiding_Admin(object):
    actions = ['to_next_deliver','tran_factory','to_import_execl']
    t_cloth_factory = True
    search_box_flag = True
    downloadxls = True
    hide_page_action = True
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
            sheet = w.add_sheet(u'服装工厂生产订单')
            style = XFStyle()

            sheet.write(0, 0, u'日期', style)  # 日期
            sheet.write(0, 1, u'商品SKU', style)  # SKU
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
            sheet.write(0, 12, u'订单号', style)  # 订单号

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
                    diffDay = (paidDate.now() - obj.auditDate).days
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

                if obj.OrderNo is not None:
                    sheet.write(row, 12, str(obj.OrderNo), style)  # 订单号
                else:
                    sheet.write(row, 12, '', style)  # 订单号
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
        except Exception as e:
            messages.info(self.request,"导出数据到execl报错:%s，请联系开发人员"%(str(e)))
    to_import_execl.short_description = u'导出数据到execl'

    def tran_factory(self, request, objs):
        try:
            errorList = []
            cursor = connection.cursor()
            for obj in objs:
                if str(obj.currentState) == '16':
                    #查看工厂承包类型 10 包工包料   11 包工不包料
                    strSelectSql = "select type from t_cloth_factory where name='%s'"%(obj.outFactory)
                    cursor.execute(strSelectSql)
                    typeRecord = cursor.fetchone()
                    costPrice = 0
                    if len(typeRecord) == 0 or typeRecord[0] == 10:
                        costPrice = obj.goodsCostPrice
                    else:
                        strSelectSql = "select ProcessCosts from t_supply_chain_production_basic where MainSKU=(select MainSKU from t_product_mainsku_sku where ProductSKU='%s' limit 1) limit 1"%(obj.SKU)
                        cursor.execute(strSelectSql)
                        processCostRecord = cursor.fetchone()
                        if processCostRecord:
                            costPrice = processCostRecord[0]
                    #OS901 7,OS902 6,OS903 7,OS904 15,OS905 6,OS906 7,OS909 6
                    days = OSCODE_DICT[obj.OSCode] if (obj.OSCode in OSCODE_DICT.keys()) else 6
                    size =  obj.SKU.split('-')[-1] if ('-' in obj.SKU) else obj.SKU
                    #入仓库类型
                    storeID = '19'
                    if obj.SpecialPurchaseFlag is not None and obj.SpecialPurchaseFlag == "customermade":
                        storeID = '82'
                    strInsertSql = "insert into factory_db.t_factory_order_info(OrderNID,OrderStatus,StockType,OrderDate,SKU,Price,Size,Number,OsCode,Merchandiser,OutFactory,Note,OriginalNID,storeID) " \
                                   "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    param = (obj.OrderNo,'ordered',obj.OSCode, paidDate.now(),obj.SKU,costPrice,size,obj.productNumbers,str(days),obj.buyer,obj.outFactory,obj.FactoryRemark,obj.id,storeID)
                    cursor.execute(strInsertSql,param)
                    obj.dispatchMan = request.user.first_name
                    obj.disPatchDate = paidDate.now()
                    obj.currentState='18'
                    obj.save()
                else:
                    errorList.append(obj.SKU)
            cursor.close()
            connection.commit()
            if len(errorList) > 0:
                messages.error(request, u'以下SKU：%s,已转工厂生产，请勿重复提交。'%(errorList))
            messages.info(request, u'转工厂生产处理成功。')
        except Exception as e:
            messages.error(request,u'转工厂生产处理错误:%s，请联系IT查看'%(e))
    tran_factory.short_description = u'转工厂生产'

    def to_next_deliver(self, request, objs):
        try:
            listSKU = []
            for obj in objs:
                if str(obj.currentState) == '16':
                    obj.dispatchMan = request.user.first_name
                    obj.disPatchDate = paidDate.now()
                    obj.currentState = '20'
                    obj.save()
                else:
                    listSKU.append(obj.SKU)
            if len(listSKU) > 0:
                messages.info(request,u"商品编码：" + str(listSKU) + u",已转新系统生产,待新系统生产完成到货后自动更新记录。")
        except Exception as e:
            messages.info(self.request, u'%s,%s,提交审核通过报错，请联系开发人员。' % (obj.SKU,str(e)))
    to_next_deliver.short_description = u'转->检验交付数量和单价'

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

    def show_rawNumbers(self, obj):
        rt = u'<strong>原材料数量:</strong>%s(%s) <br><strong>采购数量:</strong>%s<br><strong>外派工厂:</strong>%s<br><strong>采购备注:</strong>%s<br><strong>审核备注:</strong>%s' % (
        obj.rawNumbers, obj.unit, obj.productNumbers, obj.outFactory, obj.remarkApply, obj.remarkSpeModify)

        return mark_safe(rt)
    show_rawNumbers.short_description = mark_safe('<p align="center" style="width:150px;color:#428bca;">排单信息</p>')

    def show_confirmRemark(self, obj):
        diffDay = 0
        if obj.auditDate is not None:
           diffDay = (paidDate.now() - obj.auditDate).days
        rt = u"<div align='center'><font color='black'>%s天</font></div><br>" % (diffDay)
        if obj.OSCode == 'OS901' or not obj.OSCode:
            if diffDay > 7:
                rt = u"<div align='center'><font style='font-weight:bold;' color='red'>%s天</font></div><br>" % (diffDay)
        elif obj.OSCode == 'OS902' or obj.OSCode == 'OS905':
            if diffDay > 8:
                rt = u"<div align='center'><font style='font-weight:bold;' color='red'>%s天</font></div><br>" % (diffDay)
        elif obj.OSCode == 'OS903':
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
        rt = u'<p style="width:200px;"><strong>商品名称:</strong>%s <br><strong>供应商名:</strong>%s <br><strong>商品状态:</strong>%s<br><strong>商品类别:</strong>%s<br><strong>侵权站点:</strong>%s<br><strong>上一步处理人员:</strong>%s<br><strong>上一步处理时间:</strong>%s</p>' % (obj.goodsName,obj.Supplier, obj.goodsState,obj.goodsclass,obj.TortInfo,obj.auditMan,obj.auditDate)
        return mark_safe(rt)
    GoodsInfo.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">商品及流程信息</p>')

    def OrderInfo(self,obj):
        try:
            input_id = str(obj.id)
            rt = '<div id = "planOrder_%s">' % (input_id,)
            FactoryRemark = '' if obj.FactoryRemark is None else obj.FactoryRemark
            if str(obj.currentState) == '16':
                rt = u'%s<strong>转工厂生产备注</strong>:<input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_cloth_factory_dispatch_needpurchase\')" ' \
                     u'%s title="%s"/><span id="%s"></span></br>' \
                     u'<strong>转工厂生产订单号</strong>:%s<br>' \
                     u'<input type="button" style="width:100px;hight:35px;margin-left:0px" id="btn_%s" value="转工厂生产"><br>' \
                     u'<p id="result_%s"  style="color:green;"></p></div>' \
                     % (rt, FactoryRemark,input_id,'FactoryRemark','',FactoryRemark,str(input_id)+'_FactoryRemark',
                        obj.OrderNo, input_id,input_id)

                tt = """%s<script>                   
                        $(document).ready(function(){            
                            $("#btn_%s").click(function(){
                                document.getElementById("btn_%s").disabled="true";
                                $.ajax({url:"/t_cloth_factory_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",
                                data:{"id":"%s","SKU":"%s","productNumbers_Num":0,"rawNum_Num":0,"selData":'',"remarkApply":'',"remarkAudit":'','completeNumber':0,'dispatchfactory':'dispatchfactory'},
                                success:function(data){if(data.result=="OK"){document.getElementById("result_%s").innerHTML="转工厂生产成功!";}
                                                       else if(data.result=="NG"){document.getElementById("result_%s").innerHTML="转工厂生产失败,请检查!";}},
                                error:function(data){document.getElementById("result_%s").innerHTML="转工厂生产失败,请检查!";}
                            })})
                        })</script>"""
                rt = tt % (
                rt, input_id,input_id, input_id, obj.SKU, input_id, input_id,input_id)
            else:
                diffDay = 0
                if obj.disPatchDate is not None:
                    diffDay = (paidDate.now() - obj.disPatchDate).days
                tt = u"<font color='black'><strong>转工厂生产中</strong>:%s天</font><br>" % (diffDay)
                if obj.OSCode == 'OS901' or not obj.OSCode:
                    if diffDay > 7:
                        tt = u"<font style='font-weight:bold;' color='red'>转工厂生产中:%s天</font><br>" % (diffDay)
                elif obj.OSCode == 'OS902' or obj.OSCode == 'OS905':
                    if diffDay > 8:
                        tt = u"<font style='font-weight:bold;' color='red'>转工厂生产中:%s天</font><br>" % (diffDay)
                elif obj.OSCode == 'OS903':
                    if diffDay > 10:
                        tt = u"<font style='font-weight:bold;' color='red'>转工厂生产中:%s天</font><br>" % (diffDay)
                elif obj.OSCode == 'OS904':
                    if diffDay > 15:
                        tt = u"<font style='font-weight:bold;' color='red'>转工厂生产中:%s天</font><br>" % (diffDay)
                elif obj.OSCode == 'OS909':
                    if diffDay > 6:
                        tt = u"<font style='font-weight:bold;' color='red'>转工厂生产中:%s天</font><br>" % (diffDay)
                else:
                    tt = tt
                rt = '%s<strong>转工厂生产备注</strong>:%s<br><strong>转工厂生产订单号</strong>:%s<br>%s</div>'%(rt,FactoryRemark,obj.OrderNo,tt)
        except Exception as e:
            messages.info(self.request, u'%s,%s,加在数据存在问题，请联系开发人员。' % (obj.SKU,str(e)))
            rt = ""
        return mark_safe(rt)
    OrderInfo.short_description = mark_safe(u'<p style="width:150px;color:#428bca;" align="center">生产订单</p>')

    list_per_page = 20
    list_display = (
         'SKU','show_Picture', 'buyer', 'SalerName2','OSCode','GoodsInfo',
        'GoodsOther','ossNum', 'show_rawNumbers','OrderInfo')
    list_editable = ('remarkConfirm')

    fields = (
        'SKU', 'goodsName', 'Supplier', 'goodsState', 'OSCode','goodsCostPrice', 'oosNum', 'stockNum', 'ailableNum',
        'sevenSales', 'fifteenSales',
        'thirtySales', 'PurchaseNotInNum', 'buyer', 'productNumbers', 'loanMoney',
        'actualMoney', 'outFactory', 'rawNumbers', 'unit',
        'remarkApply', 'remarkApply', 'applyMan','auditMan','remarkAudit', )

    def get_list_queryset(self):
        request = self.request
        qs = super(t_cloth_factory_dispatch_paiding_Admin, self).get_list_queryset()
        SKU = request.GET.get('SKU', '')
        Supplier = request.GET.get('Supplier', '')
        buyer = request.GET.get('buyer', '')
        buyer = buyer.split(',')
        if '' in buyer:
            buyer = ''
        ordertype = request.GET.get('ordertype', '')
        if ordertype == 'firstorder':
            qs = qs.filter(SpecialPurchaseFlag='firstorder')
        elif ordertype == 'customermade':
            qs = qs.filter(SpecialPurchaseFlag='customermade')
        elif ordertype == 'other':
            qs = qs.filter(SpecialPurchaseFlag='other')
        elif ordertype == 'stockdemand':  # obj.OSCode == 'OS906' and obj.Stocking_plan_number is not None and obj.Stocking_plan_number != '':
            qs = qs.filter(OSCode='OS906', Stocking_plan_number__isnull=False)
        elif ordertype == 'otherall':
            qs = qs.filter(SpecialPurchaseFlag__isnull=True).filter(Stocking_plan_number__isnull=True)

        currentState = request.GET.get('currentState', '')
        outFactory = request.GET.get('outFactory', '')
        OrderNo = request.GET.get('OrderNo', '')

        createDateStart = request.GET.get('createDate_Start', '')
        createDateEnd = request.GET.get('createDate_End', '')

        searchList = {'SKU__icontains': SKU,
                      'Supplier':Supplier,
                      'buyer__in': buyer,
                      'OrderNo__icontains':OrderNo,
                      'createDate__gte': createDateStart,
                      'createDate__lt': createDateEnd,
                      'outFactory__icontains':outFactory,
                      'currentState__exact':currentState,
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
            return qs
        buyer = request.user.first_name
        return qs.filter(buyer=buyer)
        #return qs.filter(Q(currentState = 20)|Q(currentState = 22))


