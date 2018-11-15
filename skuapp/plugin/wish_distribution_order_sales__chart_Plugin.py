# coding=utf-8


from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_wish_distribution_sales_statistics_everyday import t_wish_distribution_sales_statistics_everyday as sales_statistics
from skuapp.table.t_wish_distribution_sales_statistics_total import t_wish_distribution_sales_statistics_total as sales_total_statistics
from django.db import connection
import json
from brick.function.week_and_date import *


class wish_distribution_order_sales__chart_Plugin(BaseAdminPlugin):

    wish_order_sales_chart = False

    def init_request(self, *args, **kwargs):
        return bool(self.wish_order_sales_chart)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]
        date_data = []
        order_data = []
        sales_data = []

        if 'week' in sourceURL:
            title = u'每周订单和销售额'
            flag = 2
            cur = connection.cursor()
            sql = 'select s_week, sum(s_out_order_num), sum(s_sales_num) from t_wish_distribution_sales_statistics_everyday GROUP BY s_week ORDER BY s_week desc LIMIT 8'
            cur.execute(sql)
            infos = cur.fetchall()
            cur.close()
            for info in infos:
                week_num = str(info[0])
                start_date, end_date = get_day_range(week_num)
                week_info = start_date.replace('-', '/') + '-' + end_date.replace('-', '/')
                date_data.append(week_info)
                order_data.append(int(info[1]))
                sales_data.append(int(info[2]))

        else:
            title = u'每日订单和销售额'
            flag = 1
            sales_statistics_objs = sales_statistics.objects.all().order_by('-s_date')[0:14]
            if sales_statistics_objs.exists():
                for sales_statistics_obj in sales_statistics_objs:
                    day =str(sales_statistics_obj.s_date)
                    date_data.append(day)
                    order_data.append(int(sales_statistics_obj.s_out_order_num))
                    sales_data.append(int(sales_statistics_obj.s_sales_num))

        date_data.reverse()
        order_data.reverse()
        sales_data.reverse()

        nodes.append(loader.render_to_string('wish_distribution_order_sales__chart.html',
                                             {'flag': flag, 'title':title, 'date_data':json.dumps(date_data),
                                              'order_data':order_data, 'sales_data':sales_data}))


class wish_distribution_order_sales_total__chart_Plugin(BaseAdminPlugin):

    wish_order_sales_total_chart = False

    def init_request(self, *args, **kwargs):
        return bool(self.wish_order_sales_total_chart)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]
        date_data = []
        approved_data = []
        order_data = []
        sales_data = []

        title = u'累计销售统计'
        flag = 1
        sales_total_statistics_objs = sales_total_statistics.objects.all().order_by('-a_date')[0:30]
        if sales_total_statistics_objs.exists():
            for sales_total_statistics_obj in sales_total_statistics_objs:
                day =str(sales_total_statistics_obj.a_date)
                date_data.append(int(day.replace('-', '')))
                order_data.append(int(sales_total_statistics_obj.a_out_order_num))
                sales_data.append(int(sales_total_statistics_obj.a_sales_num))
                approved_data.append(int(sales_total_statistics_obj.a_approved_num))

        date_data.reverse()
        order_data.reverse()
        sales_data.reverse()
        approved_data.reverse()

        context = {
            'flag': flag,
            'title': title,
            'date_data': date_data,
            'order_data': order_data,
            'sales_data': sales_data,
            'approved_data': approved_data
        }

        nodes.append(loader.render_to_string('wish_distribution_order_sales_total__chart.html', context))


