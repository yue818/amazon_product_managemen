# -*- coding: utf-8 -*
from django.utils.safestring import mark_safe
from skuapp.table.t_config_apiurl_asin_kf import *
from skuapp.table.t_product_survey_ing import *
from skuapp.table.t_product_wait_enquiry import *
from skuapp.table.t_product_develop_ing import *
from datetime import datetime


class t_config_apiurl_asin_kfAdmin(object):
    #actions =  ['to_t_product_wait_enquiry','to_t_product_develop_ing','do_YNDone']
    actions =  ['do_YNDone',]

    def get_id(self):
        t_product_survey_ing_obj = t_product_survey_ing()
        t_product_survey_ing_obj.save()
        temp_id=t_product_survey_ing_obj.id
        t_product_survey_ing_obj.delete()
        return temp_id

    list_per_page=10
    def show_SmallImage(self,obj) :
        url =u'%s'%(obj.SmallImage)
        rt =  '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  '%(url,url,url)
        return mark_safe(rt)
    show_SmallImage.short_description = u'图片'


    def show_asin_urls(self,obj) :
        rt = ''
        asin_objs = t_config_apiurl_asin_kf.objects.filter(id=obj.id)[0:1]
        for asin_obj in asin_objs:
            if asin_obj.URL.find('amazon.') != -1:
                rt_url = u'https://www.amazon.com/dp/%s'%asin_obj.ASIN
            if asin_obj.URL.find('ebay.') != -1:
                rt_url = u'http://www.ebay.com/itm/%s'%asin_obj.ASIN
            rt = u'%s<a href="%s"target="_blank">%s</a>'%(rt,rt_url,asin_obj.ASIN)

        return mark_safe(rt)
    show_asin_urls.short_description = u'ASIN'

    list_display   =('id','DealName','DealTime','show_SmallImage','show_asin_urls','URL','Status','Title','Serial','ListPrice','RefreshTime','Feature','Error','YNDone','Remarks','group1','group2','group3','group4','group5')
    list_editable  = ('YNDone','Remarks',)
    search_fields   =('DealName','ASIN','URL','Status','Feature','ProductGroup','Error','YNDone','Remarks','group1','group2','group3','group4','group5')
    list_filter   =('URL','DealName','DealTime','Status','RefreshTime','Feature','ProductGroup','Serial','YNDone','Remarks','group1','group2','group3','group4','group5')
    readonly_fields =('id','DealName','DealTime','SmallImage','ProductGroup','ASIN','URL','Status','Title','Brand','ListPrice','RefreshTime','Feature','Error','Serial','YNDone','Remarks','group1','group2','group3','group4','group5')
    list_display_links = ('id',)

    def to_t_product_wait_enquiry(self, request, queryset):
        for querysetid in queryset.all():
            #到1.05 t_product_wait_enquiry已开发待询价
            t_product_wait_enquiry_obj = t_product_wait_enquiry()
            #obj = t_product_build_ing()
            #obj.__dict__ = querysetid.__dict__
            t_product_wait_enquiry_obj.id = self.get_id()
            t_product_wait_enquiry_obj.MainSKU = ''
            t_product_wait_enquiry_obj.CreateTime = datetime.now()
            t_product_wait_enquiry_obj.CreateStaffName = request.user.first_name
            t_product_wait_enquiry_obj.StaffID= request.user.username
            t_product_wait_enquiry_obj.SourcePicPath =querysetid.SmallImage
            
            if querysetid.URL.find('amazon.') != -1:
                t_product_wait_enquiry_obj.SourceURL = u'https://www.amazon.com/dp/%s'%querysetid.ASIN
            if querysetid.URL.find('ebay.') != -1:
                t_product_wait_enquiry_obj.SourceURL = u'http://www.ebay.com/itm/%s'%querysetid.ASIN
            
            t_product_wait_enquiry_obj.Name =querysetid.Title
            t_product_wait_enquiry_obj.Pricerange=querysetid.ListPrice
            t_product_wait_enquiry_obj.SpecialRemark = 'ASIN=%s'%(querysetid.ASIN)
            t_product_wait_enquiry_obj.save()

            querysetid.YNDone= '1'
            querysetid.DealName = request.user.first_name
            querysetid.DealTime =datetime.now()
            querysetid.Remarks =u'转到-已开发待询价'
            querysetid.save()
    to_t_product_wait_enquiry.short_description = u'转到-已开发待询价'


    def to_t_product_develop_ing(self, request, queryset):
        for querysetid in queryset.all():
            #到 t_product_develop_ing 正在开发
            t_product_develop_ing_objs = t_product_develop_ing()
            #obj = t_product_build_ing()
            #obj.__dict__ = querysetid.__dict__
            t_product_develop_ing_objs.id = self.get_id()
            t_product_develop_ing_objs.MainSKU = ''
            t_product_develop_ing_objs.CreateTime = datetime.now()
            t_product_develop_ing_objs.CreateStaffName = request.user.first_name
            t_product_develop_ing_objs.StaffID= request.user.username
            t_product_develop_ing_objs.SourcePicPath =querysetid.SmallImage
            
            if querysetid.URL.find('amazon.') != -1:
                t_product_develop_ing_objs.SourceURL = u'https://www.amazon.com/dp/%s'%querysetid.ASIN
            if querysetid.URL.find('ebay.') != -1:
                t_product_develop_ing_objs.SourceURL = u'http://www.ebay.com/itm/%s'%querysetid.ASIN
            
            t_product_develop_ing_objs.Name =querysetid.Title
            t_product_develop_ing_objs.Pricerange=querysetid.ListPrice
            t_product_develop_ing_objs.SpecialRemark = 'ASIN=%s'%(querysetid.ASIN)
            t_product_develop_ing_objs.save()

            querysetid.YNDone= '1'
            querysetid.DealName = request.user.first_name
            querysetid.DealTime =datetime.now()
            querysetid.Remarks =u'转到-正在开发'
            querysetid.save()
    to_t_product_develop_ing.short_description = u'转到-正在开发'



    def do_YNDone(self, request, queryset):
        for querysetid in queryset.all():
            if querysetid.YNDone != '1':
                t_config_apiurl_asin_kf.objects.filter(id = querysetid.id).update(YNDone =u'1')

    do_YNDone.short_description = u'全部已做过'


    def get_list_queryset(self):
        request = self.request
        qs = super(t_config_apiurl_asin_kfAdmin, self).get_list_queryset()
        if request.user.is_superuser:
            return qs
        return qs.filter(DealName = request.user.first_name)
