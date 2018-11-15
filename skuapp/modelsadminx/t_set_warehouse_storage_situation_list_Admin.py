# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_set_warehouse_storage_situation_list_Admin.py
 @time: 2017-12-19 16:24

"""   
from xadmin.layout import Fieldset, Row
import datetime
from skuapp.table.t_shipping_management import t_shipping_management
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.db.models import Count
from datetime import datetime as ddtime
from skuapp.table.public import *

class t_set_warehouse_storage_situation_list_Admin(object):
    purchase_order = False
    jump_temp = False
    search_box_flag = True
    site_left_menu_stocking_purchase = True
    def show_ProductImage(self,obj) :
        rt =  '<img src="%s"  width=120 height=120/>  '%(obj.ProductImage)
        return mark_safe(rt)
    show_ProductImage.short_description = u'商品图片'

    def show_LogisticsNumber(self,obj) :
        rt = ''
        if obj.LogisticsNumber is not None and obj.LogisticsNumber.strip() != '':
            rt = rt + '<a target="_blank" href="https://www.baidu.com/s?wd=%s">%s</a>'%(obj.LogisticsNumber,obj.LogisticsNumber)
        return mark_safe(rt)
    show_LogisticsNumber.short_description = u'物流单号'

    def show_Delivery_status(self, obj):
        try:
            rt = ""
            strStatus = ""
            for status in getChoices(ChoiceDeliveryStatus):
                if status[0] == obj.Delivery_status:
                    strStatus = status[1]
                    break
            if  obj.Delivery_status == 'notyet':
                diffDate = (ddtime.now() - obj.StorageDate).days if obj.StorageDate is not None else 0
                flag = 1 if ((obj.StorageDate is not None) and (str(ddtime.now()) > str(obj.StorageDate + datetime.timedelta(days=2)))) else 0
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
    show_Delivery_status.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">批次状态</p>')

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
                strTmp =  '<a target="_blank" href="https://www.baidu.com/s?wd=%s">%s</a>' % (obj.LogisticsNumber, obj.LogisticsNumber)
            rt = u'<strong>商品SKU:</strong>%s<br><strong>店铺SKU:</strong>%s<br><strong>产品性质:</strong>%s<br><strong>商品名称:</strong>%s<br><strong>' \
                 u'计划需求人:</strong>%s<br><strong>物流信息:</strong>%s<br><strong>仓库:</strong>%s<br><strong>备注:</strong>%s' % (
                obj.ProductSKU, obj.ShopSKU, Product_nature_value, obj.ProductName,obj.Demand_people ,strTmp,Warehouse_value,obj.Remarks)
            return mark_safe(rt)
        except Exception, ex:
            messages.info(self.request, "商品信息加载错误,请联系IT解决:%s" % (str(ex)))
            rt = ""
    show_goodsInfo.short_description = u'商品信息'

    def show_opInfo(self, obj):
        try:
            from skuapp.table.t_stocking_demand_list import t_stocking_demand_list
            from skuapp.table.t_stocking_purchase_order import t_stocking_purchase_order
            rt = u'<table border="1" ><tr><th>操作员</th><th>告警信息</th><th>操作时间</th><tr>'
            t_stocking_demand_list_obj = t_stocking_demand_list.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).values('Demand_people','Stock_plan_date', 'Auditor',
                                        'AuditTime','submitAuditMan','submitAuditDate','genPurchasePlanMan','genPurchasePlanDate')
            t_stocking_purchase_order_obj = t_stocking_purchase_order.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).values('completeInstoreMan','completeInstoreDate',
                                        'splitMan','splitTime')

            if len(t_stocking_demand_list_obj) > 0:
                diffDate1 = (t_stocking_demand_list_obj[0]['AuditTime'] - t_stocking_demand_list_obj[0]['Stock_plan_date']).days if (t_stocking_demand_list_obj[0]['AuditTime'] is not None and t_stocking_demand_list_obj[0]['Stock_plan_date'] is not None) else 0
                diffDate2 = (t_stocking_demand_list_obj[0]['genPurchasePlanDate'] - t_stocking_demand_list_obj[0]['AuditTime']).days if (t_stocking_demand_list_obj[0]['AuditTime'] is not None and t_stocking_demand_list_obj[0]['genPurchasePlanDate'] is not None) else 0
                diffDate3 = 0
                diffDate4 = 0
                strCompleteMan = ""
                if len(t_stocking_purchase_order_obj) > 0:
                    strCompleteMan = t_stocking_purchase_order_obj[0]['completeInstoreMan'] if t_stocking_purchase_order_obj[0]['completeInstoreMan'] is not None else u"系统定时刷新"
                    diffDate3 = (t_stocking_purchase_order_obj[0]['completeInstoreDate'] - t_stocking_demand_list_obj[0]['genPurchasePlanDate']).days if (t_stocking_demand_list_obj[0]['genPurchasePlanDate'] is not None and t_stocking_purchase_order_obj[0]['completeInstoreDate'] is not None) else 0
                    if obj.genBatchTime:
                        diffDate4 = (obj.genBatchTime - t_stocking_purchase_order_obj[0]['completeInstoreDate']).days if (t_stocking_purchase_order_obj[0]['completeInstoreDate'] is not None) else 0
                    else:
                        diffDate4 = (datetime.datetime.now() - t_stocking_purchase_order_obj[0]['completeInstoreDate']).days if (t_stocking_purchase_order_obj[0]['completeInstoreDate'] is not None) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_demand_list_obj[0]['Demand_people'],diffDate1, t_stocking_demand_list_obj[0]['Stock_plan_date'])
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_demand_list_obj[0]['Demand_people'],diffDate1, t_stocking_demand_list_obj[0]['Stock_plan_date'])
                if diffDate2 > 2:
                    rt = rt + u'<tr style="color:red"><th>审核:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_demand_list_obj[0]['Auditor'], diffDate2, t_stocking_demand_list_obj[0]['AuditTime'])
                else:
                    rt = rt + u'<tr style=""><th>审核:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_demand_list_obj[0]['Auditor'], diffDate2, t_stocking_demand_list_obj[0]['AuditTime'])
                if diffDate3 > 2:
                    rt = rt + u'<tr style="color:red"><th>生成采购:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_demand_list_obj[0]['genPurchasePlanMan'], diffDate3,t_stocking_demand_list_obj[0]['genPurchasePlanDate'])
                else:
                    rt = rt + u'<tr style=""><th>生成采购:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_demand_list_obj[0]['genPurchasePlanMan'], diffDate3,t_stocking_demand_list_obj[0]['genPurchasePlanDate'])

                if len(t_stocking_purchase_order_obj) > 0:
                    if diffDate4 > 2:
                        rt = rt + u'<tr style="color:red"><th>完成采购:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_purchase_order_obj[0]['completeInstoreMan'], diffDate4,t_stocking_purchase_order_obj[0]['completeInstoreDate'])
                    else:
                        rt = rt + u'<tr style=""><th>完成采购:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (t_stocking_purchase_order_obj[0]['completeInstoreMan'], diffDate4,t_stocking_purchase_order_obj[0]['completeInstoreDate'])
                else:
                    if diffDate4 > 2:
                        rt = rt + u'<tr style="color:red"><th>完成采购:</th><th>延迟%s天</th><th></th></tr>' % (diffDate4)
                    else:
                        rt = rt + u'<tr style=""><th>完成采购:</th><th>延迟%s天</th><th></th></tr>' % (diffDate4)

            if obj.genBatchTime:
                rt = rt + u'<tr style=""><th>生成批次:%s</th><th></th><th>%s</th></tr>' % (obj.genBatchMan, obj.genBatchTime)

            rt = rt + "</table>"
        except Exception, ex:
            messages.info(self.request,"采购状态加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_opInfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">操作记录信息</p>')

    list_display = ('Stocking_plan_number', 'show_Delivery_status', 'Purchase_Order_No','show_goodsInfo', 'show_ProductImage',
                    'Stocking_quantity', 'The_arrival_of_the_number', 'Stock_plan_unfinished_quantity', 'Arrival_status',
                    'Storage_status', 'Delivery_status','checkStatus', 'AccountNum','level','show_opInfo')
    list_editable = ('The_arrival_of_the_number','Arrival_date', 'Remarks')

    fields = ('The_arrival_of_the_number', 'Arrival_date', 'Remarks')

    form_layout = (
        Fieldset(u'请认真填写',
                 Row('The_arrival_of_the_number', '', '', ),
                 Row('Arrival_date', '', '', ),
                 Row('Remarks', '', '', ),
                 css_class='unsort '
                 ),)

    actions = ['already_Arrival','has_been_storage','already_Ship','already_Ship2']
    def has_been_storage(self, request, objs):
        for obj in objs:
            if obj.Storage_status == 'notyet':
                obj.StorageDate = datetime.datetime.now()
                obj.Storage_status = 'already'
                obj.save()

    has_been_storage.short_description = u'2、确认入库'

    def already_Ship(self, request, objs):
        from django.db import connection
        
        The_lot_number = 'SHIP' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-' + str(objs[0].id)
        myplan = []
        myproductinfo = []
        warehouselist = []
        Cargo_infor = []
        for obj in objs:
            if obj.Arrival_status == 'already' and obj.Storage_status == 'already' and obj.Delivery_status == 'notyet':
                myplan.append(obj.Stocking_plan_number)
                myproductinfo.append(obj.ProductSKU + '*' + str(obj.The_arrival_of_the_number))
                warehouselist.append(obj.Destination_warehouse)
                productinfo = [obj.ProductSKU,obj.Stocking_quantity,obj.The_arrival_of_the_number,'',obj.ProductName,'']
                Cargo_infor.append(productinfo)

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

                if uploadresult['result'] != '':
                    objs.update(Delivery_lot_number=The_lot_number, Delivery_status='already',genBatchMan=request.user.first_name,genBatchTime=ddtime.now())

                    t_shipping_management.objects.create(Stocking_plan_number='|'.join(myplan), Cargo_infor=uploadresult['result'],
                                                         Delivery_lot_number = The_lot_number,Destination_warehouse = warehouselist[0],OplogTime=ddtime.now(),
                                                         Status = 'notyet',All_ProductSKU_Num = ';'.join(myproductinfo))
                else:
                    messages.error(request, u'导出失败！请稍后 重试。。。')
            else:
                messages.error(request, u'导出失败！请稍后 重试。。。%s' % exresult['error'])
        

    already_Ship.short_description = u'3、生成发货批次'
    
    def already_Ship2(self, request, objs):
        from django.db import connection
        '''
        The_lot_number = 'SHIP' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-' + str(objs[0].id)
        myplan = []
        myproductinfo = []
        warehouselist = []
        Cargo_infor = []
        for obj in objs:
            if obj.Arrival_status == 'already' and obj.Storage_status == 'already' and obj.Delivery_status == 'notyet':
                myplan.append(obj.Stocking_plan_number)
                myproductinfo.append(obj.ProductSKU + '*' + str(obj.The_arrival_of_the_number))
                warehouselist.append(obj.Destination_warehouse)
                productinfo = [obj.ProductSKU,obj.Stocking_quantity,obj.The_arrival_of_the_number,'',obj.ProductName,'']
                Cargo_infor.append(productinfo)

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

                if uploadresult['result'] != '':
                    objs.update(Delivery_lot_number=The_lot_number, Delivery_status='already')

                    t_shipping_management.objects.create(Stocking_plan_number='|'.join(myplan), Cargo_infor=uploadresult['result'],
                                                         Delivery_lot_number = The_lot_number,Destination_warehouse = warehouselist[0],Oplogtime=ddtime.now()
                                                         Status = 'notyet',All_ProductSKU_Num = ';'.join(myproductinfo))
                else:
                    messages.error(request, u'导出失败！请稍后 重试。。。')
            else:
                messages.error(request, u'导出失败！请稍后 重试。。。%s' % exresult['error'])
        '''
        lis = []
        for obj in objs:
            ss = obj.Destination_warehouse
            lis.append(str(obj.AccountNum))
        cur = connection.cursor()
        sql = "SELECT AccountNum,sum(case when Arrival_status='already' then 1 else 0 end ),sum(case when Arrival_status='notyet' then 1 else 0 end),Destination_warehouse FROM t_set_warehouse_storage_situation_list WHERE AccountNum IN (%s) AND Delivery_status = 'notyet' AND Destination_warehouse='%s' GROUP BY AccountNum"%((str(lis).replace('[','').replace(']','')),ss)
        #messages.error(request,lis)
        #messages.error(request,sql)
        cur.execute(sql)
        rows = cur.fetchall()
        rows = list(rows)

        return render(request, 'storage.html',{'rows':rows})

    already_Ship2.short_description = u'4、生成发货批次(针对FBW仓库)'

    def already_Arrival(self, request, objs):
        for obj in objs:
            if obj.Arrival_status == 'notyet':
                if obj.The_arrival_of_the_number is not None :
                    obj.Stock_plan_unfinished_quantity = obj.Stocking_quantity - obj.The_arrival_of_the_number
                    obj.Arrival_date = datetime.datetime.now()
                    obj.Arrival_status = 'already'
                    obj.save()
                else:
                    messages.error(request,u'请填写该SKU的到货数量。。。')

    already_Arrival.short_description = u'1、已经到货'

    def get_list_queryset(self):
        request=self.request
        qs = super(t_set_warehouse_storage_situation_list_Admin, self).get_list_queryset()

        Status = request.GET.get('Status', '')  # 采购状态
        Purchase_Order_No= request.GET.get('Purchase_Order_No', '')  # 采购单号
        Delivery_lot_number = request.GET.get('Delivery_lot_number', '')  # 发货批次号
        Stocking_plan_number = request.GET.get('Stocking_plan_number', '')  # 备货计划号
        Arrival_status = request.GET.get('Arrival_status', '')  # 到货状态
        Storage_status = request.GET.get('Storage_status', '')  # 入库状态
        Delivery_status = request.GET.get('Delivery_status', '')  # 批次状态
        PriceStart = request.GET.get('PriceStart', '')  #成本价
        PriceEnd = request.GET.get('PriceEnd', '')  #成本价
        Demand_people = request.GET.get('Demand_people', '')  # 计划需求人
        Product_nature = request.GET.get('Product_nature', '')  # 产品性质
        ProductSKU = request.GET.get('ProductSKU', '')  # 商品sku
        ProductName = request.GET.get('ProductName', '')  # 商品名称
        WeightStart = request.GET.get('WeightStart', '')  #克重
        WeightEnd = request.GET.get('WeightEnd', '')  # 克重
        AccountNum = request.GET.get('AccountNum', '')  # 帐号
        Site = request.GET.get('Site', '')  # 站点
        Destination_warehouse= request.GET.get('Destination_warehouse', '')  # 目的地仓库
        level = request.GET.get('level', '')  # 紧急程度
        UpdateTimeStart = request.GET.get('UpdateTimeStart', '')  # 更新时间
        UpdateTimeEnd = request.GET.get('UpdateTimeEnd', '')  # 更新时间
        QTYStart = request.GET.get('QTYStart', '')  # 采购数量
        QTYEnd= request.GET.get('QTYEnd', '')  # 采购数量
        The_arrival_of_the_numberStart= request.GET.get('The_arrival_of_the_numberStart', '')  # 本次到货数量
        The_arrival_of_the_numberEnd= request.GET.get('The_arrival_of_the_numberEnd', '')  # 本次到货数量
        Stock_plan_unfinished_quantityStart= request.GET.get('Stock_plan_unfinished_quantityStart', '')  # 备货计划数量
        Stock_plan_unfinished_quantityEnd= request.GET.get('Stock_plan_unfinished_quantityEnd', '')  # 备货计划数量
        Stocking_quantityStart= request.GET.get('Stocking_quantityStart', '')  # 计划采购数量
        Stocking_quantityEnd= request.GET.get('Stocking_quantityEnd', '')  # 计划采购数量
        Arrival_dateStart= request.GET.get('Arrival_dateStart', '')  # 预计到货日期
        Arrival_dateEnd= request.GET.get('Arrival_dateEnd', '')  # 预计到货日期
        StorageDateStart= request.GET.get('StorageDateStart', '')  # 入库日期
        StorageDateEnd= request.GET.get('StorageDateEnd', '')  # 入库日期
        LogisticsNumber= request.GET.get('LogisticsNumber', '')  # 物流单号
        OplogTimeStart = request.GET.get('OplogTimeStart','')  #记录生成时间
        OplogTimeEnd =request.GET.get('OplogTimeEnd','') #记录生成时间


        searchList = {
            'Status__exact':Status,
            'Delivery_lot_number__exact':Delivery_lot_number,
            'Storage_status__exact':Storage_status,
            'Destination_warehouse__exact':Destination_warehouse,
            'Purchase_Order_No__exact':Purchase_Order_No,
            'Arrival_status__exact':Arrival_status,
            'Delivery_status__exact':Delivery_status,
            'Demand_people__exact':Demand_people,
            'level__exact':level,
            'Site__exact':Site,
            'AccountNum__exact':AccountNum,
            'Product_nature__exact':Product_nature,
            'ProductName__exact':ProductName,
            'ProductSKU__icontains':ProductSKU,
            'LogisticsNumber__exact':LogisticsNumber,
            'Stocking_plan_number__exact':Stocking_plan_number,
            'Price__gte':PriceStart,'Price__lt':PriceEnd,
            'Weight__gte':WeightStart,'Weight__lt':WeightEnd,
            'UpdateTime__gte':UpdateTimeStart,'UpdateTime__lt':UpdateTimeEnd,
            'OplogTime__gte':OplogTimeStart,'OplogTime__lt':OplogTimeEnd,
            'QTY__gte':QTYStart,'QTY__lt':QTYEnd,
            'Stocking_quantity__gte':Stocking_quantityStart,'Stocking_quantity__lt':Stocking_quantityEnd,
            'The_arrival_of_the_number__gte':The_arrival_of_the_numberStart,'The_arrival_of_the_number__lt':The_arrival_of_the_numberEnd,
            'Arrival_date__gte':Arrival_dateStart,'Arrival_date__lt':Arrival_dateEnd,
            'StorageDate__gte':StorageDateStart,'StorageDate__lt':StorageDateEnd,
            'Stock_plan_unfinished_quantity__gte':Stock_plan_unfinished_quantityStart,'Stock_plan_unfinished_quantity__lt':Stock_plan_unfinished_quantityEnd,
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

        return qs.order_by('-Delivery_status','StorageDate')