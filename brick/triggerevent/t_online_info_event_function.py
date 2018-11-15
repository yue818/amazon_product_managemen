#-*-coding:utf-8-*-
"""
 @desc:
 @author: wangzy
 @site:
 @software: PyCharm
 @file: t_online_info_event_function.py
 @time: 2018/5/23 13:47
"""


class t_online_info_event_function():
    def __init__(self,db_conn):
        self.cnxn = db_conn

    '''
    说明:根据sku获取t_online_info表中ProductID
    入参:商品SKU
    出参:列表中存放ProductID
    '''
    def get_allProductid_by_sku(self,sku):
        try:
            cursor = self.cnxn.cursor()
            cursor.execute(
                "select DISTINCT ProductID from t_online_info WHERE SKU = %s;", (sku,))
            objs = cursor.fetchall()
            cursor.close()
            productidlist = []
            for obj in objs:
                productidlist.append(obj[0])

            return {'errorcode': 1, 'errortext': u'', 'list': productidlist}
        except Exception, e:
            return {'errorcode': -1, 'errortext': 'get_allProductid_by_sku:%s:%s' % (Exception, e)}

    '''
    说明:根据sku更新t_online_info表中GoodsStatus值
    入参:商品状态、商品SKU
    出参:更新结果
    '''
    def updata_by_sku(self, goodsstatus, sku):
        try:
            productidlist = []
            cursor = self.cnxn.cursor()
            cursor.execute(
                "UPDATE t_online_info SET GoodsStatus = %s WHERE SKU = %s;", (goodsstatus, sku,))
            cursor.close()
            return {'errorcode': 1, 'errortext': u'', 'list': productidlist}
        except Exception, e:
            return {'errorcode': -1, 'errortext': 'updata_by_sku:%s:%s' % (Exception, e)}

    '''
        说明:根据sku更新t_online_info表中sku置为空
        入参:商品SKU
        出参:更新结果
        '''
    def updata_sku_by_sku(self, sku):
        try:
            productidlist = []
            cursor = self.cnxn.cursor()
            cursor.execute(
                "UPDATE t_online_info SET sku = %s WHERE SKU = %s;", (None, sku,))
            cursor.close()
            return {'errorcode': 1, 'errortext': u'', 'list': productidlist}
        except Exception, e:
            return {'errorcode': -1, 'errortext': 'updata_sku_by_sku:%s:%s' % (Exception, e)}

    '''
    说明:根据sku更新t_online_info_wish表中GoodsFlags值
    入参:productid、商品状态
    出参:更新结果
    '''
    def updata_by_productid(self, productid,GoodsFlag):
        try:
            productidlist = []
            cursor = self.cnxn.cursor()
            cursor.execute(
                "UPDATE t_online_info_wish SET GoodsFlag = %s WHERE ProductID = %s ;",(GoodsFlag, productid,))
            cursor.close()
            return {'errorcode': 1, 'errortext': u'', 'list': productidlist}
        except Exception, e:
            return {'errorcode': -1, 'errortext': 'updata_by_productid:%s:%s' % (Exception, e)}


    '''
    说明：根据product获取所有商品状态
    '''
    def get_goodsstatus_by_productid(self,productid,strSKU):
        try:
            cursor = self.cnxn.cursor()
            print(productid)
            cursor.execute("select DISTINCT GoodsStatus from t_online_info WHERE ProductID =%s and SKU is not NULL ;",(productid,))
            infos = cursor.fetchall()
            cursor.close()
            infolist = []
            for info in infos:
                infolist.append(info[0])
            return {'errorcode': 1, 'errortext': u'', 'list': infolist}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}