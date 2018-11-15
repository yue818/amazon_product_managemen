# coding=utf-8


from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages

class wish_distribution_navigation_Plugin(BaseAdminPlugin):
    wish_distribution_navigation = False

    def init_request(self, *args, **kwargs):
        return bool(self.wish_distribution_navigation)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]

        if 't_templet_public_wish_listing' in sourceURL:
            flag = 1
        elif 't_templet_wish_collection_box' in sourceURL:
            flag = 2
        elif 't_templet_public_wish' in sourceURL:
            flag = 3
        elif 't_templet_wish_wait_upload' in sourceURL:
            flag = 4
        elif 't_templet_wish_upload_result' in sourceURL:
            flag = 5
        elif 't_product_image_modify' in sourceURL:
            flag = 6
        else:
            flag = 0
        nodes.append(loader.render_to_string('wish_distribution_navigation.html', {'flag':flag}))