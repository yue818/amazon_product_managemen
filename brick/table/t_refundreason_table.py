# -*- coding: utf-8 -*-
import sys
import traceback


class t_refundreason_table():
	def __init__(self,db_conn):
		self.db_conn = db_conn

	def queryRefundReason(self,):
		result = {}
		try:
			cursor = self.db_conn.cursor()
			cursor.execute("select refundreason,status1,status2,reason from t_refundreason_table;")
			result['datasrcset'] = cursor.fetchall()
			result['errorcode']  = 0
			cursor.close()
			return result
		except Exception, ex:
			result['errorcode'] = -1
			print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
			return result
