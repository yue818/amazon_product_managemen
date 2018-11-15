# coding=utf-8

from xadmin.views import BaseAdminPlugin
from django.template import loader


class wish_distribution_listing_sku_query_Plugin(BaseAdminPlugin):
    listing_sku_query = False

    def init_request(self, *args, **kwargs):
        return bool(self.listing_sku_query)

    def block_search_cata_nav(self, context, nodes):
        mysku = self.request.GET.get('mysku', '')
        if mysku == '':
            pass
        else:
            skuList = mysku.split(',')
            del skuList[0]
            mysku = ','.join(skuList)

        rt = u'<form action="/Project/admin/skuapp/t_templet_public_wish_listing/">'
        rt = u'%s<textarea name="mysku" style="width:1400px;height:50px;border:solid 1px;">%s</textarea>' % (rt, mysku)
        rt =u'%s<input type="submit" class="btn btn-primary" value="下一个"></form></div>' % rt
        nodes.append(loader.render_to_string('SKU.html', {'rt':rt}))