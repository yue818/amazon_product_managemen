# -*- coding: utf-8 -*-
from .t_product_Admin import *
from brick.function.formatUrl import format_urls
class t_product_repeats_Admin(t_product_Admin):
    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'----操作历史----'

    # def show_urls(self,obj) :
    #     Platform,linkurl = format_urls(obj.SourceURL if obj.SourceURL else '')
    #     if 'can not formate' in Platform:
    #         linkurl = 'reverse_url'
    #     pSupplier,pSupplierurl =format_urls(obj.SupplierPUrl1 if obj.SupplierPUrl1 else '')
    #     if 'can not formate' in pSupplier:
    #         pSupplierurl = 'Supplierurl'
    #     rt = u'反:<a href="%s" target="_blank" >%s:%s</a><br>供:<a href="%s" target="_blank" >%s:%s</a>'%(obj.SourceURL,Platform,linkurl,obj.SupplierPUrl1,pSupplier,pSupplierurl)
    #     return mark_safe(rt)
    # show_urls.short_description = u'链接信息'

    def show_CreateStaff(self,obj):
        rt = '%s <br> %s' % (obj.CreateStaffName, obj.CreateTime)
        return mark_safe(rt)
    show_CreateStaff.short_description = u'创建人/时间'

    list_display= ('id','show_CreateStaff','show_SourcePicPath','show_SourcePicPath2','SpecialSell','SpecialRemark','MainSKU','show_skulist','Name2','show_urls','show_oplog',)
    #list_display_links= ('SourcePicPath','SourcePicPath2',) #('SourcePicPath2','id','MainSKU','Name2','Keywords','Pricerange','SupplierPUrl1','SupplierPDes','UnitPrice','Weight','SpecialSell',)
    #search_fields=('id','MainSKU','Name2','StaffID','SourceURL',)
    #readonly_fields =  ALL_FIELDS_TUPLE
    #list_filter = ('UpdateTime',)
