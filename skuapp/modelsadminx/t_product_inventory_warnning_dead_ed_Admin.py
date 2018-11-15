# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_product_inventory_warnning_dead_ed import *
from django.contrib import messages
from skuapp.table.t_tort_aliexpress import *
import requests
from django.http import HttpResponseRedirect
import datetime,time
class t_product_inventory_warnning_dead_ed_Admin(object):
    search_box_flag = True
    #kc_flag = True
    search_flag = False
    #show_kc = True
    
    def show_Picture(self,obj) :
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(obj.image_url,obj.image_url,obj.image_url)
        return mark_safe(rt)
    show_Picture.short_description = u'图片'
    
    def show_AvailableNumber(self,obj):
        rt = ''
        if obj.AllAvailableNumber <=0 :
            rt = '<div class="box" style="width: 80px;height: 30px;background-color: #FFCC33;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(obj.AllAvailableNumber)
        else :
            rt = '%s'%(obj.AllAvailableNumber)
        return mark_safe(rt)
    show_AvailableNumber.short_description = u'可用数量'
    
    def show_Money(self,obj):
        rt = ''
        if obj.Money <= 0:
            rt = '<div class="box" style="width: 80px;height: 30px;background-color: #66FF66;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(obj.Money)
        else:
            rt = '%s'%(obj.Money)
        return mark_safe(rt)
    show_Money.short_description=u'库存金额'
    
    def show_MainSKU(self,obj):
        rt = ''
        if obj.radio <= 0.8:
            rt = '<div class="box" style="width: 80px;height: 30px;background-color: #FF3333;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(obj.MainSKU)
        else:
            rt = '%s'%(obj.MainSKU)
        return mark_safe(rt)
    show_MainSKU.short_description=u'主SKU'
    
    def show_tortInfo(self,obj) :
        rt = ''
        if obj.tortinfo == '未侵权':
            rt = '%s'%(obj.tortinfo)
        else:
            rt = '<div class="box" style="width: 80px;height: 30px;background-color: #66FF66;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(obj.tortinfo)
        return mark_safe(rt)
    show_tortInfo.short_description = u'侵权状态' 

    list_display = ('show_Picture','show_MainSKU','show_tortInfo','order7daysAll','order15daysAll','order30daysAll','show_AvailableNumber','UnitPrice','Weight','show_Money','CreateTime','radio','Discount','SHMstatus')
    #list_editable = ('HandleResults','Remark','Discount')
    #readonly_fields = ('handleTime','Status')
    
    def get_list_queryset(self,):
        request = self.request
        qs = super(t_product_inventory_warnning_dead_ed_Admin, self).get_list_queryset()
        MainSKU = request.GET.get('MainSKU','')
        Purchaser = request.GET.get('Purchaser','')
        radio = request.GET.get('radio','')
        tortinfo = request.GET.get('tortinfo','')
        storeName = request.GET.get('storeName','')
        SalerName = request.GET.get('SalerName','')
        SHMstatus = request.GET.get('SHMstatus','')
        orders7DaysStart = request.GET.get('orders7DaysStart','')
        orders7DaysEnd = request.GET.get('orders7DaysEnd','')
        GoodsCategoryID = request.GET.get('GoodsCategoryID','')
        
        searchList = {'MainSKU__exact': MainSKU,'Purchaser__exact': Purchaser,
                        'radio__lte': radio,'SalerName__exact': SalerName,
                        'storeName__icontains': storeName,'GoodsCategoryID__exact': GoodsCategoryID,
                        'tortinfo__icontains': tortinfo,
                        'order7daysAll__gte': orders7DaysStart, 'order7daysAll__lt': orders7DaysEnd}
                     
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
        return qs.filter(SHMstatus = 'WCSH')