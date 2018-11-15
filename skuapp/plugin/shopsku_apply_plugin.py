#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: shopsku_apply_plugin.py
 @time: 2018-02-22 10:13
"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from skuapp.table.t_sys_department_staff import t_sys_department_staff
import json

class shopsku_apply_plugin(BaseAdminPlugin):
    shopsku_apply = False

    def init_request(self, *args, **kwargs):
        return bool(self.shopsku_apply)

    def block_before_fieldsets(self, context, nodes):
        shoplist = []
        t_sys_department_staff_objs = t_sys_department_staff.objects.filter(StaffID=self.request.user.username)
        if t_sys_department_staff_objs.exists():
            DepartmentID = t_sys_department_staff_objs[0].DepartmentID
            objs = t_store_configuration_file.objects.filter(Department=DepartmentID)
            for obj in objs:
                shoplist.append(obj.ShopName)
        else :
            objs = t_store_configuration_file.objects.filter()
            for obj in objs:
                shoplist.append(obj.ShopName)
        nodes.append(loader.render_to_string('shopsku_apply_plugin_shopname.html',{'shoplist':json.dumps(shoplist)}))