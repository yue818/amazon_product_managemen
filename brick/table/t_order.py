# -*- coding: utf-8 -*-

import datetime, time
from brick.table.t_chart_wish_refund_log import t_chart_wish_refund_log
from brick.wish.wish_api_before.token_verification import verb_token
from brick.wish.api.wishapi import cwishapi

from brick.table.t_wish_information_of_order_fine import t_wish_information_of_order_fine as order_fine

from brick.table.t_order_of_wish_fbw_fee import t_order_of_wish_fbw_fee

def strtimeaddseconds(srctime,seconds):
    b= time.strptime(srctime,'%Y-%m-%dT%H:%M:%S')
    c = time.mktime(b) + seconds
    x = time.localtime(c)
    d=time.strftime('%Y-%m-%dT%H:%M:%S',x)
    #print d
    return d

class t_order():
    def __init__(self,ShopName,cnxn):
        self.cnxn =cnxn
        self.ShopName       = ShopName #  models.CharField(u'店铺名称',max_length=32,blank = True,null = True)

        auth_info = verb_token(self.ShopName, self.cnxn)
        self.access_token = auth_info.get('access_token')

    def getMax_OrderLastUpdated(self):
        cursor =self.cnxn.cursor()
        sql_Max_OrderLastUpdated = 'select max(OrderLastUpdated) from t_order_log where ShopName = %s '

        cursor.execute(sql_Max_OrderLastUpdated,(self.ShopName,))
        Max_OrderLastUpdated_obj = cursor.fetchone()
        if Max_OrderLastUpdated_obj is None  or len(Max_OrderLastUpdated_obj) <=0 or Max_OrderLastUpdated_obj[0] is None:
            Max_OrderLastUpdated = '1970-01-01'
            return Max_OrderLastUpdated
        print 'sql_Max_OrderLastUpdated_obj = %s %s'%(type(Max_OrderLastUpdated_obj),Max_OrderLastUpdated_obj)
        Max_OrderLastUpdated = Max_OrderLastUpdated_obj[0]
        cursor.close()
        if Max_OrderLastUpdated is None:
            Max_OrderLastUpdated = '1970-01-01'
        return Max_OrderLastUpdated

    def getMax_OrderLastUpdated2(self):
        cursor =self.cnxn.cursor()
        sql_Max_OrderLastUpdated = 'select max(lastupdated) from t_order where ShopName = %s '

        cursor.execute(sql_Max_OrderLastUpdated,(self.ShopName,))
        Max_OrderLastUpdated_obj = cursor.fetchone()
        if Max_OrderLastUpdated_obj is None  or len(Max_OrderLastUpdated_obj) <=0 or Max_OrderLastUpdated_obj[0] is None:
            utcnowtemp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            Max_OrderLastUpdated = strtimeaddseconds(utcnowtemp,-32*86400)
            return Max_OrderLastUpdated
        print 'sql_Max_OrderLastUpdated_obj = %s %s'%(type(Max_OrderLastUpdated_obj),Max_OrderLastUpdated_obj)
        Max_OrderLastUpdated = Max_OrderLastUpdated_obj[0]
        cursor.close()

        return Max_OrderLastUpdated

    def setMax_OrderLastUpdated(self,PlatformName,Max_OrderLastUpdated):
        cursor =self.cnxn.cursor()
        sql_Max_OrderLastUpdated = 'select max(OrderLastUpdated) from t_order_log where ShopName = %s '
        cursor.execute(sql_Max_OrderLastUpdated,(self.ShopName,))
        Max_OrderLastUpdated_obj = cursor.fetchone()
        #插入
        if  Max_OrderLastUpdated_obj is None or len(Max_OrderLastUpdated_obj) <=0 or Max_OrderLastUpdated_obj[0] is None :
            sql_Max_OrderLastUpdated = 'insert into t_order_log(ShopName,PlatformName,OrderLastUpdated) values (%s,%s,%s)'
            cursor.execute(sql_Max_OrderLastUpdated,(self.ShopName,PlatformName,Max_OrderLastUpdated))
        else:
            sql_Max_OrderLastUpdated = 'update t_order_log set  OrderLastUpdated =%s where ShopName = %s '
            cursor.execute(sql_Max_OrderLastUpdated,(Max_OrderLastUpdated,self.ShopName))
        print 'setMax_OrderLastUpdated sql =%s'%sql_Max_OrderLastUpdated

        cursor.close()

    def insertWish(self,csv_reader):
        #cnxn = MySQLdb.connect(DATABASES['HOST'],DATABASES['USER'],DATABASES['PASSWORD'],DATABASES['NAME'] )
        cursor =self.cnxn.cursor()
        #ShopIP = socket.gethostbyname(socket.gethostname())

        Max_OrderLastUpdated = self.getMax_OrderLastUpdated2()

        index=0
        for row in csv_reader:
            if index < 1:
                index +=1
                continue
            index +=1
            #print(row)
            PlatformName = 'Wish'
            ShopName = self.ShopName
            OrderDate          = row[0]
            OrderId            = row[1]
            OrderState         = row[3]

            ShopSKU            = row[4]


            SKU = ''

            Title              = row[5] #.replace('\'','`')


            ProductID       = row[6]
            ImageURL = row[8]
            if ImageURL is not None:
                ImageURL     = row[8].split(r'?')[0]

            Price           = row[11]
            Shipping        = row[13]
            Quantity        = row[15]
            TotalCost       = row[16]
            Shippedon       = row[19]
            LastUpdated     = row[36]
            RefundDate      = row[41]
            RefundReason    = row[42]
            UpdateTime      = datetime.datetime.now()

            sql_delete = "delete from t_order where OrderId=%s"
            cursor.execute(sql_delete,(OrderId,))

            sql_insert = "INSERT INTO t_order(PlatformName,ShopName,OrderDate,OrderId,OrderState,SKU,ShopSKU,ProductID,Quantity,Price,Shipping,Shippedon,LastUpdated,UpdateTime,Image,Title,TotalCost,RefundDate,RefundReason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); "

            #print sql_insert
            cursor.execute(sql_insert,(PlatformName,ShopName,OrderDate,OrderId,OrderState,SKU,ShopSKU,ProductID,Quantity,Price,Shipping,Shippedon,LastUpdated,UpdateTime,ImageURL,Title,TotalCost,RefundDate,RefundReason))


        self.cnxn.commit()
        cursor.close()
    def insertWishV2(self,data):
        t_chart_wish_refund_log_obj = t_chart_wish_refund_log(self.cnxn)
        t_order_of_wish_fbw_fee_obj = t_order_of_wish_fbw_fee(self.cnxn)
        #{'Order': {'last_updated': '2017-12-23T04:20:10', 'refunded_time': '2017-12-23', 'variant_id': '58ca21d8415c9d10f9e1f5c5', 'requires_delivery_confirmation': 'False', 'refunded_by': 'REFUNDED BY WISH FOR MERCHANT', 'cost': '0.85', 'shipping_cost': '0.85', 'sku': 'YIYI0683', 'shipping_provider': 'Yanwen', 'order_total': '1.7', 'state': 'REFUNDED', 'refunded_reason': 'Shipping taking too long', 'product_name': 'Silver Small  Bells Bracelet Women&#39;s Fashion Jewelry Bracelet Adjustable', 'transaction_id': '59ffdfaef3d77e7c40e39bd6', 'order_time': '2017-11-06T04:06:07', 'order_id': '59ffdfaf7fb32058245cea71', 'price': '1.0', 'ShippingDetail': {'phone_number': '2056168267', 'city': 'Pensacola', 'name': 'Cindy Steadman', 'country': 'US', 'zipcode': '32507', 'street_address1': '10085 north loop rd #4', 'state': 'Florida'}, 'is_wish_express': 'False', 'product_image_url': 'https:\\/\\/contestimg.wish.com\\/api\\/webimage\\/58ca21d8415c9d10f9e1f5c3-normal.jpg?cache_buster=07f5b38ede50dd311f1f68157ae14cc7', 'shipped_date': '2017-11-06', 'tracking_confirmed': 'True', 'product_id': '58ca21d8415c9d10f9e1f5c3', 'shipping': '1.0', 'tracking_number': '8001535543033', 'tracking_confirmed_date': '2017-11-11T02:35:34', 'buyer_id': '57c6f9fbc3eea72dc2328dfd', 'quantity': '1'}}
        #{'Order': {'last_updated': '2017-12-23T02:07:23', 'variant_id': '58e7544b28c2731929227750', 'requires_delivery_confirmation': 'False', 'shipped_date': '2017-12-23', 'cost': '1.7', 'shipping_cost': '0.85', 'sku': 'YIYI0696', 'shipping_provider': 'PX4', 'order_total': '2.55', 'state': 'SHIPPED', 'product_name': 'Soft Ball Puzzle Fun Baby Infant Baby Teether Toy Rattles Spherical Molar Baby Physical Exercise Toy', 'transaction_id': '5a3c27c0cbe959d4e463031e', 'order_time': '2017-12-21T21:29:36', 'order_id': '5a3c27c0df424514f14d3b86', 'price': '2.0', 'ShippingDetail': {'phone_number': '096225134', 'city': 'Hirschau', 'name': 'Nicoleta Bischof', 'country': 'DE', 'zipcode': '92242', 'street_address1': 'Klostergasse 22'}, 'is_wish_express': 'False', 'product_image_url': 'https:\\/\\/contestimg.wish.com\\/api\\/webimage\\/58e7544b28c273192922774e-normal.jpg?cache_buster=ab029a461cdd1d41ba05ef5ffe5b1320', 'tracking_confirmed': 'False', 'product_id': '58e7544b28c273192922774e', 'shipping': '1.0', 'tracking_number': 'OZ034586029PY', 'buyer_id': '5918d37818b43a855637ce38', 'quantity': '1'}}
        redreshdict = {}

        cursor = self.cnxn.cursor()
        redreshdict['ShopName'] = self.ShopName
        productlist = []
        for row in data:
            PlatformName = 'Wish'
            ShopName     = self.ShopName
            OrderDate    = row['Order'].get('order_time','')
            OrderId      = row['Order'].get('order_id','')
            OrderState   = row['Order'].get('state','')
            ShopSKU      = row['Order'].get('sku','')
            SKU          = ''
            Title        = row['Order'].get('product_name','') #.replace('\'','`')
            ProductID    = row['Order'].get('product_id','')

            productlist.append(ProductID)
            ImageURL = row['Order'].get('product_image_url','').replace('\\','')

            Price           = row['Order'].get('price','')
            Shipping        = row['Order'].get('shipping','')
            Quantity        = row['Order'].get('quantity','')
            TotalCost       = row['Order'].get('order_total','')
            Shippedon       = row['Order'].get('shipped_date','')
            LastUpdated     = row['Order'].get('last_updated','')
            RefundDate      = row['Order'].get('refunded_time','')
            RefundReason    = row['Order'].get('refunded_reason','').decode("unicode-escape")
            UpdateTime      = datetime.datetime.now()

            is_wish_express = row['Order'].get('is_wish_express','')  # 海外仓信息 标志
            is_fbw = row['Order'].get('is_fbw')  # fbw 订单处理
            fbw_fee_list = row['Order'].get('fbw_fees', [])
            if is_fbw == 'True':
                fbw_default = {
                    'currency': None,
                    'amount': None,
                    'fee_name': None,
                    'fee_type_text': None,
                    'fee_type': None,
                    'order_id': None
                }

                fbw_fee = fbw_fee_list[0]['FBWFee'] if len(fbw_fee_list) >= 1 else fbw_default
                fbw_fee['fbw_warehouse_code'] = row['Order'].get('fbw_warehouse_code')
                fbw_fee['order_id'] = OrderId
                fee_result = t_order_of_wish_fbw_fee_obj.insert_fbw_fee(fbw_fee)

            ShippingDetail = row['Order'].get('ShippingDetail','')  # 买家信息 标志

            fine_ids = row['Order'].get('fine_ids',[])  # 罚款ID

            log_param = {'OrderID':OrderId,'OrderState':OrderState,'OrderFlag':'',}

            cursor.execute("select count(OrderId) from t_order WHERE OrderId = %s ; ", (OrderId,))
            ordernum = cursor.fetchone()
            if ordernum[0] > 0 :
                sql_update = "update t_order set OrderState = %s, SKU = %s, LastUpdated = %s, UpdateTime = %s," \
                             " TotalCost = %s, RefundDate = %s, RefundReason = %s, WishExpress = %s, FBWStatus=%s," \
                             "BuyerInfor = %s " \
                             "WHERE OrderId = %s ;"

                cursor.execute(sql_update, (OrderState,SKU,LastUpdated,UpdateTime,TotalCost,RefundDate,RefundReason,
                                            is_wish_express,is_fbw,str(ShippingDetail),OrderId))

                log_param['OrderFlag'] = 'OrderUpdate'
            else:
                sql_insert = "INSERT INTO t_order(PlatformName,ShopName,OrderDate,OrderId,OrderState,SKU,ShopSKU," \
                             "ProductID,Quantity,Price,Shipping,Shippedon,LastUpdated,UpdateTime,Image,Title," \
                             "TotalCost,RefundDate,RefundReason,WishExpress,FBWStatus,BuyerInfor) VALUES " \
                             "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); "
                cursor.execute(sql_insert,
                               (PlatformName,ShopName,OrderDate,OrderId,OrderState,SKU,ShopSKU,
                               ProductID,Quantity,Price,Shipping,Shippedon,LastUpdated,UpdateTime,ImageURL,Title,
                               TotalCost,RefundDate,RefundReason,is_wish_express,is_fbw,str(ShippingDetail)))

                log_param['OrderFlag'] = 'OrderInsert'
            t_chart_wish_refund_log_obj.insert_data_log(log_param)

            for fine_id in fine_ids:
                param_data = {'access_token': self.access_token, 'fine_id': fine_id}
                fine_infor_result = cwishapi().fine_info(param_data)
                if fine_infor_result['errorcode'] == 1:
                    fine_infor_result['fine_info']['order_id'] = OrderId
                    order_fine_insert_result = order_fine(self.cnxn).insert(fine_infor_result['fine_info'])

        # 整理order信息
        redreshdict['ProductID'] = productlist
        #self.cnxn.commit()
        # cursor.execute("commit;")
        cursor.close()

        return redreshdict


    def get_order_data_by_productid(self,productid,warehouse):
        sevtimeq = (datetime.datetime.utcnow() + datetime.timedelta(days=-8)).strftime('%Y-%m-%d')
        sevtimej = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

        if warehouse == 'STANDARD':
            sql = "select ProductID,date_format(LEFT(OrderDate,10), '%%Y%%m%%d'),count(Quantity),now(), 'STANDARD' from hq_db.t_order " \
                  "where LEFT(OrderDate,10) between %s and %s and ProductID = %s AND " \
                  "(WishExpress='False' or WishExpress is null) AND (FBWStatus='False' or FBWStatus is null) " \
                  "group by productid,LEFT(OrderDate,10) ORDER BY LEFT(OrderDate,10) ASC;"

        elif warehouse == 'FBW':
            sql = "select ProductID,date_format(LEFT(OrderDate,10), '%%Y%%m%%d'),count(Quantity),now() , " \
                  "(SELECT fbw_warehouse_code FROM t_order_of_wish_fbw_fee WHERE order_id = OrderID) as fbw_warehouse_code" \
                  " from hq_db.t_order " \
                  "where LEFT(OrderDate,10) between %s and %s and ProductID = %s AND FBWStatus = 'True' " \
                  "group by ProductID, LEFT(OrderDate,10) ORDER BY LEFT(OrderDate,10) ASC;"

        else:
            sql = "select ProductID,date_format(LEFT(OrderDate,10), '%%Y%%m%%d'),count(Quantity),now(), '{}' from hq_db.t_order " \
                  "where LEFT(OrderDate,10) between %s and %s and ProductID = %s AND WishExpress = 'True' and " \
                  "(FBWStatus='False' or FBWStatus is null) AND BuyerInfor LIKE \"%%'country': '{}'%%\"" \
                  "group by productid,LEFT(OrderDate,10) ORDER BY LEFT(OrderDate,10) ASC;".format(warehouse, warehouse)

        # print 'sql==={}'.format(sql)
        ordcur = self.cnxn.cursor()
        ordcur.execute(sql, (sevtimeq,sevtimej,productid,))
        objs = ordcur.fetchall()
        ordcur.close()

        return objs


    def fbw_shopsku_sales(self, product_id, shopsku, warecode):
        try:
            sql = "SELECT SUM(Quantity),Shipping FROM t_order WHERE ProductID=%s and ShopSKU=%s and FBWStatus = 'True' " \
                  " and orderID in (SELECT order_id FROM t_order_of_wish_fbw_fee WHERE fbw_warehouse_code=%s);"
            cursor = self.cnxn.cursor()
            cursor.execute(sql, (product_id, shopsku, warecode))
            obj = cursor.fetchone()
            cursor.close()
            if obj and obj[0]:
                return {'errorcode': 1, 'ofsales': obj[0], 'Shipping': obj[1]}
            else:
                return {'errorcode': 0}
        except Exception as error:
            return {'errorcode': -1, 'errortext': u'{}'.format(error)}



















