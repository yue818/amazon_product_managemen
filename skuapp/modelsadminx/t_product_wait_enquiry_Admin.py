# -*- coding: utf-8 -*-
from .t_product_Admin import *
from datetime import datetime
from brick.function.formatUrl import format_urls

class t_product_wait_enquiry_Admin(t_product_Admin):
    enter_ed_classification = True
    search_box1_flag = True

    actions = ['to_enquiry_ing', 'to_repeats',]
    def to_repeats(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_repeats()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username
            obj.fromT = self.model._meta.verbose_name
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'XJ',querysetid.Name2,querysetid.id)
            t_product_mainsku_sku.objects.filter(pid=obj.id).delete()  # 删除主SKU下所有的子SKU属性
            querysetid.delete()
    to_repeats.short_description = u'不开发产品'

    def to_recycle(self, request, queryset):
        super(t_product_wait_enquiry_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'

    def to_enquiry_ing(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_enquiry_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.XJTime = datetime.now()
            obj.XJStaffName = request.user.first_name
            obj.save()

            begin_t_product_oplog(request,querysetid.MainSKU,'XJ',querysetid.Name2,querysetid.id)
            querysetid.delete()
    to_enquiry_ing.short_description = u'领取去询价'
    
    def show_messages(self,obj):
        rt = u'开发:%s <br>时间:%s <br>服装体系备注:%s'%(obj.KFStaffName,obj.KFTime,obj.ClothingNote)
        return mark_safe(rt)
    show_messages.short_description = u'<span style="color:#428bca;">信息</span>'
    
    def show_ClothingSystem(self,obj):
        rt = u'一级:%s <br>二级:%s <br>三级:%s ' %(obj.ClothingSystem1,obj.ClothingSystem2,obj.ClothingSystem3)
        return mark_safe(rt)
    show_ClothingSystem.short_description = u'<span style="color:#428bca">服装分类</span>'
    
    def show_Supplier(self,obj):
        rt = u'名称:%s <br>商品标题:%s' %(obj.SupplierID,obj.SupplierPDes)
        return mark_safe(rt)
    show_Supplier.short_description = u'<span style="color:#428bca">供货商信息</span>'

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

    def show_KFStaffName(self,obj):
        rt = u'开发: %s<br> 时间:%s <br>审核: %s <br> 时间:%s <br>询价: %s <br> 时间:%s' % (obj.KFStaffName,obj.KFTime,obj.DYSHStaffName,obj.DYSHTime,obj.XJStaffName,obj.XJTime)
        return mark_safe(rt)
    show_KFStaffName.short_description = u'<span style="color:#428bca">开发-时间/审核-时间/询价-时间</span>'

    list_display= ('id','show_KFStaffName','show_SourcePicPath','SpecialRemark','SpecialSell','OrdersLast7Days','Keywords','show_ClothingSystem','ClothingNote','LargeCategory','Pricerange','show_SourcePicPath2','show_Supplier','show_urls',)
    list_editable=('SpecialRemark','ClothingNote','LargeCategory','SpecialSell')
    #def save_model(self, request, obj, form, change):
    list_filter = ()
    search_fields = ()

    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.save()
        
    def get_list_queryset(self):
        request = self.request
        qs = super(t_product_wait_enquiry_Admin, self).get_list_queryset()

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
        AuditStaffName     = request.GET.get('AuditStaffName', '')  # 录入员
        
        WeightStart = request.GET.get('WeightStart','')#克重
        WeightEnd = request.GET.get('WeightEnd','')
    
        updateTimeStart = request.GET.get('updateTimeStart','')#更新时间
        updateTimeEnd = request.GET.get('updateTimeEnd', '')

        searchList = { 'MainSKU__exact':MainSKU,'ContrabandAttribute__exact':ContrabandAttribute,
                       'Storehouse__exact':Storehouse, 'LargeCategory__exact':LargeCategory,
                        'YNphoto__exact': YNphoto,'YNphoto__exact':YNphoto,'Buyer__exact':Buyer, 'DYStaffName__exact':DYStaffName,
                        'KFStaffName__exact':KFStaffName, 'XJStaffName__exact':XJStaffName, 'JZLStaffName__exact':JZLStaffName,
                        'PZStaffName__exact':PZStaffName, 'MGStaffName__exact':MGStaffName, 'LRStaffName__exact':LRStaffName,
                        'AuditStaffName__exact':AuditStaffName,'Weight__gte':WeightStart, 'Weight__lt':WeightEnd,
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

        if Cate1 != '':
            if Cate2 != '':
                if Cate3 != '':
                    qs = qs.filter(ClothingSystem3=Cate3)
                else:
                    qs = qs.filter(ClothingSystem2=Cate2)
            else:
                qs = qs.filter(ClothingSystem1=Cate1)

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            return qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            return qs.exclude(LargeCategory__in=catelist)
        else:
            return qs