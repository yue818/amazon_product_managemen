# -*- coding: utf-8 -*-


class t_templet_joom_upload_result():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def update_result_status(self, resultstatus, errormessage, resultid):
        updcur = self.db_conn.cursor()
        sql = "UPDATE t_templet_joom_upload_result SET Status=%s, ErrorMessage=%s WHERE id=%s;"
        updcur.execute(sql, (resultstatus, errormessage, resultid))
        updcur.execute('commit')
        updcur.close()

    def get_count_num(self, parentsku):
        parcur = self.db_conn.cursor()
        sql = "SELECT COUNT(ParentSKU) FROM t_templet_joom_upload_result WHERE ParentSKU=%s;"
        parcur.execute(sql, (parentsku,))
        obj = parcur.fetchone()
        parcur.close()
        num = 0
        if obj:
            num = obj[0]
        return num
