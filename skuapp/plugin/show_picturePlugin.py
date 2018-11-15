# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
#增加图片
class show_picturePlugin(BaseAdminPlugin):
    show_pic = False
    def init_request(self, *args, **kwargs):
        return bool(self.show_pic)
    def block_before_fieldsets(self, context, nodes):
        if context['original'] is None :
            nodes.append(loader.render_to_string('research_and_supplier.html',
                                                 {'SourcePicPath': "",
                                                  'SourcePicPath2': ""}))
            return
        nodes.append(loader.render_to_string('research_and_supplier.html', {'SourcePicPath': context['original'].SourcePicPath, 'SourcePicPath2': context['original'].SourcePicPath2}))
