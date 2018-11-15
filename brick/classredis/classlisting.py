# -*- coding: utf-8 -*-
class classlisting():
    def __init__(self,db_conn=None,redis_conn=None):
        self.db_conn = db_conn
        self.redis_conn = redis_conn

    def __private_set_attr(self,name,key,value):
        if self.redis_conn is not None and value is not None:
            return self.redis_conn.hset(name, key,value)

    def __private_get_attr(self,name,key):
        if self.redis_conn is not None:
            return self.redis_conn.hget(name,key)

    def __private_del_attr(self, name):
        if self.redis_conn is not None:
            return self.redis_conn.delete(name)

    def delname(self,name):
        self.__private_del_attr(name)

    #ShopSKUList
    def getShopSKUList(self,listingid):
        shopsku = self.__private_get_attr(listingid,'ShopSKUList')
        if shopsku is None and self.db_conn is not None:
            shopcur = self.db_conn.cursor()
            shopcur.execute("select ShopSKU from t_online_info WHERE ProductID = %s ;",(listingid,))
            objs = shopcur.fetchall()
            shopcur.close()
            shopskulist = []
            for obj in objs:
                if obj and obj[0] is not None:
                    shopskulist.append(obj[0])
            shopsku = '|'.join(shopskulist)
            if len(shopskulist) >= 1:
                self.setShopSKUList(listingid, shopsku)
        if shopsku is not None:
            shopsku = shopsku.split('|')
        return shopsku

    #JoomShopSKUList
    def getJoomShopSKUList(self,listingid):
        shopsku = self.__private_get_attr(listingid,'ShopSKUList')
        if shopsku is None and self.db_conn is not None:
            shopcur = self.db_conn.cursor()
            shopcur.execute("select ShopSKU from t_online_info_joom_detail WHERE ProductID = %s ;",(listingid,))
            objs = shopcur.fetchall()
            shopcur.close()
            shopskulist = []
            for obj in objs:
                if obj and obj[0] is not None:
                    shopskulist.append(obj[0])
            shopsku = '|'.join(shopskulist)
            if len(shopskulist) >= 1:
                self.setShopSKUList(listingid, shopsku)
        if shopsku is not None:
            shopsku = shopsku.split('|')
        return shopsku

    def setShopSKUList(self,listingid,ShopSKUList):
        return self.__private_set_attr(listingid,'ShopSKUList',ShopSKUList)

    #ShopName
    def getShopName(self,listingid):
        shopname = self.__private_get_attr(listingid,'ShopName')
        if shopname is None and self.db_conn is not None:
            namecur = self.db_conn.cursor()
            namecur.execute("select ShopName from t_online_info WHERE ProductID = %s ;",(listingid,))
            obj = namecur.fetchone()
            namecur.close()
            if obj:
                shopname = obj[0]
                self.setShopName(listingid,shopname)
        return shopname

    #JoomShopName
    def getJoomShopName(self,listingid):
        shopname = self.__private_get_attr(listingid,'ShopName')
        if shopname is None and self.db_conn is not None:
            namecur = self.db_conn.cursor()
            namecur.execute("select ShopName from t_online_info_joom_detail WHERE ProductID = %s ;",(listingid,))
            obj = namecur.fetchone()
            namecur.close()
            if obj:
                shopname = obj[0]
                self.setShopName(listingid,shopname)
        return shopname

    def setShopName(self,listingid,ShopName):
        return self.__private_set_attr(listingid,'ShopName',ShopName)

    #Title
    def getTitle(self,listingid):
        title = self.__private_get_attr(listingid,'Title')
        if title is None and self.db_conn is not None:
            titlecur = self.db_conn.cursor()
            titlecur.execute("select Title from t_online_info WHERE ProductID = %s ;",(listingid,))
            obj = titlecur.fetchone()
            titlecur.close()
            if obj:
                title = obj[0]
                self.setTitle(listingid,title)
        return title

    #Title
    def getJoomTitle(self,listingid):
        title = self.__private_get_attr(listingid,'Title')
        if title is None and self.db_conn is not None:
            titlecur = self.db_conn.cursor()
            titlecur.execute("select Title from t_online_info_joom_detail WHERE ProductID = %s ;",(listingid,))
            obj = titlecur.fetchone()
            titlecur.close()
            if obj:
                title = obj[0]
                self.setTitle(listingid,title)
        return title

    def setTitle(self,listingid,Title):
        return self.__private_set_attr(listingid,'Title',Title)

    #Status
    def getStatus(self,listingid):
        status = self.__private_get_attr(listingid,'Status')
        if status is None and self.db_conn is not None:
            statuscur = self.db_conn.cursor()
            statuscur.execute("select `Status` from t_online_info WHERE ProductID = %s ;",(listingid,))
            objs = statuscur.fetchall()
            statuscur.close()
            statuslist = []
            for obj in objs:
                if obj and obj[0] is not None:
                    statuslist.append(obj[0])
            if 'Enabled' in statuslist:
                status = 'Enabled'
            else:
                status = 'Disabled'
            self.setStatus(listingid,status)
        return status

    #JoomStatus
    def getJoomStatus(self,listingid):
        status = self.__private_get_attr(listingid,'Status')
        if status is None and self.db_conn is not None:
            statuscur = self.db_conn.cursor()
            statuscur.execute("select `Status` from t_online_info_joom_detail WHERE ProductID = %s ;",(listingid,))
            objs = statuscur.fetchall()
            statuscur.close()
            statuslist = []
            for obj in objs:
                if obj and obj[0] is not None:
                    statuslist.append(obj[0])
            if 'Enabled' in statuslist:
                status = 'Enabled'
            else:
                status = 'Disabled'
            self.setStatus(listingid,status)
        return status

    def setStatus(self,listingid,Status):
        return self.__private_set_attr(listingid,'Status',Status)

    #DateUploaded
    def getDateUploaded(self,listingid):
        dateupload = self.__private_get_attr(listingid,'DateUploaded')
        if dateupload is None and self.db_conn is not None:
            updacur = self.db_conn.cursor()
            updacur.execute("select DateUploaded from t_online_info WHERE ProductID = %s ;",(listingid,))
            obj = updacur.fetchone()
            updacur.close()
            if obj:
                dateupload = obj[0]
                self.setDateUploaded(listingid,dateupload)
        return dateupload

    #JoomDateUploaded
    def getJoomDateUploaded(self,listingid):
        dateupload = self.__private_get_attr(listingid,'DateUploaded')
        if dateupload is None and self.db_conn is not None:
            updacur = self.db_conn.cursor()
            updacur.execute("select DateUploaded from t_online_info_joom_detail WHERE ProductID = %s ;",(listingid,))
            obj = updacur.fetchone()
            updacur.close()
            if obj:
                dateupload = obj[0]
                self.setDateUploaded(listingid,dateupload)
        return dateupload

    def setDateUploaded(self,listingid,DateUploaded):
        return self.__private_set_attr(listingid,'DateUploaded',DateUploaded)

    #ReviewState
    def getReviewState(self,listingid):
        reviewstatus = self.__private_get_attr(listingid, 'ReviewState')
        if reviewstatus is None and self.db_conn is not None:
            revcur = self.db_conn.cursor()
            revcur.execute("select ReviewState from t_online_info WHERE ProductID = %s ;", (listingid,))
            obj = revcur.fetchone()
            revcur.close()
            if obj:
                reviewstatus = obj[0]
                self.setReviewState(listingid, reviewstatus)
        return reviewstatus

    #JoomReviewState
    def getJoomReviewState(self,listingid):
        reviewstatus = self.__private_get_attr(listingid, 'ReviewState')
        if reviewstatus is None and self.db_conn is not None:
            revcur = self.db_conn.cursor()
            revcur.execute("select ReviewState from t_online_info_joom_detail WHERE ProductID = %s ;", (listingid,))
            obj = revcur.fetchone()
            revcur.close()
            if obj:
                reviewstatus = obj[0]
                self.setReviewState(listingid, reviewstatus)
        return reviewstatus

    def setReviewState(self,listingid,ReviewState):
        return self.__private_set_attr(listingid,'ReviewState',ReviewState)

    # mainsku
    def getmainsku(self, listingid):
        mainsku = self.__private_get_attr(listingid, 'MainSKU')
        if mainsku is None and self.db_conn is not None:
            maincur = self.db_conn.cursor()
            maincur.execute("select MainSKU from t_online_info WHERE ProductID = %s and MainSKU is not NULL;", (listingid,))
            objs = maincur.fetchall()
            maincur.close()
            mainskulist = []
            for obj in objs:
                if obj and obj[0] is not None:
                    mainskulist.append(obj[0])
            if mainskulist:
                mainsku = '|'.join(mainskulist)
                self.setmainsku(listingid, mainsku)
        if mainsku is not None:
            mainsku = mainsku.split('|')
        return mainsku

    # Joommainsku
    def getJoommainsku(self, listingid):
        mainsku = self.__private_get_attr(listingid, 'MainSKU')
        if mainsku is None and self.db_conn is not None:
            maincur = self.db_conn.cursor()
            maincur.execute("select MainSKU from t_online_info_joom_detail WHERE ProductID = %s ;", (listingid,))
            objs = maincur.fetchall()
            maincur.close()
            mainskulist = []
            for obj in objs:
                if obj and obj[0] is not None:
                    mainskulist.append(obj[0])
            if mainskulist:
                mainsku = '|'.join(mainskulist)
                self.setmainsku(listingid, mainsku)
        if mainsku is not None:
            mainsku = mainsku.split('|')
        return mainsku

    def setmainsku(self, listingid, mainsku):
        return self.__private_set_attr(listingid, 'MainSKU', mainsku)

    # public
    def getvaluefromredis(self, listingid):
        return self.__private_get_attr(listingid, 'hyflag')

    def setvaluefromredis(self, listingid, hyflag):
        return self.__private_set_attr(listingid, 'hyflag', hyflag)

    def delkeyfromredis(self, listingid):
        return self.__private_del_attr(listingid)

    # 加钻
    def set_is_promoted_listingid(self,listingid,value):
        self.__private_set_attr(listingid,'is_promoted',value)

    def get_is_promoted_listingid(self,listingid):
        promoted = self.__private_get_attr(listingid,'is_promoted')
        if promoted is None and self.db_conn is not None:
            procur = self.db_conn.cursor()
            procur.execute("select is_promoted from t_online_info WHERE  ProductID = %s ;",(listingid,))
            obj = procur.fetchone()
            procur.close()
            if obj:
                promoted = obj[0]
                self.set_is_promoted_listingid(listingid,promoted)
        return promoted

    # 海外仓
    def set_WishExpress_listingid(self,listingid,value):
        self.__private_set_attr(listingid,'WishExpress',value)

    def get_WishExpress_listingid(self,listingid):
        WishExpress = self.__private_get_attr(listingid,'WishExpress')
        if WishExpress is None and self.db_conn is not None:
            wecur = self.db_conn.cursor()
            wecur.execute("select WishExpress from t_online_info WHERE  ProductID = %s ;",(listingid,))
            obj = wecur.fetchone()
            wecur.close()
            if obj:
                WishExpress = obj[0]
                self.set_WishExpress_listingid(listingid,WishExpress)
        return WishExpress


    # 7天order数
    def get_order7days_listingid(self,listingid):
        order7days = self.__private_get_attr(listingid, 'Order7days')
        if order7days is None and self.db_conn is not None:
            ordcur = self.db_conn.cursor()
            ordcur.execute("select Orders7Days from t_online_info_wish WHERE ProductID=%s;",(listingid,))
            obj = ordcur.fetchone()
            ordcur.close()
            if obj:
                order7days = obj[0]
                self.set_order7days_listingid(listingid, order7days)
        return order7days

    # Joom7天order数
    def get_Joomorder7days_listingid(self,listingid):
        order7days = self.__private_get_attr(listingid, 'Order7days')
        if order7days is None and self.db_conn is not None:
            ordcur = self.db_conn.cursor()
            ordcur.execute("select Orders7Days from t_online_info_joom_detail WHERE ProductID=%s;",(listingid,))
            obj = ordcur.fetchone()
            ordcur.close()
            if obj:
                order7days = obj[0]
                self.set_order7days_listingid(listingid, order7days)
        return order7days

    def set_order7days_listingid(self,listingid,value):
        self.__private_set_attr(listingid, 'Order7days', value)