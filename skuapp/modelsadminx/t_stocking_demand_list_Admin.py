# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_list_Admin.py
 @time: 2017-12-19 14:47

"""
from xadmin.layout import Fieldset, Row
import datetime as tmpDate,random
from pyapp.models import b_goods as py_b_goods,B_Supplier as py_b_Supplier
from skuapp.table.t_stocking_purchase_order import t_stocking_purchase_order
from django.contrib import messages
from django.utils.safestring import mark_safe
from datetime import datetime as ddtime
from skuapp.table.public import *
from skuapp.table.t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
from django.db import connection as hqdb_conn

class t_stocking_demand_list_Admin(object):
    search_box_flag = True
    importfile_plugin =True
    jump_temp = False
    site_left_menu_stocking_purchase = True
    def show_ProductImage(self,obj) :
        rt =  '<img src="%s"  width="120" height="120"/>  '%(obj.ProductImage)
        return mark_safe(rt)
    show_ProductImage.short_description = u'商品图片'

    def show_Status(self, obj):
        try:
            rt = ""
            strStatus = ""
            diffDate = 0
            for status in getChoices(ChoicePlanStatus):
                if status[0] == obj.Status:
                    strStatus = status[1]
                    break
            if (obj.Status == 'notgenerated' ) or (obj.Status == 'back' ) or (obj.Status == 'noaudit'):
                flag = 1 if ((obj.Stock_plan_date is not None) and (str(ddtime.now()) > str(obj.Stock_plan_date + tmpDate.timedelta(days=1)))) else 0
                diffDate = (ddtime.now() - obj.Stock_plan_date).days if obj.Stock_plan_date is not None else 0
                if flag == 1:
                    rt = '<div class="box" style="width: 150px;height: 80px;background-color: red;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (strStatus,diffDate)
                else:
                    rt = '<div class="box" style="width: 150px;height: 80px;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (strStatus,diffDate)
            elif  obj.Status == 'audit':
                diffDate = (ddtime.now() - obj.AuditTime).days if obj.AuditTime is not None else 0
                flag = 1 if ((obj.AuditTime is not None) and (str(ddtime.now()) > str(obj.AuditTime + tmpDate.timedelta(days=2)))) else 0
                if flag == 1:
                    rt = '<div class="box" style="width: 150px;height: 80px;background-color: red;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (strStatus,diffDate)
                else:
                    rt = '<div class="box" style="width: 150px;height: 80px;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (strStatus,diffDate)
            elif  obj.Status == 'notpurchased':
                diffDate = (ddtime.now() - obj.genPurchasePlanDate).days if obj.genPurchasePlanDate is not None else 0
                strStatus = u'计划已生成,未采购'
                flag = 1 if ((obj.genPurchasePlanDate is not None) and  (str(ddtime.now()) > str(obj.genPurchasePlanDate + tmpDate.timedelta(days=2)))) else 0
                if flag == 1:
                    rt = '<div class="box" style="width: 150px;height: 80px;background-color: red;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (strStatus,diffDate)
                else:
                    rt = '<div class="box" style="width: 150px;height: 80px;text-align: center;line-height: 20px;border-radius: 4px"><br>%s<br>超期%s天</div>' % (strStatus,diffDate)
            else:
                rt = strStatus
        except Exception, ex:
            messages.info(self.request,"采购状态加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_Status.short_description = mark_safe('<p align="center" style="width:120px;color:#428bca;">采购状态</p>')

    def show_opInfo(self, obj):
        try:
            rt = u'<table border="1"><tr><th>操作员</th><th>告警信息</th><th>操作时间</th></tr>'
            if obj.Status == 'notgenerated' or obj.Status == 'back' or obj.Status == 'noaudit':
                #rt = u'<div style="width:120px"><strong>计划需求人:</strong>%s' % (obj.Demand_people)
                diffDate1 = (ddtime.now() - obj.Stock_plan_date).days if obj.Stock_plan_date is not None else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>'%(obj.Demand_people,diffDate1,obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
            elif  obj.Status == 'audit':
                diffDate1 = (obj.AuditTime - obj.Stock_plan_date).days if (obj.AuditTime is not None and obj.Stock_plan_date is not None) else 0
                diffDate2 = (ddtime.now() - obj.AuditTime ).days if (obj.AuditTime is not None ) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                if diffDate2 > 2:
                    rt = rt + u'<tr style="color:red"><th>审核:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Auditor, diffDate2, obj.AuditTime)
                else:
                    rt = rt + u'<tr style=""><th>审核:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Auditor, diffDate2, obj.AuditTime)
            elif  obj.Status == 'notpurchased':
                diffDate1 = (obj.AuditTime - obj.Stock_plan_date).days if (obj.AuditTime is not None and obj.Stock_plan_date is not None) else 0
                diffDate2 = (obj.genPurchasePlanDate - obj.AuditTime).days if (obj.AuditTime is not None and obj.genPurchasePlanDate is not None) else 0
                diffDate3 = (ddtime.now() - obj.genPurchasePlanDate).days if (obj.genPurchasePlanDate is not None)  else 0
                if diffDate1 > 2:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                if diffDate2 > 2:
                    rt = rt + u'<tr style="color:red"><th>审核:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Auditor, diffDate2, obj.AuditTime)
                else:
                    rt = rt + u'<tr style=""><th>审核:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Auditor, diffDate2, obj.AuditTime)
                if diffDate3 > 2:
                    rt = rt + u'<tr style="color:red"><th>生成采购:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.genPurchasePlanMan, diffDate3, obj.genPurchasePlanDate)
                else:
                    rt = rt + u'<tr style=""><th>生成采购:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.genPurchasePlanMan, diffDate3, obj.genPurchasePlanDate)
            elif  obj.Status == 'already':
                diffDate1 = (obj.AuditTime - obj.Stock_plan_date).days if (obj.AuditTime is not None and obj.Stock_plan_date is not None) else 0
                diffDate2 = (obj.genPurchasePlanDate - obj.AuditTime).days if (obj.AuditTime is not None and obj.genPurchasePlanDate is not None) else 0
                diffDate3 = (obj.completePurchaseDate - obj.genPurchasePlanDate).days if (obj.genPurchasePlanDate is not None and obj.completePurchaseDate is not None) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people,diffDate1, obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people,diffDate1, obj.Stock_plan_date)
                if diffDate2 > 2:
                    rt = rt + u'<tr style="color:red"><th>审核:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Auditor,diffDate2, obj.AuditTime)
                else:
                    rt = rt + u'<tr style=""><th>审核:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.Auditor,diffDate2, obj.AuditTime)
                if diffDate3 > 2:
                    rt = rt + u'<tr style="color:red"><th>生成采购:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.genPurchasePlanMan,diffDate3, obj.genPurchasePlanDate)
                else:
                    rt = rt + u'<tr style=""><th>生成采购:%s</th><th>延迟%s天</th><th>%s</th></tr>' % (obj.genPurchasePlanMan,diffDate3, obj.genPurchasePlanDate)
                if obj.completePurchaseMan:
                    rt = rt + u'<tr style=""><th>完成采购:%s</th><th></th><th>%s</th></tr>' % (obj.completePurchaseMan, obj.completePurchaseDate)
            rt = rt + "</table>"
        except Exception, ex:
            messages.info(self.request,"操作记录加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_opInfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">操作记录信息</p>')

    def show_opTimeInfo(self, obj):
        try:
            rt = ""
            if obj.Status == 'notgenerated':
                rt = u'<div style="width:200px"><strong>计划生成时间:</strong>%s<div>'%(obj.Stock_plan_date)
            elif obj.Status == 'back' :
                rt = u'<strong>计划需求人:</strong>%s<br><strong>计划生成时间:</strong>%s<br><strong>提交审核人:</strong>%s<br><strong>提交审核时间:</strong>%s<br><strong>审核不通过人:</strong>%s<br><strong>审核不通过时间:</strong>%s' % (
                obj.Demand_people, obj.Stock_plan_date,obj.submitAuditMan,obj.submitAuditDate,obj.Auditor,obj.AuditTime)
            elif  obj.Status == 'noaudit':
                rt = u'<strong>计划需求人:</strong>%s<br><strong>计划生成时间:</strong>%s<br><strong>提交审核人:</strong>%s<br><strong>提交审核时间:</strong>%s' % (
                    obj.Demand_people, obj.Stock_plan_date, obj.submitAuditMan,obj.submitAuditDate)
            elif  obj.Status == 'audit':
                rt = u'<strong>计划需求人:</strong>%s<br><strong>计划生成时间:</strong>%s<br><strong>提交审核人:</strong>%s<br><strong>提交审核时间:</strong>%s<br><strong>审核通过人:</strong>%s<br><strong>审核通过时间:</strong>%s' % (
                    obj.Demand_people, obj.Stock_plan_date, obj.submitAuditMan,obj.submitAuditDate,obj.Auditor,obj.AuditTime)
            elif  obj.Status == 'notpurchased':
                rt = u'<strong>计划需求人:</strong>%s<br><strong>计划生成时间:</strong>%s<br><strong>提交审核人:</strong>%s<br><strong>提交审核时间:</strong>%s<br><strong>审核通过人:</strong>%s<br><strong>审核通过时间:</strong>%s<br><strong>生成采购计划人:</strong>%s<br><strong>生成计划时间:</strong>%s' % (
                    obj.Demand_people, obj.Stock_plan_date, obj.submitAuditMan,obj.submitAuditDate,obj.Auditor, obj.AuditTime,obj.genPurchasePlanMan,obj.genPurchasePlanDate)
            elif  obj.Status == 'already':
                rt = u'<strong>计划需求人:</strong>%s<br><strong>计划生成时间:</strong>%s<br><strong>提交审核人:</strong>%s<br><strong>提交审核时间:</strong>%s<br><strong>审核通过人:</strong>%s<br><strong>审核通过时间:</strong>%s<br><strong>生成采购计划人:</strong>%s<br><strong>生成计划时间:</strong>%s<br><strong>采购完成人:</strong>%s<br><strong>采购完成时间:</strong>%s' % (
                    obj.Demand_people, obj.Stock_plan_date,obj.submitAuditMan,obj.submitAuditDate, obj.Auditor, obj.AuditTime,obj.genPurchasePlanMan,obj.genPurchasePlanDate,obj.completePurchaseMan,obj.completePurchaseDate)

        except Exception, ex:
            messages.info(self.request,"操作记录加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_opTimeInfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">操作时间信息</p>')

    def getHopeNum(self,productSKU):
        try:
            strSql = '''
            		with Goods as 
                    (
                    select  gs.nid  as GoodsSKUID,gs.SKU,g.Purchaser,gs.maxnum,gs.minnum,g.sellDays,
                    gs.CostPrice,g.CostPrice as CostPrice1,gs.GoodsSKUStatus,g.LinkUrl5
                    from B_GoodsSKU(nolock) gs, B_Goods(nolock) g                  
                    where g.NID=gs.GoodsID and g.used=0 
                    ),
                    /*采购未入库数*/--已完全入库订单商品
                    InStoreD as 
                    (  
                    select  om.NID as StockOrderID, m.StoreID, d.GoodsSKUID, sum(d.Amount) as Number   
                    from CG_StockInD(nolock) d    
                    inner join CG_StockInM(nolock) m on d.StockInNID = m.NID and m.StoreID=49  
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
                    inner join KC_StockChangeM(nolock) cm on cm.nid=cd.StockChangenid and cm.checkflag=0  and cm.StoreInID=49  
                    inner  join Goods g on cd.GoodsSKUID = g.GoodsSKUID        
                    where  cm.MakeDate > (GETDATE()-45)       
                    group by cd.GoodsSKUID,cm.StoreInID 
                    ),
                    --今天实际采购数量
                    PurchaseNum as 
                    (
                     select  d.GoodsSKUID, sum(d.Amount) as Amount,max(m.makedate) as Makedate,max(AudieDate) as AudieDate,
                     case min(m.checkflag) when 1 then '审核通过' when 3 then '作废' else '未审核' end as Checkflag
                     from CG_StockOrderD(nolock) d 
                     inner join CG_StockOrderM(nolock) m 
                     on m.NID=d.StockOrderNID and m.StoreID=49 and m.makedate>=CONVERT(VARCHAR(20),GETDATE()-1,23)+' 16:40:00'
                     group by d.GoodsSKUID
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
                    IsNull(g.GoodsSKUStatus,'') as GoodsStatus,g.Purchaser, g.SKU,g.LinkUrl5,pnum.Amount,pnum.Checkflag,pnum.Makedate,pnum.AudieDate,
                    round(d.Number * case when IsNull(g.CostPrice,0) <> 0 then g.CostPrice else IsNull(g.CostPrice1,0) end ,2) as 'AllCostPrice',
                            round(cast(d.SellCount1 as float)/nullif(cast(d.SellCount2 as float)-cast(d.SellCount1 as float),0),2) as 'Ratio'
                    From  kc_Currentstock_ExcludeBlacklist d with(nolock)
                    inner join Goods g on d.GoodsSKUID = g.GoodsSKUID and d.StoreID =49    
                    left join UnInStore u on d.GoodsSKUID = u.GoodsSKUID and d.StoreID = u.StoreID
                    left join UnPaiDNum up on up.GoodsSKUID = d.GoodsSKUID and d.StoreID = up.StoreID
                    left join StockChange sc on sc.goodsskuid = d.goodsskuid and sc.storeinid = d.storeid
                    left join B_GoodsSKULocation(nolock) bgs ON g.GoodsSKUID = bgs.GoodsSKUID AND bgs.StoreID =49
                    left join PurchaseNum pnum on d.GoodsSKUID = pnum.GoodsSKUID 
                    where g.SKU='%s'
                    )
                     
                    select KcMaxNum,KcMinNum,SellCount1,SellCount2,SellCount3, Number,ReservationNum,UseNumber,NotInStore,hopeUseNum,UnPaiDNum,SuggestNum,
                    case when AvgDayNum=0.0 then case when hopeUseNum=0.0 then 0.0 when hopeUseNum <0.0 then -99999.0 else 99999.0 end 
                    else round(hopeUseNum/(AvgDayNum*case when Ratio is null then 1 when Ratio>2 then 2 when Ratio=0 then 0.1 else Ratio end),2) end as SaleDay,
                    MaxDelayDays,SaleReNum,LocationName,hopeUseNum-SellCount2 as 'StockDiff15', Ratio,GoodsStatus,Purchaser,SKU,AllCostPrice,
                    round(AvgDayNum*case when Ratio is null then 1 when Ratio>2 then 2 when Ratio=0 then 0.1 else Ratio end,2) as AvgDayNum,
                    isnull(LinkUrl5,'无') as LinkUrl5,isnull(Amount,0) as Amount,isnull(Checkflag,' ') as Checkflag, Makedate, AudieDate
                    from Result ;
            '''%(productSKU)
            reslut = {'errorcode':-1,'errortext':'','returnConent':()}
            from brick.pydata.py_syn.py_conn import py_conn
            py_connObj = py_conn()
            sqlServerInfo = py_connObj.py_conn_database()
            if sqlServerInfo['errorcode'] == 0:
                sqlServerInfo['py_cursor'].execute(strSql)
                returnContent = sqlServerInfo['py_cursor'].fetchone()
                if returnContent:
                    reslut['errorcode'] = 0
                    #库存量、占有量、 未入库量、预计可用数量、未派单量、建议采购数量、可卖天数、日平均销量
                    reslut['returnConent'] = (returnContent[5],returnContent[6],returnContent[8],returnContent[9],returnContent[10],returnContent[11],returnContent[12],returnContent[22])
            else:
                pass
            py_connObj.py_close_conn_database()
        except Exception, ex:
            messages.info(self.request, "获取库存量、占有量、 未入库量、预计可用数量、未派单量、建议采购数量、可卖天数失败,请联系IT解决:%s" % (str(ex)))
            py_connObj.py_close_conn_database()
        return reslut

    list_display = ('Stocking_plan_number','show_Status','Stock_plan_date','Product_nature','ProductSKU','ProductName','show_ProductImage','Stocking_quantity','Destination_warehouse','level','Demand_people','Auditor','AccountNum','neworold','show_opInfo','AmazonFactory')

    fields = ('ProductSKU', 'Stocking_quantity', 'AccountNum', 'Site','Demand_people',
              'Destination_warehouse', 'level','Remarks','Product_nature','ShopSKU','neworold','AmazonFactory')

    form_layout = (
        Fieldset(u'请认真填写备货需求',
                 Row('ProductSKU', 'Stocking_quantity','Product_nature',),
                 Row('AccountNum', 'Site','Demand_people',),
                 Row('Destination_warehouse', 'level','ShopSKU',),
                 Row('neworold', 'AmazonFactory', '', ),
                 Row('Remarks', '','',),
                 css_class='unsort '
                 ),)

    actions = ['purchasing_plan_audit','summit_AmazonFactory','get_excel_product_registration_form']

    def purchasing_plan_audit(self,request,objs):
        skuinto = []
        for obj in objs:
            if (obj.Status == "notgenerated" or obj.Status == "back") and obj.AmazonFactory != 'yes':
                obj.Status = 'noaudit' # 未审核
                obj.submitAuditMan = request.user.first_name
                obj.submitAuditDate=ddtime.now()
                obj.OplogTime = ddtime.now()
                obj.save()
            else:
                skuinto.append(obj.ProductSKU)
        if len(skuinto) > 0:
            messages.info(request,"以下商品：%s 已提交审核,不能重复提交审核"%(str(skuinto)))

    purchasing_plan_audit.short_description = u'未生成采购计划-提交审核'

    def summit_AmazonFactory(self,request,objs):
        try:
            cursor = hqdb_conn.cursor()
            listProductSKU = []
            insertinto = []
            sucessInfo = []
            FBAList = []
            for obj in objs:
                if obj.ProductSKU[:4] == "FBA-":
                    FBAList.append(obj.ProductSKU)
                    continue
                if (obj.Status == "notgenerated" or obj.Status == "back") and  obj.AmazonFactory == "yes":
                    strSql = '''
                        SELECT a.BmpUrl,a.SKU,a.TortInfo,a.GoodsStatus,a.Purchaser,a.SalerName2,a.SellCount1,a.SellCount2,a.SellCount3,a.UseNumber,
                        ifnull(c.OnlineNotIn,0)+a.NotInStore as NotInStore,a.CostPrice,
                        aa.SuggestNum*a.SellCount1-a.Number-a.NotInStore-ifnull(c.OnlineNotIn,0) as SuggestNum,
                        ifnull(c.OnlineNotIn,0)+a.hopeUseNum as hopeUseNum,
                        a.UnPaiDNum,a.ReservationNum,a.Number,a.GoodsName,a.SupplierName,a.Model,
                        (a.hopeUseNum+ifnull(c.OnlineNotIn,0))/a.AverageNumber as SaleDay,
                        a.CgCategory,a.AverageNumber, 
                        if(((a.hopeUseNum+ifnull(c.OnlineNotIn,0))/a.AverageNumber)<=aa.SuggestMin,1,2) as flag,aa.OSCode
                        FROM py_db.kc_currentstock_sku a inner join py_db.kc_currentstock_sku_oscode aa on a.SourceOSCode=aa.OSCode and aa.OSCode in ('OS906')
                        left join ( select SKU, SUM(if(currentState=22,productNumbers - completeNumbers, ifnull(completeNumbers,productNumbers))) AS OnlineNotIn
                                                from t_cloth_factory_dispatch 
                                                where currentState in (20,22)
                                                group by SKU) c on a.SKU=c.SKU
                        where a.sku='%s' and  a.SupplierName in ('广州工厂','易臻工厂','马俊杰') and a.used=0 and a.storeID = 1 			
                        and a.SKU not in (select b.SKU from t_cloth_factory_dispatch b where b.currentState<12);
                        '''%(obj.ProductSKU)
                    cursor.execute(strSql)
                    tuppleKcCurrent = cursor.fetchone()

                    if tuppleKcCurrent:
                        # 获取FBA和非FBA 7天销量、15天销量、30天销量 累计
                        sevenSales = tuppleKcCurrent[6]
                        fifteenSales = tuppleKcCurrent[7]
                        thirtySales = tuppleKcCurrent[8]
                        FBASKU = "FBA-" + obj.ProductSKU
                        if len(FBASKU) > 0:
                            strSql = "select sellcount1,sellcount2,sellcount3 from py_db.kc_currentstock_sku where sku='%s' and storeID=2;"%(FBASKU)
                            cursor.execute(strSql)
                            tuppleNoSKUCurrent = cursor.fetchone()
                            if tuppleNoSKUCurrent:
                                sevenSales = sevenSales + tuppleNoSKUCurrent[0]
                                fifteenSales = fifteenSales + tuppleNoSKUCurrent[1]
                                thirtySales = thirtySales + tuppleNoSKUCurrent[2]

                        getOtherInfo = self.getHopeNum(obj.ProductSKU) # 库存量、占有量、 未入库量、预计可用数量、未派单量、建议采购数量、可卖天数、日平均销量
                        stockNum =tuppleKcCurrent[16]
                        occupyNum = tuppleKcCurrent[15]
                        PurchaseNotInNum = tuppleKcCurrent[10]
                        ailableNum = tuppleKcCurrent[13]
                        oosNum = tuppleKcCurrent[14]
                        SuggestNum = tuppleKcCurrent[12]
                        SaleDay = tuppleKcCurrent[20]
                        AverageNumber = tuppleKcCurrent[22]
                        if getOtherInfo['errorcode'] != -1:
                            stockNum = getOtherInfo['returnConent'][0]
                            occupyNum = getOtherInfo['returnConent'][1]
                            PurchaseNotInNum = getOtherInfo['returnConent'][2]
                            ailableNum = getOtherInfo['returnConent'][3]
                            oosNum = getOtherInfo['returnConent'][4]
                            SuggestNum = getOtherInfo['returnConent'][5]
                            SaleDay = getOtherInfo['returnConent'][6]
                            AverageNumber = getOtherInfo['returnConent'][7]

                        strInsert = '''
                            INSERT INTO t_cloth_factory_dispatch(BmpUrl,SKU,TortInfo,goodsState,buyer,SalerName2,sevenSales,fifteenSales,thirtySales,
                                UseNumber,PurchaseNotInNum,goodsCostPrice,SuggestNum,ailableNum,oosNum,occupyNum,stockNum,goodsName,Supplier,girard,SaleDay,
                                goodsclass,AverageNumber,flag,OSCode,Stocking_plan_number) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        '''
                        param = (tuppleKcCurrent[0],tuppleKcCurrent[1],tuppleKcCurrent[2],tuppleKcCurrent[3],tuppleKcCurrent[4],tuppleKcCurrent[5],sevenSales,fifteenSales,thirtySales,
                                 tuppleKcCurrent[9],PurchaseNotInNum,tuppleKcCurrent[11],obj.Stocking_quantity,ailableNum,oosNum,occupyNum,stockNum,tuppleKcCurrent[17],tuppleKcCurrent[18],tuppleKcCurrent[19],SaleDay,
                                 tuppleKcCurrent[21],AverageNumber,tuppleKcCurrent[23],tuppleKcCurrent[24],obj.Stocking_plan_number)
                        cursor.execute(strInsert,param)

                        insertinto.append(t_stocking_purchase_order(
                            Stocking_plan_number=obj.Stocking_plan_number, Stock_plan_date=obj.Stock_plan_date,
                            ProductSKU=obj.ProductSKU, ProductName=obj.ProductName, QTY=obj.Stocking_quantity,
                            Price=obj.ProductPrice, Buyer=request.user.first_name, ThePeople=request.user.first_name,
                            TheTime=ddtime.now(), Warehouse=obj.Destination_warehouse, Status='notyet',
                            Stocking_quantity=obj.Stocking_quantity, Weight=obj.ProductWeight,
                            ProductImage=obj.ProductImage,Supplier=obj.Supplier, Supplierlink=obj.Supplierlink, Remarks=obj.Remarks,
                            ExcelStatus='never',Demand_people=obj.Demand_people, level=obj.level, Product_nature=obj.Product_nature,
                            Site=obj.Site,AccountNum=obj.AccountNum, ShopSKU=obj.ShopSKU, OplogTime=ddtime.now()
                        ))

                        obj.OplogTime = ddtime.now()
                        obj.Status = 'notpurchased'  # 计划已生成，未采购
                        obj.submitAuditMan = request.user.first_name
                        obj.submitAuditDate = ddtime.now()
                        obj.Auditor = request.user.first_name
                        obj.AuditTime = ddtime.now()
                        obj.genPurchasePlanDate = ddtime.now()  # 生成采购计划时间
                        obj.genPurchasePlanMan = request.user.first_name  # 生成采购计划人
                        obj.save()

                        sucessInfo.append(obj.ProductSKU)
                        cursor.execute("commit")
                    else:
                        listProductSKU.append(obj.ProductSKU)
                else:
                    listProductSKU.append(obj.ProductSKU)
            if len(insertinto) > 0:
                t_stocking_purchase_order.objects.bulk_create(insertinto)
            if listProductSKU:
                messages.info(request,"商品SKU:%s,不能提交供应链服装采购;原因：非亚马逊服装、服装排单流程存在未审核记录或者在库存表未关联到商品SKU."%(listProductSKU))
            if FBAList:
                messages.info(request,"商品SKU:%s,不能带前缀FBA提交供应链服装采购,请重新去除前缀FBA-提交备货需求."%(FBAList))
            cursor.close()
            if sucessInfo:
                messages.success(request, '商品SKU:%s,已流转供应链服装采购，可在[4-采购计划]中查看处理进度.'%(sucessInfo))
        except Exception, ex:
            messages.error(request,"提交到供应链服装采购错误,请联系IT解决:%s"%(str(ex)))
    summit_AmazonFactory.short_description = u'提交供应链服装采购'

    def get_excel_product_registration_form(self,request,objs):
        from app_djcelery.tasks import product_registration_form_excel_task
        getexcel = []
        for obj in objs:
            ProductPrice = obj.ProductPrice
            if obj.ProductPrice is None:
                ProductPrice = '0'
            ProductWeight = obj.ProductWeight
            if obj.ProductWeight is None:
                ProductWeight = '0'
            objlist = [obj.ProductName,obj.ProductSKU,obj.ProductSKU,'%.2f'%(float(ProductPrice)/6.5),
                       '','','USD','',u'包裹','zh','',float(ProductWeight)/1000,'','',3,0]
            getexcel.append(objlist)
        product_registration_form_excel_task.delay(getexcel,request.user.username)
        messages.success(request,u'请稍后到“下载中心”，下载文件。。。')
    get_excel_product_registration_form.short_description = u'导出商品注册表'

    def save_models(self,):
        try:
            obj = self.new_obj
            request = self.request

            old_obj = None

            if obj is None or obj.id is None or obj.id <= 0:
                pass
            else:
                old_obj = self.model.objects.get(pk=obj.pk)
            obj.save()

            obj.Stocking_plan_number = ddtime.now().strftime('%Y%m%d%H%M%S') + '_' + str(obj.id)
            obj.Stock_plan_date      = ddtime.now()
            obj.OplogTime            = ddtime.now()

            if obj.Demand_people is None or obj.Demand_people.strip() == "":
                obj.Demand_people = request.user.first_name

            py_b_goods_objs = py_b_goods.objects.filter(SKU=obj.ProductSKU)
            if py_b_goods_objs.exists():
                obj.ProductImage = u'http://fancyqube.net:89/ShopElf/images/%s.jpg'%py_b_goods_objs[0].SKU.replace('OAS-','').replace('FBA-','')
                obj.ProductName  = py_b_goods_objs[0].GoodsName
                obj.ProductPrice = py_b_goods_objs[0].CostPrice
                obj.ProductWeight= py_b_goods_objs[0].Weight
                obj.Supplierlink = py_b_goods_objs[0].LinkUrl

                py_b_Supplier_objs = py_b_Supplier.objects.filter(NID=py_b_goods_objs[0].SupplierID)
                if py_b_Supplier_objs.exists():
                    obj.Supplier     = py_b_Supplier_objs[0].SupplierName

            obj.Buyer = ''

            obj.Status = u'notgenerated' # 未生成采购计划

            obj.save()
        except Exception, ex:
            messages.info(self.request,"保存报错:%s"%(str(ex)))
        
    def get_list_queryset(self):
        request = self.request
        
        qs = super(t_stocking_demand_list_Admin, self).get_list_queryset()
        Status = request.GET.get('Status', '')  # 采购状态
        Stocking_plan_number = request.GET.get('Stocking_plan_number', '')   #备货计划号
        Stock_plan_dateStart      = request.GET.get('Stock_plan_dateStart', '')     # 备货计划时间
        Stock_plan_dateEnd      = request.GET.get('Stock_plan_dateEnd', '')     # 备货计划时间
        Demand_people = request.GET.get('Demand_people', '')             # 计划需求人
        Product_nature = request.GET.get('Product_nature', '')            #产品性质
        ProductSKU = request.GET.get('ProductSKU', '')                     #商品sku
        ProductName = request.GET.get('ProductName', '')                    # 商品名称
        ProductWeightStart = request.GET.get('ProductWeightStart', '')
        ProductWeightEnd = request.GET.get('ProductWeightEnd', '')                #商品克重
        Supplier = request.GET.get('Supplier', '')                         # 供应商
        AccountNum = request.GET.get('AccountNum', '')                     # 帐号
        Site = request.GET.get('Site', '')                                  # 站点
        Destination_warehouse = request.GET.get('Destination_warehouse', '')# 目的地仓库
        level = request.GET.get('level', '')                                # 紧急程度
        Auditor = request.GET.get('Auditor', '')                            #审核人
        AuditTimeStart = request.GET.get('AuditTimeStart', '')                        #审核时间
        AuditTimeEnd = request.GET.get('AuditTimeEnd', '')                        #审核时间
        Buyer = request.GET.get('Buyer', '')                                #采购人

        UpdateTimeStart = request.GET.get('UpdateTimeStart', '')            # 更新时间
        UpdateTimeEnd = request.GET.get('UpdateTimeEnd', '')               # 更新时间
        neworold = request.GET.get('neworold', '')  # 新品备货
        OplogTimeStart = request.GET.get('OplogTimeStart','')  #记录生成时间
        OplogTimeEnd =request.GET.get('OplogTimeEnd','') #记录生成时间


        searchList = {
                        'Stocking_plan_number__exact':Stocking_plan_number,
                        'Stock_plan_date__gte':Stock_plan_dateStart,'Stock_plan_date__lt':Stock_plan_dateEnd,
                        'Demand_people__exact':Demand_people,'Product_nature__exact':Product_nature,
                        'ProductSKU__icontains': ProductSKU,'ProductName__exact':ProductName,
                        'ProductWeight__gte':ProductWeightStart,
                        'ProductWeight__lt':ProductWeightEnd,
                        'Supplier__exact':Supplier,
                        'AccountNum__exact':AccountNum,'Site__exact':Site,
					    'Destination_warehouse__exact': Destination_warehouse,
                        'level__exact':level,
                        'Auditor__exact': Auditor,
                        'AuditTime__gte': AuditTimeStart,'AuditTime__lt': AuditTimeEnd,
                        'Buyer__exact':Buyer,
                        'Status__exact':Status,
                        'UpdateTime__gte':UpdateTimeStart,'UpdateTime__lt':UpdateTimeEnd,
                        'OplogTime__gte':OplogTimeStart,'OplogTime__lt':OplogTimeEnd,
                        'neworold__exact': neworold,
                      }

        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
        if Status == "" or Status == "already":
            return qs
        elif Status == "audit":
            return qs.order_by("AuditTime")
        elif Status == "noaudit":
            return qs.order_by("submitAuditDate")
        elif Status == "notpurchased":
            return qs.order_by("genPurchasePlanDate")
        elif Status == "notgenerated":
            return qs.order_by("Stock_plan_date")
        else:
            return qs.order_by("Stock_plan_date")

