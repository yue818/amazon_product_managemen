# -*- coding: utf-8 -*-
class t_sys_shopdef_Admin(object):
    list_display=('id','ShopID','ShopDesc','StaffID','ShopkeeperName','CreateTime','UpdateTime',)
    readonly_fields = ('id',)
    list_display_links = list_display

    search_fields=('ShopID','ShopDesc','StaffID','ShopkeeperName',)
    list_filter = ('ShopkeeperName','CreateTime','UpdateTime',)
    fieldsets = (
        (u'操作记录', {'fields': ('id','ShopID','ShopDesc','CreateTime',)}),
    )

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.StaffID = request.user.username
        obj.ShopkeeperName=request.user.first_name
        obj.save()

    def get_list_queryset(self):
        request = self.request
        if request.user.is_superuser:
            qs = super(t_sys_shopdef_Admin, self).get_list_queryset()
            return qs
        qs = super(t_sys_shopdef_Admin, self).get_list_queryset().filter(StaffID=request.user.username)
        return qs
