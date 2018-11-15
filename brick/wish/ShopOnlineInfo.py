# -*- coding: utf-8 -*-
import logging
import time, datetime
import StringIO, csv, sys
import requests, urllib2
import copy

from brick.table.t_api_schedule import t_api_schedule
from brick.table.t_order import t_order, strtimeaddseconds
from app_djcelery.celery import app
from brick.table.t_online_info import t_online_info
from wishlisting import refreshordersale
from wishlisting import refreshwishlisting
from brick.table.get_wish_product_order_updatetime import get_wish_product_order_updatetime
from brick.table.t_store_configuration_file import t_store_configuration_file
from brick.table.t_online_info_wish import t_online_info_wish

from brick.wish.api.wishapi import cwishapi

from brick.table.t_wish_shopcode_warehouse import t_wish_shopcode_warehouse

import traceback
# flag 为 1 增量更新
@app.task
def F_EXE_SHOP_ONLINE_INFO(db_conn,OneCmdRecoreDict,flag):

    from django_redis import get_redis_connection  # get_redis_connection(alias='product')

    t_api_scheduleImp = t_api_schedule(None,db_conn,get_redis_connection(alias='product'))

    print '--------------------------------------------------------------------OneCmdRecoreDict=%s'%OneCmdRecoreDict
    if not OneCmdRecoreDict.has_key('CMDID') or OneCmdRecoreDict is None or OneCmdRecoreDict['CMDID']  is None:
        print 'OneCmdRecoreDict=%s'%OneCmdRecoreDict
        #time.sleep(30)
        # redis_conn.client_kill('r-uf6206e9df36e854.redis.rds.aliyuncs.com:6379')
        return
    for cmdid in OneCmdRecoreDict['CMDID']:
        print 'cmdid=================',cmdid
        newOneCmdRecoreDict = copy.deepcopy(OneCmdRecoreDict)
        newOneCmdRecoreDict['CMDID'] = cmdid
        print 'newOneCmdRecoreDict=================', newOneCmdRecoreDict
        record = {}
        try:
            auth_info = t_api_scheduleImp.getauthByShopName(newOneCmdRecoreDict['ShopName'])

            cwishapi_obj = cwishapi()
            cResult = cwishapi_obj.warehouseid(auth_info['access_token'])
            assert cResult['errorcode'] == 1, cResult['errortext']

            warehouse_obj = t_wish_shopcode_warehouse(db_conn)
            wReault = warehouse_obj.update_shopcode_waregouse(newOneCmdRecoreDict['ShopName'], cResult['data'])
            assert wReault['errorcode'] == 1, wReault['errortext']

            ShopOnlineInfoImp = ShopOnlineInfo(t_api_scheduleImp,newOneCmdRecoreDict,flag,db_conn)
            print '0000000000000000000000'
            myresult = ShopOnlineInfoImp.do()
            print '1111111111111111111111'

            params = {}
            params['ShopName'] = myresult['ShopName']
            params['ProductID'] = ''
            params['dbcnxn'] = db_conn
            for productid in set(myresult['ProductID']):
                params['ProductID'] = productid
                if myresult['CMDID'] == 'GetListOrders':
                    refreshordersale.run(params)
                elif myresult['CMDID'] == 'GetShopSKUInfo':
                    refreshwishlisting.run(params)

            record = myresult['record']

        except Exception, ex:
            record = {}
            newOneCmdRecoreDict['Status'] = 'Exception'
            newOneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
            newOneCmdRecoreDict['errorinfo'] = '%s  f_GetShopSKUInfo except Exception= %s ex=%s  __LINE__=%s;%s'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),Exception,ex,sys._getframe().f_lineno,traceback.format_exc())
            #t_api_scheduleImp.refreshScheduleTimeAndTimedelta(newOneCmdRecoreDict)
            #t_api_scheduleImp.updateOneCmd(newOneCmdRecoreDict)
            t_api_scheduleImp.moveOneCmd(newOneCmdRecoreDict)
            print '%s  f_GetShopSKUInfo except Exception= %s ex=%s  __LINE__=%s;%s'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),Exception,ex,sys._getframe().f_lineno,traceback.print_exc())
            #print traceback.print_exc()
            time.sleep(1)

        if record:
            # {'start':start,'end':end,'type':type}
            get_wish_product_order_updatetime_obj = get_wish_product_order_updatetime(db_conn,newOneCmdRecoreDict['ShopName'])
            get_wish_product_order_updatetime_obj.update_time_or_insert(record['start'],record['end'],record['type'])


