# -*- coding: utf-8 -*-
class t_sys_platform_role_Admin(object):
    list_display=('id','StaffID','PlatformName','StaffName',)
    readonly_fields = ('id','StaffID','StaffName',)
    fieldsets = (
            (u'设置平台角色', {'fields': ('id','StaffID','StaffName','PlatformName',)}),
        )

    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        messages.error(request,  'obj :  %s %s %s'%(obj.StaffID,obj.PlatformName, obj.StaffName) )
        #self.message_user(request,  'form :  %s %s %s'%(form.StaffID,form.PlatformName, form.StaffName) )
        t_sys_platform_role_objs = t_sys_platform_role.objects.filter(StaffID = request.user.username,PlatformName=obj.PlatformName)
        if  t_sys_platform_role_objs.count() <=0:

            obj.StaffID = request.user.username
            obj.StaffName = request.user.first_name
            obj.save()
            self.message_user(request,  u'增加成功：%s %s %s'%(obj.StaffID,obj.PlatformName, obj.StaffName) )
        else:
            messages.error(request,  '已存在重复了：%s %s %s'%(t_sys_platform_role_objs[0].StaffID,t_sys_platform_role_objs[0].PlatformName, t_sys_platform_role_objs[0].StaffName) )