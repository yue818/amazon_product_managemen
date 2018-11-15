# coding=utf-8


from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages

class plateform_distribution_navigation_Plugin(BaseAdminPlugin):
    plateform_distribution_navigation = False

    def init_request(self, *args, **kwargs):
        return bool(self.plateform_distribution_navigation)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]

        flag = 0
        result = {}

        WISH = [{'t_templet_public_wish_listing':{'flag':1, 'name':u'Listing'}},
                {'t_templet_wish_collection_box':{'flag':2, 'name':u'采集箱'}},
                {'t_templet_public_wish_review':{'flag':3, 'name':u'模板审核'}},
                {'t_templet_public_wish':{'flag':4, 'name':u'公共模板'}},
                {'t_templet_wish_wait_upload':{'flag':5, 'name':u'定时铺货'}},
                {'t_templet_wish_upload_review': {'flag': 6, 'name': u'铺货审核'}},
                {'t_templet_wish_upload_result':{'flag':7, 'name':u'铺货结果'}},
                {'t_product_image_modify/?_p_UpdateFlag__exact=1':{'flag':8, 'name':u'主图维护'}},
                {'t_product_image_modify':{'flag':9, 'name':u'全部主图'}}
        ]

        Aliexpress = [{'t_templet_aliexpress_collection_box':{'flag':1, 'name':u'采集箱'}},
                      {'t_templet_public_aliexpress':{'flag':2, 'name':u'公共模板'}},
                      {'t_templet_aliexpress_wait_upload':{'flag':3, 'name':u'待铺货'}},
                      {'t_aliexpress_distribution_shop': {'flag': 4, 'name': u'账号群设置'}},

        ]

        JOOM = [
            {'t_templet_public_joom_listing': {'flag': 1, 'name': u'Listing'}},
            {'t_templet_joom_collection_box': {'flag': 2, 'name': u'采集箱'}},
            {'t_templet_public_joom': {'flag': 3, 'name': u'公共模板'}},
            {'t_templet_joom_wait_upload': {'flag': 4, 'name': u'待铺货'}},
        ]
        
        eBay = [{'t_templet_public_ebay_listing': {'flag': 1, 'name': u'Listing'}},
                {'t_templet_ebay_collection_box': {'flag': 2, 'name': u'采集箱'}},
                {'t_templet_public_ebay': {'flag': 3, 'name': u'公共模板'}},
                {'t_templet_ebay_wait_upload': {'flag': 4, 'name': u'定时铺货'}},
                {'t_templet_ebay_upload_result': {'flag': 5, 'name': u'铺货结果'}},
                {'t_ebay_product_image_modify': {'flag': 6, 'name': u'主图维护'}}
        ]
        
        plateform = [WISH, Aliexpress, JOOM, eBay]

        for each_plate in plateform:
            for each_model in each_plate:
                for k, v in each_model.items():
                    if k in sourceURL:
                        result = each_plate
                        flag = v['flag']
                        break
                if flag != 0:
                    break
            if flag != 0:
                break

        nodes.append(loader.render_to_string('plateform_distribution_navigation.html', {'flag':flag, 'result':result}))