# coding=utf-8


"""
WISH 铺货统计
"""

from __future__ import  division
from django.db import connection
import datetime


class WishDistributionStatistics(object):

    def __init__(self):
        # 采集数
        self.collect_num_sql = 'SELECT COUNT(id), LEFT(CreateTime,10) from t_templet_wish_collection_box GROUP BY LEFT(CreateTime,10)'
        # 制作模板数
        self.make_templet_num_sql = 'SELECT COUNT(id), LEFT(CreateTime,10) from t_templet_public_wish GROUP BY LEFT(CreateTime,10)'
        # 转到待铺货数
        self.to_wait_upload_num_sql = 'SELECT COUNT(id), LEFT(CreateTime,10) from t_templet_wish_wait_upload GROUP BY LEFT(CreateTime,10)'
        # 提交铺货模板数
        self.post_upload_num_sql = 'SELECT COUNT(id), LEFT(PostTime,10) from t_templet_wish_wait_upload GROUP BY LEFT(PostTime,10)'

        # 定时铺货数
        self.upload_num_sql = 'SELECT COUNT(id), LEFT(InsertTime,10) from t_templet_wish_upload_result GROUP BY LEFT(InsertTime,10)'
        # 铺货成功数
        self.success_upload_num_sql = 'SELECT COUNT(id), LEFT(InsertTime,10) from t_templet_wish_upload_result WHERE `Status`="SUCCESS" GROUP BY LEFT(InsertTime,10)'
        # 铺货待执行数
        self.wait_upload_num_sql = 'SELECT COUNT(id), LEFT(InsertTime,10) from t_templet_wish_upload_result WHERE `Status`="ING" GROUP BY LEFT(InsertTime,10)'
        # 铺货店铺数
        self.shop_num_sql = 'SELECT COUNT(DISTINCT ShopName), LEFT(InsertTime,10) from t_templet_wish_upload_result GROUP BY LEFT(InsertTime,10)'
        # 今日铺货成功数
        self.today_success_num_sql = 'SELECT COUNT(id), LEFT(Schedule,10) from t_templet_wish_upload_result WHERE `Status`="SUCCESS" GROUP BY LEFT(Schedule,10)'

        # 出单数
        self.out_order_num_sql = 'select COUNT(orderid),LEFT(orderdate, 10) from t_order where ProductID in (select ProductID from t_online_info_wish where DataSources="UPLOAD") GROUP BY LEFT(orderdate, 10)'
        # 出单链接数
        self.out_order_link_num_sql = 'select COUNT(DISTINCT ProductID),LEFT(orderdate, 10) from t_order where ProductID in (select ProductID from t_online_info_wish where DataSources="UPLOAD") GROUP BY LEFT(orderdate, 10)'
        # 审核通过数
        self.aproved_num_sql = 'SELECT COUNT(DISTINCT ProductID), LEFT(DateUploaded,10) from t_online_info_wish WHERE DataSources = "UPLOAD" and ReviewState="approved" and `Status`="Enabled" GROUP BY LEFT(DateUploaded,10)'
        # 销售额
        self.sales_num_sql = "SELECT sum(sold), c.OrderDate from (SELECT (substring_index(a.Price,'$',-1)+substring_index(a.Shipping,'$',-1))*a.Quantity as sold, a.ProductID,LEFT(a.OrderDate,10) as OrderDate from t_order a, (SELECT ProductID, left(DateUploaded,10) as DateUploaded from t_online_info_wish WHERE DataSources = 'UPLOAD') b WHERE a.ProductID = b.ProductID) c GROUP BY c.OrderDate"


    def get_result_single_dict(self, sql, cur):
        """
        获取 key为日期，val为int的数据
        :return: key为日期，val为int数据
        """

        infos_dict = {}

        cur.execute(sql)
        infos = cur.fetchall()
        for info in infos:
            num = info[0]
            date = info[1]
            infos_dict[date] = num
        return infos_dict


    def get_date_list(self):
        """
        日期列表
        """
        date_list = []
        end_date = '2017-11-23'
        today = datetime.date.today()
        one_day = datetime.timedelta(days=1)

        while str(today) > end_date:
            today = today - one_day
            date_list.append(str(today))
        date_list.reverse()
        return date_list


    def get_average(self, num_1, num_2):
        """
        求平均数
        :param num_1: 被除数
        :param num_2: 除数
        :return: 商
        """
        result = 0
        try:
            result = num_1 / num_2
        except:
            pass
        return result


    def get_percent(self, num_1, num_2):
        """
        求百分比
        :param num_1:
        :param num_2:
        :return:
        """
        result = '%.2f%%' % 0
        try:
            result = '%.2f%%' % (float(num_1) / int(num_2) * 100)
        except:
            pass
        return result


    def get_week(self, date):
        date_list = list(str(date).split('-'))
        week_tuple = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2])).isocalendar()
        week_int = int(str(week_tuple[0]) + str(week_tuple[1]).zfill(2))
        return week_int


    def handle_data(self):
        """
        处理插入到表中所需的数据
        :return: 数据集
        """
        result_params = []
        sales_params = []
        total_params = []

        cur = connection.cursor()

        # 获取查询结果集
        collect_num_dict = self.get_result_single_dict(self.collect_num_sql, cur)
        make_templet_num_dict = self.get_result_single_dict(self.make_templet_num_sql, cur)
        to_wait_upload_num_dict = self.get_result_single_dict(self.to_wait_upload_num_sql, cur)
        post_upload_num_dict = self.get_result_single_dict(self.post_upload_num_sql, cur)

        upload_num_dict = self.get_result_single_dict(self.upload_num_sql, cur)
        success_upload_num_dict = self.get_result_single_dict(self.success_upload_num_sql, cur)
        wait_upload_num_dict = self.get_result_single_dict(self.wait_upload_num_sql, cur)
        shop_num_dict = self.get_result_single_dict(self.shop_num_sql, cur)
        today_success_num_dict = self.get_result_single_dict(self.today_success_num_sql, cur)

        out_order_num_dict = self.get_result_single_dict(self.out_order_num_sql, cur)
        out_order_link_num_dict = self.get_result_single_dict(self.out_order_link_num_sql, cur)
        aproved_num_dict = self.get_result_single_dict(self.aproved_num_sql, cur)
        sales_num_dict = self.get_result_single_dict(self.sales_num_sql, cur)

        cur.close()

        date_list = self.get_date_list()

        # 累计数据
        execute_success_total = 0
        out_order_link_total = 0
        approved_total = 0
        out_order_total = 0
        sales_total = 0

        for date in date_list:

            # 每日铺货统计 MODEL
            collect_num = collect_num_dict.get(date, 0)
            make_templet_num = make_templet_num_dict.get(date, 0)
            to_wait_upload_num = to_wait_upload_num_dict.get(date, 0)
            post_upload_num = post_upload_num_dict.get(date, 0)

            upload_num = upload_num_dict.get(date, 0)
            success_upload_num = success_upload_num_dict.get(date, 0)
            wait_upload_num = wait_upload_num_dict.get(date, 0)
            shop_num = shop_num_dict.get(date, 0)
            today_success_num = today_success_num_dict.get(date, 0)

            shop_average_num = self.get_average(success_upload_num, shop_num)
            templet_average_num = self.get_average(success_upload_num, post_upload_num)

            result_param_tuple = (0, date, collect_num, make_templet_num, to_wait_upload_num, post_upload_num, upload_num,
                           success_upload_num, wait_upload_num, shop_num, shop_average_num, templet_average_num,today_success_num)
            result_params.append(result_param_tuple)

            # 每日销售统计 MODEL
            out_order_link_num = out_order_link_num_dict.get(date, 0)
            out_order_num = out_order_num_dict.get(date, 0)
            aproved_num = aproved_num_dict.get(date, 0)
            sales_num = sales_num_dict.get(date, 0)
            week_int = self.get_week(date)

            sales_param_tuple = (0, date, out_order_num, aproved_num, sales_num, week_int)
            sales_params.append(sales_param_tuple)

            # 销售数据累计
            execute_success_total += success_upload_num
            out_order_link_total += out_order_link_num
            approved_total += aproved_num
            approved_percent = self.get_percent(approved_total, execute_success_total)
            out_order_total += out_order_num
            out_order_percent = self.get_percent(out_order_link_total, execute_success_total)
            sales_total += sales_num

            total_param = (0, date, execute_success_total, approved_total, approved_percent, out_order_total,
                           out_order_percent, sales_total)
            total_params.append(total_param)

        return result_params, sales_params, total_params


    def insert_into_table(self, result_params, sales_params, total_params):
        """
        将结果插入到表中
        :param param: 数据集
        """
        cur = connection.cursor()

        # 每日铺货统计
        for result_param in result_params:
            delete_sql_1 = 'delete from t_wish_distribution_result_statistics_everyday where d_date=\"%s\" ' % result_param[1]
            insert_sql_1 = 'insert into t_wish_distribution_result_statistics_everyday VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

            cur.execute(delete_sql_1)
            cur.execute(insert_sql_1, result_param)

        # 每日销售统计
        for sales_param in sales_params:
            delete_sql_2 = 'delete from t_wish_distribution_sales_statistics_everyday where s_date=\"%s\" ' % sales_param[1]
            insert_sql_2 = 'insert into t_wish_distribution_sales_statistics_everyday VALUES (%s,%s,%s,%s,%s,%s)'

            cur.execute(delete_sql_2)
            cur.execute(insert_sql_2, sales_param)

        # 销售数据累计
        date_list = []
        select_sql = 'select a_date from t_wish_distribution_sales_statistics_total'
        cur.execute(select_sql)
        date_infos = cur.fetchall()
        for date_info in date_infos:
            date_list.append(str(date_info[0]))

        for total_param in total_params:
             if total_param[1] not in date_list:
                insert_sql_3 = 'insert into t_wish_distribution_sales_statistics_total VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
                cur.execute(insert_sql_3, total_param)
        cur.execute("commit;")
        cur.close()