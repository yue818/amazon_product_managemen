# coding=utf-8


from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages

class salesshowlisting_Plugin(BaseAdminPlugin):
    salesshowlisting_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.salesshowlisting_flag)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]

        if 't_report_sales_daily_byplatform' in sourceURL:
            flag = 1
        elif 't_report_sales_daily_byshopname' in sourceURL:
            flag = 2
        elif 't_report_sales_daily_byproductid' in sourceURL:
            flag = 3
        elif 't_report_sales_daily_bymainsku' in sourceURL:
            flag = 5
        elif 't_report_sales_daily_bysku' in sourceURL:
            flag = 6
        elif 't_report_sales_daily' in sourceURL:
            flag = 4
        else:
            flag = 0
        nodes.append(loader.render_to_string('salesshowlisting.html', {'flag':flag}))