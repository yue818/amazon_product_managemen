# coding=utf-8


class t_wish_distribution_sales_statistics_everyday_Admin(object):
    wish_order_sales_chart = True

    list_display = ('s_date', 's_out_order_num', 's_sales_num')

    list_display_links = ('id')

    list_per_page = 14