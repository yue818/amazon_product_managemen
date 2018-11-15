# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_online_info_wish.py
 @time: 2017-12-22 13:10

"""   

class t_online_info_wish():
    def __init__(self,db_cnxn):
        self.db_cnxn = db_cnxn

    def refreshwishdata(self,params):
        mycur = self.db_cnxn.cursor()
        mycur.execute("insert into t_online_info_wish set "
                      "PlatformName='Wish',ProductID=%s,ShopIP='',ShopName=%s,Title=%s,SKU=%s,"
                      "ShopSKU=%s,Price=%s,Quantity=0,Orders7Days=%s,SoldYesterday=%s,"
                      "SoldTheDay=%s,SoldXXX=%s,DateOfOrder=%s,RefreshTime=%s,"
                      "Image=%s,Status=%s,ReviewState=%s,DateUploaded=%s,LastUpdated=%s,OfSales=%s,"
                      "ParentSKU=%s,Seller=%s,TortInfo=%s,MainSKU=%s,DataSources=%s,OperationState=%s"
                      ",Published=%s,market_time=%s,is_promoted=%s,WishExpress=%s,SName=%s,MainSKULargeCate=%s,"
                      "MainSKUSmallCate=%s,GoodsFlag=%s,ShopsFlag=%s,BindingFlag=%s,BeforeReviewState=%s,"
                      "AdStatus=%s,Rating=%s,ADShow=%s,SalesTrend=%s,Order7daysDE=%s,Order7daysGB=%s,"
                      "Order7daysUS=%s,OfsalesDE=%s,OfsalesGB=%s,OfsalesUS=%s,"
                      "Order7daysFBW=%s,OfsalesFBW=%s,FBW_Flag=%s"
                      " on duplicate KEY update"
                      " Title=%s,Orders7Days=%s,SoldYesterday=%s,"
                      "SoldTheDay=%s,SoldXXX=%s,DateOfOrder=%s,RefreshTime=%s,Status=%s,"
                      "ReviewState=%s,DateUploaded=%s,LastUpdated=%s,OfSales=%s,Seller=%s,"
                      "MainSKU=%s,DataSources=%s,OperationState=%s,Published=%s,"
                      "market_time=%s,ShopSKU=%s,is_promoted=%s,WishExpress=%s,"
                      "MainSKULargeCate=%s,MainSKUSmallCate=%s,GoodsFlag=%s,ShopsFlag=%s,"
                      "AdStatus=%s,"
                      "BeforeReviewState=%s,Rating=%s,ADShow=%s,SalesTrend=%s,Image=%s,Order7daysDE=%s,Order7daysGB=%s,"
                      "Order7daysUS=%s,OfsalesDE=%s,OfsalesGB=%s,OfsalesUS=%s,"
                      "Order7daysFBW=%s,OfsalesFBW=%s,FBW_Flag=%s ;",
                      (params['ProductID'],params['ShopName'],params['Title'],params['SKU'],
                       params['ShopSKU'],params['Price'],params['Orders7Days'],params['SoldYesterday'],
                       params['SoldTheDay'],params['SoldXXX'],params['DateOfOrder'],params['RefreshTime'],
                       params['Image'],params['Status'],params['ReviewState'],params['DateUploaded'],
                       params['LastUpdated'],params['OfSales'],params['ParentSKU'],params['Seller'],
                       params['TortInfo'], params['MainSKU'], params['DataSources'], params['OperationState'],
                       params['Published'],params['market_time'],params['is_promoted'],params['WishExpress'],
                       params['SName'], params['MainSKULargeCate'], params['MainSKUSmallCate'],
                       params['GoodsFlag'], params['ShopsFlag'], params['BindingFlag'],params['BeforeReviewState'],
                       params['AdStatus'],params['Rating'],params['ADShow'],params['SalesTrend'],
                       params['Order7daysDE'], params['Order7daysGB'], params['Order7daysUS'],
                       params['OfsalesDE'], params['OfsalesGB'], params['OfsalesUS'],
                       params['Order7daysFBW'], params['OfsalesFBW'], params['FBW_Flag'],
                       # --------------------------分割线----------------------- #
                       params['Title'],params['Orders7Days'],params['SoldYesterday'],params['SoldTheDay'],
                       params['SoldXXX'],params['DateOfOrder'],params['RefreshTime'],params['Status'],params['ReviewState'],
                       params['DateUploaded'],params['LastUpdated'],params['OfSales'],params['Seller'],
                       params['MainSKU'], params['DataSources'], params['OperationState'],
                       params['Published'], params['market_time'],params['ShopSKU'],params['is_promoted'],
                       params['WishExpress'],params['MainSKULargeCate'],params['MainSKUSmallCate'],
                       params['GoodsFlag'],params['ShopsFlag'], params['AdStatus'],
                       params['BeforeReviewState'],params['Rating'],params['ADShow'],params['SalesTrend'],params['Image'],
                       params['Order7daysDE'], params['Order7daysGB'], params['Order7daysUS'],
                       params['OfsalesDE'], params['OfsalesGB'], params['OfsalesUS'],
                       params['Order7daysFBW'], params['OfsalesFBW'], params['FBW_Flag'],
                       ))
        mycur.execute("commit;")
        mycur.close()


    def UpdateWishStatusAD(self,productid,status):
        '''
        :param productid:
        :param status: 1 正常(在线); 0 正常(不在线); -1 api调用错误; -2 执行代码异常;
        :return:
        '''
        try:
            if status:
                cursor = self.db_cnxn.cursor()
                cursor.execute("update t_online_info_wish set AdStatus=%s WHERE ProductID=%s;",(status,productid,))
                cursor.execute("commit;")
                cursor.close()
            return {'errorcode': 1, 'errortext': status}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}

    def UpdateWishSNameByShopName(self,shopname,status,f=0):
        '''
        :param shopname:
        :param status:  0 店铺状态正常; -1 店铺状态异常
        :return:
        '''
        try:
            if status == '0':
                statustmp = '-1'
            elif status == '-1':
                statustmp = '0'
            else:
                return {'errorcode': 1, 'errortext': status}

            cursor = self.db_cnxn.cursor()
            cursor.execute("SELECT ProductID from t_online_info_wish WHERE ShopName=%s AND (SName=%s or SName is NULL);", (shopname,statustmp, ))
            sobjs = cursor.fetchall()
            for sobj in sobjs:
                cursor.execute("update t_online_info_wish set SName=%s WHERE ProductID=%s and ShopName=%s;",(status,sobj[0],shopname,))

                if f == 0: # 为了兼容 店铺配置文件中 的事务性
                    cursor.execute("commit;")
            cursor.close()
            return {'errorcode': 1, 'errortext': status}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}


    def UpdateWishStatus(self,productid,status):
        try:
            cursor = self.db_cnxn.cursor()
            cursor.execute("update t_online_info_wish set Status=%s WHERE ProductID=%s;",(status,productid,))
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode': 1, 'errortext': ''}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}


    def get_product_id_rating(self, product_id):
        try:
            cursor = self.db_cnxn.cursor()
            cursor.execute("SELECT Rating from t_online_info_wish WHERE ProductID=%s ;",(product_id,))
            sobj = cursor.fetchone()
            cursor.close()
            if sobj:
                return {'errorcode': 1, 'rating': sobj[0]}
            else:
                return {'errorcode': 0, 'errortext': u'该product_id: %s 没有找到记录 ' % product_id}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}


