# -*- coding: utf-8 -*-
#bianyong 2018-06-05

import time
import MySQLdb
import sys
import traceback

DATABASES = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq_db',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1',
        'CHARSET': 'utf8'
            }


 
db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'],charset=DATABASES['CHARSET'])


cursor =db_conn.cursor()
sql = 'select mainsku,num from temp_mainsku_num  order by num desc ;'
cursor.execute(sql)
temp_mainsku_num_1_objs=cursor.fetchall()



i =0 
for temp_mainsku_num_1_obj in temp_mainsku_num_1_objs:
    #print temp_mainsku_num_1_obj
    #if i > 1 :
    	#break
    i = i+1
    print '-------------------------------------------------'
    print 'running [ %s --%s ---(%s %s)]'%(i,len(temp_mainsku_num_1_objs),temp_mainsku_num_1_obj[0],temp_mainsku_num_1_obj[1])
    if temp_mainsku_num_1_obj[0] is None or temp_mainsku_num_1_obj[0] =='':
        continue
    print temp_mainsku_num_1_obj
 
    sql_t_online_info_wish_000_no7num = 'select  shopname,productid,mainsku,orders7days,ofsales,datasources,status  from t_online_info_wish_000 where mainsku= %s '
    sql_t_online_info_wish_000_no7num = sql_t_online_info_wish_000_no7num + 'order by orders7days, ofsales ,datasources desc  ;'
    #print sql_t_online_info_wish_000_no7num
    cursor.execute(sql_t_online_info_wish_000_no7num,(temp_mainsku_num_1_obj[0],))
    j =0 
    t_online_info_wish_000_no7num_objs=cursor.fetchall()
    for t_online_info_wish_000_no7num_obj in t_online_info_wish_000_no7num_objs:
        #print t_online_info_wish_000_no7num_obj
        if (j>= temp_mainsku_num_1_obj[1] -10  or t_online_info_wish_000_no7num_obj[3] >0):
            break
        sql_insert = 'insert into t_online_info_wish_000_no7num_delete (shopname ,productid ,mainsku  ,orders7days  ,ofsales ,datasources ,status)  values(%s,%s,%s,%s,%s,%s,%s) ; '
        cursor.execute(sql_insert,(t_online_info_wish_000_no7num_obj[0],t_online_info_wish_000_no7num_obj[1],t_online_info_wish_000_no7num_obj[2],
			                           t_online_info_wish_000_no7num_obj[3],                                 t_online_info_wish_000_no7num_obj[4],t_online_info_wish_000_no7num_obj[5],t_online_info_wish_000_no7num_obj[6]))
        j= j+1
    print 'insert num =%s, all=%s '%(j,temp_mainsku_num_1_obj[1])
    cursor.execute("commit;")
cursor.close()