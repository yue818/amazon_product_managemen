# coding=utf-8


class t_wish_distribution_sales_statistics_total_Admin(object):
    wish_order_sales_total_chart = True

    list_display = ('a_date', 'a_execute_success_num', 'a_approved_num', 'a_approved_percent', 'a_out_order_num',
                    'a_out_order_percent', 'a_sales_num')

    list_display_links = ('id')

    list_per_page = 14