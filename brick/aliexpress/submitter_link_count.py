#-*-encoding:utf-8-*-
import MySQLdb
import json
from brick.classredis.classshopsku import classshopsku
import datetime
import traceback

class submitter_link_count(object):
    def __init__(self):
        self.connection = MySQLdb.connect(user="by15161458383",passwd="K120Esc1",host="rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com",db="hq",port=3306,charset='utf8')
    
    def close_db(self):
        self.connection.close()
        
    def get_submitter(self,datestart,dateafter):
        classshopsku_obj = classshopsku(self.connection)
        mycur = self.connection.cursor()

        sql = '''select product_skus,shopName from t_erp_aliexpress_online_info where gmt_create > '%s' and gmt_create < '%s' ''' % (datestart,dateafter)
        mycur.execute(sql)
        
        product_skus = mycur.fetchall()
        submitter_all = {}
        shopName_list = []#店铺统计
        submitter_list = []#刊登人统计
        
        for product_sku in product_skus:
            try:
                sku_infos = json.loads(product_sku[0])
                sku_info_list = sku_infos.get('aeop_ae_product_sku', '')
                for i in range(len(sku_info_list)):
                    shopsku = sku_info_list[i].get('sku_code', '')
                    submitter = classshopsku_obj.getPublished(shopsku)
                    if submitter is None:
                        submitter = classshopsku_obj.getPublished(shopsku.split('\\')[0].split('*')[0])
                    
                    if not submitter or len(submitter) < 2:
                        submitter = '空'.decode('utf-8')
                    key = '%s%s%s' % (product_sku[1],'|',submitter)#店铺|刊登人

                    if product_sku[1] not in shopName_list:#新的店铺
                        shopName_list.append(product_sku[1])
                        submitter_list.append(submitter_list)
                        submitter_all.setdefault(key,0)
                    else:
                        if submitter not in submitter_list:#新的刊登人
                            submitter_list.append(submitter_list)
                            submitter_all.setdefault(key,0) 
                    submitter_all[key] = submitter_all[key] + 1
                    break
            except Exception, e:
                print traceback.print_exc()
        mycur.close()
        return submitter_all
         
    def insert_db(self):
        #dateinit = '2018-07-01'
        #datestart = datetime.datetime.strptime(dateinit,'%Y-%m-%d')
        dateend = datetime.datetime.now().strftime('%Y-%m-%d')
        dateend = datetime.datetime.strptime(dateend,'%Y-%m-%d')
        datestart = dateend - datetime.timedelta(days=7)
        
        while datestart < dateend:
            dateafter = datestart + datetime.timedelta(days=1)
            result_dict = {}
            result_dict = self.get_submitter(datestart,dateafter)
            if result_dict:
                mycur = self.connection.cursor()
                try:
                    for key in result_dict:
                        shopName_list = key.split('|')
                        #shopName_list.append(result_dict[key])
                        print shopName_list

                        sql = '''insert into t_erp_aliexpress_shop_link_daily(gmt_create,shopName,link_number,submitter) 
                                values('%s','%s',%s,'%s')''' % (datestart.strftime('%Y-%m-%d'),shopName_list[0],result_dict[key],shopName_list[1])
                        mycur.execute(sql)
                        
                except Exception, e:
                    print traceback.print_exc()
            datestart += datetime.timedelta(days=1)
        sql = '''update t_erp_aliexpress_shop_link_daily a,t_erp_aliexpress_shop_info b set
                a.seller_zh = b.seller_zh,a.accountName = b.accountName where 
                a.shopName = b.shopName'''
        mycur.execute(sql)
        
        self.connection.commit()
        mycur.close()
        self.close_db()
if __name__ == '__main__':
    req = submitter_link_count()
    req.insert_db()