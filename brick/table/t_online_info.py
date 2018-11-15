# -*- coding: utf-8 -*-
import sys
import os
sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Project.settings')

import datetime, time, socket
from brick.classredis import classlisting, classshopsku, classsku
from brick.table.t_store_configuration_file import t_store_configuration_file
import logging
import json

from brick.wish.api.wishapi import cwishapi
from brick.table.t_config_online_amazon import t_config_online_amazon

from brick.table.t_wish_shopcode_warehouse import t_wish_shopcode_warehouse

from brick.triggerevent.t_event_class import t_event_class
from brick.table.t_online_info_wish import t_online_info_wish
from brick.wish.wish_api_before.token_verification import verb_token
from brick.wish.wishlisting.refresh_fbw_flag import refresh_fbw_flag

class t_online_info():
    def __init__(self,ShopName,cnxn,redis_conn=None):
        self.cnxn =cnxn
        self.redis_conn = redis_conn
        self.PlatformName   = ''#   models.CharField(u'平台',choices=ChoicesPlatformName,max_length=16,blank = True,null = True)
        self.ProductID      = ''#  models.CharField(u'ProductID',max_length=32,blank = True,null = True)
        self.ShopIP         = ''#  models.CharField(u'URL',max_length=32,blank = True,null = True)
        self.ShopName       = ShopName #  models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
        self.Title          = ''#  models.CharField(u'Title',max_length=100,blank = True,null = True)
        self.SKU            = ''# models.CharField(u'商品SKU',max_length=32,blank = True,null = True)
        self.ShopSKU        =  ''# models.CharField(u'店铺SKU',max_length=32,blank = True,null = True)
        self.Price          =  ''# models.CharField(u'价格',max_length=32,blank = True,null = True)
        self.RefreshTime    =  None# models.DateTimeField(u'刷新时间',blank = True,null = True)
        self.Image          =  ''#  models.CharField(u'图片',max_length=200,blank = True,null = True)

        #wish专用
        self.last_ProductID = None
        self.last_ProductName = None
        self.last_ParentSKU = None
        self.last_ImageURL = None
        self.last_DateUploaded = None
        self.last_ReviewState = None
        self.last_OfWishes = None
        self.last_OfSales = None
        self.last_LastUpdated = None
        self.last_ExtraImages = None
        self.last_Description  = None
        self.last_Tags        = None

        warehouse_obj = t_wish_shopcode_warehouse(self.cnxn)
        wResult = warehouse_obj.get_warehouse(self.ShopName)
        if wResult['errorcode'] != 1:  #
            # t_store_configuration_file_obj = t_store_configuration_file(self.cnxn)
            # ssResult = t_store_configuration_file_obj.update_shopStatus('-1', self.ShopName)  # 更新店铺配置文件中的 店铺状态
            # assert ssResult['errorcode'] == 0, ssResult['errortext']
            #
            # t_online_info_wish_obj = t_online_info_wish(self.cnxn)
            # SNResult = t_online_info_wish_obj.UpdateWishSNameByShopName(self.ShopName, '-1')  # shopname
            # assert SNResult['errorcode'] == 1, SNResult['errortext']

            raise Exception(wResult['errortext'])
        self.warehouse = wResult['warehouse']

        auth_info = verb_token(self.ShopName, self.cnxn)
        self.access_token = auth_info['access_token']


    def insert(self,GetReport_datas):
        #cnxn = MySQLdb.connect(DATABASES['HOST'],DATABASES['USER'],DATABASES['PASSWORD'],DATABASES['NAME'] )
        cursor =self.cnxn.cursor()
        ShopIP = socket.gethostbyname(socket.gethostname())
        sql_delete = 'delete from t_online_info where ShopIP =\'%s\' '%ShopIP
        cursor.execute(sql_delete)
        for i, val in enumerate(GetReport_datas):
            if i ==0:
                continue
            GetReport_data = val.split('\t')
            PlatformName = 'Amazon'
            ProductID = GetReport_data[16]

            ShopName = self.ShopName
            Title = GetReport_data[0] #.replace('\'','`')
            ShopSKU = GetReport_data[3].strip()


            SKU = ''

            Price = GetReport_data[4]
            Quantity = GetReport_data[5]
            RefreshTime= datetime.datetime.now()
            Image = ''
            sql_insert = "INSERT INTO t_online_info(ShopIP,ShopName,PlatformName,ProductID,Title,SKU,ShopSKU,Price,Quantity,RefreshTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); "

            #print sql_insert
            cursor.execute(sql_insert,(ShopIP,ShopName,PlatformName,ProductID,Title,SKU,ShopSKU,Price,Quantity,RefreshTime))
        self.cnxn.commit()
        cursor.close()


    def getMax_ProductLastUpdated(self):
        cursor =self.cnxn.cursor()
        sql_Max_ProductLastUpdated = "select max(ProductLastUpdated) from t_order_log where ShopName = %s "

        cursor.execute(sql_Max_ProductLastUpdated,(self.ShopName,))
        Max_ProductLastUpdated_obj = cursor.fetchone()
        if Max_ProductLastUpdated_obj is None  or len(Max_ProductLastUpdated_obj) <=0 or Max_ProductLastUpdated_obj[0] is None:
            Max_ProductLastUpdated = '1970-01-01'
            return Max_ProductLastUpdated
        print 'sql_Max_ProductLastUpdated_obj = %s %s'%(type(Max_ProductLastUpdated_obj),Max_ProductLastUpdated_obj)
        Max_ProductLastUpdated = Max_ProductLastUpdated_obj[0]
        cursor.close()
        if Max_ProductLastUpdated is None:
            Max_ProductLastUpdated = '1970-01-01'
        return Max_ProductLastUpdated


    def getMax_ProductLastUpdated2(self):
        cursor =self.cnxn.cursor()
        sql_Max_ProductLastUpdated = "select max(LastUpdated) from t_online_info where ShopName = %s "

        cursor.execute(sql_Max_ProductLastUpdated,(self.ShopName,))
        Max_ProductLastUpdated_obj = cursor.fetchone()
        if Max_ProductLastUpdated_obj is None  or len(Max_ProductLastUpdated_obj) <=0 or Max_ProductLastUpdated_obj[0] is None:
            Max_ProductLastUpdated = '1970-01-01'
            return Max_ProductLastUpdated
        print 'sql_Max_ProductLastUpdated_obj = %s %s'%(type(Max_ProductLastUpdated_obj),Max_ProductLastUpdated_obj)
        Max_ProductLastUpdated = Max_ProductLastUpdated_obj[0]
        cursor.close()
        if Max_ProductLastUpdated is None:
            Max_ProductLastUpdated = '1970-01-01'
        return Max_ProductLastUpdated


    def setMax_ProductLastUpdated(self,PlatformName,Max_ProductLastUpdated):
        cursor =self.cnxn.cursor()
        sql_Max_ProductLastUpdated = 'select max(ProductLastUpdated) from t_order_log where ShopName = %s '
        cursor.execute(sql_Max_ProductLastUpdated,(self.ShopName,))
        Max_ProductLastUpdated_obj = cursor.fetchone()
        #插入
        if  Max_ProductLastUpdated_obj is None or len(Max_ProductLastUpdated_obj) <=0 or Max_ProductLastUpdated_obj[0] is None :
            sql_Max_ProductLastUpdated = 'insert into t_order_log(ShopName,PlatformName,ProductLastUpdated) values (%s,%s,%s) '
            cursor.execute(sql_Max_ProductLastUpdated,(self.ShopName,PlatformName,Max_ProductLastUpdated))
        else:
            sql_Max_ProductLastUpdated = 'update t_order_log set  ProductLastUpdated =%s where ShopName = %s '
            cursor.execute(sql_Max_ProductLastUpdated,(Max_ProductLastUpdated,self.ShopName))
        print 'setMax_ProductLastUpdated sql =%s'%sql_Max_ProductLastUpdated

        cursor.close()


    def insertWish(self,csv_reader):


        #cnxn = MySQLdb.connect(DATABASES['HOST'],DATABASES['USER'],DATABASES['PASSWORD'],DATABASES['NAME'] )
        cursor =self.cnxn.cursor()
        #ShopIP = socket.gethostbyname(socket.gethostname())
        #sql_delete = 'delete from t_online_info where ShopName =\'%s\' '%self.ShopName.strip()
        #cursor.execute(sql_delete)
        Max_ProductLastUpdated = self.getMax_ProductLastUpdated2()
        index=0
        for row in csv_reader:
            if index < 1:
                index +=1
                continue
            index +=1
            #print(row)
            ProductID    = row[0]
            ProductName  = row[1] #.replace('\'','`')
            OfWishes     = row[3]
            OfSales      = row[4]
            ParentSKU    = row[5]
            VariationID  = row[8]
            ShopSKU      = row[9]
            Price        = row[14]
            Inventory    = row[16]
            Status       = row[18]
            ReviewState  = row[20]

            ImageURL = row[22]
            if ImageURL is not None:
                ImageURL     = row[22].split(r'?')[0]

            LastUpdated  = row[26]
            DateUploaded = row[27]

            Shipping     = row[15]
            Color        = row[11]
            Size         = row[10]
            msrp         = row[12]
            ShippingTime = row[17]
            ExtraImages  = row[23]
            VariationID  = row[8]
            Description  = row[2]
            Tags         = row[24]

            if ProductID is None or ProductID.strip() == '':
                ProductID = self.last_ProductID
            else:
                self.last_ProductID    = ProductID

            if ProductName is None or ProductName.strip() == '':
                ProductName = self.last_ProductName
            else:
                self.last_ProductName    = ProductName

            if OfWishes is None or OfWishes.strip() == '':
                OfWishes = self.last_OfWishes
            else:
                self.last_OfWishes    = OfWishes

            if OfSales is None or OfSales.strip() == '':
                OfSales = self.last_OfSales
            else:
                self.last_OfSales    = OfSales

            if ParentSKU is  None or ParentSKU.strip() == '':
                ParentSKU    = self.last_ParentSKU
            else:
                self.last_ParentSKU    = ParentSKU

            if ReviewState is  None or ReviewState.strip() == '':
                ReviewState    = self.last_ReviewState
            else:
                self.last_ReviewState    = ReviewState

            if ImageURL is  None or ImageURL.strip() == '':
                ImageURL    = self.last_ImageURL
            else:
                self.last_ImageURL    = ImageURL

            if LastUpdated is  None or LastUpdated.strip() == '':
                LastUpdated    = self.last_LastUpdated
            else:
                self.last_LastUpdated    = LastUpdated

            if DateUploaded is  None or DateUploaded.strip() == '':
                DateUploaded    = self.last_DateUploaded
            else:
                self.last_DateUploaded    = DateUploaded

            if ExtraImages is  None or ExtraImages.strip() == '':
                ExtraImages    = self.last_ExtraImages
            else:
                self.last_ExtraImages    = ExtraImages

            if Description is  None or Description.strip() == '':
                Description    = self.last_Description
            else:
                self.last_Description    = Description

            if Tags is  None or Tags.strip() == '':
                Tags    = self.last_Tags
            else:
                self.last_Tags    = Tags


            #print 'ProductID=%s    ParentSKU=%s    VariationID=%s     ShopSKU=%s    Price=%s    Inventory=%s    Status=%s    ImageURL=%s    DateUploaded=%s'%(
                            #ProductID,ParentSKU,VariationID,ShopSKU,Price,Inventory,Status,ImageURL,DateUploaded)

            ShopName = self.ShopName.strip()
            PlatformName = 'Wish'
            Title = ProductName


            SKU = ''

            Quantity = Inventory
            RefreshTime= datetime.datetime.now()

            sql_delete = 'delete from t_online_info where  ProductID= %s and ShopSKU =%s  ; '
            cursor.execute(sql_delete,(ProductID,ShopSKU))

            sql_insert = 'INSERT INTO t_online_info(ShopIP,ShopName,PlatformName,ProductID,Title,SKU,ShopSKU,Price,Quantity,RefreshTime,Image,Status,DateUploaded,ParentSKU,ReviewState,OfWishes,OfSales,LastUpdated,Shipping,Color,Size,msrp,ShippingTime,ExtraImages,VariationID,Description,Tags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ; '

            #print sql_insert
            cursor.execute(sql_insert,(self.ShopIP,ShopName,PlatformName,ProductID,Title,SKU,ShopSKU,Price,Quantity,RefreshTime,ImageURL,Status,DateUploaded,ParentSKU,ReviewState,OfWishes,OfSales,LastUpdated,Shipping,Color,Size,msrp,ShippingTime,ExtraImages,VariationID,Description,Tags))

            sql_update = "update  py_db.b_goodsskulinkshop a, t_online_info b set b.sku = a.sku where a.shopsku =   b.shopsku  and  b.ProductID  = %s and b.ShopSKU = %s "
            cursor.execute(sql_update,(ProductID,ShopSKU))

            sql_update_mainsku = 'update t_online_info set MainSKU  = getMainSKU(SKU) ,MainShopSKU = getMainSKU(shopSKU)  where   ProductID= %s and ShopSKU =%s '
            cursor.execute(sql_update_mainsku,(ProductID,ShopSKU))
        self.cnxn.commit()
        cursor.close()


    def insertWishV2(self,data):
        refreshdict = {}
        refreshdict['ShopName'] = ''
        prolist = []
        #cnxn = MySQLdb.connect(DATABASES['HOST'],DATABASES['USER'],DATABASES['PASSWORD'],DATABASES['NAME'] )
        cursor =self.cnxn.cursor()
        #ShopIP = socket.gethostbyname(socket.gethostname())
        #sql_delete = 'delete from t_online_info where ShopName =\'%s\' '%self.ShopName.strip()
        #cursor.execute(sql_delete)

        classlisting_obj = classlisting.classlisting(self.cnxn,self.redis_conn)

        classshopsku_obj = classshopsku.classshopsku(self.cnxn, self.redis_conn, self.ShopName)

        # classshopname_obj = classshopname.classshopname(db_conn = self.cnxn)
        t_store_configuration_file_obj = t_store_configuration_file(self.cnxn)

        classsku_obj     = classsku.classsku(self.cnxn,self.redis_conn)
        t_event_class_obj = t_event_class()

        cwishapi_obj = cwishapi()
        insert_product = []
        delete_product = []
        update_product = []
        # logger = logging.getLogger('sourceDns.webdns.views')
        for row in data:
            #print(row)
            ProductID    = row['Product']['id']
            # logger.error("ProductID===%s" % (ProductID, ))
            prolist.append(ProductID)

            is_promoted = row['Product'].get('is_promoted', '')
            classlisting_obj.set_is_promoted_listingid(ProductID, is_promoted)

            WishExpress = '%s' % row['Product'].get('wish_express_country_codes', '[]')

            classlisting_obj.set_WishExpress_listingid(ProductID, WishExpress)

            ProductName  = row['Product']['name']
            if '\u' in ProductName:
                try:
                    ProductName = ProductName.decode("unicode_escape")
                except:
                    pass

            OfWishes     = row['Product']['number_saves']
            OfSales      = row['Product']['number_sold']
            ParentSKU    = row['Product']['parent_sku'].replace('&lt;','<').replace('&gt;','>').replace("&#39;","'").replace('\\/', '/')

            if '\u' in ParentSKU:
                try:
                    ParentSKU = ParentSKU.decode("unicode_escape")
                except:
                    pass

            ReviewState  = row['Product']['review_status']  #当前 wish查看状态
            be_sql = "select DISTINCT ReviewState,BeforeReviewState from t_online_info WHERE ProductID=%s LIMIT 1;"
            cursor.execute(be_sql, (ProductID,))
            beforers = cursor.fetchone()
            BeforeReviewState = None  # 上一个wish查看状态
            if beforers and len(beforers) == 2:
                if ReviewState == 'rejected' and beforers[0] == 'rejected' and beforers[1]:
                    BeforeReviewState = beforers[1]
                elif beforers[0]:
                    BeforeReviewState = beforers[0]

            ImageURL     = row['Product']['main_image'].replace('\\', '')
            DateUploaded = time.strftime("%Y-%m-%d",time.strptime(row['Product']['date_uploaded'], "%m-%d-%Y"))  # row['Product']['date_uploaded'] 07-01-2017
            LastUpdated  = time.strftime("%Y-%m-%dT%H:%M:%S",time.strptime(row['Product']['last_updated'], "%m-%d-%YT%H:%M:%S"))  # row['Product']['last_updated']  08-03-2017T10:21:09
            ExtraImages  = row['Product']['extra_images'].replace('\\', '')
            Description  = row['Product']['description']
            if '\u' in Description:
                try:
                    Description = Description.decode("unicode_escape")
                except:
                    pass

            ShopName     = self.ShopName.strip()
            refreshdict['ShopName'] = ShopName
            PlatformName = 'Wish'
            Tags_dict    = row['Product']['tags']
            Title = ProductName

            DepartmentID = t_store_configuration_file_obj.getDepartmentbyshopcode(ShopName)  # 获取该店铺的部门编号
            seller = t_store_configuration_file_obj.getsellerbyshopcode(ShopName)  # 获取该店铺的 销售员 目前没有走redis
            Published = t_store_configuration_file_obj.getPublishedbyshopcode(ShopName)  # 获取该店铺的 刊登人 目前没有走redis
            if seller is None or seller.strip() == '':
                seller = Published

            SKU = ''
            RefreshTime= datetime.datetime.now()
            #print RefreshTime
            Tags =''
            for Tag_dict in Tags_dict:
                if Tags == '':
                    Tags =  Tag_dict['Tag']['name']
                else:
                    Tags = '%s,%s'%(Tags,Tag_dict['Tag']['name'])

            # cursor.execute('Delete from t_online_info where  ProductID= %s ; ',(ProductID,))

            shopskulist = []  # 定义ShopSKU列表

            filterdict = {}# 用于 存放 需要修改的 商品SKU
            vidlist = []
            fbw_flag_list = [] # fbw标记列表
            for variant in row['Product']['variants']:
                VariationID  = variant['Variant']['id'] # 平台唯一ID
                vidlist.append(VariationID)

                shopskutmp = variant['Variant']['sku'].replace('&lt;','<').replace('&gt;','>').replace('&amp;','&').replace("&#39;","'").replace('\\/', '/')
                # logger.error("shopskutmp===%s" % (shopskutmp, ))

                if '\u' in shopskutmp:
                    try:
                        shopskutmp = shopskutmp.decode('unicode-escape')
                    except:
                        pass

                eshopsku = shopskutmp

                # 刷新fbw标记
                fbw_flag = refresh_fbw_flag(product_id=ProductID, shopsku=eshopsku, shopname=ShopName, connection=self.cnxn)
                fbw_flag_list.append(fbw_flag)

                SKU = classshopsku_obj.getSKU(eshopsku) # 商品SKU get

                sku_goodsstatus = None
                if SKU is not None and SKU.strip() != '':
                    sku_goodsstatus = classsku_obj.get_goodsstatus_by_sku(SKU)  # 获取商品SKU的商品状态
                # 下面是简单的转换
                if sku_goodsstatus == u'正常':
                    sku_goodsstatus = '1'
                elif sku_goodsstatus == u'售完下架':
                    sku_goodsstatus = '2'
                elif sku_goodsstatus == u'临时下架':
                    sku_goodsstatus = '3'
                elif sku_goodsstatus == u'停售':
                    sku_goodsstatus = '4'

                #print sku_goodsstatus
                ShopSKUImage = ''
                if variant['Variant'].has_key('main_image'):
                    ShopSKUImage     = variant['Variant']['main_image'].replace('\\','')
                classshopsku_obj.setImage(eshopsku,ShopSKUImage) # 变体图 set

                Price        = variant['Variant']['price']
                classshopsku_obj.setPrice(eshopsku,Price)        # 价格 set

                Inventory    = variant['Variant']['inventory']
                if Inventory == '':
                    Inventory = None
                classshopsku_obj.setQuantity(eshopsku,Inventory) # 库存 set

                Status       = variant['Variant'].get('enabled','')# "enabled": "False",
                if Status.strip() == 'False':
                    Statusssss = 'Disabled'
                elif Status.strip() == 'True': # True
                    Statusssss = 'Enabled'
                else:
                    Statusssss = Status
                classshopsku_obj.setStatus(eshopsku,Statusssss)      # 状态 set

                if Statusssss == 'Enabled':
                    filterdict[SKU] = 0

                Shipping     = variant['Variant']['shipping']
                if Shipping == '':
                    Shipping = None
                classshopsku_obj.setShipping(eshopsku,Shipping)  # 运费 set

                Color        = ''
                if variant['Variant'].has_key('color'):
                    Color     = variant['Variant']['color'].replace('&amp;', '&')  #  &
                classshopsku_obj.setColor(eshopsku,Color)        # 颜色 set

                Size         = ''
                if variant['Variant'].has_key('size'):
                    Size     = variant['Variant']['size'][:30]
                classshopsku_obj.setSize(eshopsku,Size)          # 尺寸 set

                msrp         = variant['Variant']['msrp']
                classshopsku_obj.setmsrp(eshopsku,msrp)           # 标签价 set

                ShippingTime = variant['Variant']['shipping_time']
                classshopsku_obj.setshippingtime(eshopsku,ShippingTime) # 运输时间 set
                # Quantity = Inventory

                cursor.execute("select count(VariationID) from t_online_info WHERE ProductID=%s and VariationID=%s;",
                               (ProductID,VariationID,))
                somecount = cursor.fetchone()
                if somecount[0] > 0:
                    sql_update = "update t_online_info set Title=%s,Price=%s,Quantity=%s,RefreshTime=%s,Image=%s,Status=%s," \
                                 "ReviewState=%s,OfWishes=%s,OfSales=%s,LastUpdated=%s,Shipping=%s,Color=%s,`Size`=%s,msrp=%s," \
                                 "ShippingTime=%s,ExtraImages=%s,Description=%s,Tags=%s,ShopSKUImage=%s,is_promoted=%s," \
                                 "WishExpress=%s,seller=%s,Published=%s,SKU=%s,MainSKU=%s,BeforeReviewState=%s,ShopSKU=%s" \
                                 " WHERE ProductID=%s and VariationID=%s;"

                    cursor.execute(sql_update,(Title,Price,Inventory,RefreshTime,ImageURL,Statusssss,
                                               ReviewState,OfWishes,OfSales,LastUpdated,Shipping,Color,Size,msrp,
                                               ShippingTime,ExtraImages,Description,Tags,ShopSKUImage,is_promoted,
                                               WishExpress,seller,Published,SKU,
                                               classsku_obj.get_bemainsku_by_sku(SKU),BeforeReviewState,shopskutmp,
                                               ProductID,VariationID))
                    # if not SKU:
                    update_product.append(ProductID)
                else:
                    sql_insert = 'INSERT INTO t_online_info(ShopIP,ShopName,PlatformName,ProductID,Title,' \
                                 'SKU,ShopSKU,Price,Quantity,RefreshTime,Image,Status,DateUploaded,ParentSKU,' \
                                 'ReviewState,OfWishes,OfSales,LastUpdated,Shipping,Color,`Size`,msrp,' \
                                 'ShippingTime,ExtraImages,VariationID,Description,Tags,' \
                                 'MainSKU,ShopSKUImage,is_promoted,WishExpress,DepartmentID,seller,Published,' \
                                 'GoodsStatus,filtervalue,APIState,BeforeReviewState)' \
                                 ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,' \
                                 '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ; '
                    cursor.execute(sql_insert,(self.ShopIP,ShopName,PlatformName,ProductID,Title,SKU,
                                               shopskutmp,Price,Inventory,RefreshTime,ImageURL,Statusssss,DateUploaded,
                                               ParentSKU,ReviewState,OfWishes,OfSales,LastUpdated,Shipping,Color,
                                               Size,msrp,ShippingTime,ExtraImages,VariationID,Description,Tags,
                                               classsku_obj.get_bemainsku_by_sku(SKU),ShopSKUImage,is_promoted,WishExpress,
                                               DepartmentID,seller,Published,sku_goodsstatus,1,'nothing',BeforeReviewState))
                    insert_product.append(ProductID)
                # sql_update = "update  py_db.b_goodsskulinkshop a, t_online_info b set b.sku = a.sku ,b.MainSKU  = getMainSKU(a.SKU) ,b.MainShopSKU = getMainSKU(b.shopSKU) where a.shopsku =  b.shopsku and  b.ProductID  = %s and b.ShopSKU = %s "
                # cursor.execute(sql_update,(ProductID,ShopSKU))

                shopskulist.append(shopskutmp)
                # logger.error("shopskulist===%s" % (shopskulist, ))
                # logger.error("join===%s" % ('|'.join(shopskulist), ))
                #sql_update_mainsku = 'update t_online_info set MainSKU  = getMainSKU(SKU) ,MainShopSKU = getMainSKU(shopSKU)  where   ProductID= %s and ShopSKU =%s '
                #cursor.execute(sql_update_mainsku,(ProductID,ShopSKU))

            # 获取该产品的海外仓运费和库存

            for we in eval(WishExpress):  # 是属于海外仓的
                # raise Exception(self.warehouse)
                if self.warehouse.has_key(we) and we in ['DE', 'GB', 'US']:
                    warehouseid = self.warehouse[we]
                    vgoodsinfos = cwishapi_obj.warehouse_vgoodsinfo(self.access_token, ProductID, warehouseid)
                    # assert vgoodsinfos['errorcode'] == 1, vgoodsinfos['errortext']
                    if vgoodsinfos['errorcode'] == 1:
                        for vgoods in vgoodsinfos['data']:
                            wvid = vgoods['Variant']['id']

                            shopsku = vgoods['Variant']['sku'].replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace("&#39;", "'").replace('\\/', '/')
                            if '\u' in shopsku:
                                try:
                                    shopsku = shopsku.decode('unicode-escape')
                                except:
                                    pass

                            wshipping = vgoods['Variant']['shipping']   # DEExpressShipping
                            if wshipping == '':
                                wshipping = None
                            ws = getattr(classshopsku_obj, "setWish%sShipping" % we)
                            ws(shopsku, wshipping)
                            # eval("classshopsku_obj.setWish%sShipping" % we)(shopsku, wshipping)

                            winventory = vgoods['Variant']['inventory']   # DEExpressInventory
                            if winventory == '':
                                winventory = None
                            wi = getattr(classshopsku_obj, "setWish%sQuantity" % we)
                            wi(shopsku, winventory)
                            # eval("classshopsku_obj.setWish%sQuantity" % we)(shopsku, winventory)

                            vsql = "update t_online_info set " + we + "ExpressShipping=%s," + we + \
                                   "ExpressInventory=%s WHERE ProductID=%s and VariationID=%s;"

                            cursor.execute(vsql, (wshipping, winventory, ProductID, wvid))

            if vidlist:  # 删除多余的变体信息
                del_param_list = []
                old_shopsku_list = classlisting_obj.getShopSKUList(ProductID)
                if old_shopsku_list:
                    for del_shopsku in old_shopsku_list:
                        if del_shopsku not in shopskulist:
                            del_param_list.append([ProductID, del_shopsku])
                            delete_product.append(ProductID)
                            # del_sku = classshopsku_obj.getSKU(del_shopsku)
                            # if del_sku:
                            #     delete_sku.append(del_sku)

                cursor.executemany("delete from t_online_info WHERE ProductID=%s and ShopSKU=%s ;", del_param_list)

            classlisting_obj.setShopSKUList(ProductID, '|'.join(shopskulist))  # ProductID ShopSKUList
            # for k,v in filterdict.items():
            #     cursor.execute("update t_online_info set filtervalue = 0 WHERE ProductID=%s and SKU=%s;",(ProductID,k,))

            if fbw_flag_list and 'True' in fbw_flag_list:
                cursor.execute("update t_online_info set FBW_Flag = 'True' WHERE ProductID=%s ;", (ProductID, ))
            elif 'False' in fbw_flag_list:
                cursor.execute("update t_online_info set FBW_Flag = 'False' WHERE ProductID=%s ;", (ProductID,))

        self.cnxn.commit()

        for inproduct in set(insert_product):
            iResult = t_event_class_obj.t_online_info_insert_trigger(inproduct)

        for delproduct in set(delete_product):
            del_Result = t_event_class_obj.t_online_info_delete_trigger(delproduct)

        for updproduct in set(update_product):
            upd_Result = t_event_class_obj.t_online_info_update_trigger(updproduct)

        cursor.close()
        refreshdict['ProductID'] = prolist
        return refreshdict

    def getshopproductdata(self, productid):
        keylist = ['PlatformName','ProductID','ShopIP','ShopName','Title','SKU',
                   'ShopSKU','Price','Quantity','RefreshTime','Image',
                   'Status','DateUploaded','ParentSKU','ReviewState','OfWishes','OfSales','LastUpdated',
                   'MainSKU','BeforeReviewState','is_promoted','WishExpress','countID','FBW_Flag']

        mycur = self.cnxn.cursor()
        sql = "select PlatformName,ProductID,ShopIP,ShopName,Title,group_concat(SKU separator ',') as SKU," \
              "group_concat(ShopSKU separator ',') as ShopSKU,Price,Quantity,MAX(RefreshTime),Image," \
              "if('Enabled' in (SELECT `Status` from t_online_info a WHERE a.ProductID =%s ),'Enabled','Disabled') " \
              "as `Status`," \
              "DateUploaded,ParentSKU,ReviewState,OfWishes,OfSales,LastUpdated," \
              "group_concat(DISTINCT MainSKU separator ',') as MainSKU," \
              "BeforeReviewState,is_promoted,WishExpress,COUNT(ProductID),FBW_Flag " \
              "from t_online_info WHERE ShopName=%s and ProductID=%s GROUP BY ProductID ;"

        mycur.execute(sql, (productid, self.ShopName, productid))
        objs = mycur.fetchall()
        mycur.close()

        datalist = []
        for obj in objs:
            datadict = {}
            for i in range(len(obj)):
                datadict[keylist[i]] = obj[i]
            datalist.append(datadict)

        return datalist

    def update_status_by_productid(self,status,productid):
        try:
            updcur = self.cnxn.cursor()
            updcur.execute('update t_online_info set Status = %s where ProductID = %s ;',(status,productid,))
            updcur.execute('commit;')
            updcur.close()
            return {'errorcode': 0, 'errortext': ''}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}

    def update_status_by_shopsku(self,status,shopsku):
        try:
            updcur = self.cnxn.cursor()
            updcur.execute('update t_online_info set Status = %s where ShopSKU = %s ;',(status,shopsku,))
            updcur.execute('commit;')
            updcur.close()
            return {'errorcode': 0, 'errortext': ''}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}

    def get_all_shopsku_infor_by_productid(self,productid):
        getcur = self.cnxn.cursor()
        getcur.execute("select SKU,ShopSKU,Quantity,Price,Status,Shipping,ShopName,ShopSKUImage,Color,`Size`,msrp,ShippingTime "
                       "from t_online_info WHERE ProductID = %s ;",(productid,))
        objs = getcur.fetchall()
        getcur.close()
        return objs

    def update_status_by_sku(self,status,sku):
        updcur = self.cnxn.cursor()
        updcur.execute('update t_online_info set Status = %s where SKU = %s ;',(status,sku,))
        updcur.execute('commit;')
        updcur.close()


    def get_maxpirce(self,productid):
        cursor = self.cnxn.cursor()
        cursor.execute("select ParentSKU,MAX(Price),MAX(Shipping) from t_online_info WHERE ProductID=%s and Status='Enabled';",(productid,))
        priceinfo = cursor.fetchone()
        cursor.close()
        return priceinfo

    def get_listingid_by_shopname_shopsku(self,shopsku):
        try:
            cursor = self.cnxn.cursor()
            cursor.execute("select ProductID,ParentSKU from t_online_info WHERE ShopName=%s and ShopSKU=%s;",(self.ShopName,shopsku,))
            proinfo = cursor.fetchone()
            cursor.close()
            if proinfo:
                return {'errorcode': 0, 'errortext': '','productid':proinfo[0],'parentsku':proinfo[1]}
            else:
                return {'errorcode': 1, 'errortext': u'该店铺名和该店铺SKU没有找到对应的ProductID'}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}


    def get_goodsstatus_by_productid(self,productid):
        cursor = self.cnxn.cursor()
        cursor.execute("select DISTINCT GoodsStatus from t_online_info WHERE ProductID=%s;",(productid,))
        infos = cursor.fetchall()
        cursor.close()
        infolist = []
        for info in infos:
            infolist.append(info[0])
        return infolist

    def get_shopskustatus_by_productid(self,productid):
        cursor = self.cnxn.cursor()
        cursor.execute("select DISTINCT Status from t_online_info WHERE ProductID=%s;",(productid,))
        infos = cursor.fetchall()
        cursor.close()
        infolist = []
        for info in infos:
            infolist.append(info[0])
        return infolist

    def get_binding_by_productid(self,productid):
        cursor = self.cnxn.cursor()
        cursor.execute("select COUNT(id) from t_online_info WHERE ProductID=%s AND SKU is NULL;",(productid,))
        count = cursor.fetchone()
        cursor.close()
        return count[0]


    def getonlinestatusbyproductid(self,productid):
        try:
            mycur = self.cnxn.cursor()
            mycur.execute("select if('Enabled' in (SELECT `Status` from t_online_info a WHERE a.ProductID = %s ),'Enabled','Disabled') as `Status`,"
                          "ReviewState from t_online_info WHERE ShopName=%s and ProductID=%s GROUP BY ProductID ;",(productid,self.ShopName,productid,))
            objs = mycur.fetchone()
            mycur.close()
            if objs:
                return {'errorcode': 0, 'errortext': '','Status':objs[0],'ReviewState':objs[1]}
            else:
                return {'errorcode': 1, 'errortext': u'该店铺名和ProductID没有找到数据'}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}







