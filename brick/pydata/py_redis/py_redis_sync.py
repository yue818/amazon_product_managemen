# coding: utf-8
"""
@author: wangzy
@contact: 15205512335
@site:商品状态、商品库存量、占有量、7天销量、可卖天数、预计可用库存、商品库存位置  同步redis
	  预计可用库存 公式
	  预计可用库存=库存量(KC_CurrentStock.Number)-占用量(KC_CurrentStock.ReservationNum)+未入库量(redis)-未派单量(关联订单表获取)+预期入库量(调拨单关联获取)+异常订单量((关联订单表获取)
@software: PyCharm
@file: py_redis_sync.py
@time: 2018-04-27 15:21
"""
import copy
import datetime, time, calendar
import sys
from py_SynRedis_pub import py_SynRedis_pub,connRedis
import MySQLdb
from django.db import  connection
import pymssql
import ConfigParser

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'hq_db',
		'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
		'PORT': '3306',
		'USER': 'by15161458383',
		'PASSWORD': 'K120Esc1'
	},
	'mysql': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'hq',
		'HOST': '192.168.105.111',
		'PORT': '3306',
		'USER': 'root',
		'PASSWORD': 'root123'
	},
	'sqlserver': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'ShopElf',
		'HOST': '122.226.216.10',
		'PORT': '18794',
		'USER': 'fancyqube',
		'PASSWORD': 'K120Esc1'
	},
}

