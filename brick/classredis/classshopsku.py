# -*- coding: utf-8 -*-

class classshopsku():
    def __init__(self,db_conn=None,redis_conn=None,shopname=None):
        self.db_conn = db_conn
        self.redis_conn = redis_conn
        self.shopname = shopname
        self.platform = self.__get_platform()

    def __get_platform(self):
        return self.shopname.split('-')[0] if self.shopname else None

    def __newKey(self, k): #
        return '{}.{}'.format(self.shopname, k) if self.shopname else k

    #私有方法
    def __private_set_attr(self,name,key,value):
        if self.platform == 'Wish':
            key = self.__newKey(key)

        if self.redis_conn is not None and value is not None:
            self.redis_conn.hset(name, key,value)

    def __private_get_attr(self,name,key):
        if self.platform == 'Wish':
            key = self.__newKey(key)
            
        if self.redis_conn is not None:
            return self.redis_conn.hget(name,key)

    def __private_del_attr(self, name, key):
        if self.redis_conn is not None:
            self.redis_conn.hdel(name, key)

    def __private_del_all(self, name):
        if self.redis_conn is not None:
            return self.redis_conn.delete(name)

    def delname(self,name):
        self.__private_del_all(name)

    def getskueach(self,shopsku):
        sku = self.__private_get_attr(shopsku, 'SKU')
        if sku is None and self.db_conn is not None:
            skusor = self.db_conn.cursor()
            skusor.execute("select SKU from py_db.b_goodsskulinkshop WHERE ShopSKU = %s ;", (shopsku,))
            obj = skusor.fetchone()
            if obj:
                sku = obj[0]
                self.setSKU(shopsku, sku)
            else:
                skusor.execute("select SKU from py_db.b_goods WHERE SKU = %s ;", (shopsku,))
                skuobj = skusor.fetchone()
                if skuobj:
                    sku = skuobj[0]
                    self.setSKU(shopsku, sku)
                else:
                    skusor.execute("select sku from t_shopsku_information_binding where shopsku = %s;", (shopsku,))
                    skuobj = skusor.fetchone()
                    if skuobj:
                        sku = skuobj[0]
            skusor.close()
        return sku

    # 商品sku
    def getSKU(self,shopsku):
        if shopsku:
            shopsku = shopsku.strip()
        sku = None
        skulist = []
        for shopskutmp in shopsku.split('+'):
            newshopsku = shopskutmp.split('*')[0].split('\\')[0].split('/')[0]
            sku = self.getskueach(newshopsku.strip())

            if sku:
                newshopsku_list = shopskutmp.split('*')
                if len(newshopsku_list) == 1 or self.platform == 'Wish':
                    skulist.append(sku.strip())
                else:
                    skulist.append((sku + '*' + str(newshopsku_list[1])).strip())
        if skulist:
            sku = '+'.join(skulist)
        return sku

    def setSKU(self,shopsku,sku):
        return self.__private_set_attr(shopsku,'SKU',sku)

    def delsku(self,shopsku):
        self.__private_del_attr(shopsku,'SKU')

    #Price
    def getPrice(self,shopsku):
        price = self.__private_get_attr(shopsku,'Price')
        if price is None and self.db_conn is not None:
            pricur = self.db_conn.cursor()
            if self.shopname:
                pricur.execute("select Price from t_online_info WHERE ShopSKU = %s and ShopName = %s ;",(shopsku, self.shopname))
            else:
                pricur.execute("select Price from t_online_info WHERE ShopSKU = %s;",(shopsku,))
            obj = pricur.fetchone()
            pricur.close()
            if obj:
                price = obj[0]
                self.setPrice(shopsku,price)
        return price

    #JoomPrice
    def getJoomPrice(self,shopsku):
        # price = self.__private_get_attr(shopsku,'Price')
        price = None
        if price is None and self.db_conn is not None:
            pricur = self.db_conn.cursor()
            pricur.execute("select Price from t_online_info_joom_detail WHERE ShopSKU = %s ;",(shopsku,))
            obj = pricur.fetchone()
            pricur.close()
            if obj:
                price = obj[0]
                # self.setPrice(shopsku,price)
        return price

    def setPrice(self,shopsku,Price):
        return self.__private_set_attr(shopsku,'Price',Price)

    #Quantity
    def getQuantity(self,shopsku):
        quantity = self.__private_get_attr(shopsku,'Quantity')
        if quantity is None and self.db_conn is not None:
            quacur = self.db_conn.cursor()
            if self.shopname:
                quacur.execute("select Quantity from t_online_info WHERE ShopSKU = %s and ShopName = %s  ;", (shopsku, self.shopname))
            else:
                quacur.execute("select Quantity from t_online_info WHERE ShopSKU = %s ;", (shopsku,))
            obj = quacur.fetchone()
            quacur.close()
            if obj:
                quantity = obj[0]
                self.setQuantity(shopsku,quantity)
        return quantity

    #JoomQuantity
    def getJoomQuantity(self,shopsku):
        # quantity = self.__private_get_attr(shopsku,'Quantity')
        quantity = None
        if quantity is None and self.db_conn is not None:
            quacur = self.db_conn.cursor()
            quacur.execute("select Quantity from t_online_info_joom_detail WHERE ShopSKU = %s ;", (shopsku,))
            obj = quacur.fetchone()
            quacur.close()
            if obj:
                quantity = obj[0]
                # self.setQuantity(shopsku,quantity)
        return quantity

    def setQuantity(self,shopsku,Quantity):
        return self.__private_set_attr(shopsku,'Quantity',Quantity)

    def getWishDEQuantity(self,shopsku):
        quantity = self.__private_get_attr(shopsku, 'DEQuantity')
        if quantity is None and self.db_conn is not None:
            quacur = self.db_conn.cursor()
            if self.shopname:
                quacur.execute("select DEExpressInventory from t_online_info WHERE ShopSKU = %s and ShopName = %s  ;", (shopsku, self.shopname))
            else:
                quacur.execute("select DEExpressInventory from t_online_info WHERE ShopSKU = %s ;", (shopsku,))
            obj = quacur.fetchone()
            quacur.close()
            if obj:
                quantity = obj[0]
                self.setWishDEQuantity(shopsku,quantity)
        return quantity

    def setWishDEQuantity(self,shopsku,Quantity):
        return self.__private_set_attr(shopsku,'DEQuantity',Quantity)

    def getWishGBQuantity(self, shopsku):
        quantity = self.__private_get_attr(shopsku, 'GBQuantity')
        if quantity is None and self.db_conn is not None:
            quacur = self.db_conn.cursor()
            if self.shopname:
                quacur.execute("select GBExpressInventory from t_online_info WHERE ShopSKU = %s and ShopName = %s  ;", (shopsku, self.shopname))
            else:
                quacur.execute("select GBExpressInventory from t_online_info WHERE ShopSKU = %s ;", (shopsku,))
            obj = quacur.fetchone()
            quacur.close()
            if obj:
                quantity = obj[0]
                self.setWishGBQuantity(shopsku, quantity)
        return quantity

    def setWishGBQuantity(self, shopsku, Quantity):
        return self.__private_set_attr(shopsku, 'GBQuantity', Quantity)

    def getWishUSQuantity(self, shopsku):
        quantity = self.__private_get_attr(shopsku, 'USQuantity')
        if quantity is None and self.db_conn is not None:
            quacur = self.db_conn.cursor()
            if self.shopname:
                quacur.execute("select USExpressInventory from t_online_info WHERE ShopSKU = %s and ShopName = %s  ;", (shopsku, self.shopname))
            else:
                quacur.execute("select USExpressInventory from t_online_info WHERE ShopSKU = %s ;", (shopsku,))
            obj = quacur.fetchone()
            quacur.close()
            if obj:
                quantity = obj[0]
                self.setWishUSQuantity(shopsku, quantity)
        return quantity

    def setWishUSQuantity(self, shopsku, Quantity):
        return self.__private_set_attr(shopsku, 'USQuantity', Quantity)

    #Status
    def getStatus(self,shopsku):
        status = self.__private_get_attr(shopsku,'Status')
        if status is None and self.db_conn is not None:
            stacur = self.db_conn.cursor()
            if self.shopname:
                stacur.execute("select Status from t_online_info WHERE ShopSKU = %s and ShopName = %s  ;",(shopsku, self.shopname))
            else:
                stacur.execute("select Status from t_online_info WHERE ShopSKU = %s ;",(shopsku,))
            obj = stacur.fetchone()
            stacur.close()
            if obj:
                status = obj[0]
                self.setStatus(shopsku,status)
        return status

    #JoomStatus
    def getJoomStatus(self,shopsku):
        # status = self.__private_get_attr(shopsku,'Status')
        status = None
        if status is None and self.db_conn is not None:
            stacur = self.db_conn.cursor()
            stacur.execute("select Status from t_online_info_joom_detail WHERE ShopSKU = %s ;",(shopsku,))
            obj = stacur.fetchone()
            stacur.close()
            if obj:
                status = obj[0]
                # self.setStatus(shopsku,status)
        return status

    def setStatus(self,shopsku,status):
        self.__private_set_attr(shopsku,'Status',status)

    #Shipping
    def getShipping(self,shopsku):
        shipping = self.__private_get_attr(shopsku,'Shipping')
        if shipping is None and self.db_conn is not None:
            shicur = self.db_conn.cursor()
            if self.shopname:
                shicur.execute("select Shipping from t_online_info where ShopSKU = %s and ShopName = %s  ;",(shopsku, self.shopname))
            else:
                shicur.execute("select Shipping from t_online_info where ShopSKU = %s ;",(shopsku,))
            obj = shicur.fetchone()
            shicur.close()
            if obj:
                shipping = obj[0]
                self.setShipping(shopsku,shipping)
        return shipping

    #JoomShipping
    def getJoomShipping(self,shopsku):
        # shipping = self.__private_get_attr(shopsku,'Shipping')
        shipping = None
        if shipping is None and self.db_conn is not None:
            shicur = self.db_conn.cursor()
            shicur.execute("select Shipping from t_online_info_joom_detail where ShopSKU = %s ;",(shopsku,))
            obj = shicur.fetchone()
            shicur.close()
            if obj:
                shipping = obj[0]
                # self.setShipping(shopsku,shipping)
        return shipping

    def setShipping(self,shopsku,Shipping):
        return self.__private_set_attr(shopsku,'Shipping',Shipping)

    def getWishDEShipping(self,shopsku):
        shipping = self.__private_get_attr(shopsku,'DEShipping')
        if shipping is None and self.db_conn is not None:
            shicur = self.db_conn.cursor()
            if self.shopname:
                shicur.execute("select DEExpressShipping from t_online_info where ShopSKU = %s and ShopName = %s  ;",(shopsku, self.shopname))
            else:
                shicur.execute("select DEExpressShipping from t_online_info where ShopSKU = %s ;",(shopsku,))
            obj = shicur.fetchone()
            shicur.close()
            if obj:
                shipping = obj[0]
                self.setWishDEShipping(shopsku,shipping)
        return shipping

    def setWishDEShipping(self,shopsku,Shipping):
        return self.__private_set_attr(shopsku,'DEShipping',Shipping)

    def getWishGBShipping(self,shopsku):
        shipping = self.__private_get_attr(shopsku,'GBShipping')
        if shipping is None and self.db_conn is not None:
            shicur = self.db_conn.cursor()
            if self.shopname:
                shicur.execute("select GBExpressShipping from t_online_info where ShopSKU = %s and ShopName = %s  ;",(shopsku, self.shopname))
            else:
                shicur.execute("select GBExpressShipping from t_online_info where ShopSKU = %s ;",(shopsku,))
            obj = shicur.fetchone()
            shicur.close()
            if obj:
                shipping = obj[0]
                self.setWishGBShipping(shopsku,shipping)
        return shipping

    def setWishGBShipping(self,shopsku,Shipping):
        return self.__private_set_attr(shopsku,'GBShipping',Shipping)

    def getWishUSShipping(self,shopsku):
        shipping = self.__private_get_attr(shopsku,'USShipping')
        if shipping is None and self.db_conn is not None:
            shicur = self.db_conn.cursor()
            if self.shopname:
                shicur.execute("select USExpressShipping from t_online_info where ShopSKU = %s and ShopName = %s  ;",(shopsku, self.shopname))
            else:
                shicur.execute("select USExpressShipping from t_online_info where ShopSKU = %s ;",(shopsku,))
            obj = shicur.fetchone()
            shicur.close()
            if obj:
                shipping = obj[0]
                self.setWishUSShipping(shopsku,shipping)
        return shipping

    def setWishUSShipping(self,shopsku,Shipping):
        return self.__private_set_attr(shopsku,'USShipping',Shipping)

    #Image
    def getImage(self,shopsku):
        image =  self.__private_get_attr(shopsku,'Image')
        if image is None and self.db_conn is not None:
            imacur = self.db_conn.cursor()
            if self.shopname:
                imacur.execute("select ShopSKUImage from t_online_info WHERE ShopSKU = %s and ShopName = %s ;",(shopsku, self.shopname))
            else:
                imacur.execute("select ShopSKUImage from t_online_info WHERE ShopSKU = %s ;",(shopsku,))
            obj = imacur.fetchone()
            imacur.close()
            if obj:
                image = obj[0]
                self.setImage(shopsku,image)
        return image

    #JoomImage
    def getJoomImage(self,shopsku):
        # image =  self.__private_get_attr(shopsku,'Image')
        image = None
        if image is None and self.db_conn is not None:
            imacur = self.db_conn.cursor()
            imacur.execute("select ShopSKUImage from t_online_info_joom_detail WHERE ShopSKU = %s ;",(shopsku,))
            obj = imacur.fetchone()
            imacur.close()
            if obj:
                image = obj[0]
                # self.setImage(shopsku,image)
        return image

    def setImage(self,shopsku,Image):
        return self.__private_set_attr(shopsku,'Image',Image)

    #Color
    def getColor(self,shopsku):
        color = self.__private_get_attr(shopsku,'Color')
        if color is None and self.db_conn is not None:
            colcur = self.db_conn.cursor()
            if self.shopname:
                colcur.execute("select Color from t_online_info WHERE ShopSKU = %s and ShopName = %s;",(shopsku, self.shopname))
            else:
                colcur.execute("select Color from t_online_info WHERE ShopSKU = %s ;",(shopsku,))
            obj = colcur.fetchone()
            colcur.close()
            if obj:
                color = obj[0]
                self.setColor(shopsku,color)
        return color

    #JoomColor
    def getJoomColor(self,shopsku):
        # color = self.__private_get_attr(shopsku,'Color')
        color = None
        if color is None and self.db_conn is not None:
            colcur = self.db_conn.cursor()
            colcur.execute("select Color from t_online_info_joom_detail WHERE ShopSKU = %s ;",(shopsku,))
            obj = colcur.fetchone()
            colcur.close()
            if obj:
                color = obj[0]
                # self.setColor(shopsku,color)
        return color

    def setColor(self,shopsku,Color):
        return self.__private_set_attr(shopsku,'Color',Color)

    #Size
    def getSize(self,shopsku):
        site = self.__private_get_attr(shopsku,'Size')
        if site is None and self.db_conn is not None:
            sitcur = self.db_conn.cursor()
            if self.shopname:
                sitcur.execute("select `Size` from t_online_info WHERE ShopSKU = %s and ShopName = %s;",(shopsku, self.shopname))
            else:
                sitcur.execute("select `Size` from t_online_info WHERE ShopSKU = %s ;",(shopsku,))
            obj = sitcur.fetchone()
            sitcur.close()
            if obj:
                site = obj[0]
                self.setSize(shopsku,site)
        return site

    #JoomSize
    def getJoomSize(self,shopsku):
        # size = self.__private_get_attr(shopsku,'Size')
        size = None
        if size is None and self.db_conn is not None:
            sitcur = self.db_conn.cursor()
            sitcur.execute("select `Size` from t_online_info_joom_detail WHERE ShopSKU = %s ;",(shopsku,))
            obj = sitcur.fetchone()
            sitcur.close()
            if obj:
                size = obj[0]
                # self.setSize(shopsku,size)
        return size

    def setSize(self,shopsku,Size):
        return self.__private_set_attr(shopsku,'Size',Size)

    # msrp
    def getmsrp(self, shopsku):
        msrp = self.__private_get_attr(shopsku, 'msrp')
        if msrp is None and self.db_conn is not None:
            msrcur = self.db_conn.cursor()
            if self.shopname:
                msrcur.execute("select msrp from t_online_info WHERE ShopSKU = %s and ShopName = %s;", (shopsku, self.shopname))
            else:
                msrcur.execute("select msrp from t_online_info WHERE ShopSKU = %s ;", (shopsku,))
            obj = msrcur.fetchone()
            msrcur.close()
            if obj:
                msrp = obj[0]
                self.setmsrp(shopsku, msrp)
        return msrp

    # Joommsrp
    def getJoommsrp(self, shopsku):
        # msrp = self.__private_get_attr(shopsku, 'msrp')
        msrp = None
        if msrp is None and self.db_conn is not None:
            msrcur = self.db_conn.cursor()
            msrcur.execute("select msrp from t_online_info_joom_detail WHERE ShopSKU = %s ;", (shopsku,))
            obj = msrcur.fetchone()
            msrcur.close()
            if obj:
                msrp = obj[0]
                # self.setmsrp(shopsku, msrp)
        return msrp

    def setmsrp(self, shopsku, msrp):
        return self.__private_set_attr(shopsku, 'msrp', msrp)

    # ShippingTime
    def getshippingtime(self, shopsku):
        shippingtime = self.__private_get_attr(shopsku, 'ShippingTime')
        if shippingtime is None and self.db_conn is not None:
            shtcur = self.db_conn.cursor()
            if self.shopname:
                shtcur.execute("select ShippingTime from t_online_info WHERE ShopSKU = %s and ShopName = %s;", (shopsku, self.shopname))
            else:
                shtcur.execute("select ShippingTime from t_online_info WHERE ShopSKU = %s ;", (shopsku,))
            obj = shtcur.fetchone()
            shtcur.close()
            if obj:
                shippingtime = obj[0]
                self.setshippingtime(shopsku, shippingtime)
        return shippingtime

    # JoomShippingTime
    def getJoomshippingtime(self, shopsku):
        # shippingtime = self.__private_get_attr(shopsku, 'ShippingTime')
        shippingtime = None
        if shippingtime is None and self.db_conn is not None:
            shtcur = self.db_conn.cursor()
            shtcur.execute("select ShippingTime from t_online_info_joom_detail WHERE ShopSKU = %s ;", (shopsku,))
            obj = shtcur.fetchone()
            shtcur.close()
            if obj:
                shippingtime = obj[0]
                # self.setshippingtime(shopsku, shippingtime)
        return shippingtime

    def setshippingtime(self, shopsku, shippingtime):
        return self.__private_set_attr(shopsku, 'ShippingTime', shippingtime)

    # 商品Published
    def getPublished(self, shopsku):
        published = self.__private_get_attr(shopsku, 'Published')
        if (published is None or published.strip() == '') and self.db_conn is not None:
            persor = self.db_conn.cursor()
            persor.execute("select PersonCode from py_db.b_goodsskulinkshop WHERE ShopSKU = %s;", (shopsku,))
            obj = persor.fetchone()
            persor.close()
            if obj:
                published = obj[0]
                self.setPublished(shopsku, published)
        return published

    def setPublished(self, shopsku, published):
        return self.__private_set_attr(shopsku, 'Published', published)

    # 所属店铺
    def get_shopname_by_shopsku(self, shopsku):
        shopname = self.__private_get_attr(shopsku, 'ShopName')
        if shopname is None and self.db_conn is not None:
            persor = self.db_conn.cursor()
            persor.execute("select ShopName from t_online_info WHERE ShopSKU = %s;", (shopsku,))
            obj = persor.fetchone()
            persor.close()
            if obj:
                shopname = obj[0]
                self.set_shopname_by_shopsku(shopsku, shopname)
        return shopname

    # 所属Joom店铺
    def get_Joomshopname_by_shopsku(self, shopsku):
        # shopname = self.__private_get_attr(shopsku, 'ShopName')
        shopname = None
        if shopname is None and self.db_conn is not None:
            persor = self.db_conn.cursor()
            persor.execute("select ShopName from t_online_info_joom_detail WHERE ShopSKU = %s ;", (shopsku,))
            obj = persor.fetchone()
            persor.close()
            if obj:
                shopname = obj[0]
                # self.set_shopname_by_shopsku(shopsku, shopname)
        return shopname

    def set_shopname_by_shopsku(self, shopsku, shopname):
        return self.__private_set_attr(shopsku, 'ShopName', shopname)