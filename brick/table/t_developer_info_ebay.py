# -*- coding: utf-8 -*-

import traceback


class t_developer_info_ebay():

	def __init__(self,db_conn):
		self.db_conn = db_conn

	def queryDeveloperEbay(self,appID):
		result = {}
		try:
			cursor = self.db_conn.cursor()
			sql = "select deviceID, certID, runame,runIP from t_developer_info_ebay where appID = %s"
			cursor.execute(sql,(appID,))
			result['datasrcset'] = cursor.fetchone()
			result['errorcode']  = 0
			cursor.close()
			return result
		except Exception, ex:
			result['errorcode'] = -1
			print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
			return result



