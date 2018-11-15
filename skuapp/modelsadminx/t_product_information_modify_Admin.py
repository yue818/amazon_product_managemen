# -*- coding: utf-8 -*-


from .t_product_Admin import *
from django.db.models import Q
from datetime import datetime
from brick.public.product_modify_show_function import product_modify_show_function


class t_product_information_modify_Admin(product_modify_show_function):
    search_box_flag = True
    downloadxls = True
    show_sku = True
    enter_ed_classification = True

    list_display = (
        'id', 'MainSKU', 'show_SKU_InputBox', 'show_PIC', 'show_product', 'Select',
        'show_XGcontext', 'show_details', 'Mstatus', 'show_sq', 'show_sh', 'remarks', 'BHRemark'
    )
    list_display_links = ('',)
    fields = ('MainSKU',)
    form_layout = (
        Fieldset(u'请输入商品SKU',
                 Row('MainSKU', ),
                 css_class='unsort'
                 )
    )

    actions = ['to_recycle', 'to_modify', 'to_excel', 'to_excel_new', 'to_excel_reduction']

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
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username
            obj.SQStaffNameing = request.user.first_name
            obj.save()

            # end_t_product_oplog(request,querysetid.MainSKU,'DEL',querysetid.Name2,querysetid.id)
            querysetid.delete()
    to_recycle.short_description = u'扔进回收站'

    def to_modify(self, request, queryset):
        for querysetid in queryset.all():
            if querysetid.Mstatus == 'DLQ':
                if request.user.has_perm('skuapp.change_t_product_information_modify'):
                    t_product_information_modify.objects.filter(id=querysetid.id).update(Mstatus='DXG',
                                                                                         LQTime=datetime.now(),
                                                                                         LQStaffName=request.user.first_name)
                else:
                    messages.error(request, '对不起！您没有领取的权限！ ID：%s' % querysetid.id)
            elif querysetid.Mstatus == 'DXG':
                messages.error(request, '对不起！信息组已领取！ ID：%s' % querysetid.id)
            elif querysetid.Mstatus == 'DSH':
                messages.error(request, '对不起！该记录还未审核！ ID：%s' % querysetid.id)
            elif querysetid.Mstatus == 'SHSB':
                messages.error(request, '对不起！该记录未通过审核！ ID：%s' % querysetid.id)
    to_modify.short_description = u'领去修改(信息组操作)'

    def get_list_queryset(self):
        request = self.request
        qs = super(t_product_information_modify_Admin, self).get_list_queryset()
        qs = qs.filter(Q(Mstatus='DLQ') | Q(Mstatus='BBH') | Q(Mstatus='DHT') | Q(Mstatus='SHSB'))

        flagcloth = request.GET.get('classCloth', '')

        MainSKU = request.GET.get('MainSKU', '')
        SKU = request.GET.get('SKU', '')
        Name2 = request.GET.get('Name2', '')
        KFTimeStart = request.GET.get('KFTimeStart', '')
        KFTimeEnd = request.GET.get('KFTimeEnd', '')
        Select = request.GET.get('Select', '')
        Mstatus = request.GET.get('Mstatus', '')
        SQStaffNameing = request.GET.get('SQStaffNameing', '')
        SQTimeingStart = request.GET.get('SQTimeingStart', '')
        SQTimeingEnd = request.GET.get('SQTimeingEnd', '')
        SHStaffName = request.GET.get('SHStaffName', '')
        SHTimeStart = request.GET.get('SHTimeStart', '')
        SHTimeEnd = request.GET.get('SHTimeEnd', '')

        allobj = User.objects.filter(groups__id__in=[6])
        userID = []
        for each in allobj:
            userID.append(each.id)
        if (request.user.id in userID) or (request.user.is_superuser == 1):
            qs = qs
        else:
            qs = qs.filter(SQStaffNameing=request.user.first_name)

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']
        if flagcloth == '1':
            qs = qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            qs = qs.exclude(LargeCategory__in=catelist)
        else:
            qs = qs

        if Select == '22':
            qs = qs.filter(CostReduction__isnull=False)
            searchList = {
                'MainSKU__exact': MainSKU, 'SKU__contains': SKU, 'Name2__exact': Name2, 'DevDate__gte': KFTimeStart,
                'DevDate__lt': KFTimeEnd, 'Mstatus__exact': Mstatus, 'SQStaffNameing__exact': SQStaffNameing,
                'SQTimeing__gte': SQTimeingStart, 'SQTimeing__lt': SQTimeingEnd, 'SHStaffName__exact': SHStaffName,
                'SHTime__gte': SHTimeStart, 'SHTime__lt': SHTimeEnd
            }
        else:
            if Select == '1000':
                searchList = {
                    'MainSKU__exact': MainSKU, 'SKU__contains': SKU, 'Name2__exact': Name2, 'DevDate__gte': KFTimeStart,
                    'DevDate__lt': KFTimeEnd, 'PackFlag__exact': '1', 'Mstatus__exact': Mstatus,
                    'SQStaffNameing__exact': SQStaffNameing, 'SQTimeing__gte': SQTimeingStart,
                    'SQTimeing__lt': SQTimeingEnd, 'SHStaffName__exact': SHStaffName, 'SHTime__gte': SHTimeStart,
                    'SHTime__lt': SHTimeEnd
                }
            else:
                searchList = {
                    'MainSKU__exact': MainSKU, 'SKU__contains': SKU, 'Name2__exact': Name2, 'DevDate__gte': KFTimeStart,
                    'DevDate__lt': KFTimeEnd, 'Select__exact': Select, 'Mstatus__exact': Mstatus,
                    'SQStaffNameing__exact': SQStaffNameing, 'SQTimeing__gte': SQTimeingStart,
                    'SQTimeing__lt': SQTimeingEnd, 'SHStaffName__exact': SHStaffName, 'SHTime__gte': SHTimeStart,
                    'SHTime__lt': SHTimeEnd
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
            except:
                messages.error(request, u'输入的查询数据有问题！')
        return qs