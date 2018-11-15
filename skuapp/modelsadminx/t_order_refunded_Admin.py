# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_order_refunded import *

import time


class t_order_refunded_Admin(object):
    cexport_oss = True
    search_box_flag = True
    def show_Image(self,obj) :
        rt =  '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  '%(obj.Image,obj.Image,obj.Image)
        return mark_safe(rt)
    show_Image.short_description = u'图片'
    list_display= ('id','show_Image','Title','ShopName','OrderDate','OrderId','OrderState','ShopSKU','ProductID','Quantity','Price','Shipping','Shippedon','LastUpdated','UpdateTime','RefundReason','RefundDate')
    list_filter= ('OrderState','ShopName','UpdateTime','OrderDate','LastUpdated',)
    search_fields= ('id','ShopName','OrderDate','OrderId','OrderState','ShopSKU','ProductID','Quantity','Price','Shipping','Shippedon','LastUpdated','Image','Title')
#    def get_list_queryset(self):
#      return super(t_order_refunded_Admin, self).get_list_queryset().filter(OrderState__in=['REFUNDED BY WISH FOR MERCHANT','REFUNDED BY WISH','REFUNDED BY MERCHANT','REFUNDED'])
    
    def get_list_queryset(self,):
        request = self.request
        qs = super(t_order_refunded_Admin, self).get_list_queryset().filter(OrderState__in=['REFUNDED BY WISH FOR MERCHANT','REFUNDED BY WISH','REFUNDED BY MERCHANT','REFUNDED','CANCELLED BY CUSTOMER','CANCELLED BY WISH (FLAGGED TRANSACTION)'])

        orderState = request.GET.get('orderState','')
        shopName = request.GET.get('shopName','')
        orderDateStart = request.GET.get('orderDateStart','')
        orderDateEnd = request.GET.get('orderDateEnd','')
        orderId = request.GET.get('orderId','').strip()
        productID = request.GET.get('productID','').strip()
        refundReason = request.GET.get('refundReason','')
        refundDateStart = request.GET.get('refundDateStart','')
        refundDateEnd = request.GET.get('refundDateEnd','')
		
		


        
        searchList = {'OrderState__exact': orderState, 'ShopName__exact': shopName,   
                      'OrderDate__gte': orderDateStart,'OrderDate__lt': orderDateEnd, 
                      'OrderId__exact':orderId, 'ProductID__exact': productID,
                      'RefundReason__exact': refundReason, 
                      'RefundDate__gte': refundDateStart, 'RefundDate__lt': refundDateEnd,                     
                      }
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    #if k == 'ShopName__exact':
                      #  v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
    
        return qs
