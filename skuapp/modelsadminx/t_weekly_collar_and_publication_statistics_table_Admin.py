#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_weekly_collar_and_publication_statistics_table_Admin.py
 @time: 2018-04-16 13:07
"""

class t_weekly_collar_and_publication_statistics_table_Admin(object):
    purchase_order = True
    weeklflag = True
    list_display   = ('id','DepartmentID','Week_No','Seller','Receive_No','PubNum','NoPubNum','DepNum',)
    list_filter    = ('DepartmentID','Week_No','Receive_No','PubNum','NoPubNum','DepNum',)
    search_fields  = ('id','DepartmentID','Week_No','Seller','Receive_No','PubNum','NoPubNum','DepNum',)








