# -*- coding: utf-8 -*-
from .t_product_Admin import *
from pyapp.models import b_goods as py_b_goods
from skuapp.table.t_product_enter_ed import t_product_enter_ed
from skuapp.table.t_product_depart_get import t_product_depart_get
from skuapp.table.t_product_oplog import t_product_oplog
from datetime import datetime
from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
from brick.function.formatUrl import format_urls

class t_product_saler_requirement_photograph_Admin(t_product_Admin):
    search_box_flag = True
    enter_ed_classification = True
    repeat_sku =True




    actions = ['to_receive']

    def to_receive(self, request, objs):
        from skuapp.table.t_product_photograph import t_product_photograph
        for querysetid in objs:
            t_product_photograph_obj = t_product_photograph()
            t_product_photograph_obj.__dict__ = querysetid.__dict__
            #t_product_photo_ing_obj.PZStaffName = request.user.first_name
            t_product_photograph_obj.SampleState = 'notyet'
            t_product_photograph_obj.SalesApplicant=querysetid.PZStaffNameing
            t_product_photograph_obj.Entertime=datetime.now()

            t_product_photograph_obj.save()

            t_product_oplog.objects.create(pid=querysetid.id, MainSKU=querysetid.MainSKU,
                                           Name=querysetid.Name, Name2=querysetid.Name2, OpID=request.user.username,
                                           OpName=request.user.first_name,
                                           StepID=u'LQXQ', StepName='领取实拍需求', BeginTime=datetime.now())
            # querysetid.LQTimeing = datetime.now()
            # querysetid.LQStaffNameing = request.user.first_name
            # querysetid.LQState = 'y'
            # querysetid.SampleState = '未取样'
            # querysetid.save()
            querysetid.delete()
            messages.success(request, u'%s领取成功！' %querysetid.MainSKU)

    to_receive.short_description = u'领取实拍需求'

    def show_skuattrs(self, obj):
        try:
            rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU-</th><th style="text-align:center">属性</th></tr>'
            if obj.PZRemake == '1':
                from skuapp.table.t_combination_sku_log import t_combination_sku_log
                t_combination_sku_log_objs = t_combination_sku_log.objects.filter(Com_SKU=obj.MainSKU).values_list('Pro_SKU', flat=True)
                if t_combination_sku_log_objs.exists():
                    strSKU = t_combination_sku_log_objs[0]
                    subSkuList = strSKU.split('+')
                    for objSubSkuList in subSkuList:
                        t_product_mainsku_sku_objs1 = t_product_mainsku_sku.objects.filter(SKU=objSubSkuList)
                        if t_product_mainsku_sku_objs1.exists():
                            rt = '%s <tr><td>%s</td><td>%s</td></tr> ' % (
                                rt, t_product_mainsku_sku_objs1[0].SKU, t_product_mainsku_sku_objs1[0].SKUATTRS)
                else:
                    t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=obj.pid,
                                                                                      MainSKU=obj.MainSKU).order_by('SKU')
                    for t_product_mainsku_sku_obj in t_product_mainsku_sku_objs:
                        rt = '%s <tr><td>%s</td><td>%s</td></tr> ' % (
                        rt, t_product_mainsku_sku_obj.SKU, t_product_mainsku_sku_obj.SKUATTRS)

            elif obj.PZRemake == '0':
                #b_goods_objs = py_b_goods.objects.values('SKU', 'GoodsName').filter(SKU__startswith=obj.MainSKU)

                #mdf by wangzy 20180510
                subSkuList = []
                from skuapp.table.t_combination_sku_log import t_combination_sku_log
                t_combination_sku_log_objs = t_combination_sku_log.objects.filter(Com_SKU=obj.MainSKU).values_list(
                    'Pro_SKU', flat=True)
                if t_combination_sku_log_objs.exists():
                    strSKU = t_combination_sku_log_objs[0]
                    subSkuList = strSKU.split('+')
                else:
                    t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=obj.MainSKU)
                    for t_product_mainsku_sku_objs_row in t_product_mainsku_sku_objs:
                        subSkuList.append(t_product_mainsku_sku_objs_row.ProductSKU)
                b_goods_objs = py_b_goods.objects.values('SKU', 'GoodsName').filter(SKU__in=subSkuList)

                for b_goods_obj in b_goods_objs:
                    rt = '%s <tr><td>%s</td><td>%s</td></tr> ' % (rt, b_goods_obj['SKU'], b_goods_obj['GoodsName'])

            rt = '%s</table>' % rt
        except Exception,e:
            rt = '<table  style="text-align:center"><tr><th style="text-align:center">子SKU-</th><th style="text-align:center">属性</th></tr>'
            messages.error(self.request,'error---%s,strMain=%s'%(str(e),obj.MainSKU))
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
    #
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

    def show_oplog(self, obj):
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id, MainSKU=obj.MainSKU).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,' % (rt, t_product_oplog_obj.StepName, t_product_oplog_obj.OpName)
        return rt

    show_oplog.short_description = u'-----------操作历史-----------'
    
    
        
    def show_messages1(self,obj) :
        rt = u'拍照申请时间:%s <br>拍照员:%s <br>拍照时间:%s'%(obj.PZTimeing,obj.PZStaffName,obj.PZTime)
        return mark_safe(rt)
    show_messages1.short_description = u'信息1'
    
    def show_messages2(self,obj):
        rt = u'领取人:%s <br>领取时间:%s <br> 销售申请人:%s <br>业绩归属人2:%s <br>采购员:%s'%(obj.LQStaffNameing,obj.LQTimeing,obj.PZStaffNameing,obj.YJGS2StaffName,obj.Buyer)
        return mark_safe(rt)
    show_messages2.short_description = u'信息2'
    
    def CmpAndMainSKU(self,obj):
        from skuapp.table.t_combination_sku_log import t_combination_sku_log
        t_combination_sku_log_objs = t_combination_sku_log.objects.filter(Com_SKU=obj.MainSKU)
        rt = ''
        if t_combination_sku_log_objs.exists():
            rt = '<div class="box" style="width: 137px;height: 170px;background-color: #A6FFA6;text-align: center;line-height: 30px;border-radius: 4px">%s<br>组合SKU</div>' % (
                obj.MainSKU)
        else:
            rt = '<div class="box" style="width: 137px;height: 170px;background-color: #FFF4C1;text-align: center;line-height: 30px;border-radius: 4px">%s<br>主SKU</div>' % (
                obj.MainSKU)
        return mark_safe(rt)
    CmpAndMainSKU.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">主/组合SKU</p>')

    list_display = ('pid', 'CmpAndMainSKU', 'show_skuattrs', 'PZRemake', 'SampleState', 'show_Request',
                    'MGProcess', 'PPosition','LargeCategory','show_messages1', 'show_messages2',
                    'show_SourcePicPath', 'Name2', 'Keywords', 'JZLTime',#'JZLStaffName',
                    'show_SourcePicPath2','show_urls', 'show_oplog',)
    list_filter = ('UpdateTime',
                   'Weight',
                   # 'Electrification','Powder','Liquid','Magnetism','Buyer',
                   'ContrabandAttribute', 'Buyer',
                   'Storehouse',
                   'PZStaffNameing', 'PZStaffName', 'MGProcess', 'LargeCategory',
                   'PPosition',
                   'PictureRequest',
				   'LQTimeing',
				   'LQStaffNameing',
				   'LQState','YJGS2StaffName','Buyer'
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
                       'PZTimeing', 'PZStaffNameing','SampleState','YJGS2StaffName')
    # list_editable = ('SampleState',)
    # 分组表单
    fields = ('MainSKU', 'PPosition',
              'PictureRequest',
              'PZTimeing', 'PZStaffNameing',
              'PZTime', 'PZStaffName', 'SampleState','SelectWays'
              )

    form_layout = (
        Fieldset(u'拍照信息',
                 Row('MainSKU', 'SelectWays','PPosition', ),
                 Row('PictureRequest', ),
                 Row('PZTimeing', 'PZStaffNameing', ),
                 Row('PZTime', 'PZStaffName', ),
                 css_class='unsort '
                 )
    )
    show_detail_fields = ['id']

    # def save_model(self, request, obj, form, change):
    def save_models(self):
        try:
            obj = self.new_obj
            request = self.request
            mid = obj.id
            ramkes = obj.PictureRequest
            #SampleState = obj.SampleState
            old_obj = None
            ways = obj.SelectWays

            if obj is None or obj.id is None or obj.id <= 0:
                t_product_Admin_obj = t_product_Admin()
                mid = t_product_Admin_obj.get_id()
            else:
                old_obj = self.model.objects.get(pk=obj.pk)
            obj.id = mid
            PPosition = obj.PPosition
            obj.save()

            t_product_enter_ed_objs = t_product_enter_ed.objects.filter(MainSKU=obj.MainSKU)
            # mdf by wangzy begin
            if ways == 'n':
                b_goods_objs = py_b_goods.objects.values('SKU', 'GoodsName', 'NID', 'SalerName2', 'Purchaser','CategoryCode').filter(SKU__startswith=obj.MainSKU)
            else:
                subSkuList = []
                t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(MainSKU=obj.MainSKU)
                from skuapp.table.t_combination_sku_log import t_combination_sku_log
                t_combination_sku_log_objs = t_combination_sku_log.objects.filter(Com_SKU=obj.MainSKU).values_list('Pro_SKU',flat=True)
                if t_combination_sku_log_objs.exists():
                    strSKU = t_combination_sku_log_objs[0]
                    subSkuList = strSKU.split('+')
                else:
                    for t_product_mainsku_sku_objs_row in t_product_mainsku_sku_objs:
                        subSkuList.append(t_product_mainsku_sku_objs_row.ProductSKU)
                b_goods_objs = py_b_goods.objects.values('SKU', 'GoodsName', 'NID', 'SalerName2', 'Purchaser',
                                                         'CategoryCode').filter(SKU__in=subSkuList)
            #end

            # s = True
            if t_product_enter_ed_objs.exists():
                # messages.success(request, '从已完成拍摄表中找到')
                obj.__dict__ = t_product_enter_ed_objs[0].__dict__
                obj.YNphoto = '0'
                obj.PictureRequest = u'%s; <br> %s' % (ramkes, t_product_enter_ed_objs[0].PictureRequest)
                obj.MGProcess = '0'  # 等待拍照
                obj.PZTimeing = datetime.now()
                obj.PZStaffNameing = request.user.first_name
                obj.StaffID = request.user.username
                obj.pid = t_product_enter_ed_objs[0].id
                obj.PZRemake = '1'
                if b_goods_objs.exists():
                    for b_goods_obj in b_goods_objs:
                        if b_goods_obj is not None and b_goods_obj['SalerName2'].strip() != '':
                            user = User.objects.filter(first_name=b_goods_obj['SalerName2']).first()
                            if user is not None:
                                username = user.username
                                obj.YJGS2StaffName = username
                                # break
                        if b_goods_obj is not None and b_goods_obj['Purchaser'].strip() != '':
                            user = User.objects.filter(first_name=b_goods_obj['Purchaser']).first()
                            if user is not None:
                                obj.Buyer = user.first_name
                else:
                    obj.YJGS2StaffName = t_product_enter_ed_objs[0].YJGS2StaffName
                    obj.Buyer = t_product_enter_ed_objs[0].Buyer
                # t_product_enter_ed.objects.filter(id=obj.pid).update(YNphoto='0', MGProcess='0', MGTime=None)
                # t_product_depart_get.objects.filter(pid=obj.pid).update(YNphoto='0', MGProcess='0', MGTime=None)

            elif b_goods_objs.exists():
                # messages.success(request, '从py_b_goods表中找到')
                obj.PictureRequest = ramkes
                obj.Name2 = b_goods_objs[0]['GoodsName']
                obj.pid = b_goods_objs[0]['NID']

                for b_goods_obj in b_goods_objs:
                    if b_goods_obj is not None and b_goods_obj['SalerName2'].strip() !='':
                        user = User.objects.filter(first_name=b_goods_obj['SalerName2']).first()
                        if user is not None:
                            username = user.username
                            obj.YJGS2StaffName = username
                            # break
                    if b_goods_obj is not None and b_goods_obj['Purchaser'].strip() != '':
                        user = User.objects.filter(first_name=b_goods_obj['Purchaser']).first()
                        if user is not None:
                            obj.Buyer = user.first_name

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
                    CategorySql = "select CategoryName from b_goodscats b where b.CategoryCode='%s'" % b_goods_objs[0]['CategoryCode']
                    cursor.execute(CategorySql)
                    CategoryNameTmp = cursor.fetchone()
                    if CategoryNameTmp:
                        CategoryName = CategoryNameTmp[0].encode("utf-8")
                    if cursor:
                        cursor.close()
                obj.LargeCategory = CategoryName

                #obj.YJGS2StaffName = b_goods_objs[0]['SalerName2']
                # for b_goods in b_goods_objs:
                #     if b_goods['SalerName2'] is not None or b_goods['SalerName2'].strip() != '':
                #         messages.success(request, '非空'+b_goods['SalerName2'].strip())
                #         print('************'+b_goods['SalerName2'].strip()+'&\n&\n&\n&\n&\n&\n&\n&\n&\n&&&&&&&&&&&&&&&&&&&&&&&&&')
                #     else:
                #         messages.success(request, '空')
            else:
                obj.PictureRequest = ramkes
                messages.error(request, "错误:此SKU不存在！")
                obj.MGProcess = '4'
                obj.PZStaffNameing=request.user.first_name
            obj.PPosition = PPosition
            obj.PZStaffName = None
            obj.PZTime = None
            obj.SampleState = '未取样'
            obj.id = mid
            obj.LQTimeing = None
            obj.LQStaffNameing = None
            obj.LQState = 'n'
            obj.SelectWays = ways
            obj.save()
            t_product_oplog.objects.create(pid=mid, MainSKU=obj.MainSKU,
                                           Name=obj.Name, Name2=obj.Name2, OpID=request.user.username,
                                           OpName=request.user.first_name,
                                           StepID=u'ZJSP', StepName='增加实拍需求', BeginTime=datetime.now())
        except Exception,e:
            messages.error(self.request,'error---%s,strMain=%s'%(str(e),obj.MainSKU))

    def get_list_queryset(self, ):
        from django.db.models import Q
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        request = self.request
        qs = super(t_product_saler_requirement_photograph_Admin, self).get_list_queryset()

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

        searchList = {'MainSKU__exact': MainSKU, 'ContrabandAttribute__exact': ContrabandAttribute,
                      'Storehouse__exact': Storehouse, 'LargeCategory__exact': LargeCategory,
                      'PPosition__exact': PPosition, 'Buyer__exact': Buyer, 'PZStaffNameing__exact': PZStaffNameing,
                      'PictureRequest__contains': PictureRequest,
                      'PZStaffName__exact': PZStaffName, 'MGProcess__exact': MGProcess,
                      'Weight__gte': WeightStart, 'Weight__lt': WeightEnd,
                      'UpdateTime__gte': updateTimeStart, 'UpdateTime__lt': updateTimeEnd,
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

        #qs = qs.filter(Q(SampleState='notyet') | Q(SampleState__isnull=True))

        # qs = qs.filter(Q(PZStaffNameing = request.user.first_name) | Q(Buyer = request.user.first_name) | Q(YJGS2StaffName = request.user.first_name))

        if flagcloth == '1':
            qs = qs.filter(
                Q(LargeCategory=u'001.时尚女装') | Q(LargeCategory=u'002.时尚男装') | Q(MainSKU__istartswith='SW') | Q(
                    MainSKU__istartswith='K')).exclude(
                Q(MainSKU__istartswith='KEY') | Q(MainSKU__istartswith='KN') | Q(MainSKU__istartswith='key'))
        elif flagcloth == '2':
            qs = qs.exclude(
                Q(LargeCategory=u'001.时尚女装') | Q(LargeCategory=u'002.时尚男装') | Q(MainSKU__istartswith='SW') | Q(
                    MainSKU__istartswith='K1') | Q(MainSKU__istartswith='K2'))

        # current_group_set = list()
        # try:
        #     current_user = request.user
        #     current_group_set = Group.objects.filter(user=current_user).all()
        #     print current_group_set
        # except Exception, e:
        #     messages.error(request, e)
        #     pass
        # xs = Group.objects.get(name='销售组')
        # # cg = Group.objects.get(name='采购组')
        # if xs in current_group_set:
        #     qs = qs.filter(Q(PZStaffNameing=request.user.first_name))
        #     messages.success(request, '在销售组里面')
        #     return qs
        # elif cg in current_group_set:
        #     qs = qs.filter(Q(Buyer=request.user.first_name))
        #     messages.success(request, '在采购组里面')
        # else:
            # qs1 = qs.filter(Q(YJGS2StaffName__isnull = False)).filter(Q(YJGS2StaffName = request.user.first_name))
            # qs2 = qs.filter(Q(YJGS2StaffName__isnull=True)).filter(Q(Buyer=request.user.first_name))
            # qs = []
            # qs.extend(qs1)
            # qs.extend(qs2)
        # 超级管理员可见
        #debug = False  #管理员是否全部可见 False：是/True：否 （只显示跟自己相关的
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=request.user.username,urltable="t_product_saler_requirement_photograph").count()
        except:
            pass
        if request.user.is_superuser or flag != 0:
            return qs
        qs = qs.filter(Q(PZStaffNameing=request.user.first_name) | Q(YJGS2StaffName=request.user.username) | Q(YJGS2StaffName__isnull=True , Buyer=request.user.first_name) | Q(YJGS2StaffName='' , Buyer=request.user.first_name))
        return qs