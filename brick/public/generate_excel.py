# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: generate_excel.py
 @time: 2017-12-30 13:29

"""
import xlwt

def generate_excel(allobjs,pathname):
    result = {}
    try:
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('Sheet1')

        for index, item in enumerate(allobjs[0]):
            worksheet.write(0, index, item)

        row = 0
        for i in range(1,len(allobjs)):
            row = row + 1
            for idx, val in enumerate(allobjs[i]):
                worksheet.write(row, idx, val)

        workbook.save(pathname)
        result['code'] = 0
        result['error']= ''
    except Exception,ex:
        result['code'] = 1
        result['error'] = '%s:%s'%(Exception,ex)
    return result