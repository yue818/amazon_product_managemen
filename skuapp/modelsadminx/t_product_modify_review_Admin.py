# -*- coding: utf-8 -*-


from pyapp.models import b_goods as py_b_goods
from .t_product_Admin import *
from datetime import datetime as dttime
from brick.public.product_modify_show_function import product_modify_show_function
from pyapp.models import b_goods as xxxx
from pyapp.models import kc_currentstock


class t_product_modify_review_Admin(product_modify_show_function):
    search_box_flag = True
    enter_ed_classification = True

    def show_KC(self, obj):
        InputBox = obj.InputBox.replace("\r\n", "")
        rt = u"<a id=show_KC_%s>查看</a><script>$('#show_KC_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'月销售量-可用库存量',fix:false,shadeClose: true,maxmin:true,area:['500px','400px'],content:'/t_product_modify_review/modify_review_Z_KC/?KID=%s',});});</script>" % (
        obj.id, obj.id, InputBox)
        return mark_safe(rt)
    show_KC.short_description = u'月销售量-可用库存量'

    list_display = (
        'id', 'MainSKU', 'show_KC', 'show_SKU_InputBox', 'show_PIC', 'show_product', 'Select',
        'show_XGcontext', 'show_details', 'Mstatus', 'show_sq'
    )
    list_display_links = ('',)
    readonly_fields = ('id', 'SourcePicPath', 'SourcePicPath2', 'Pricerange', 'OrdersLast7Days',)

    actions = ['to_pass', 'to_notpass', 'to_recycle', 'to_excel_reduction' ]

    def to_pass(self, request, queryset):
        for querysetid in queryset.all():
            t_product_information_modify.objects.filter(id=querysetid.id).update(Mstatus="DLQ", SHTime=dttime.now(),
                                                                                 SHStaffName=request.user.first_name)
    to_pass.short_description = u"审核通过"

    def to_notpass(self, request, queryset):
        for querysetid in queryset.all():
            t_product_information_modify.objects.filter(id=querysetid.id).update(Mstatus="SHSB", SHTime=dttime.now(),
                                                                                 SHStaffName=request.user.first_name)
    to_notpass.short_description = u"审核不通过"

    def to_recycle(self, request, queryset):
        for querysetid in queryset.all():
            obj = t_product_recycle()
            obj.MainSKU = querysetid.MainSKU  # 子SKU
            obj.SKU = querysetid.SKU  # 子SKU
            obj.Name2 = querysetid.Name2  # 商品名称
            obj.NowPrice = querysetid.NowPrice
            obj.Keywords = querysetid.Keywords  # 英文关键词
            obj.Keywords2 = querysetid.Keywords2  # 中文关键词
            obj.SourcePicPath2 = querysetid.SourcePicPath2  # 供应商图
            obj.UnitPrice = querysetid.UnitPrice  # 价格
            obj.Material = querysetid.Material  # 材质
            obj.fromTDel = self.model._meta.verbose_name
            obj.id = querysetid.id
            obj.CreateTime = dttime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username
            obj.SQStaffNameing = request.user.first_name
            obj.save()
            querysetid.delete()
    to_recycle.short_description = u'扔进回收站'

    def get_list_queryset(self):
        request = self.request
        qs = super(t_product_modify_review_Admin, self).get_list_queryset()
        qs = qs.filter(Mstatus='DSH')

        flagcloth = request.GET.get('classCloth', '')

        MainSKU = request.GET.get('MainSKU', '')
        SKU = request.GET.get('SKU', '')
        Name2 = request.GET.get('Name2', '')
        KFTimeStart = request.GET.get('KFTimeStart', '')
        KFTimeEnd = request.GET.get('KFTimeEnd', '')
        Select = request.GET.get('Select', '')
        SQStaffNameing = request.GET.get('SQStaffNameing', '')
        SQTimeingStart = request.GET.get('SQTimeingStart', '')
        SQTimeingEnd = request.GET.get('SQTimeingEnd', '')

        if Select == '22':
            qs = qs.filter(CostReduction__isnull=False)
            searchList = {
                'MainSKU__exact': MainSKU, 'SKU__contains': SKU, 'Name2__exact': Name2, 'DevDate__gte': KFTimeStart,
                'DevDate__lt': KFTimeEnd, 'SQStaffNameing__exact': SQStaffNameing, 'SQTimeing__gte': SQTimeingStart,
                'SQTimeing__lt': SQTimeingEnd
            }
        else:
            if Select == '1000':
                searchList = {
                    'MainSKU__exact': MainSKU, 'SKU__contains': SKU, 'Name2__exact': Name2, 'DevDate__gte': KFTimeStart,
                    'DevDate__lt': KFTimeEnd, 'PackFlag__exact': '1', 'SQStaffNameing__exact': SQStaffNameing,
                    'SQTimeing__gte': SQTimeingStart, 'SQTimeing__lt': SQTimeingEnd
                }
            else:
                searchList = {
                    'MainSKU__exact': MainSKU, 'SKU__contains': SKU, 'Name2__exact': Name2, 'DevDate__gte': KFTimeStart,
                    'DevDate__lt': KFTimeEnd, 'Select__exact': Select, 'SQStaffNameing__exact': SQStaffNameing,
                    'SQTimeing__gte': SQTimeingStart, 'SQTimeing__lt': SQTimeingEnd
                }

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        v = 'Wish-' + v.zfill(4)
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            qs = qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            qs = qs.exclude(LargeCategory__in=catelist)

        return qs


