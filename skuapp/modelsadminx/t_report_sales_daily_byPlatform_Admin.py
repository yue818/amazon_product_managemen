# -*- coding: utf-8 -*-

class t_report_sales_daily_byPlatform_Admin(object):
    salesshowlisting_flag = True
    sales_show_PlatformName_flag = True


    list_display = ('OrderDay', 'PlatformName', 'SalesVolume',)
    list_editable = None
    list_filter = None  # 过滤器list_filter
    search_fields = None  # 搜索功能
    readonly_fields = None  # 只读属性对象
    list_per_page = 50  # 页面显示数量
