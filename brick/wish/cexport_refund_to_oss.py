# -*- coding: utf-8 -*-
import sys
from brick.table.t_order_refunded import *
from brick.table.t_refundreason_table import *
from brick.function.concat_tuples_to_list import *
from brick.function.cexporcsv import *
from django.contrib import messages
import traceback
import datetime
import logging
from django.http import request

#ossinfo的定义
#表头的定义
# PREFIX = 'http://'
# ACCESS_KEY_ID= 'LTAIH6IHuMj6Fq2h'
# ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
# ENDPOINT = 'vpc100-oss-cn-shanghai.aliyuncs.com'
# ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
# BUCKETNAME_XLS  = 'fancyqube-download'


ossinfo = {'ACCESS_KEY_ID':'LTAIH6IHuMj6Fq2h', 'ACCESS_KEY_SECRET':'N5eWsbw8qBkMfPREkgF2JnTsDASelM', 'ENDPOINT_OUT': 'oss-cn-shanghai.aliyuncs.com', 'BUCKETNAME_XLS': 'fancyqube-download'}
header1 = [u"店铺单号", u"对应销售单号", u"退款类型", u"主表备注", u"ShopSKU",u'商品SKU', u"SKU", u"数量", u"金额", u"退款日期", u"退款原因", u"店铺名", u"订单日期", u"装运日期"]
header2 = [u"退款原因", u"退款类型", u"售后类型", u"重寄售后原因"]
csvheaders = [u"店铺单号", u"对应销售单号", u"退款类型", u"主表备注", u"ShopSKU",u'商品SKU', u"SKU", u"数量", u"金额", u"退款日期", u"退款原因", u"店铺名", u"订单日期", u"装运日期",u"退款类型", u"售后类型", u"重寄售后原因"]
condkey = u"退款原因"


#params =  {db_conn, StrTime, EndTime}
#result = {errorcode, errortext,path}
class cexport_refund_to_oss():
    def __init__(self):
        pass

    # params合法法校验
    # 00:00
    def isvalid(self,params):
        result = {}
        st = datetime.datetime.strptime(params['StrTime'], "%Y-%m-%d")
        ed = datetime.datetime.strptime(params['EndTime'], "%Y-%m-%d")

        daycount = (ed-st).days
        if daycount <= 60 and daycount >= 0:
            return True
        else:
            messages.error(request, u'Please enter the correct content!')
            print  '%s is not invalid' % params
            return False

	#params =  {db_conn, StrTime, EndTime}
	#result = {errorcode, errortext,path}
    def fexport_refund_to_oss(self,params):
        #logging.info(params)
        print params
        result = {}
        timeparams = {'StrTime':params['StrTime'], 'EndTime':params['EndTime']}
        if not self.isvalid(timeparams):
            return result
        try:
            t_refundreason_table_obj = t_refundreason_table(params['db_conn'])
            RefundReasonData = t_refundreason_table_obj.queryRefundReason()
            if RefundReasonData['errorcode'] <> 0:
                result = {'errorcode':-1, 'errortext':'not find RefundReasonData'}
                return result
            t_order_refund_obj = t_order_refunded(params['db_conn'])
            RefundData = t_order_refund_obj.queryRefund(params['StrTime'], params['EndTime'])

            if not RefundData['datasrcset']:
                result = {'errorcode': -1, 'errortext': 'not find RefundData'}
                return result
            concat_tuples_to_list_obj = concat_tuples_to_list()
            tuples = {'tuple1':RefundData['datasrcset'], 'tuple2':RefundReasonData['datasrcset']}
            headers = {'header1':header1, 'header2':header2}
            RefundDataAndReason = concat_tuples_to_list_obj.concat_datasrcset(tuples, headers,condkey)

            if RefundDataAndReason['errorcode'] <> 0:
                result = {'errorcode':-1, 'errortext':'Unsuccessfully get RefundReasonData'}
                return result
            cexporcsv_obj = cexporcsv()
            timeparams = {'StrTime': params['StrTime'], 'EndTime': params['EndTime']}
            print 'x', timeparams
            ossresult = cexporcsv_obj.export_to_oss(csvheader=csvheaders, datasrcset=RefundDataAndReason['datasrcset'], ossinfo=ossinfo, urlload='refund',timeParams=timeparams, username=params['UserName'])

            if ossresult['errorcode'] <> 0:
                result = {'errorcode': -1, 'errortext':'Unsuccessfully in export_to_oss'}
                return result
            result['osspath'] = ossresult['osspath']
            result['errorcode'] = 0
            logging.info('successfully result = %s'%result)
            print 'OUTPUT::result', result
            return result
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result




 

