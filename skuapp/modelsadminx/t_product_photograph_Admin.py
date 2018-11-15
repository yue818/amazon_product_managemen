# -*- coding: utf-8 -*-
from .t_product_Admin import *
from pyapp.models import b_goods as py_b_goods
from skuapp.table.t_product_enter_ed import t_product_enter_ed
from skuapp.table.t_product_depart_get import t_product_depart_get
from skuapp.table.t_product_oplog import t_product_oplog
from datetime import datetime
from brick.function.formatUrl import format_urls
from django.forms.models import model_to_dict

from skuapp.table.t_product_art_pre_ed import t_product_art_pre_ed
from skuapp.table.t_product_art_ed import t_product_art_ed
from skuapp.table.t_product_enter_ed import t_product_enter_ed
from skuapp.table.t_product_enter_ing import t_product_enter_ing

class t_product_photograph_Admin(t_product_Admin):
    search_box_flag = True
    enter_ed_classification = True
    repeat_sku = True

    actions = ['to_alreadly', 'to_recycle']

    def to_alreadly(self, request, objs):
        objs.update(SampleState='alreadly',Entertime=datetime.now())

    # objs.update(SampleState='notyet')
    to_alreadly.short_description = u'已有样品'

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
                
        super(t_product_photograph_Admin, self).to_recycle(request, queryset)
                 

    to_recycle.short_description = u'扔进回收站'

    def show_skuattrs(self, obj):
        rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU-</th><th style="text-align:center">属性</th></tr>'
        if obj.PZRemake == '1':
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.pid,
                                                                              MainSKU=obj.MainSKU).order_by('SKU')
            for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
                rt = '%s <tr><td>%s</td><td>%s</td></tr> ' % (
                rt, t_product_mainsku_sku_obj.SKU, t_product_mainsku_sku_obj.SKUATTRS)

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
    #
    # show_urls.short_description = u'链接信息'
    
    def show_messages1(self,obj) :
        rt = u'拍照申请人:%s <br> 拍照申请时间:%s <br>拍照员:%s <br>拍照时间:%s'%(obj.PZStaffNameing,obj.PZTimeing,obj.PZStaffName,obj.PZTime)
        return mark_safe(rt)
    show_messages1.short_description = u'拍照信息'
    
    
    def show_messages2(self,obj) :
        rt = u'业绩归属人2:%s <br>采购员:%s<br>建资料员:%s <br> 建资料时间:%s'%(obj.YJGS2StaffName,obj.Buyer,obj.JZLStaffName,obj.JZLTime)
        return mark_safe(rt)
    show_messages2.short_description = u'业绩/采购/建资料信息'
    
    def show_messages3(self,obj) :
        rt = u'商品名:%s <br> 英文标题:%s'%(obj.Name2,obj.Keywords)
        return mark_safe(rt)
    show_messages3.short_description = u'商品信息'
    
        

    def show_oplog(self, obj):
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.pid, MainSKU=obj.MainSKU).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,' % (rt, t_product_oplog_obj.StepName, t_product_oplog_obj.OpName)
        return rt

    show_oplog.short_description = u'-----------操作历史-----------'

    list_display = ('pid', 'MainSKU', 'show_skuattrs', 'PZRemake', 'SampleState', 'show_Request', 'LargeCategory',
                    'MGProcess', 'PPosition', 'show_messages1', 'show_messages2',
                    'show_SourcePicPath', 'show_messages3', 'show_SourcePicPath2','SalesApplicant','Entertime',
                    'show_urls', 'show_oplog')
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
                       # 'Electrification','Powder','Liquid','Magnetism',  #u'违禁品',
                       'ContrabandAttribute',
                       'Remark',  # 备注
                       'DYTime', 'DYStaffName', 'DYSHTime', 'DYSHStaffName', 'XJTime', 'XJStaffName', 'KFTime',
                       'KFStaffName', 'JZLTime', 'JZLStaffName',
                       'PZTime', 'PZStaffName', 'MGTime', 'MGStaffName', 'LRTime', 'LRStaffName',
                       'PZTimeing', 'PZStaffNameing',)
    # list_editable = ('SampleState',)
    # 分组表单
    fields = ('MainSKU', 'PPosition',
              'PictureRequest',
              'PZTimeing', 'PZStaffNameing',
              'PZTime', 'PZStaffName', 'SampleState'
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

    # def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        mid = obj.id
        ramkes = obj.PictureRequest
        SampleState = obj.SampleState
        old_obj = None
        if obj is None or obj.id is None or obj.id <= 0:
            t_product_Admin_obj = t_product_Admin()
            mid = t_product_Admin_obj.get_id()
        else:
            old_obj = self.model.objects.get(pk=obj.pk)
        obj.id = mid
        PPosition = obj.PPosition
        obj.save()

        t_product_enter_ed_objs = t_product_enter_ed.objects.filter(MainSKU=obj.MainSKU)
        b_goods_objs = py_b_goods.objects.values('SKU', 'GoodsName', 'NID', 'SalerName2', 'CategoryCode').filter(
            SKU__startswith=obj.MainSKU)

        if t_product_enter_ed_objs.exists():
            obj.__dict__ = t_product_enter_ed_objs[0].__dict__
            obj.SalesApplicant=None
            obj.Entertime=datetime.now()

            obj.YNphoto = '0'
            obj.PictureRequest = u'%s; <br> %s' % (ramkes, t_product_enter_ed_objs[0].PictureRequest)
            obj.MGProcess = '0'  # 等待拍照
            obj.PZTimeing = datetime.now()
            obj.PZStaffNameing = request.user.first_name
            obj.StaffID = request.user.username
            obj.pid = t_product_enter_ed_objs[0].id
            obj.PZRemake = '1'

            # t_product_enter_ed.objects.filter(id=obj.pid).update(YNphoto='0', MGProcess='0', MGTime=None)
            # t_product_depart_get.objects.filter(pid=obj.pid).update(YNphoto='0', MGProcess='0', MGTime=None)

        elif b_goods_objs.exists():
            obj.PictureRequest = ramkes
            obj.Name2 = b_goods_objs[0]['GoodsName']
            obj.pid = b_goods_objs[0]['NID']

            for b_goods_obj in b_goods_objs:
                if b_goods_obj is not None and b_goods_obj['SalerName2'].strip() != '':
                    user = User.objects.filter(first_name=b_goods_obj['SalerName2']).first()
                    if user is not None:
                        username = user.username
                        obj.YJGS2StaffName = username
                        break

            obj.YNphoto = '0'
            obj.MGProcess = '0'  # 等待拍照
            obj.PZTimeing = datetime.now()
            obj.PZStaffNameing = request.user.first_name
            obj.StaffID = request.user.username
            obj.PZRemake = '0'

            CategoryName = ''
            from django.db import connections
            if connections:
                cursor = connections['syn'].cursor()
                CategorySql = "select CategoryName from b_goodscats b where b.CategoryCode='%s'" % b_goods_objs[0][
                    'CategoryCode']
                cursor.execute(CategorySql)
                CategoryNameTmp = cursor.fetchone()
                if CategoryNameTmp:
                    CategoryName = CategoryNameTmp[0].encode("utf-8")
                if cursor:
                    cursor.close()
            obj.LargeCategory = CategoryName

        else:
            obj.PictureRequest = ramkes
            messages.error(request, "错误:此SKU不存在！")
            obj.MGProcess = '4'

        obj.PPosition = PPosition
        obj.PZStaffName = None
        obj.PZTime = None
        obj.SampleState = SampleState
        obj.id = mid
        obj.save()

        t_product_oplog.objects.create(pid=mid, MainSKU=obj.MainSKU,
                                       Name=obj.Name, Name2=obj.Name2, OpID=request.user.username,
                                       OpName=request.user.first_name,
                                       StepID=u'ZJSP', StepName='增加实拍', BeginTime=datetime.now())

    def get_list_queryset(self, ):
        from django.db.models import Q
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        request = self.request
        qs = super(t_product_photograph_Admin, self).get_list_queryset()

        PPosition = request.GET.get('PPosition', '')  # 拍照位置
        # Electrification = request.GET.get('Electrification','')     # 是否带电
        # Powder          = request.GET.get('Powder','')              # 是否粉末
        # Liquid          = request.GET.get('Liquid','')              # 是否液体
        # Magnetism       = request.GET.get('Magnetism','')           # 是否带磁
        ContrabandAttribute = request.GET.get('ContrabandAttribute', '')
        Storehouse = request.GET.get('Storehouse', '')  # 发货仓库
        LargeCategory = request.GET.get('LargeCategory', '')  # 大类名称
        MGProcess = request.GET.get('MGProcess', '')  # 图片状态 0待实拍 1待制作 2完成实拍 3完成制作 4错误
        MainSKU = request.GET.get('MainSKU', '')  # 主SKU
        flagcloth = request.GET.get('classCloth', '')

        Buyer = request.GET.get('Buyer', '')  # 采购员
        PZStaffNameing = request.GET.get('PZStaffNameing', '')  # 拍照申请人
        PZStaffName = request.GET.get('PZStaffName', '')  # 拍照员
        PictureRequest = request.GET.get('PictureRequest', '')  # 图片要求

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

        qs = qs.filter(Q(SampleState='notyet') | Q(SampleState__isnull=True))

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            qs = qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            qs = qs.exclude(LargeCategory__in=catelist)

        # 加管理员可见
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=request.user.username,
                                                   urltable="t_product_photograph").count()
        except:
            pass
        if request.user.is_superuser or flag != 0:
            return qs
        qs = qs.filter(Q(PZStaffNameing=request.user.first_name) | Q(YJGS2StaffName=request.user.username) | Q(
            YJGS2StaffName__isnull=True, Buyer=request.user.first_name) | Q(YJGS2StaffName='',
                                                                            Buyer=request.user.first_name))
        return qs
