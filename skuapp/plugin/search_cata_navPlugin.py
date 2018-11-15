# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.db import transaction,connection
from django.template import loader

class search_cata_navPlugin(BaseAdminPlugin):
    search_cata_navigator = False
    cata_of_platform = 'ebay'
    department_desc = 'others'
    
    def init_request(self, *args, **kwargs):
        return bool(self.search_cata_navigator)
        
    def block_search_cata_nav(self, context, nodes):               
        # toDO
        nodes.append(loader.render_to_string('search_cata_nav.html', {"cata_department_desc":self.department_desc, "cata_of_platform":self.cata_of_platform}))
          
    def get_media(self, media):
        media.add_js([self.static('searchnav/js/search.nav.ebay.index.js')])

        return media