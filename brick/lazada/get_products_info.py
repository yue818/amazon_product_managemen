#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2018-08-20 10:45
@Author  : chenchen
@Site    : lazada
@File    : get_products_info.py
@Software: PyCharm
'''
import lazop
import MySQLdb
import time,datetime
import re
import json
from lzd_app.table.t_online_info_lazada_detail import t_online_info_lazada_detail



class get_products_info():
    def __init__(self,ip,appkey,appSecret):
        conn = MySQLdb.connect(host='rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com', user='by15161458383', passwd='K120Esc1',
                           db='hq_db', port=3306,
                           charset='utf8')
        self.conn = conn
        self.cur = conn.cursor()
        cur = self.cur
        site_dic = {
            'Philippines':'api.lazada.com.ph/rest',
            'Indonesia':'api.lazada.co.id/rest',
            'Vietnam':'api.lazada.vn/rest',
            'Singapore':'api.lazada.sg/rest',
            'Thailand':'api.lazada.co.th/rest',
            'Malaysia':'api.lazada.com.my/rest'
        }

        # try:
        new_dic = {}
        for k,v in site_dic.items():
            sql = "SELECT access_token,shopname FROM t_config_online_lazada WHERE ip = '%s' AND site = '%s'"%(ip,k)
            cur.execute(sql)
            row = cur.fetchone()
            try:
                new_dic[k] = '%s,%s,http://%s:9193/fancyqube/%s'%(row[0],row[1],ip,v)
            except:
                continue
        # except Exception:
        #     print u'没获取到当前的access_token或者token已失效!!!'
        self.ip = ip
        self.new_dic = new_dic
        self.appkey = appkey
        self.appSecret = appSecret

    def get_products(self,):
        cur = self.cur
        for k,v in self.new_dic.items():
            sum = 0
            while True:
                client = lazop.LazopClient(v.split(",")[2],self.appkey,self.appSecret)
                request = lazop.LazopRequest('/products/get','GET')
                request.add_api_param('filter', 'all')
                request.add_api_param('offset', str(sum))
                request.add_api_param('limit', '300')
                request.add_api_param('options', '1')
                response = client.execute(request, v.split(",")[0])
                try:
                    products_info = response.body['data']['products']
                except:
                    sum = sum + 100
                    continue
                count = len(products_info)
                #TODO
                lis = []
                for pro_info in products_info:
                    item_id = pro_info.get('item_id')
                    attributes = pro_info.get('attributes')
                    name = attributes.get('name')
                    brand = attributes.get('brand')
                    warranty_type = attributes.get('warranty_type')
                    dr = re.compile(r'<[^>]+>', re.S)
                    try:
                        short_description = dr.sub('', attributes.get('short_description'))
                    except:
                        short_description = ''
                    model = attributes.get('model')
                    try:
                        description = dr.sub('', attributes.get('description'))
                    except:
                        description = ''
                    primary_category = pro_info.get('primary_category')
                    lis.append([item_id,v.split(",")[1],k,name,brand,warranty_type,short_description,model,description,primary_category,datetime.datetime.now(),1,v.split(",")[1],k,`name`,brand,warranty_type,short_description,model,description,primary_category,datetime.datetime.now(),1])

                    skus = pro_info.get('skus')
                    lis2 = []
                    for skus_info in skus:
                        if len(skus) == 1:
                            color_family = attributes.get('color_family')
                        else:
                            color_family = skus_info.get('color_family')
                        package_width = skus_info.get('package_width')
                        special_from_time = skus_info.get('special_from_time')
                        Available = skus_info.get('Available')
                        compatible_variation = skus_info.get('_compatible_variation_')
                        package_length = skus_info.get('package_length')
                        fulfillmentStock = skus_info.get('fulfillmentStock')
                        Status = skus_info.get('Status')
                        SkuId = skus_info.get('SkuId')
                        Url = skus_info.get('Url')
                        price = skus_info.get('price')
                        special_price = skus_info.get('special_price')
                        package_weight = skus_info.get('package_weight')
                        nonsellableStock = skus_info.get('nonsellableStock')
                        package_height = skus_info.get('package_height')
                        package_content = skus_info.get('package_content')
                        special_to_time = skus_info.get('special_to_time')
                        ReservedStock = skus_info.get('ReservedStock')
                        SellerSku = skus_info.get('SellerSku')
                        special_from_date = skus_info.get('special_from_date')
                        ShopSku = skus_info.get('ShopSku')
                        special_to_date = skus_info.get('special_to_date')
                        AllocatedStock = skus_info.get('AllocatedStock')
                        Images = str(skus_info.get('Images'))
                        quantity = skus_info.get('quantity')
                        lis2.append([item_id, ShopSku, color_family, package_width, special_from_time, Available,
                                     compatible_variation, package_length, fulfillmentStock, Status, SkuId, Url, price,
                                     special_price, package_weight, nonsellableStock, package_height,
                                     package_content, special_to_time, ReservedStock, SellerSku, special_from_date,
                                     special_to_date, AllocatedStock, Images, quantity, color_family, package_width,
                                     special_from_time, Available, compatible_variation, package_length,
                                     fulfillmentStock, Status,
                                     SkuId, Url, price, special_price, package_weight, nonsellableStock, package_height,
                                     package_content, special_to_time, ReservedStock, SellerSku, special_from_date,
                                     special_to_date, AllocatedStock, Images, quantity])
                    sql2 = 'INSERT INTO t_online_info_lazada_detail (item_id,ShopSku,color_family,package_width,special_from_time,Available,compatible_variation,package_length,fulfillmentStock,Status,SkuId,Url,price,special_price,package_weight,nonsellableStock,package_height,package_content,special_to_time,ReservedStock,SellerSku,special_from_date,special_to_date,AllocatedStock,Images,quantity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
                           ' on duplicate key update color_family = %s,package_width=%s,special_from_time=%s,Available=%s,compatible_variation=%s,package_length=%s,fulfillmentStock=%s,Status=%s,SkuId=%s,Url=%s,price=%s,special_price=%s,package_weight=%s,nonsellableStock=%s,package_height=%s,package_content=%s,special_to_time=%s,ReservedStock=%s,SellerSku=%s,special_from_date=%s,special_to_date=%s,AllocatedStock=%s,Images=%s,quantity=%s;'
                    cur.executemany(sql2, lis2)
                    cur.execute("commit;")
                    lis2 = []


                sql = 'INSERT INTO t_online_info_lazada (item_id,shopname,site,`name`,brand,warranty_type,short_description,model,description,primary_category,updatetime,refresh_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update shopname =%s,site=%s,`name`=%s,brand=%s,warranty_type=%s,short_description=%s,model=%s,description=%s,primary_category=%s,updatetime=%s,refresh_status=%s;'
                cur.executemany(sql,lis)
                cur.execute("commit;")
                lis = []

                if count < 300:
                    sum = sum + count
                    print '>>>>>>>>>>>>>>>>>>{}站点抓取结束,总记录为{}条'.format(k,sum)
                    break
                sum = sum + 300
                print '>>>>>>>>>>>>>>>>>已抓取{}站点{}条产品信息'.format(k,sum)
            sql_u1 = 'UPDATE t_online_info_lazada SET status = 2 WHERE refresh_status = 0 AND shopname = "%s" AND site = "%s"' % (v.split(",")[1].strip(), k)  # 未刷新的置为异常
            sql_u2 = 'UPDATE t_online_info_lazada SET refresh_status = 0'
            cur.execute(sql_u1)
            cur.execute(sql_u2)
            cur.execute("commit;")
        self.conn.close()


    def get_products_by_site(self,site,username):
        cur = self.cur
        new_messages = {}
        if site:
            site = site.strip()
            url = self.new_dic[site].split(',')[2]
            shopname = self.new_dic[site.strip()].split(',')[1]
            access_token = self.new_dic[site.strip()].split(',')[0]
            client = lazop.LazopClient(url, self.appkey, self.appSecret)
            request = lazop.LazopRequest('/products/get', 'GET')
            request.add_api_param('filter', 'all')
            request.add_api_param('limit', '1')
            response = client.execute(request, access_token)
            try:
                all_count = response.body['data']['total_products']
                all_count = int(all_count)
            except:
                all_count = 0
            sql3 = 'INSERT INTO t_online_info_lazada_schedule(username,all_count,status) VALUES("%s","%s","%s")' % (username,all_count,'running')
            cur.execute(sql3)
            cur.execute("commit;")
            sum = 0
            while True:
                client = lazop.LazopClient(url, self.appkey, self.appSecret)
                request = lazop.LazopRequest('/products/get', 'GET')
                request.add_api_param('filter', 'all')
                request.add_api_param('offset', str(sum))
                request.add_api_param('limit', '100')
                request.add_api_param('options', '1')
                response = client.execute(request, access_token)
                try:
                    products_info = response.body['data']['products']
                except:
                    sum = sum + 100
                    continue
                count = len(products_info)
                lis = []
                for pro_info in products_info:
                    item_id = pro_info.get('item_id')
                    attributes = pro_info.get('attributes')
                    name = attributes.get('name')
                    brand = attributes.get('brand')
                    warranty_type = attributes.get('warranty_type')
                    dr = re.compile(r'<[^>]+>', re.S)
                    try:
                        short_description = dr.sub('', attributes.get('short_description'))
                    except:
                        short_description = ''
                    model = attributes.get('model')
                    try:
                        description = dr.sub('', attributes.get('description'))
                    except:
                        description = ''
                    primary_category = pro_info.get('primary_category')
                    lis.append(
                        [item_id, shopname, site, name, brand, warranty_type, short_description, model, description,
                         primary_category,datetime.datetime.now(),1,shopname, site, `name`, brand, warranty_type, short_description, model,
                         description, primary_category,datetime.datetime.now(),1])

                    skus = pro_info.get('skus')
                    # print '-----------------长度-------{}'.format(len(skus))
                    lis2 = []
                    for skus_info in skus:
                        if len(skus) == 1:
                            color_family = attributes.get('color_family')
                        else:
                            color_family = skus_info.get('color_family')
                        package_width = skus_info.get('package_width')
                        special_from_time = skus_info.get('special_from_time')
                        Available = skus_info.get('Available')
                        compatible_variation = skus_info.get('_compatible_variation_')
                        package_length = skus_info.get('package_length')
                        fulfillmentStock = skus_info.get('fulfillmentStock')
                        Status = skus_info.get('Status')
                        SkuId = skus_info.get('SkuId')
                        Url = skus_info.get('Url')
                        price = skus_info.get('price')
                        special_price = skus_info.get('special_price')
                        package_weight = skus_info.get('package_weight')
                        nonsellableStock = skus_info.get('nonsellableStock')
                        package_height = skus_info.get('package_height')
                        package_content = skus_info.get('package_content')
                        special_to_time = skus_info.get('special_to_time')
                        ReservedStock = skus_info.get('ReservedStock')
                        SellerSku = skus_info.get('SellerSku')
                        special_from_date = skus_info.get('special_from_date')
                        ShopSku = skus_info.get('ShopSku')
                        special_to_date = skus_info.get('special_to_date')
                        AllocatedStock = skus_info.get('AllocatedStock')
                        Images = str(skus_info.get('Images'))
                        quantity = skus_info.get('quantity')
                        lis2.append([item_id, ShopSku, color_family, package_width, special_from_time, Available,
                                     compatible_variation, package_length, fulfillmentStock, Status, SkuId, Url, price,
                                     special_price, package_weight, nonsellableStock, package_height,
                                     package_content, special_to_time, ReservedStock, SellerSku, special_from_date,
                                     special_to_date, AllocatedStock, Images, quantity, color_family, package_width,
                                     special_from_time, Available,compatible_variation, package_length, fulfillmentStock, Status,
                                     SkuId,Url, price,special_price, package_weight, nonsellableStock, package_height,
                                     package_content, special_to_time, ReservedStock, SellerSku, special_from_date,
                                     special_to_date, AllocatedStock, Images, quantity])
                    sql2 = 'INSERT INTO t_online_info_lazada_detail (item_id,ShopSku,color_family,package_width,special_from_time,Available,compatible_variation,package_length,fulfillmentStock,Status,SkuId,Url,price,special_price,package_weight,nonsellableStock,package_height,package_content,special_to_time,ReservedStock,SellerSku,special_from_date,special_to_date,AllocatedStock,Images,quantity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
                           ' on duplicate key update color_family = %s,package_width=%s,special_from_time=%s,Available=%s,compatible_variation=%s,package_length=%s,fulfillmentStock=%s,Status=%s,SkuId=%s,Url=%s,price=%s,special_price=%s,package_weight=%s,nonsellableStock=%s,package_height=%s,package_content=%s,special_to_time=%s,ReservedStock=%s,SellerSku=%s,special_from_date=%s,special_to_date=%s,AllocatedStock=%s,Images=%s,quantity=%s;'
                    cur.executemany(sql2, lis2)
                    cur.execute("commit;")
                    lis2 = []

                sql = 'INSERT INTO t_online_info_lazada (item_id,shopname,site,`name`,brand,warranty_type,short_description,model,description,primary_category,updatetime,refresh_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update shopname =%s,site=%s,`name`=%s,brand=%s,warranty_type=%s,short_description=%s,model=%s,description=%s,primary_category=%s,updatetime=%s,refresh_status=%s;'
                cur.executemany(sql, lis)
                cur.execute("commit;")
                lis = []

                if count < 100:
                    sum = sum + count
                    print '>>>>>>>>>>>>>>>>>>{}站点抓取结束,总记录为{}条'.format(site, sum)
                    new_messages['success'] = 0
                    sql5 = 'update t_online_info_lazada_schedule set exe_count = "%s",status = "success" WHERE username = "%s"' % (sum,username)
                    cur.execute(sql5)
                    cur.execute("commit;")
                    break
                sum = sum + 100
                sql4 = 'update t_online_info_lazada_schedule set exe_count = "%s" WHERE username = "%s"' % (sum,username)
                cur.execute(sql4)
                cur.execute("commit;")
                print '>>>>>>>>>>>>>>>>>已抓取{}站点{}条产品信息'.format(site, sum)
            sql_u1 = 'UPDATE t_online_info_lazada SET status = 2 WHERE refresh_status = 0 AND shopname = "%s" AND site = "%s"'%(shopname,site) #未刷新的置为异常
            sql_u2 = 'UPDATE t_online_info_lazada SET refresh_status = 0'
            cur.execute(sql_u1)
            cur.execute(sql_u2)
            cur.execute("commit;")
            self.conn.close()

        return new_messages


    def get_products_by_sellersku(self,site,seller_sku_list):
        cur = self.cur
        seller_sku_list = json.dumps(seller_sku_list)
        url = self.new_dic[site.strip()].split(',')[2]
        access_token = self.new_dic[site.strip()].split(',')[0]
        shopname = self.new_dic[site.strip()].split(',')[1]
        client = lazop.LazopClient(url, self.appkey, self.appSecret)
        request = lazop.LazopRequest('/products/get', 'GET')
        request.add_api_param('filter', 'all')
        request.add_api_param('limit', '300')
        request.add_api_param('sku_seller_list', seller_sku_list)
        response = client.execute(request, access_token)
        if response.code == '0':
            try:
                products_info = response.body['data']['products']
            except:
                return 'false'
            count = len(products_info)
            lis = []
            for pro_info in products_info:
                item_id = pro_info.get('item_id')
                attributes = pro_info.get('attributes')
                name = attributes.get('name')
                brand = attributes.get('brand')
                warranty_type = attributes.get('warranty_type')
                dr = re.compile(r'<[^>]+>', re.S)
                try:
                    short_description = dr.sub('', attributes.get('short_description'))
                except:
                    short_description = ''
                model = attributes.get('model')
                try:
                    description = dr.sub('', attributes.get('description'))
                except:
                    description = ''
                primary_category = pro_info.get('primary_category')
                lis.append(
                    [item_id, shopname, site, name, brand, warranty_type, short_description, model, description,
                     primary_category, shopname, site, `name`, brand, warranty_type, short_description, model,
                     description, primary_category])

                skus = pro_info.get('skus')
                # print '-----------------长度-------{}'.format(len(skus))
                lis2 = []
                for skus_info in skus:
                    if len(skus) == 1:
                        color_family = attributes.get('color_family')
                    else:
                        color_family = skus_info.get('color_family')
                    package_width = skus_info.get('package_width')
                    special_from_time = skus_info.get('special_from_time')
                    Available = skus_info.get('Available')
                    compatible_variation = skus_info.get('_compatible_variation_')
                    package_length = skus_info.get('package_length')
                    fulfillmentStock = skus_info.get('fulfillmentStock')
                    Status = skus_info.get('Status')
                    SkuId = skus_info.get('SkuId')
                    Url = skus_info.get('Url')
                    price = skus_info.get('price')
                    special_price = skus_info.get('special_price')
                    package_weight = skus_info.get('package_weight')
                    nonsellableStock = skus_info.get('nonsellableStock')
                    package_height = skus_info.get('package_height')
                    package_content = skus_info.get('package_content')
                    special_to_time = skus_info.get('special_to_time')
                    ReservedStock = skus_info.get('ReservedStock')
                    SellerSku = skus_info.get('SellerSku')
                    special_from_date = skus_info.get('special_from_date')
                    ShopSku = skus_info.get('ShopSku')
                    special_to_date = skus_info.get('special_to_date')
                    AllocatedStock = skus_info.get('AllocatedStock')
                    Images = str(skus_info.get('Images'))
                    quantity = skus_info.get('quantity')
                    lis2.append([item_id, ShopSku, color_family, package_width, special_from_time, Available,
                                 compatible_variation, package_length, fulfillmentStock, Status, SkuId, Url, price,
                                 special_price, package_weight, nonsellableStock, package_height,
                                 package_content, special_to_time, ReservedStock, SellerSku, special_from_date,
                                 special_to_date, AllocatedStock, Images, quantity])
                t_online_info_lazada_detail.objects.filter(item_id=item_id).delete()
                sql2 = 'INSERT INTO t_online_info_lazada_detail (item_id,ShopSku,color_family,package_width,special_from_time,Available,compatible_variation,package_length,fulfillmentStock,Status,SkuId,Url,price,special_price,package_weight,nonsellableStock,package_height,package_content,special_to_time,ReservedStock,SellerSku,special_from_date,special_to_date,AllocatedStock,Images,quantity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
                cur.executemany(sql2, lis2)
                cur.execute("commit;")
                lis2 = []
            sql = 'INSERT INTO t_online_info_lazada (item_id,shopname,site,`name`,brand,warranty_type,short_description,model,description,primary_category) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update shopname =%s,site=%s,`name`=%s,brand=%s,warranty_type=%s,short_description=%s,model=%s,description=%s,primary_category=%s;'
            cur.executemany(sql, lis)
            cur.execute("commit;")
            return 'success'
        else:
            return 'false'
        self.conn.close()


    def remove_product(self,site,seller_sku_list): #暴力
        url = self.new_dic[site.strip()].split(',')[2]
        access_token = self.new_dic[site.strip()].split(',')[0]
        client = lazop.LazopClient(url, self.appkey, self.appSecret)
        request = lazop.LazopRequest('/product/remove')
        request.add_api_param('seller_sku_list', seller_sku_list)
        response = client.execute(request, access_token)
        print(response.body)

    def up_down_shelves(self,site,SellerSku,flag):
        new_messages = {}
        url = self.new_dic[site.strip()].split(',')[2]
        access_token = self.new_dic[site.strip()].split(',')[0]
        client = lazop.LazopClient(url, self.appkey, self.appSecret)
        request = lazop.LazopRequest('/product/update')
        if isinstance(SellerSku,list):
            for sk in SellerSku:
                for k,v in sk.items():
                    xml_one = '<?xml version="1.0" encoding="UTF-8"?><Request><Product><Skus>'
                    for vv in v:
                        xml_one = '%s<Sku><SellerSku>%s</SellerSku><active>%s</active></Sku>'%(xml_one,vv,flag)
                    xml_one = '%s</Skus></Product></Request>'%xml_one
                    request.add_api_param('payload', xml_one)
                    response = client.execute(request, access_token)
                    if response.code == '0':
                        if flag == 'true':
                            status = 'active'
                        else:
                            status = 'inactive'
                        t_online_info_lazada_detail.objects.filter(SellerSku__in=v).update(Status=status)
                    new_messages[k] = str(response.code)
        else:
            xml_one = '<?xml version="1.0" encoding="UTF-8"?><Request><Product><Skus><Sku><SellerSku>%s</SellerSku><active>%s</active></Sku></Skus></Product></Request>'%(SellerSku,flag)
            request.add_api_param('payload',xml_one)
            response = client.execute(request, access_token)
            if response.code == '0':
                if flag == 'true':
                    status = 'active'
                else:
                    status = 'inactive'
                t_online_info_lazada_detail.objects.filter(SellerSku__exact=SellerSku).update(Status=status)
                new_messages['success'] = SellerSku
        return new_messages

if __name__ == '__main__':
    # cur = conn.cursor()
    # sql = 'SELECT ip,appkey,appsecret FROM t_config_online_lazada GROUP BY ip ORDER BY id DESC;'
    # cur.execute(sql)
    # rows = cur.fetchall()
    # for row in rows:
    #     get_products_info(str(row[0]), str(row[1]), str(row[2])).get_products()
    # print '>>>>>>>>>>>>>所有店铺数据同步成功'
    # get_products_info('120.25.65.33', '105965', '5XMwLe8yxWEXHszLUJbuAoV3cQmdcZtn').get_products()
    get_products_info('120.24.16.119', '105963', 'U2PvhDry2IuTXfXp32jG1K4Z9bYCKlsq').get_products()

    # client = lazop.LazopClient('http://120.27.44.178:9193/fancyqube/api.lazada.sg/rest', '105709', 'DHQ0KXJh8swX6xnHt9Q7AcKHvrfgZZzH')
    # request = lazop.LazopRequest('/products/get', 'GET')
    # request.add_api_param('filter', 'all')
    # request.add_api_param('limit', '10')
    # request.add_api_param('sku_seller_list', '["SLZOSME11715"]')
    # response = client.execute(request, '50000401b14rFOpe6kdvhKsVHo1ff69225gQi3lySDjYFTpjxs1TMN2asPd5Qg')
    # print(response.type)
    # print(response.body)
    # get_products_info('120.27.44.178', '105709', 'DHQ0KXJh8swX6xnHt9Q7AcKHvrfgZZzH').get_products_by_sellersku('Thailand',["SLZOSME9111"])
