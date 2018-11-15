# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fba_genbatch_Admin.py
 @time: 2018-08-14 16:24

"""   
from xadmin.layout import Fieldset, Row
from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
from skuapp.table.t_stocking_demand_fba_deliver import t_stocking_demand_fba_deliver
from django.utils.safestring import mark_safe
from .t_product_Admin import *
from skuapp.table.public import *
from pyapp.models import b_goods as py_b_goods
from datetime import datetime as ddtime
import datetime,random
from Project.settings import *
from skuapp.table.t_stocking_demand_fba_detail import t_stocking_demand_fba_detail

class t_stocking_demand_fba_genbatch_Admin(object):
    search_box_flag = True
    fba_tree_menu_flag = True
    hide_page_action = True
    downloadxls = True
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
            rt = u'<strong>商品SKU:</strong>%s<br><strong>店铺SKU:</strong>%s<br><strong>产品性质:</strong>%s<br><strong>商品名称:</strong>%s<br><strong>' \
                 u'计划需求人:</strong>%s<br><strong>供应商:</strong>%s<br><strong>采购人:</strong>%s<br><strong>普元备注:</strong>%s' \
                 u'<br><strong>物流信息:</strong>%s<br><strong>仓库:</strong>%s<br><strong>采购链接:</strong>%s' % (
                obj.ProductSKU,obj.ShopSKU, Product_nature_value, obj.ProductName,obj.Demand_people ,obj.Supplier,obj.Buyer,obj.pyRemark,strTmp,Warehouse_value,django_wrap(strSupplierlink, ';', 1))
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

        rt = """<img src="%s"  width="120" height="120"  title="%s" onerror="this.title=''" />  """ % (picture_url , picture_url)

        # rt =  '<img src="%s"  width="120" height="120"/>  '%(obj.ProductImage)
        return mark_safe(rt)
    show_ProductImage.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">商品图片</p>')

    def show_LogisticsNumber(self,obj) :
        rt = ''
        if obj.LogisticsNumber is not None and obj.LogisticsNumber.strip() != '':
            rt = rt + '<a target="_blank" href="https://www.baidu.com/s?wd=%s">%s</a>'%(obj.LogisticsNumber,obj.LogisticsNumber)
        return mark_safe(rt)
    show_LogisticsNumber.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">物流单号</p>')

    def show_Delivery_status(self, obj):
        try:
            rt = ""
            strStatus = ""
            diffDate = 0
            for status in getChoices(ChoiceFBAPlanStatus):
                if status[0] == obj.Status:
                    strStatus = status[1]
                    break
            if obj.Status == 'genbatch':
                diffDate = (ddtime.now() - obj.CheckTime).days if obj.CheckTime is not None else 0
                flag = 1 if ((obj.CheckTime is not None) and (
                            str(ddtime.now()) > str(obj.CheckTime + datetime.timedelta(days=2)))) else 0
                if flag==1:
                    rt = '<div class="box" style="width: 150px;height: 80px;background-color: red;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % ('待生成批次', diffDate)
                else:
                    rt = '<div class="box" style="width: 150px;height: 80px;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % ('待生成批次', diffDate)
            elif obj.Status == 'completedeliver':
                rt = '完成发货'
            elif obj.genStatus=='completegenbatch':
                rt = '完成生成批次'
            else:
                rt = strStatus
        except Exception, ex:
            messages.info(self.request, "pici状态加载错误,请联系IT解决:%s" % (str(ex)))
            rt = ""
        return mark_safe(rt)
    show_Delivery_status.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">批次状态</p>')

    def show_opInfo(self, obj):
        try:
            rt = u'<table border="1"><tr><th>操作员</th><th>告警信息</th><th>操作时间</th></tr>'
            if obj.Status == 'genbatch':
                diffDate1 = (obj.genPurchasePlanDate - obj.Stock_plan_date).days if (obj.Stock_plan_date is not None and obj.genPurchasePlanDate is not None) else 0
                diffDate2 = (obj.completePurchaseDate - obj.genPurchasePlanDate).days if (obj.recordPurchaseCodeDate is not None and obj.completePurchaseDate is not None) else 0
                diffDate3 = (obj.CheckTime - obj.completePurchaseDate).days if (obj.completePurchaseDate is not None and obj.CheckTime is not None) else 0
                diffDate4 = (ddtime.now() - obj.CheckTime).days if (obj.CheckTime is not None) else 0
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
                if diffDate4 > 2:
                    rt = rt + u'<tr style="color:red"><th>生成批次:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.genBatchMan, diffDate4, obj.genBatchDate)
                else:
                    rt = rt + u'<tr style=""><th>生成批次:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.genBatchMan, diffDate4, obj.genBatchDate)
            if obj.genStatus == 'completegenbatch':
                diffDate1 = (obj.genPurchasePlanDate - obj.Stock_plan_date).days if (obj.Stock_plan_date is not None and obj.genPurchasePlanDate is not None) else 0
                diffDate2 = (obj.completePurchaseDate - obj.genPurchasePlanDate).days if (obj.recordPurchaseCodeDate is not None and obj.completePurchaseDate is not None) else 0
                diffDate3 = (obj.CheckTime - obj.completePurchaseDate).days if (obj.completePurchaseDate is not None and obj.CheckTime is not None) else 0
                diffDate4 = (obj.genBatchDate - obj.CheckTime).days if (obj.CheckTime is not None and obj.genBatchDate is not None) else 0
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
                if diffDate4 > 2:
                    rt = rt + u'<tr style="color:red"><th>生成批次:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.genBatchMan, diffDate4, obj.genBatchDate)
                else:
                    rt = rt + u'<tr style=""><th>生成批次:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.genBatchMan, diffDate4, obj.genBatchDate)
            rt = rt + "</table>"
        except Exception, ex:
            messages.info(self.request,"操作记录加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_opInfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">操作记录信息</p>')

    def show_infors_number(self,obj) :
        try:
            if obj.Delivery_lot_number:
                rt = u'<strong>采购订单号:</strong>%s<br><strong>1688单号:</strong>%s<br><strong>物流单号:</strong>%s<br><strong>发货批次号:</strong>%s' % (
                    obj.Single_number, obj.Ali_number,obj.LogisticsNumber,obj.Delivery_lot_number )
            else:
                rt = u'<strong>采购订单号:</strong>%s<br><strong>1688单号:</strong>%s<br><strong>物流单号:</strong>%s' % (
                    obj.Single_number, obj.Ali_number, obj.LogisticsNumber)
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

    def checkDataInfo(self,obj) :
        try:
            rt = ""
            Check = "全检"
            if obj.isCheck == 0:
                Check = "全检"
            elif obj.isCheck == 1:
                Check = "抽检"
            else:
                Check = "免检"
            CheckNumber = 0 if obj.CheckNumber is None else obj.CheckNumber
            CheckQualified = 0 if obj.CheckQualified is None else obj.CheckQualified
            checkCompleteNum = 0 if obj.checkCompleteNum is None else obj.checkCompleteNum
            checkInferiorNum = 0 if obj.checkInferiorNum is None else obj.checkInferiorNum
            PercentOfPass = '0' if obj.PercentOfPass is None else str(obj.PercentOfPass)+'%'
            rt = u'<strong>质检选择:</strong>%s<br><strong>抽检数量:</strong>%s<br><strong>合格数量:</strong>%s<br><strong>合格率为:</strong>%s<br>' \
                 u'<strong>合格总量:</strong>%s<br><strong>次品总量:</strong>%s' % (
                Check, CheckNumber, CheckQualified,PercentOfPass,checkCompleteNum,checkInferiorNum)
        except Exception as e:
            messages.info(self.request, u'%s,%s,质检合格率加载数据存在问题题，请联系开发人员。' % (obj.ProductSKU, str(e)))
            rt = ""
        return mark_safe(rt)

    checkDataInfo.short_description = mark_safe(u'<p style="width:100px;color:#428bca;" align="center">质检合格率</p>')

    list_display = (
    'Stocking_plan_number','show_Delivery_status','Product_nature','Destination_warehouse','level', 'AccountNum','show_goodsInfo', 'show_ProductImage', 'show_infors_number',
    'purchaseNum', 'checkDataInfo', 'show_opInfo')
    list_editable = (
    'Single_number', 'Supplierlink', 'Ali_number', 'Arrival_date', 'Buyer', 'Logistics_costs', 'LogisticsNumber',
    'pay_method', 'Prepayments', 'QTY', 'Remarks', 'OplogTime', 'The_arrival_of_the_number')
    fields = (
    'Single_number', 'Supplier', 'Ali_number', 'Arrival_date', 'Buyer', 'QTY', 'Remarks', 'Supplierlink', 'OplogTime')

    actions = ['already_Ship','get_excel_to_py']


    def already_Ship(self, request, objs):
        from django.db import connection
        
        The_lot_number = 'SHIP' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-' + str(objs[0].id)
        myplan = []
        myproductinfo = []
        warehouselist = []
        Cargo_infor = []
        for obj in objs:
            if obj.Status == 'genbatch':
                myplan.append(obj.Stocking_plan_number)
                deliverNum = obj.The_arrival_of_the_number if obj.checkCompleteNum is None  else obj.checkCompleteNum
                myproductinfo.append(obj.ProductSKU + '*' + str(deliverNum))
                warehouselist.append(obj.Destination_warehouse)
                productinfo = [obj.ProductSKU,obj.Stocking_quantity,deliverNum,'',obj.ProductName,'']
                Cargo_infor.append(productinfo)

                t_stocking_demand_fba_detail.objects.filter(
                    Stocking_plan_number=obj.Stocking_plan_number).update(
                    Status='completegenbatch')

        if len(set(warehouselist)) > 1:
            messages.error(request,u'同一批次必须是同一目的地仓库！！！')
        elif len(set(warehouselist)) == 1:
            from brick.public.generate_excel import generate_excel
            from brick.public.create_dir import mkdir_p
            from Project.settings import BUCKETNAME_overseas_warehouse_cargo_infor_xls,MEDIA_ROOT
            import os,oss2
            from brick.public.upload_to_oss import upload_to_oss

            Cargo_infor.insert(0,['SKU',u'计划发货数量',u'实际发货数量',u'备注',u'产品名称',u'仓位'])

            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            # if not os.path.exists(path):
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

            mkdir_p(path)
            os.popen('chmod 777 %s' % (path))

            filename = request.user.username + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
            exresult = generate_excel(Cargo_infor,path + '/' + filename)
            if exresult['code'] == 0:
                os.popen(r'chmod 777 %s' % (path + '/' + filename))
                upload_to_oss_obj = upload_to_oss(BUCKETNAME_overseas_warehouse_cargo_infor_xls)
                uploadresult = upload_to_oss_obj.upload_to_oss({'path':request.user.username,'name':filename,'byte':open(path + '/' + filename),'del':1})
                if uploadresult['result'] == '':
                    messages.error(request, u'导出失败！请稍后 重试。。。')
                else:
                    objs.update(Delivery_lot_number=The_lot_number,Status='completegenbatch',genStatus='completegenbatch',genBatchMan=request.user.first_name, genBatchDate=ddtime.now())
                    t_stocking_demand_fba_deliver.objects.create(Stocking_plan_number='|'.join(myplan),
                                                         Cargo_infor=uploadresult['result'],
                                                         Delivery_lot_number=The_lot_number,
                                                         Destination_warehouse=warehouselist[0], OplogTime=ddtime.now(),
                                                         Status='deliver', All_ProductSKU_Num=';'.join(myproductinfo),editSKU=';'.join(myproductinfo))
            else:
                messages.error(request, u'导出失败！请稍后 重试。。。%s' % exresult['error'])
    already_Ship.short_description = u'生成发货批次'

    def get_excel_to_py(self, request, objs):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        # if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet(u'采购计划单')

        sheetlist = [u'需求人',u'备货计划号',u'采购订单',u'1688单号',u'sku',u'商品名称',u'图片',u'采购数量',
                     u'含税单价',u'仓库',u'供应商',u'采购链接',u'网页URL2',u'包装规格',u'预计到货日期',u'采购人',u'备货计划时间',u'采购状态',u'账号',u'备注',]

        for index,item in enumerate(sheetlist):
            sheet.write(0,index,item)

        # 写数据
        idlist = []
        row = 0
        for qs in objs:

            row = row + 1

            column = 0
            sheet.write(row, column, qs.Demand_people)  # 需求人

            column = column + 1
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
            sheet.write(row, column, qs.QTY) # 采购数量

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
            PackName = ''
            py_b_goods_obj = py_b_goods.objects.filter(SKU = qs.ProductSKU).values('LinkUrl2','PackName')
            if py_b_goods_obj.exists():
                URL2 = py_b_goods_obj[0]['LinkUrl2']
                PackName = py_b_goods_obj[0]['PackName']
            sheet.write(row, column, URL2)  # 网页URL2
            column = column + 1
            sheet.write(row, column, PackName)  # 包装规格

            column = column + 1
            sheet.write(row, column, qs.Arrival_date)  # 预计到货日期

            column = column + 1
            sheet.write(row, column, qs.Buyer) # 采购人

            column = column + 1
            sheet.write(row, column, '%s'%qs.Stock_plan_date) # 备货计划时间

            column = column + 1
            sta = u'未采购'
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
        objs.filter(id__in=idlist).update(ExcelStatus='yes')
        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                    filename) + u':成功导出,可点击Download下载到本地............................。')

    get_excel_to_py.short_description = u'导出Excel表格'


    def get_list_queryset(self):
        request=self.request
        qs = super(t_stocking_demand_fba_genbatch_Admin, self).get_list_queryset()

        from django.contrib.auth.models import User
        userID = [each.id for each in User.objects.filter(groups__id__in=[65])]
        # if request.user.is_superuser or request.user.id in userID:
        if request.user.id in userID:
            qs = qs.filter(Demand_people=request.user.first_name)
        Status = request.GET.get('Status', '')  # 采购状态
        genStatus = ''
        if Status == 'completegenbatch':
            genStatus = 'completegenbatch'
            Status = ''

        Delivery_lot_number = request.GET.get('Delivery_lot_number', '')  # 采购状态
        #Status = request.GET.get('Status', '')  # 采购状态
        Stocking_plan_number = request.GET.get('Stocking_plan_number', '')  # 备货计划号
        Stock_plan_dateStart = request.GET.get('Stock_plan_dateStart', '')  # 备货计划时间
        Stock_plan_dateEnd = request.GET.get('Stock_plan_dateEnd', '')  # 备货计划时间
        Demand_people = request.GET.get('Demand_people', '')  # 计划需求人
        Product_nature = request.GET.get('Product_nature', '')  # 产品性质
        ProductSKU = request.GET.get('ProductSKU', '')  # 商品sku
        ProductName = request.GET.get('ProductName', '')  # 商品名称
        ProductWeightStart = request.GET.get('ProductWeightStart', '')
        ProductWeightEnd = request.GET.get('ProductWeightEnd', '')  # 商品克重
        Supplier = request.GET.get('Supplier', '')  # 供应商
        AccountNum = request.GET.get('AccountNum', '')  # 帐号
        Destination_warehouse = request.GET.get('Destination_warehouse', '')  # 目的地仓库
        level = request.GET.get('level', '')  # 紧急程度
        Buyer = request.GET.get('Buyer', '')  # 采购人
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
            'Delivery_lot_number__contains': Delivery_lot_number,
            'Stocking_plan_number__exact': Stocking_plan_number,
            'Stock_plan_date__gte': Stock_plan_dateStart, 'Stock_plan_date__lt': Stock_plan_dateEnd,
            'Demand_people__exact': Demand_people, 'Product_nature__exact': Product_nature,
            'ProductSKU__icontains': ProductSKU, 'ProductName__exact': ProductName,
            'ProductWeight__gte': ProductWeightStart,
            'ProductWeight__lt': ProductWeightEnd,
            'Supplier__exact': Supplier,
            'AccountNum__exact': AccountNum,
            'Destination_warehouse__exact': Destination_warehouse,
            'level__exact': level, 'isCheck__exact': isCheck,
            'Buyer__exact': Buyer,
            'Status__exact': Status,'genStatus__exact':genStatus,
            'OplogTime__gte': OplogTimeStart, 'OplogTime__lt': OplogTimeEnd,
            'neworold__exact': neworold,
            'QTYStart': QTYStart, 'QTYEnd': QTYEnd, 'LogisticsNumber__exact': LogisticsNumber,
            'Single_number__exact': Single_number, 'Ali_number__exact': Ali_number,
            'Stocking_quantityStart': Stocking_quantityStart, 'Stocking_quantityEnd': Stocking_quantityEnd,
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

        return qs