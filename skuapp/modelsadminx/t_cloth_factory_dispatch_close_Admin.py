# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_close_Admin.py
 @time: 2018/4/28 8:53
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_cloth_factory_dispatch_close import *
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.utils.safestring import mark_safe

class t_cloth_factory_dispatch_close_Admin(object):
    search_box_flag = True
    t_cloth_factory = True

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

    def show_rawNumbers(self, obj):
        rt = u'<strong>原材料数量:</strong>%s(%s)<br><strong>采购数量:</strong>%s<br><strong>外派工厂:</strong>%s<br><strong>采购备注:</strong>%s<br><strong>审核备注:</strong>%s<br><strong>交付备注:</strong>%s' % (
            obj.rawNumbers, obj.unit, obj.productNumbers, obj.outFactory, obj.remarkApply, obj.remarkAudit,str(obj.remarkDisPatch).replace('#@#',','))

        return mark_safe(rt)
    show_rawNumbers.short_description = mark_safe('<p align="center" style="width:180px;color:#428bca;">排单信息</p>')

    def show_otherInfo(self, obj):
        rt = u'<strong>生成采购计划人员:</strong>%s<br><strong>采购计划编辑人员:</strong>%s<br><strong>采购计划审核人员:</strong>%s<br><strong>转工厂交付系统人员:</strong>%s<br><strong>排单校验交付人员:</strong>%s' \
             u'<br><strong>流程关闭人员:</strong>%s' \
             u'<br><strong>创建时间:</strong>%s<br><strong>关闭时间:</strong>%s' % \
             (obj.genPurchaseMan,obj.applyMan,obj.auditMan,obj.dispatchMan,obj.confirmMan,obj.closeMan,obj.genPurchaseDate,obj.closeDate)

        return mark_safe(rt)
    show_otherInfo.short_description = mark_safe('<p align="center" style="width:200px;color:#428bca;">流程信息</p>')

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
        rt = u'<p style="width:200px;"><strong>商品名称:</strong>%s <br><strong>供应商名:</strong>%s <br><strong>商品状态:</strong>%s<br><strong>商品类别:</strong>%s<br><strong>侵权站点:</strong>%s<br><strong>上一步处理人员:</strong>%s<br><strong>上一步处理时间:</strong>%s</p>' % (obj.goodsName,obj.Supplier, obj.goodsState,obj.goodsclass,obj.TortInfo,obj.closeMan,obj.closeDate)
        return mark_safe(rt)
    GoodsInfo.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">商品及流程信息</p>')

    list_per_page = 20
    list_display = (
        'SKU','show_Picture',  'buyer', 'SalerName2','OSCode','GoodsInfo',
        'GoodsOther', 'show_rawNumbers','show_otherInfo','completeNumbers',)

    fields = (
        'SKU', 'goodsName', 'Supplier', 'goodsState', 'goodsCostPrice', 'oosNum', 'stockNum', 'ailableNum',
        'sevenSales', 'fifteenSales',
        'thirtySales', 'PurchaseNotInNum', 'buyer', 'productNumbers', 'loanMoney',
        'actualMoney', 'outFactory', 'rawNumbers', 'unit',
        'remarkApply', 'remarkApply', 'applyMan', 'auditMan',  'remarkAudit', 'createDate','closeDate','applyMan','auditMan','confirmMan',)


    def get_list_queryset(self):
        request = self.request
        qs = super(t_cloth_factory_dispatch_close_Admin, self).get_list_queryset()
        SKU = request.GET.get('SKU', '')

        Supplier = request.GET.get('Supplier', '')
        buyer = request.GET.get('buyer', '')
        buyer = buyer.split(',')
        if '' in buyer:
            buyer = ''
        oosNumStart = request.GET.get('oosNum_Start', '')
        oosNumEnd = request.GET.get('oosNum_End', '')

        goodsState = request.GET.get('goodsState', '')
        outFactory = request.GET.get('outFactory', '')
        from skuapp.table.goodsstatus_compare import goodsstatus_compare
        goodsstatus_compare_objs = goodsstatus_compare.objects.filter(py_GoodsStatus=goodsState).values_list(
            "hq_GoodsStatus", flat=True)

        createDateStart = request.GET.get('createDate_Start', '')
        createDateEnd = request.GET.get('createDate_End', '')

        searchList = {'SKU__contains': SKU,
                      'Supplier':Supplier,
                      'buyer__in': buyer,
                      'oosNum__gte': oosNumStart,
                      'oosNum__lt': oosNumEnd,
                      'goodsState__in':list(goodsstatus_compare_objs),
                      'createDate__gte': createDateStart,
                      'createDate__lt': createDateEnd,
                      'outFactory__contains': outFactory,
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

        from django.contrib.auth.models import User
        userID = [each.id for each in User.objects.filter(groups__id__in=[48])]
        if request.user.is_superuser or request.user.id in userID:
            return qs.filter(currentState = 28)
        buyer = request.user.first_name
        return qs.filter(currentState = 28,buyer=buyer)
        #return qs.filter(currentState = 28)


