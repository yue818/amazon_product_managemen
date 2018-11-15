# -*- coding: utf-8 -*-
from .t_product_Admin import *
from skuapp.table.p_trade_blacklist_zip import *
from django.utils.safestring import mark_safe
from skuapp.table.t_sys_param import *
from django.contrib import messages
from skuapp.table.b_goods import *


class p_trade_blacklist_zip_Admin(object):
    bla=True
    
    def show_pic(self,obj):
        try:
            rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(obj.pic,obj.pic,obj.pic)  
        except:
            rt = ''
        return mark_safe(rt)
    show_pic.short_description = u'图片'

    def batch_process1(self, request, queryset):
        for qs in queryset.all():
            p_trade_blacklist_zip.objects.filter(id=qs.id).update(Operate='0')
    batch_process1.short_description = u'批量处理==>已处理'

    def batch_process2(self, request, queryset):
        for qs in queryset.all():
            p_trade_blacklist_zip.objects.filter(id=qs.id).update(Operate='1')
    batch_process2.short_description = u'批量处理==>未处理'

    def batch_process3(self, request, queryset):
        for qs in queryset.all():
            p_trade_blacklist_zip.objects.filter(id=qs.id).update(Operate='2')
    batch_process3.short_description = u'批量处理==>忽略'

    def batch_process4(self, request, queryset):
        for qs in queryset.all():
            p_trade_goodsItem = p_trade_blacklist_zip.objects.filter(id=qs.id)
            b_goods_goodsSKU = b_goods.objects.filter(SKU=p_trade_goodsItem.values("AllGoodsDetail"))
            b_goods_goodsSKU.update(GoodsStatus="暂停销售", Used=1)
            p_trade_goodsItem.update(Operate='0')
    batch_process4.short_description = u'批量处理==>下架'

    actions =  ['batch_process1','batch_process2','batch_process3','batch_process4']
           
    list_display= ('NID','AllGoodsDetail','SHIPTOZIP','show_pic','SUFFIX','SHIPTOSTREET','SHIPTOSTREET2','COUNTRYCODE','EMAIL','Operate','OperateDescription','OperateTime','TbTime','ORDERTIME')
    list_editable = ('Operate','OperateDescription',)
    #list_editable_all = ('Keywords',)
    #list_filter = ('UpdateTime',
                   # 'Weight',
                   # 'Electrification','Powder','Liquid','Magnetism','Buyer',
                   # 'Storehouse',
                   # 'DYStaffName','JZLStaffName','PZStaffName','MGStaffName','LRStaffName',
                   # 'StaffName','DepartmentID',
                   # )

    list_filter = ('NID','AllGoodsDetail','SHIPTOZIP','RECEIVERID','SUFFIX','SHIPTOSTREET','SHIPTOSTREET2','COUNTRYCODE','EMAIL','Operate','OperateDescription',)

    search_fields = ('NID','AllGoodsDetail','SHIPTOZIP','RECEIVERID','SUFFIX','SHIPTOSTREET','SHIPTOSTREET2','COUNTRYCODE','EMAIL','Operate','OperateDescription',)

    readonly_fields = ('OperateTime','TbTime')





            
            
            
            
            
            
            
            