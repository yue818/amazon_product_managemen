#-*-coding:utf-8-*-
"""
 @desc:  更新上传相关库存数据
 @author: changyang
 @site:
 @software: PyCharm
 @file: upload_kc_data.py
 @time: 2018-05-17 11:42
"""
import os
import oss2
import pymssql
import pymysql
import datetime
import pandas as pd
import zipfile
import csv
import codecs
#from django.db import connection
from brick.function.updatetasklog import updatetasklog

connection = pymysql.connect(user="by15161458383", passwd="K120Esc1", host="rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com",db="py_db",port=3306,charset='utf8')

csvkcheaders = [u"商品SKU", u"商品名称", u"供应商", u"商品状态", u"商品成本单价", u"库存数量", 
                u"预计可用库存", u"7天销量", u"15天销量", u"30天销量",u"采购未入库", u"网址", 
                u"网址2",u"网址3", u"型号", u"采购员",u"缺货及未派单数量", u"占用数量", u"可用数量",
                u"网址6", u"业绩归属1", u"业绩归属2",u"建议采购数量", u"库存上限", u"库存下限",u"仓库",
                u"库位",u"建议采购", u"款式3", u"平均单价",u"库存金额", u"可卖天数", u"最低采购价格",
                u"日平均销量", u"商品类别", u"商品创建时间",u"默认发货仓库", u"商品重量(克)", 
                u"最长采购缺货天数",u"网址4", u"网址5", u"缺货占用数量",u"是否停用", u"商品成本金额",
                u"多款式网址",u"责任归属1", u"责任归属2", u"原始采购等级"]
