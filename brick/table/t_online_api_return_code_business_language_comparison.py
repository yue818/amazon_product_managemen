#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_online_api_return_code_business_language_comparison.py
 @time: 2018-05-03 13:14
"""

class t_online_api_return_code_business_language_comparison():
    def __init__(self,dbconn):
        self.dbconn = dbconn

    def insert_code_message(self,code,message):
        cursor = self.dbconn.cursor()
        cursor.execute("insert into t_online_api_return_code_business_language_comparison (Platform,Code,Message) "
                       "VALUES ('Wish',%s,%s);",(code,message))
        cursor.execute("commit;")
        cursor.close()

    def get_bl_by_code(self,code):
        cursor = self.dbconn.cursor()
        cursor.execute("select BL from t_online_api_return_code_business_language_comparison "
                       " WHERE Platform='Wish' and Code=%s ;", (code,))
        obj = cursor.fetchone()
        cursor.close()
        bl = None
        if obj:
            bl = obj[0]
        return bl




