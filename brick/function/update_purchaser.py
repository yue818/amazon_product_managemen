# -*-coding:utf-8-*-
"""
 @desc:
 @author: changyang
 @site:
 @software: PyCharm
 @file: report.py
 @time: 2018-03-23 14:15
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import pymssql
import MySQLdb
import datetime
from updatetasklog import updatetasklog

class update_purchaser(object):
    def __init__(self):
        self.pyuanConn = pymssql.connect(host='122.226.216.10', port=18793, user='fancyqube', password='K120Esc1',
                                         database='ShopElf', charset='utf8')
        self.onlineConn = MySQLdb.connect(user="by15161458383",passwd="K120Esc1",host="rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com",db="py_db",port=3306,charset='utf8')


    def checkifrun(self, purchaser):
        sql = '''select * from hq_db.djcelery_tasklog where runstart>=date_sub(sysdate(),INTERVAL 10 minute) and task_name='getdata' and args=%s limit 1'''

        cursor = self.onlineConn.cursor()
        cursor.execute(sql, (purchaser,))
        if cursor.rowcount > 0:
            cursor.close()
            return 1
        else:
            cursor.close()
            return 0

    def getdata(self, purchaser):
        #检查是否重复跑
        if self.checkifrun(purchaser) == 1:
            return
        # 从普源取数据
        try:
            taskid = updatetasklog(conn=self.onlineConn, args=purchaser, exectype=1)

            SQL = '''with Goods as 
            (
            select  gs.nid  as GoodsSKUID,gs.SKU,g.Purchaser,gs.maxnum,gs.minnum,g.sellDays,
            gs.CostPrice,g.CostPrice as CostPrice1,gs.GoodsSKUStatus,g.LinkUrl5
            from B_GoodsSKU(nolock) gs, B_Goods(nolock) g                  
            where g.NID=gs.GoodsID
            and g.used=0 and g.Purchaser='%s' 
            ),
            /*采购未入库数*/--已完全入库订单商品
            InStoreD as 
            (  
            select  om.NID as StockOrderID, m.StoreID, d.GoodsSKUID, sum(d.Amount) as Number   
            from CG_StockInD(nolock) d    
            inner join CG_StockInM(nolock) m on d.StockInNID = m.NID and m.StoreID=19  
            inner  join Goods g on d.GoodsSKUID = g.GoodsSKUID     
            left join CG_StockOrderM(nolock) om on m.StockOrder = om.BillNumber    
            where m.CheckFlag = 1 and m.MakeDate > (GETDATE()-365)    
            group by om.NID, m.StoreID, d.GoodsSKUID
            ),
            --未入库商品    
            UnInStore AS
            ( 
            select  d.GoodsSKUID,  m.StoreID,    
            SUM(case when (d.Amount - isnull(id.Number,0)) <= 0 then null else (d.Amount - isnull(id.Number,0)) end ) as UnInNum   
            from CG_StockOrderD(nolock) d    
            inner join Goods g on d.GoodsSKUID = g.GoodsSKUID    
            left join CG_StockOrderM(nolock) m on d.StockOrderNID = m.NID    
            left join InStoreD id on d.StockOrderNID = id.StockOrderID and d.GoodsSKUID = id.GoodsSKUID and id.StoreID=m.StoreID    
            where   m.MakeDate > (GETDATE()-365) and  (m.CheckFlag = 1)--审核通过的订单    
            and (m.Archive = 0)--不统计归档订单    
            group by d.GoodsSKUID,m.StoreID
            ),
            UnPaiDNum as (
            SELECT GoodsSKUID, SUM(SaleNum) AS UnPaiDNum,SUM(SalereNum) AS SalereNum, StoreID      
            FROM (    
                    SELECT gs.GoodsSKUID,     
                    SUM(ptd.L_QTY) AS SaleNum,    
                    SUM(case when pt.RestoreStock=-1 then ptd.L_QTY else 0 end) AS SalereNum,ISNULL(ptd.StoreID,0)AS StoreID    
                    FROM P_TradeDt(nolock) ptd     
                    inner join P_trade(nolock) pt on pt.NID=ptd.TradeNID    
                    inner join Goods gs on gs.SKU=ptd.SKU               
                    WHERE pt.FilterFlag <= 5     
                    GROUP BY gs.GoodsSKUID,ISNULL(ptd.StoreID,0)     
                    UNION all
                    SELECT  gs.GoodsSKUID,     
                    SUM(ptdu.L_QTY) AS SaleNum,    
                    SUM(case when pt.RestoreStock=-1 then ptdu.L_QTY else 0 end) AS SalereNum, ISNULL(ptdu.StoreID,0) AS StoreID    
                    FROM P_TradeDtUn(nolock) ptdu     
                    inner join P_TradeUn(nolock) pt on pt.NID=ptdu.TradeNID     
                    inner join Goods gs on gs.SKU=ptdu.SKU         
                    WHERE pt.FilterFlag = 1                             
                    GROUP BY gs.GoodsSKUID,ISNULL(ptdu.StoreID,0)     
                    ) AS C    
            GROUP BY GoodsSKUID,StoreID
            ),
            --调拨单保存之后的预期入库    
            StockChange as 
            (    
            select cd.GoodsSKUID,sum(cd.amount) as hopenum,cm.StoreInID 
            from  KC_StockChangeD(nolock) cd     
            inner join KC_StockChangeM(nolock) cm on cm.nid=cd.StockChangenid and cm.checkflag=0  and cm.StoreInID=19  
            inner  join Goods g on cd.GoodsSKUID = g.GoodsSKUID        
            where  cm.MakeDate > (GETDATE()-45)       
            group by cd.GoodsSKUID,cm.StoreInID 
            ),
            Result as 
            (
            SELECT
            case when d.KcMaxNum=0 then g.maxnum else d.KcMaxNum end   as 'KcMaxNum',    
            case when d.KcMinNum=0 then g.minnum else d.KcMinNum end   as 'KcMinNum',    
            d.SellCount1, d.SellCount2, d.SellCount3, 
            round((d.SellCount1/7.0+d.SellCount2/15.0+d.SellCount3/30.0)/3.00,2) as 'AvgDayNum', 
            d.Number , d.ReservationNum, (d.Number-d.ReservationNum) as 'UseNumber',    
            case when g.CostPrice<>0 then g.CostPrice else g.CostPrice1 end as 'CostPrice', 
            d.Price,
            d.Money, 
            isnull(u.UnInNum,0) as 'NotInStore',
            d.Number-d.ReservationNum+isnull(u.UnInNum,0)-ISNULL(up.UnPaiDNum,0) + isnull(sc.hopenum,0)+isnull(up.SaleReNum,0) as 'hopeUseNum', 
            isnull(up.UnPaiDNum,0) as 'UnPaiDNum', 
            case when     
                     (case when d.KcMaxNum>0 then d.KcMaxNum else g.MaxNum end)    
                     -(d.Number-d.ReservationNum+isnull(up.SaleReNum,0))+    
                     (case when d.KcMinNum>0 then d.KcMinNum else g.MinNum end)    
                     -isnull(u.UnInNum,0)+ISNULL(up.UnPaiDNum,0)<0 then  0     
                     else    
                     (case when d.KcMaxNum>0 then d.KcMaxNum else g.MaxNum end)    
                     -(d.Number-d.ReservationNum+isnull(up.SaleReNum,0))+    
                     (case when d.KcMinNum>0 then d.KcMinNum else g.MinNum end)    
                     -isnull(u.UnInNum,0)+ISNULL(up.UnPaiDNum,0) end  as 'SuggestNum',
             isnull((select max(DATEDIFF(DAY,Dateadd(hour,8,bb.ORDERTIME), GETDATE()))     
                     from P_TradeDtUn(nolock) aa left join P_TradeUn(nolock) bb on aa.TradeNID = bb.NID      
                     where bb.FilterFlag = 1 and aa.SKU=g.SKU),0) as 'MaxDelayDays',
             isnull(up.SaleReNum,0) as 'SaleReNum',
            (SELECT TOP 1 bsl.LocationName FROM B_StoreLocation bsl WHERE bsl.nid = isNull(bgs.LocationID,0) ) AS 'LocationName',
            IsNull(g.GoodsSKUStatus,'') as GoodsStatus,g.Purchaser, g.SKU,g.LinkUrl5,
            round(d.Number * case when IsNull(g.CostPrice,0) <> 0 then g.CostPrice else IsNull(g.CostPrice1,0) end ,2) as AllCostPrice
            From  KC_CurrentStock(nolock) d 
            inner join Goods g on d.GoodsSKUID = g.GoodsSKUID and d.StoreID =19    
            left join UnInStore u on d.GoodsSKUID = u.GoodsSKUID and d.StoreID = u.StoreID
            left join UnPaiDNum up on up.GoodsSKUID = d.GoodsSKUID and d.StoreID = up.StoreID
            left join StockChange sc on sc.goodsskuid = d.goodsskuid and sc.storeinid = d.storeid
            left join B_GoodsSKULocation(nolock) bgs ON g.GoodsSKUID = bgs.GoodsSKUID AND bgs.StoreID =19
            )
             
            select KcMaxNum,KcMinNum,SellCount1,SellCount2,SellCount3, Number,ReservationNum,UseNumber,CostPrice,
            Price,Money,NotInStore,hopeUseNum,UnPaiDNum,SuggestNum,
            case when AvgDayNum=0.0 then case when hopeUseNum=0.0 then 0.0 when hopeUseNum <0.0 then -99999.0 else 99999.0 end 
            else round(hopeUseNum/AvgDayNum,1) end as SaleDay,
            MaxDelayDays,SaleReNum,LocationName,hopeUseNum-SellCount2 as 'StockDiff15',
            round(cast(SellCount1 as float)/nullif(cast(SellCount2 as float)-cast(SellCount1 as float),0),2) as Ratio,
            GoodsStatus,Purchaser,SKU,AllCostPrice,AvgDayNum,isnull(LinkUrl5,'无') as LinkUrl5
            from Result ''' % purchaser

            with self.pyuanConn.cursor() as cursor:
                cursor.execute(SQL)
                data = cursor.fetchall()
            self.pyuanConn.commit()

            cursor = self.onlineConn.cursor()

            # 向临时表插入需要更新的数据 :
            SQL = '''INSERT INTO py_db.kc_currentstock_sku_temp(kcMaxNum,kcMinNum,SellCount1,SellCount2,SellCount3,
                        Number,ReservationNum,UseNumber,CostPrice,Price,Money,NotInStore,hopeUseNum,
                        UnPaiDNum,SuggestNum,SaleDay,MaxDelayDays,SaleReNum,LocationName,StockDiff15,
                        Radio,GoodsStatus,Purchaser,SKU,AllCostPrice,AvgDayNum,LinkUrl5)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    '''
            cursor.executemany(SQL, data)
            self.onlineConn.commit()

            # 更新数据
            SQL = '''update py_db.kc_currentstock_sku a,py_db.kc_currentstock_sku_temp b
                    set a.kcMaxNum=b.kcMaxNum,
                    a.kcMinNum=b.kcMinNum,
                    a.SellCount1=b.SellCount1,
                    a.SellCount2=b.SellCount2,
                    a.SellCount3=b.SellCount3,
                    a.Number=b.Number,
                    a.ReservationNum=b.ReservationNum,
                    a.UseNumber=b.UseNumber,
                    a.CostPrice=b.CostPrice,
                    a.Price=b.Price,
                    a.Money=b.Money,
                    a.NotInStore=b.NotInStore,
                    a.hopeUseNum=b.hopeUseNum,
                    a.UnPaiDNum=b.UnPaiDNum,
                    a.SuggestNum=b.SuggestNum,
                    a.SaleDay=b.SaleDay,
                    a.MaxDelayDays=b.MaxDelayDays,
                    a.SaleReNum=b.SaleReNum,
                    a.LocationName=b.LocationName,
                    a.StockDiff15=b.StockDiff15,
                    a.Radio=b.Radio,
                    a.GoodsStatus=b.GoodsStatus,
                    a.Purchaser=b.Purchaser,
                    a.AllCostPrice=b.AllCostPrice,
                    a.AverageNumber=b.AvgDayNum,
                    a.LinkUrl5=b.LinkUrl5,
                    a.Updatetime=sysdate(),
                    a.OSCode = py_db.f_stockoutcheck(b.sellcount1,b.sellcount2,b.sellcount3,ifnull(b.hopeusenum,0),ifnull(b.saleday,0),ifnull(b.radio,0),a.tortinfo,a.cgcategory,a.goodsname,a.goodsstatus)
                    where a.SKU= b.SKU and a.StoreID=1 and b.Purchaser='%s' ''' % (purchaser, )

            cursor.execute(SQL)
            self.onlineConn.commit()

            #删除表的个人数据
            SQL = '''delete from py_db.kc_currentstock_sku_log_realtime where Purchaser='%s' ''' % (purchaser, )
            cursor.execute(SQL)
            self.onlineConn.commit()

            #插入新数据
            SQL = '''insert into py_db.kc_currentstock_sku_log_realtime(PODate,Purchaser,SKU,StoreName,GoodsName,SupplierName,OSCode,PurchaseLevel,PreUsedNum,NotInStore1,
                Sales7Order,Sales15Order,Sales30Order,StockNumber,Radio,SaleDay,AvgDayNum,CostPrice,UseNumber,OrderDesc,TortInfo,MainSKU,LinkUrl,Model,
                LinkUrl2,SalerName2,ReservationNum,UnPaiDNum,CreateDate,GoodsStatus,SuggestMin,SuggestMax)
                Select CURDATE() as PODate,Purchaser,SKU,'浦江仓库' as StoreName,a.GoodsName,a.SupplierName,a.OSCode,b.FirstClass,HopeUseNum,
                NotInStore,SellCount1,SellCount2,SellCount3,Number,Radio,SaleDay,AverageNumber,CostPrice,UseNumber,LinkUrl5 as OrderDesc,TortInfo,
                MainSKU,LinkUrl,Model,LinkUrl2,SalerName2,ReservationNum,UnPaiDNum,CreateDate,a.GoodsStatus,
                if(a.OSCode='OS130',b.SuggestNum,a.AverageNumber*b.SuggestMin) as SuggestMin,if(a.OSCode='OS130',b.SuggestNum,a.AverageNumber*b.SuggestMax) as SuggestMax
                from kc_currentstock_sku  a,kc_currentstock_sku_oscode b
                where a.OSCode=b.OSCode  and a.Purchaser='%s'
                and a.SKU not in (select sku from py_db.kc_currentstock_sku_log where podate=CURDATE() and PurchaseStatus='H')
                and StoreID=1 and used =0 and a.OSCode>='OS100' ''' % (purchaser, )
            cursor.execute(SQL)
            self.onlineConn.commit()

            updatetasklog(conn=self.onlineConn, taskid=taskid, exectype=2)
            print '数据更新成功!......'

        except Exception, ex:
            updatetasklog(conn=self.onlineConn, taskid=taskid, exectype=3, msg=ex.message)
            print '数据更新失败!', ex.message
        finally:
            # 删除临时表数据(临时表中间数据过渡)
            SQL = '''DELETE FROM py_db.kc_currentstock_sku_temp WHERE Purchaser='%s' ''' % (purchaser,)
            cursor.execute(SQL)
            self.onlineConn.commit()

            cursor.close()

    def closeconn(self):
        self.pyuanConn.close()
        self.onlineConn.close()


if __name__ == '__main__':
    import time
    s = time.clock()

    rep = StockData()
    rep.getdata(u'葛晶')

    rep.closeconn()

    print 'exec time:', time.clock() - s
