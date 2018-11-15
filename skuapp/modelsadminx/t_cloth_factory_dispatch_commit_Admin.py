# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_commit_Admin.py
 @time: 2018/4/28 8:53
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_cloth_factory_dispatch_commit import *
from django.contrib import messages
from .t_product_Admin import *
from django.utils.safestring import mark_safe

class t_cloth_factory_dispatch_commit_Admin(object):
    search_box_flag = True
    actions = ['to_commit', 'to_no_commit',]
    t_cloth_factory = True


    def show_Picture(self,obj) :
       # self.update_status(obj)
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(obj.BmpUrl,obj.BmpUrl,obj.BmpUrl)
        return mark_safe(rt)
    show_Picture.short_description = u'图片'

    def to_no_commit(self, request, objs):
        from skuapp.table.t_cloth_factory_dispatch_commit import t_cloth_factory_dispatch_commit
        from datetime import datetime        
        for obj in objs:
            t_cloth_factory_dispatch_commit_obj = t_cloth_factory_dispatch_commit()
            t_cloth_factory_dispatch_commit_obj.__dict__ = obj.__dict__
            t_cloth_factory_dispatch_commit_obj.summitCheckMan = request.user.first_name
            t_cloth_factory_dispatch_commit_obj.summitCheckDate = datetime.now()
            t_cloth_factory_dispatch_commit_obj.currentState = '24'
            t_cloth_factory_dispatch_commit_obj.save()
    to_no_commit.short_description = u'下一步-检验数量和单价'

    def show_Picture(self,obj) :
       # self.update_status(obj)
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(obj.BmpUrl,obj.BmpUrl,obj.BmpUrl)
        return mark_safe(rt)
    show_Picture.short_description = u'图片'

    def show_rawNumbers(self, obj):
        rt = u'原材料数量:%s(%s) <br>商品SKU数量:%s<br>外派工厂:%s<br>采购备注:%s<br>排单备注:%s' % (obj.rawNumbers,obj.unit,obj.productNumbers,obj.outFactory,obj.remarkApply,obj.remarkSpeModify)

        return mark_safe(rt)
    show_rawNumbers.short_description = mark_safe('<p align="center" style="width:200px;color:#428bca;">排单信息</p>')

    list_per_page = 20

    list_display = (
        'id', 'show_Picture', 'SKU', 'goodsName', 'goodsstate', 'OSCode','Supplier', 'buyer', 'SalerName2',
        'sevenSales', 'goodsCostPrice', 'ailableNum', 'PurchaseNotInNum',
        'oosNum','goodsclass','TortInfo', 'show_rawNumbers', )

    fields = (
        'SKU', 'goodsName', 'Supplier', 'goodsstate', 'goodsCostPrice', 'oosNum', 'stockNum', 'ailableNum',
        'sevenSales', 'fifteenSales',
        'thirtySales', 'PurchaseNotInNum', 'buyer', 'productNumbers', 'loanMoney',
        'actualMoney', 'outFactory', 'rawNumbers', 'unit',
        'remarkApply', 'remarkApply', 'remarkAudit','remarkDisPatch',)

    def get_list_queryset(self):
        request = self.request
        qs = super(t_cloth_factory_dispatch_commit_Admin, self).get_list_queryset()

        SKU = request.GET.get('SKU', '')
        Supplier = request.GET.get('Supplier', '')
        buyer = request.GET.get('buyer', '')
        buyer = buyer.split(',')
        if '' in buyer:
            buyer = ''
        oosNumStart = request.GET.get('oosNum_Start', '')
        oosNumEnd = request.GET.get('oosNum_End', '')

        searchList = {'SKU__contains': SKU,
                      'Supplier__contains': Supplier,
                      'buyer__in': buyer,
                      'oosNum__gte': oosNumStart,
                      'oosNum__lt': oosNumEnd,
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
        return qs.filter(currentState = 20)


