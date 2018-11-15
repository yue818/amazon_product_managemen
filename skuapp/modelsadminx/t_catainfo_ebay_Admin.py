# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_catainfo_ebay import *
from skuapp.table.t_hotsale_proinfo_ebay import *
class t_catainfo_ebay_Admin(object):
    list_per_page=10
    def title_url(self,obj) :
        rt = ''
        rt = u'<a href="/xadmin/skuapp/t_hotsale_proinfo_ebay/?_p_CatagoryID=%s"target="_blank">%s</a>'%(obj.CatagoryID,obj.CatagoryName1)
        return mark_safe(rt)
    title_url.short_description = u'类目名称'

    list_display =('CatagoryID','title_url','mount','refresh','LastRefreshTimeE','cata1','cata2','cata3','bsSoldCond','tagBS','department')
    search_fields =('CatagoryID','CatagoryName1','cata1','cata2','cata3')
    list_filter =('LastRefreshTimeE','CreateTime','CatagoryLv','cata1','cata2','cata3','bsSoldCond','tagBS','department')
    list_display_links = ('CatagoryID')
    list_editable = ('tagBS','URL','bsURL','cata1','cata2','cata3','bsSoldCond','department')
    readonly_fields = ('mount','refresh','LastRefreshTimeE','CreateTime','StaffID')
    def save_models(self):
        obj = self.new_obj
        request = self.request
        if obj is None or obj.id is None or obj.id <=0:
            obj.StaffID = request.user.username
            obj.CreateTime = datetime.now()
            obj.mount = 0
            obj.refresh = 0
        obj.save()
        
    def delete_models(self, queryset):
        n = queryset.count()
        noDelete = 0
        if n:
            for obj in queryset:
                if obj.tagBS == 'Y':
                    noDelete = noDelete + 1
                    continue
                products = t_hotsale_proinfo_ebay.objects.filter(CatagoryID=obj.CatagoryID)
                if products is None or products.count() ==0:
                    return
                for product in products:
                    product.delete()
                obj.delete()
            self.message_user("Successfully deleted %d catagories. %d catagories are not deleted because of in use! "%(n-noDelete, noDelete), 'success')
        
