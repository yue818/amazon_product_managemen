# -*- coding: utf-8 -*-
"""
 @desc:开发产品审核 如果是“通过审核”操作，记录审核人以及审核时间，将选中记录推送至“已开发带询价”界面
                    如果是“驳回“操作，请首先检测“产品专员备注”，如果为空，请提示错误，不予操作，如果“产品专员备注“不为空，将选中记录推送到”正在开发“界面
                    如果是”不开发“操作，请首先检测”产品专员备注“，如果为空，请提示错误，不予操作，如果“产品专员备注“不为空，将选中记录推送到”不开发产品“界面
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_product_develop_audit_Admin.py
 @time: 2018/5/04 16:53
"""
from .t_product_Admin import *
from datetime import datetime as ddtime
from brick.function.formatUrl import format_urls

class t_product_develop_audit_Admin(t_product_Admin):
    enter_ed_classification = True
    search_box_flag = True

    #save_on_top =True

    actions = ['to_wait_enquiry','to_reject','to_notdevelop' ]
    def to_reject(self, request, queryset):
        arr_Id = []
        from skuapp.table.t_product_develop_ing import t_product_develop_ing
        for querysetid in queryset.all():
            try:
                if querysetid.SpecialSell is not None and querysetid.SpecialSell.strip() != '':

                    t_product_develop_ing_obj = t_product_develop_ing()
                    t_product_develop_ing_obj.__dict__ = querysetid.__dict__
                    t_product_develop_ing_obj.AuditStaffName = request.user.first_name
                    t_product_develop_ing_obj.AuditTime = ddtime.now()
                    t_product_develop_ing_obj.save()

                    end_t_product_oplog(request, querysetid.MainSKU, 'BACK', querysetid.Name2, querysetid.id)

                else:
                    arr_Id.append(querysetid.id)
            except Exception, ex:
                messages.error(request, 'audit no pass id=%s error:'%(querysetid.id) + repr(ex))
        if len(arr_Id) != 0:
            messages.error(request, u'以下流水号:' + str(arr_Id) + u'产品专员备注为空，请添加产品专员备注后再驳回。')
    to_reject.short_description = u'审核不通过(驳回)'

    def to_notdevelop(self, request, queryset):
        arr_Id = []
        from skuapp.table.t_product_repeats import t_product_repeats
        for querysetid in queryset.all():
            try:
                if querysetid.SpecialSell is not None and querysetid.SpecialSell.strip() != '':
                    t_product_repeats_obj = t_product_repeats()
                    t_product_repeats_obj.__dict__ = querysetid.__dict__
                    t_product_repeats_obj.AuditStaffName = request.user.first_name
                    t_product_repeats_obj.AuditTime = ddtime.now()
                    t_product_repeats_obj.CreateTime = ddtime.now()
                    t_product_repeats_obj.CreateStaffName = request.user.first_name
                    t_product_repeats_obj.StaffID = request.user.username
                    t_product_repeats_obj.fromT = u't_product_develop_audit'
                    t_product_repeats_obj.save()

                    end_t_product_oplog(request, querysetid.MainSKU, 'NOKF', querysetid.Name2, querysetid.id)

                    querysetid.delete()
                else:
                    arr_Id.append(querysetid.id)
            except Exception, ex:
                messages.error(request, 'no develop id=%s error:'%(querysetid.id) + repr(ex))
        if len(arr_Id) != 0:
            messages.error(request, u'以下流水号:' + str(arr_Id) + u'产品专员备注为空，请添加产品专员备注后再驳回。')
    to_notdevelop.short_description = u'不开发'
    
    def show_SupplierName(self,obj):
        import datetime
        # from reportapp.models import t_report_supplier_sku_m
        from reportapp.table.t_report_supplier_sku_m import t_report_supplier_sku_m
        from pyapp.table.t_product_b_goods import t_product_b_goods
        from pyapp.models import B_Supplier
        from  pyapp.models import b_supplier_money

        supplierSkuCount = 0
        cgSkuCount = 0
        CGALLmoney = 0.00
        lastMonth = datetime.datetime.now().strftime('%Y%m')
        supplier_status = u'新'
        is_blacklist = u'否'
        try:
            if lastMonth[-2:] == '01':
                lastMonth = str((int(lastMonth[:4]) - 1)) + '12'
            else:
                lastMonth = str(int(lastMonth) - 1)

            SupplierName_num_objs = b_supplier_money.objects.filter(SupplierName=obj.SupplierID).values('CGSKUcount','CGALLmoney')
            if SupplierName_num_objs:
                cgSkuCount = SupplierName_num_objs[0]['CGSKUcount']
                CGALLmoney = SupplierName_num_objs[0]['CGALLmoney']
            SupplierID_param = B_Supplier.objects.filter(SupplierName=obj.SupplierID).values('NID', 'Used', 'IsBlacklist')
            if SupplierID_param:
                supplierSkuCount = t_product_b_goods.objects.filter(Q(GoodsStatus='正常')|Q(GoodsStatus='临时下架')|Q(GoodsStatus='在售'),SupplierID=SupplierID_param[0]['NID'],Used=0).count()

                if SupplierID_param[0]['Used'] in [0, '0']:
                    supplier_status = u'正常'
                else:
                    supplier_status = u'已停'

                if SupplierID_param[0]['IsBlacklist'] == 1:
                    is_blacklist = u'是'
        except Exception,ex:
            messages.error(request,'%s_%s:%s'%(traceback.print_exc(),Exception,ex))
        rr = u'供应商状态:%s<br>是否黑名单:%s<br>正常或临时状态SKU总数:%s<br>近一个月采购SKU总数:%s<br>近一个月采购总金额:%s'%\
             (supplier_status, is_blacklist, supplierSkuCount, cgSkuCount, CGALLmoney)

        return mark_safe(rr)
    show_SupplierName.short_description = mark_safe('<p align="center" style="width:150px;color:#428bca;">供应商采购信息</p>')
    
    def to_wait_enquiry(self, request, queryset):
        for querysetid in queryset.all():
            try:
                if querysetid.LargeCategory is not None and querysetid.LargeCategory.strip() != '' and querysetid.SmallCategory is not None and querysetid.SmallCategory.strip() != '':
                    #下一步
                    obj = t_product_wait_enquiry()
                    obj.__dict__ = querysetid.__dict__
                    obj.id = querysetid.id
                    obj.AuditStaffName = request.user.first_name
                    obj.AuditTime = ddtime.now()
                    obj.save()

                    end_t_product_oplog(request,querysetid.MainSKU,'PASS',querysetid.Name2,querysetid.id)

                    #记录调研调研历史
                    t_product_survey_history_obj = t_product_survey_history(SourcePicPath=querysetid.SourcePicPath,SourceURL=querysetid.SourceURL,SourcePicPath2=querysetid.SourcePicPath2,SupplierPUrl1=querysetid.SupplierPUrl1,StaffID=request.user.username,StaffName=request.user.first_name,pid=querysetid.id)
                    t_product_survey_history_obj.save()

                    querysetid.delete()
                else:
                    messages.error(request,u'大类或小类为空，请选择，并再次提交。')
            except Exception, ex:
                messages.error(request, 'audit pass id=%s error:'%(querysetid.id) + repr(ex))

    to_wait_enquiry.short_description = u'审核通过(待询价)'

    def show_messages(self,obj):
        rt = u'开发:%s <br>时间:%s <br>服装体系备注:%s'%(obj.KFStaffName,obj.KFTime,obj.ClothingNote)
        return mark_safe(rt)
    show_messages.short_description = u'<span style="color:#428bca;">信息</span>'
    
    # def show_urls(self,obj) :
    #     Platform,linkurl = format_urls(obj.SourceURL if obj.SourceURL else '')
    #     if 'can not formate' in Platform:
    #         linkurl = 'reverse_url'
    #     pSupplier,pSupplierurl =format_urls(obj.SupplierPUrl1 if obj.SupplierPUrl1 else '')
    #     if 'can not formate' in pSupplier:
    #         pSupplierurl = 'Supplierurl'
    #     rt = u'反:<a href="%s" target="_blank" >%s:%s</a><br>供:<a href="%s" target="_blank" >%s:%s</a>'%(obj.SourceURL,Platform,linkurl,obj.SupplierPUrl1,pSupplier,pSupplierurl)
    #     return mark_safe(rt)
    # show_urls.short_description = u'链接信息'


    #调研显示和编辑字段
    #list_display=('id','show_SourcePicPath','OrdersLast7Days','Pricerange','ShelveDay','Keywords','Keywords2','SpecialRemark','show_urls',)
    #list_editable=('OrdersLast7Days','Keywords','Keywords2','SpecialRemark','ShelveDay','Pricerange',)
    list_per_page=20
    list_display= ('id','KFStaffName','KFTime','SpecialSell','show_SourcePicPath','ShelveDay','OrdersLast7Days','ClothingSystem1','ClothingSystem2','ClothingSystem3','ClothingNote','Pricerange','Keywords','LargeCategory','show_SourcePicPath2','SupplierPDes','SupplierID','show_SupplierName','show_urls',)
    readonly_fields = ('SourcePicPath','SourcePicPath2','Pricerange','OrdersLast7Days','Keywords','Keywords2',)
    list_editable=('ClothingSystem1','ClothingSystem2','ClothingSystem3','ShelveDay','LargeCategory','SpecialSell','SupplierPDes','SupplierID',)
    list_filter=()
    search_fields=()


    #def get_queryset(self, request):
    def get_list_queryset(self):
        request = self.request

        qs = super(t_product_develop_audit_Admin, self).get_list_queryset()

        flagcloth = request.GET.get('classCloth', '')
        Cate1 = request.GET.get('cate1','')
        Cate2 = request.GET.get('cate2','')
        Cate3 = request.GET.get('cate3','')
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

        searchList = {  'MainSKU__exact':MainSKU,'ContrabandAttribute__exact':ContrabandAttribute,
                        'Storehouse__exact':Storehouse, 'LargeCategory__exact':LargeCategory,
                        'YNphoto__exact': YNphoto,'YNphoto__exact':YNphoto,'Buyer__exact':Buyer, 'DYStaffName__exact':DYStaffName,
                        'KFStaffName__exact':KFStaffName, 'XJStaffName__exact':XJStaffName, 'JZLStaffName__exact':JZLStaffName,
                        'PZStaffName__exact':PZStaffName, 'MGStaffName__exact':MGStaffName, 'LRStaffName__exact':LRStaffName,
                        'Weight__gte':WeightStart, 'Weight__lt':WeightEnd,
                        'UpdateTime__gte': updateTimeStart, 'UpdateTime__lt': updateTimeEnd,'ClothingSystem1__exact':Cate1,
                       'ClothingSystem2__exact': Cate2,'ClothingSystem3__exact':Cate3,
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

        if Cate1 !='':
            if Cate2 !='':
                if Cate3 !='':
                    qs = qs.filter(ClothingSystem3 = Cate3)
                else:
                    qs = qs.filter(ClothingSystem2 = Cate2)
            else:
                qs = qs.filter(ClothingSystem1 = Cate1)

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']
        if flagcloth == '1':
            return qs.filter(AuditStaffName = 'commitaudit').filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            return qs.filter(AuditStaffName = 'commitaudit').exclude(LargeCategory__in=catelist)
        else:
            return qs.filter(AuditStaffName = 'commitaudit')
            
        #return qs.filter(StaffID = request.user.username).filter(AuditStaffName = 'commitaudit')
