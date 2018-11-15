#  _*_ coding:utf-8 _*_

import time
import datetime
import urllib2
import httplib
import requests
import json

class haiying_data_in_db():
    def t_config_wishapi_product_analyse_info(self,hy_record,cursor):
        SourcePicPath = 'https://contestimg.wish.com/api/webimage/' + hy_record['pid'] + '-small.jpg'
        optime = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        cursor.execute(
            "insert into t_config_wishapi_product_analyse_info (Pid,Name,SourcePicPath,approved_date,NumBought,ShelveDay,UnitPrice,OrdersLast7Days,OrdersLast7to14Days,SupplierID,salesgrowth,Op_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on  DUPLICATE key update NumBought=%s,OrdersLast7Days=%s,salesgrowth=%s,Op_time=%s ;",
            (hy_record['pid'], hy_record['pname'], SourcePicPath, hy_record['approved_date'], hy_record['num_bought'],hy_record['gen_time'], hy_record['price'], hy_record['salesweek1'], hy_record['salesweek2'], hy_record['supplier_url'], hy_record['salesgrowth'],optime, hy_record['num_bought'],hy_record['salesweek1'],hy_record['salesgrowth'],optime))
        cursor.execute('commit;')

    #抓取上架时间是15天内的wish商品id
    def t_config_wishapi_product_analyse_all_info(self,hy_record,cursor):
        start_time = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        SourcePicPath = 'https://contestimg.wish.com/api/webimage/' + hy_record['pid'] + '-small.jpg'
        curtime = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        if hy_record['gen_time'] is None or hy_record['approved_date'] is None:
            return 1
        hy_record['pname'] = hy_record['pname'].replace('\'','\'\'')
        ta = time.strptime(curtime, "%Y/%m/%d/%H/%M/%S")
        ShelveDay = hy_record['gen_time']
        tb = time.strptime(ShelveDay, "%Y-%m-%d")
        y,m,d,H,M,S = ta[0:6]
        dataTimea=datetime.datetime(y,m,d,H,M,S)
        y,m,d,H,M,S = tb[0:6]
        dataTimeb=datetime.datetime(y,m,d,H,M,S)
        daysDiff=(dataTimea-dataTimeb).days
        print daysDiff
        print hy_record['feed_tile_text']
        # print tuple(hy_record['c_ids'])
        optime = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        if daysDiff <= 31 and hy_record['num_bought'] >= 10 :
        #if daysDiff <= 31:
            sql = "insert into t_config_wishapi_product_analyse_info_original (Pid,Name,mid,mname,SourcePicPath,approved_date,is_promo,is_verified,is_HWC,num_rating,rating,o_price,"\
                "o_shipping,shipping,NumBought,ShelveDay,UnitPrice,OrdersLast7Days,OrdersLast7to14Days,totalprice,dailybought,SupplierID,salesgrowth,Op_time,c_ids,op_flag)  "\
                "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s,'%s','%s',%s,%s,%s,%s,'%s',%s,'%s','%s',%s) on  DUPLICATE key update ShelveDay=%s,num_rating=%s,rating=%s,NumBought=%s,OrdersLast7Days=%s,salesgrowth=%s,Op_time=%s ;"\
                %(hy_record['pid'], hy_record['pname'],hy_record['mid'],hy_record['mname'], SourcePicPath, hy_record['approved_date'], hy_record['is_promo'], hy_record['is_verified'], hy_record['is_HWC'],hy_record['num_rating'],hy_record['rating'],hy_record['o_price'],hy_record['o_shipping'],hy_record['shipping'],int(hy_record['feed_tile_text']),hy_record['gen_time'],hy_record['price'],hy_record['salesweek1'], hy_record['salesweek2'], hy_record['totalprice'],hy_record['dailybought'],hy_record['supplier_url'],hy_record['salesgrowth'],optime,','.join(hy_record['c_ids']),0,hy_record['gen_time'],hy_record['num_rating'],hy_record['rating'],int(hy_record['num_bought']),hy_record['salesweek1'],hy_record['salesgrowth'],optime)
            print sql
            cursor.execute(sql)
            cursor.execute('commit;')
        end_time = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        print "start time:%s" %(start_time)
        print "end time:%s" % (end_time)

        # 上架时间是15天内的wish商品id抓取boughtthis
    def t_config_wishapi_product_analyse_all_info_boughtthis(self, cursor):
        start_time = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        sql = "select Pid,Name,mid,mname,SourcePicPath,approved_date,is_promo,is_verified,is_HWC,num_rating,rating,o_price,"\
                "o_shipping,shipping,NumBought,ShelveDay,UnitPrice,OrdersLast7Days,OrdersLast7to14Days,totalprice,dailybought,SupplierID,salesgrowth,Op_time,c_ids "\
                "from t_config_wishapi_product_analyse_info_original where op_flag = 0 AND boughtthis_flag= 0"
        cursor.execute(sql)
        pid_objs = {}
        maxnum = 5000
        while True:
            pid_objs = cursor.fetchmany(maxnum)
            for pid_obj in pid_objs:
                url = "http://47.251.3.95:81/wish/getStarbyId?id=%s&num_bought=1" %(pid_obj[0])
                objes = {}
                objesg = {}
                objes['errcode'] = 'SUCCESS'
                num_bought = 0
                try:
                    response = requests.get(url)
                except Exception as e:
                    objes['errcode'] = 'get num_bought requests fail'
                if response.status_code != 200:
                  objes['errcode'] = 'get num_bought requests back fail'
                  num_bought = 0
                else:
                    objesg = response.content.replace("\r\n", ' ')
                    print objesg
                    objesgs = json.loads(objesg)
                    num_bought = objesgs['num_bought'].replace('+ bought this','').replace(' bought this','')
                    print num_bought
                    if len(num_bought) == 0:
                        objes['errcode'] = 'get num_bought is null'
                        num_bought = 0
                    optime = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
                    print pid_obj
                    print pid_obj[0]
                    if objes['errcode'] == 'SUCCESS' or objes['errcode'] == 'get num_bought is null':
                        pname = str(pid_obj[1]).replace('\'', '\'\'')
                        sql = "insert into t_config_wishapi_product_analyse_info_original_trans (Pid,Name,mid,mname,SourcePicPath,approved_date,is_promo,is_verified,is_HWC,num_rating,rating,o_price," \
                              "o_shipping,shipping,NumBought,ShelveDay,UnitPrice,OrdersLast7Days,OrdersLast7to14Days,totalprice,dailybought,SupplierID,salesgrowth,Op_time,c_ids,op_flag,getboughtinfo,boughtthis,boughtthis_time)  " \
                              "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s,'%s','%s',%s,%s,%s,%s,'%s',%s,'%s','%s',%s,'%s',%s,'%s') on  DUPLICATE key update op_flag=%s;" \
                              % (pid_obj[0], pname, pid_obj[2], pid_obj[3], pid_obj[4],
                                 pid_obj[5], pid_obj[6], pid_obj[7],
                                 pid_obj[8], pid_obj[9], pid_obj[10], pid_obj[11],
                                 pid_obj[12], pid_obj[13], int(pid_obj[14]),
                                 pid_obj[15], pid_obj[16], pid_obj[17], pid_obj[18],
                                 pid_obj[19], pid_obj[20], pid_obj[21],
                                 pid_obj[22], optime, pid_obj[24], 1,objes['errcode'],num_bought,optime,1)
                        sql1 = "update t_config_wishapi_product_analyse_info_original set getboughtinfo='%s',op_flag=%s where Pid = '%s' " % (objes['errcode'], 1, str(pid_obj[0]))
                        cursor.execute(sql)
                        cursor.execute(sql1)

                    else:
                        sql = "update t_config_wishapi_product_analyse_info_original set getboughtinfo='%s' where Pid = '%s' " % (objes['errcode'], str(pid_obj[0]))
                        cursor.execute(sql)
                    cursor.execute('commit;')
            if len(pid_objs) < maxnum:
                break
        end_time = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        print "start time:%s" %(start_time)
        print "end time:%s" % (end_time)

        # 每天刷新boughtthis
    def t_config_wishapi_product_analyse_all_info_boughtthis_trans(self, cursor):
        start_time = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        sql = "select Pid,Name,mid,mname,SourcePicPath,approved_date,is_promo,is_verified,is_HWC,num_rating,rating,o_price,"\
                "o_shipping,shipping,NumBought,ShelveDay,UnitPrice,OrdersLast7Days,OrdersLast7to14Days,totalprice,dailybought,SupplierID,salesgrowth,Op_time,c_ids,boughtthis_time "\
                "from t_config_wishapi_product_analyse_info_original_trans "
        cursor.execute(sql)
        cursor.execute(sql)
        pid_objs = {}
        maxnum = 5000
        while True:
            pid_objs = cursor.fetchmany(maxnum)
            for pid_obj in pid_objs:
                url = "http://47.251.3.95:81/wish/getStarbyId?id=%s&num_bought=1" %(pid_obj[0])
                objes = {}
                objesg = {}
                objes['errcode'] = 'SUCCESS'
                num_bought = 0
                try:
                    response = requests.get(url)
                except Exception as e:
                    objes['errcode'] = 'get num_bought requests fail'
                if response.status_code != 200:
                  objes['errcode'] = 'get num_bought requests back fail'
                  num_bought = 0
                else:
                    objesg = response.content.replace("\r\n", ' ')
                    print objesg
                    objesgs = json.loads(objesg)
                    num_bought = objesgs['num_bought'].replace('+ bought this','').replace(' bought this','')
                    print num_bought
                    if len(num_bought) == 0:
                        objes['errcode'] = 'get num_bought is null'
                        num_bought = 0
                    optime = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
                    if objes['errcode'] == 'SUCCESS':
                        sql = "update t_config_wishapi_product_analyse_info_original_trans set boughtthis=%s where Pid = '%s' " % (num_bought, str(pid_obj[0]))
                        cursor.execute(sql)
                    if num_bought >= 100:
                        pname = str(pid_obj[1]).replace('\'', '\'\'')
                        sql = "insert into t_config_wishapi_product_analyse_info_original_trans_plus (Pid,Name,mid,mname,SourcePicPath,approved_date,is_promo,is_verified,is_HWC,num_rating,rating,o_price," \
                              "o_shipping,shipping,NumBought,ShelveDay,UnitPrice,OrdersLast7Days,OrdersLast7to14Days,totalprice,dailybought,SupplierID,salesgrowth,Op_time,c_ids,op_flag,getboughtinfo,boughtthis,boughtthis_time,uprush_time)  " \
                              "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s,'%s','%s',%s,%s,%s,%s,'%s',%s,'%s','%s',%s,'%s',%s,'%s','%s') on  DUPLICATE key update op_flag=%s;" \
                              % (pid_obj[0], pname, pid_obj[2], pid_obj[3], pid_obj[4],
                                 pid_obj[5], pid_obj[6], pid_obj[7],
                                 pid_obj[8], pid_obj[9], pid_obj[10], pid_obj[11],
                                 pid_obj[12], pid_obj[13], int(pid_obj[14]),
                                 pid_obj[15], pid_obj[16], pid_obj[17], pid_obj[18],
                                 pid_obj[19], pid_obj[20], pid_obj[21],
                                 pid_obj[22], optime, pid_obj[24], 1,objes['errcode'],num_bought,pid_obj[25],optime,1)
                        sql1 = "delete from t_config_wishapi_product_analyse_info_original_trans where pid = '%s'" %(str(pid_obj[0]))
                        sql2 = "update t_config_wishapi_product_analyse_info_original set getboughtinfo='%s',boughtthis_flag=%s where Pid = '%s' " % (objes['errcode'], 1, str(pid_obj[0]))
                        cursor.execute(sql)
                        cursor.execute(sql1)
                        cursor.execute(sql2)
                    cursor.execute('commit;')
            if len(pid_objs) < maxnum:
                break
        end_time = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        print "start time:%s" %(start_time)
        print "end time:%s" % (end_time)

        # 删除过期数据
    def t_config_wishapi_product_analyse_all_info_boughtthis_trans_delete(self, cursor):
        optime = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        sql = "select Pid,Name,mid,mname,SourcePicPath,approved_date,is_promo,is_verified,is_HWC,num_rating,rating,o_price,"\
                "o_shipping,shipping,NumBought,ShelveDay,UnitPrice,OrdersLast7Days,OrdersLast7to14Days,totalprice,dailybought,SupplierID,salesgrowth,Op_time,c_ids,boughtthis,boughtthis_time "\
                "from t_config_wishapi_product_analyse_info_original_trans  where datediff(NOW(),shelveday) > 45"
        cursor.execute(sql)
        pid_objs = cursor.fetchall
        for pid_obj in pid_objs:
            if len(pid_obj) == 0:
                continue
            sql = "insert into t_config_wishapi_product_analyse_info_original_trans_delete (Pid,Name,mid,mname,SourcePicPath,approved_date,is_promo,is_verified,is_HWC,num_rating,rating,o_price," \
                  "o_shipping,shipping,NumBought,ShelveDay,UnitPrice,OrdersLast7Days,OrdersLast7to14Days,totalprice,dailybought,SupplierID,salesgrowth,Op_time,c_ids,op_flag,getboughtinfo,boughtthis,boughtthis_time,delete_time)  " \
                  "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s,'%s','%s',%s,%s,%s,%s,'%s',%s,'%s','%s',%s,'%s',%s,'%s','%s') on  DUPLICATE key update op_flag=%s;" \
                  % (pid_obj[0], pname, pid_obj[2], pid_obj[3], pid_obj[4],
                     pid_obj[5], pid_obj[6], pid_obj[7],
                     pid_obj[8], pid_obj[9], pid_obj[10], pid_obj[11],
                     pid_obj[12], pid_obj[13], int(pid_obj[14]),
                     pid_obj[15], pid_obj[16], pid_obj[17], pid_obj[18],
                     pid_obj[19], pid_obj[20], pid_obj[21],
                     pid_obj[22], optime, pid_obj[24], 1, objes['errcode'], num_bought, pid_obj[25], optime,1)
            cursor.execute(sql)
        sql1 = "delete from t_config_wishapi_product_analyse_info_original_trans where datediff(NOW(),shelveday) > 45 "
        sql2 = "delete from t_config_wishapi_product_analyse_info_original where datediff(NOW(),shelveday) > 45 "
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute('commit;')
        end_time = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        print "start time:%s" %(optime)
        print "end time:%s" % (end_time)

    def t_config_wishapi_product_cid_info(self,hy_record,cursor):
        optime = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        cursor.execute(
            "insert into t_product_category_dict (category,categoryname,f_category,f_categoryname,op_time) values (%s,%s,%s,%s,%s) on  DUPLICATE key update categoryname=%s,f_category=%s,f_categoryname=%s,Op_time=%s ;",
            (hy_record['cid'], hy_record['cname'], hy_record['f_cid'], hy_record['f_cname'],optime, hy_record['cname'], hy_record['f_cid'], hy_record['f_cname'],optime))
        cursor.execute('commit;')

        # 上架时间是一个月内的wish商品id抓取浏览量
    def t_config_wishapi_product_analyse_all_info_view_his_data(self, cursor,cursor1):
        from get_data_from_haiying import Haiying
        hy = Haiying()
        objes = {}
        objes['aver'] = 0
        start_time = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        sql = "select Pid,Name,mid,mname,SourcePicPath,approved_date,is_promo,is_verified,is_HWC,num_rating,rating,o_price,"\
                "o_shipping,shipping,NumBought,ShelveDay,UnitPrice,OrdersLast7Days,OrdersLast7to14Days,totalprice,dailybought,SupplierID,salesgrowth,Op_time,c_ids "\
                "from t_config_wishapi_product_analyse_info_original where ShelveDay >= (select date_sub(NOW(), interval 1 month))"
        cursor.execute(sql)
        pid_objs = {}
        maxnum = 5000
        while True:
            pid_objs = cursor.fetchmany(maxnum)
            for pid_obj in pid_objs:
                try:
                    print pid_obj[0]
                    viwtt = hy.data_viw_bypid(pid_obj[0])
                    for obj in viwtt:
                        if obj is None:
                            objes['errcode'] = 'get data is none'
                        else:
                            a = obj['view_his_data']
                            print "a=%s" %a
                            if len(a) ==0:
                                objes['errcode'] = 'get data is none'
                            else:
                                sum_1=0.00
                                sum_2=0.00
                                for x in a:
                                    if x is not None:
                                        sum_1 += 1
                                        sum_2 += x['viewing']
                                        print sum_1
                                        print sum_2
                                        aver = ("%.2f" % (sum_2 / sum_1))
                                        objes['aver'] = aver  # ���火苗评价评价
                                        objes['errcode'] = 'SUCCESS'
                                    else:
                                        objes['aver'] = 0  # ���火苗评价评价
                                        objes['errcode'] = 'SUCCESS'
                except Exception as e:
                    objes['aver'] = 0
                    objes['errcode'] = 'fail'
                print objes['aver']
                if objes['errcode'] == 'SUCCESS' and float(objes['aver']) > 0:
                    pname = str(pid_obj[1]).replace('\'', '\'\'')
                    optime = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
                    sql = "insert into t_config_wishapi_product_analyse_info_original_trans (product_id,Name,mid,mname,SourcePicPath,approved_date,is_promo,is_verified,is_HWC,num_rating,rating,o_price," \
                          "o_shipping,shipping,NumBought,ShelveDay,UnitPrice,OrdersLast7Days,OrdersLast7to14Days,totalprice,dailybought,SupplierID,salesgrowth,Op_time,c_ids,op_flag,getboughtinfo,boughtthis,boughtthis_time,viewdata)  " \
                          "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s,'%s','%s',%s,%s,%s,%s,'%s',%s,'%s','%s',%s,'%s',%s,'%s',%s) on  DUPLICATE key update viewdata=%s,num_rating=%s,rating=%s,NumBought=%s;" \
                          % (pid_obj[0], pname, pid_obj[2], pid_obj[3], pid_obj[4],
                             pid_obj[5], pid_obj[6], pid_obj[7],
                             pid_obj[8], pid_obj[9], pid_obj[10], pid_obj[11],
                             pid_obj[12], pid_obj[13], int(pid_obj[14]),
                             pid_obj[15], pid_obj[16], pid_obj[17], pid_obj[18],
                             pid_obj[19], pid_obj[20], pid_obj[21],
                             pid_obj[22], optime, pid_obj[24], 1,objes['errcode'],pid_obj[14],optime,objes['aver'],objes['aver'],pid_obj[9], pid_obj[10],int(pid_obj[14]))
                    print "sql = %s" %sql
                    cursor1.execute(sql)
                    cursor1.execute('commit;')
            if len(pid_objs) < maxnum:
                break
        end_time = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
        print "start time:%s" %(start_time)
        print "end time:%s" % (end_time)

        # 每天刷新boughtthis