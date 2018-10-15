#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: site_left_menu_plugin_wish.py
 @time: 2018-03-07 9:25
"""
from django.template import loader
from xadmin.views import BaseAdminPlugin

class site_left_menu_Plugin_wish(BaseAdminPlugin):
    site_left_menu_flag_wish = False

    def init_request(self, *args, **kwargs):
        return bool(self.site_left_menu_flag_wish)

    def block_left_navbar(self, context, nodes):
        # sourceURL = str(context['request']).split("'")[1]
        # title_list = [{'title': u'平台商品', 'selected': '0'}]
        # test_list = [
        #     {'url': '/Project/admin/storeapp/t_online_info_wish_store/', 'value': u'全部',
        #         'title': u'平台商品', 'selected': '0'},
        #     {'url': '/Project/admin/storeapp/t_online_info_wish_store/?status=online', 'value': u'在线',
        #         'title': u'平台商品', 'selected': '0'},
        #     {'url': '/Project/admin/storeapp/t_online_info_wish_store/?reviewState=pending', 'value': u'待审核',
        #         'title': u'平台商品', 'selected': '0'},
        #     {'url': '/Project/admin/storeapp/t_online_info_wish_store/?reviewState=rejected', 'value': u'被拒绝',
        #         'title': u'平台商品', 'selected': '0'},
        #  ]

        reviewState = self.request.GET.get('reviewState','')
        pathlist = []
        if reviewState:
            path = self.request.get_full_path().split('?')[-1]
            for pa in path.split('&'):
                if pa.find('reviewState') == -1:
                    pathlist.append(pa)

        join = ''
        if pathlist:
            join = '&'.join(pathlist) + '&'

        paramsList = [
            {
                'title':u'全部','href':self.request.path,'flag':'',
                'branch':[
                    {'title':u'已审核','href':self.request.path + '?' + join + 'reviewState=approved','flag':'approved'},
                    {'title':u'待审核','href':self.request.path + '?' + join + 'reviewState=pending','flag':'pending'},
                    {'title':u'被拒绝','href':self.request.path + '?' + join + 'reviewState=rejected','flag':'rejected'},
                ]
            },
        ]

        nodes.append(loader.render_to_string('site_left_menu_Plugin_wish.html',{'paramsList': paramsList,'reviewState':reviewState}))

