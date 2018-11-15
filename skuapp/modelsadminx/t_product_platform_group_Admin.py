# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class t_product_platform_group_Admin(object):
    list_display=('id','PlatformName','Date','QNumber','YNumber','RefreshTime',)
    #readonly_fields = ('id',)
    list_display_links = list_display

    search_fields=('id','PlatformName','QNumber','YNumber',)
    list_filter = ('PlatformName','RefreshTime','QNumber','YNumber','Date',)
    data_charts = {
        "平台调研数": {'title': u"平台调研数", "x-field": "Date", "y-field": ("QNumber","YNumber"), "order": ('Date',)}
    }
