#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: update_wish_tort_status.py
 @time: 2018-05-04 14:23
"""

def update_wish_tort_status(site,mainsku,dbconn):
    cursor = dbconn.cursor()
    cursor.execute("select ProductID from t_online_info WHERE MainSKU=%s ;",(mainsku,))
    proobjs = cursor.fetchall()

    prolist = []
    for pro in proobjs:
        prolist.append(pro[0])

    ssors = dbconn.cursor()
    ssors.execute("select Site from t_tort_aliexpress WHERE MainSKU=%s and MainSKU is not NULL and MainSKU != '';",(mainsku,))
    siteobjs = ssors.fetchall()
    ssors.close()
    sitelist = []
    for siteobj in siteobjs:
        sitelist.append(siteobj[0])

    if 'Wish' in sitelist:
        tinfo = 'WY'
    else:
        tinfo = 'Y'
    
    if prolist:
        sql = "update t_online_info_wish set TortInfo='%s' WHERE ProductID in %s ;"%(tinfo,tuple(set(prolist)))

        print sql
        cursor.execute(sql.replace("u'","'"))
        cursor.execute("commit;")

    cursor.close()








