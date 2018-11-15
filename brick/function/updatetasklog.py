#-*-coding:utf-8-*-
"""  
 @desc:  记录djcelery 任务运行log
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: updatetasklog.py
 @time: 2018-04-22 11:42
"""

import uuid
import sys

def updatetasklog(conn, taskid='', args='', exectype=1, msg=''):

    if taskid == '':
        taskid = str(uuid.uuid1())

    taskname = sys._getframe().f_back.f_code.co_name

    cursor = conn.cursor()

    if exectype == 1:
        sql = 'insert into hq_db.djcelery_tasklog(task_id,task_name,args) values(%s,%s,%s)'
        cursor.execute(sql, (taskid, taskname, args, ))
        conn.commit()
    elif exectype == 2:
        sql = '''update hq_db.djcelery_tasklog set state='SUCC', runend=sysdate(), msg=%s where task_id=%s'''
        cursor.execute(sql, (msg, taskid,))
        conn.commit()
    else:
        sql = '''update hq_db.djcelery_tasklog set state='FAIL', runend=sysdate(), msg=%s where task_id=%s'''
        cursor.execute(sql, (msg, taskid,))
        conn.commit()

    cursor.close()

    return taskid