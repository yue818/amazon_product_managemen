# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_tort_brands_info import *

class t_tort_brands_infoAdmin(object):

    def show_PIC(self,obj) :
        t_tort_brands_info_objs = t_tort_brands_info.objects.filter(id = obj.id)
        rt =  '<img src="%s"  alt = "%s"  title="%s"  />  '%(t_tort_brands_info_objs[0].pictureUrl,t_tort_brands_info_objs[0].pictureUrl,t_tort_brands_info_objs[0].pictureUrl)
        return mark_safe(rt)
    show_PIC.short_description = u'图形商标'

    list_display = ('brands','viceBrands','show_PIC')
    list_display_links = ('id',)
    search_fields = ('brands','viceBrands')
    list_filter = ('class_name',)