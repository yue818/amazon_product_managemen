#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time
# import socket
# from brick.classredis import classlisting, classshopsku, classsku
from brick.table.t_store_configuration_file import t_store_configuration_file
from brick.table.t_templet_joom_upload_result import t_templet_joom_upload_result
from brick.table.t_online_info_joom import t_online_info_joom
from brick.table.t_distribution_product_to_store_result import t_distribution_product_to_store_result


class t_online_info_joom_detail():

    def __init__(self, ShopName, cnxn, ShopIP=None, redis_conn=None):
        self.cnxn = cnxn
        self.redis_conn = redis_conn
        self.PlatformName = ''  # models.CharField(u'平台',choices=ChoicesPlatformName,max_length=16,blank = True,null = True)
        self.ProductID = ''  # models.CharField(u'ProductID',max_length=32,blank = True,null = True)
        self.ShopIP = ShopIP  # models.CharField(u'URL',max_length=32,blank = True,null = True)
        self.ShopName = ShopName  # models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
        self.Title = ''  # models.CharField(u'Title',max_length=100,blank = True,null = True)
        self.SKU = ''  # models.CharField(u'商品SKU',max_length=32,blank = True,null = True)
        self.ShopSKU = ''  # models.CharField(u'店铺SKU',max_length=32,blank = True,null = True)
        self.Price = ''  # models.CharField(u'价格',max_length=32,blank = True,null = True)
        self.RefreshTime = None  # models.DateTimeField(u'刷新时间',blank = True,null = True)
        self.Image = ''  # models.CharField(u'图片',max_length=200,blank = True,null = True)

    def insertJoomV2(self, data):
        refreshdict = {}
        refreshdict['ShopName'] = ''
        prolist = []
        cursor = self.cnxn.cursor()

        # classlisting_obj = classlisting(db_conn=self.cnxn, redis_conn=self.redis_conn)
        # classshopsku_obj = classshopsku(db_conn=self.cnxn, redis_conn=self.redis_conn)
        # classsku_obj = classsku(db_cnxn=self.cnxn, redis_cnxn=self.redis_conn)
        t_store_configuration_file_obj = t_store_configuration_file(self.cnxn)

        for row in data:
            ProductID = row['Product'].get('id')
            prolist.append(ProductID)

            is_promoted = row['Product'].get('is_promoted', '')
            # classlisting_obj.set_is_promoted_listingid(ProductID, is_promoted)

            JoomExpress = '%s' % row['Product'].get('joom_express_country_codes', '[]')
            # classlisting_obj.set_JoomExpress_listingid(ProductID, JoomExpress)

            ProductName = row['Product'].get('name')
            OfJoomes = row['Product'].get('number_saves')
            OfSales = row['Product'].get('number_sold')
            ParentSKU = row['Product'].get('parent_sku', '').replace('&lt;', '<').replace('&gt;', '>')
            ReviewState = row['Product'].get('review_status')
            ImageURL = row['Product'].get('main_image', '').split(r'?')[0].replace('\\', '')
            DateUploaded = time.strftime("%Y-%m-%d", time.strptime(row['Product'].get('date_uploaded'), "%Y-%m-%dT%H:%M:%SZ"))  # row['Product']['date_uploaded'] 2017-11-11T06:41:33Z
            if row['Product'].get('last_updated'):
                last_update_time = row['Product'].get('last_updated')
            else:
                last_update_time = row['Product'].get('date_uploaded')
            LastUpdated = time.strftime("%Y-%m-%dT%H:%M:%S", time.strptime(last_update_time, "%Y-%m-%dT%H:%M:%SZ"))  # row['Product']['last_updated']  2017-11-11T06:41:33Z
            ExtraImages = row['Product'].get('extra_images', '').replace('\\', '')
            Description = row['Product'].get('description')
            ShopName = self.ShopName.strip()
            refreshdict['ShopName'] = ShopName
            PlatformName = 'Joom'
            Tags_dict = row['Product'].get('tags', '')
            Title = ProductName

            DepartmentID, seller, Published = t_store_configuration_file_obj.getinfobyshopcode(ShopName)  # 获取该店铺的部门 编号 销售员 刊登人
            if seller is None or seller.strip() == '':
                seller = Published

            SKU = ''
            RefreshTime = datetime.datetime.now()
            Tags = ''
            for Tag_dict in Tags_dict:
                if Tags == '':
                    Tags = Tag_dict['Tag'].get('name')
                else:
                    Tags = '%s,%s' % (Tags, Tag_dict['Tag'].get('name'))

            shopskulist = []  # 定义ShopSKU列表

            filterdict = {}  # 用于 存放 需要修改的 商品SKU
            for variant in row['Product'].get('variants', [{'Variant': None}]):
                VariationID = variant['Variant'].get('id')
                ShopSKU = variant['Variant'].get('sku').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                # SKU = classshopsku_obj.getSKU(ShopSKU)  # 商品SKU get

                sku_goodsstatus = None
                # if SKU is not None and SKU.strip() != '':
                #     sku_goodsstatus = classsku_obj.get_goodsstatus_by_sku(SKU)  # 获取商品SKU的商品状态
                # # 下面是简单的转换
                # if sku_goodsstatus == u'正常':
                #     sku_goodsstatus = '1'
                # elif sku_goodsstatus == u'售完下架':
                #     sku_goodsstatus = '2'
                # elif sku_goodsstatus == u'临时下架':
                #     sku_goodsstatus = '3'
                # elif sku_goodsstatus == u'停售':
                #     sku_goodsstatus = '4'

                ShopSKUImage = ''
                if 'main_image' in variant['Variant'].keys():
                    ShopSKUImage = variant['Variant'].get('main_image').replace('\\', '')
                # classshopsku_obj.setImage(ShopSKU, ShopSKUImage)  # 变体图 set

                Price = variant['Variant'].get('price')
                # classshopsku_obj.setPrice(ShopSKU, Price)        # 价格 set

                Inventory = variant['Variant'].get('inventory')
                # classshopsku_obj.setQuantity(ShopSKU, Inventory)  # 库存 set

                Status = variant['Variant'].get('enabled', '')  # "enabled": "False",
                Statusssss = Status
                # classshopsku_obj.setStatus(ShopSKU, Statusssss)      # 状态 set

                if Statusssss == 'True':
                    filterdict[ShopSKU] = 0

                Shipping = variant['Variant'].get('shipping')
                # classshopsku_obj.setShipping(ShopSKU, Shipping)  # 运费 set

                Color = ''
                if 'color' in variant['Variant'].keys():
                    Color = variant['Variant'].get('color')
                # classshopsku_obj.setColor(ShopSKU, Color)        # 颜色 set

                Size = ''
                if 'size' in variant['Variant'].keys():
                    Size = variant['Variant'].get('size')[:30]
                # classshopsku_obj.setSize(ShopSKU, Size)          # 尺寸 set

                msrp = variant['Variant'].get('msrp')
                # classshopsku_obj.setmsrp(ShopSKU, msrp)           # 标签价 set

                ShippingTime = variant['Variant'].get('shipping_time')
                # classshopsku_obj.setshippingtime(ShopSKU, ShippingTime)  # 运输时间 set
                # Quantity = Inventory

                cursor.execute("SELECT COUNT(ProductID) FROM t_online_info_joom_detail WHERE ProductID=%s AND ShopSKU=%s;", (ProductID, ShopSKU,))
                somecount = cursor.fetchone()
                if somecount[0] > 0:
                    sql_update = "UPDATE t_online_info_joom_detail SET Title=%s,Price=%s,Quantity=%s,RefreshTime=%s,Image=%s,Status=%s," \
                                 "ReviewState=%s,OfJoomes=%s,OfSales=%s,LastUpdated=%s,Shipping=%s,Color=%s,`Size`=%s,msrp=%s," \
                                 "ShippingTime=%s,ExtraImages=%s,Description=%s,Tags=%s,ShopSKUImage=%s,is_promoted=%s," \
                                 "JoomExpress=%s,seller=%s,Published=%s,GoodsStatus=%s WHERE ProductID=%s AND ShopSKU=%s;"
                    cursor.execute(sql_update, (Title, Price, Inventory, RefreshTime, ImageURL, Statusssss,
                                   ReviewState, OfJoomes, OfSales, LastUpdated, Shipping, Color, Size, msrp,
                                   ShippingTime, ExtraImages, Description, Tags, ShopSKUImage, is_promoted,
                                   JoomExpress, seller, Published, sku_goodsstatus, ProductID, ShopSKU))
                else:
                    sql_insert = 'INSERT INTO t_online_info_joom_detail (ShopIP,ShopName,PlatformName,ProductID,Title,' \
                                 'SKU,ShopSKU,Price,Quantity,RefreshTime,Image,Status,DateUploaded,ParentSKU,' \
                                 'ReviewState,OfJoomes,OfSales,LastUpdated,Shipping,Color,`Size`,msrp,' \
                                 'ShippingTime,ExtraImages,VariationID,Description,Tags,' \
                                 'MainSKU,ShopSKUImage,is_promoted,JoomExpress,DepartmentID,seller,Published,' \
                                 'GoodsStatus,filtervalue,APIState)' \
                                 ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,' \
                                 '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
                    cursor.execute(sql_insert, (self.ShopIP, ShopName, PlatformName, ProductID, Title, SKU,
                                                ShopSKU, Price, Inventory, RefreshTime, ImageURL, Statusssss, DateUploaded,
                                                ParentSKU, ReviewState, OfJoomes, OfSales, LastUpdated, Shipping, Color,
                                                Size, msrp, ShippingTime, ExtraImages, VariationID, Description, Tags,
                                                '', ShopSKUImage, is_promoted, JoomExpress, DepartmentID, seller,
                                                Published, sku_goodsstatus, 1, 'nothing'))
                cursor.execute('commit;')

                shopskulist.append(ShopSKU)
            # classlisting_obj.setShopSKUList(ProductID, '|'.join(shopskulist))  # ProductID ShopSKUList

            for k, v in filterdict.items():
                sql = "UPDATE t_online_info_joom_detail SET filtervalue = 0 WHERE ProductID=%s AND ShopSKU=%s;"
                cursor.execute(sql, (ProductID, k))
                cursor.execute('commit;')

            params = dict()
            params['ShopName'] = ShopName
            params['ShopIP'] = self.ShopIP
            params['ProductID'] = ProductID
            params['Seller'] = seller
            params['dbcnxn'] = self.cnxn
            self.refresh_joom_listing_run(params)

        cursor.execute('commit;')
        cursor.close()
        refreshdict['ProductID'] = prolist
        return refreshdict

    def refresh_joom_listing_run(self, params):
        shopalldata = None

        infodata = self.getshopproductdata(params['ProductID'])
        if infodata['code'] == 0:
            shopalldata = infodata['mydata']

        if shopalldata is not None:
            # t_report_orders1days_objs = t_report_orders1days(params['dbcnxn'])
            # t_store_configuration_file_obj = t_store_configuration_file(params['dbcnxn'])
            # classlisting_obj = classlisting(params['dbcnxn'])
            # classmainsku_obj = classmainsku(params['dbcnxn'])
            t_templet_joom_upload_result_obj = t_templet_joom_upload_result(params['dbcnxn'])
            # classshopsku_obj = classshopsku(db_conn=params['dbcnxn'], redis_conn=self.redis_conn)
            t_online_info_joom_obj = t_online_info_joom(params['dbcnxn'])
            t_distribution_product_to_store_result_obj = t_distribution_product_to_store_result(params['dbcnxn'])

            for obj in shopalldata:
                datedict = {}
                datedict['ProductID'] = obj[1]
                datedict['ShopName'] = obj[3]
                datedict['Title'] = obj[4]
                datedict['SKU'] = obj[5]
                datedict['ShopSKU'] = obj[6]
                datedict['Price'] = obj[7]
                datedict['RefreshTime'] = obj[9]

                # yyyymmdd = obj[9].strftime('%Y%m%d')

                # TODO 订单同步做完之后才有
                # datedict['SoldTheDay']    = t_report_orders1days_objs.getSoldTheDay(obj[1],yyyymmdd)
                # datedict['SoldYesterday'] = t_report_orders1days_objs.getSoldYesterday(obj[1],yyyymmdd)
                # datedict['Orders7Days']   = t_report_orders1days_objs.getOrders7Days(obj[1],yyyymmdd)
                # datedict['SoldXXX']       = int(datedict['SoldTheDay']) - int(datedict['SoldYesterday'])
                datedict['SoldTheDay'] = None
                datedict['SoldYesterday'] = None
                datedict['Orders7Days'] = None
                datedict['SoldXXX'] = None

                # classlisting_obj.set_order7days_listingid(datedict['ProductID'],datedict['Orders7Days'])

                datedict['DateOfOrder'] = None
                datedict['Image'] = obj[10]
                datedict['Status'] = obj[11]
                datedict['ReviewState'] = obj[14]
                datedict['DateUploaded'] = obj[12]
                datedict['LastUpdated'] = obj[17]
                datedict['OfSales'] = obj[16]
                datedict['ParentSKU'] = obj[13]

                datedict['is_promoted'] = obj[-3]
                datedict['JoomExpress'] = obj[-2]

                datedict['Seller'] = params['Seller']

                datedict['MainSKU'] = obj[18]

                datedict['TortInfo'] = 'N'
                # mainskulist = classlisting_obj.getmainsku(obj[1])
                # if mainskulist:
                #     tortlist = []
                #     for mainsku in mainskulist:
                #         tortsite = classmainsku_obj.get_tort_by_mainsku(mainsku)
                #         if tortsite is not None:
                #             tortlist = tortlist + tortsite
                #     if tortlist:
                #         if 'Wish' in tortlist:
                #             datedict['TortInfo'] = 'WY'
                #         else :
                #             datedict['TortInfo'] = 'Y'

                datedict['DataSources'] = "NORMAL"
                if t_templet_joom_upload_result_obj.get_count_num(obj[13]) >= 1:
                    datedict['DataSources'] = "UPLOAD"
                else:
                    if t_distribution_product_to_store_result_obj.get_count_num(obj[13], params['ShopName']) >= 1:
                        datedict['DataSources'] = "UPLOAD"

                datedict['OperationState'] = 'No'
                if obj[11] == 'Disabled':
                    datedict['OperationState'] = 'Yes'
                datedict['Published'] = obj[-1]
                # if obj[6] is not None and obj[6].strip() != '':
                #     datedict['Published'] = classshopsku_obj.getPublished((obj[6].split(',')[0]).strip())

                datedict['market_time'] = None

                refreshresult = t_online_info_joom_obj.refresh_joom_data(datedict)
                print 'refreshresult %s' % refreshresult

    def getshopproductdata(self, productid):
        result = {}
        try:
            mycur = self.cnxn.cursor()
            sql = "SELECT PlatformName,ProductID,ShopIP,ShopName,Title,group_concat(SKU separator ',') AS SKU, " \
                  "group_concat(ShopSKU separator ',') AS ShopSKU,Price,Quantity,RefreshTime,Image, " \
                  "IF('True' IN (SELECT `Status` FROM t_online_info_joom_detail a WHERE a.ProductID = '%s' ),'True','False') AS `Status`, " \
                  "DateUploaded,ParentSKU,ReviewState,OfJoomes,OfSales,LastUpdated,group_concat(MainSKU separator ',') as MainSKU,is_promoted,JoomExpress,Published " \
                  "FROM t_online_info_joom_detail WHERE ShopName='%s' AND ProductID='%s' GROUP BY ProductID;"
            full_sql = sql % (productid, self.ShopName, productid)
            mycur.execute(full_sql)
            objs = mycur.fetchall()
            mycur.close()
            result['code'] = 0
            result['error'] = ''
            result['mydata'] = objs
        except Exception, ex:
            result['code'] = 1
            result['error'] = '%s:%s' % (Exception, ex)
            result['mydata'] = []
        return result
