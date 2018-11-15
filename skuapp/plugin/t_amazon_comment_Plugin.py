# coding=utf-8


from xadmin.views import BaseAdminPlugin
from django.template import loader
import json
from django.contrib import messages

class t_amazon_comment_Plugin(BaseAdminPlugin):
    t_amazon_comment = False

    def init_request(self, *args, **kwargs):
        return bool(self.t_amazon_comment)

    # def get_media(self, media):
    #     media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
    #     return media

    def block_search_cata_nav(self, context, nodes):
        nodes.append(loader.render_to_string('t_amazon_comment.html'))