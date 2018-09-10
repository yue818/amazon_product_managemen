# -*- coding: utf-8 -*-
import sys, os, base64, datetime, hashlib, hmac, urllib2, json
import pyodbc
import pymssql
import time, traceback
from brick.table.t_order_amazon_india_su import *
from brick.table.t_order_track_info_amazon_india_siu import *
import logging
import logging.handlers

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='/tmp/api_order_apply_trackno_amazon_india.log',
                    filemode='a')
logging.handlers.RotatingFileHandler('/tmp/api_order_apply_trackno_amazon_india.log',
                                     maxBytes=10 * 1024 * 1024,
                                     backupCount=5)

reload(sys)
sys.setdefaultencoding("utf-8")

def get_pyOrderNumber(AmazonOrderId):
    pyOrderNumber = ''
    #py_cnxn = pyodbc.connect('DRIVER={SQLServer};SERVER=122.226.216.10;port=18793;DATABASE=ShopElf;UID=sa;PWD=$%^AcB2@9!@#')
    py_cnxn = pymssql.connect(host='122.226.216.10',
                              user='fancyqube',
                              password='K120Esc1',
                              database='ShopElf',
                              port='18793')
    py_cursor = py_cnxn.cursor()
    sql = "SELECT NID FROM p_trade WHERE ADDRESSOWNER = 'amazon11' and TRANSACTIONID = '%s'" % AmazonOrderId
    # py_cursor.execute("SELECT NID "
    #                   "FROM p_trade "
    #                   "WHERE ADDRESSOWNER='amazon11' "
    #                   "and TRANSACTIONID = ?;",
    #                   (AmazonOrderId,))
    py_cursor.execute(sql)
    nid = py_cursor.fetchone()
    if nid:
        pyOrderNumber = nid[0]
    py_cursor.close()
    py_cnxn.close()
    return pyOrderNumber

class AMZTrackApiSchedule():
    def __init__(self, cnxn):
        self.cnxn = cnxn

    def get_response_by_url_and_params(self, url, params):
        req = urllib2.Request(url=url)
        req.add_header("Content-Type", "application/json")
        response = urllib2.urlopen(req, data=params, timeout=30)
        return response

    def hash_md5(self, signdata):
        m = hashlib.md5()
        m.update(signdata)
        psw = m.hexdigest()
        signature = psw.upper()
        return signature

    def construct_req_params(self, params, tkNum):
        request_dict = eval(params)
        timeStamp = int(time.time() * 1000)
        appKey = '6dd8a3d04db5430c9ab1eebe6373b82d'
        request_dict['RequestName'] = 'getLables'
        request_dict['TimeStamp'] = timeStamp
        # 'TrackNumber':['1521510657882'],'ImageType':'PDF'
        request_dict['Content'] = '{"TrackNumber":["' + tkNum + '"],"ImageType":"URL"}'
        signatureData = {"AppId": request_dict['AppId'], "TimeStamp": timeStamp}
        keyset = sorted(signatureData.keys())
        signdata = ''
        for i in range(0, len(keyset)):
            signdata = signdata + keyset[i]  + '=' + str(signatureData[keyset[i]])
        signdata += 'Key=' + appKey
        request_dict['Sign'] = self.hash_md5(signdata)
        return json.dumps(request_dict)

    def start_apply(self, params):
        logging.debug('\n\n\n\n0.params %s' % params)
        result_dic = {'errorcode': 0, 'errortext': '', 'params': params, 'result': ''}
        try:
            rt_data = params.split('||')
            param_split = rt_data[0]
            url = rt_data[1]
            order_id = rt_data[2]
            #result_dic['params'] = url +'||' + order_id
            dealResult = 'Failed'

            if param_split is not None:
                    t_order_amazon_india_obj = t_order_amazon_india(self.cnxn)
                    AmazonOrderId = t_order_amazon_india_obj.select_AmazonOrderId(order_id)
                    print '\n2.AmazonOrderId result is: %s' %AmazonOrderId
                    logging.debug('\n2.AmazonOrderId result is: %s' % AmazonOrderId)
                    respons = self.get_response_by_url_and_params(url, str(param_split))
                    response_read = respons.read()
                    response_json = json.loads(response_read)
                    print '\n3.json file response_json is:\n'
                    print u'%s' % response_json
                    logging.debug('\n3.json file response_json is: %s' % response_json)
                    is_data_true = 0
                    tkNum = ''
                    applyTracking = 1

                    if response_json['VerifyCode'] == '00':
                        t_order_track_info_amazon_india_imp = t_order_track_info_amazon_india(self.cnxn)
                        if response_json['ResultCode'] == '0000':
                            dealResult = 'Success'
                        else:
                            applyTracking = '""'
                        print '\n4.response_json[Data] is: %s' %response_json['Data']
                        logging.debug('\n4.response_json[Data] is: %s' % response_json['Data'])
                        if len(response_json['Data']) > 0:
                            request_dict = eval(param_split)
                            track_service = request_dict['Content']['ServiceCode']
                            is_data_true = 1
                            tkNum = response_json['Data']['TrackNumber']
                            upTime = datetime.datetime.now()
                            t_order_track_info_amazon_india_imp.insert_trackNumber(AmazonOrderId,tkNum,'gati',track_service,upTime)
                    else:
                        pass

                    print '\n6.is_data_true is: %s'%is_data_true
                    logging.debug('\n6.is_data_true is: %s' % response_json['Data'])
                    if is_data_true == 1:
                        params_struct = self.construct_req_params(param_split, tkNum)
                        respons = self.get_response_by_url_and_params(url, params_struct)
                        respons_dict = json.loads(respons.read())
                        print '\n7.respons_dict is \n%s'%respons_dict
                        logging.debug('\n7.respons_dict is \n%s' % respons_dict)
                        LableData = respons_dict['Data']['Labels'][0]['LableData']
                        upTime = datetime.datetime.now()
                        t_order_track_info_amazon_india_imp = t_order_track_info_amazon_india(self.cnxn)
                        t_order_track_info_amazon_india_imp.update_LableData(LableData,upTime,tkNum)
                    upTime = datetime.datetime.now()
                    pyOrderNumber = get_pyOrderNumber(AmazonOrderId)
                    print '\n9.pyOrderNumber is  %s' %pyOrderNumber
                    logging.debug('\n9.pyOrderNumber is  %s' % pyOrderNumber)
                    t_order_amazon_india_obj.update_PYNo(dealResult, upTime,pyOrderNumber,response_json['ResultMsg'],AmazonOrderId,applyTracking)
                    result_dic['result'] = 'AmazonOrderId = ' + str(AmazonOrderId)  + ';' + 'response_json =' + u'%s' % response_json
            else:
                result_dic['result'] = 'params is None '

            time.sleep(1)
        except Exception, ex:
            result_dic['errorcode'] = -1
            print '************%s*************' % ex
            result_dic['errortext'] = '%s:%s' % (Exception, ex)
            rt_data = params.split('||')
            order_id = rt_data[2]
            t_order_amazon_india_obj = t_order_amazon_india(self.cnxn)
            AmazonOrderId = t_order_amazon_india_obj.select_AmazonOrderId(order_id)
            t_order_amazon_india_obj = t_order_amazon_india(self.cnxn)
            t_order_amazon_india_obj.update_when_fail(str(ex).replace("'", '`'), datetime.datetime.now(), AmazonOrderId, '')
            logging.error('\nERROR %s:%s' % (Exception, ex))
            traceback.print_exc(file=open('/tmp/api_order_apply_trackno_amazon_india.log', 'a'))
            time.sleep(1)


        return result_dic


