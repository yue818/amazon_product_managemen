# -*- coding: utf-8 -*-
import sys
import oss2
from datetime import datetime
import csv
import traceback
import logging
import pandas as pd
import os
import random



PREFIX = 'http://'

class cexporcsv():
	# datasrcset 是一个列表
	# csvheader 也是一个列表
    # ossinfo ={ACCESS_KEY_ID,ACCESS_KEY_SECRET，ENDPOINT，BUCKETNAME_XLS}
	# result = { 'errorcode':0 , 'osspath':osspath}
	def export_to_oss(self,datasrcset,csvheader,ossinfo, urlload, timeParams, username):
		result = {}
		try:
			if not datasrcset:
				result['errorcode'] = -1
				result['errortext'] = 'the resultset %s is not exists' % datasrcset
				return result
			if timeParams:
				osspath = username+'_'+timeParams['StrTime']+'_'+timeParams['EndTime']+'_'+datetime.now().strftime('%Y%m%d%H%M%S')+'_'+str(random.randint(0, 99))+ '.csv'
			else:
				osspath = datetime.now().strftime('%Y%m%d%H%M%S') + '_' + str(random.randint(0, 99)) + '.csv'
			csvfile = pd.DataFrame(columns=csvheader, data=datasrcset)
			try:
				csvfile.to_csv(osspath, encoding = "gbk")
			except:
				csvfile.to_csv(osspath)
			print 'osspath',osspath
			if os.path.exists(osspath):
				auth = oss2.Auth(ossinfo['ACCESS_KEY_ID'], ossinfo['ACCESS_KEY_SECRET'])
				bucket = oss2.Bucket(auth, ossinfo['ENDPOINT_OUT'], ossinfo['BUCKETNAME_XLS'])
				if urlload:

					bucket.put_object('%s/%s' %(urlload,osspath), open(osspath))
					result['osspath'] = PREFIX + ossinfo['BUCKETNAME_XLS'] + '.' + ossinfo['ENDPOINT_OUT'] + '/'+urlload+'/' + osspath
					print 'result[osspath]', result['osspath']
				else:
					bucket.put_object('uploadurl/%s' % (urlload, osspath), open(osspath))
					result['osspath'] = PREFIX + ossinfo['BUCKETNAME_XLS'] + '.' + ossinfo['ENDPOINT_OUT'] + '/uploadurl/' + osspath
				# 只保有oss上传文件
				os.remove(osspath)
				result['errorcode'] = 0
				return result
			else:
				result['errorcode'] = -1
				result['errortext'] = 'no such location file:%s'%file
				logging.error('no such location file')
				return result
		except Exception, ex:
			result['errorcode'] = -1
			result['errortext'] = '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
			return result
