# -*- coding: utf-8 -*-

from brick.db.dbconnect import execute_db


class t_config_online_joom():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def getauthByShopName(self, ShopName):
        shocur = self.db_conn.cursor()
        sql = "SELECT IP, `ShopName`, K, V FROM t_config_online_joom WHERE `ShopName`='%s';" % (ShopName,)
        shocur.execute(sql)
        t_config_online_joom_objs = shocur.fetchall()
        shocur.close()
        auth_info = {}
        for t_config_online_joom_obj in t_config_online_joom_objs:
            auth_info['IP'] = t_config_online_joom_obj[0]
            auth_info['ShopName'] = t_config_online_joom_obj[1]
            k = t_config_online_joom_obj[2]
            v = t_config_online_joom_obj[3]
            auth_info[k] = v
        return auth_info

    def getalljoomauth(self):
        sql = "SELECT IP, `ShopName`, K, V FROM t_config_online_joom;"
        res = execute_db(sql, self.db_conn, 'select')
        auth_infos = dict()
        for i in res:
            if auth_infos.get(i['ShopName']):
                auth_infos[i['ShopName']]['IP'] = i['IP']
                auth_infos[i['ShopName']][i['K']] = i['V']
            else:
                auth_infos[i['ShopName']] = dict()
                auth_infos[i['ShopName']]['ShopName'] = i['ShopName']
        auth_info_list = list()
        for i in auth_infos.keys():
            auth_info_list.append(auth_infos[i])
        return auth_info_list
