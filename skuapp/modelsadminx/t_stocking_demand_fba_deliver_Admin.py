# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fba_deliver_Admin.py
 @time: 2018-08-15 16:35

"""
from xadmin.layout import Fieldset, Row
from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
from brick.public.django_wrap import django_wrap
from datetime import datetime as dattime
from django.utils.safestring import mark_safe
from django.contrib import messages
from skuapp.table.public import getChoices,ChoiceWarehouse,ChoiceLevel
import xlwt
import os,oss2
from Project.settings import MEDIA_ROOT,BUCKETNAME_XLS
from brick.public.create_dir import mkdir_p
from brick.public.generate_excel import generate_excel
from skuapp.table.public import *
import datetime
from skuapp.table.t_stocking_demand_fba_detail import t_stocking_demand_fba_detail

class t_stocking_demand_fba_deliver_Admin(object):
    search_box_flag = True
    fba_tree_menu_flag = True
    hide_page_action = True
    downloadxls = True
    def del_None(self,col):
        rt = col
        if not col:
            rt = ''
        return rt
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

            from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
            t_stocking_demand_fba_obj = t_stocking_demand_fba.objects.filter(
                Delivery_lot_number=obj.Delivery_lot_number)
            # t_stocking_demand_fba_obj = t_stocking_demand_fba.objects.filter(Delivery_lot_number=obj.Delivery_lot_number).first()
            genBatchMan = ''
            for row in t_stocking_demand_fba_obj:
                genBatchMan = row.genBatchMan

            rt = ""
            strStatus = ""
            for status in getChoices(ChoiceFBAPlanStatus):
                if status[0] == obj.Status:
                    strStatus = status[1]
                    break
            if  obj.Status == 'deliver':
                flag = 1 if ((obj.OplogTime is not None) and (str(dattime.now()) > str(obj.OplogTime + datetime.timedelta(days=2)))) else 0
                diffDate = (dattime.now() - obj.OplogTime).days if obj.OplogTime is not None else 0
                if flag == 1:
                    rt = '<div class="box" style="width: 150px;height: 120px;background-color: red;text-align: center;line-height: 20px;border-radius: 4px">%s<br>超期%s天<br>上一步处理人:%s<br>上一步处理时间:%s</div>' % (strStatus,diffDate,genBatchMan,obj.OplogTime)

                else:

                    rt = '<div class="box" style="width: 150px;height: 120px;text-align: center;line-height: 20px;border-radius: 4px">%s<br>超期%s天<br>上一步处理人:%s<br>上一步处理时间:%s</div>' % (strStatus,diffDate,genBatchMan,obj.OplogTime)
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
    show_Cargo_inforLink.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">货物信息</p>')

    def show_All_ProductSKU_Num(self,obj):
        try:
            rt = ""
            rt = u"<strong>商品SKU*数量:</strong><br>"
            rt = rt + django_wrap(obj.All_ProductSKU_Num,';',2)
            rt = rt + u"<br><strong>计划备货号:</strong><br>"
            rt = rt + django_wrap(obj.Stocking_plan_number, '|', 2)
        except Exception, ex:
            messages.info(self.request,"商品SKU*数量加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_All_ProductSKU_Num.short_description =  mark_safe('<p align="center" style="width:100px;color:#428bca;">商品SKU*数量/计划备货号集合</p>')

    def edit_sku(self,obj):
        try:
            rt = ""
            if obj.Status == "deliver":
                if obj.editSKU is not None:
                    listSKU = obj.editSKU.split(';')
                    rt = '%s<strong>商品SKU实际发货数量编辑:</strong><br><table>' % (rt)
                    idList = []
                    for sku in listSKU:
                        tmpList = sku.split('*')
                        idList.append(tmpList[0])
                        rt = '%s<tr><th><strong>%s</strong>:</th><th><input type="text" style="width:60px;height:25px" id="%s" value="%s"></th></tr>' % (
                            rt, tmpList[0], tmpList[0], tmpList[1])
                    rt = '%s<tr><th></th><th align="left"><input type="button" style="width:60px;height:25px;" id="btn1_%s" value="确定"></th></tr>' % (
                        rt, obj.id)
                    rt = '%s</table>' % (rt)
                    rt = '%s<br><p id="result1_%s"  style="color:green;"></p>' % (rt, obj.id)
                    rt = '%s<input id="idlist_%s"  style="display:none;" value="%s">' % (rt, obj.id, ','.join(idList))
                    tt = """%s<script>                        
                                $(document).ready(function(){
                                    $("#btn1_%s").click(function(){
                                        var strID = document.getElementById("idlist_%s").value;
                                        idList = strID.split(",");
                                        var allProductNum = "";
                                        var strTmp = "";
                                        for ( var i = 0; i <idList.length; i++){
                                            strTmp = document.getElementById(idList[i]).value;
                                            if(isNaN(strTmp)){
                                                var strTip = idList[i] + ":输入非数字，请修改后重新提交";
                                                alert(strTip);
                                                return;
                                            }
                                            allProductNum = allProductNum + idList[i] + "*" + strTmp + ";";
                                        }
                                        allProductNum=(allProductNum.substring(allProductNum.length-1)==';')?allProductNum.substring(0,allProductNum.length-1):allProductNum;                                
                                        $.ajax({url:"/fba_deliver_skunum_dealdata/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",
                                        data:{"id":"%s","edit_skus":allProductNum},
                                        success:function(data){if(data.result=="OK"){document.getElementById("result1_%s").innerHTML="修改成功!";}
                                                               else if(data.result=="NG"){document.getElementById("result1_%s").innerHTML="修改失败,请检查!";}},
                                        error:function(data){document.getElementById("result1_%s").innerHTML="修改报错,请检查!";}
                                    })})
                                })</script>"""
                    rt = tt % (rt, obj.id, obj.id, obj.id, obj.id, obj.id, obj.id)
            else:
                rt = u"%s<strong>实际商品SKU*数量:</strong><br>" % (rt)
                rt = rt + django_wrap(obj.editSKU, ';', 2)
        except Exception, ex:
            messages.info(self.request, "可编辑的SKU加载错误,请联系IT解决:%s" % (str(ex)))
            rt = ""
        return mark_safe(rt)
    edit_sku.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">商品SKU实际发货量</p>')

    def show_Supplierlink(self,obj) :
        from brick.public.django_wrap import django_wrap
        rt = ''
        if obj.LogisticsNumber is not None and obj.LogisticsNumber.strip() != '':
            listNumber = obj.LogisticsNumber.split(',')
            i = 1
            for row in listNumber:
                rt = rt + '<a target="_blank" href="http://139.224.60.129:8321/track_query.aspx?track_number=%s">查看物流%s</a><br>'%(row,str(i))
                i+=1

        return mark_safe(rt)
    show_Supplierlink.short_description = u'物流信息'

    def show_infors_number(self,obj) :
        rt = ''
        try:
            read = ''
            if obj.Status != 'deliver':
                read = 'readonly'
            rt = '<font style="color:red">物流单号多个用英文(,)逗号分开</font><br>'
            rt = rt + '<table>'
            rt = u'%s<tr><th>物流单号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_deliver\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                 (rt, self.del_None(obj.LogisticsNumber), obj.id, 'LogisticsNumber', read,
                  self.del_None(obj.LogisticsNumber), str(obj.id) + '_LogisticsNumber')
            rt = u'%s<tr><th>入库单号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_deliver\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
                 u'<tr><th>发货人：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_deliver\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
                 u'<tr><th>物流方式：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_deliver\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                 (rt,self.del_None(obj.Warehouse_number),obj.id,'Warehouse_number',read,self.del_None(obj.Warehouse_number),str(obj.id)+'_Warehouse_number',
                  self.del_None(obj.Sender),obj.id,'Sender',read,self.del_None(obj.Sender),str(obj.id)+'_Sender',
                  self.del_None(obj.LogisticsMode), obj.id, 'LogisticsMode', read, self.del_None(obj.LogisticsMode), str(obj.id) + '_LogisticsMode',)

            rt = u'%s<tr><th>货物品类：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_deliver\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                 (rt,self.del_None(obj.GoodsCategory),obj.id,'GoodsCategory',read,self.del_None(obj.GoodsCategory),str(obj.id)+'_GoodsCategory')

            rt = u'%s<tr><th>头程物流商：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_deliver\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                 (rt, self.del_None(obj.The_first_Logistics_providers), obj.id, 'The_first_Logistics_providers', read,
                  self.del_None(obj.The_first_Logistics_providers), str(obj.id) + '_The_first_Logistics_providers')
            rt = u'%s<tr><th>头程费用：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_deliver\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                 (rt, self.del_None(obj.The_first_Logistics_cost), obj.id, 'The_first_Logistics_cost', read,
                  self.del_None(obj.The_first_Logistics_cost), str(obj.id) + '_The_first_Logistics_cost')

            rt = u'%s<tr><th>实际发货总量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_deliver\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
                 u'<tr><th>发货箱数：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_deliver\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
                 u'<tr><th>发货重量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_deliver\')" %s title="%s"/><span id="%s"></span></th></tr> ' \
                 u'<tr><th>发货尺寸：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_deliver\')" %s title="%s"/><span id="%s"></span></th></tr> '\
                 u'<tr><th>备注：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_stocking_demand_fba_deliver\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
                 (rt, self.del_None(obj.Num), obj.id, 'Num', read,self.del_None(obj.Num), str(obj.id) + '_Num',
                  self.del_None(obj.BoxNum), obj.id, 'BoxNum', read, self.del_None(obj.BoxNum), str(obj.id) + '_BoxNum',
                  self.del_None(obj.BoxWeight), obj.id, 'BoxWeight', read, self.del_None(obj.BoxWeight),str(obj.id) + '_BoxWeight',
                  self.del_None(obj.BoxSize), obj.id, 'BoxSize', read, self.del_None(obj.BoxSize),str(obj.id) + '_BoxSize',
                  self.del_None(obj.remark), obj.id, 'remark', read, self.del_None(obj.remark),str(obj.id) + '_remark',)
            rt = rt + '</table>'
        except Exception, ex:
            rt = ''
            messages.info(self.request,"填写信息加载报错,请联系开发人员解决:%s"%(str(ex)))
        return mark_safe(rt)
    show_infors_number.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">填写信息</p>')

    list_display = ('Delivery_lot_number','show_status','show_All_ProductSKU_Num','edit_sku','show_infors_number','show_Supplierlink','Destination_warehouse','Delivery_date',
                    'show_Cargo_inforLink','show_Invoice_BoxPaste')
    list_editable = ('Delivery_date',)

    actions = ['generate_number', 'complete_delivery','get_excel_to_py','is_reject']

    def generate_number(self, request, objs):
        from app_djcelery.tasks import generate_fba_delivery_invoices
        idlist = []
        for obj in objs:
            idlist.append(obj.id)
            obj.getDetailedList = request.user.first_name
            obj.getDetailedTime = dattime.now()
            obj.save()
        # generate_delivery_invoices.delay(idlist)
        #generate_fba_delivery_invoices.delay(idlist,request.user.username)
        generate_fba_delivery_invoices(idlist, request.user.username)
        messages.success(request,u'发票正在生成中。。。请稍等刷新页面下载。。')
    generate_number.short_description = u'获取发货清单和箱标'

    def complete_delivery(self, request, objs):
        noConfirmList = []
        for obj in objs:
            if obj.Status == 'deliver':
                if obj.editFlag is None or obj.editFlag != '1' or obj.Num is None:
                    noConfirmList.append(obj.Delivery_lot_number)
                    continue
                t_stocking_demand_fba.objects.filter(Delivery_lot_number = obj.Delivery_lot_number).update(Status = 'completedeliver')
                obj.Sender = request.user.first_name
                obj.Delivery_date = dattime.now()
                obj.Status = 'completedeliver'
                obj.OplogTime=dattime.now()
                obj.save()

                t_stocking_demand_fba_detail.objects.filter(
                    Stocking_plan_number=obj.Stocking_plan_number).update(
                    Status='completedeliver')
        if noConfirmList:
            messages.info(self.request, "以下批次号:%s,实际发货数量未确认或未填写实际总数量,不能确认发货操作。" % (str(noConfirmList)))

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

            t_stocking_demand_fba_objs = t_stocking_demand_fba.objects.filter(Delivery_lot_number = qs.Delivery_lot_number)
            for obj in t_stocking_demand_fba_objs:
                warehouse = ''
                for ware in getChoices(ChoiceWarehouse):
                    if obj.Destination_warehouse == ware[0]:
                        warehouse = ware[1]

                level = ''
                for lev in getChoices(ChoiceLevel):
                    if obj.level == lev[0]:
                        level = lev[1]

                house = u'浦江集货仓'
                if ('%s'%obj.Single_number).find(u'DBD') != -1:
                    house = u'浦江仓库'

                thelist.append([qs.Delivery_lot_number,obj.ProductSKU,obj.ShopSKU,obj.checkCompleteNum,qs.Warehouse_number,qs.GoodsCategory,qs.The_first_Logistics_cost,
                                qs.LogisticsNumber,qs.Sender,batsta,obj.ProductPrice,house,warehouse,obj.ProductName,level,obj.Demand_people,obj.Remarks,obj.AccountNum])
        thelist.insert(0,[u'发货批次号',u'SKU',u'店铺SKU',u'发货数量',u'入库单号',u'货物品类',u'头程费用',u'	物流单号',u'发货人',u'本批次发货状态',
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
            from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
            for obj in objs:
                if obj.Status == 'deliver':
                    t_stocking_demand_fba.objects.filter(Delivery_lot_number=obj.Delivery_lot_number).update(Delivery_lot_number=None,Status='genbatch',genStatus=None)

                    obj.delete()
                    messages.success(request,u'驳回成功的备货计划号为:%s'%obj.Stocking_plan_number)
                else:
                    messages.error(request,u'已经发货的批次不允许驳回')
        else:
            messages.error(request, u'必须为超级用户才可以操作')

    is_reject.short_description = u'批次驳回(超级用户)'

    def save_models(self,):
        pass

    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_demand_fba_deliver_Admin, self).get_list_queryset()
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
                      'Delivery_date__gte':Delivery_dateStart, 'Delivery_date__lt':Delivery_dateEnd,
                      'All_ProductSKU_Num__icontains':All_ProductSKU_Num,
                      'Num__gte':NumStart, 'Num__lt':NumEnd,
                      'BoxNum__gte':BoxNumStart, 'BoxNum__lt':BoxNumEnd,
                      'BoxWeight__gte':BoxWeightStart, 'BoxWeight__lt':BoxWeightEnd,
                      'BoxSize__gte':BoxSizeStart, 'BoxSize__lt':BoxSizeEnd,
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
    
        return qs