# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: read_excel.py
 @time: 2018-04-28 9:57
"""  
import xlrd


def read_excel():
    # 打开文件
    work_book = xlrd.open_workbook(r'E:\t_config_apiurl_amazon_input.xls')
    # 获取所有sheet
    print work_book.sheet_names()  # [u'sheet', u'sheet']

    # 获取sheet
    sheet_name = work_book.sheet_names()[3]
    print sheet_name

    # 根据sheet索引或者名称获取sheet内容
    sheet = work_book.sheet_by_name('Sheet2')
    # sheet的名称，行数，列数
    print sheet.name, sheet.nrows, sheet.ncols
    rows = sheet.row_values(3)  # 获取第四行内容
    cols = sheet.col_values(2)  # 获取第三列内容
    print rows
    print cols

    # 获取单元格内容的三种方法
    print sheet.cell(1, 0).value.encode('utf-8')
    print sheet.cell_value(1, 0).encode('utf-8')
    print sheet.row(1)[0].value.encode('utf-8')

    # 获取单元格内容的数据类型
    print sheet.cell(1, 3).ctype


if __name__ == '__main__':
    read_excel()

def get_leaf_type():
    work_book = xlrd.open_workbook(r'E:\t_config_apiurl_amazon_input.xls')
    sheet = work_book.sheet_by_name('Sheet3')
    group_all = dict()
    for i in range(1, sheet.nrows):
        group_all[int(sheet.row_values(i)[0])] = sheet.row_values(i)[4]

    group_select = group_all.copy()

    for key in group_all.keys():
        for val in group_all.values():
            if group_all[key] in val and group_all[key] != val:
                # group_select.pop(key)
                group_select[key] = None
                break

    for key, value in group_select.items():
        if not value:
            print str(key)+','


get_leaf_type()


def save_models():
    import xlrd
    wb = xlrd.open_workbook(r'C:\h.xlsx')
    table = wb.sheets()[0]
    nrows = table.nrows
    insert_values = []
    for rownum in xrange(1, 10):
        row = table.row_values(rownum)
        if row[0]:
            external_product_id = str(row[0])
            if '.' in external_product_id:
                external_product_id = external_product_id.split('.')[0]
        print external_product_id

save_models()