#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_wish_shopcode_warehouse.py
 @time: 2018/6/1 10:46
"""

class t_wish_shopcode_warehouse():
    def __init__(self, conn):
        self.conn = conn

    def update_shopcode_waregouse(self, shopcode, datadict):
        """
        :param shopcode:
        :param datadict:
        :return:
        """
        try:
            paramlist = [[shopcode, 'STANDARD', 'STANDARD', 'STANDARD']]
            for ddk, ddv in datadict.items():
                paramlist.append([shopcode, ddk, ddv, ddv])

            cursor = self.conn.cursor()
            cursor.executemany("insert into t_wish_shopcode_warehouse set shopcode=%s, warecode=%s, warehouse=%s "
                               "on duplicate KEY update warehouse=%s;", paramlist)

            cursor.execute("commit;")
            cursor.close()
            return {'errorcode': 1, 'errortext': ''}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}


    def get_warehouse(self,shopcode):
        """
        :param shopcode:
        :return:
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("select warecode, warehouse from t_wish_shopcode_warehouse WHERE shopcode=%s ;", (shopcode, ))
            objs = cursor.fetchall()
            cursor.close()
            ddict = {}
            for obj in objs:
                ddict[obj[0]] = obj[1]
            if ddict:
                return {'errorcode': 1, 'errortext': '', 'warehouse': ddict, 'params': shopcode}
            else:
                return {'errorcode': 0,
                        'errortext': u'没有找到该店铺相关的仓库信息,店铺状态可能有问题或token信息错误 ShopCode：%s' % shopcode,
                        'warehouse': ddict,
                        'params': shopcode}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e), 'params': shopcode}




