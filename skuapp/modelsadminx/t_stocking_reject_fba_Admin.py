# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_reject_fba_Admin.py
 @time: 2018-08-08

"""
from xadmin.layout import Fieldset, Row
import datetime as tmpDate,random
from pyapp.models import b_goods as py_b_goods,B_Supplier as py_b_Supplier
from django.contrib import messages
from django.utils.safestring import mark_safe
from datetime import datetime as ddtime
from skuapp.table.public import *
from django.db import connection as hqdb_conn

class t_stocking_reject_fba_Admin(object):
    search_box_flag = True
    importfile_plugin =True
    fba_tree_menu_flag = True
    hide_page_action = True

    def show_ProductImage(self,obj) :
        from Project.settings import BmpUrl
        # 获取图片的url
        picture_url = obj.ProductImage  # 获取图片的url
        sku = obj.ProductSKU  # 获取商品SKU
        if not picture_url:
            picture_url = BmpUrl + sku + '.jpg'

        rt = """<img src="%s"  width="120" height="120"  title="%s" onerror="this.title=''" />  """ % (picture_url, picture_url)
        return mark_safe(rt)
    show_ProductImage.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">商品图片</p>')

    list_display = (
    'PurchaseOrderNum', 'RejectNumber', 'RejectDate', 'RejectMan', 'ProductSKU', 'ProductName', 'show_ProductImage',
    'RejectNum', 'RejectStatus', 'Remarks')

    fields = ('ProductSKU', 'RejectNum', 'RejectStatus', 'Remarks', 'PurchaseOrderNum')
    list_editable = ('RejectNum', 'Remarks',)
    form_layout = (
        Fieldset(u'请认真填写备货需求',
                 Row('ProductSKU', 'RejectNum', 'RejectStatus', ),
                 Row('PurchaseOrderNum', '', '', ),
                 Row('Remarks', '', '', ),
                 css_class='unsort '
                 ),)


    actions = ['summitReject','not_demand']

    def summitReject(self,request,objs):
        try:
            for obj in objs:
                obj.Status = 'rejecting'
                obj.SummbitRejectMan = request.user.first_name
                obj.SummbitRejectDate = ddtime.now()
                obj.save()
        except Exception, ex:
            messages.info(self.request, "保存报错:%s" % (str(ex)))
    summitReject.short_description = u'提交->转退管理'


    def not_demand(self,request,objs):
        insertinto = []
        from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
        for obj in objs:
            if obj.Status == "reject":
                insertinto.append(t_stocking_demand_fba(
                    Stocking_plan_number=obj.RejectNumber, Stock_plan_date=obj.RejectDate,
                    Demand_people=obj.RejectMan,
                    ProductSKU=obj.ProductSKU, ProductImage=obj.ProductImage, ProductName=obj.ProductName,
                    ProductPrice=0.0,
                    ProductWeight=0.0,
                    Supplier='', Supplierlink='', Buyer='',
                    Status='giveup', Stocking_quantity=obj.RejectNum, QTY=obj.RejectNum,
                    Destination_warehouse='',
                    AccountNum='', Site='', level='', Product_nature='generalcargo',
                    Remarks=u'转退', ShopSKU='', neworold='2', AmazonFactory='no'
                ))
            obj.Status = 'giveup'
            obj.GiveupMan = request.user.first_name
            obj.GiveupDate = ddtime.now()
            obj.save()
        t_stocking_demand_fba.objects.bulk_create(insertinto)
    not_demand.short_description = u'废弃'


    def save_models(self,):
        try:
            obj = self.new_obj
            request = self.request
            old_obj = None
            if obj is None or obj.id is None or obj.id <= 0:
                pass
            else:
                old_obj = self.model.objects.get(pk=obj.pk)
            obj.save()

            obj.RejectNumber = ddtime.now().strftime('%Y%m%d%H%M%S') + '_' + str(obj.id)
            obj.RejectDate = ddtime.now()
            obj.RejectMan = request.user.first_name

            py_b_goods_objs = py_b_goods.objects.filter(SKU=obj.ProductSKU)
            if py_b_goods_objs.exists():
                obj.ProductImage = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % py_b_goods_objs[0].SKU.replace(
                    'OAS-', '').replace('FBA-', '')
                obj.ProductName = py_b_goods_objs[0].GoodsName

            obj.Status='reject'

            obj.save()
        except Exception, ex:
            messages.info(self.request,"保存报错:%s"%(str(ex)))

    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_reject_fba_Admin, self).get_list_queryset()
        from django.contrib.auth.models import User
        userID = [each.id for each in User.objects.filter(groups__id__in=[65])]
        # if request.user.is_superuser or request.user.id in userID:
        if request.user.id in userID:
            qs = qs.filter(RejectMan=request.user.first_name)
        Status = 'reject'
        RejectNumber = request.GET.get('RejectNumber', '')   #转退计划号
        RejectDateStart      = request.GET.get('RejectDateStart', '')     # 转退计划时间
        RejectDateEnd      = request.GET.get('RejectDateEnd', '')     # 转退计划时间
        RejectMan = request.GET.get('RejectMan', '')             # 转退申请人
        PurchaseOrderNum = request.GET.get('PurchaseOrderNum', '')            #采购单号
        ProductSKU = request.GET.get('ProductSKU', '')                     #商品sku
        ProductName = request.GET.get('ProductName', '')                    # 商品名称
        RejectNumStart = request.GET.get('RejectNumStart', '')
        RejectNumEnd = request.GET.get('RejectNumEnd', '')                #转退数量
        RejectStatus = request.GET.get('RejectStatus', '')                         # 转退状态


        searchList = {
                        'RejectNumber__exact':RejectNumber,
                        'Status__exact': Status,
                        'RejectMan__exact': RejectMan,
                        'PurchaseOrderNum__icontains': PurchaseOrderNum,
                        'ProductSKU__icontains': ProductSKU,
                        'ProductName__icontains': ProductName,
                        'RejectStatus__exact': RejectStatus,
                        'RejectDateStart__gte': RejectDateStart, 'RejectDateEnd__lt': RejectDateEnd,
                        'RejectNumStart__gte': RejectNumStart, 'RejectNumEnd__lt': RejectNumEnd,
                      }

        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')

        return qs

