# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: fba_refresh-20181024.py
 @time: 2018/10/24 16:01
"""
import chardet


finance_data = ['2018-02-04 02:04:43','114-2185291-8683417','Amazon.com',' FUYK0393H01','1','','Commission','USD','-1.0','31735208989706','Shipment','AMZ-0076-FYshun-US/PJ','2018-10-29 10:27:09.884000']
# finance_data_str ='2018-02-04 02:04:43||114-2185291-8683417||Amazon.com|| FUYK0393H01||1||||Commission||USD||-1.0||31735208989706||Shipment||AMZ-0076-FYshun-US/PJ||2018-10-29 10:27:09.884000'

# print finance_data_str

with open('c:/test.log', 'a') as f_w:
    finance_data_str = '||'.join(finance_data)
    print chardet.detect(finance_data_str)['encoding']
    print finance_data_str.decode('ISO-8859-1').encode('utf-8')
    # f_w.write(finance_data_str + '\n')