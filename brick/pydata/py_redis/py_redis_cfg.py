#  _*_ coding:utf-8 _*_
#  _*_ codeding by dj _*_
#  _*_ date 20180126 _*_
#  _*_ 功能：通过海鹰API接口获取数据配置文件 _*_


py_redis_cfg = {
    'B_Goods': {
        'NID': 0,
        'GoodsCode': 3,
        'GoodsName': 4,
        'SKU': 6,
        'BarCode': 7,
        'FitCode': 8,
        'Class': 11,
        'Model': 12,
        'Unit': 13,
        'SalePrice': 18,
        'CostPrice': 19,
        'Weight': 22,
        'Used': 27,
        'SupplierID': 33,
        'CreateDate': 38,
        'SalerName': 40,
        'SellDays': 42,
        'DevDate': 46,
        'SalerName2': 47,
        'PackageCount': 52,
        'StockDays': 54,
        'Purchaser': 56,
        'LinkUrl': 57,
        'LinkUrl2': 58,
        'LinkUrl3': 59,
        'StockMinAmount': 60,
        'MinPrice': 61,
        'LinkUrl4': 92,
        'LinkUrl5': 93,
        'LinkUrl6': 94,
        'ifexsistkey':'y',
        'key': 6
    },
    'B_GoodsSKU': {
        'NID': 0,
        'GoodsID': 1,
        'SKU': 2,
        'property1': 3,
        'property2': 4,
        'property3': 5,
        'SKUName': 6,
        'Weight': 14,
        'CostPrice': 15,
        'MaxNum': 17,
        'MinNum': 18,
        'GoodsSKUStatus': 19,
        'ChangeStatusTime': 20,
        'ModelNum': 23,
        'linkurl': 25,
        'ifexsistkey': 'y',
        'key': 2
    }
    'KC_CurrentStock':{
        'NID': 0,
        'StoreID': 1,
        'GoodsID': 2,
        'GoodsSKUID': 3,
        'Number': 4,
        'Money': 5,
        'Price': 6,
        'ReservationNum': 7,
        'OutCode': 8,
        'WarningCats': 9,
        'KcMaxNum': 11,
        'KcMinNum': 12,
        'SellCount1': 13,
        'SellCount2': 14,
        'SellCount3': 15,
        'SellDays': 16,
        'StockDays': 17,
        'SellCount': 18,
        'ifexsistkey': 'n',
        'getkey': ''
    }
}


