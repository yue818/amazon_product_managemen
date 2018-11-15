# -*- coding: utf-8 -*-
import traceback



class t_config_store_ebay():

	def __init__(self,db_conn):
		self.db_conn = db_conn

	def update_token(self, params):
		result = {}
		try:
			cursor = self.db_conn.cursor()
			sql = "update t_config_store_ebay set token = %s,tokenExpireTime = %s where id = %s"
			cursor.execute(sql, (params['token'], params['tokenExpireTime'], params['id'],))
			cursor.execute('commit;')
			result['errorcode'] = 0
			cursor.close()
			return result
		except Exception, ex:
			result['errorcode'] = -1
			print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
			return result


	def queryConfigEbay(self,id):
		result = {}
		try:
			cursor = self.db_conn.cursor()
			sql = "select accountID, accountPassword, appID from t_config_store_ebay where id = %s"
			cursor.execute(sql,(id,))
			result['datasrcset'] = cursor.fetchone()
			result['errorcode']  = 0
			cursor.close()
			return result
		except Exception, ex:
			result['errorcode'] = -1
			print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
			return result

	def update_refresh_token(self,params):
		result = {}
		try:
			cursor = self.db_conn.cursor()
			sql = "update t_config_store_ebay set refresh_token = %s,refresh__time = %s, refresh_token_expires_in=%s where id = %s"
			cursor.execute(sql,(params['refresh_token'], params['refresh__time'], params['refresh_token_expires_in'],params['id']))
			cursor.execute('commit;')
			result['errorcode'] = 0
			cursor.close()
			return result
		except Exception, ex:
			result['errorcode'] = -1
			print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
			return result






