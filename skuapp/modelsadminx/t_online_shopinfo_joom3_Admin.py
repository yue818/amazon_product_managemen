# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

class t_online_shopinfo_joom3_Admin(object):
    
    #def show_item_description(self,obj) :
        #return mark_safe(obj.item_description)
   # show_item_description.short_description = u'item_description'
    
    def show_main_image(self,obj) :
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(obj.main_image,obj.main_image,obj.main_image)
        return mark_safe(rt)
    show_main_image.short_description = u'main_image'
    
    def show_extra_images(self,obj) :
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(obj.extra_images,obj.extra_images,obj.extra_images)
        return mark_safe(rt)
    show_extra_images.short_description = u'extra_images'
    
    list_display = ('id','product_id','show_main_image','show_extra_images','name','description','parent_sku','number_sold','number_saves','number_orders','number_refunds','refund_rate','review_status','original_image_url','tags','is_promoted','Variant_id','sku','price','shipping','msrp','inventory','shipping_time','size','Variant_enabled','date_uploaded','product_enabled')
    list_editable = ('name','description','parent_sku','number_sold','number_saves','number_orders','number_refunds','refund_rate','review_status','show_main_image','show_extra_images','original_image_url','tags','is_promoted','Variant_id','sku','price','shipping','msrp','inventory','shipping_time','size','Variant_enabled','date_uploaded','product_enabled')
    list_filter = ('product_id','name','parent_sku','tags','is_promoted','Variant_id','sku','price','shipping','msrp','inventory','shipping_time','size','Variant_enabled','date_uploaded','product_enabled')
    search_fields = ('product_id','name','parent_sku','tags','is_promoted','Variant_id','sku','price','shipping','msrp','inventory','shipping_time','size','Variant_enabled','date_uploaded','product_enabled')
    
    
    
           
    
