# coding=utf-8


class t_wish_distribution_result_statistics_everyday_Admin(object):

    list_display = ('d_date', 'd_collect_num', 'd_make_templet_num', 'd_to_wait_upload_num', 'd_post_upload_num',
                    'd_to_upload_num', 'd_success_upload_num', 'd_wait_upload_num', 'd_shop_num', 'd_shop_average_num',
                    'd_templet_average_num', 'd_today_success_num')

    list_display_links = ('id')

    list_per_page = 14