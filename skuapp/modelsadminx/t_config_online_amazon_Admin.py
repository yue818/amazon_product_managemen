# -*- coding: utf-8 -*-
from skuapp.table.t_sys_param import t_sys_param
from django.utils.safestring import mark_safe

class t_config_online_amazon_Admin(object):
    def show_site_cn_name(self, obj):  
        t_sys_param_objs  =  t_sys_param.objects.filter(TypeDesc='ChoiceSiteconfiguration').filter(V=obj.site)
        rt = ''
        for cn_site in t_sys_param_objs:
            rt = cn_site.VDesc
        return mark_safe(rt)
    show_site_cn_name.short_description = u'站点名称'

    list_display=('id','IP','Name','K','V','shop_name','show_site_cn_name',)
    list_filter = ('IP','Name','K','V','shop_name','site',)
    search_fields = ('IP','Name','K','V','shop_name','site',)