class upload_kc_data(object):
    def __init__(self):
        # self.pyuanConn = pymssql.connect(host='122.226.216.10', port=18794, user='fancyqube', password='K120Esc1',database='ShopElf', charset='utf8')
        self.pyuanConn = pymssql.connect(host='122.226.216.10', port=18793, user='sa', password='$%^AcB2@9!@#',
                                         database='ShopElf', charset='utf8')
        self.curtime = datetime.datetime.now().strftime('%H%M%S')

    def uploadOss(self, username, filename):
        ossAuth=oss2.Auth('LTAIH6IHuMj6Fq2h', 'N5eWsbw8qBkMfPREkgF2JnTsDASelM')
        ossBucket=oss2.Bucket(ossAuth, 'oss-cn-shanghai.aliyuncs.com', 'fancyqube-kc-csv')
        ossBucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        
        for object_info in oss2.ObjectIterator(ossBucket, prefix='%s/' % (username,)):
            ossBucket.delete_object(object_info.key)
        remoteName = username + "/" + os.path.basename(filename)
        try:
            result = ossBucket.put_object_from_file(remoteName, filename)
            os.remove(filename)
            print "upload success!"
            return result
        except Exception, e:
            print "error ", e
            return -1

    def write_excel(self):
        #df = pd.read_sql(sql, con=connection)

        filename = datetime.datetime.now().strftime('%Y-%m-%d %H%M%S') + '_库存预警'.decode('utf-8') + '.csv'
        #df.to_csv(filename, index=False, header=csvkcheaders, encoding='gbk')
        #out = open(filename,'wb')
        #out.write(codecs.BOM_UTF8)
        out = codecs.open(filename,'a',encoding='gbk')
        csv_write = csv.writer(out,dialect='excel')
        csv_write.writerow(csvkcheaders)
        
        cur = connection.cursor()
        #--------------------总的
        sql = '''Select SKU,GoodsName,SupplierName,pyGoodsStatus as GoodsStatus,CostPrice,Number,hopeUseNum,SellCount1,
            SellCount2,SellCount3,NotInStore,LinkUrl,LinkUrl2,LinkUrl3,Model,Purchaser,UnPaiDNum,ReservationNum,
            UseNumber,LinkUrl6,SalerName,SalerName2,SuggestNum,KcMaxNum,KcMinNum,'浦江仓库'as StoreName,LocationName,
            IsCg,Style,Price,Money,SaleDay,MinPrice,AverageNumber,CategoryCode,CreateDate,'浦江仓库'as DefStoreName,
            Weight, MaxDelayDays,LinkUrl4,LinkUrl5,SaleReNum,Used,AllCostPrice,MoreStyleUrl,possessMan1,possessMan2,SourceOSCode
            from py_db.kc_currentstock_sku where StoreID=1 and Used=0  '''
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            csv_write.writerow(row)
            
        # 压缩
        filename_zip = filename.replace('csv', 'zip')
        f = zipfile.ZipFile(filename_zip, 'w', zipfile.ZIP_DEFLATED)
        f.write(filename)
        f.close()

        username = 'kc_current_stock'
        self.uploadOss(username, filename_zip)

    def getdata(self):
        # 从普源取数据
        with self.pyuanConn.cursor() as cursor:
            cursor.execute('exec p_online_PurchasingWarning')
            data = cursor.fetchall()
        self.pyuanConn.commit()

        cursor = connection.cursor()

        # 删除临时表数据(临时表中间数据过渡)
        SQL = '''truncate table py_db.kc_currentstock_sku_tempall '''
        cursor.execute(SQL)
        connection.commit()

        # 向临时表插入需要更新的数据
        cursor.execute('call py_db.sp_kc_currentstock_task(0)')
        SQL = cursor.fetchone()[0]

        cursor.executemany(SQL, data)
        connection.commit()

        # 更新数据到SKU表
        cursor.execute('call py_db.sp_kc_currentstock_task(1)')
        connection.commit()
        cursor.close()
        print u'采购预警数据已更新完成!'

    def updateskuloginfo(self):

        cursor = connection.cursor()

        if self.curtime >= '170000':
            cursor.execute('call py_db.sp_kc_currentstock_task(3)') #更新采购任务表18:00

            cursor.execute('call py_db.sp_kc_currentstock_task(4)') #捕获 补单，备货，多采单 18:00
        else:
            cursor.execute('call py_db.sp_kc_currentstock_task(2)') #插入采购任务表6:30

        connection.commit()
        cursor.close()
        print u'采购任务单已更新完成!'

    def get_clothing_data(self):

        cursor = connection.cursor()
        cursor.execute('call py_db.sp_kc_currentstock_task(5)') #广州服装 供应链商品 任务 6:30
        connection.commit()
        cursor.close()
        print u'服装供应链采购任务更新完成!'

    def day_interval(self, lag=1):
        to_day = datetime.date.today() - datetime.timedelta(days=lag)
        day1 = datetime.datetime(year=to_day.year, month=to_day.month, day=to_day.day)
        begin = day1 - datetime.timedelta(hours=8)
        end = day1 + datetime.timedelta(hours=16) - datetime.timedelta(seconds=1)

        to_day = to_day.strftime('%Y-%m-%d')
        begin = begin.strftime('%Y-%m-%d %H:%M:%S')
        end = end.strftime('%Y-%m-%d %H:%M:%S')

        return to_day, begin, end

    def get_sku_statistics(self):
        SQL1 ='call py_db.sp_kc_currentstock_task(6)'

        #-- and pt.FilterFlag = 1
        SQL2 = 'exec p_online_StockStatistics %s,%s'

        SQL3 = '''update py_db.kc_currentstock_sku_statistics 
                set UpdateTime=sysdate(),
                NormalNum=%s,
                abNormalNum=%s,
                Ratio=%s
                where StDay=%s'''

        if self.curtime >= '170000':  # 插入新数据
            cursor = connection.cursor()
            cursor.execute(SQL1)
            connection.commit()
            cursor.close()
        else:# 更新
            cursor1 = self.pyuanConn.cursor()
            interval = self.day_interval(1)
            cursor1.execute(SQL2, (interval[1], interval[2], ))
            data = cursor1.fetchone() #NormalNum,abNormalNum,Ratio,OrderDay
            cursor1.close()

            cursor2 = connection.cursor()
            cursor2.execute(SQL3, data)
            connection.commit()
            cursor2.close()

        print u'缺货率数据已更新完成!'

    def closeconn(self):
        self.pyuanConn.close()

    def run(self):
        taskid = ''
        try:
            # 以防跑重复
            if self.curtime < '170000':
                sql = 'SELECT SKU FROM kc_currentstock_sku_log WHERE PODate=CURDATE() LIMIT 20'
                cursor = connection.cursor()
                cursor.execute(sql)
                if cursor.rowcount >= 10:
                    print 'Already runned ......'
                    cursor.close()
                    self.closeconn()
                    return

            taskid = updatetasklog(conn=connection, exectype=1)
            self.getdata()

            self.updateskuloginfo()

            self.get_sku_statistics()

            if self.curtime < '170000':
                self.get_clothing_data()

                self.write_excel()

            updatetasklog(conn=connection, taskid=taskid, exectype=2)
            self.closeconn()
        except Exception, ex:
            updatetasklog(conn=connection, taskid=taskid, exectype=3, msg=repr(ex))

if __name__ == '__main__':

    rep = upload_kc_data()
    rep.run()