# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_history_Admin.py
 @time: 2018/4/28 8:53
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
from datetime import datetime
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.db.models import Q

class t_cloth_factory_dispatch_history_Admin(object):
    search_box_flag = True
    t_cloth_factory = True
    def ossNum(self, obj):
        rt = ""
        if obj.oosNum > 0:
            rt = u"<font size='4' color='red'>%s</font>"%(obj.oosNum)
        else:
            rt = u"<font size='4' color='red'>0</font>"
        return mark_safe(rt)
    ossNum.short_description = mark_safe(u'<p style="width:100px;color:#428bca;" align="center">缺货及未派单量</p>')

    def GoodsOther(self,obj):
        rt = u'<p style="width:120px;"><strong>商品成本价:</strong>%s <br><strong>7天销量:</strong>%s <br><strong>预计库存量:</strong>%s<br><strong>采购未入库量:</strong>%s</p>' % (obj.goodsCostPrice,obj.sevenSales,obj.ailableNum,obj.PurchaseNotInNum)
        if obj.SpecialPurchaseFlag is not None and obj.SpecialPurchaseFlag != '':
            if obj.SpecialPurchaseFlag == 'firstorder':
                rt = rt + u'<br><strong>注:手动新增-网采转供应链排单(首单)</strong>'
            elif obj.SpecialPurchaseFlag == 'customermade':
                rt = rt + u'<br><strong>注:手动新增-客户定做</strong>'
            elif obj.SpecialPurchaseFlag == 'other':
                rt = rt + u'<br><strong>注:手动新增-浦江仓库</strong>'
        elif obj.OSCode == 'OS906' and obj.Stocking_plan_number is not None and obj.Stocking_plan_number != '':
            rt = rt + u'<br><strong>注:海外仓备货转服装排单</strong>'
        else:
            rt = rt + u'<br><strong>注:系统自动生成采购</strong>'
        return mark_safe(rt)
    GoodsOther.short_description = mark_safe(u'<p style="width:120px;color:#428bca;" align="center">商品其他信息</p>')

    def GoodsInfo(self,obj):
        rt = u'<p style="width:200px;"><strong>商品名称:</strong>%s <br><strong>供应商名:</strong>%s <br><strong>商品状态:</strong>%s<br><strong>商品类别:</strong>%s<br><strong>侵权站点:</strong>%s<br><strong>上一步处理人员:</strong>%s<br><strong>上一步处理时间:</strong>%s</p>' % (obj.goodsName,obj.Supplier, obj.goodsState,obj.goodsclass,obj.TortInfo,obj.genPurchaseMan,obj.genPurchaseDate)
        return mark_safe(rt)
    GoodsInfo.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">商品及流程信息</p>')

    def show_Picture(self,obj) :
        # self.update_status(obj)
        from Project.settings import BmpUrl
        # 获取图片的url
        picture_url = obj.BmpUrl  # 获取图片的url
        sku = obj.SKU  # 获取商品SKU
        if not picture_url:
            picture_url = BmpUrl + sku + '.jpg'

        rt = """<img src="%s"  width="120" height="120"  title="%s" onerror="this.title=''" />  """ % (picture_url, picture_url)
        return mark_safe(rt)
    show_Picture.short_description = mark_safe(u'<p style="width:120px;color:#428bca;" align="center">图片</p>')

    list_per_page = 20
    list_display = ('SKU', 'show_Picture', 'buyer', 'SalerName2','OSCode','GoodsInfo', 'GoodsOther',
                    'ossNum', 'SuggestNum', 'SaleDay', 'remarkGenPurchase',)

    fields = (
    'SKU', 'goodsName', 'Supplier', 'goodsState', 'goodsCostPrice', 'oosNum', 'stockNum', 'ailableNum',
    'sevenSales', 'fifteenSales',
    'thirtySales', 'PurchaseNotInNum', 'buyer',  'productNumbers', 'loanMoney',
    'actualMoney', 'outFactory', 'unit','rawNumbers',
    'remarkApply','productNumbers',)


    def get_list_queryset(self):
        request = self.request
        qs = super(t_cloth_factory_dispatch_history_Admin, self).get_list_queryset()

        #PurchaseNotInNum = request.GET.get('PurchaseNotInNum', '')
        SKU = request.GET.get('SKU', '')

        Supplier = request.GET.get('Supplier', '')
        buyer = request.GET.get('buyer', '')
        buyer = buyer.split(',')
        if '' in buyer:
            buyer = ''
        oosNumStart = request.GET.get('oosNum_Start', '')
        oosNumEnd = request.GET.get('oosNum_End', '')
        genPurchaseDate_Start = request.GET.get('genPurchaseDate_Start', '')
        genPurchaseDate_End = request.GET.get('genPurchaseDate_End', '')
        goodsState = request.GET.get('goodsState', '')
        from skuapp.table.goodsstatus_compare import goodsstatus_compare
        goodsstatus_compare_objs = goodsstatus_compare.objects.filter(py_GoodsStatus=goodsState).values_list(
            "hq_GoodsStatus", flat=True)

        createDateEnd = (datetime.now()).strftime('%Y-%m-%d 00:00:00')
        currentState = request.GET.get('currentState', '')

        createDateStart = request.GET.get('createDate_Start', '')
        createDateEnd1 = request.GET.get('createDate_End', '')
        if createDateEnd1 > createDateEnd:
            createDateEnd1 = createDateEnd
        searchList = {'SKU__contains': SKU,
                      'Supplier':Supplier,
                      'buyer__in': buyer,
                      'oosNum__gte': oosNumStart,
                      'oosNum__lt': oosNumEnd,
                      'genPurchaseDate__gte': genPurchaseDate_Start,
                      'genPurchaseDate__lt': genPurchaseDate_End,
                      'goodsState__in':list(goodsstatus_compare_objs),
                      'createDate__gte': createDateStart,
                      'createDate__lt': createDateEnd1,
                      'currentState':currentState,
                      }
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
                messages.error(request, u'输入的查询数据有问题！')

        from django.contrib.auth.models import User
        userID = [each.id for each in User.objects.filter(groups__id__in=[48])]
        if request.user.is_superuser or request.user.id in userID:
            return qs.filter(Q(currentState = 0)|Q(currentState = 32))
        buyer = request.user.first_name
        return qs.filter(Q(currentState = 0)|Q(currentState = 32),buyer=buyer)

        #qs.filter(Q(CategoryCode=u'001.时尚女装') | Q(CategoryCode=u'002.时尚男装')| Q(CategoryCode=u'025.内衣')| Q(CategoryCode=u'021.泳装')| Q(CategoryCode=u'024.儿童服装')).filter(GoodsStatus='normal')