class ShopOnlineInfo():
    def __init__(self,t_api_scheduleImp,OneCmdRecoreDict,flag,db_conn):
        self.t_api_scheduleImp = t_api_scheduleImp
        self.OneCmdRecoreDict = OneCmdRecoreDict
        self.flag = flag
        self.db_conn = db_conn

    def do(self):
        result = {}
        if self.OneCmdRecoreDict['CMDID'] == 'UpdateInventory':
            self.UpdateInventory()
            result['CMDID'] = 'UpdateInventory'

        elif self.OneCmdRecoreDict['CMDID'] == 'GetShopSKUInfo':
            result = self.GetShopSKUInfoV2()
            result['CMDID'] = 'GetShopSKUInfo'

        elif self.OneCmdRecoreDict['CMDID'] == 'GetListOrders':
            result = self.GetListOrders2()
            result['CMDID'] = 'GetListOrders'

        else:
            result['CMDID'] = 'Other'
            pass
        return result

    def UpdateInventory(self):
        pass

    def GetShopSKUInfo(self):
        if self.OneCmdRecoreDict['TransactionID'] is None or self.OneCmdRecoreDict['TransactionID'].strip()=='':
            Params_dict = eval(self.OneCmdRecoreDict['Params'].replace("`","'"))
            #import requests
            #url_create = "https://merchant.wish.com/api/v2/product/create-download-job"
            data = {
                'access_token':self.t_api_scheduleImp.auth_info['access_token'] ,
                'format': 'json',
            }
            self.getSince(data)
            print 'data=%s'%data
            dict_ret = requests.post(Params_dict['url_create'], params=data, timeout = 10)

            print  dict_ret.__dict__
            print '---------------\n'
            #dict_ret =eval(ret)
            print 'dict_ret=%s'%dict_ret
            print '---------------\n'
            _content = eval(dict_ret._content)
            #刷新一下token  1015 :问令牌过期   4000:权存取 1016:失效
            if  _content['code']== 1015 or _content['code']== 1016:# or _content['code']== 4000   or _content['code']== 1017  or _content['code']== 1018  or _content['code']== 9000   :
                # self.RefreshToken()

                self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                self.OneCmdRecoreDict['TransactionID'] = ''
                self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)
                return
            if dict_ret.status_code==200 and  _content['code']==0 :
                    self.OneCmdRecoreDict['Status'] = '1'
                    self.OneCmdRecoreDict['ProcessingStatus'] = 'SUBMIT'
                    self.OneCmdRecoreDict['ActualBeginTime'] = datetime.datetime.now()
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.OneCmdRecoreDict['TransactionID'] = '{`job_id`:`%s`}'%(_content['data']['job_id'])
                    self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                    self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)
            else: #报错
                    #self.OneCmdRecoreDict['Status'] = '-2'
                    #self.OneCmdRecoreDict['ProcessingStatus'] = dict_ret.status_code
                    self.OneCmdRecoreDict['Status'] = dict_ret.status_code
                    self.OneCmdRecoreDict['ProcessingStatus'] = _content['code']
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)

        else:
            TransactionID_dict = eval(self.OneCmdRecoreDict['TransactionID'].replace("`","'"))
            print 'TransactionID_dict=%s'%TransactionID_dict

            Params_dict = eval(self.OneCmdRecoreDict['Params'].replace("`","'"))
            print self.OneCmdRecoreDict['Params']

            data = {
                'access_token':self.t_api_scheduleImp.auth_info['access_token'] ,
                'format': 'json',
                'job_id': TransactionID_dict['job_id'],
            }
            dict_ret = requests.post(Params_dict['url_status'], params=data, timeout = 10)

            #dict_ret =eval(ret)
            #print json.dumps(dict_ret, indent=1)
            print '---------------\n'
            print 'dict_ret=%s'%dict_ret
            print '---------------\n'
            print dict_ret.__dict__
            print '---------------\n'
            print dict_ret._content
            _content = eval(dict_ret._content)
            #刷新一下token  1015 :问令牌过期   4000:权存取
            if  _content['code']== 1015 or _content['code']== 1016:#or _content['code']== 4000  or _content['code']== 1016 or _content['code']== 1017  or _content['code']== 1018  or _content['code']== 9000   :
                # self.RefreshToken()

                self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                self.OneCmdRecoreDict['TransactionID'] = ''
                self.OneCmdRecoreDict['ProcessingStatus'] = _content['code']
                self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)
                return
            if dict_ret.status_code  ==200 and  _content['code']==0 :
                if _content['data']['status']  == 'FINISHED' :
                    if _content['data']['total_count'] > 0 and  _content['data'].has_key('download_link'):
                        #下载数据
                        download_link = _content['data']['download_link'].replace('\\','')
                        print 'download_link=%s'%download_link
                        req = urllib2.Request(download_link)
                        csv_bytes = urllib2.urlopen(req, timeout = 600).read().decode('ascii', 'ignore')
                        csv_reader = csv.reader(StringIO(csv_bytes))
                        t_online_info_obj = t_online_info(self.t_api_scheduleImp.auth_info['ShopName'],self.t_api_scheduleImp.cnxn)
                        t_online_info_obj.insertWish(csv_reader)

                    self.OneCmdRecoreDict['Status'] = '2'
                    self.OneCmdRecoreDict['ProcessingStatus'] = _content['data']['status']
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
                elif _content['data']['status']  == 'PENDING' or _content['data']['status']  == 'RUNNING' :
                    self.OneCmdRecoreDict['Status'] = '1'
                    self.OneCmdRecoreDict['ProcessingStatus'] = _content['data']['status']
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                    self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)

                else:
                    self.OneCmdRecoreDict['Status'] = '-2'
                    self.OneCmdRecoreDict['ProcessingStatus'] = _content['data']['status']
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
            else: #报错
                    self.OneCmdRecoreDict['Status'] = dict_ret.status_code
                    self.OneCmdRecoreDict['ProcessingStatus'] = _content['code']
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)

    def GetShopSKUInfoV2(self):
        refreshdict = {'ShopName':'','ProductID':[],'record':{}}
        record = {}
        pageurl = ''
        datalist = []

        shopstatus = None
        while True:
            if pageurl == '':
                url_List_all_Products = "https://merchant.wish.com/api/v2/product/multi-get"
                data = {
                    'access_token':self.t_api_scheduleImp.auth_info['access_token'] ,
                    'format': 'json',
                    'limit': '250',
                    'show_rejected': 'true',
                }
                if self.flag == 1:
                    record = self.getSinceV2(data,'Product')
                print 'data=%s' % data
                dict_ret = requests.get(url_List_all_Products, params=data, timeout = 30)
                print '---------------',pageurl
                _content = eval(dict_ret._content)

                if dict_ret.status_code==200 and  _content['code']==0 :
                    # datalist.append(_content['data'])
                    datalist = datalist + _content['data']

                    t_store_configuration_file_obj = t_store_configuration_file(self.db_conn)
                    t_store_configuration_file_obj.update_shopStatus('0',self.t_api_scheduleImp.auth_info['ShopName'])

                    t_online_info_wish_obj = t_online_info_wish(self.db_conn)
                    t_online_info_wish_obj.UpdateWishSNameByShopName(self.t_api_scheduleImp.auth_info['ShopName'],'0')

                    if _content.has_key('paging') and _content['paging'].has_key('next'):
                        pageurl = _content['paging']['next'].replace('\\','')
                    else:
                        self.t_api_scheduleImp.cnxn.commit()
                        self.OneCmdRecoreDict['Status'] = '2'
                        self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                        self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
                        break
                else:
                    shopstatus = self.j_result_code(_content)
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.OneCmdRecoreDict['TransactionID'] = ''
                    self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                    self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)
                    break
            else:
                print '---------------', pageurl
                paging_bytes = None
                try:
                    paging_req = urllib2.Request(pageurl)
                    paging_bytes = urllib2.urlopen(paging_req, timeout=60).read()
                except Exception, ex:
                    datalist = []
                    record = {}
                    self.OneCmdRecoreDict['Status'] = 'Exception'
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.OneCmdRecoreDict['errorinfo'] = '%s  F_EXE_API_WISH except Exception= %s ex=%s  __LINE__=%s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), Exception, ex,sys._getframe().f_lineno)
                    self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
                    break

                if paging_bytes is not None:
                    paging_bytes_dict = eval(paging_bytes)
                    # datalist.append(paging_bytes_dict['data'])
                    datalist = datalist + paging_bytes_dict['data']

                    if paging_bytes_dict.has_key('paging') and paging_bytes_dict['paging'].has_key('next'):
                        if len(paging_bytes_dict['paging']['next']) <= 10 :
                            break
                        else:
                            pageurl = paging_bytes_dict['paging']['next'].replace('\\', '')
                    else:
                        break
                else:
                    break
        # t_store_configuration_file_obj.update_shopStatus(shopstatus, self.t_api_scheduleImp.auth_info['ShopName'])
        if datalist :
            t_online_info_obj = t_online_info(self.t_api_scheduleImp.auth_info['ShopName'],
                                              self.t_api_scheduleImp.cnxn,
                                              self.t_api_scheduleImp.redis_conn)
            refreshdict = t_online_info_obj.insertWishV2(datalist)

            self.t_api_scheduleImp.cnxn.commit()
            self.OneCmdRecoreDict['Status'] = '2'
            self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
            self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
        refreshdict['record'] = record
        return refreshdict

    def getSince(self,data):
        t_online_info_obj = t_online_info(self.t_api_scheduleImp.auth_info['ShopName'],self.t_api_scheduleImp.cnxn)
        Max_ProductLastUpdated = t_online_info_obj.getMax_ProductLastUpdated2()
        get_wish_product_order_updatetime_obj = get_wish_product_order_updatetime(self.t_api_scheduleImp.cnxn,self.t_api_scheduleImp.auth_info['ShopName'])
        end = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        if Max_ProductLastUpdated=='1970-01-01':
            #没找到那就是
            start = None
        else:
            #[最大时间+1s,现在)
            start=strtimeaddseconds(Max_ProductLastUpdated,-600)

            data['since'] = start
            self.OneCmdRecoreDict['cmdtext'] = '[ %s , %s )'%(start,end)
        get_wish_product_order_updatetime_obj.update_time_or_insert(start, end,'Product')

    def getStartAndEnd(self,data):
        t_order_obj = t_order(self.t_api_scheduleImp.auth_info['ShopName'],self.t_api_scheduleImp.cnxn)
        Max_OrderLastUpdated = t_order_obj.getMax_OrderLastUpdated2()
        get_wish_product_order_updatetime_obj = get_wish_product_order_updatetime(self.t_api_scheduleImp.cnxn,self.t_api_scheduleImp.auth_info['ShopName'])
        end = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        if Max_OrderLastUpdated=='1970-01-01':
            #没找到那就是
            start = None
        else:
            #[最大时间+1s,现在)
            start=strtimeaddseconds(Max_OrderLastUpdated,-600)
            end = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            data['since'] = start
            #data['start'] = start
            #data['end'] = end
            self.OneCmdRecoreDict['cmdtext'] = '[ %s , %s )'%(start,end)
        get_wish_product_order_updatetime_obj.update_time_or_insert(start, end,'Order')

    def getSinceV2(self,data,type):
        get_wish_product_order_updatetime_obj = get_wish_product_order_updatetime(self.t_api_scheduleImp.cnxn,self.t_api_scheduleImp.auth_info['ShopName'])
        updatetimeobj = get_wish_product_order_updatetime_obj.get_updatetime(type)
        end = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        if updatetimeobj:
            start = updatetimeobj[1] # 上次更新时间
            # 从上次更新 往前推 8个小时 刷新数据
            ss = (datetime.datetime.strptime(start,'%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=-8)).strftime('%Y-%m-%dT%H:%M:%S')
            data['since'] = ss
            self.OneCmdRecoreDict['cmdtext'] = '[ %s , %s )' % (start, end)
        else:
            if type == 'Order':
                utcnowtemp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
                start = strtimeaddseconds(utcnowtemp, -32 * 86400)
            else:
                start = None
        return {'start':start,'end':end,'type':type}


    def RefreshToken(self):
        params = {
                    'client_id':self.t_api_scheduleImp.auth_info['client_id'],
                    'client_secret':self.t_api_scheduleImp.auth_info['client_secret'],
                    'refresh_token':self.t_api_scheduleImp.auth_info['refresh_token'],
                    'grant_type':'refresh_token' ,
                }
        refresh_token_ret = requests.post('https://merchant.wish.com/api/v2/oauth/refresh_token', params=params, timeout = 10)
        print  'refresh_token_ret=%s'%refresh_token_ret.__dict__
        _content = eval(refresh_token_ret._content.replace(':null,',':0,'))
        access_token = _content['data']['access_token']
        refresh_token = _content['data']['refresh_token']

        cursor =self.t_api_scheduleImp.cnxn.cursor()
        sql_access_token = 'update t_config_online_amazon set V= \'%s\' where Name =\'%s\' and K =\'%s\' '%(access_token,self.OneCmdRecoreDict['ShopName'],'access_token')
        print sql_access_token
        cursor.execute(sql_access_token)
        sql_refresh_token = 'update t_config_online_amazon set V= \'%s\' where Name =\'%s\' and K =\'%s\' '%(refresh_token,self.OneCmdRecoreDict['ShopName'],'refresh_token')
        print sql_refresh_token
        cursor.execute(sql_refresh_token)

        last_refresh_token_time =  datetime.datetime.now()
        sql_insert ='insert into t_config_online_amazon(Name,K,V) values(%s,%s,%s)'
        cursor.execute(sql_insert,(self.OneCmdRecoreDict['ShopName'],'last_refresh_token_time',last_refresh_token_time))
        self.t_api_scheduleImp.cnxn.commit()
        cursor.close()

    def j_result_code(self,_content):
        shopstatus = None
        t_store_configuration_file_obj = t_store_configuration_file(self.db_conn)
        t_online_info_wish_obj = t_online_info_wish(self.db_conn)

        # 刷新一下token  1015 :问令牌过期   4000:权存取 1016:失效
        if _content['code'] == 1001:  # 数据缺失
            shopstatus = 'Missing Parameter'

        if _content['code'] == 1015:
            # self.RefreshToken()
            shopstatus = 'Access Token Expired'

        if _content['code'] == 1016:  # 店铺被关  授权吊销
            shopstatus = 'Access Token Revoked'

        if _content['code'] == 1017:
            shopstatus = 'Authorization Code Expired'

        if _content['code'] == 1018:
            shopstatus = 'Access Token Redeemed'

        if _content['code'] == 4000:
            shopstatus = 'Unauthorized Access'

        if _content['code'] == 9000:
            shopstatus = 'Unknown'

        if _content['code'] == 2000:
            shopstatus = '-1'  # 账户状态异常
            t_store_configuration_file_obj.update_shopStatus(shopstatus, self.t_api_scheduleImp.auth_info['ShopName'])
            t_online_info_wish_obj.UpdateWishSNameByShopName(self.t_api_scheduleImp.auth_info['ShopName'], shopstatus)

        if _content['code'] == 1004:
            shopstatus = 'Product Removed.'

        if _content['code'] == 1028:
            shopstatus = ''

        return shopstatus

    def GetListOrders(self):
        if self.OneCmdRecoreDict['TransactionID'] is None or self.OneCmdRecoreDict['TransactionID'].strip()=='':
            Params_dict = eval(self.OneCmdRecoreDict['Params'].replace("`","'"))
            #import requests
            #url_create = "https://merchant.wish.com/api/v2/product/create-download-job"
            data = {
                'access_token':self.t_api_scheduleImp.auth_info['access_token'] ,
                'format': 'json',
            }
            self.getStartAndEnd(data)
##          if Params_dict.has_key('start') and Params_dict.has_key('end'):
##              data['start'] = Params_dict['start']
##              data['end'] = Params_dict['end']
            print 'data===================================%s'%data
            dict_ret = requests.post(Params_dict['url_create'], params=data, timeout = 30)

            print  dict_ret.__dict__
            print '---------------\n'
            #dict_ret =eval(ret)
            print 'dict_ret=%s'%dict_ret
            print '---------------\n'
            _content = eval(dict_ret._content)

            #刷新一下token  1015 :问令牌过期   4000:权存取
            if  _content['code']== 1015 or _content['code']== 1016:#or _content['code']== 4000  or _content['code']== 1016 or _content['code']== 1017  or _content['code']== 1018  or _content['code']== 9000   :
                # self.RefreshToken()

                self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                self.OneCmdRecoreDict['TransactionID'] = ''
                self.OneCmdRecoreDict['ProcessingStatus'] =_content['code']
                #self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                #self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)
                return
            if dict_ret.status_code==200 and  _content['code']==0 :
                    self.OneCmdRecoreDict['Status'] = '1'
                    self.OneCmdRecoreDict['ProcessingStatus'] = 'SUBMIT'
                    self.OneCmdRecoreDict['ActualBeginTime'] = datetime.datetime.now()
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.OneCmdRecoreDict['TransactionID'] = '{`job_id`:`%s`}'%(_content['data']['job_id'])
                    #self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                    #self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)
            else: #报错
                    self.OneCmdRecoreDict['Status'] = dict_ret.status_code
                    self.OneCmdRecoreDict['ProcessingStatus'] = _content['code']
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    #self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                    #self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)
                    self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
        else:
            TransactionID_dict = eval(self.OneCmdRecoreDict['TransactionID'].replace("`","'"))
            print 'TransactionID_dict=%s'%TransactionID_dict

            Params_dict = eval(self.OneCmdRecoreDict['Params'].replace("`","'"))
            print self.OneCmdRecoreDict['Params']

            data = {
                'access_token':self.t_api_scheduleImp.auth_info['access_token'] ,
                'format': 'json',
                'job_id': TransactionID_dict['job_id'],
            }
            dict_ret = requests.post(Params_dict['url_status'], params=data, timeout = 30)

            #dict_ret =eval(ret)
            #print json.dumps(dict_ret, indent=1)

            print '--------------- dict_ret=%s'%dict_ret

            print '---------------dict_ret.__dict__ =%s'%dict_ret.__dict__

            print '---------------dict_ret._content=%s'%dict_ret._content
            _content = eval(dict_ret._content)
            #刷新一下token  1015 :问令牌过期   4000:权存取
            if  _content['code']== 1015 or _content['code']== 1016:#or _content['code']== 4000  or _content['code']== 1016 or _content['code']== 1017  or _content['code']== 1018  or _content['code']== 9000   :
                # self.RefreshToken()

                self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                self.OneCmdRecoreDict['TransactionID'] = ''
                self.OneCmdRecoreDict['ProcessingStatus'] =_content['code']
                #self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                #self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)
                return
            if dict_ret.status_code  ==200 and  _content['code']==0 :
                if _content['data']['status']  == 'FINISHED' :
                    if _content['data']['total_count'] > 0 and  _content['data'].has_key('download_link'):
                        #下载数据
                        download_link = _content['data']['download_link'].replace('\\','')
                        print 'download_link=%s'%download_link
                        req = urllib2.Request(download_link)
                        csv_bytes = urllib2.urlopen(req, timeout = 600).read().decode('ascii', 'ignore')
                        csv_reader = csv.reader(StringIO(csv_bytes))
                        #for row in csv_reader:
                            #print row
                        t_order_obj = t_order(self.t_api_scheduleImp.auth_info['ShopName'],self.t_api_scheduleImp.cnxn)
                        t_order_obj.insertWish(csv_reader)

                    self.OneCmdRecoreDict['Status'] = '2'
                    self.OneCmdRecoreDict['ProcessingStatus'] = _content['data']['status']
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
                elif _content['data']['status']  == 'PENDING' or _content['data']['status']  == 'RUNNING' :
                    self.OneCmdRecoreDict['Status'] = '1'
                    self.OneCmdRecoreDict['ProcessingStatus'] = _content['data']['status']
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    #self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                    #self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)

                else:
                    self.OneCmdRecoreDict['Status'] = '-2'
                    self.OneCmdRecoreDict['ProcessingStatus'] = _content['data']['status']
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
            else: #报错
                    print '--------------------dict_ret.status_code=%s'%(dict_ret.status_code)
                    self.OneCmdRecoreDict['Status'] = '-3'
                    self.OneCmdRecoreDict['ProcessingStatus'] = dict_ret.status_code
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    #self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                    #self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)
                    #self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)

    def GetListOrders2(self):
        refreshdict = {'ShopName': '', 'ProductID': [], 'record': {}}

        record = {}
        pageurl = ''
        prolist = []

        shopstatus = None
        while True:
            if pageurl == '':
                print '--------------' + pageurl
                url_List_all_Orders = "https://merchant.wish.com/api/v2/order/multi-get"

                data = {
                    'access_token':self.t_api_scheduleImp.auth_info['access_token'] ,
                    'format': 'json',
                    'limit': '500',
                    "fbw_included": "true",
                }
                if self.flag == 1:
                    record = self.getSinceV2(data,'Order')
                print 'data=%s'%data
                dict_ret = requests.get(url_List_all_Orders, params=data,timeout=30)

                _content = eval(dict_ret._content)
                if dict_ret.status_code==200 and  _content['code']==0 :
                    prolist = prolist + _content['data']

                    t_store_configuration_file_obj = t_store_configuration_file(self.db_conn)
                    t_store_configuration_file_obj.update_shopStatus('0', self.t_api_scheduleImp.auth_info['ShopName'])

                    t_online_info_wish_obj = t_online_info_wish(self.db_conn)
                    t_online_info_wish_obj.UpdateWishSNameByShopName(self.t_api_scheduleImp.auth_info['ShopName'], '0')

                    if _content.has_key('paging') and _content['paging'].has_key('next'):
                        pageurl = _content['paging']['next'].replace('\\','')
                    else:
                        self.t_api_scheduleImp.cnxn.commit()
                        self.OneCmdRecoreDict['Status'] = '2'
                        self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                        self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
                        break
                else:
                    shopstatus = self.j_result_code(_content)
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.OneCmdRecoreDict['TransactionID'] = ''
                    self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                    self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)
                    break
            else:
                paging_bytes = None
                print '--------------'+pageurl
                try:
                    paging_req = urllib2.Request(pageurl)
                    paging_bytes = urllib2.urlopen(paging_req, timeout = 60).read()
                except Exception,ex:
                    prolist = []
                    record = {}
                    self.OneCmdRecoreDict['Status'] = 'Exception'
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.OneCmdRecoreDict['errorinfo'] = '%s  F_EXE_API_WISH except Exception= %s ex=%s  __LINE__=%s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), Exception, ex,sys._getframe().f_lineno)
                    self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
                    break

                if paging_bytes is not None:
                    paging_bytes_dict = eval(paging_bytes)
                    prolist = prolist + paging_bytes_dict['data']

                    if paging_bytes_dict.has_key('paging') and paging_bytes_dict['paging'].has_key('next'):
                        if len(paging_bytes_dict['paging']['next']) <= 10 :
                            break
                        else:
                            pageurl = paging_bytes_dict['paging']['next'].replace('\\','')
                    else:
                        break
                else:
                    break

        if prolist:
            t_order_obj = t_order(self.t_api_scheduleImp.auth_info['ShopName'],self.t_api_scheduleImp.cnxn)
            refreshdict = t_order_obj.insertWishV2(prolist)

            self.t_api_scheduleImp.cnxn.commit()
            self.OneCmdRecoreDict['Status'] = '2'
            self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
            self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
        refreshdict['record'] = record
        return refreshdict
