# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_shipping_management_Admin.py
 @time: 2017-12-19 16:35

"""
from xadmin.layout import Fieldset, Row
from skuapp.table.t_set_warehouse_storage_situation_list import t_set_warehouse_storage_situation_list
from brick.public.django_wrap import django_wrap
from datetime import datetime as dattime
from django.utils.safestring import mark_safe
from django.contrib import messages
from skuapp.table.public import getChoices,ChoiceWarehouse,ChoiceLevel
from skuapp.table.t_stocking_demand_list import t_stocking_demand_list
import xlwt
import os,oss2
from Project.settings import MEDIA_ROOT,BUCKETNAME_XLS
from brick.public.create_dir import mkdir_p
from brick.public.generate_excel import generate_excel
from skuapp.table.public import getChoices,Choicebatchstatus
import datetime

class t_shipping_management_Admin(object):
    downloadxls = True
    search_box_flag = True
    purchase_order = False
    jump_temp = False
    site_left_menu_stocking_purchase = True
    def show_Invoice_BoxPaste(self,obj):
        if obj.Invoice is not None and obj.Invoice.strip() != '':
            rt = u'发票:<a href = "%s">下载</a><br>'%obj.Invoice
        else:
            rt = u'发票: <br>'
        if obj.BoxPaste is not None and obj.BoxPaste.strip() != '':
            rt = u'%s箱标:<a href = "%s">下载</a><br>'%(rt,obj.BoxPaste)
        else:
            rt = u'%s箱标: <br>'%rt
        rt = u"%s<a id='import_%s'>添加</a><script>$('#import_%s').on('click',function()" \
             u"{layer.open({type:2,skin:'layui-layer-lan',title:'上传发票和箱标',fix:false," \
             u"shadeClose: true,maxmin:true,area:['500px','500px'],content:" \
             u"'/importfile_Invoice_BoxPaste/?myid=%s&batchnum=%s',});});</script>"%(rt,obj.id,obj.id,obj.id,obj.Delivery_lot_number)
        return mark_safe(rt)
    show_Invoice_BoxPaste.short_description = u'发票/箱标'

    def show_status(self, obj):
        try:
            rt = ""
            strStatus = ""
            for status in getChoices(Choicebatchstatus):
                if status[0] == obj.Status:
                    strStatus = status[1]
                    break
            if  obj.Status == 'notyet':
                flag = 1 if ((obj.OplogTime is not None) and (str(dattime.now()) > str(obj.OplogTime + datetime.timedelta(days=2)))) else 0
                diffDate = (dattime.now() - obj.OplogTime).days if obj.OplogTime is not None else 0
                if flag == 1:
                    rt = '<div class="box" style="width: 150px;height: 120px;background-color: red;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天<br>上一步处理时间:%s' % (strStatus,diffDate,obj.OplogTime)
                else:
                    rt = '<div class="box" style="width: 150px;height: 120px;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天<br>上一步处理时间:%s</div>' % (strStatus,diffDate,obj.OplogTime)
            else:
                rt = strStatus
        except Exception, ex:
            messages.info(self.request,"采购状态加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_status.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">本批次发货状态</p>')

    def show_Stocking_plan_number(self,obj):
        rt = django_wrap(obj.Stocking_plan_number, '|', 3)
        return mark_safe(rt)
    show_Stocking_plan_number.short_description = u'计划备货号'

    def show_Cargo_inforLink(self,obj):
        rt = ''
        if obj.Cargo_infor is not None and obj.Cargo_infor.strip() != '':
            rt = '<a href = "%s">%s</a>'%(obj.Cargo_infor,u'货物信息下载')
        return mark_safe(rt)
    show_Cargo_inforLink.short_description = u'货物信息'

    def show_All_ProductSKU_Num(self,obj):
        rt = django_wrap(obj.All_ProductSKU_Num,';',3)
        return mark_safe(rt)
    show_All_ProductSKU_Num.short_description = u'商品SKU*数量集合'

    list_display = ('Delivery_lot_number','show_status','Warehouse_number','show_All_ProductSKU_Num','LogisticsMode','GoodsCategory','Destination_warehouse','Delivery_date','Sender',
                    'The_first_Logistics_providers','The_first_Logistics_cost','LogisticsNumber','show_Cargo_inforLink','show_Stocking_plan_number',
                    'Num','BoxNum','BoxWeight','BoxSize','show_Invoice_BoxPaste')
    list_editable = ('The_first_Logistics_providers','The_first_Logistics_cost','LogisticsMode','GoodsCategory','Warehouse_number','LogisticsNumber','All_ProductSKU_Num','Sender','Num','BoxNum','BoxWeight','BoxSize',)
    fields = ('Sender', 'The_first_Logistics_providers','The_first_Logistics_cost','LogisticsNumber','Cargo_infor','All_ProductSKU_Num',
                'Num','BoxNum','BoxWeight','BoxSize'
                )

    form_layout = (
        Fieldset(u'请认真填写',
                 Row('The_first_Logistics_providers', 'The_first_Logistics_cost','', ),
                 Row('Cargo_infor', '', '', ),
                 Row('Num','BoxNum','BoxWeight',),
                 Row('BoxSize',),
                 Row('Sender', '', '', ),
                 Row('All_ProductSKU_Num', '', '', ),
                 css_class='unsort '
                 ),)

    actions = ['generate_number', 'complete_delivery','get_excel_to_py','is_reject']

    def generate_number(self, request, objs):
        from app_djcelery.tasks import generate_delivery_invoices
        idlist = []
        for obj in objs:
            idlist.append(obj.id)
            obj.getDetailedList = request.user.first_name
            obj.getDetailedTime = dattime.now()
            obj.save()
        # generate_delivery_invoices.delay(idlist)
        generate_delivery_invoices.delay(idlist,request.user.username)
        messages.success(request,u'发票正在生成中。。。请稍等刷新页面下载。。')
    generate_number.short_description = u'获取发货清单和箱标'

    def complete_delivery(self, request, objs):
        for obj in objs:
            if obj.Status == 'notyet':
                t_set_warehouse_storage_situation_list.objects.filter(Delivery_lot_number = obj.Delivery_lot_number).update(Delivery_status = 'completed')
                obj.Sender = request.user.first_name
                obj.Delivery_date = dattime.now()
                obj.Status = 'already'
                obj.OplogTime=dattime.now()
                obj.save()

    complete_delivery.short_description = u'确认发货'

    def get_excel_to_py(self, request, objs):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        # if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        # 写数据
        thelist = []
        for qs in objs:
            batsta = None
            for batbb in getChoices(Choicebatchstatus):
                if batbb[0] == qs.Status:
                    batsta = batbb[1]
                    break

            t_set_warehouse_storage_situation_list_objs = t_set_warehouse_storage_situation_list.objects.filter(Delivery_lot_number = qs.Delivery_lot_number)
            for obj in t_set_warehouse_storage_situation_list_objs:
                remarks = None
                t_stocking_demand_list_objs = t_stocking_demand_list.objects.filter(Stocking_plan_number = obj.Stocking_plan_number)
                if t_stocking_demand_list_objs.exists():
                    remarks = t_stocking_demand_list_objs[0].Remarks
                warehouse = ''
                for ware in getChoices(ChoiceWarehouse):
                    if obj.Destination_warehouse == ware[0]:
                        warehouse = ware[1]

                level = ''
                for lev in getChoices(ChoiceLevel):
                    if obj.level == lev[0]:
                        level = lev[1]

                house = u'浦江集货仓'
                if ('%s'%obj.Purchase_Order_No).find(u'调拨') != -1 or  ('%s'%obj.Purchase_Order_No).find(u'调货') != -1:
                    house = u'浦江仓库'

                thelist.append([obj.ProductSKU,obj.ShopSKU,obj.The_arrival_of_the_number,qs.Warehouse_number,qs.GoodsCategory,qs.The_first_Logistics_cost,
                                qs.LogisticsNumber,qs.Sender,batsta,obj.Price,house,warehouse,obj.ProductName,level,obj.Demand_people,remarks,obj.AccountNum])
        thelist.insert(0,[u'SKU',u'店铺SKU',u'Qty',u'入库单号',u'货物品类',u'头程费用',u'	物流单号',u'发货人',u'本批次发货状态',
                          u'含税单价',u'出库仓',u'入库仓',u'产品名称',u'紧急程度',u'计划需求人',u'备注',u'店铺名(账号)'])
        filename = request.user.username + '_' + dattime.now().strftime('%Y%m%d%H%M%S') + '.xls'

        getexcel = generate_excel(thelist,path + '/' + filename)
        if getexcel['code'] == 0:
            from brick.public.upload_to_oss import upload_to_oss
            os.popen(r'chmod 777 %s' % (path + '/' + filename))
            upload_to_oss_obj = upload_to_oss(BUCKETNAME_XLS)
            myresult = upload_to_oss_obj.upload_to_oss({'path':request.user.username,'name':filename,'byte':open(path + '/' + filename),'del':0})
            if myresult['errorcode'] == 0:
                messages.error(request, myresult['result'] + u':成功导出,可点击Download下载到本地............................。')
        else:
            messages.error(request, u'导出失败。。。。。')

    get_excel_to_py.short_description = u'导出Excel表格'

    def is_reject(self,request,objs):
        if request.user.is_superuser:
            from skuapp.table.t_set_warehouse_storage_situation_list import t_set_warehouse_storage_situation_list
            for obj in objs:
                if obj.Status == 'notyet':
                    t_set_warehouse_storage_situation_list.objects.filter(Delivery_lot_number=obj.Delivery_lot_number).update(Delivery_lot_number=None,Delivery_status='notyet')

                    obj.delete()
                    messages.success(request,u'驳回成功的备货计划号为:%s'%obj.Stocking_plan_number)
                else:
                    messages.error(request,u'已经发货的批次不允许驳回')
        else:
            messages.error(request, u'必须为超级用户才可以操作')

    is_reject.short_description = u'批次驳回(超级用户)'

    def save_models(self,):
        obj = self.new_obj
        request = self.request

        old_obj = None
        if obj is None or obj.id is None or obj.id <= 0:
            pass
        else:
            old_obj = self.model.objects.get(pk=obj.pk)
        obj.save()

        if obj.Sender is None or obj.Sender.strip() == '':
            obj.Sender = request.user.first_name

        obj.save()
    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_shipping_management_Admin, self).get_list_queryset()
        CgStatus = request.GET.get('Status', '')
        Stocking_plan_number=request.GET.get('Stocking_plan_number','')
        LogisticsMode=request.GET.get('LogisticsMode','')
        BoxPaste=request.GET.get('BoxPaste','')
        The_first_Logistics_providers=request.GET.get('The_first_Logistics_providers','')
        The_first_Logistics_costStart=request.GET.get('The_first_Logistics_costStart','')
        The_first_Logistics_costEnd=request.GET.get('The_first_Logistics_costEnd','')
        LogisticsNumber=request.GET.get('LogisticsNumber','')
        Warehouse_number=request.GET.get('Warehouse_number','')
        Sender=request.GET.get('Sender','')

       # Invoice=request.GET.get('Invoice','')
        Delivery_lot_number=request.GET.get('Delivery_lot_number','')
        Delivery_dateStart=request.GET.get('Delivery_dateStart','')
        Delivery_dateEnd=request.GET.get('Delivery_dateEnd','')
        Destination_warehouse=request.GET.get('Destination_warehouse','')
        All_ProductSKU_Num=request.GET.get('All_ProductSKU_Num','')

        NumStart=request.GET.get('NumStart','')
        NumEnd=request.GET.get('NumEnd','')
        BoxNumStart=request.GET.get('BoxNumStart','')
        BoxNumEnd=request.GET.get('BoxNumEnd','')
        BoxWeightStart=request.GET.get('BoxWeightStart','')
        BoxWeightEnd=request.GET.get('BoxWeightEnd','')
        BoxSizeStart=request.GET.get('BoxSizeStart','')
        BoxSizeEnd=request.GET.get('BoxSizeEnd','')
        UpdateTimeStart=request.GET.get('UpdateTimeStart','')
        UpdateTimeEnd=request.GET.get('UpdateTimeEnd','')
        GoodsCategory=request.GET.get('GoodsCategory','')
        OplogTimeStart = request.GET.get('OplogTimeStart','')  #记录生成时间
        OplogTimeEnd =request.GET.get('OplogTimeEnd','') #记录生成时间



        searchList = {
                      'Status__exact': CgStatus,
                      'Stocking_plan_number__icontains':Stocking_plan_number,
                      'LogisticsMode__exact':LogisticsMode,
                      'LogisticsNumber__exact':LogisticsNumber,
                      'GoodsCategory__exact':GoodsCategory,
                      'The_first_Logistics_providers__exact':The_first_Logistics_providers,
                      'BoxPaste__exact':BoxPaste,
                      'The_first_Logistics_cost__gte':The_first_Logistics_costStart,'The_first_Logistics_cost__lt':The_first_Logistics_costEnd,
                      'Destination_warehouse__exact':Destination_warehouse,
                      'LogisticsNumber__exact':LogisticsNumber,
                      'Warehouse_number__contains':Warehouse_number,
                      'Delivery_lot_number__contains':Delivery_lot_number,
                      'Sender__exact':Sender,

                    #  'Invoice__exact':Invoice,
                      'Delivery_date__gte':Delivery_dateStart, 'Delivery_date__lt':Delivery_dateEnd,
                      'All_ProductSKU_Num__icontains':All_ProductSKU_Num,
                      'Num__gte':NumStart, 'Num__lt':NumEnd,
                      'BoxNum__gte':BoxNumStart, 'BoxNum__lt':BoxNumEnd,
                      'BoxWeight__gte':BoxWeightStart, 'BoxWeight__lt':BoxWeightEnd,
                      'BoxSize__gte':BoxSizeStart, 'BoxSize__lt':BoxSizeEnd,
                      'UpdateTime__gte':UpdateTimeStart, 'UpdateTime__lt':UpdateTimeEnd,
                      'UpdateTime__gte':UpdateTimeStart,'UpdateTime__lt':UpdateTimeEnd,

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
    
        return qs.order_by('-Status','OplogTime')