#coding=utf-8  
import datetime
import os, glob, cookielib , sys , oss2
import MySQLdb
import string
from xlwt import *
csvkcheaders = [u"网址6", u"SKU码", u"商品成本单价", u"商品名称", u"商品状态", u"库存数量", 
                u"7天销量", u"15天销量", u"30天销量", u"采购未入库", u"预计可用库存", u"型号",u"供应商",
                u"网址", u"网址2",u"网址3", u"采购员",u"缺货及未派单数量", u"占用数量", u"可用数量",
                u"业绩归属1", u"业绩归属2",u"建议采购数量", u"库存上限", u"库存下限",u"仓库",
                u"库位",u"建议采购", u"款式3", u"平均单价",u"库存金额", u"可卖天数", u"最低采购价格",
                u"日平均销量", u"商品类别", u"商品创建时间",u"默认发货仓库", u"商品重量(克)", 
                u"最长采购缺货天数",u"网址4", u"网址5", u"缺货占用数量",u"是否停用", u"商品成本金额",
                u"多款式网址",u"责任归属1", u"责任归属2",]
class upload_kc_to_oss(object):
    def __init__(self):
        self.onlineConn = "init..."  
    def uploadOss(self,username,filename):
        ossAuth=oss2.Auth('LTAIH6IHuMj6Fq2h','N5eWsbw8qBkMfPREkgF2JnTsDASelM')
        ossBucket=oss2.Bucket(ossAuth,'oss-cn-shanghai.aliyuncs.com','fancyqube-kc-csv')
        ossBucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        
        for  object_info in oss2.ObjectIterator(ossBucket,prefix='%s/%s'%(username,username)):
            ossBucket.delete_object(object_info.key)
        remoteName = username + "/" + os.path.basename(filename)
        try:
            result=ossBucket.put_object_from_file(remoteName,filename)
            os.remove(filename)
            print "upload success!"
        except Exception,e:
            print "error ",e
            return -1

    def write_excel(self,Purchaser,username,Purchaser_one_data):
        #print "time:",(datetime.datetime.now() - s)
        w = Workbook()
        sheet = w.add_sheet(u'库存预警')
    
        for i in range(len(csvkcheaders)):
            sheet.write(0,i,csvkcheaders[i])
        cloumn = 0
        try:
            for data in Purchaser_one_data:
                cloumn = cloumn + 1
                sheet.write(cloumn,0,data['LinkUrl6'])
                sheet.write(cloumn,1,data['SKU'])
                sheet.write(cloumn,2,data['CostPrice'])
                sheet.write(cloumn,3,data['GoodsName'])
                
        
                if data['GoodsStatus'] == 'normal':#商品状态
                    sheet.write(cloumn,4,u'正常')
                elif data['GoodsStatus'] == 'over':
                    sheet.write(cloumn,4,u'售完下架')
                elif data['GoodsStatus'] == 'temporary':
                    sheet.write(cloumn,4,u'临时下架')
                else:
                    sheet.write(cloumn,4,u'停售')
                
                sheet.write(cloumn,5,data['Number'])                
                sheet.write(cloumn,6,data['SellCount1'])
                sheet.write(cloumn,7,data['SellCount2'])
                sheet.write(cloumn,8,data['SellCount3'])
                
                sheet.write(cloumn,9,data['NotInStore'])
                sheet.write(cloumn,10,data['hopeUseNum'])
                sheet.write(cloumn,11,data['Model'])
                sheet.write(cloumn,12,data['SupplierName'])
                sheet.write(cloumn,13,data['LinkUrl'])
                sheet.write(cloumn,14,data['LinkUrl2'])
                sheet.write(cloumn,15,data['LinkUrl3'])
                
                sheet.write(cloumn,16,data['Purchaser'])
                sheet.write(cloumn,17,data['UnPaiDNum'])
                sheet.write(cloumn,18,data['ReservationNum'])
                sheet.write(cloumn,19,data['UseNumber'])
                
                sheet.write(cloumn,20,data['SalerName'])
                sheet.write(cloumn,21,data['SalerName2'])
                sheet.write(cloumn,22,data['SuggestNum'])
                sheet.write(cloumn,23,data['KcMaxNum'])
                sheet.write(cloumn,24,data['KcMinNum'])
                if data['storeID'] == 1:#仓库
                    sheet.write(cloumn,25,u'浦江仓库')
                elif data['storeID'] == 2:
                    sheet.write(cloumn,25,u'亚马逊仓库')
                elif data['storeID'] == 3:
                    sheet.write(cloumn,25,u'海外仓仓库')
                else:
                    sheet.write(cloumn,25,u'其它仓库')
        
                sheet.write(cloumn,26,data['LocationName'])
                if data['IsCg'] == 'Y':#建议采购-----------------------
                    sheet.write(cloumn,27,1)
                else:
                    sheet.write(cloumn,27,0)
            
                sheet.write(cloumn,28,data['Style'])
                sheet.write(cloumn,29,data['Price'])
                sheet.write(cloumn,30,data['Money'])
                sheet.write(cloumn,31,data['SaleDay'])
                sheet.write(cloumn,32,data['MinPrice'])
                sheet.write(cloumn,33,data['AverageNumber'])
                sheet.write(cloumn,34,data['CategoryCode'])
                sheet.write(cloumn,35,str(data['CreateDate']))
                if data['storeID'] == 1:#仓库
                    sheet.write(cloumn,36,u'浦江仓库')
                elif data['storeID'] == 2:
                    sheet.write(cloumn,36,u'亚马逊仓库')
                elif data['storeID'] == 3:
                    sheet.write(cloumn,36,u'海外仓仓库')
                else:
                    sheet.write(cloumn,36,u'其它仓库')
                sheet.write(cloumn,37,data['Weight'])
                sheet.write(cloumn,38,data['MaxDelayDays'])
                sheet.write(cloumn,39,data['LinkUrl4'])
                sheet.write(cloumn,40,data['LinkUrl5'])
                sheet.write(cloumn,41,data['SaleReNum'])
                sheet.write(cloumn,42,data['Used'])
                sheet.write(cloumn,43,data['AllCostPrice'])
                sheet.write(cloumn,44,data['MoreStyleUrl'])
                sheet.write(cloumn,45,data['possessMan1'])
                sheet.write(cloumn,46,data['possessMan2'])
        except Exception as e:
            print(e.message)

        filename = username + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(filename)

        return filename