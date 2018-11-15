# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fba_detail_Admin.py
 @time: 2018-08-08

"""
from xadmin.layout import Fieldset, Row
import datetime as tmpDate,random
from pyapp.models import b_goods as py_b_goods,B_Supplier as py_b_Supplier
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.db import connection as hqdb_conn
from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
from skuapp.table.t_stocking_demand_fba_deliver import t_stocking_demand_fba_deliver
from Project.settings import *
from datetime import datetime as ddtime
from .t_product_Admin import *
from skuapp.table.public import *

class t_stocking_demand_fba_detail_Admin(object):
    search_box_flag = True
    fba_tree_menu_flag = True
    downloadxls = True

    creatStartTime = '2018-08-01 00:00:00'
    creatEndTime = '2099-12-31 23:59:59'

    def show_ProductImage(self,obj) :
        rt =  '<img src="%s"  width="120" height="120"/>  '%(obj.ProductImage)
        return mark_safe(rt)
    show_ProductImage.short_description = u'商品图片'

    def deal_status(self,planStatus):
        strStatus = planStatus
        for status in getChoices(ChoiceFBAPlanStatus):
            if status[0] == planStatus:
                strStatus = status[1]
                break
        return strStatus

    def deal_none(self,value):
        value = '' if value is None else value
        return value

    def show_kcnum(self,obj):
        try:
            rt = '0'
            curNumber = 0
            cursor = hqdb_conn.cursor()
            strSKU = obj.ProductSKU
            strFBASKU = "FBA-" + strSKU
            if obj.ProductSKU[:4] == "FBA-":
                strFBASKU = obj.ProductSKU[4:]
            comSKU = '\'' + strSKU + '\',\'' +strFBASKU + '\''
            strSql = "select sum(Number),sum(ReservationNum) from py_db.kc_currentstock " \
                     "where goodsid in(select nid from py_db.b_goods where sku in(%s)) and StoreID='73';"%(comSKU)
            cursor.execute(strSql)
            tuppleKcCurrent = cursor.fetchone()
            if tuppleKcCurrent:
                Number = tuppleKcCurrent[0] if tuppleKcCurrent[0] is not None else 0
                ReservationNum = tuppleKcCurrent[1] if tuppleKcCurrent[1] is not None else 0
                curNumber = int(Number) - int(ReservationNum)
            rt = str(curNumber)
            cursor.close()
        except Exception, ex:
            rt = '0'
            messages.error(self.request, "提交到供应链服装采购错误,请联系IT解决:%s" % (str(ex)))
        return mark_safe(rt)

    show_kcnum.short_description = mark_safe('<p align="center" style="width:200px;color:#428bca;">集货仓库存(库存-占用)</p>')

    def show_purchasedetail(self, obj):
        try:
            rt = ''
            from django.db import connection
            hqSql = "select ProductSKU,GROUP_CONCAT(Stocking_plan_number,'*',IFNULL(Stocking_quantity,0),'*',IFNULL(QTY,0))," \
                    "GROUP_CONCAT(IFNULL(Delivery_lot_number,'not'),'*',(case  when Status is NULL  then 'nostatus' when Status='' then 'nostatus' else Status end))  " \
                    "from t_stocking_demand_fba " \
                    "where ProductSKU='%s' and Stock_plan_date>'%s' and Stock_plan_date<'%s' and Status not in ('giveup','abnormalcheck','abnormalpurchase') GROUP BY ProductSKU"\
                    %(obj.ProductSKU,t_stocking_demand_fba_detail_Admin.creatStartTime,t_stocking_demand_fba_detail_Admin.creatEndTime)
            cursor = connection.cursor()
            cursor.execute(hqSql)
            resultObjs = cursor.fetchone()
            if resultObjs:
                rt = u'<table border="1" width="700"><tr><th width="200">备货计划号</th><th width="100">备货数量</th><th width="100">实际采购数量</th><th width="100">采购状态</th><th width="200">备货时间</th></tr>'
                Stocking_plan_numberList = resultObjs[1].split(',')
                Delivery_lot_numberList = resultObjs[2].split(',')
                for (row1,row2) in zip(Stocking_plan_numberList,Delivery_lot_numberList):
                    if row2.split('*')[1] == 'completedeliver':
                        rt = rt + u'<tr style="color:red;font-weight:bold"><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr>' % \
                             (row1.split('*')[0],row1.split('*')[1],row1.split('*')[2], self.deal_status(row2.split('*')[1]),str(row1.split('*')[0])[:10])
                    else:
                        rt = rt + u'<tr style=""><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr>' % \
                             (row1.split('*')[0], row1.split('*')[1], row1.split('*')[2],self.deal_status(row2.split('*')[1]), str(row1.split('*')[0])[:10])
                rt = rt + "</table>"
            cursor.close()

        except Exception, ex:
            messages.info(self.request,"加载数据存在问题,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_purchasedetail.short_description = mark_safe('<p align="center" style="width:120px;color:#428bca;">采购订单信息</p>')

    def show_deliverdetail(self, obj):
        try:
            rt = ''
            dic_productSKUNum={}
            from django.db import connection
            args = '%' + obj.ProductSKU + '%'
            hqSql = "select Stocking_plan_number,All_ProductSKU_Num,Delivery_lot_number from t_stocking_demand_fba_deliver " \
                    "where All_ProductSKU_Num like '%s' and Status='completedeliver' and  Delivery_date>'%s' and Delivery_date < '%s';"%\
                    (args,t_stocking_demand_fba_detail_Admin.creatStartTime,t_stocking_demand_fba_detail_Admin.creatEndTime)

            cursor = connection.cursor()
            cursor.execute(hqSql)
            resultObjs = cursor.fetchall()
            for obj_result in resultObjs:
                skuNumList = str(list(obj_result)[1]).split(';')
                Stocking_plan_numberList = str(list(obj_result)[0]).split('|')
                for (obj_skuNumList,obj_number) in zip(skuNumList,Stocking_plan_numberList):
                    Sku = obj_skuNumList.split("*")[0]
                    Num = obj_skuNumList.split("*")[1]
                    if dic_productSKUNum.has_key(Sku):
                        tmp = dic_productSKUNum[Sku]
                        tmp[obj_number] = int(Num)
                        tmp[obj_number+'batchid'] = obj_result[2]
                        dic_productSKUNum[Sku] = tmp
                    else:
                        dicTmp = {}
                        dicTmp[obj_number] = int(Num)
                        dicTmp[obj_number+'batchid'] = obj_result[2]
                        dic_productSKUNum[Sku] = dicTmp
            if dic_productSKUNum.has_key(obj.ProductSKU):
                rt = u'<table border="1" width="600"><tr><th width="200">批次号</th><th width="200">备货计划号</th><th width="200">已发货数量</th></tr>'
                for key in dic_productSKUNum[obj.ProductSKU].keys():
                    batchid = ''
                    planid = ''
                    num = 0
                    if 'batchid' in key:
                        continue
                    else:
                        planid = key
                        batchid = dic_productSKUNum[obj.ProductSKU][planid+'batchid']
                        num = dic_productSKUNum[obj.ProductSKU][planid]

                    rt = rt + u'<tr style=""><th>%s</th><th>%s</th><th>%s</th></tr>' % \
                         (batchid,planid,num)
                rt = rt + "</table>"
            else:
                rt = ''
            cursor.close()

        except Exception, ex:
            messages.info(self.request,"加载数据存在问题,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_deliverdetail.short_description = mark_safe('<p align="center" style="width:120px;color:#428bca;">发货订单信息</p>')

    def show_opInfo(self, obj):
        try:
            rt = u'<table border="1"><tr><th>操作员</th><th>告警信息</th><th>操作时间</th></tr>'
            if obj.Status == 'giveup':
                #rt = u'<div style="width:120px"><strong>计划需求人:</strong>%s' % (obj.Demand_people)
                diffDate1 = (obj.giveupDate - obj.Stock_plan_date).days if (obj.Stock_plan_date is not None and obj.giveupDate is not None) else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>'%(obj.Demand_people,diffDate1,obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                rt = rt + u'<tr style=""><th>废弃:%s</th><th> </th><th>%s</th></tr>' % (obj.giveupMan, obj.giveupDate)
            elif obj.Status == 'notgenpurchase':
                diffDate1 = (ddtime.now() - obj.Stock_plan_date).days if obj.Stock_plan_date is not None else 0
                if diffDate1 > 1:
                    rt = rt + u'<tr style="color:red"><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
                else:
                    rt = rt + u'<tr style=""><th>需求:%s</th><th> 延迟%s天</th><th>%s</th></tr>' % (obj.Demand_people, diffDate1, obj.Stock_plan_date)
            rt = rt + "</table>"
        except Exception, ex:
            messages.info(self.request,"操作记录加载错误,请联系IT解决:%s"%(str(ex)))
            rt = ""
        return mark_safe(rt)
    show_opInfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">操作记录信息</p>')

    def show_OPinfo(self,obj):
        try:
            rt = ''
            #获取状态、计划需求提出人、计划需求提出时间、
            t_stocking_demand_fba_objs = t_stocking_demand_fba.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).\
                values_list('Status','Demand_people','Stock_plan_date','recordPurchaseCodeMan','recordPurchaseCodeDate','CheckMan','CheckTime','genBatchMan','genBatchDate')
            rt = u'<table border="1" width="350"><tr>' \
                 u'<th width="100">操作类型</th><th width="100">操作人</th><th width="150">操作时间</th></tr>'
            if t_stocking_demand_fba_objs:
                rt = rt + u'<tr><th width="100">备货需求</th><th width="100">%s</th><th width="150">%s</th></tr><tr><th width="100">采购</th><th width="100">%s</th>' \
                          u'<th width="150">%s</th></tr><tr><th width="100">质检</th><th width="100">%s</th><th width="150">%s</th></tr>' \
                          u'<tr><th width="100">生成批次</th><th width="100">%s</th><th width="150">%s</th></tr>' % \
                     (self.deal_none(t_stocking_demand_fba_objs[0][1]),self.deal_none(t_stocking_demand_fba_objs[0][2]),
                      self.deal_none(t_stocking_demand_fba_objs[0][3]),self.deal_none(t_stocking_demand_fba_objs[0][4]),
                      self.deal_none(t_stocking_demand_fba_objs[0][5]),self.deal_none(t_stocking_demand_fba_objs[0][6]),
                      self.deal_none(t_stocking_demand_fba_objs[0][7]),self.deal_none(t_stocking_demand_fba_objs[0][8]))

                #实际发货数量
                DeliverNum = 0
                if t_stocking_demand_fba_objs[0][0] == "completedeliver":
                    t_stocking_demand_fba_deliver_objs = t_stocking_demand_fba_deliver.objects.filter(Stocking_plan_number__icontains=obj.Stocking_plan_number).\
                        values_list('Sender','OplogTime')
                    if t_stocking_demand_fba_deliver_objs:
                        rt = rt + '<tr><th width="100">发货</th><th width="100">%s</th><th width="150">%s</th></tr>'%(self.deal_none(t_stocking_demand_fba_deliver_objs[0][0]),self.deal_none(t_stocking_demand_fba_deliver_objs[0][1]))
            rt = rt + "</table>"
        except Exception, ex:
            messages.info(self.request, "记录加载错误,请联系IT解决:%s" % (str(ex)))
            rt = ""
        return mark_safe(rt)
    show_OPinfo.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">操作信息</p>')

    def show_info(self,obj):
        try:
            rt = ''
            #获取状态、备货数量、实际采购数量、到货数量、抽检数量、抽检合格数量、合格总量、次品总量、转退数量
            t_stocking_demand_fba_objs = t_stocking_demand_fba.objects.filter(Stocking_plan_number=obj.Stocking_plan_number).\
                values_list('Status','Stocking_quantity','QTY','The_arrival_of_the_number','CheckNumber','CheckQualified','checkCompleteNum','checkInferiorNum','tranReturnNum')
            rt = u'<table border="1" width="1000"><tr>' \
                 u'<th width="100">备货数量</th><th width="100">实际采购数量</th>' \
                 u'<th width="100">到货数量</th><th width="100">抽检数量</th>' \
                 u'<th width="100">抽检合格数量</th><th width="100">合格总量</th>' \
                 u'<th width="100">次品总量</th><th width="100">转退数量</th>' \
                 u'<th width="100">实际发货数量</th><th width="100">状态</th></tr>'
            if t_stocking_demand_fba_objs:
                rt = rt + u'<tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th>' % \
                     (self.deal_none(t_stocking_demand_fba_objs[0][1]),self.deal_none(t_stocking_demand_fba_objs[0][2]),self.deal_none(t_stocking_demand_fba_objs[0][3]),
                      self.deal_none(t_stocking_demand_fba_objs[0][4]),
                      self.deal_none(t_stocking_demand_fba_objs[0][5]),self.deal_none(t_stocking_demand_fba_objs[0][6]),self.deal_none(t_stocking_demand_fba_objs[0][7]),
                      self.deal_none(t_stocking_demand_fba_objs[0][8]))

                #实际发货数量
                DeliverNum = 0
                if t_stocking_demand_fba_objs[0][0] == "completedeliver":
                    t_stocking_demand_fba_deliver_objs = t_stocking_demand_fba_deliver.objects.filter(Stocking_plan_number__icontains=obj.Stocking_plan_number).\
                        values_list('Stocking_plan_number','editSKU')
                    if t_stocking_demand_fba_deliver_objs:
                        Stocking_plan_numberList = t_stocking_demand_fba_deliver_objs[0][0].split('|')
                        EditSKUsList = t_stocking_demand_fba_deliver_objs[0][1].split(';')
                        for (row1, row2) in zip(Stocking_plan_numberList, EditSKUsList):
                            if obj.Stocking_plan_number == row1:
                                DeliverNum = row2.split('*')[1]
                                break
                rt = rt + "<th>%s</th><th>%s</th></tr>"%(DeliverNum,self.deal_status(t_stocking_demand_fba_objs[0][0]))
            rt = rt + "</table>"
        except Exception, ex:
            messages.info(self.request, "记录加载错误,请联系IT解决:%s" % (str(ex)))
            rt = ""
        return mark_safe(rt)
    show_info.short_description = mark_safe('<p align="center" style="width:100px;color:#428bca;">采购信息</p>')

    list_display = ('Stocking_plan_number','ProductSKU','show_kcnum','show_info','show_OPinfo','Remarks')
    list_editable = ('Remarks',)
    actions = [ 'genExecl','checkRecord']

    def genExecl(self,request,objs):
        try:
            from xlwt import *
            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            # if not os.path.exists(path):
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

            mkdir_p(path)
            os.popen('chmod 777 %s' % (path))

            #datastyle = xlwt.XFStyle()
            #datastyle.num_format_str = 'yyyy-mm-dd'
            w = Workbook()
            sheet = w.add_sheet(u'采购明细数据')
            sheetlist = [u'备货计划号',u'采购单号',u'发货批次号',u'批次发货总数量',u'商品SKU',u'备货数量', u'实际采购数量', u'到货数量', u'抽检数量', u'抽检合格数量', u'合格总量', u'次品总量', u'转退数量',
                         u'实际发货数量', u'备货需求人', u'备货需求时间', u'采购人', u'采购时间', u'质检人', u'质检时间',u'生成批次人', u'生成批次时间', u'发货人', u'发货时间', u'状态',u'备注' ]

            for index, item in enumerate(sheetlist):
                sheet.write(0, index, item)
            row = 0
            for obj in objs:

                t_stocking_demand_fba_objs = t_stocking_demand_fba.objects.filter(Stocking_plan_number=obj.Stocking_plan_number). \
                    values_list('Stocking_quantity', 'QTY', 'The_arrival_of_the_number', 'CheckNumber',
                                'CheckQualified', 'checkCompleteNum', 'checkInferiorNum', 'tranReturnNum','Demand_people',
                                             'Stock_plan_date','recordPurchaseCodeMan','recordPurchaseCodeDate','CheckMan','CheckTime','genBatchMan','genBatchDate','Status','Single_number')
                if t_stocking_demand_fba_objs:
                    DeliverNum = 0
                    Sender = ''
                    OplogTime = ''
                    Delivery_lot_number = ''
                    Num = ''
                    if t_stocking_demand_fba_objs[0][16] == "completedeliver":
                        t_stocking_demand_fba_deliver_objs = t_stocking_demand_fba_deliver.objects.filter(
                            Stocking_plan_number__icontains=obj.Stocking_plan_number). \
                            values_list('Stocking_plan_number', 'editSKU','Sender','OplogTime','Delivery_lot_number','Num')
                        if t_stocking_demand_fba_deliver_objs:
                            Stocking_plan_numberList = t_stocking_demand_fba_deliver_objs[0][0].split('|')
                            EditSKUsList = t_stocking_demand_fba_deliver_objs[0][1].split(';')
                            Sender = t_stocking_demand_fba_deliver_objs[0][2]
                            OplogTime = t_stocking_demand_fba_deliver_objs[0][3]
                            Delivery_lot_number = t_stocking_demand_fba_deliver_objs[0][4]
                            Num = t_stocking_demand_fba_deliver_objs[0][5]
                            for (row1, row2) in zip(Stocking_plan_numberList, EditSKUsList):
                                if obj.Stocking_plan_number == row1:
                                    DeliverNum = row2.split('*')[1]
                                    break

                    row = row + 1
                    column = 0
                    sheet.write(row, column, obj.Stocking_plan_number)  # 备货计划号

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][17]))  # 采购单号

                    column = column + 1
                    sheet.write(row, column, Delivery_lot_number)  # 发货批次

                    column = column + 1
                    sheet.write(row, column, Num)  # 发货总数量

                    column = column + 1
                    sheet.write(row, column, obj.ProductSKU)  # 商品SKU

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][0]))  # 备货数量

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][1]))  # 实际采购数量

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][2]))  # 到货数量

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][3]))  # 抽检数量

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][4]))  # 抽检合格数量

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][5]))  # 合格总量

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][6]))  # 次品总量

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][7]))  # 转退数量

                    column = column + 1
                    sheet.write(row, column, DeliverNum)  # 实际发货数量

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][8]))  # 备货需求人

                    column = column + 1
                    sheet.write(row, column, '%s'%self.deal_none(t_stocking_demand_fba_objs[0][9]))  # 备货需求时间

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][10]))  # 采购人',

                    column = column + 1
                    sheet.write(row, column, '%s'%self.deal_none(t_stocking_demand_fba_objs[0][11]))  # 采购时间

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][12]))  # 质检人

                    column = column + 1
                    sheet.write(row, column, '%s'%self.deal_none(t_stocking_demand_fba_objs[0][13]))  # 质检时间

                    column = column + 1
                    sheet.write(row, column, self.deal_none(t_stocking_demand_fba_objs[0][14]))  # 生成批次人

                    column = column + 1
                    sheet.write(row, column, '%s'%self.deal_none(t_stocking_demand_fba_objs[0][15]))  # 生成批次时间

                    column = column + 1
                    sheet.write(row, column, Sender)  # 发货人

                    column = column + 1
                    sheet.write(row, column, '%s'%OplogTime)  # 发货时间

                    column = column + 1
                    sheet.write(row, column, '%s'%self.deal_status(t_stocking_demand_fba_objs[0][16]))  # 状态

                    column = column + 1
                    sheet.write(row, column,obj.Remarks)  # 状态

            filename = request.user.username + '_' + ddtime.now().strftime('%Y%m%d%H%M%S') + '.xls'
            w.save(path + '/' + filename)
            os.popen(r'chmod 777 %s' % (path + '/' + filename))

            # 上传oss对象
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
            bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
            # 删除现有的
            for object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_' % (request.user.username, request.user.username)):
                bucket.delete_object(object_info.key)
            bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))
            messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                        filename) + u':成功导出,可点击Download下载到本地............................。')
        except Exception, ex:
            messages.info(self.request, "导出execl错误,请联系IT解决:%s" % (str(ex)))
    genExecl.short_description = u'生成明细数据'

    def checkRecord(self,request,objs):
        try:
            for obj in objs:
                obj.AuditFlag = 1
                obj.AuditMan = request.user.first_name
                obj.AuditDate = ddtime.now()
                obj.save()
        except Exception, ex:
            messages.info(self.request,"保存报错:%s"%(str(ex)))
    checkRecord.short_description = u'提交已核实记录'

    def save_models(self,):
        try:
            pass
        except Exception, ex:
            messages.info(self.request,"保存报错:%s"%(str(ex)))
        
    def get_list_queryset(self):
        request = self.request
        qs = super(t_stocking_demand_fba_detail_Admin, self).get_list_queryset()

        tmpStart = request.GET.get('createDateStart', '')
        if tmpStart:
            t_stocking_demand_fba_detail_Admin.creatStartTime = tmpStart
        tmpEnd = request.GET.get('createDateEnd', '')
        if tmpEnd:
            t_stocking_demand_fba_detail_Admin.creatEndTime = tmpEnd

        Status1 = request.GET.get('Status1', '')  # 采购状态
        if Status1 != '':
            qs = qs.filter(Status=Status1)
        ProductSKU = request.GET.get('ProductSKU', '')                     #商品sku
        AuditFlag = request.GET.get('AuditFlag', '')  # 核实状态

        searchList = {
                        'ProductSKU__icontains': ProductSKU,
                        'AuditFlag__exact': AuditFlag,
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
        return qs

