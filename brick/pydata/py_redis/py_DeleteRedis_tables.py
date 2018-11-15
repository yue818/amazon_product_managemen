from py_SynRedis_pub import py_SynRedis_pub

if __name__ == "__main__":
    py = py_SynRedis_pub()
    listTable = ['CG_StockInM','CG_StockOrderM','CG_StockOrderM_1','CG_StockOrderD','CG_StockInD']

    for tableName in listTable:
        if len(tableName) > 0:
            print(tableName)
            py.DelHashKeys(tableName)