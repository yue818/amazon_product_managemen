#-*-coding:utf-8-*-

"""  
 @desc:  实时更新eBay店铺商品SKU状态
 @author: changyang  
 @site: 
 @software: PyCharm
 @file: t_update_t_online_info_ebay_gstatus.py
 @time: 2018-08-23 15:48
"""

import sys
import os
sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
from t_event_database import t_event_database

def run(josnData):
    '''
    说明：根据事件触发调用该函数
    入参：josn格式数据（{"sku":"WF-1197-WT-S","old":"正常","new":"","used":""}）
    '''
    try:
        result = {}
        goodsstatus = None
        dbconnect = t_event_database()
        dbResult = dbconnect.run()
        assert dbResult['errorcode'] == 0, 'line =%s mysql connect error'%(sys._getframe().f_lineno)

        mysqlCursor = (dbResult['db_conn']).cursor()
        strSKU = josnData["sku"]
        strNewStatus = josnData["new"]
        strUsed = josnData["used"]
        if str(strUsed) == '1':
            goodsstatus = '4'
        else:
            mysqlCursor.execute("select statuscode from goodsstatus_compare WHERE hq_GoodsStatus = %s ;", (strNewStatus,))
            statusobj = mysqlCursor.fetchone()
            if statusobj:
                goodsstatus = statusobj[0]
            else:
                assert 2 == 1, 'line=%s goodsstaus=%s not in goodsstatus_compare' % (sys._getframe().f_lineno, strNewStatus)

        # update goodsstateus
        sql = "select itemid from t_online_info_ebay_subsku where productsku='%s'" % strSKU
        mysqlCursor.execute(sql)
        if mysqlCursor.rowcount > 0:
            itemids = [x[0] for x in mysqlCursor.fetchall()]
            itemids = str(itemids)[1:-1].replace('u','')

            sql2 = "update t_online_info_ebay_subsku set productstatus='%s' where productsku='%s'" % (goodsstatus, strSKU)
            mysqlCursor.execute(sql2)

            sql3 = '''update t_online_info_ebay a,( 
                    SELECT itemid,GROUP_CONCAT(distinct productstatus ) as productstatus
                    FROM t_online_info_ebay_subsku
                    WHERE itemid in (%s)
                    group by itemid) b
                    set a.productstatus=b.productstatus
                    where a.itemid=b.itemid;'''
            
            mysqlCursor.execute(sql3 % itemids)

            sql4 = "update t_online_info_ebay set productstatus='%s' where isVariations='NO' and productsku='%s'" % (goodsstatus, strSKU)
            mysqlCursor.execute(sql4)
        else:
            sql4 = "update t_online_info_ebay set productstatus='%s' where productsku='%s'" % (goodsstatus, strSKU)
            mysqlCursor.execute(sql4)

        dbResult['db_conn'].commit()
        result['errorcode'] = 0
        result['errortext'] = 'sku=%s update to %s success' % (strSKU, goodsstatus)
    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = repr(ex)
        mysqlCursor.close()
        dbResult['db_conn'].close()
        return result

    mysqlCursor.close()
    dbResult['db_conn'].close()
    return result


if __name__ == '__main__':
    josnData = {"sku": "WDS0147LB", "old": u"正常", "new": u"临时下架", "used": ""}
    x= run(josnData)
    print x