# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.db import connection
from django.contrib import messages
from django.db.models import Q

class v_product_customization_show_Admin(object):
    search_box_flag = True
    left_flag = True

    list_per_page = 20
    def show_Picture(self,obj) :
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(obj.BmpUrl,obj.BmpUrl,obj.BmpUrl)
        return mark_safe(rt)
    show_Picture.short_description = u'图片'

    def show_Oscode(self, obj):
        rt = ''
        if not obj.SourceOSCode:
            return mark_safe(rt)
        cur = connection.cursor()
        sql = "select SecondClass from py_db.kc_currentstock_sku_oscode where OSCode = '%s'" % obj.SourceOSCode
        cur.execute(sql)
        OSCodeScript = cur.fetchone()

        rt = u"%s<br>%s " % (obj.SourceOSCode, OSCodeScript[0])
        cur.close()
        return mark_safe(rt)

    show_Oscode.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">采购等级码</p>')

    def show_binding(self, obj):
        cur = connection.cursor()
        sql = "SELECT getFL(Memo), COUNT(*) FROM py_db.b_goodsskulinkshop WHERE SKU = %s GROUP BY getFL(Memo);"
        cur.execute(sql, (obj.SKU,))
        infors = cur.fetchall()
        cur.close()
        rt = '<table class="table table-bordered table-striped table-hover">'
        for infor in infors:
            rt = rt + u'<tr><td>{}</td><td>{}</td></tr>'.format(infor[0], infor[1])
        return mark_safe(rt + '</table>')

    show_binding.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">SKU绑定统计</p>')

    list_display = (
    'show_Picture', 'SKU', 'show_binding', 'GoodsStatus', 'Number', 'UseNumber', 'ReservationNum', 'SellCount1', 'SellCount2',
    'SellCount3', 'NotInStore', 'hopeUseNum', 'Purchaser', 'SalerName2', 'SupplierName', 'SaleDay', 'show_Oscode',
    'tortinfo', 'UpdateTime')

    def get_list_queryset(self, ):
        request = self.request
        qs = super(v_product_customization_show_Admin, self).get_list_queryset()
        SKU = request.GET.get('SKU', '')
        SKU = SKU.split(',')
        if '' in SKU:
            SKU = ''
        AllAvailableNumberStart = request.GET.get('AllAvailableNumberStart', '')
        AllAvailableNumberEnd = request.GET.get('AllAvailableNumberEnd', '')
        isClothes = request.GET.get('clothes', '0')
        Purchaser = request.GET.get('Purchaser', '')
        Purchaser = Purchaser.split(',')
        if '' in Purchaser:
            Purchaser = ''
        radioStart = request.GET.get('radioStart', '')
        radioEnd = request.GET.get('radioEnd', '')
        tortinfo = request.GET.get('tortinfo', '')
        storeID = request.GET.get('storeID', '')
        storeID = storeID.split(',')
        if '' in storeID:
            storeID = ''
        SalerName = request.GET.get('SalerName', '')
        IsCg = request.GET.get('IsCg', '')
        IsCg = IsCg.split(',')
        if '' in IsCg:
            IsCg = ''
        SaleDateStart = request.GET.get('SaleDateStart', '')
        SaleDateEnd = request.GET.get('SaleDateEnd', '')
        SupplierName = request.GET.get('SupplierName', '')
        handleResults = request.GET.get('handleResults', '')
        orders7DaysStart = request.GET.get('orders7DaysStart', '')
        orders7DaysEnd = request.GET.get('orders7DaysEnd', '')
        orders15DaysStart = request.GET.get('orders15DaysStart', '')
        orders15DaysEnd = request.GET.get('orders15DaysEnd', '')
        orders30DaysStart = request.GET.get('orders30DaysStart', '')
        orders30DaysEnd = request.GET.get('orders30DaysEnd', '')
        NotInStoreStart = request.GET.get('NotInStoreStart', '')
        NotInStoreEnd = request.GET.get('NotInStoreEnd', '')
        hopeUseNumStart = request.GET.get('hopeUseNumStart', '')
        hopeUseNumEnd = request.GET.get('hopeUseNumEnd', '')
        LargeCategory = request.GET.get('LargeCategory', '')
        GoodsStatus = request.GET.get('GoodsStatus', '')
        GoodsStatus = [gs for gs in GoodsStatus.split(',') if gs]
        OSCode = request.GET.get('OSCode', '')
        NotSuggest = request.GET.get('NotSuggest', '')
        MainSKU = request.GET.get('MainSKU', '')
        MainSKU = [gs for gs in MainSKU.split(',') if gs]

        searchList = {'SKU__in': SKU, 'Purchaser__in': Purchaser,
                      'SalerName2__exact': SalerName, 'storeID__in': storeID,
                      'CategoryCode__exact': LargeCategory,
                      'FromClothes__exact': isClothes,
                      'OSCode__exact': OSCode, 'MainSKU__in': MainSKU,
                      'tortinfo__icontains': tortinfo, 'IsCg__in': IsCg,
                      'GoodsStatus__in': GoodsStatus, 'SupplierName__exact': SupplierName,
                      'UseNumber__gte': AllAvailableNumberStart, 'UseNumber__lt': AllAvailableNumberEnd,
                      'SaleDay__gte': SaleDateStart, 'SaleDay__lt': SaleDateEnd,
                      'radio__gte': radioStart, 'radio__lt': radioEnd,
                      'SellCount1__gte': orders7DaysStart, 'SellCount1__lt': orders7DaysEnd,
                      'SellCount2__gte': orders15DaysStart, 'SellCount2__lt': orders15DaysEnd,
                      'SellCount3__gte': orders30DaysStart, 'SellCount3__lt': orders30DaysEnd,
                      'NotInStore__gte': NotInStoreStart, 'NotInStore__lt': NotInStoreEnd,
                      'hopeUseNum__gte': hopeUseNumStart, 'hopeUseNum__lt': hopeUseNumEnd, }

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！:{}'.format(ex))
        if NotSuggest == '1':
            qs = qs.exclude(SupplierName__contains="广州工厂").exclude(SupplierName__contains="易臻工厂")
        if handleResults == 'Y':
            return qs.filter(HandleResults='Y')
        elif handleResults == 'W':
            return qs.filter(HandleResults='W')
        elif handleResults == 'H':
            return qs.filter(HandleResults='H')
        else:
            return qs









