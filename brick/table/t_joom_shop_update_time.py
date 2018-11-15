#!/usr/bin/python
# -*- coding: utf-8 -*-


class t_joom_shop_update_time():
    def __init__(self, db_coon, shopname):
        self.db_coon = db_coon
        self.shopname = shopname

    def get_updatetime(self, stype):
        procur = self.db_coon.cursor()
        sql = "SELECT lastupdatetime, nowupdatetime FROM t_joom_shop_update_time WHERE stype=%s AND shopname=%s ;"
        procur.execute(sql, (stype, self.shopname,))
        obj = procur.fetchone()
        procur.close()
        return obj

    def update_time_or_insert(self, lastupdatetime, nowupdatetime, stype):
        updcur = self.db_coon.cursor()
        sql = "INSERT INTO t_joom_shop_update_time SET lastupdatetime=%s," \
            "nowupdatetime=%s, stype=%s, shopname=%s " \
            "ON DUPLICATE KEY UPDATE lastupdatetime=%s, nowupdatetime=%s;"
        updcur.execute(sql, (lastupdatetime, nowupdatetime, stype, self.shopname, lastupdatetime, nowupdatetime))
        updcur.execute("commit;")
        updcur.close()
