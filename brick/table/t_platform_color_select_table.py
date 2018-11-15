#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_platform_color_select_table.py
 @time: 2018-03-30 12:49
"""
class t_platform_color_select_table():
    def __init__(self,db_conn):
        self.db_conn = db_conn

    def get_wish_color(self):
        cursor = self.db_conn.cursor()
        cursor.execute("select Color from t_platform_color_select_table WHERE Platform = 'Wish';")
        objs = cursor.fetchall()
        cursor.close()
        colorlist = []
        for obj in objs:
            colorlist.append(obj[0])
        return colorlist








