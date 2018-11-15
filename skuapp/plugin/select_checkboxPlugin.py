# coding=utf-8

from xadmin.views import BaseAdminPlugin

class select_checkboxPlugin(BaseAdminPlugin):
    select_checkbox_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.select_checkbox_flag)

    def get_media(self,media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.select.checkbox.js')])
        return media