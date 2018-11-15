# coding=utf-8


from skuapp.table.t_product_price_check_recycle import *

class t_product_price_check_recycle_Admin(object):
    list_display=('id','GoodsSKU','RecycleStaffName','RecycleTime','SQStaffName','SQTime',
                  'XGStaffName','XGTime','Mstatus','LQStaffName','LQTime','OldPrice','NowPrice',
                  'OldSupplier','OldSupplierURL','NewSupplier','NewSupplierURL','remarks',
                  'XGcontext','remarks2')   #指定要显示的字段
