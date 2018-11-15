# -*- coding: utf-8 -*-

from .t_product_Admin import *
class t_product_unique_ed_Admin(t_product_Admin):

    #save_on_top =True
    actions = ['develop_ing', 'to_recycle',]
    def develop_ing(self, request, queryset):
        for querysetid in queryset.all():
            #下一步
            obj = t_product_develop_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID = request.user.username
            obj.save()

            begin_t_product_oplog(request,querysetid.MainSKU,'KF',querysetid.Name2,querysetid.id)
            querysetid.delete()
    develop_ing.short_description = u'领用去开发'

    def to_recycle(self, request, queryset):
        super(t_product_unique_ed_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'



    list_display=('id','DYTime','DYStaffName','show_SourcePicPath','OrdersLast7Days','Keywords','Tags','ShelveDay','Pricerange','SpecialRemark','show_urls',)
    #list_display_links= None
    #search_fields=('id','MainSKU','StaffID','Keywords',)