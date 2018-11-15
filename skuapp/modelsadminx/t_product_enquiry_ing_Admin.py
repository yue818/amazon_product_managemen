# -*- coding: utf-8 -*-
from .t_product_Admin import *
from datetime import datetime
from brick.function.formatUrl import format_urls

class t_product_enquiry_ing_Admin(t_product_Admin):
    enter_ed_classification = True
    search_box1_flag = True

    actions = ['enquiry_ed', 'to_wait_enquiry','to_repeats']
    def to_wait_enquiry(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_wait_enquiry()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username

            obj.XJTime = None
            obj.XJStaffName = None
            obj.save()

            querysetid.delete()
    to_wait_enquiry.short_description = u'退回到‘待询价’'

    def to_repeats(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_repeats()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username
            obj.fromT = u't_product_enquiry_ing'
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'XJ',querysetid.Name2,querysetid.id)
            t_product_mainsku_sku.objects.filter(pid=obj.id).delete()  # 删除主SKU下所有的子SKU属性
            querysetid.delete()
    to_repeats.short_description = u'不开发产品'

    def enquiry_ed(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_build_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username

            obj.XJTime = datetime.now()
            obj.XJStaffName = request.user.first_name

            obj.JZLTime = datetime.now()
            obj.JZLStaffName = request.user.first_name
            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'XJ',querysetid.Name2,querysetid.id)
            begin_t_product_oplog(request,querysetid.MainSKU,'JZL',querysetid.Name2,querysetid.id)
            querysetid.delete()
    enquiry_ed.short_description = u'询价完成'

    def to_recycle(self, request, queryset):
        super(t_product_enquiry_ing_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'
    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_messages(self,obj):
        rt = u'开发:%s <br>时间:%s <br>询价:%s <br>时间:%s' %(obj.KFStaffName,obj.KFTime,obj.XJStaffName,obj.XJTime)
        return mark_safe(rt)
    show_messages.short_description = u'<span style="color:#428bca;">信息</span>'

    def show_ClothingSystem(self,obj):
        rt = u'一级:%s <br>二级:%s <br>三级:%s ' %(obj.ClothingSystem1,obj.ClothingSystem2,obj.ClothingSystem3)
        return mark_safe(rt)
    show_ClothingSystem.short_description = u'<span style="color:#428bca">服装分类</span>'

    def show_SupplierID(self,obj):
        a = 1
        SupplierID = ''
        for sid in obj.SupplierID:
            SupplierID += sid
            if a%6 == 0:
                SupplierID += '<br>'
            a += 1
        return mark_safe(SupplierID)
    show_SupplierID.short_description = u'<span style="color:#428bca">供货商名称</span>'

    # def show_urls(self, obj):
    #     Platform, linkurl = format_urls(obj.SourceURL if obj.SourceURL else '')
    #     if 'can not formate' in Platform:
    #         linkurl = 'reverse_url'
    #     pSupplier, pSupplierurl = format_urls(obj.SupplierPUrl1 if obj.SupplierPUrl1 else '')
    #     if 'can not formate' in pSupplier:
    #         pSupplierurl = 'Supplierurl'
    #     rt = u'反:<a href="%s" target="_blank" >%s:%s</a><br>供:<a href="%s" target="_blank" >%s:%s</a>' % (
    #     obj.SourceURL, Platform, linkurl, obj.SupplierPUrl1, pSupplier, pSupplierurl)
    #     return mark_safe(rt)
    # show_urls.short_description = u'<span style="color:#428bca">链接信息</span>'

    def show_KFStaffName(self,obj):
        rt = u'开发: %s<br> 时间:%s <br>审核: %s <br> 时间:%s <br>询价: %s <br> 时间:%s' % (obj.KFStaffName,obj.KFTime,obj.DYSHStaffName,obj.DYSHTime,obj.XJStaffName,obj.XJTime)
        return mark_safe(rt)
    show_KFStaffName.short_description = u'<span style="color:#428bca">开发-时间/审核-时间/询价-时间</span>'

    list_display= ('id','show_KFStaffName','show_SourcePicPath','SpecialSell','SpecialRemark','ShelveDay','OrdersLast7Days','Pricerange','show_ClothingSystem','ClothingNote','show_SourcePicPath2','SupplierPDes','show_SupplierID','UnitPrice','Weight','show_urls',)

    list_editable=('SupplierPDes','Weight','UnitPrice','SpecialSell','ClothingNote',)
    list_filter = ('UpdateTime',
                    'Weight',
                    # 'Electrification','Powder','Liquid','Magnetism','Buyer',
                    'ContrabandAttribute',
                    'ContrabandAttribute', 'Buyer',
                    'Storehouse',
                    'DYStaffName','JZLStaffName','PZStaffName','MGStaffName','LRStaffName','LargeCategory','StaffID',
                    )
    fields =  ('SupplierPUrl1','SupplierPDes','UnitPrice','Weight','SpecialSell')
    list_filter = ()
    search_fields = ()
    form_layout = (
        Fieldset(u'询价结果',
                    Row('SupplierPUrl1','',''),
                    Row('SupplierPDes', 'UnitPrice','Weight',),
                    Row('SpecialSell','','',),
                    css_class = 'unsort '
                )
                  )

    def get_list_queryset(self):
        request = self.request
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        qs = super(t_product_enquiry_ing_Admin, self).get_list_queryset()

        flagcloth = request.GET.get('classCloth', '')
        Cate1 = request.GET.get('cate1','')
        Cate2 = request.GET.get('cate2','')
        Cate3 = request.GET.get('cate3','')
        
        # Electrification = request.GET.get('Electrification','')     # 是否带电
        # Powder          = request.GET.get('Powder','')              # 是否粉末
        # Liquid          = request.GET.get('Liquid','')              # 是否液体
        # Magnetism       = request.GET.get('Magnetism','')           # 是否带磁
        ContrabandAttribute = request.GET.get('ContrabandAttribute', '')
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
        StaffID         = request.GET.get('StaffID','')         #工号
        
        WeightStart = request.GET.get('WeightStart','')#克重
        WeightEnd = request.GET.get('WeightEnd','')
    
        updateTimeStart = request.GET.get('updateTimeStart','')#更新时间
        updateTimeEnd = request.GET.get('updateTimeEnd', '')

        searchList = {  'MainSKU__exact':MainSKU,'ContrabandAttribute__exact':ContrabandAttribute,
                        'Storehouse__exact':Storehouse, 'LargeCategory__exact':LargeCategory,
                        'YNphoto__exact': YNphoto,'StaffID__exact':StaffID,'Buyer__exact':Buyer, 'DYStaffName__exact':DYStaffName,
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
            qs = qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            qs = qs.exclude(LargeCategory__in=catelist)
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=request.user.username,urltable="t_product_enquiry_ing").count()
        except:
            pass
        if request.user.is_superuser or flag != 0:
            return qs
        return qs.filter(StaffID = request.user.username)

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        #from django.db import connection
        obj = self.new_obj
        request = self.request
        old_obj = None

        if obj is None or obj.id is None or obj.id <=0:
            obj.id = self.get_id()
        else:
            old_obj = self.model.objects.get(pk=obj.pk)
        #
        if old_obj:
            obj.ClothingSystem1 = old_obj.ClothingSystem1
            obj.ClothingSystem2 = old_obj.ClothingSystem2
            obj.ClothingSystem3 = old_obj.ClothingSystem3

        obj.save()
        # raise Exception(connection.queries)

        #读取供应商信息
        self.read1688_2(request,old_obj,obj)

        obj.save()

