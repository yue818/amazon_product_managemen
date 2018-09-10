
import MySQLdb
cnxn = MySQLdb.connect('hequskuapp.mysql.rds.aliyuncs.com','by15161458383','K120Esc1','hq_db' )
cursor =cnxn.cursor();
sql1 = "select DISTINCT(cata1) from t_catainfo_ebay"
#sql='update t_config_mstsc set  RegionId="cn-qingdao",InstanceId="i-m5eijiwzg03cxwhz3lti" where ip="10.29.168.221"'
cursor.execute(sql1)
rs = []
while True:
    cata1_objs=cursor.fetchone()
    if not cata1_objs:
        break
    print cata1_objs
    d = dict(zip(('a','b'), (cata1_objs,cata1_objs)))
    rs.append(d)
print rs
'''
# -*- coding: utf-8 -*-
#from Project.skuapp.table.t_catainfo_ebay import *
#cata1 = t_hotsale_proinfo_ebay.objects.filter(CatagoryID=obj.CatagoryID)
import sys
sys.path.append('Project/skuapp/public/t_catainfo_ebay_json.py')    
from t_catainfo_ebay_json import *
#t_catainfo_ebay_json=""
cata1_objs = t_catainfo_ebay_json.objects.all().values_list("cata1")
if len(cata1_objs)>0:
    for cata1_obj in cata1_objs:
        cata2_objs = t_catainfo_ebay_json.objects.filter(cata1=cata1_obj).values_list("cata2")
        t_catainfo_ebay_json="["+cata1_obj+":"+"{"+cata2_objs+"}"
        print t_catainfo_ebay_json

        if len(cata2_objs)>0
            for cata2_obj in cata2_objs:
                cata3_objs = t_hotsale_proinfo_ebay.objects.filter(cata2=cata2_obj).values_list("cata3")
                if len(cata3_objs)>0
                    for cata3_obj in cata3_objs:
                        cata4_objs = t_hotsale_proinfo_ebay.objects.filter(cata3=cata3_obj).values_list("cata4")
                        if len(cata3_objs)>0
                        for cata4_obj in cata4_objs:
                            cata5_objs = t_hotsale_proinfo_ebay.objects.filter(cata4=cata4_obj).values_list("cata5")
                            #t_catainfo_ebay_json={cata1_obj:}
'''
