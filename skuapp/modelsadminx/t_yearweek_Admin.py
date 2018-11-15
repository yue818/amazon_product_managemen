# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class t_yearweek_Admin(object):

    list_display=('yearweek','kf_allcount','kf_avg','kf_number','jzl_allcount','jzl_avg','jzl_number','id')

    data_charts = {
        "总数": {'title': u"总数", "x-field": "yearweek", "y-field": ( "kf_allcount","jzl_allcount"), "order": ('yearweek',)},
        "人数": {'title': u"人数", "x-field": "yearweek", "y-field": ( "kf_number","jzl_number"), "order": ('yearweek',)},
        "平均数": {'title': u"平均数", "x-field": "yearweek", "y-field": ('kf_avg','jzl_avg',), "order": ('yearweek',)}
    }
