# -*- coding: utf-8 -*-

class t_templet_wish_upload_result():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    #
    def update_result_status(self, resultstatus, errormessage, resultid ):
        updcur = self.db_conn.cursor()
        updcur.execute("update t_templet_wish_upload_result set Status = %s,ErrorMessage = %s where id = %s ;", (resultstatus, errormessage, resultid))
        updcur.execute('commit')
        updcur.close()

    def get_count_num(self,parentsku,shopname):
        parcur = self.db_conn.cursor()
        parcur.execute("select count(ParentSKU) from t_templet_wish_upload_result WHERE "
                       "ParentSKU = %s and ShopName = %s ; ",(parentsku,shopname))  # and Status = 'SUCCESS'
        obj = parcur.fetchone()
        parcur.close()
        num = 0
        if obj:
            num = obj[0]
        return num
