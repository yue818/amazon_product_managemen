# -*- coding: utf-8 -*-
from .t_product_Admin import *
class t_product_survey_ed_Admin(t_product_Admin):

    #save_on_top =True
    #actions = ['unique_ed', 'to_repeats','pass','notpass',]
    actions = ['to_pass','to_notpass',]
    def to_pass(self, request, queryset):
        cursor = connection.cursor() # 得到处理的游标对象
        for querysetid in queryset.all():
            obj = t_product_unique_ed()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name

            obj.DYSHTime = datetime.now()
            obj.DYSHStaffName = request.user.first_name

            obj.save()

            end_t_product_oplog(request,querysetid.MainSKU,'DYSH',querysetid.Name2,querysetid.id)

            querysetid.delete()
    to_pass.short_description = u'审核通过'

    def to_notpass(self, request, queryset):
        self.to_recycle(request, queryset)
    to_notpass.short_description = u'审核不通过'

    # def show_urls(self,obj) :
    #     rt = u'反向:<a href="%s" target="_blank" >%s</a><br>供货商:<a href="%s" target="_blank" >%s</a>'%(obj.SourceURL,obj.SourceURL,obj.SupplierPUrl1,obj.SupplierPUrl1)
    #     return mark_safe(rt)
    # show_urls.short_description = u'链接信息'

    list_display=('id','DYTime','DYStaffName','show_SourcePicPath','OrdersLast7Days','Pricerange','ShelveDay','Keywords','SpecialRemark','show_urls',)
    #list_display_links=('SourcePicPath',)
    #search_fields=('id','MainSKU','StaffID','Keywords','Keywords2',)
    #list_filter = ('UpdateTime','StaffID',)
    #list_editable=('OrdersLast7Days','Keywords','Keywords2','ShelveDay','Pricerange','SpecialRemark',)
    list_editable=('OrdersLast7Days','Keywords','SpecialRemark','ShelveDay','Pricerange',)
    #list_editable=( 'SpecialRemark', )
