#coding=utf-8  
import datetime
import os, oss2
import MySQLdb
import pymssql
from xlwt import *

csvkcheaders = [u"SKU码", u"商品名称", u"供应商", u"商品状态", u"商品成本单价", u"库存数量", 
                u"预计可用库存", u"7天销量", u"15天销量", u"30天销量",u"采购未入库", u"网址", 
                u"网址2",u"网址3", u"型号", u"采购员",u"缺货及未派单数量", u"占用数量", u"可用数量",
                u"网址6", u"业绩归属1", u"业绩归属2",u"建议采购数量", u"库存上限", u"库存下限",u"仓库",
                u"库位",u"建议采购", u"款式3", u"平均单价",u"库存金额", u"可卖天数", u"最低采购价格",
                u"日平均销量", u"商品类别", u"商品创建时间",u"默认发货仓库", u"商品重量(克)", 
                u"最长采购缺货天数",u"网址4", u"网址5", u"缺货占用数量",u"是否停用", u"商品成本金额",
                u"多款式网址",u"责任归属1", u"责任归属2",]
class upload_kc_to_oss(object):
    def __init__(self):
        self.onlineConn = MySQLdb.connect(user="by15161458383",passwd="K120Esc1",host="rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com",db="py_db",port=3306,charset='utf8')
        self.pyuanConn = pymssql.connect(host='122.226.216.10', port=18793, user='fancyqube', password='K120Esc1',database='ShopElf', charset='utf8')

    def uploadOss(self,username,filename):
        ossAuth=oss2.Auth('LTAIH6IHuMj6Fq2h','N5eWsbw8qBkMfPREkgF2JnTsDASelM')
        ossBucket=oss2.Bucket(ossAuth,'oss-cn-shanghai.aliyuncs.com','fancyqube-kc-csv')
        ossBucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        
        for object_info in oss2.ObjectIterator(ossBucket,prefix='%s/%s'%(username,username)):
            ossBucket.delete_object(object_info.key)
        remoteName = username + "/" + os.path.basename(filename)
        try:
            result=ossBucket.put_object_from_file(remoteName,filename)
            os.remove(filename)
            print "upload success!"
            return result
        except Exception, e:
            print "error ", e
            return -1

    def write_excel(self, Purchaser, username):
        cur = self.onlineConn.cursor()
        sql = "select * from py_db.kc_currentstock_sku where storeID = 1 and GoodsStatus != 'stop' and Purchaser='%s'"%Purchaser
        cur.execute(sql)
        numrows = int(cur.rowcount)
    
        w = Workbook()
        sheet = w.add_sheet(u'库存预警')
    
        for i in range(len(csvkcheaders)):
            sheet.write(0,i,csvkcheaders[i])
        cloumn = 0
        for i in range(1,numrows):
            rows = cur.fetchone()
            cloumn = cloumn + 1
            sheet.write(cloumn,0,rows[2])
            sheet.write(cloumn,1,rows[3])
            sheet.write(cloumn,2,rows[4])
        
            if rows[5] == 'normal':#商品状态
                sheet.write(cloumn,3,u'正常')
            elif rows[5] == 'over':
                sheet.write(cloumn,3,u'售完下架')
            elif rows[5] == 'temporary':
                sheet.write(cloumn,3,u'临时下架')
            else:
                sheet.write(cloumn,3,u'停售')
            sheet.write(cloumn,4,rows[6])
            sheet.write(cloumn,5,rows[7])
            sheet.write(cloumn,6,rows[55])
            sheet.write(cloumn,7,rows[8])
            sheet.write(cloumn,8,rows[9])
            sheet.write(cloumn,9,rows[10])
            sheet.write(cloumn,10,rows[54])
            sheet.write(cloumn,11,rows[11])
            sheet.write(cloumn,12,rows[12])
            sheet.write(cloumn,13,rows[13])
            sheet.write(cloumn,14,rows[14])
            sheet.write(cloumn,15,rows[15])
            sheet.write(cloumn,16,rows[56])
            sheet.write(cloumn,17,rows[16])
            sheet.write(cloumn,18,rows[17])
            sheet.write(cloumn,19,rows[18])
            sheet.write(cloumn,20,rows[19])
            sheet.write(cloumn,21,rows[20])
            sheet.write(cloumn,22,rows[57])
            sheet.write(cloumn,23,rows[21])
            sheet.write(cloumn,24,rows[22])
            if rows[32] == 1:#仓库
                sheet.write(cloumn,25,u'浦江仓库')
            elif rows[32] == 2:
                sheet.write(cloumn,25,u'亚马逊仓库')
            elif rows[32] == 3:
                sheet.write(cloumn,25,u'海外仓仓库')
            else:
                sheet.write(cloumn,25,u'其它仓库')
        
            sheet.write(cloumn,26,rows[23])
            if rows[53] == 'Y':#建议采购-----------------------
                sheet.write(cloumn,27,1)
            else:
                sheet.write(cloumn,27,0)
            
            sheet.write(cloumn,28,rows[24])
            sheet.write(cloumn,29,rows[25])
            sheet.write(cloumn,30,rows[26])
            sheet.write(cloumn,31,rows[27])
            sheet.write(cloumn,32,rows[28])
            sheet.write(cloumn,33,rows[29])
            sheet.write(cloumn,34,rows[30])
            sheet.write(cloumn,35,str(rows[31]))
            if rows[32] == 1:#仓库
                sheet.write(cloumn,36,u'浦江仓库')
            elif rows[32] == 2:
                sheet.write(cloumn,36,u'亚马逊仓库')
            elif rows[32] == 3:
                sheet.write(cloumn,36,u'海外仓仓库')
            else:
                sheet.write(cloumn,36,u'其它仓库')
            sheet.write(cloumn,37,rows[33])
            sheet.write(cloumn,38,rows[58])
            sheet.write(cloumn,39,rows[34])
            sheet.write(cloumn,40,rows[35])
            sheet.write(cloumn,41,rows[59])
            sheet.write(cloumn,42,rows[36])
            sheet.write(cloumn,43,rows[37])
            sheet.write(cloumn,44,rows[38])
            sheet.write(cloumn,45,rows[39])
            sheet.write(cloumn,46,rows[40])
        
        cur.close()

        filename = username + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(filename)

        return filename

    def getdata(self):
        # 从普源取数据
        SQL = '''with Goods as 
        (
        select  gs.nid  as GoodsSKUID,gs.SKU,g.Purchaser,gs.maxnum,gs.minnum,g.sellDays,
        gs.CostPrice,g.CostPrice as CostPrice1,gs.GoodsSKUStatus
        from B_GoodsSKU(nolock) gs , B_Goods(nolock) g                  
        where g.NID=gs.GoodsID
        and g.used=0
        ),
        /*采购未入库数*/--已完全入库订单商品  and g.Purchaser= 
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
        d.Number , d.ReservationNum, (d.Number-d.ReservationNum) as 'UseNumber',    
        case when g.CostPrice<>0 then g.CostPrice else g.CostPrice1 end as 'CostPrice', 
        d.Price,
        d.Money, 
        u.UnInNum as 'NotInStore',
        d.Number-d.ReservationNum+isnull(u.UnInNum,0)-ISNULL(up.UnPaiDNum,0) + isnull(sc.hopenum,0)+isnull(up.SaleReNum,0) as 'hopeUseNum', 
        up.UnPaiDNum as 'UnPaiDNum', 
        case when     
                 (case when d.KcMaxNum>0 then d.KcMaxNum else g.MaxNum end)    
                 -(d.Number-d.ReservationNum+isnull(up.SaleReNum,0))+    
                 (case when d.KcMinNum>0 then d.KcMinNum else g.MinNum end)    
                 -isnull(u.UnInNum,0)+ISNULL(up.UnPaiDNum,0)<0 then  0     
                 else    
                 (case when d.KcMaxNum>0 then d.KcMaxNum else g.MaxNum end)    
                 -(d.Number-d.ReservationNum+isnull(up.SaleReNum,0))+    
                 (case when d.KcMinNum>0 then d.KcMinNum else g.MinNum end)    
                 -isnull(u.UnInNum,0)+ISNULL(up.UnPaiDNum,0) end     
                as 'SuggestNum',
         case     
                when d.SellCount=0 then 0 --没有销售的，直接为 0     
                else     
                cast((d.Number-d.ReservationNum+isnull(up.SaleReNum,0))/    
                 (case when d.SellCount =0 then 1 else d.SellCount end)    
                 *    
                 (case when isnull(g.sellDays,0) <=0  then 1 else g.sellDays end) as dec(12,1))
                end     
                as 'SaleDay',
         isnull((select max(DATEDIFF(DAY,Dateadd(hour,8,bb.ORDERTIME), GETDATE()))     
                 from P_TradeDtUn(nolock) aa left join P_TradeUn(nolock) bb on aa.TradeNID = bb.NID      
                 where bb.FilterFlag = 1 and aa.SKU=g.SKU),0) as 'MaxDelayDays',
         isnull(up.SaleReNum,0) as 'SaleReNum',
        (SELECT TOP 1 bsl.LocationName FROM B_StoreLocation bsl WHERE bsl.nid = isNull(bgs.LocationID,0) ) AS 'LocationName',
        IsNull(g.GoodsSKUStatus,'') as GoodsStatus,g.Purchaser, g.SKU,
        round(d.Number * case when IsNull(g.CostPrice,0) <> 0 then g.CostPrice else IsNull(g.CostPrice1,0) end ,2)as AllCostPrice
        From  KC_CurrentStock(nolock) d 
        inner join Goods g on d.GoodsSKUID = g.GoodsSKUID and d.StoreID =19    
        left join UnInStore u on d.GoodsSKUID = u.GoodsSKUID and d.StoreID = u.StoreID
        left join UnPaiDNum up on up.GoodsSKUID = d.GoodsSKUID and d.StoreID = up.StoreID
        left join StockChange sc on sc.goodsskuid = d.goodsskuid and sc.storeinid = d.storeid
        left join B_GoodsSKULocation(nolock) bgs ON g.GoodsSKUID = bgs.GoodsSKUID AND bgs.StoreID =19
        )

        select KcMaxNum,KcMinNum,SellCount1,SellCount2,SellCount3, Number,ReservationNum,UseNumber,CostPrice,
        Price,Money,NotInStore,hopeUseNum,UnPaiDNum,SuggestNum,SaleDay,MaxDelayDays,SaleReNum,LocationName,
        hopeUseNum-SellCount2 as 'StockDiff15',case when SaleDay<=3 then 'Y' else 'N' end as 'IsCg',
        round(cast(SellCount1 as float)/nullif(cast(SellCount2 as float)-cast(SellCount1 as float),0),2) as Ratio,
        case when GoodsStatus in ('在售','正常') then 'normal'
        when GoodsStatus in ('清仓','清仓(合并)','处理库尾','组合') then 'stop'
        when GoodsStatus = '售完下架' then 'over'
        when GoodsStatus = '临时下架' then 'temporary' end as GoodsStatus,Purchaser,SKU,AllCostPrice
        from Result '''

        with self.pyuanConn.cursor() as cursor:
            cursor.execute(SQL)
            data = cursor.fetchall()
        self.pyuanConn.commit()

        cursor = self.onlineConn.cursor()

        # 删除临时表数据(临时表中间数据过渡)
        SQL = '''truncate table py_db.kc_currentstock_sku_temp '''
        cursor.execute(SQL)
        self.onlineConn.commit()

        # 向临时表插入需要更新的数据
        SQL = '''INSERT INTO py_db.kc_currentstock_sku_temp(kcMaxNum,kcMinNum,SellCount1,SellCount2,SellCount3,
                    Number,ReservationNum,UseNumber,CostPrice,Price,Money,NotInStore,hopeUseNum,
                    UnPaiDNum,SuggestNum,SaleDay,MaxDelayDays,SaleReNum,LocationName,StockDiff15,
                    IsCg,Radio,GoodsStatus,Purchaser,SKU,AllCostPrice)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                '''
        cursor.executemany(SQL, data)
        self.onlineConn.commit()

        # 采购员先置空where Purchaser='%s' and  StoreID=1'''% (purchaser, )
        SQL = '''update py_db.kc_currentstock_sku set Purchaser='' where StoreID=1 and Used=0 '''
        cursor.execute(SQL)
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
                a.IsCg=b.IsCg,
                a.Radio=b.Radio,
                a.GoodsStatus=b.GoodsStatus,
                a.Purchaser=b.Purchaser,
                a.AllCostPrice=b.AllCostPrice,
                a.Updatetime=sysdate()
                where a.SKU= b.SKU and a.StoreID=1'''

        cursor.execute(SQL)
        self.onlineConn.commit()

        cursor.close()

    def main(self):
        self.getdata()

        SQL='''select a.Purchaser,b.username
                from py_db.cg_purchaser a ,hq_db.auth_user b
                where a.Purchaser=b.first_name'''
        cursor = self.onlineConn.cursor()

        cursor.execute(SQL)
        data = cursor.fetchall()

        for purchaser, username in data:
            filename = self.write_excel(purchaser, username)
            self.uploadOss(username, filename)

        self.closeconn()

    def closeconn(self):
        self.pyuanConn.close()
        self.onlineConn.close()


if __name__ == '__main__':

    rep = upload_kc_to_oss()
    rep.main()