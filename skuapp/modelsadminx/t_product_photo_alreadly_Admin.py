# -*- coding: utf-8 -*-
from .t_product_Admin import *
from pyapp.models import b_goods as py_b_goods
from skuapp.table.t_product_enter_ed import t_product_enter_ed
from skuapp.table.t_product_depart_get import t_product_depart_get
from skuapp.table.t_product_oplog import t_product_oplog
from datetime import datetime
from brick.function.formatUrl import format_urls
class t_product_photo_alreadly_Admin(t_product_Admin):
    enter_ed_classification = True
    search_box_flag = True
    repeat_sku = True
    sku_count = True

    actions = ['to_receive']
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



    def to_receive(self, request, objs):
        from skuapp.table.t_product_photo_ing import t_product_photo_ing
        for querysetid in objs:
            t_product_photo_ing_obj = t_product_photo_ing()
            t_product_photo_ing_obj.__dict__ = querysetid.__dict__
            t_product_photo_ing_obj.PZStaffName = request.user.first_name
            t_product_photo_ing_obj.Entertime=datetime.now()
            t_product_photo_ing_obj.save()

            t_product_oplog.objects.create(pid=querysetid.pid, MainSKU=querysetid.MainSKU,
                                           Name=querysetid.Name, Name2=querysetid.Name2, OpID=request.user.username,
                                           OpName=request.user.first_name,
                                           StepID=u'LQSP', StepName='领取拍照', BeginTime=datetime.now())

            querysetid.delete()

    to_receive.short_description = u'领取拍照'

    def show_skuattrs(self, obj):
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU-</th><th style="text-align:center">属性</th></tr>'
        if obj.PZRemake == '1':
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=obj.MainSKU).order_by(
                'ProductSKU')
            for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
                rt = '%s <tr><td>%s</td><td>%s</td></tr> ' % (
                rt, t_product_mainsku_sku_obj.ProductSKU, t_product_mainsku_sku_obj.SKUATTRS)

        elif obj.PZRemake == '0':
            b_goods_objs = py_b_goods.objects.values('SKU', 'GoodsName').filter(SKU__startswith=obj.MainSKU)
            for b_goods_obj in b_goods_objs:
                rt = '%s <tr><td>%s</td><td>%s</td></tr> ' % (rt, b_goods_obj['SKU'], b_goods_obj['GoodsName'])

        rt = '%s</table>' % rt
        return mark_safe(rt)

    show_skuattrs.short_description = mark_safe('<p align="center"> 子SKU</p>')

    def show_Request(self, obj):
        piclist = list((u'%s' % (obj.PictureRequest,)).replace('<br>', ''))
        num = 0
        while True:
            num = num + 32
            if num >= len(piclist):
                break
            piclist.insert(num, '<br>')
        return mark_safe(''.join(piclist))

    show_Request.short_description = u'图片要求备注'
    
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
    
    def show_messages1(self,obj) :
        rt = u'拍照申请人:%s <br> 拍照申请时间:%s <br>拍照员:%s <br>拍照时间:%s'%(obj.PZStaffNameing,obj.PZTimeing,obj.PZStaffName,obj.PZTime)
        return mark_safe(rt)
    show_messages1.short_description = u'拍照信息'

    def show_messages2(self, obj):
        rt = u'业绩归属人2:%s <br>采购员:%s<br>建资料员:%s <br> 建资料时间:%s' % (obj.YJGS2StaffName, obj.Buyer, obj.JZLStaffName, obj.JZLTime)
        return mark_safe(rt)
    show_messages2.short_description = u'业绩/采购/建资料信息'

    def show_messages3(self, obj):
        rt = u'商品名:%s <br> 英文标题:%s' % (obj.Name2, obj.Keywords)
        return mark_safe(rt)
    show_messages3.short_description = u'商品信息'

    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.pid, MainSKU=obj.MainSKU).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,' % (rt, t_product_oplog_obj.StepName, t_product_oplog_obj.OpName)
        return rt

    show_oplog.short_description = u'-----------操作历史-----------'
    
    list_display= ('pid','MainSKU','show_skuattrs','PZRemake','SampleState','show_Request','LargeCategory',
                   'MGProcess','PPosition','show_messages1','show_messages2',
                   'show_SourcePicPath','show_messages3','show_SourcePicPath2',
                   'SalesApplicant','Entertime','show_urls','show_oplog',)
    list_filter = ('UpdateTime',
                   'Weight',
                   # 'Electrification','Powder','Liquid','Magnetism','Buyer',
                   'ContrabandAttribute', 'Buyer',
                   'Storehouse',
                   'PZStaffNameing', 'PZStaffName', 'MGProcess', 'LargeCategory',
                   'PPosition',
                   'PictureRequest',
                   )
    readonly_fields = ('pid', 'SourceURL', 'OrdersLast7Days', 'Keywords', 'Keywords2', 'SpecialRemark',
                       'Pricerange', 'ShelveDay', 'Name', 'Tags',  # u'调研结果',
                       'SupplierPUrl1', 'SupplierPDes', 'SupplierID',  # u'开发结果',
                       'UnitPrice', 'Weight', 'SpecialSell',  # u'询价结果',
                       'Name2', 'Material', 'Unit', 'MinOrder', 'SupplierArtNO',
                       'SupplierPColor', 'SupplierPUrl2', 'OrderDays', 'StockAlarmDays', 'LWH',
                       'SupplierContact', 'Storehouse', 'ReportName', 'ReportName2', 'MinPackNum',  # 建资料
                       'ContrabandAttribute',  # 'Electrification','Powder','Liquid','Magnetism',  #u'违禁品',
                       'Remark',  # 备注
                       'DYTime', 'DYStaffName', 'DYSHTime', 'DYSHStaffName', 'XJTime', 'XJStaffName', 'KFTime',
                       'KFStaffName', 'JZLTime', 'JZLStaffName',
                       'PZTime', 'PZStaffName', 'MGTime', 'MGStaffName', 'LRTime', 'LRStaffName',
                       'PZTimeing', 'PZStaffNameing',)
    list_editable = ('SampleState',)
    list_display_links = ('',)
    # 分组表单
    fields = ('MainSKU', 'PPosition',
              'PictureRequest',
              'PZTimeing', 'PZStaffNameing',
              'PZTime', 'PZStaffName', 'SampleState',
              )

    form_layout = (
        Fieldset(u'拍照信息',
                 Row('MainSKU', 'SampleState', 'PPosition', ),
                 Row('PictureRequest', ),
                 Row('PZTimeing', 'PZStaffNameing', ),
                 Row('PZTime', 'PZStaffName', ),
                 css_class='unsort '
                 )
    )
    show_detail_fields = ['id']

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_product_photo_alreadly_Admin, self).get_list_queryset()

        PPosition = request.GET.get('PPosition', '')  # 拍照位置
        # Electrification = request.GET.get('Electrification','')     # 是否带电
        # Powder          = request.GET.get('Powder','')              # 是否粉末
        # Liquid          = request.GET.get('Liquid','')              # 是否液体
        # Magnetism       = request.GET.get('Magnetism','')           # 是否带磁
        ContrabandAttribute = request.GET.get('ContrabandAttribute', '')  # 商品属性
        Storehouse = request.GET.get('Storehouse', '')  # 发货仓库
        LargeCategory = request.GET.get('LargeCategory', '')  # 大类名称
        MGProcess = request.GET.get('MGProcess', '')  # 图片状态 0待实拍 1待制作 2完成实拍 3完成制作 4错误
        MainSKU = request.GET.get('MainSKU', '')  # 主SKU

        Buyer = request.GET.get('Buyer', '')  # 采购员
        PZStaffNameing = request.GET.get('PZStaffNameing', '')  # 拍照申请人
        PZStaffName = request.GET.get('PZStaffName', '')  # 拍照员
        PictureRequest = request.GET.get('PictureRequest', '')  # 图片要求
        flagcloth = request.GET.get('classCloth', '')

        WeightStart = request.GET.get('WeightStart', '')  # 克重
        WeightEnd = request.GET.get('WeightEnd', '')

        updateTimeStart = request.GET.get('updateTimeStart', '')  # 更新时间
        updateTimeEnd = request.GET.get('updateTimeEnd', '')
        BJP_FLAG        = request.GET.get('BJP_FLAG','')

        searchList = {'MainSKU__exact': MainSKU, 'ContrabandAttribute__exact': ContrabandAttribute,
                      'Storehouse__exact': Storehouse, 'LargeCategory__exact': LargeCategory,
                      'PPosition__exact': PPosition, 'Buyer__exact': Buyer, 'PZStaffNameing__exact': PZStaffNameing,
                      'PictureRequest__contains': PictureRequest,
                      'PZStaffName__exact': PZStaffName, 'MGProcess__exact': MGProcess,
                      'Weight__gte': WeightStart, 'Weight__lt': WeightEnd,
                      'UpdateTime__gte': updateTimeStart, 'UpdateTime__lt': updateTimeEnd,'BJP_FLAG__exact':BJP_FLAG,
                      }

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    # v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        qs = qs.filter(SampleState='alreadly')

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            return qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            return qs.exclude(LargeCategory__in=catelist)
        else:
            return qs
