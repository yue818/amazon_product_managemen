# -*- coding: utf-8 -*-
from .t_product_Admin import *
from brick.public.django_wrap import django_wrap
from datetime import datetime
from brick.function.formatUrl import format_urls
from skuapp.table.t_product_art_pre_ed import t_product_art_pre_ed
from skuapp.table.t_product_art_ed import t_product_art_ed
from skuapp.table.t_product_enter_ed import t_product_enter_ed
from skuapp.table.t_product_enter_ing import t_product_enter_ing
class t_product_art_ing_Admin(t_product_Admin):
    enter_ed_classification = True
    #save_on_top =True
    search_box_flag = True
    sku_count= True
    actions = ['art_ed','to_recycle']


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



    def to_recycle(self, request, queryset):
        for obj in queryset:
            if len(t_product_enter_ed.objects.filter(MainSKU=obj.MainSKU))!=0:
                messages.error(request,obj.MainSKU+"该sku在录入完成中存在，不能删除")
                queryset=queryset.exclude(MainSKU=obj.MainSKU)
            else:
                try:
                    t_product_art_pre_ed.objects.filter(MainSKU=obj.MainSKU).delete()
                    t_product_art_ed.objects.filter(MainSKU=obj.MainSKU).delete()
                    t_product_enter_ing.objects.filter(MainSKU=obj.MainSKU).delete() 
                except Exception as e:
                    pass
        super(t_product_art_ing_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'

    def art_ed(self, request, objs):
        from skuapp.table.t_product_pic_completion import t_product_pic_completion
        for obj in objs:
            if obj.MGProcess == '1':# 待制作
                t_product_pic_completion_obj = t_product_pic_completion()
                t_product_pic_completion_obj.__dict__ = obj.__dict__
                t_product_pic_completion_obj.MGProcess='3' # 完成制作
                t_product_pic_completion_obj.MGStaffName=request.user.first_name
                t_product_pic_completion_obj.MGTime=datetime.now()
                t_product_pic_completion_obj.id = obj.id
                t_product_pic_completion_obj.save()

                t_product_enter_ed.objects.filter(id=obj.pid,MainSKU=obj.MainSKU).update(MGProcess='3',MGStaffName=request.user.first_name,MGTime=datetime.now())
                t_product_depart_get.objects.filter(pid=obj.pid,MainSKU=obj.MainSKU).update(MGProcess='3',MGStaffName=request.user.first_name,MGTime=datetime.now())
                end_t_product_oplog(request, obj.MainSKU, 'MG', obj.Name2, obj.pid)
                obj.delete()

            elif obj.MGProcess == '5': # 待换图
                t_product_pic_completion_obj = t_product_pic_completion()
                t_product_pic_completion_obj.__dict__ = obj.__dict__
                t_product_pic_completion_obj.MGProcess='6'
                t_product_pic_completion_obj.MGStaffName=request.user.first_name
                t_product_pic_completion_obj.MGTime = datetime.now()
                t_product_pic_completion_obj.id = obj.id
                t_product_pic_completion_obj.save()
                
                skucode = re.split(r'(\d+)',obj.MainSKU)
                if len(skucode)>=2:
                    newMainSKU = skucode[0] + skucode[1]
                else:
                    newMainSKU = obj.MainSKU

                t_product_enter_ed.objects.filter(MainSKU=newMainSKU).update(MGProcess='6',MGStaffName=request.user.first_name,MGTime=datetime.now())
                t_product_depart_get.objects.filter(MainSKU=newMainSKU).update(MGProcess='6',MGStaffName=request.user.first_name,MGTime=datetime.now())

                t_product_information_modify_objs = t_product_information_modify.objects.filter(InputBox=obj.MainSKU,id=obj.pid)
                for t_product_information_modify_obj in t_product_information_modify_objs:
                    if t_product_information_modify_obj.Mstatus == 'DHT':
                        t_product_information_modify_obj.Mstatus = 'WCHT'
                        t_product_information_modify_obj.XGStaffName = request.user.first_name
                        t_product_information_modify_obj.XGTime = datetime.now()
                        t_product_information_modify_obj.save()
                end_t_product_oplog(request, obj.MainSKU, 'MG', obj.Name2, obj.pid)
                obj.delete()

            elif obj.MGProcess == '7': # 实拍制作 完成
                t_product_pic_completion_obj = t_product_pic_completion()
                t_product_pic_completion_obj.__dict__ = obj.__dict__
                t_product_pic_completion_obj.MGTime = datetime.now()
                t_product_pic_completion_obj.MGStaffName = request.user.first_name
                t_product_pic_completion_obj.MGProcess = '2'
                t_product_pic_completion_obj.id = obj.id
                t_product_pic_completion_obj.save()

                t_product_enter_ed.objects.filter(id=obj.pid,MainSKU=obj.MainSKU).update(PZTime=obj.PZTime,PZStaffName=obj.PZStaffName,MGTime=datetime.now(),MGStaffName=request.user.first_name,MGProcess='2')
                t_product_depart_get.objects.filter(pid=obj.pid,MainSKU=obj.MainSKU).update(PZTime=obj.PZTime,PZStaffName=obj.PZStaffName,MGTime=datetime.now(),MGStaffName=request.user.first_name,MGProcess='2')
                end_t_product_oplog(request, obj.MainSKU, 'MG', obj.Name2, obj.pid)
                obj.delete()

    art_ed.short_description = u'美工完成'

    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.pid,MainSKU=obj.MainSKU).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_skulist_XG(self,obj) :
        rt = u'<table  style="text-align:center">' \
             u'<tr>' \
             u'<th style="text-align:center">子SKU-</th>' \
             u'<th style="text-align:center">属性-</th>' \
             u'<th style="text-align:center">单价-</th>' \
             u'<th style="text-align:center">克重-</th>' \
             u'<th style="text-align:center">包装规格-</th>' \
             u'<th style="text-align:center">内包装成本-</th>' \
             u'<th style="text-align:center">最小包装数-</th>' \
             u'<th style="text-align:center">服装类信息-</th>' \
             u'<th style="text-align:center">供应商链接</th>' \
             u'<th style="text-align:center">供应商货号</th>' \
             u'</tr>'
        if obj.MainSKU is not None:
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=obj.MainSKU).order_by('SKU')
            for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
                PackName = ''
                CostPrice = 0
                PackNID = t_product_mainsku_sku_obj.PackNID
                try:
                    if PackNID > 0:
                        B_PackInfo_obj = B_PackInfo.objects.get(id__exact=PackNID)
                        if B_PackInfo_obj is not None:
                            PackName = B_PackInfo_obj.PackName
                            CostPrice = B_PackInfo_obj.CostPrice
                except Exception, ex:
                    pass    

                SupplierLink = t_product_mainsku_sku_obj.SupplierLink
                if not SupplierLink:
                    SupplierLink = obj.SupplierPUrl1

                SupplierNum = t_product_mainsku_sku_obj.SupplierNum
                if not SupplierNum:
                    SupplierNum = obj.SupplierArtNO

                rt = u'%s <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' \
                     u'<td><input value="%s" style="width: 100px;border:none;background-color:transparent;" type="text" readonly title="%s"/></td>' \
                     u'<td><input value="%s" style="width: 100px;border:none;background-color:transparent;" type="text" readonly title="%s"/></td>' \
                     u'</tr> ' % \
                     (
                     rt, t_product_mainsku_sku_obj.SKU, t_product_mainsku_sku_obj.SKUATTRS, t_product_mainsku_sku_obj.UnitPrice,
                     t_product_mainsku_sku_obj.Weight, PackName, CostPrice, t_product_mainsku_sku_obj.MinPackNum,
                     t_product_mainsku_sku_obj.DressInfo, SupplierLink, SupplierLink,SupplierNum,SupplierNum
                     )

        rt = '%s</table>' % rt
        return mark_safe(rt)
    show_skulist_XG.short_description = mark_safe('<p align="center"> 子SKU信息</p>')
    
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
    # show_urls.short_description = u'链接信息'

    def show_messages2(self, obj):
        rt = u'%s <br>%s' % (obj.JZLStaffName, obj.JZLTime)
        return mark_safe(rt)
    show_messages2.short_description = u'建资料信息'

    def show_MainSKU(self,obj) :
        rt = django_wrap(obj.MainSKU,',',3)
        return mark_safe(rt)
    show_MainSKU.short_description = u'*主SKU'

    def show_PictureRequest(self,obj) :
        piclist = list((u'%s'%(obj.PictureRequest,)).replace('<br>',''))
        num = 0
        while True:
            num = num + 32
            if num >= len(piclist):
                break
            piclist.insert(num, '<br>')
        return mark_safe(''.join( piclist ))
    show_PictureRequest.short_description = u'图片要求'

    list_display= ('pid','show_PictureRequest','MGProcess','MGStaffName','MGTime','show_messages2','show_SourcePicPath2','show_MainSKU','show_skulist_XG','Name2','Material','SpecialSell','SalesApplicant','Entertime','show_urls','show_oplog')
    #list_display_links=('id','SourcePicPath2','MainSKU','Name2','Material','SpecialSell',)
    list_filter = ('UpdateTime',
                    'Weight',
                     'Buyer','ContrabandAttribute',
                    'Storehouse',
                    'DYStaffName','KFStaffName','XJStaffName','JZLStaffName','PZStaffName','MGStaffName','LRStaffName','LargeCategory',
                    'MGProcess',
                    )

    readonly_fields = ('pid','SKU',)
    #search_fields=('id','MainSKU','StaffID','Name2',)
    search_fields =None
     # 分组表单
    fieldsets = (
        (u'调研结果', {
            'fields': (
                ('id',),
                ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SpecialRemark','Pricerange','ShelveDay', ),
                ('Name','Tags',),
                ('SourcePicPath',),
                       ),
                }),

        (u'开发结果', {
            'fields': (
                ('SupplierPUrl1','SupplierPDes','SupplierID',),
                ('SourcePicPath2',)
                       ),
                }),

        (u'询价结果', {
            'fields': (
                ('UnitPrice','Weight','SpecialSell',),
                       ),
                }),

        (u'建资料', {
            'fields': (
                    ('Name2','Material','Unit',),
                    ('MinPackNum','MinOrder','SupplierArtNO','SupplierPColor','SupplierPUrl2',),
                    ('OrderDays','StockAlarmDays',),
                    ('LWH','SupplierContact','Storehouse',),
                       ),
                }),

        (u'违禁品属性', {
            'fields': (
                ('ContrabandAttribute',),
                       ),
                }),
        (u'备注信息', {'fields': ('Remark',)}),

        (u'SKU信息', {
            'fields': (
                ('LargeCategory','SmallCategory','Category3','MainSKU','SKU',),
                       ),
                }),


     )
    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.StaffID = request.user.username
        obj.save()

    def get_list_queryset(self,):
        request = self.request
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        qs = super(t_product_art_ing_Admin, self).get_list_queryset()
        
        # Electrification = request.GET.get('Electrification','')
        # Powder          = request.GET.get('Powder','')
        # Liquid          = request.GET.get('Liquid','')
        # Magnetism       = request.GET.get('Magnetism','')
        ContrabandAttribute = request.GET.get('ContrabandAttribute', '')
        Storehouse      = request.GET.get('Storehouse','')
        LargeCategory   = request.GET.get('LargeCategory','')
        MainSKU = request.GET.get('MainSKU','')
        MHMainSKU = request.GET.get('MHMainSKU','')

        YNphoto = request.GET.get('YNphoto','') # 图片处理 0实拍 1制作 
        MGProcess       = request.GET.get('MGProcess','')#图片状态 0待实拍 1待制作 2完成实拍 3完成制作 4错误
        
        Buyer           = request.GET.get('Buyer','')#采购员
        DYStaffName     = request.GET.get('DYStaffName','')#调研员
        KFStaffName     = request.GET.get('KFStaffName','')#开发员
        XJStaffName     = request.GET.get('XJStaffName','')#询价员
        JZLStaffName    = request.GET.get('JZLStaffName','')#建资料员
        PZStaffName     = request.GET.get('PZStaffName','')#拍照员
        MGStaffName     = request.GET.get('MGStaffName','')#美工员
        LRStaffName     = request.GET.get('LRStaffName','')#录入员
        flagcloth = request.GET.get('classCloth', '')
        
        WeightStart = request.GET.get('WeightStart','')#克重
        WeightEnd = request.GET.get('WeightEnd','')
    
        orders7DaysStart = request.GET.get('orders7DaysStart','')
        orders7DaysEnd = request.GET.get('orders7DaysEnd','')
        updateTimeStart = request.GET.get('updateTimeStart','')#refreshTimeStart
        updateTimeEnd = request.GET.get('updateTimeEnd', '')
        BJP_FLAG        = request.GET.get('BJP_FLAG','')

        searchList = { 'ContrabandAttribute__exact':ContrabandAttribute, 'MainSKU__exact':MainSKU,
                        'Storehouse__exact':Storehouse, 'LargeCategory__exact':LargeCategory,
                        'YNphoto__exact': YNphoto,'MGProcess__exact':MGProcess, 'Buyer__exact':Buyer, 'DYStaffName__exact':DYStaffName,
                        'KFStaffName__exact':KFStaffName, 'XJStaffName__exact':XJStaffName, 'JZLStaffName__exact':JZLStaffName,
                        'PZStaffName__exact':PZStaffName, 'MGStaffName__exact':MGStaffName, 'LRStaffName__exact':LRStaffName,
                        'Weight__gte':WeightStart, 'Weight__lt':WeightEnd, 'Orders7DaysAll__gte': orders7DaysStart, 'Orders7DaysAll__lt': orders7DaysEnd,
                        'UpdateTime__gte': updateTimeStart, 'UpdateTime__lt': updateTimeEnd,'MainSKU__contains':MHMainSKU,'BJP_FLAG__exact':BJP_FLAG,
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

        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=request.user.username,urltable="t_product_art_ing").count()
        except:
            pass 
        if request.user.is_superuser or flag != 0:
            qs = qs
        else:
            qs = qs.filter(MGStaffName=request.user.first_name)

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            return qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            return qs.exclude(LargeCategory__in=catelist)
        else:
            return qs
        

        
        
        
        
        