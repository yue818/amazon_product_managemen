# coding:utf-8
"""
@author: wangzhiyang
@contact: 15205512335
@site:
@software: PyCharm
@time: 2018-07-23
@desc:海外仓集货仓-采购后同步入库状态
"""
from django.db import connection
from py_conn import py_conn
import sys
import MySQLdb
from datetime import datetime as ddtime
import ConfigParser
import time

class b_stockStatus:
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        #self.cf.read("/home/wangzhiyang/Project/brick/pydata/py_redis/py_Config.conf")
        self.cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_redis/py_Config.conf")
        self.strCurrentDate = time.strftime("%Y%m%d%H")
        self.logPath = self.cf.get("Syn_StockStatus", "log_path")
        self.fileHead = self.cf.get("Syn_StockStatus", "fileHead")
        self.strFileName = self.logPath + self.fileHead + self.strCurrentDate + '.log'


    def Recordlog(self, message, logLevel, nLine):
        strTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        strInfo = "[" + strTime + "][" + str(__file__) + "," + str(nLine) + "," + str(logLevel) + "]:" + str(
            message) + "\n"
        with open(self.strFileName, 'a+') as f:
            f.write(strInfo)
        f.close()

    def get_hqdb_purchase(self,hqdb_conn):
        result = {'errorcode': 0,'errortext':'','returnresult':()}
        try:
            hqdb_cursor = hqdb_conn.cursor()
            str_hqdb_selectSql = "select Stocking_plan_number,Single_number,Warehouse, ProductSKU,ProductImage,Price,Stocking_quantity,LogisticsNumber,Weight,'notyet'," \
                                 "'already',ProductName,Remarks,'already',QTY,level,Site,Product_nature,Demand_people,AccountNum,ShopSKU from t_stocking_purchase_order " \
                                 "where Status in('notyet','purchasing') and  (Single_number like 'CGD%' or Single_number like 'DBD%'); " #Status='notyet' and
            hqdb_cursor.execute(str_hqdb_selectSql)
            tupple_hqdb_stockStatus = hqdb_cursor.fetchall()
            result['errortext'] =  'success'
            result['returnresult'] = tupple_hqdb_stockStatus
            hqdb_cursor.close()
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            result['returnresult'] = ()
            self.Recordlog("get_hqdb_purchase:" + str(ex),"error",sys._getframe().f_lineno)
        return result

    def get_hqdb_fba_purchase(self,hqdb_conn):
        result = {'errorcode': 0,'errortext':'','returnresult':()}
        try:
            hqdb_cursor = hqdb_conn.cursor()
            str_hqdb_selectSql = "select Stocking_plan_number,Single_number,Destination_warehouse, ProductSKU,ProductImage,ProductPrice,Stocking_quantity,LogisticsNumber,ProductWeight,'notyet'," \
                                 "'already',ProductName,Remarks,'already',QTY,level,Site,Product_nature,Demand_people,AccountNum,ShopSKU from t_stocking_demand_fba " \
                                 "where Status='purchasing' and  (Single_number like 'CGD%' or Single_number like 'DBD%'); " #Status='notyet' and
            hqdb_cursor.execute(str_hqdb_selectSql)
            tupple_hqdb_stockStatus = hqdb_cursor.fetchall()
            result['errortext'] =  'success'
            result['returnresult'] = tupple_hqdb_stockStatus
            hqdb_cursor.close()
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            result['returnresult'] = ()
            self.Recordlog("get_hqdb_fba_purchase:" + str(ex),"error",sys._getframe().f_lineno)
        return result

    def get_hqdb_fba_reject(self,hqdb_conn):
        result = {'errorcode': 0,'errortext':'','returnresult':()}
        try:
            hqdb_cursor = hqdb_conn.cursor()
            str_hqdb_selectSql = "select ProductSKU,RejectNumber,PurchaseOrderNum,RejectNum,ReturnNumber,isCheckTranReturn " \
                                 "from t_stocking_reject_fba where Status='rejecting' and ReturnNumber is not null and ReturnNumber!='';  " #Status='notyet' and
            hqdb_cursor.execute(str_hqdb_selectSql)
            tupple_hqdb_stockStatus = hqdb_cursor.fetchall()
            result['errortext'] =  'success'
            result['returnresult'] = tupple_hqdb_stockStatus
            hqdb_cursor.close()
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            result['returnresult'] = ()
            self.Recordlog("get_hqdb_fba_reject:" + str(ex),"error",sys._getframe().f_lineno)
        return result

    def get_py_complete_purchase(self,sqlserverInfo,purchaseOrderNo,productSKU):
        result = {'errorcode': 0,'errortext':'','returnresult':()}
        try:
            if sqlserverInfo['errorcode'] == 0:
                str_py_selectSql = ""
                if purchaseOrderNo[:3] == "CGD": #采购订单获取
                    str_py_selectSql = "select OrderAmount,sum(Amount),GoodsID from CG_StockInD(nolock) d where d.StockInNID in "\
                    "(select  nid from CG_StockInM(nolock) m where m.stockorder='%s' and  m.CheckFlag=1) "\
                    "and d.GoodsID = (select top 1 nid from B_Goods where SKU='%s') group by GoodsID,OrderAmount; "%(purchaseOrderNo,productSKU)
                elif purchaseOrderNo[:3] == "RRD": #退货订单
                    '''
                        select * from CG_StockInD where StockInNID in(1139571,1137611);
                        select * from CG_StockInM where NID in(1139571,1137611);
                        select * from CG_StockInM where stockorder='CGD-2018-08-31-2628';
                        select * from CG_StockInM where stockorder='RKD201809020860';
                    '''
                    str_py_selectSql = '''
                                                select OrderAmount,Amount,GoodsID from CG_StockInD(nolock) where StockInNID=
                                                 (select top 1 nid from CG_StockInM(nolock) where  BillNumber='%s') 
                                                 and GoodsID = (select top 1 nid from B_Goods where SKU='%s');
                                                 ''' % (purchaseOrderNo, productSKU)
                    #-- and StockOrder =( select top 1  BillNumber from CG_StockInM(nolock) where StockOrder='%s')
                else: #调拨单号获取
                    str_py_selectSql = "select sum(Amount),sum(Amount),GoodsID from KC_StockChangeD "\
                                        "where StockChangeNID in (select nid from KC_StockChangeM where BillNumber='%s' and checkflag=1) "\
                                        "and GoodsID=(select top 1 nid from b_goods where sku='%s') group by GoodsID; " % (purchaseOrderNo, productSKU)
                sqlserverInfo['py_cursor'].execute(str_py_selectSql)
                tupple_py_purchase = sqlserverInfo['py_cursor'].fetchone()
                result['errortext'] =  'success'
                result['returnresult'] = tupple_py_purchase
            else:
                result['errorcode'] = -1
                result['errortext'] = 'get_py_complete_purchase:__LINE__=%s,connect fail' % (sys._getframe().f_lineno)
                result['returnresult'] = ()
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            result['returnresult'] = ()
        return result

    def get_py_complete_purchase_memo(self,sqlserverInfo,purchaseOrderNo,productSKU):
        result = {'errorcode': 0,'errortext':'','returnresult':()}
        try:
            if sqlserverInfo['errorcode'] == 0:
                str_py_selectSql = ""
                str_py_selectSql = "select CGM.Note from CG_StockOrderM CGM left join CG_StockOrderD CGD on CGM.NID = CGD.StockOrderNID " \
                                   " where CGM.BillNumber='%s'and CGD.GoodsID = (select top 1 nid from B_Goods where SKU='%s') ; " % (
                                   purchaseOrderNo, productSKU)

                sqlserverInfo['py_cursor'].execute(str_py_selectSql)
                tupple_py_purchase = sqlserverInfo['py_cursor'].fetchone()
                result['errortext'] =  'success'
                result['returnresult'] = tupple_py_purchase
            else:
                result['errorcode'] = -1
                result['errortext'] = 'get_py_complete_purchase_memo:__LINE__=%s,connect fail' % (sys._getframe().f_lineno)
                result['returnresult'] = ()
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            result['returnresult'] = ()
        return result

    def get_py_uncomplete_purchase(self,sqlserverInfo,purchaseOrderNo,productSKU):
        result = {'errorcode': 0}
        try:
            if sqlserverInfo['errorcode'] == 0:
                str_py_selectSql = "select Amount,InAmount,GoodsSKUID,GoodsID from CG_StockOrderD(nolock) d where d.StockOrderNID="\
                                    "(select top 1 nid from CG_StockOrderM(nolock) m where m.BillNumber='%s' and  (m.Archive=0 and m.checkflag=1) and m.inflag=0) "\
                                    "and d.GoodsID = (select top 1 nid from B_Goods where SKU='%s'); "%(purchaseOrderNo,productSKU)
                sqlserverInfo['py_cursor'].execute(str_py_selectSql)
                tupple_py_unpurchase = sqlserverInfo['py_cursor'].fetchone()
                result['errortext'] =  'success'
                result['returnresult'] = tupple_py_unpurchase
            else:
                result['errorcode'] = -2
                result['errortext'] = '__LINE__=%s,connect fail' % ( sys._getframe().f_lineno)
                result['returnresult'] = ()
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            result['returnresult'] = ()
        return result

    #普元全部入库后更新表记录  只要有订单号即已采购
    def alreadly_purchased(self,obj,InAmount,hqdb_conn):
        result = {'errorcode': 0,'errortext':''}
        try:
            hqdb_cursor = hqdb_conn.cursor()
            updateSql = "update t_stocking_demand_list set Status='already' where Stocking_plan_number='%s'"%(obj[0])
            hqdb_cursor.execute(updateSql)
            updateSql = "update t_stocking_purchase_order set The_arrival_of_the_number=%s,completeInstoreMan=%s,completeInstoreDate=%s,Status='already'," \
                        "Arrival_status='already',Storage_status='already',Arrival_date1=%s,StorageDate=%s where Stocking_plan_number=%s"
            parm1 = (InAmount, '系统定时刷新',ddtime.now(),ddtime.now(),ddtime.now(),obj[0])
            hqdb_cursor.execute(updateSql, parm1)

            selectSql = "select count(1) from t_set_warehouse_storage_situation_list where Stocking_plan_number='%s'"%(obj[0])
            hqdb_cursor.execute(selectSql)
            storageRecord = hqdb_cursor.fetchone()
            if storageRecord[0] == 0:
                updateSql = "insert into t_set_warehouse_storage_situation_list(Stocking_plan_number,Purchase_Order_No,Destination_warehouse,ProductSKU ,ProductImage," \
                            "Price,Stocking_quantity,LogisticsNumber,Weight,Delivery_status ,Arrival_status ,ProductName," \
                            "Remarks,Storage_status,QTY,level,Site,Product_nature,Demand_people,AccountNum,ShopSKU,OplogTime," \
                            "Arrival_date,StorageDate,The_arrival_of_the_number,Stock_plan_unfinished_quantity,checkStatus) " \
                            "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s)"
                parm3 = (obj[0],obj[1],obj[2],obj[3],obj[4],obj[5],obj[6],obj[7],obj[8],'notyet','already',obj[11],obj[12],'already',obj[14],obj[15],obj[16],
                         obj[17],obj[18],obj[19],obj[20],ddtime.now(),ddtime.now(),ddtime.now(),InAmount,int(obj[14])-int(InAmount),'notcheck')
                hqdb_cursor.execute(updateSql, parm3)
            hqdb_cursor.execute("commit")
            hqdb_cursor.close()
            self.Recordlog("update all sucess", "info", sys._getframe().f_lineno)
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            self.Recordlog("alreadly_purchased:" + result['errortext'], "info", sys._getframe().f_lineno)
        return result

    # fba普元全部入库后更新表记录  只要有订单号即已采购
    def fba_alreadly_purchased(self, obj, InAmount, hqdb_conn):
        result = {'errorcode': 0, 'errortext': ''}
        try:
            hqdb_cursor = hqdb_conn.cursor()
            updateSql = "update t_stocking_demand_fba set The_arrival_of_the_number=%s,checkCompleteNum=%s,checkInferiorNum=0,completePurchaseMan=%s,completePurchaseDate=%s,Status='check',completeStatus = 'completepurchase' " \
                        "where Stocking_plan_number=%s"
            parm1 = (InAmount,InAmount, '系统定时刷新', ddtime.now(),obj[0])
            hqdb_cursor.execute(updateSql, parm1)
            hqdb_cursor.execute("commit")
            hqdb_cursor.close()
            self.Recordlog("update all sucess", "info", sys._getframe().f_lineno)
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            self.Recordlog("fba_alreadly_purchased:" + result['errortext'], "info", sys._getframe().f_lineno)
        return result

    # 普元未入库后更新表记录  只要有订单号即已采购
    def not_purchased(self, obj,hqdb_conn):
        result = {'errorcode': 0}
        try:
            #t_stocking_demand_list.objects.filter(Stocking_plan_number=obj[0]).update(Status='already')
            hqdb_cursor = hqdb_conn.cursor()
            updateSql = "update t_stocking_demand_list set Status='already' where Stocking_plan_number='%s'"%(obj[0])
            hqdb_cursor.execute(updateSql)
            hqdb_cursor.execute("commit")
            hqdb_cursor.close()
            self.Recordlog("update t_stocking_demand_list sucess", "info", sys._getframe().f_lineno)
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            self.Recordlog("not_purchased:" + result['errortext'], "info", sys._getframe().f_lineno)
        return result

    # fba普元未入库后更新表记录  只要有订单号即已采购
    def fba_not_purchased(self, obj, hqdb_conn):
        result = {'errorcode': 0}
        try:
            hqdb_cursor = hqdb_conn.cursor()
            updateSql = "update t_stocking_demand_fba set Status='purchasing' where Stocking_plan_number='%s'" % (obj[0])
            hqdb_cursor.execute(updateSql)
            hqdb_cursor.execute("commit")
            hqdb_cursor.close()
            self.Recordlog("update t_stocking_demand_fba sucess", "info", sys._getframe().f_lineno)
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            self.Recordlog("fba_not_purchased:" + result['errortext'], "info", sys._getframe().f_lineno)
        return result

    # 普元部分入库后更新表记录  只要有订单号即已采购
    def partion_alreadly_purchased(self, obj, InAmount,hqdb_conn):
        result = {'errorcode': 0}
        try:
            #t_stocking_purchase_order.objects.filter(Stocking_plan_number=obj[0]).update(The_arrival_of_the_number=InAmount,Status='partion',Arrival_status='partion',Storage_status='partion')
            #t_stocking_demand_list.objects.filter(Stocking_plan_number=obj[0]).update(Status='already')
            hqdb_cursor = hqdb_conn.cursor()
            updateSql = "update t_stocking_demand_list set Status='already' where Stocking_plan_number='%s'"%(obj[0])
            hqdb_cursor.execute(updateSql)
            updateSql = "update t_stocking_purchase_order set The_arrival_of_the_number=%s where Stocking_plan_number=%s"
            parm1 = (InAmount,obj[0])
            hqdb_cursor.execute(updateSql, parm1)
            hqdb_cursor.execute("commit")
            hqdb_cursor.close()
            self.Recordlog("update part sucess", "info", sys._getframe().f_lineno)
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            self.Recordlog("alreadly_purchased:" + result['errortext'], "info", sys._getframe().f_lineno)
        return result

    # fba普元部分入库后更新表记录  只要有订单号即已采购
    def fba_partion_alreadly_purchased(self, obj, InAmount, hqdb_conn):
        result = {'errorcode': 0}
        try:
            hqdb_cursor = hqdb_conn.cursor()
            updateSql = "update t_stocking_demand_fba set The_arrival_of_the_number=%s,checkCompleteNum=%s,checkInferiorNum=0 where Stocking_plan_number=%s"
            parm1 = (InAmount,InAmount, obj[0])
            hqdb_cursor.execute(updateSql, parm1)
            hqdb_cursor.execute("commit")
            hqdb_cursor.close()
            self.Recordlog("update fab part sucess", "info", sys._getframe().f_lineno)
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            self.Recordlog("fba_partion_alreadly_purchased:" + result['errortext'], "info", sys._getframe().f_lineno)
        return result

    # fba获取普元备注，备注修改
    def fba_update_remark(self, obj,Remark, hqdb_conn):
        result = {'errorcode': 0, 'errortext': ''}
        try:
            hqdb_cursor = hqdb_conn.cursor()
            updateSql = "update t_stocking_demand_fba set pyRemark=%s " \
                        "where Stocking_plan_number=%s"
            parm1 = (Remark, obj[0])
            hqdb_cursor.execute(updateSql, parm1)
            hqdb_cursor.execute("commit")
            hqdb_cursor.close()
            self.Recordlog("update remark sucess", "info", sys._getframe().f_lineno)
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            self.Recordlog("fba_update_remark:" + result['errortext'], "info", sys._getframe().f_lineno)
        return result

    # 同步物流单号
    def syn_LogisticsNumber(self,objs,sqlserverInfo,hqdb_conn):
        result = {'errorcode': 0,'errortext':''}
        strBillNumber = ''
        try:
            for obj in objs['returnresult']:
                strBillNumber = obj[1]
                if sqlserverInfo['errorcode'] == 0:
                    str_py_selectSql = "select alibabaorderid,LogisticOrderNo from cg_stockorderm WHERE BillNumber = '%s'; " % (obj[1])
                    sqlserverInfo['py_cursor'].execute(str_py_selectSql)
                    tupple_hqdb_Logistic = sqlserverInfo['py_cursor'].fetchone()
                    if tupple_hqdb_Logistic:
                        hqdb_cursor = hqdb_conn.cursor()
                        updateSql = "update t_stocking_purchase_order set Ali_number=%s,LogisticsNumber=%s where Single_number=%s"
                        parm = (tupple_hqdb_Logistic[0],tupple_hqdb_Logistic[1],obj[1])
                        hqdb_cursor.execute(updateSql,parm)
                        hqdb_cursor.close()
                        hqdb_conn.commit()
                        self.Recordlog("syn_LogisticsNumber:Stocking_plan_number=" + obj[0] + ";update success", "info",sys._getframe().f_lineno)
                    result['errortext'] = 'success'
                else:
                    result['errorcode'] = -2
                    result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s,connect fail' % (Exception, ex, sys._getframe().f_lineno)
                    break
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            self.Recordlog("syn_LogisticsNumber:" + strBillNumber + result['errortext'] + ";update fail", "error",sys._getframe().f_lineno)
        return result

    # fba同步物流单号
    def syn_fba_LogisticsNumber(self, objs, sqlserverInfo, hqdb_conn):
        result = {'errorcode': 0, 'errortext': ''}
        strBillNumber = ''
        try:
            for obj in objs['returnresult']:
                strBillNumber = obj[1]
                if sqlserverInfo['errorcode'] == 0:
                    str_py_selectSql = "select alibabaorderid,LogisticOrderNo from cg_stockorderm WHERE BillNumber = '%s'; " % (
                    obj[1])
                    sqlserverInfo['py_cursor'].execute(str_py_selectSql)
                    tupple_hqdb_Logistic = sqlserverInfo['py_cursor'].fetchone()
                    if tupple_hqdb_Logistic:
                        hqdb_cursor = hqdb_conn.cursor()
                        updateSql = "update t_stocking_demand_fba set Ali_number=%s,LogisticsNumber=%s where Single_number=%s"
                        parm = (tupple_hqdb_Logistic[0], tupple_hqdb_Logistic[1], obj[1])
                        hqdb_cursor.execute(updateSql, parm)
                        hqdb_cursor.close()
                        hqdb_conn.commit()
                        self.Recordlog("syn_fba_LogisticsNumber:Stocking_plan_number=" + obj[0] + ";update success",
                                       "info", sys._getframe().f_lineno)
                    result['errortext'] = 'success'
                else:
                    result['errorcode'] = -2
                    result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s,connect fail' % (
                    Exception, ex, sys._getframe().f_lineno)
                    break
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            self.Recordlog("syn_LogisticsNumber:" + strBillNumber + result['errortext'] + ";update fail", "error",
                           sys._getframe().f_lineno)
        return result

    #同步到货状况
    def syn_purchase_data(self,objs,sqlserverInfo,hqdb_conn):
        result = {'errorcode': 0,'errortext':'','count':0}
        try:
            nRow = 0
            for row in objs['returnresult']:
                # 入库已审核
                dic_return_complete_py_data = self.get_py_complete_purchase(sqlserverInfo, row[1], row[3])
                if dic_return_complete_py_data['errorcode'] == 0:
                    if dic_return_complete_py_data['returnresult']:
                        OrderAmount = dic_return_complete_py_data['returnresult'][0]
                        InAmount = dic_return_complete_py_data['returnresult'][1]
                        if InAmount == 0:  # 入库数量为0  未入库
                            self.not_purchased(row,hqdb_conn)
                        elif InAmount < OrderAmount:  # 部分入库
                            self.partion_alreadly_purchased(row, InAmount,hqdb_conn)
                        else:
                            self.alreadly_purchased(row, InAmount,hqdb_conn)
                        nRow += 1
                    else:
                        # 采购已审核未完全入库
                        # dic_return_uncomplete_py_data = self.get_py_uncomplete_purchase(sqlserverInfo, row[1],row[3])
                        continue
                else:
                    self.Recordlog("dic_return_complete_py_data:" + row[0] + dic_return_complete_py_data['errortext'] , "error",sys._getframe().f_lineno)
                    continue
            result['count'] = nRow
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            self.Recordlog("dic_return_complete_py_data:" + result['errortext'], "error",
                           sys._getframe().f_lineno)
        return result

    # fba同步到货状况
    def syn_fba_purchase_data(self, objs, sqlserverInfo, hqdb_conn):
        result = {'errorcode': 0, 'errortext': '', 'count': 0}
        try:
            nRow = 0
            for row in objs['returnresult']:
                # 入库已审核
                dic_return_complete_py_data = self.get_py_complete_purchase(sqlserverInfo, row[1], row[3])
                dic_return_complete_memo_py_data = self.get_py_complete_purchase_memo(sqlserverInfo, row[1], row[3])
                if dic_return_complete_py_data['errorcode'] == 0 and dic_return_complete_memo_py_data['errorcode'] == 0:
                    #获取普元备注
                    if dic_return_complete_memo_py_data['returnresult']:
                        self.fba_update_remark(row, dic_return_complete_memo_py_data['returnresult'][0], hqdb_conn)
                    if dic_return_complete_py_data['returnresult']:
                        OrderAmount = dic_return_complete_py_data['returnresult'][0]
                        InAmount = dic_return_complete_py_data['returnresult'][1]
                        if InAmount == 0:  # 入库数量为0  未入库
                            self.fba_not_purchased(row, hqdb_conn)
                        elif InAmount < OrderAmount:  # 部分入库
                            self.fba_partion_alreadly_purchased(row, InAmount, hqdb_conn)
                        else:
                            self.fba_alreadly_purchased(row, InAmount, hqdb_conn)
                        nRow += 1
                    else:
                        # 采购已审核未完全入库
                        # dic_return_uncomplete_py_data = self.get_py_uncomplete_purchase(sqlserverInfo, row[1],row[3])
                        continue
                else:
                    self.Recordlog(
                        "syn_fba_purchase_data:" + row[0] + dic_return_complete_py_data['errortext'], "error",
                        sys._getframe().f_lineno)
                    continue
            result['count'] = nRow
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            self.Recordlog("syn_fba_purchase_data:" + result['errortext'], "error",
                           sys._getframe().f_lineno)
        return result

    # fba同步转退状况  objs：ProductSKU,RejectNumber(退货单号),PurchaseOrderNum(采购单号),RejectNum(退货数量), ReturnNumber(退货单号),isCheckTranReturn 1次品转退  0正常转退
    def syn_fba_reject_data(self, objs, sqlserverInfo, hqdb_conn):
        result = {'errorcode': 0, 'errortext': '', 'count': 0}
        try:
            nRow = 0
            hqdb_cursor = hqdb_conn.cursor()
            for row in objs['returnresult']:
                # 入库已审核
                dic_return_complete_py_data = self.get_py_complete_purchase(sqlserverInfo, row[4], row[0])
                #print dic_return_complete_py_data
                if dic_return_complete_py_data['errorcode'] == 0:
                    if dic_return_complete_py_data['returnresult']:
                        OrderAmount = dic_return_complete_py_data['returnresult'][0]
                        RejectAmount = dic_return_complete_py_data['returnresult'][1]
                        #更新退货表中的数量
                        strUpdateReject = "update t_stocking_reject_fba set ActualRejectNum=%s,Status='completereject' where RejectNumber='%s'"%(RejectAmount,row[1])
                        #print strUpdateReject
                        hqdb_cursor.execute(strUpdateReject)
                        if row[5] is not None and int(row[5]) == 1: #次品不需要更新备货数据，在备货已更新
                            continue
                        #备货需求表合格总数量修改
                        strSelectDemand = "select Stocking_plan_number,checkCompleteNum,tranReturnNum,deliverNum,Remarks from t_stocking_demand_fba where ProductSKU='%s' and Single_number='%s'"%(row[0],row[2])
                        hqdb_cursor.execute(strSelectDemand)
                        tupple_hqdb_DemandInfo = hqdb_cursor.fetchone()
                        #print tupple_hqdb_DemandInfo
                        if tupple_hqdb_DemandInfo:
                            checkCompleteNum = (tupple_hqdb_DemandInfo[1]-RejectAmount) if tupple_hqdb_DemandInfo[1] is not None else (0-RejectAmount)
                            tranReturnNum = (tupple_hqdb_DemandInfo[2]+RejectAmount) if tupple_hqdb_DemandInfo[2] is not None else RejectAmount
                            Remarks = (tupple_hqdb_DemandInfo[4]+u"转退数量对备货和发货数量已扣减") if tupple_hqdb_DemandInfo[4] is not None else u"转退数量对备货数量已扣减"
                            strUpdateDemand = "update t_stocking_demand_fba set checkCompleteNum=%s,tranReturnNum=%s,deliverNum=%s,Remarks='%s' where ProductSKU='%s' and Single_number='%s'" % (
                                checkCompleteNum,tranReturnNum,checkCompleteNum,Remarks,row[0],row[2])
                            hqdb_cursor.execute(strUpdateDemand)
                            #对已发货的数据记录修改
                            strSelectDeliver = "select id,Delivery_lot_number,Stocking_plan_number,All_ProductSKU_Num " \
                                              "from t_stocking_demand_fba_deliver where Stocking_plan_number like '%%%%%s%%%%' and All_ProductSKU_Num like '%%%%%s%%%%'"%(tupple_hqdb_DemandInfo[0],row[0])
                            hqdb_cursor.execute(strSelectDeliver,())
                            tupple_hqdb_DeliverInfo = hqdb_cursor.fetchone()
                            if tupple_hqdb_DeliverInfo:
                                SKUList = tupple_hqdb_DeliverInfo[3].split(';')
                                strAllSKU = ''
                                for oneSku in SKUList:
                                    strTmp = oneSku
                                    if str(row[0]) in oneSku:
                                        tmpList = oneSku.split('*')
                                        strTmp = str(tmpList[0]) + "*" + str(int(tmpList[1])-int(RejectAmount))
                                    strAllSKU = strAllSKU + strTmp + ";"
                                strUpdateDemand = "update t_stocking_demand_fba_deliver set All_ProductSKU_Num='%s' where id=%s" % (strAllSKU[0:-1],tupple_hqdb_DeliverInfo[0])
                                hqdb_cursor.execute(strUpdateDemand)
                        nRow += 1
                    else:
                        #
                        # dic_return_uncomplete_py_data = self.get_py_uncomplete_purchase(sqlserverInfo, row[1],row[3])
                        continue
                else:
                    self.Recordlog("syn_fba_reject_data:" + row[0] + dic_return_complete_py_data['errortext'], "error",sys._getframe().f_lineno)
                    continue
            result['count'] = nRow
            hqdb_cursor.close()
            hqdb_conn.commit()
        except Exception, ex:
            hqdb_cursor.close()
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            self.Recordlog("syn_fba_reject_data:" + result['errortext'], "error",
                           sys._getframe().f_lineno)
        return result

    def deal_purchase_data(self):
        result = {'errorcode': 0,'errortext':'','count':0}
        try:
            self.Recordlog("start deal:" , "info",sys._getframe().f_lineno)
            pyconn = py_conn()
            sqlserverInfo = pyconn.py_conn_database()
            hqdb_conn = connection
            #hqdb_conn = MySQLdb.Connect('192.168.105.111', 'root', 'root123', 'hq', charset='utf8')
            #hqdb_conn = MySQLdb.Connect('hequskuapp.mysql.rds.aliyuncs.com', 'by15161458383','K120Esc1', 'hq_db',charset="utf8")
            if sqlserverInfo['errorcode'] == 0 and hqdb_conn is not None:
                #同步物理单号
                dic_return_hqdb_data_01 = self.get_hqdb_purchase(hqdb_conn)
                dic_return_hqdb_data = dic_return_hqdb_data_01
                if dic_return_hqdb_data_01['errorcode'] == 0 and len(dic_return_hqdb_data_01['returnresult']) > 0:
                    tmp = self.syn_LogisticsNumber(dic_return_hqdb_data_01,sqlserverInfo,hqdb_conn)
                    if tmp['errorcode'] != 0:
                        result['errorcode'] = tmp['errorcode']
                        result['errortext'] = tmp['errortext']
                        self.Recordlog("syn_LogisticsNumber:" + result['errortext'], "error", sys._getframe().f_lineno)
                #获取online系统采购记录
                if dic_return_hqdb_data['errorcode'] == 0 and len(dic_return_hqdb_data_01['returnresult']) > 0:
                    tmp = self.syn_purchase_data(dic_return_hqdb_data,sqlserverInfo,hqdb_conn)
                    if tmp['errorcode'] != 0:
                        result['errorcode'] = tmp['errorcode']
                        result['errortext'] = tmp['errortext']
                        result['count'] = tmp['count']
                        self.Recordlog("syn_purchase_data:" + result['errortext'], "error", sys._getframe().f_lineno)
            else:
                result['errorcode'] = sqlserverInfo['errorcode']
                result['errortext'] = '__LINE__=%s,connect fail' % (sys._getframe().f_lineno)
                result['count'] = 0
                self.Recordlog("deal_purchase_data:" + "connect fail", "info", sys._getframe().f_lineno)
            hqdb_conn.close()
            pyconn.py_close_conn_database()
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            result['count'] = 0
            pyconn.py_close_conn_database()
            self.Recordlog("deal_purchase_data:" + str(ex), "info", sys._getframe().f_lineno)
        self.Recordlog("end deal:", "info", sys._getframe().f_lineno)
        return result

    def deal_fba_purchase_data(self):
        result = {'errorcode': 0, 'errortext': '', 'count': 0}
        try:
            self.Recordlog("start deal fba:", "info", sys._getframe().f_lineno)
            pyconn = py_conn()
            sqlserverInfo = pyconn.py_conn_database()
            hqdb_conn = connection
            #hqdb_conn = MySQLdb.Connect('192.168.105.111', 'root', 'root123', 'hq', charset='utf8')
            # hqdb_conn = MySQLdb.Connect('hequskuapp.mysql.rds.aliyuncs.com', 'by15161458383','K120Esc1', 'hq_db',charset="utf8")
            if sqlserverInfo['errorcode'] == 0 and hqdb_conn is not None:
                # 同步物理单号
                dic_return_hqdb_fba_data_01 = self.get_hqdb_fba_purchase(hqdb_conn)
                print  dic_return_hqdb_fba_data_01
                dic_return_hqdb_fba_data = dic_return_hqdb_fba_data_01
                if dic_return_hqdb_fba_data_01['errorcode'] == 0 and len(dic_return_hqdb_fba_data_01['returnresult']) > 0:
                    tmp = self.syn_fba_LogisticsNumber(dic_return_hqdb_fba_data_01, sqlserverInfo, hqdb_conn)
                    if tmp['errorcode'] != 0:
                        result['errorcode'] = tmp['errorcode']
                        result['errortext'] = tmp['errortext']
                        self.Recordlog("syn_LogisticsNumber:" + result['errortext'], "error", sys._getframe().f_lineno)
                # 获取online系统采购记录
                if dic_return_hqdb_fba_data['errorcode'] == 0 and len(dic_return_hqdb_fba_data['returnresult']) > 0:
                    tmp = self.syn_fba_purchase_data(dic_return_hqdb_fba_data, sqlserverInfo, hqdb_conn)
                    if tmp['errorcode'] != 0:
                        result['errorcode'] = tmp['errorcode']
                        result['errortext'] = tmp['errortext']
                        result['count'] = tmp['count']
                        self.Recordlog("syn_fba_purchase_data:" + result['errortext'], "error", sys._getframe().f_lineno)
            else:
                result['errorcode'] = sqlserverInfo['errorcode']
                result['errortext'] = '__LINE__=%s,connect fail' % (sys._getframe().f_lineno)
                result['count'] = 0
                self.Recordlog("deal_fba_purchase_data:" + "connect fail", "info", sys._getframe().f_lineno)
            hqdb_conn.close()
            pyconn.py_close_conn_database()
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            result['count'] = 0
            pyconn.py_close_conn_database()
            self.Recordlog("deal_fba_purchase_data:" + str(ex), "info", sys._getframe().f_lineno)
        self.Recordlog("end deal:", "info", sys._getframe().f_lineno)
        return result

    #退货后台处理
    def deal_fba_reject_data(self):
        result = {'errorcode': 0, 'errortext': '', 'count': 0}
        try:
            self.Recordlog("start deal fba_reject:", "info", sys._getframe().f_lineno)
            pyconn = py_conn()
            sqlserverInfo = pyconn.py_conn_database()
            hqdb_conn = connection
            #hqdb_conn = MySQLdb.Connect('192.168.105.111', 'root', 'root123', 'hq', charset='utf8')
            #hqdb_conn = MySQLdb.Connect('hequskuapp.mysql.rds.aliyuncs.com', 'by15161458383','K120Esc1', 'hq_db',charset="utf8")
            if sqlserverInfo['errorcode'] == 0 and hqdb_conn is not None:
                # 获取online系统转退记录
                dic_return_hqdb_fba_reject_data = self.get_hqdb_fba_reject(hqdb_conn)
                # 获取普元转退数量 select ProductSKU,RejectNumber,PurchaseOrderNum,RejectNum, ReturnNumber,isCheckTranReturn
                if dic_return_hqdb_fba_reject_data['errorcode'] == 0 and len(dic_return_hqdb_fba_reject_data['returnresult']) > 0:
                    tmp = self.syn_fba_reject_data(dic_return_hqdb_fba_reject_data, sqlserverInfo, hqdb_conn)
                    if tmp['errorcode'] != 0:
                        result['errorcode'] = tmp['errorcode']
                        result['errortext'] = tmp['errortext']
                        result['count'] = tmp['count']
                        self.Recordlog("deal_fba_reject_data:" + result['errortext'], "error", sys._getframe().f_lineno)
            else:
                result['errorcode'] = sqlserverInfo['errorcode']
                result['errortext'] = '__LINE__=%s,connect fail' % (sys._getframe().f_lineno)
                result['count'] = 0
                self.Recordlog("deal_fba_reject_data:" + "connect fail", "info", sys._getframe().f_lineno)
            hqdb_conn.close()
            pyconn.py_close_conn_database()
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            result['count'] = 0
            pyconn.py_close_conn_database()
            self.Recordlog("deal_fba_reject_data:" + str(ex), "info", sys._getframe().f_lineno)
        self.Recordlog("end deal:", "info", sys._getframe().f_lineno)
        return result
