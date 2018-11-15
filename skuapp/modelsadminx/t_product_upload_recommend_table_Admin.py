# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from pyapp.models import b_goods as py_b_goods

class t_product_upload_recommend_table_Admin(object):
    def show_Picture(self,obj) :
        url = obj.PICURL.replace('-original.','-medium.')
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(url,url,url)
        return mark_safe(rt)
    show_Picture.short_description = u'图片'
    
    def show_MainSKU_product(self,obj) :
        rt =  "<a href='/Project/admin/skuapp/t_online_info_wish/?_p_MainSKU__exact=%s'>%s</a>"%(obj.MainSKU,obj.MainSKU)
        return mark_safe(rt)
    show_MainSKU_product.short_description = u'主SKU'
        
    list_display = ('id','PlatformName','show_Picture','show_MainSKU_product','CreateTime','Order7days','Nub','UpLoad_Nub',)
    search_fields = ('id','PlatformName','PICURL','MainSKU',)
    list_filter = ('PlatformName','CreateTime','MainSKU','Order7days','Nub','UpLoad_Nub',)