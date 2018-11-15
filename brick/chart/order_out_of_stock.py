# coding=utf-8

from django.db import connection
import xlrd


def read_excel(file_obj, plateform, now_time, first_name):
    """
    读取EXCEL文件内的信息
    :param file_obj: 缺货订单导入EXCEL文件对象
    :return: 返回EXCEL文件内的信息
    """
    data = xlrd.open_workbook(filename=None, file_contents=file_obj.read())

    table = data.sheets()[0]
    nrows = table.nrows
    order_list = []
    file_name = file_obj.name

    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            try:
                export_date = xlrd.xldate_as_datetime(row[0], 0) #处理Excel表里的日期类型
            except:
                continue
            order_id = row[1]
            delay_days = row[2]
            seller = row[3]
            details = row[4]
            trading_time = row[5]
            order_temp_list = [0, plateform, export_date, order_id, delay_days, seller, details, trading_time, file_name,
                               now_time, first_name]
            order_list.append(order_temp_list)
    return order_list


def insert_into_original_table(param):
    """
    将表中数据插入到缺货订单表中，这是运营人员导入的订单初始表，不做任何处理
    :param param:
    :return:
    """
    cur = connection.cursor()
    sql = 'insert into t_order_out_of_stock VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    cur.execute(sql, tuple(param))
    cur.execute('commit;')
    cur.close()


def order_out_of_stock(file_obj, now_time, first_name, plateform):
    order_list = read_excel(file_obj, plateform, now_time, first_name)
    for order in order_list:
        insert_into_original_table(order)