class py_redis_sync():
	def __init__(self):
		self.db_conn = ''
		self.sqlcursor = ''
		self.db_conn_py = ''
		self.sqlcursor_py = ''
		self.cf = ConfigParser.ConfigParser()
		#self.cf.read("py_Config.conf")
		self.cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_redis/py_Config.conf")
		self.strCurrentDate = time.strftime("%Y%m%d")
		self.logPath = self.cf.get("SynLOG", "log_path")
		self.fileHead = self.cf.get("SynLOG", "fileHead")
		self.strFileName = self.logPath + self.fileHead + self.strCurrentDate + '.log'

		self.InAndOutPATH = self.cf.get("InAndOut", "PATH")
		self.InAndOutIP = self.cf.get("InAndOut", "IP")
		self.InAndOutUSER = self.cf.get("InAndOut", "USER")
		self.InAndOutPASS = self.cf.get("InAndOut", "PASS")
		self.InAndOutPORT = self.cf.get("InAndOut", "PORT")
		self.InAndOutSPLIT = self.cf.get("InAndOut", "SPLIT")


	def Recordlog(self,message,logLevel,nLine):
		strTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		strInfo = "[" + strTime + "][" + str(__file__) + "," + str(nLine) + "," + str(logLevel) + "]:" + str(message) + "\n"
		with open(self.strFileName, 'a+') as f:
			f.write(strInfo)
		f.close()

	'''
		说明：如果本地数据库连接，需要关闭数据库
	'''
	def connSql(self, flag=0):
		if flag == 111:

			# 正式环境
			self.db_conn = connection
			self.sqlcursor = self.db_conn.cursor()
		if flag == 10:
			# 个人测试库环境(192.168.105.111)
			#self.db_conn_py = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'],DATABASES['default']['PASSWORD'],DATABASES['syn']['NAME'], charset='utf8')
			# 正式环境
			self.db_conn_py = pymssql.connect(host=DATABASES['sqlserver']['HOST'], user=DATABASES['sqlserver']['USER'], password=DATABASES['sqlserver']['PASSWORD'], database=DATABASES['sqlserver']['NAME'],port=DATABASES['sqlserver']['PORT'])
			self.sqlcursor_py = self.db_conn_py.cursor()

	'''
	说明：如果本地数据库连接，需要关闭数据库
	'''
	def closeSql(self, flag=0):
		if flag == 111:
			self.sqlcursor.close()
			self.db_conn.close()
		if flag == 10:
			self.db_conn_py.close()
			self.sqlcursor_py.close()

	'''
	说明：获取普源商品状态与mysql对应值
	'''
	def getStatusConfig(self):
		reload(sys)
		sys.setdefaultencoding('utf8')
		self.connSql(111)
		strSql = "select hq_GoodsStatus,statuscode from goodsstatus_compare"
		n = self.sqlcursor.execute(strSql)
		sArray = self.sqlcursor.fetchall()
		gDicCfg = {}
		for sRowArray in sArray:
			# print('sRowArray={}'.format(sRowArray[0]))
			gDicCfg[str(sRowArray[0])] = sRowArray[1]
		self.closeSql(111)
		return gDicCfg

	'''
	说明:写redis店铺7天销量：根据每天销量表进行统计
	'''
	def dealShopSevenSales_Syn(self):
		reload(sys)
		sys.setdefaultencoding('utf8')
		self.connSql(111)
		strSql = "select concat(ShopName,'@#@',ShopSKU),sum(SalesVolume) from t_report_sales_daily where orderday between  DATE_ADD(SYSDATE(),INTERVAL -8 DAY)  " \
				 "and DATE_ADD(SYSDATE(),INTERVAL -1 DAY) GROUP BY ShopSKU,ShopName "

		n = self.sqlcursor.execute(strSql)
		sArray = self.sqlcursor.fetchall()

		with connRedis.pipeline(transaction=False) as p:
			j = 0
			for sRowArray in sArray:
				try:
					updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
					if sRowArray[0] == "":
						continue
					# p.hset(str(sRowArray[0].encode('gb2312')), "sevensales", sRowArray[1])  #测试环境可以
					p.hset(sRowArray[0], "SevenSales", sRowArray[1])  # 正式环境
					p.hset(sRowArray[0], "SevenSales_UpdateTime", updateTime)

					if j == 20000:
						p.execute()
						j = 0
					j += 1
					# print('{},sRowArray={},i={}'.format(str(sRowArray[0].encode('gb2312')),sRowArray[0],i))
				except Exception as e:
					self.Recordlog(e.message + ";" + str(sRowArray[0]), "error", sys._getframe().f_lineno)
					continue
			p.execute()

		self.closeSql(111)
	'''
	说明：同步商品状态
	'''
	def DealGoodsStatus(self):
		try:
			reload(sys)
			sys.setdefaultencoding('utf8')
			dicConfig = self.getStatusConfig()

			self.connSql(10)
			strSql = "select sku,goodsstatus from b_goods(nolock)"
			n = self.sqlcursor_py.execute(strSql)
			tupResult = self.sqlcursor_py.fetchall()
			self.closeSql(10)
			with connRedis.pipeline(transaction=False) as p:
				j = 0
				updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
				for row in tupResult:
					try:
						# 商品状态
						if row[1] is None or row[1] == "":
							strStatus = u"停售"
						else:
							strStatus = row[1]
						nTmpStatus = dicConfig.get(str(strStatus).replace('\n', ''))
						p.hset(row[0], 'GoodsStatus', nTmpStatus)
						p.hset(row[0], 'UpdateTime', updateTime)
						j += 1
						if j == 20000:
							p.execute()
							j = 0
					except Exception as e:
						self.Recordlog(e.message + "Syn Error:SKU="+row[0], "error", sys._getframe().f_lineno)
				p.execute()
		except Exception as e:
				self.Recordlog(e.message + "sql exec error", "error", sys._getframe().f_lineno)
	'''
	说明：同步商品重量
	'''
	def DealGoodsWeight(self):
		try:
			reload(sys)
			sys.setdefaultencoding('utf8')

			self.connSql(10)
			strSql = "select sku,Weight,PackageCount from b_goods(nolock)"
			n = self.sqlcursor_py.execute(strSql)
			tupResult = self.sqlcursor_py.fetchall()
			self.closeSql(10)
			strWeight = '0'
			with connRedis.pipeline(transaction=False) as p:
				j = 0
				updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
				for row in tupResult:
					try:
						# 商品状态
						if row[1] is None or row[1] == "":
							strWeight = '0'
						else:
							strWeight = row[1]
						# 最小包装数量
						if row[2] is None or row[2] == "":
							PackageCount = '0'
						else:
							PackageCount = row[2]
						p.hset(row[0], 'Weight', strWeight)
						p.hset(row[0], 'PackageCount', PackageCount)
						p.hset(row[0], 'UpdateTime', updateTime)
						j += 1
						if j == 20000:
							p.execute()
							j = 0
					except Exception as e:
						self.Recordlog(e.message + "Syn Error:SKU="+row[0], "error", sys._getframe().f_lineno)
				p.execute()
		except Exception as e:
				self.Recordlog(e.message + "sql exec error", "error", sys._getframe().f_lineno)

	'''
	说明：根据sql语句获取：库存上线、库存下限、7天销量、15天销量、30天销量、库存量、占有量、可用数量(库存-占用)、成本价、售价、采购未入库
		预计可用库存、缺货及未派单数量、建议采购数量、可卖天数、最长采购缺货天数、缺货占用数量、库位、商品状态、采购员、商品SKU
	'''
	def GetSqlServerData(self):
		try:
			self.connSql(10)
			strSql ='''
				with Goods as 
				(
					select  gs.nid  as GoodsSKUID,gs.SKU,g.Purchaser,gs.maxnum,gs.minnum,g.sellDays,
					gs.CostPrice,g.CostPrice as CostPrice1,g.DevDate,g.CreateDate,g.GoodsStatus,g.Weight
					from B_GoodsSKU(nolock) gs , B_Goods(nolock) g                  
					where g.NID=gs.GoodsID
				),
				/*采购未入库数*/--已完全入库订单商品 
				InStoreD as 
				(  
					select  om.NID as StockOrderID, m.StoreID, d.GoodsSKUID, sum(d.Amount) as Number   
					from CG_StockInD(nolock) d    
					inner join CG_StockInM(nolock) m on d.StockInNID = m.NID and m.StoreID in(19)  
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
					inner join KC_StockChangeM(nolock) cm on cm.nid=cd.StockChangenid and cm.checkflag=0  and cm.StoreInID in(19)  
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
					d.Money, 
					u.UnInNum as 'UnInStockNum',
					d.Number-d.ReservationNum+isnull(u.UnInNum,0)-ISNULL(up.UnPaiDNum,0) + isnull(sc.hopenum,0)+isnull(up.SaleReNum,0) as 'HopeUseNum', 
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
						as 'CanSellNum',
					 isnull((select max(DATEDIFF(DAY,Dateadd(hour,8,bb.ORDERTIME), GETDATE()))     
						 from P_TradeDtUn(nolock) aa left join P_TradeUn(nolock) bb on aa.TradeNID = bb.NID      
						 where bb.FilterFlag = 1 and aa.SKU=g.SKU),0) as 'MaxPurchaseDays',isnull(up.SaleReNum,0) as 'OssNum',
					(SELECT TOP 1 bsl.LocationName    
						   FROM B_StoreLocation bsl WHERE bsl.nid = isNull(bgs.LocationID,0) ) AS 'Location',
					g.Purchaser, g.GoodsStatus, g.SKU,g.GoodsSKUID,g.Weight as 'Weight',
					case   when d.SellCount=0 then 99999 --没有销售的，直接为 0     
						else cast((d.Number-d.ReservationNum+isnull(up.SaleReNum,0))/(case when d.SellCount =0 then 1 else d.SellCount end)*
						(case when isnull(g.sellDays,0) <=0  then 1 else g.sellDays end) as dec(12,2)) end as 'canday'
					From  KC_CurrentStock(nolock) d 
					inner join Goods g on d.GoodsSKUID = g.GoodsSKUID and d.StoreID in(19)    
					left join UnInStore u on d.GoodsSKUID = u.GoodsSKUID and d.StoreID = u.StoreID
					left join UnPaiDNum up on up.GoodsSKUID = d.GoodsSKUID and d.StoreID = up.StoreID
					left join StockChange sc on sc.goodsskuid = d.goodsskuid and sc.storeinid = d.storeid
					left join B_GoodsSKULocation(nolock) bgs ON g.GoodsSKUID = bgs.GoodsSKUID AND bgs.StoreID in(19)
					--where g.SKU  in('CAR0870BK','新款自拍王白色','EAR-0738-SV\CYY','浦江仓库零配件','龙岗仓库零配件')
				)
				
				select 
					KcMaxNum, KcMinNum,Convert(NUMERIC(18,0),isnull(SellCount1,0)),SellCount2,SellCount3,Convert(NUMERIC(18,0),isnull(Number,0)),Convert(NUMERIC(18,0),isnull(ReservationNum,0)),UseNumber,Convert(NUMERIC(18,2),isnull(CostPrice,0.00)),Money,
					Convert(NUMERIC(18,0),isnull(UnInStockNum,0)),Convert(NUMERIC(18,0),isnull(HopeUseNum,0)),Convert(NUMERIC(18,0),isnull(UnPaiDNum,0)),SuggestNum,CanSellNum,MaxPurchaseDays,Convert(NUMERIC(18,0),isnull(OssNum,0)),Location,
					GoodsStatus,Purchaser,SKU,GoodsSKUID,Convert(NUMERIC(18,2),isnull(canday,99999)),Weight
				from Result
			'''
			n = self.sqlcursor_py.execute(strSql)
			tuppleResult = self.sqlcursor_py.fetchall()
			self.closeSql(10)
			return  tuppleResult
		except Exception as e:
				self.Recordlog(e.message + "sql exec error", "error", sys._getframe().f_lineno)
				return ()

	'''
	说明：根据从普源查询结果写入redis
	'''
	def dealOtherData_Syn(self):
		reload(sys)
		sys.setdefaultencoding('utf8')
		dicConfig = self.getStatusConfig()
		#print time.strftime('GetSqlServerData:%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		tuppleResult = self.GetSqlServerData()
		#print time.strftime('GetSqlServerData:%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		if len(tuppleResult) != 0:
			with connRedis.pipeline(transaction=False) as p:
				j = 0
				for row in tuppleResult:
					try:
						updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
						strSKU = row[20]
						#商品库存量
						if row[5] is None:
							p.hset(strSKU, 'Number', 0)
						else:
							p.hset(strSKU, 'Number', row[5])
						#商品占有量
						if row[6] is None:
							p.hset(strSKU, 'ReservationNum', 0)
						else:
							p.hset(strSKU, 'ReservationNum', row[6])
						#商品成本价
						p.hset(strSKU, 'CostPrice', row[8])
						# 商品7天销量
						if row[2] is None:
							p.hset(strSKU, 'SellCount1', 0)
						else:
							p.hset(strSKU, 'SellCount1', row[2])
						# 商品采购未入库
						if row[10] is None:
							p.hset(strSKU, 'NotInStore', 0)
						else:
							p.hset(strSKU, 'NotInStore', row[10])
						# 商品可卖天数
						if row[22] is None:
							p.hset(strSKU, 'CanSaleDay', 0)
						else:
							p.hset(strSKU, 'CanSaleDay', row[22])
						# 商品预计可用库存
						p.hset(strSKU, 'HopeUseNum', row[11])
						# 商品缺货及未派单数量
						p.hset(strSKU, 'UnPaiDNum', row[12])
						#商品库位
						p.hset(strSKU, 'Location', row[17])
						# 商品 刷新时间
						p.hset(strSKU, 'UpdateTime', updateTime)
						#print(row[20])
						j +=1
						if j == 20000:
							p.execute()
							j = 0
					except Exception as e:
						strInfo = "%s,SKU=%s,GoodsStatus=%s,Number=%s,ReservationNum=%s,Price=%s,SellCount1=%s,NotInStore=%s," \
								  "CanSaleDay=%s,HopeUseNum=%s,UnPaiDNum=%s,Location=%s,UpdateTime=%s"\
								  %(row[21],row[20],str(row[18]),row[5],row[6],row[8],row[2],row[10],row[14],row[11],row[12],row[17],updateTime)
						self.Recordlog(e.message + str(strInfo),"error", sys._getframe().f_lineno)
						continue
				p.execute()

	'''
	说明：调用写入redis函数
	'''
	def WriteDataToRedis(self):
		startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		self.Recordlog("dealShopSevenSales_Syn:" + startTime, "info", sys._getframe().f_lineno)
		self.dealShopSevenSales_Syn()
		startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		self.Recordlog("DealGoodsWeight_Syn:" + startTime, "info", sys._getframe().f_lineno)
		#self.DealGoodsStatus()
		self.DealGoodsWeight()
		startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		self.Recordlog("dealOtherData_Syn:" + startTime, "info", sys._getframe().f_lineno)
		self.dealOtherData_Syn()
		startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		self.Recordlog("End:" + startTime, "info", sys._getframe().f_lineno)

#test = py_redis_sync()
#test.WriteDataToRedis()


