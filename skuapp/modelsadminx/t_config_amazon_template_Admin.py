#-*-coding:utf-8-*-
from datetime import datetime

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_config_amazon_template_Admin.py
 @time: 2018/7/25 15:28
"""   
class t_config_amazon_template_Admin(object):
    list_per_page=20
    amazon_site_left_menu_tree_flag = True

    list_display = ('shopName', 'template_name', 'freight', )

    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.CreateTime = datetime.now()
        obj.CreateName = request.user.first_name
        obj.save()

    def get_list_queryset(self,):
        """显示可显示的，自己本人的"""
        request = self.request
        qs = super(t_config_amazon_template_Admin, self).get_list_queryset()
        if request.user.is_superuser:
            pass
        else:
            qs = qs.filter(CreateName = request.user.first_name)
        return qs