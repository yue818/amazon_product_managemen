# -*- coding: utf-8 -*-
from .t_product_Admin import *
from datetime import datetime as ddtime
from skuapp.table.t_product_photograph import t_product_photograph
from skuapp.table.t_product_photo_ing import t_product_photo_ing
from skuapp.table.t_product_develop_ed import t_product_develop_ed
from skuapp.table.t_product_art_ing import t_product_art_ing
from brick.table.b_supplier import b_supplier as br_b_supplier
from django.db import connection
br_b_supplier_obj = br_b_supplier(db_conn=connection)



class t_product_art_ed_Admin(t_product_Admin):
    search_box_flag = False

    def delete_models(self, queryset):
        from skuapp.table.Delete_Log_model import Delete_Log_Model
        from django.forms.models import model_to_dict
        import datetime
        insert_list=[]
        fmt_str_list=[]
        for obj in queryset:
            result=obj.delete()
            if result[0]==1:
                params=model_to_dict(obj)
                for k,v in params.items():
                    if isinstance(v, datetime.datetime):
                        v = v.strftime('%Y-%m-%d %H:%M:%S')
                    fmt_str=r'"{}":"{}"'.format(str(k),str(v))
                    fmt_str_list.append(fmt_str)
                delete_content='{'+','.join(fmt_str_list)+'}'
                sku=params.get('MainSKU')
                insert_row=Delete_Log_Model(actiontime=datetime.datetime.now(),username=self.user,sku=sku,where=self.model_name,delete_content=delete_content)
                insert_list.append(insert_row)
        try:
            Delete_Log_Model.objects.bulk_create(insert_list)
        except:
            pass




    actions = ['to_repeats_art_ed','to_not_pass_art_ed','to_pass_art_ed','to_recycle',]
    def to_repeats_art_ed(self, request, queryset):

        for querysetid in queryset.all():
                obj = t_product_repeats()
                obj.__dict__ = querysetid.__dict__
                obj.id = querysetid.id
                obj.CreateTime = ddtime.now()
                obj.CreateStaffName = request.user.first_name
                obj.StaffID= request.user.username
                obj.save()
                #不开发产品删除拍照美工中的数据
                try:
                    t_product_photograph.objects.filter(MainSKU=querysetid.MainSKU).delete()
                    t_product_photo_ing.objects.filter(MainSKU=querysetid.MainSKU).delete()
                    t_product_develop_ed.objects.filter(MainSKU=querysetid.MainSKU).delete()
                    t_product_art_ing.objects.filter(MainSKU=querysetid.MainSKU).delete()
                except Exception as e:
                    raise e
                 

                end_t_product_oplog(request,querysetid.MainSKU,'SH',querysetid.Name2,querysetid.id)
                t_product_mainsku_sku.objects.filter(pid=obj.id).delete()  # 删除主SKU下所有的子SKU属性
                querysetid.delete()

            

    to_repeats_art_ed.short_description = u'不开发产品'

    def to_recycle(self, request, queryset):
        for obj in queryset: 
            try:
                t_product_photograph.objects.filter(MainSKU=obj.MainSKU).delete()
                t_product_photo_ing.objects.filter(MainSKU=obj.MainSKU).delete()
                t_product_develop_ed.objects.filter(MainSKU=obj.MainSKU).delete()
                t_product_art_ing.objects.filter(MainSKU=obj.MainSKU).delete() 
            except Exception as e:
                raise e           
        super(t_product_art_ed_Admin, self).to_recycle(request, queryset)
        
       
    to_recycle.short_description = u'扔进回收站'
    def to_not_pass_art_ed(self, request, queryset):

        for querysetid in queryset.all():
            obj = t_product_build_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = ddtime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            #录入员和录入员此阶段为空，保存审核人和审核人ID add by wangzy 20180326
            obj.PZStaffName = request.user.username
            obj.LRStaffName = request.user.first_name

            t_product_oplog_objs = t_product_oplog.objects.filter(pid = querysetid.id,StepID='JZL')[0:1]
            if t_product_oplog_objs.exists():
                obj.StaffID= t_product_oplog_objs[0].OpID
            obj.save()

            #修改操作记录
            t_product_oplog.objects.filter(pid = querysetid.id,StepID='JZL').update(MainSKU  = '',EndTime = ddtime.now())
            querysetid.delete()

    to_not_pass_art_ed.short_description = u'审核不通过'
    def to_pass_art_ed(self, request, queryset):
        #from datetime import datetime as datime
        for querysetid in queryset.all():
            obj = t_product_enter_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = ddtime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()
            end_t_product_oplog(request, querysetid.MainSKU, 'SH', querysetid.Name2, querysetid.id)
            begin_t_product_oplog(request, querysetid.MainSKU, 'LR', querysetid.Name2, querysetid.id)
            t_product_oplog.objects.filter(pid=querysetid.id, StepID='LR').update(OpID=request.user.username,OpName=request.user.first_name,BeginTime=ddtime.now(),)

            querysetid.delete()

    to_pass_art_ed.short_description = u'审核通过'

    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id,StepID='JZL',MainSKU=obj.MainSKU).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'



    def show_PackName(self,obj) :
        rt = ''
        PackNID= obj.PackNID
        if PackNID <=0 :
            return rt
        B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
        if B_PackInfo_obj is not None:
            rt =  B_PackInfo_obj.PackName
        return rt
    show_PackName.short_description = u'包装规格'

    def show_CostPrice(self,obj) :
        rt = ''
        PackNID= obj.PackNID
        if PackNID <=0 :
            return rt
        B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
        if B_PackInfo_obj is not None:
            rt =  B_PackInfo_obj.CostPrice
        return rt
    show_CostPrice.short_description = u'内包装成本'

    def show_Remark(self,obj) :
        return mark_safe(u'【%s】<br>%s<br>%s<br>%s'%(obj.LWH,obj.Remark,obj.SupplierPUrl1,obj.SupplierPUrl2 ))
    show_Remark.short_description = u'备注'
    
    def show_SupplierName(self,obj):
        import datetime
        # from reportapp.models import t_report_supplier_sku_m
        from reportapp.table.t_report_supplier_sku_m import t_report_supplier_sku_m
        from pyapp.table.t_product_b_goods import t_product_b_goods
        from pyapp.models import B_Supplier
        from  pyapp.models import b_supplier_money
        
        try:
            supplierSkuCount = 0
            cgSkuCount = 0
            CGALLmoney = 0.00
            lastMonth = datetime.datetime.now().strftime('%Y%m')

            if lastMonth[-2:] == '01':
                lastMonth = str((int(lastMonth[:4]) - 1)) + '12'
            else:
                lastMonth = str(int(lastMonth) - 1)

            SupplierName_num_objs = b_supplier_money.objects.filter(SupplierName=obj.SupplierID).values('CGSKUcount','CGALLmoney')
            if SupplierName_num_objs:
                cgSkuCount = SupplierName_num_objs[0]['CGSKUcount']
                CGALLmoney = SupplierName_num_objs[0]['CGALLmoney']
            SupplierID_param = B_Supplier.objects.filter(SupplierName=obj.SupplierID).values('NID')
            if SupplierID_param:
                supplierSkuCount = t_product_b_goods.objects.filter(Q(GoodsStatus='正常')|Q(GoodsStatus='临时下架')|Q(GoodsStatus='在售'),SupplierID=SupplierID_param[0]['NID'],Used=0).count()
        except Exception,ex:
            messages.error(request,'%s_%s:%s'%(traceback.print_exc(),Exception,ex))
        return mark_safe(u'%s<br>当前供应商下商品SKU状态为正常或临时下架的总数量:%s<br>近一个月采购SKU总数:%s<br>近一个月采购总金额:%s'%(obj.SupplierID,supplierSkuCount,cgSkuCount,CGALLmoney))
    show_SupplierName.short_description = mark_safe('<p align="center" style="width:150px;color:#428bca;">供应商信息</p>')
    
    def show_wjp(self,obj) :
        rt = ''
        if obj.ContrabandAttribute == '普货':
            rt = ''
        else:
            rt = obj.ContrabandAttribute
        return rt
    show_wjp.short_description = u'违禁品'

    def show_name2(self,obj) :
        PrepackMark = obj.PrepackMark
        if PrepackMark is None:
            PrepackMark=''
        Name2 = obj.Name2
        if obj.ContrabandAttribute and obj.ContrabandAttribute != u'普货':
            if obj.SmallCategory != u'手表': #手表特殊
                wjp = u'-违禁品'
                return u'%s%s%s'%(Name2,wjp,PrepackMark)
        return u'%s%s'%(Name2,PrepackMark)
    show_name2.short_description = mark_safe(u'商品<br>名称<br>(中文)')

    def show_supplier_status(self,obj) :
        uf = br_b_supplier_obj.GetSupplierStatus(obj.SupplierID)
        if uf and int(uf) == 1:
            SupplierUSED = u'已停用'
        elif uf and int(uf) == 0:
            SupplierUSED = u'正常'
        else:
            SupplierUSED = u'新'
        return SupplierUSED
    show_supplier_status.short_description = u'供应商状态'


    list_display= ('id','JZLTime','JZLStaffName','show_SourcePicPath2','MainSKU','Buyer','possessMan2','SpecialRemark','PrepackMark','show_skulist','LargeCategory','SmallCategory','show_name2','Material','SupplierArtNO','Unit','MinOrder','show_SupplierName','show_supplier_status','ReportName','ReportName2','show_oplog','show_wjp','show_Remark','auditnote')
    #list_display_links= ('id','SourcePicPath2',)#,'MainSKU','LargeCategory','SmallCategory','Name2','Material','SupplierArtNO','Unit','MinPackNum','SupplierID','Keywords2','Keywords',)
    list_editable=('SpecialRemark','Buyer','possessMan2','PrepackMark','auditnote')
    #readonly_fields = ('id',)
    #search_fields=('id','MainSKU','Name2','StaffID',)
    #list_filter = ('UpdateTime',)

    # 分组表单
    fields = ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SpecialRemark',
              'Pricerange','ShelveDay','Name','Tags', #u'调研结果',
              'SupplierPUrl1','SupplierPDes','SupplierID', # u'开发结果',
              'UnitPrice','Weight','SpecialSell', #u'询价结果',
              'Name2','Material','Unit','MinOrder','SupplierArtNO',
              'SupplierPColor','SupplierPUrl2','OrderDays','StockAlarmDays','LWH',
              'SupplierContact','Storehouse','ReportName','ReportName2','MinPackNum',#建资料
              'ContrabandAttribute',#'Electrification','Powder','Liquid','Magnetism',  #u'违禁品',
              'Remark', #备注
              'MainSKU', #主SKU
              'DYTime','DYStaffName','DYSHTime','DYSHStaffName','XJTime','XJStaffName','KFTime','KFStaffName','JZLTime','JZLStaffName',
              'PZTime','PZStaffName','MGTime','MGStaffName','LRTime','LRStaffName','AI_FLAG','SourceURL2','IP_FLAG'
              )

    form_layout = (
        Fieldset(u'调研结果',
                    Row('SourceURL','SourceURL2'),
                    Row('OrdersLast7Days','Pricerange', ''),
                    Row('Keywords','Keywords2','Tags'),
                    Row('ShelveDay','Name','SpecialRemark'),
                    css_class = 'unsort '
                ),
        Fieldset(u'开发&询价',
                    Row('SupplierPUrl1','SupplierPDes','SupplierID'),
                    Row('UnitPrice','Weight','SpecialSell'),
                    css_class = 'unsort  '
                ),
        Fieldset(u'建资料',
                    Row('Name2','Material','Unit'),
                    Row('MinOrder','SupplierArtNO', 'SupplierPColor'),
                    Row('SupplierPUrl2','OrderDays','StockAlarmDays'),
                    Row('LWH', 'SupplierContact','Storehouse'),
                    Row('ReportName','ReportName2','MinPackNum'),
                    Row('AI_FLAG','IP_FLAG',''),
                    css_class = 'unsort '
                ),
        Fieldset(u'违禁品',
                    Row('ContrabandAttribute',),
                    css_class = 'unsort '
                ),
        Fieldset(u'备注信息',
                    Row('Remark'),
                    css_class = 'unsort '
                ),
        Fieldset(u'主SKU信息',
                    Row('MainSKU'),
                    css_class = 'unsort '
                ),

                  )
    show_detail_fields = ['id']
    def get_list_queryset(self):
        request = self.request
        qs = super(t_product_art_ed_Admin, self).get_list_queryset()
        if request.user.is_superuser:
            return qs
        return qs.filter(StaffID = request.user.username)
     
    def get_list_queryset(self,):
        request = self.request
        qs = super(t_product_art_ed_Admin, self).get_list_queryset()
        
        # Electrification = request.GET.get('Electrification','')     # 是否带电
        # Powder          = request.GET.get('Powder','')              # 是否粉末
        # Liquid          = request.GET.get('Liquid','')              # 是否液体
        # Magnetism       = request.GET.get('Magnetism','')           # 是否带磁
        ContrabandAttribute  = request.GET.get('ContrabandAttribute','')    #商品属性
        Storehouse      = request.GET.get('Storehouse','')          # 发货仓库
        LargeCategory   = request.GET.get('LargeCategory','')       # 大类名称
        MainSKU = request.GET.get('MainSKU','')                     # 主SKU
        
        YNphoto = request.GET.get('YNphoto','') # 图片处理 0实拍 1制作 
        
        Buyer           = request.GET.get('Buyer','')           #采购员
        DYStaffName     = request.GET.get('DYStaffName','')     #调研员
        KFStaffName     = request.GET.get('KFStaffName','')     #开发员
        XJStaffName     = request.GET.get('XJStaffName','')     #询价员
        JZLStaffName    = request.GET.get('JZLStaffName','')    #建资料员
        PZStaffName     = request.GET.get('PZStaffName','')     #拍照员
        MGStaffName     = request.GET.get('MGStaffName','')     #美工员
        LRStaffName     = request.GET.get('LRStaffName','')     #录入员
        
        WeightStart = request.GET.get('WeightStart','')#克重
        WeightEnd = request.GET.get('WeightEnd','')
    
        updateTimeStart = request.GET.get('updateTimeStart','')#更新时间
        updateTimeEnd = request.GET.get('updateTimeEnd', '')

        searchList = { 'MainSKU__exact':MainSKU,'ContrabandAttribute__exact':ContrabandAttribute,
                        'Storehouse__exact':Storehouse, 'LargeCategory__exact':LargeCategory,
                        'YNphoto__exact': YNphoto,'Buyer__exact':Buyer, 'DYStaffName__exact':DYStaffName,
                        'KFStaffName__exact':KFStaffName, 'XJStaffName__exact':XJStaffName, 'JZLStaffName__exact':JZLStaffName,
                        'PZStaffName__exact':PZStaffName, 'MGStaffName__exact':MGStaffName, 'LRStaffName__exact':LRStaffName,
                        'Weight__gte':WeightStart, 'Weight__lt':WeightEnd, 
                        'UpdateTime__gte': updateTimeStart, 'UpdateTime__lt': updateTimeEnd,
                        }

        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    #if k == 'ShopName__exact':
                        #v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
                
        if request.user.is_superuser:
            return qs
        return qs.filter(StaffID = request.user.username)
        

