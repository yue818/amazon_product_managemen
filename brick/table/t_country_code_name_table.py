#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_country_code_name_table.py
 @time: 2018/8/25 14:34
"""

class t_country_code_name_table():
    def __init__(self, connection):
        self.connection = connection

    def GetAllCountryCode(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("select country_code, country_name from t_country_code_name_table;")
            objs = cursor.fetchall()
            cursor.close()
            datadict = {}
            for obj in objs:
                datadict[obj[0]] = obj[1]
            return {'errorcode': 1, 'data': datadict}
        except Exception as error:
            return {'errorcode': -1, 'errortext': u'{}'.format(error)}








