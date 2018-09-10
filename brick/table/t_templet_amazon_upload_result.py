#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_upload_result.py
 @time: 2017/12/23 17:15
"""
class t_templet_amazon_upload_result():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def getMQResponseInfos(self, params):
        shocur = self.db_conn.cursor()
        shocur.execute("select id,mqResponseInfo from t_templet_amazon_upload_result  where `status` = 'OPEN' ;")
        t_templet_amazon_upload_result_objs = shocur.fetchall()
        mqResponseInfoIds = []
        for t_templet_amazon_upload_result_obj in t_templet_amazon_upload_result_objs:
            mqResponseInfos = {}
            mqResponseInfos['id'] = t_templet_amazon_upload_result_obj[0]
            mqResponseInfos['mqResponseInfo'] = t_templet_amazon_upload_result_obj[1]
            mqResponseInfoIds.append(mqResponseInfos)
        shocur.close()
        return mqResponseInfoIds

    def updateStatus(self,params):
        shocur = self.db_conn.cursor()
        shocur.execute("update t_templet_amazon_upload_result set `status`=%s,resultInfo=%s,errorMessages=%s,mqResponseInfo=%s where id = %s ;",
                       (params['status'],params['resultInfo'],params['errorMessages'],str(params['mqResponseInfo']).replace('"','').replace("'", ''),params['id']))
        shocur.execute("commit;")
        shocur.close()



