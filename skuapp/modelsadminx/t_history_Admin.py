# -*- coding: utf-8 -*-
class t_history_Admin(object):

    list_display   =('username','user_url','url_time','url_names','user_urls')
    list_editable  = ('username','user_url','url_time','url_names','user_urls')
    search_fields   =('username','user_url','url_time','url_names','user_urls')
    list_filter   =('username','user_url','url_time','url_names','user_urls')

