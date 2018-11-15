# -*- coding: utf-8 -*-
from .t_product_Admin import *
from brick.public.django_wrap import django_wrap
from datetime import datetime
from brick.function.formatUrl import format_urls
class t_product_develop_ed_Admin(t_product_Admin):
    search_box_flag = True
    enter_ed_classification = True
    sku_count= True
    actions = ['art_ing', ]

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





    def art_ing(self, request, queryset):

        for querysetid in queryset.all():
            #下一步
            obj = t_product_art_ing()
            obj.__dict__ = querysetid.__dict__
            obj.Entertime=datetime.now()
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.MGStaffName = request.user.first_name
            obj.MGTime = datetime.now()
            obj.save()

            begin_t_product_oplog(request,querysetid.MainSKU,'MG',querysetid.Name2,querysetid.pid)
            querysetid.delete()

    art_ing.short_description = u'领用美工任务'
    
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

    def to_recycle(self, request, queryset):
        super(t_product_develop_ed_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'

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
        if obj.MainSKU is not None and obj.MGProcess != '5':
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
                         rt, t_product_mainsku_sku_obj.SKU, t_product_mainsku_sku_obj.SKUATTRS,
                         t_product_mainsku_sku_obj.UnitPrice,
                         t_product_mainsku_sku_obj.Weight, PackName, CostPrice, t_product_mainsku_sku_obj.MinPackNum,
                         t_product_mainsku_sku_obj.DressInfo, SupplierLink, SupplierLink,SupplierNum,SupplierNum
                     )

        rt = '%s</table>' % rt
        return mark_safe(rt)
    show_skulist_XG.short_description = mark_safe('<p align="center"> 子SKU信息</p>')

    def show_Request(self,obj) :
        piclist = list((u'%s'%(obj.PictureRequest,)).replace('<br>',''))
        num = 0
        while True:
            num = num + 32
            if num >= len(piclist):
                break
            piclist.insert(num, '<br>')
        return mark_safe(''.join( piclist ))
    show_Request.short_description = u'图片要求备注'

    def show_MainSKU(self,obj) :
        rt = django_wrap(obj.MainSKU,',',3)
        return mark_safe(rt)
    show_MainSKU.short_description = u'*主SKU'

    list_display= ('pid','JZLTime','JZLStaffName','MGProcess','show_Request','show_SourcePicPath2','show_MainSKU','show_skulist_XG','Name2','Material','SpecialSell','StaffID','SalesApplicant','Entertime','show_oplog','show_urls',)
    search_fields = ('pid', 'MainSKU', 'StaffID', 'Name2',)
    readonly_fields = ('pid','SourcePicPath','SourcePicPath2','Pricerange','OrdersLast7Days',)
    list_display_links=('',)
    #
    # readonly_fields = ('id','SKU',)
    # #search_fields=('id','MainSKU','StaffID','Name2',)
    #  # 分组表单
    # fieldsets = (
    #     (u'调研结果', {
    #         'fields': (
    #             ('id',),
    #             ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SpecialRemark','Pricerange','ShelveDay', ),
    #             ('Name','Tags',),
    #             ('SourcePicPath',),
    #                    ),
    #             }),
    #
    #     (u'开发结果', {
    #         'fields': (
    #             ('SupplierPUrl1','SupplierPDes','SupplierID',),
    #             ('SourcePicPath2',)
    #                    ),
    #             }),
    #
    #     (u'询价结果', {
    #         'fields': (
    #             ('UnitPrice','Weight','SpecialSell',),
    #                    ),
    #             }),
    #
    #     (u'建资料', {
    #         'fields': (
    #                 ('Name2','Material','Unit',),
    #                 ('MinPackNum','MinOrder','SupplierArtNO','SupplierPColor','SupplierPUrl2',),
    #                 ('OrderDays','StockAlarmDays',),
    #                 ('LWH','SupplierContact','Storehouse',),
    #                    ),
    #             }),
    #
    #     (u'违禁品属性', {
    #         'fields': (
    #             ('Electrification','Powder','Liquid','Magnetism',),
    #                    ),
    #             }),
    #     (u'备注信息', {'fields': ('Remark',)}),
    #
    #     (u'SKU信息', {
    #         'fields': (
    #             ('LargeCategory','SmallCategory','Category3','MainSKU','SKU',),
    #                    ),
    #             }),
    #
    #
    #  )

    #def save_model(self, request, obj, form, change):
    # def save_models(self):
    #     obj = self.new_obj
    #     request = self.request
    #     obj.StaffID = request.user.username
    #     obj.save()
    #     if request.method == 'POST':
    #         files = request.FILES.getlist('myfiles')
    #         if obj.ArtPicPath is None :
    #             obj.ArtPicPath = ' '
    #         for f in files :
    #             if  obj.ArtPicPath.find(f.name) < 0 :
    #                 obj.ArtPicPath  += f.name+ r'; '
    #             obj.save()
    #
    #             path = MEDIA_ROOT + 'upload_imgs/' + str(obj.id)
    #             if not os.path.exists(path):
    #                 os.mkdir(path)
    #             destination = open(path + '/' +  f.name,'wb+')
    #             for chunk in f.chunks():
    #               destination.write(chunk)
    #             destination.close()
    #
    #             #先删除重复的图片路径
    #             t_product_pictures.objects.filter(TradeID=obj.id,ArtPicPath='upload_imgs/' + str(obj.id) + '/'  +  f.name).delete()
    #             #保存数据库 t_product_pictures 路径
    #             t_product_pictures_obj = t_product_pictures(TradeID=obj.id,ArtPicPath='upload_imgs/' + str(obj.id) + '/'  +  f.name)
    #             t_product_pictures_obj.save()
                
    def get_list_queryset(self,):
        from django.db.models import Q
        request = self.request
        flagcloth = request.GET.get('classCloth', '')
        qs = super(t_product_develop_ed_Admin, self).get_list_queryset()

        ContrabandAttribute = request.GET.get('ContrabandAttribute', '')
        Storehouse      = request.GET.get('Storehouse','')          # 发货仓库
        LargeCategory   = request.GET.get('LargeCategory','')       # 大类名称
        mgprocess       = request.GET.get('MGProcess','')           # 图片状态
        MainSKU = request.GET.get('MainSKU','')                     # 主SKU
        MHMainSKU = request.GET.get('MHMainSKU','')                     # 主SKU

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
        BJP_FLAG        = request.GET.get('BJP_FLAG','')

        searchList = { 'ContrabandAttribute__exact':ContrabandAttribute, 'Storehouse__exact':Storehouse, 'LargeCategory__exact':LargeCategory,
                        'YNphoto__exact': YNphoto,'Buyer__exact':Buyer, 'DYStaffName__exact':DYStaffName,
                        'KFStaffName__exact':KFStaffName, 'XJStaffName__exact':XJStaffName, 'JZLStaffName__exact':JZLStaffName,
                        'PZStaffName__exact':PZStaffName, 'MGStaffName__exact':MGStaffName, 'LRStaffName__exact':LRStaffName,
                        'Weight__gte':WeightStart, 'Weight__lt':WeightEnd, 'MainSKU__contains':MHMainSKU,'MainSKU__exact':MainSKU,
                        'UpdateTime__gte': updateTimeStart, 'UpdateTime__lt': updateTimeEnd,'MGProcess__exact':mgprocess,'BJP_FLAG__exact':BJP_FLAG,
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

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            return qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            return qs.exclude(LargeCategory__in=catelist)
        else:
            return qs


