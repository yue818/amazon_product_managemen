# -*- coding: utf-8 -*-

#15)    调研历史表 t_product_survey_history
class t_product_survey_history_Admin(object):
    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.pid).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_mainsku(self,obj) :
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.pid,StepID='JZL')
        if t_product_oplog_objs.count() > 0 :
            rt = u'%s'%(t_product_oplog_objs[0].MainSKU)
            return rt
    show_mainsku.short_description = u'主SKU'

    def show_SourcePicPath(self,obj) :
        rt =  '<img src="%s"  width="80" height="80"  alt = "%s"  title="%s"  />  '%(obj.SourcePicPath,obj.SourcePicPath,obj.SourcePicPath)
        return mark_safe(rt)
    show_SourcePicPath.short_description = u'调研图'

    def show_SourcePicPath2(self,obj) :
        rt =  '<img src="%s"  width="80" height="80"  alt = "%s"  title="%s"  />  '%(obj.SourcePicPath2,obj.SourcePicPath2,obj.SourcePicPath2)
        return mark_safe(rt)
    show_SourcePicPath2.short_description = u'供货商图'

    def show_urls(self,obj) :
        rt = u'反向: %s<br>供货商: %s,'%(obj.SourceURL,obj.SupplierPUrl1)
        return mark_safe(rt)
    show_urls.short_description = u'链接信息'

    list_per_page=50
    list_display=('id','show_SourcePicPath','show_SourcePicPath2','UpdateTime','StaffID','StaffName','show_mainsku','show_oplog','show_urls','pid',)

    list_filter = ('UpdateTime','StaffID','StaffName',)
    search_fields=('id','pid','StaffID','StaffName',)