# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_stocking_purchase_order_Admin.py
 @time: 2017-12-19 15:58

"""
from xadmin.layout import Fieldset, Row
from skuapp.table.t_stocking_demand_list import t_stocking_demand_list
from skuapp.table.t_set_warehouse_storage_situation_list import t_set_warehouse_storage_situation_list
from django.utils.safestring import mark_safe
from .t_product_Admin import *
from skuapp.table.public import *
from pyapp.models import b_goods as py_b_goods
from datetime import datetime as ddtime
import datetime,random

class t_stocking_purchase_order_Admin(object):
    downloadxls = True
    search_box_flag = True
    purchase_order = False
    jump_temp = False
    purchase_order_plugin = True
    site_left_menu_stocking_purchase = True
    # search_box_flag = True
    def show_ProductImage(self,obj) :
        rt =  '<img height = 120px width = 120px src="%s" />'%(obj.ProductImage)
        return mark_safe(rt)
    show_ProductImage.short_description = u'商品图片'

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
                if status[0] == obj.Warehouse:
                    Warehouse_value = status[1]
                    break
            if obj.LogisticsNumber is not None and obj.LogisticsNumber.strip() != '':
                strTmp =  '<a target="_blank" href="https://www.baidu.com/s?wd=%s">查看物流</a>' % obj.LogisticsNumber
            strSupplierlink = obj.Supplierlink if obj.Supplierlink is not None else ""
            rt = u'<strong>商品SKU:</strong>%s<br><strong>店铺SKU:</strong>%s<br><strong>产品性质:</strong>%s<br><strong>商品名称:</strong>%s<br><strong>' \
                 u'计划需求人:</strong>%s<br><strong>供应商:</strong>%s<br><strong>采购人:</strong>%s<br><strong>备注:</strong>%s' \
                 u'<br><strong>物流信息:</strong>%s<br><strong>仓库:</strong>%s<br><strong>采购链接:</strong>%s' % (
                obj.ProductSKU, obj.ShopSKU, Product_nature_value, obj.ProductName,obj.Demand_people ,obj.Supplier,obj.Buyer,obj.Remarks,strTmp,Warehouse_value,django_wrap(strSupplierlink, ';', 1))
            return mark_safe(rt)
        except Exception, ex:
            messages.info(self.request,"商品信息加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
    show_goodsInfo.short_description = u'商品信息'

    def show_Status(self, obj):
        try:
            rt = ""
            strStatus = ""
            for status in getChoices(ChoicePurchStatus):
                if status[0] == obj.Status:
                    strStatus = status[1]
                    break
            if  obj.Status == 'notyet':
                diffDate = (ddtime.now() - obj.TheTime).days if obj.TheTime is not None else 0
                flag = 1 if ((obj.TheTime is not None) and (str(ddtime.now()) > str(obj.TheTime + datetime.timedelta(days=2)))) else 0
                if flag == 1:
                    rt = '<div class="box" style="width: 150px;height: 80px;background-color: red;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天' % (strStatus,diffDate)
                else:
                    rt = '<div class="box" style="width: 150px;height: 80px;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (strStatus,diffDate)
            else:
                rt = strStatus
        except Exception, ex:
            messages.info(self.request,"采购状态加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_Status.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">采购状态</p>')

    def show_opInfo(self, obj):
        try:
            rt = u'<table border="1" ><tr><th>操作员</th><th>告警信息</th><th>操作时间</th></tr>'
            t_stocking_demand_list_obj = t_stocking_demand_list.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).values('Demand_people','Stock_plan_date', 'Auditor',
                                        'AuditTime','submitAuditMan','submitAuditDate','genPurchasePlanMan','genPurchasePlanDate')
            if len(t_stocking_demand_list_obj) > 0:
                diffDate1 = (t_stocking_demand_list_obj[0]['AuditTime'] - t_stocking_demand_list_obj[0]['Stock_plan_date']).days if (t_stocking_demand_list_obj[0]['AuditTime'] is not None and t_stocking_demand_list_obj[0]['Stock_plan_date'] is not None) else 0
                diffDate2 = (t_stocking_demand_list_obj[0]['genPurchasePlanDate'] - t_stocking_demand_list_obj[0]['AuditTime']).days if (t_stocking_demand_list_obj[0]['AuditTime'] is not None and t_stocking_demand_list_obj[0]['genPurchasePlanDate'] is not None) else 0
                diffDate3 = 0
                if obj.completeInstoreDate:
                    diffDate3 = (obj.completeInstoreDate - t_stocking_demand_list_obj[0]['genPurchasePlanDate']).days if (
                            t_stocking_demand_list_obj[0]['genPurchasePlanDate'] is not None) else 0
                else:
                    diffDate3 = (ddtime.now() - t_stocking_demand_list_obj[0]['genPurchasePlanDate']).days if (
                            t_stocking_demand_list_obj[0]['genPurchasePlanDate'] is not None) else 0

                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_demand_list_obj[0]['Demand_people'], diffDate1, t_stocking_demand_list_obj[0]['Stock_plan_date'])
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_demand_list_obj[0]['Demand_people'], diffDate1,t_stocking_demand_list_obj[0]['Stock_plan_date'])
                if diffDate2 > 2:
                    rt = rt + u'<tr style="color:red"><th>审核:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_demand_list_obj[0]['Auditor'], diffDate2, t_stocking_demand_list_obj[0]['AuditTime'])
                else:
                    rt = rt + u'<tr style=""><th>审核:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_demand_list_obj[0]['Auditor'], diffDate2, t_stocking_demand_list_obj[0]['AuditTime'])
                if diffDate3 > 2:
                    rt = rt + u'<tr style="color:red"><th>生成采购:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_demand_list_obj[0]['genPurchasePlanMan'], diffDate3, t_stocking_demand_list_obj[0]['genPurchasePlanDate'])
                else:
                    rt = rt + u'<tr style=""><th>生成采购:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_demand_list_obj[0]['genPurchasePlanMan'], diffDate3, t_stocking_demand_list_obj[0]['genPurchasePlanDate'])
                if obj.completeInstoreDate:
                    rt = rt + u'<tr style=""><th>完成采购:%s</th><th></th><th>%s</th></tr>' % (obj.completeInstoreMan, obj.completeInstoreDate)

            rt = rt + "</table>"
        except Exception, ex:
            messages.info(self.request,"操作信息加载错误,请联系IT解决:%s"%(str(ex)))
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

    def del_None(self,col):
        rt = col
        if not col:
            rt = ''
        return rt

    def show_infors_number(self,obj) :
        read = ''
        if obj.Status == 'already':
            read = 'readonly'
        rt = '<table>'
        rt = u'%s<tr><th>采购订单号/调拨单号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_purchase_order\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
             u'<tr><th>1688单号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_purchase_order\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt,self.del_None(obj.Single_number),obj.id,'Single_number',read,self.del_None(obj.Single_number),str(obj.id)+'_Single_number',
              self.del_None(obj.Ali_number),obj.id,'Ali_number',read,self.del_None(obj.Ali_number),str(obj.id)+'_Ali_number',)

        rt = u'%s<tr><th>物流单号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_purchase_order\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt,self.del_None(obj.LogisticsNumber),obj.id,'LogisticsNumber',read,self.del_None(obj.LogisticsNumber),str(obj.id)+'_LogisticsNumber')

        rt = u'%s<tr><th>供应商：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_purchase_order\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.Supplier), obj.id, 'Supplier', read,
              self.del_None(obj.Supplier), str(obj.id) + '_Supplier')
        rt = u'%s<tr><th>采购员：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_purchase_order\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.Buyer), obj.id, 'Buyer', read,
              self.del_None(obj.Buyer), str(obj.id) + '_Buyer')
        rt = u'%s<tr><th>采购链接：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_purchase_order\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.Supplierlink), obj.id, 'Supplierlink', read,
              self.del_None(obj.Supplierlink), str(obj.id) + '_Supplierlink')

        rt = rt + '</table>'

        return mark_safe(rt)
    show_infors_number.short_description = u'单号信息'

    list_display = ('Stocking_plan_number','show_Status','show_infors_number', 'show_goodsInfo','Supplier','show_ProductImage','Stocking_quantity','QTY',
                    'The_arrival_of_the_number','Arrival_date','level','AccountNum','Remarks','show_opInfo')
    list_editable = ('Single_number', 'Supplierlink' ,'Ali_number', 'Arrival_date', 'Contract_No',
                      'Buyer', 'Logistics_costs', 'LogisticsNumber','pay_method','Prepayments','QTY','Remarks','OplogTime','The_arrival_of_the_number')
    fields = ('Single_number', 'Supplier', 'Ali_number', 'Arrival_date', 'Contract_No',
              'Buyer', 'Logistics_costs', 'pay_method','Prepayments','QTY','Remarks',
              'Supplierlink','OplogTime')

    form_layout = (
        Fieldset(u'请认真填写',
                 Row('Single_number', 'Contract_No', '', ),
                 Row('Supplier', 'Supplierlink', '', ),
                 Row('Ali_number', 'Arrival_date', 'Buyer', ),
                 Row('Logistics_costs', 'pay_method', 'Prepayments', ),
                 Row('QTY', '', '', ),
                 Row('Remarks', '', '', ),
                 css_class='unsort '
                 ),)

    actions = ['to_syn','alreadly_purchased','splitPurchase','get_excel_to_py']

    def to_syn(self,request,objs):
        from app_djcelery.tasks import syn_Logistics_number
        insertinto = []
        for obj in objs:
            insertinto.append(obj.Single_number)
        syn_Logistics_number.delay(insertinto)
        messages.success(request,u'正在执行，请稍后刷新页面。。。')
    to_syn.short_description = u'同步物流信息'


    def alreadly_purchased(self,request,objs):
        try:
            insertinto = []
            errorInfo = []
            for obj in objs:
                if (obj.Status == 'notyet' or obj.Status == 'purchasing') and obj.The_arrival_of_the_number is not None and int(obj.The_arrival_of_the_number)<=obj.QTY and obj.Single_number is not None:
                    arrNum = obj.The_arrival_of_the_number if obj.The_arrival_of_the_number is not None else 0
                    insertinto.append(t_set_warehouse_storage_situation_list(
                        Stocking_plan_number = obj.Stocking_plan_number,Purchase_Order_No = obj.Single_number,
                        Destination_warehouse = obj.Warehouse,ProductSKU = obj.ProductSKU,ProductImage = obj.ProductImage,
                        Price = obj.Price,Stocking_quantity = obj.Stocking_quantity,LogisticsNumber=obj.LogisticsNumber,
                        Weight = obj.Weight,Delivery_status = 'notyet',Arrival_status = 'already',ProductName = obj.ProductName,
                        Remarks = obj.Remarks,Storage_status = 'already',QTY = obj.QTY,level = obj.level,Site=obj.Site,
                        Product_nature=obj.Product_nature,Demand_people=obj.Demand_people,AccountNum=obj.AccountNum,ShopSKU=obj.ShopSKU,OplogTime=ddtime.now(),StorageDate = ddtime.now(),
                        Arrival_date=ddtime.now(),Stock_plan_unfinished_quantity = obj.Stocking_quantity - arrNum,
                        The_arrival_of_the_number=obj.The_arrival_of_the_number,checkStatus = 'notcheck'
                    ))

                    obj.Status = 'already'
                    obj.Arrival_status = 'already'
                    obj.Storage_status = 'already'
                    obj.Arrival_date1 = ddtime.now()
                    obj.StorageDate = ddtime.now()
                    obj.completeInstoreMan = request.user.first_name
                    obj.completeInstoreDate = ddtime.now()
                    obj.save()

                    t_stocking_demand_list.objects.filter(Stocking_plan_number = obj.Stocking_plan_number).update(Status = 'already',completePurchaseDate=ddtime.now(),completePurchaseMan=request.user.first_name)
                else:
                    errorInfo.append(obj.Stocking_plan_number)
            t_set_warehouse_storage_situation_list.objects.bulk_create(insertinto)
            if errorInfo:
                messages.info(request,u"以下不能提交完成入库备货计划号：%s,可能由于未生成采购订单号或本次到货数量未填写。"%(errorInfo))
        except Exception, ex:
            messages.info(self.request,"完成入库报错,请联系开发人员解决:%s"%(str(ex)))
    alreadly_purchased.short_description = u'完成入库'

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

        sheetlist = [u'备货计划号',u'采购订单/调拨单号',u'1688单号',u'sku',u'商品名称',u'图片',u'采购数量',
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
            sheet.write(row, column, qs.QTY) # 采购数量

            column = column + 1
            sheet.write(row, column, qs.Price) # 含税单价

            column = column + 1
            Destination_warehouse = ''
            for warehouse in getChoices(ChoiceWarehouse):
                if warehouse[1] is not None and qs.Warehouse == warehouse[0].strip():
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
            if qs.Status == 'already':
                sta = u'已采购'
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

    def splitPurchase(self, request, objs):
        try:
            #拆分订单  未采购量=采购数量-已到货数量
            insertPurchaseOrderinto = []
            insertDemandListInto = []
            insertStorageInto = []
            errorInfo = []
            successInto = []
            from skuapp.table.t_stocking_purchase_order import t_stocking_purchase_order
            for obj in objs:
                if (obj.Status == "notyet" or obj.Status == "purchasing" ) and obj.The_arrival_of_the_number is not None and int(obj.The_arrival_of_the_number)<obj.QTY and obj.Single_number is not None:
                    arrNum = obj.The_arrival_of_the_number if obj.The_arrival_of_the_number is not None else 0
                    unInStockNum = obj.QTY - arrNum
                    insertPurchaseOrderinto.append(t_stocking_purchase_order(
                        Stocking_plan_number=str(obj.Stocking_plan_number)+"_1", Stock_plan_date = obj.Stock_plan_date,
                        ProductSKU=obj.ProductSKU, ShopSKU=obj.ShopSKU,Product_nature=obj.Product_nature,
                        ProductName = obj.ProductName,ProductImage = obj.ProductImage,Stocking_quantity = unInStockNum,
                        QTY = unInStockNum,Price=obj.Price, Weight=obj.Weight, Remarks=obj.Remarks, Supplier=obj.Supplier,
                        Supplierlink=obj.Supplierlink,Buyer=obj.Buyer,ThePeople=obj.ThePeople,TheTime=obj.TheTime,
                        Warehouse=obj.Warehouse,Status='notyet',UpdateTime=ddtime.now(),Demand_people=obj.Demand_people,
                        level=obj.level,Site=obj.Site,AccountNum = obj.AccountNum,OplogTime=ddtime.now(),splitMan=request.user.first_name,
                        splitTime=ddtime.now(),splitRemark=u'被拆分订单;由订单号%s拆分'%(obj.Stocking_plan_number)
                    ))

                    insertStorageInto.append(t_set_warehouse_storage_situation_list(
                        Stocking_plan_number=obj.Stocking_plan_number, Purchase_Order_No=obj.Single_number,
                        Destination_warehouse=obj.Warehouse, ProductSKU=obj.ProductSKU, ProductImage=obj.ProductImage,
                        Price=obj.Price, Stocking_quantity=obj.Stocking_quantity, LogisticsNumber=obj.LogisticsNumber,
                        Weight=obj.Weight, Delivery_status='notyet', Arrival_status='already',
                        ProductName=obj.ProductName,The_arrival_of_the_number=arrNum,Stock_plan_unfinished_quantity=unInStockNum,
                        Remarks=obj.Remarks+";未采购部分已被拆分为订单:%s_1"%(obj.Stocking_plan_number), Storage_status='already', QTY=obj.QTY, level=obj.level, Site=obj.Site,
                        Product_nature=obj.Product_nature, Demand_people=obj.Demand_people, AccountNum=obj.AccountNum,
                        ShopSKU=obj.ShopSKU, OplogTime=ddtime.now(), StorageDate=ddtime.now(),
                        Arrival_date=ddtime.now(),checkStatus = 'notcheck'
                    ))
                    t_stocking_demand_list_obj = t_stocking_demand_list.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).values('Stock_plan_date','Demand_people','Product_nature',
                                                  'ProductSKU','ShopSKU','ProductName','ProductImage','ProductPrice','ProductWeight','Supplier','Supplierlink',
                                                  'Stocking_quantity','AccountNum','Site','Destination_warehouse','level','Auditor','AuditTime','Buyer','Remarks','Status','UpdateTime',
                                                  'neworold','OplogTime','submitAuditMan','submitAuditDate','genPurchasePlanMan','genPurchasePlanDate')
                    insertDemandListInto.append(t_stocking_demand_list(
                        Stocking_plan_number = str(obj.Stocking_plan_number)+"_1",Stock_plan_date = t_stocking_demand_list_obj[0]['Stock_plan_date'],
                        Demand_people = t_stocking_demand_list_obj[0]['Demand_people'],Product_nature = t_stocking_demand_list_obj[0]['Product_nature'],
                        ProductSKU=t_stocking_demand_list_obj[0]['ProductSKU'],ShopSKU = t_stocking_demand_list_obj[0]['ShopSKU'],
                        ProductName=t_stocking_demand_list_obj[0]['ProductName'],ProductImage = t_stocking_demand_list_obj[0]['ProductImage'],
                        ProductPrice=t_stocking_demand_list_obj[0]['ProductPrice'],ProductWeight = t_stocking_demand_list_obj[0]['ProductWeight'],
                        Supplier=t_stocking_demand_list_obj[0]['Supplier'],Supplierlink = t_stocking_demand_list_obj[0]['Supplierlink'],
                        Stocking_quantity=unInStockNum,AccountNum=t_stocking_demand_list_obj[0]['AccountNum'],Site=t_stocking_demand_list_obj[0]['Site'],
                        Destination_warehouse=t_stocking_demand_list_obj[0]['Destination_warehouse'],level=t_stocking_demand_list_obj[0]['level'],
                        Auditor=t_stocking_demand_list_obj[0]['Auditor'],AuditTime=t_stocking_demand_list_obj[0]['AuditTime'],
                        Buyer=t_stocking_demand_list_obj[0]['Buyer'],Remarks=u'由订单号%s拆分'%(obj.Stocking_plan_number),
                        Status=t_stocking_demand_list_obj[0]['Status'],UpdateTime=ddtime.now(),
                        neworold=t_stocking_demand_list_obj[0]['neworold'],OplogTime=t_stocking_demand_list_obj[0]['OplogTime'],
                        submitAuditMan=t_stocking_demand_list_obj[0]['submitAuditMan'],submitAuditDate=t_stocking_demand_list_obj[0]['submitAuditDate'],
                        genPurchasePlanMan=t_stocking_demand_list_obj[0]['genPurchasePlanMan'],genPurchasePlanDate=t_stocking_demand_list_obj[0]['genPurchasePlanDate']
                    ))
                    obj.Status = 'already'
                    obj.Arrival_status = 'already'
                    obj.Storage_status = 'already'
                    obj.Arrival_date1 = ddtime.now()
                    obj.StorageDate = ddtime.now()
                    obj.completeInstoreMan = request.user.first_name
                    obj.completeInstoreDate = ddtime.now()
                    obj.splitMan = request.user.first_name
                    obj.splitTime = ddtime.now()
                    obj.splitRemark = u'拆分订单号;此订单被拆分为:%s_1,采购完成部分自动流转下一步'%(obj.Stocking_plan_number)
                    obj.save()

                    t_stocking_demand_list.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).update(Status='already', completePurchaseDate=ddtime.now(),completePurchaseMan=request.user.first_name)
                    successInto.append(obj.Stocking_plan_number+"_1")
                else:
                    errorInfo.append(obj.Stocking_plan_number)
            t_stocking_purchase_order.objects.bulk_create(insertPurchaseOrderinto)
            t_set_warehouse_storage_situation_list.objects.bulk_create(insertStorageInto)
            t_stocking_demand_list.objects.bulk_create(insertDemandListInto)
            if errorInfo:
                messages.info(request,u"以下不能被拆分备货计划号：%s,可能由于已经生成采购订单、采购未到货或已经全部到货"%(errorInfo))
            if successInto:
                messages.info(request, u"拆分后备货计划号：%s,已采购到货并入库数量被拆分后流转下一步;未采购数量被拆分后留在当前步骤，请待采购到货后手动输入采购订单号和完成入库提交。" % (successInto))
        except Exception, ex:
            messages.error(self.request, u"拆分订单报错,请联系开发人员解决:%s" % (str(ex)))
    splitPurchase.short_description = u'拆分订单'
    
    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_purchase_order_Admin, self).get_list_queryset()
        Status = request.GET.get('Status', '')  # 采购状态
        Buyer = request.GET.get('Buyer', '')  # 采购人
        Ali_number=request.GET.get('Ali_number','') # 1688
        Warehouse=request.GET.get('Warehouse','') # 目的地仓库
        Contract_No = request.GET.get('Contract_No', '')  # 合同号
        pay_method = request.GET.get('pay_method', '')  # 付款方式
        PrepaymentsStart = request.GET.get('PrepaymentsStart', '')  # 预付款1
        PrepaymentsEnd= request.GET.get('PrepaymentsEnd', '')  # 预付款2
        ThePeople = request.GET.get('ThePeople', '')  # 制单人
        Logistics_costsStart = request.GET.get('Logistics_costsStart', '')  # 物流费
        Logistics_costsEnd = request.GET.get('Logistics_costsEnd', '')  # 物流费
        PriceStart = request.GET.get('PriceStart', '')  # 含税单价
        PriceEnd = request.GET.get('PriceEnd', '')  # 含税单价
        Stocking_plan_number = request.GET.get('Stocking_plan_number', '')  # 备货计划号
        Single_number = request.GET.get('Single_number', '')  # 采购订单号
        Demand_people = request.GET.get('Demand_people', '')  # 计划需求人
        Product_nature = request.GET.get('Product_nature', '')  # 产品性质
        ProductSKU = request.GET.get('ProductSKU', '')  # 商品sku
        ProductName = request.GET.get('ProductName', '')  # 商品名称
        WeightStart = request.GET.get('WeightStart', '')  # 商品克重
        WeightEnd = request.GET.get('WeightEnd', '')  # 商品克重
        Supplier = request.GET.get('Supplier', '')  # 供应商
        AccountNum = request.GET.get('AccountNum', '')  # 帐号
        Site = request.GET.get('Site', '')  # 站点
        ExcelStatus = request.GET.get('ExcelStatus', '')  # 导出状态
        Destination_warehouse = request.GET.get('Destination_warehouse', '')  # 目的地仓库
        level = request.GET.get('level', '')  # 紧急程度
        UpdateTimeStart = request.GET.get('UpdateTimeStart', '')  # 更新时间
        UpdateTimeEnd = request.GET.get('UpdateTimeEnd', '')  # 更新时间
        QTYStart = request.GET.get('QTYStart', '')  # 采购数量
        QTYEnd= request.GET.get('QTYEnd', '')  # 采购数量
        Stocking_quantityStart= request.GET.get('Stocking_quantityStart', '')  # 计划采购数量
        Stocking_quantityEnd= request.GET.get('Stocking_quantityEnd', '')  # 计划采购数量
        TheTimeStart= request.GET.get('TheTimeStart', '')  # 制单时间
        TheTimeEnd= request.GET.get('TheTimeEnd', '')  # 制单时间
        Arrival_dateStart= request.GET.get('Arrival_dateStart', '')  # 预计到货日期
        Arrival_dateEnd= request.GET.get('Arrival_dateEnd', '')  # 预计到货日期
        LogisticsNumber= request.GET.get('LogisticsNumber', '')  # 物流单号
        OplogTimeStart = request.GET.get('OplogTimeStart','')  #记录生成时间
        OplogTimeEnd =request.GET.get('OplogTimeEnd','') #记录生成时间




        searchList = {
            'Status__exact':Status,
            'Buyer__exact':Buyer,
            'Ali_number__exact': Ali_number  ,
            'Warehouse__exact': Warehouse ,
            'Demand_people__exact':Demand_people,
            'level__exact':level,
            'Destination_warehouse__exact': Destination_warehouse,
            'ExcelStatus__exact': ExcelStatus,
            'Site__exact':Site,
            'AccountNum__exact':AccountNum,
            'Product_nature__exact':Product_nature,
            'ProductName__exact':ProductName,
            'Supplier__exact':Supplier,
            'ProductSKU__icontains':ProductSKU ,
            'LogisticsNumber__exact':LogisticsNumber ,
            'Contract_No__exact':Contract_No,
            'Stocking_plan_number__exact':Stocking_plan_number,
            'Single_number__exact':Single_number,
            'pay_method__exact':pay_method,
            'ThePeople__exact':ThePeople,
            'Prepayments__gte':PrepaymentsStart,'Prepayments__lt':PrepaymentsEnd,
            'Logistics_costs__gte':Logistics_costsStart,'Logistics_costs__lt':Logistics_costsEnd,
            'Price__gte':PriceStart,'Price__lt':PriceEnd,
            'Weight__gte':WeightStart,'Weight__lt':WeightEnd,
            'UpdateTime__gte':UpdateTimeStart,'UpdateTime__lt':UpdateTimeEnd,
            'QTY__gte':QTYStart,'QTY__lt':QTYEnd,
            'Stocking_quantity__gte':Stocking_quantityStart,'Stocking_quantity__lt':Stocking_quantityEnd,
            'TheTime__gte':TheTimeStart,'TheTime__lt':TheTimeEnd,
            'Arrival_date__gte':Arrival_dateStart,'Arrival_date__lt':Arrival_dateEnd,
            'OplogTime__gte':OplogTimeStart,'OplogTime__lt':OplogTimeEnd,
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
    
        return qs.order_by('-Status','Stock_plan_date')





















