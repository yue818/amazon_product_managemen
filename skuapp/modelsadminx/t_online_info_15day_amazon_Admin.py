# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
import datetime

class t_online_info_15day_amazon_Admin(object):
    
    def show_item_description(self,obj) :
        return mark_safe(obj.item_description)
    show_item_description.short_description = u'item_description'
    
    def show_Picture(self,obj) :
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(obj.image_url,obj.image_url,obj.image_url)
        return mark_safe(rt)
    show_Picture.short_description = u'图片'
    
    list_display = ('id','show_Picture','item_name','show_item_description','seller_sku','order7days','orderydays','ordertdays','ordercdays','allorder','price','open_date',)
    list_editable = ('Remarks',)
    list_filter = ('item_name','item_description','seller_sku','order7days','orderydays','ordertdays','ordercdays','allorder','price','open_date',)
    search_fields = ('item_name','item_description','seller_sku',)
    
    def get_list_queryset(self):
        request = self.request
        
        return super(t_online_info_15day_amazon_Admin,self).get_list_queryset().filter(open_date__lte=(datetime.datetime.now()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d'),open_date__gte=(datetime.datetime.now()+datetime.timedelta(days=-15)).strftime('%Y-%m-%d'))
    
