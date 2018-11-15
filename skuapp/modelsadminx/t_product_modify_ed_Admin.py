# -*- coding: utf-8 -*-

from .t_product_Admin import *
from django.db.models import Q
from datetime import datetime
from skuapp.table.t_shopsku_information_binding import t_shopsku_information_binding
from skuapp.table.t_online_info_amazon_listing import t_online_info_amazon_listing
from app_djcelery.tasks import amazon_product_refresh
from brick.public.product_modify_show_function import product_modify_show_function


class t_product_modify_ed_Admin(product_modify_show_function):
    downloadxls = True
    search_box_flag = True
    enter_ed_classification = True

    list_display = (
        'id', 'MainSKU', 'show_SKU_InputBox', 'show_PIC', 'show_product', 'Select',
        'show_XGcontext', 'show_details', 'Mstatus', 'show_sq', 'show_lq', 'show_sh', 'show_xg', 'remarks', 'BHRemark'
    )
    list_display_links = ('',)
    actions = ['not_online', 'to_remark', 'batch_dis_data_by_api', 'batch_en_data_by_api', 'to_excel', 'to_excel_new', 'to_excel_reduction']

    def to_remark(self, request, queryset):
        for querysetid in queryset.all():
            t_product_information_modify_objs = t_product_information_modify.objects.filter(id=querysetid.id)  # 为了获取该记录原来的‘备注’
            t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)  # 为了获取该记录 备注 修改人的 部门编号
            if t_sys_department_staff_objs.exists():
                rr = t_sys_department_staff_objs[0].DepartmentID  # 部门编号
                xx = u'%s:%s(%s)' % (rr, request.user.first_name, str(datetime.now())[0:10])  # 现 备注
                if t_product_information_modify_objs.exists() and t_product_information_modify_objs[0].remarks is not None:
                    qq = t_product_information_modify_objs[0].remarks  # 原 备注
                    t_product_information_modify_objs.update(remarks=u'%s<br>%s' % (qq, xx))
                elif t_product_information_modify_objs.exists() and t_product_information_modify_objs[0].remarks is None:
                    t_product_information_modify_objs.update(remarks=u'%s' % (xx))
                if rr == '1':
                    t_product_information_modify.objects.filter(id=querysetid.id).update(Dep1=request.user.first_name, Dep1Date=datetime.now(), Dep1Sta='修改完成')
                if rr == '2':
                    t_product_information_modify.objects.filter(id=querysetid.id).update(Dep2=request.user.first_name, Dep2Date=datetime.now(), Dep2Sta='修改完成')
                if rr == '3':
                    t_product_information_modify.objects.filter(id=querysetid.id).update(Dep3=request.user.first_name, Dep3Date=datetime.now(), Dep3Sta='修改完成')
                if rr == '4':
                    t_product_information_modify.objects.filter(id=querysetid.id).update(Dep4=request.user.first_name, Dep4Date=datetime.now(), Dep4Sta='修改完成')
                if rr == '5':
                    t_product_information_modify.objects.filter(id=querysetid.id).update(Dep5=request.user.first_name, Dep5Date=datetime.now(), Dep5Sta='修改完成')
            else:
                messages.error(request, '对不起！没有你的部门记录！请联系相关人员')
    to_remark.short_description = u'修改完成(销售部门操作)'

    def not_online(self, request, queryset):
        for querysetid in queryset.all():
            t_product_information_modify_objs = t_product_information_modify.objects.filter(id=querysetid.id)  # 为了获取该记录原来的‘备注’
            t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=request.user.username)  # 为了获取该记录 备注 修改人的 部门编号
            if t_sys_department_staff_objs.exists():
                rr = t_sys_department_staff_objs[0].DepartmentID  # 部门编号
                xx = u'%s:%s(%s)' % (rr, request.user.first_name, str(datetime.now())[0:10])  # 现 备注
                if t_product_information_modify_objs.exists() and t_product_information_modify_objs[0].remarks is not None:
                    qq = t_product_information_modify_objs[0].remarks  # 原 备注
                    t_product_information_modify_objs.update(remarks=u'%s<br>%s(不在线)' % (qq, xx))
                elif t_product_information_modify_objs.exists() and t_product_information_modify_objs[0].remarks is None:
                    t_product_information_modify_objs.update(remarks=u'%s不在线' % (xx))
                if rr == '1':
                    t_product_information_modify.objects.filter(id=querysetid.id).update(Dep1=request.user.first_name, Dep1Date=datetime.now(), Dep1Sta='不在线')
                if rr == '2':
                    t_product_information_modify.objects.filter(id=querysetid.id).update(Dep2=request.user.first_name, Dep2Date=datetime.now(), Dep2Sta='不在线')
                if rr == '3':
                    t_product_information_modify.objects.filter(id=querysetid.id).update(Dep3=request.user.first_name, Dep3Date=datetime.now(), Dep3Sta='不在线')
                if rr == '4':
                    t_product_information_modify.objects.filter(id=querysetid.id).update(Dep4=request.user.first_name, Dep4Date=datetime.now(), Dep4Sta='不在线')
                if rr == '5':
                    t_product_information_modify.objects.filter(id=querysetid.id).update(Dep5=request.user.first_name, Dep5Date=datetime.now(), Dep5Sta='不在线')
            else:
                messages.error(request, '对不起！没有你的部门记录！请联系相关人员')
    not_online.short_description = u'不在线(销售部门操作)'

    def batch_en_data_by_api(self, request, queryset):
        from django.http import HttpResponseRedirect
        import urllib
        import datetime
        print request.user.username
        shop_sku = {}
        sku_select = []
        for record in queryset.all():
            sku_list = record.InputBox.split(',')
            for sku in sku_list:
                sku_bind_obj = t_shopsku_information_binding.objects.filter(SKU=sku)
                for seller_sku_obj in sku_bind_obj:
                    amazon_list_obj = t_online_info_amazon_listing.objects.filter(seller_sku=seller_sku_obj.ShopSKU)
                    for list_obj in amazon_list_obj:
                        seller_sku = list_obj.seller_sku
                        shop_name = list_obj.ShopName
                        sku_select.append(seller_sku)
                        if not shop_sku.has_key(shop_name):
                            shop_sku[shop_name] = [seller_sku]
                        else:
                            shop_sku[shop_name].append(seller_sku)
        sku_str = ''
        for sku_each in sku_select:
            t_online_info_amazon_listing.objects.filter(seller_sku=sku_each).update(deal_action='load_product',
                                                                                    deal_result=None,
                                                                                    deal_result_info=None,
                                                                                    UpdateTime=datetime.datetime.now())
            sku_str = sku_str + sku_each + ','
        if sku_str == '':
            sku_str = ' '
        else:
            sku_str = sku_str[:-1]
        sku_str = urllib.quote(sku_str.decode('gbk', 'replace').encode('utf-8', 'replace'))
        if shop_sku:
            amazon_product_refresh(shop_sku, 'load_product')
        return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_amazon_listing/?all=&seller_sku=%s' % sku_str)
    batch_en_data_by_api.short_description = u'产品上架'

    def batch_dis_data_by_api(self, request, queryset):
        from django.http import HttpResponseRedirect
        import urllib
        import datetime
        shop_sku = {}
        sku_select = []
        for record in queryset.all():
            sku_list = record.InputBox.split(',')
            for sku in sku_list:
                sku_bind_obj = t_shopsku_information_binding.objects.filter(SKU=sku)
                for seller_sku_obj in sku_bind_obj:
                    amazon_list_obj = t_online_info_amazon_listing.objects.filter(seller_sku=seller_sku_obj.ShopSKU)
                    for list_obj in amazon_list_obj:
                        seller_sku = list_obj.seller_sku
                        shop_name = list_obj.ShopName
                        sku_select.append(seller_sku)
                        if not shop_sku.has_key(shop_name):
                            shop_sku[shop_name] = [seller_sku]
                        else:
                            shop_sku[shop_name].append(seller_sku)
        sku_str = ''
        for sku_each in sku_select:
            t_online_info_amazon_listing.objects.filter(seller_sku=sku_each).update(deal_action='unload_product',
                                                                                    deal_result=None,
                                                                                    deal_result_info=None,
                                                                                    UpdateTime=datetime.datetime.now())
            sku_str = sku_str + sku_each + ','
        if sku_str == '':
            sku_str = ' '
        else:
            sku_str = sku_str[:-1]
        sku_str = urllib.quote(sku_str.decode('gbk', 'replace').encode('utf-8', 'replace'))
        if shop_sku:
            amazon_product_refresh(shop_sku, 'unload_product')
        return HttpResponseRedirect('/Project/admin/skuapp/t_online_info_amazon_listing/?all=&seller_sku=%s' % sku_str)
    batch_dis_data_by_api.short_description = u'产品下架'

    def get_list_queryset(self):
        request = self.request
        qs = super(t_product_modify_ed_Admin, self).get_list_queryset()
        qs = qs.filter(Q(Mstatus='WCXG') | Q(Mstatus='WCHT'))

        flagcloth = request.GET.get('classCloth', '')
        MainSKU = request.GET.get('MainSKU', '')
        SKU = request.GET.get('SKU', '')
        Name2 = request.GET.get('Name2', '')
        KFTimeStart = request.GET.get('KFTimeStart', '')
        KFTimeEnd = request.GET.get('KFTimeEnd', '')
        DepartmentalState = request.GET.get('DepartmentalState', '')
        Select = request.GET.get('Select', '')
        Mstatus = request.GET.get('Mstatus', '')
        SQStaffNameing = request.GET.get('SQStaffNameing', '')
        SQTimeingStart = request.GET.get('SQTimeingStart', '')
        SQTimeingEnd = request.GET.get('SQTimeingEnd', '')
        XGStaffName = request.GET.get('XGStaffName', '')
        XGTimeStart = request.GET.get('XGTimeStart', '')
        XGTimeEnd = request.GET.get('XGTimeEnd', '')
        SHStaffName = request.GET.get('SHStaffName', '')
        SHTimeStart = request.GET.get('SHTimeStart', '')
        SHTimeEnd = request.GET.get('SHTimeEnd', '')

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        if flagcloth == '1':
            qs = qs.filter(LargeCategory__in=catelist)
        elif flagcloth == '2':
            qs = qs.exclude(LargeCategory__in=catelist)

        if Select == '22':
            qs = qs.filter(CostReduction__isnull=False)
            searchList = {
                'MainSKU__exact': MainSKU, 'SKU__contains': SKU, 'Name2__exact': Name2, 'DevDate__gte': KFTimeStart,
                'DevDate__lt': KFTimeEnd, 'Mstatus__exact': Mstatus, 'SQStaffNameing__exact': SQStaffNameing,
                'SQTimeing__gte': SQTimeingStart, 'SQTimeing__lt': SQTimeingEnd, 'XGStaffName__exact': XGStaffName,
                'XGTime__gte': XGTimeStart, 'XGTime__lt': XGTimeEnd, 'SHStaffName__exact': SHStaffName,
                'SHTime__gte': SHTimeStart, 'SHTime__lt': SHTimeEnd
            }
        else:
            if Select == '1000':
                searchList = {
                    'MainSKU__exact': MainSKU, 'SKU__contains': SKU, 'Name2__exact': Name2, 'DevDate__gte': KFTimeStart,
                    'DevDate__lt': KFTimeEnd, 'PackFlag__exact': '1', 'Mstatus__exact': Mstatus,
                    'SQStaffNameing__exact': SQStaffNameing, 'SQTimeing__gte': SQTimeingStart,
                    'SQTimeing__lt': SQTimeingEnd, 'XGStaffName__exact': XGStaffName, 'XGTime__gte': XGTimeStart,
                    'XGTime__lt': XGTimeEnd, 'SHStaffName__exact': SHStaffName, 'SHTime__gte': SHTimeStart,
                    'SHTime__lt': SHTimeEnd
                }
            else:
                searchList = {
                    'MainSKU__exact': MainSKU, 'SKU__contains': SKU, 'Name2__exact': Name2, 'DevDate__gte': KFTimeStart,
                    'DevDate__lt': KFTimeEnd, 'Select__exact': Select, 'Mstatus__exact': Mstatus,
                    'SQStaffNameing__exact': SQStaffNameing, 'SQTimeing__gte': SQTimeingStart,
                    'SQTimeing__lt': SQTimeingEnd, 'XGStaffName__exact': XGStaffName, 'XGTime__gte': XGTimeStart,
                    'XGTime__lt': XGTimeEnd, 'SHStaffName__exact': SHStaffName, 'SHTime__gte': SHTimeStart,
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
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        if DepartmentalState == u'一部已领用':
            qs = qs.filter(Dep1__isnull=False)
        if DepartmentalState == u'一部未领用':
            qs = qs.filter(Dep1__isnull=True)
        if DepartmentalState == u'二部已领用':
            qs = qs.filter(Dep2__isnull=False)
        if DepartmentalState == u'二部未领用':
            qs = qs.filter(Dep2__isnull=True)
        if DepartmentalState == u'三部已领用':
            qs = qs.filter(Dep3__isnull=False)
        if DepartmentalState == u'三部未领用':
            qs = qs.filter(Dep3__isnull=True)
        if DepartmentalState == u'四部已领用':
            qs = qs.filter(Dep4__isnull=False)
        if DepartmentalState == u'四部未领用':
            qs = qs.filter(Dep4__isnull=True)
        if DepartmentalState == u'五部已领用':
            qs = qs.filter(Dep5__isnull=False)
        if DepartmentalState == u'五部未领用':
            qs = qs.filter(Dep5__isnull=True)

        return qs



