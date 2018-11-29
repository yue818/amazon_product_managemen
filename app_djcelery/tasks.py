# coding=utf-8


from app_djcelery.celery import app
from my_tools.operation import operation
from app_djcelery.models import Add
from Project.settings import *


@app.task
def mix_opration(param):
    """
    混合运算，两数之和 乘 两数之差
    参数：{'x':, 'y':}， 两个数字组成的字典
    返回值：计算结果
    """
    time.sleep(3)
    op = operation(param)
    add_result = op.add_op()
    sub_result = op.sub_op()

    new_param = {'x':add_result, 'y':sub_result}
    new_op = operation(new_param)
    result = new_op.mul_op()
    return result


@app.task
def only_add(x, y):
    time.sleep(1)
    return x + y

@app.task
def hello():
    time.sleep(1)
    return 'hello'

@app.task
def timing_task(param):
    """定时任务"""
    x = param['x']
    y = param['y']
    result = mix_opration.delay(param)
    dd = Add(task_id=result.id, first=x, second=y, log_date=datetime.datetime.now())
    dd.save()

@app.task
def timing_multitasking():
    for i in range(400):
        only_add.delay(i, 0)

@app.task
def print_hello():
    for i in range(400):
        hello.delay()



from brick.wish.CreateOnlineinfoTask import CreateOnlineinfoTask
from brick.wish.ShopOnlineInfo import F_EXE_SHOP_ONLINE_INFO, ShopOnlineInfo
from django.db import connection
from django.core.cache import cache

import redis
#这里替换为连接的实例host和port
host = 'r-uf6206e9df36e854.redis.rds.aliyuncs.com'
port = 6379
#这里替换为实例password
pwd = 'K120Esc1'
redis_conn = redis.StrictRedis(host=host, port=port, password=pwd)

@app.task
def show_wish_screenshot(*args):
    from skuapp.table.t_config_mstsc import t_config_mstsc
    from skuapp.public.producer import Center
    import os,sys,random
    #IP_objs=t_config_mstsc.objects.filter(platformName='Wish').values_list('IP')
    #for IP_obj in IP_objs :
    screenshot = Center()
    if len(args)>0:
        IP_obj=args[0]
        sec=args[1]
        print IP_obj, type(IP_obj), sec
        screenshot.callback('wish_screenshot.exe %s'%str(sec), str(IP_obj))
        print "%s will start wish_screenshot.exe after %s------Manual" % (IP_obj, sec)
        screenshot.closechannel()
    else:
        IP_objs=t_config_mstsc.objects.filter(PlatformName='Wish').values_list('IP')
        for IP_obj in IP_objs :
            sec = random.randint(0, 7200)
            print IP_obj,type(IP_obj),sec
            screenshot.callback('wish_screenshot.exe %s' % str(sec), str(IP_obj[0]))
            print "%s will start wish_screenshot.exe after %s------automatic" % (IP_obj[0], sec)
        screenshot.closechannel()

@app.task
def show_wish_pb(*args):
    from skuapp.table.t_config_mstsc import t_config_mstsc
    from skuapp.public.producer import Center
    import os, sys, random
    # IP_objs=t_config_mstsc.objects.filter(platformName='Wish').values_list('IP')
    # for IP_obj in IP_objs :
    screenshot = Center()
    if len(args) > 0:
        IP_obj = args[0]
        sec = args[1]
        print IP_obj, type(IP_obj), sec
        screenshot.callback('wish_pb.exe %s' % str(sec), str(IP_obj))
        print "%s will start wish_pb.exe after %s------Manual" % (IP_obj, sec)
        screenshot.closechannel()
    else:
        IP_objs = t_config_mstsc.objects.filter(PlatformName='Wish').values_list('IP')
        for IP_obj in IP_objs:
            sec = random.randint(0, 7200)
            print IP_obj, type(IP_obj), sec
            screenshot.callback('wish_pb.exe %s' % str(sec), str(IP_obj[0]))
            print "%s will start wish_pb.exe after %s------automatic" % (IP_obj[0], sec)
        screenshot.closechannel()

@app.task
def show_wish_honor(*args):
    from skuapp.table.t_config_mstsc import t_config_mstsc
    from skuapp.public.producer import Center
    import os, sys, random
    screenshot = Center()
    if len(args) > 0:
        IP_obj = args[0]
        sec = args[1]
        print "%s will start wish_honor.exe after %s------Manual" % (IP_obj, sec)
        screenshot.callback('wish_honor.exe %s' % str(sec), str(IP_obj))
        screenshot.closechannel()
    else:
        IP_objs = t_config_mstsc.objects.filter(PlatformName='Wish').values_list('IP')
        for IP_obj in IP_objs:
            sec = random.randint(0, 7200)
            print IP_obj, type(IP_obj), sec
            screenshot.callback('wish_honor.exe %s' % str(sec), str(IP_obj[0]))
            print "%s will start wish_honor.exe after %s------automatic" % (IP_obj[0], sec)
        screenshot.closechannel()

@app.task
def create_online_info_task():
    print '111111111111111111111111111111111111111'
    CreateOnlineinfoTask_obj = CreateOnlineinfoTask(connection)
    print '222222222222222222222222222222222222222'
    # CreateOnlineinfoTask_obj.CreateTasks()
    OneCmdRecoreDict_list = CreateOnlineinfoTask_obj.GetTasksV2()
    print '3333333333333333333333333333333333333333'
    # return OneCmdRecoreDict_list

    for OneCmdRecoreDict in OneCmdRecoreDict_list:
        F_EXE_SHOP_ONLINE_INFO.delay(connection, OneCmdRecoreDict, 1)


from brick.wish.CreateOrderTask import CreateOrderTask

@app.task
def create_order_task():
    CreateOrderTask_obj = CreateOrderTask(connection)
    # CreateOrderTask_obj.CreateTasks()
    OneCmdRecoreDict_list = CreateOrderTask_obj.GetTasksV2()
    # return OneCmdRecoreDict_list
    print 'list_length==============%s' % len(OneCmdRecoreDict_list)
    for OneCmdRecoreDict in OneCmdRecoreDict_list:
        F_EXE_SHOP_ONLINE_INFO.delay(connection, OneCmdRecoreDict, 1)



from brick.wish.cexport_refund_to_oss import *
from brick.db import dbconnect
@app.task
def CexportRefundCSVTask(params):
    # db_conn = dbconnect.run({})['db_conn']
    # print db_conn
    param = {'db_conn':connection, 'StrTime': params['StrTime'], 'EndTime': params['EndTime'], 'UserName':params['UserName']}
    cexport_refund_to_oss_obj = cexport_refund_to_oss()
    # cexport_refund_to_oss_obj.fexport_refund_to_oss(params)
    cexport_refund_to_oss_obj.fexport_refund_to_oss(param)


@app.task
def wish_product_infomation():
    from brick.wish.create_order_onlineinfo_task import create_order_onlineinfo_task
    from brick.wish.wishlisting.refresh_listing_fbw_flag_api import refresh_shop_fbw
    Task_obj = create_order_onlineinfo_task(connection)
    objs = Task_obj.Get_order_online_info_data()
    for obj in objs:
        F_EXE_SHOP_ONLINE_INFO.delay(connection, obj, 1)
        # 下面是刷新该店铺中fbw数据的
        obj['CMDID'] = 'FBWInfo'
        wish_fbw_product.delay(obj)

# fbw数据刷新
@app.task
def wish_fbw_product(obj):
    from brick.wish.wishlisting.refresh_listing_fbw_flag_api import refresh_shop_fbw
    refresh_shop_fbw(obj)



from django.db import connection
from brick.ebay.read_excel import read_excel
@app.task
def ebay_open(file_obj, now_time, first_name):
    """eBay采集箱解析Excel任务"""
    read_excel(file_obj, connection, first_name, now_time)
from brick.table.updateto_t_product_b_goods import *
from brick.db import dbconnect
@app.task
def updateto_t_product_b_goods_celery(MainSKU):
    db_conn = dbconnect.run({})['db_conn']
    updateto_t_product_b_goods_obj = updateto_t_product_b_goods(db_conn)
    updateto_t_product_b_goods_obj.updateMainSKU(MainSKU)


@app.task
def product_registration_form_excel_task(paramlist,user_name):
    import re,os
    from Project.settings import BUCKETNAME_DOWNLOAD,MEDIA_ROOT
    from pyapp.models import b_goods as py_b_goods
    from brick.public.generate_excel import generate_excel
    from brick.public.create_dir import mkdir_p
    from brick.public.upload_to_oss import upload_to_oss
    from skuapp.table.t_download_info import t_download_info
    from datetime import datetime as datime

    path = MEDIA_ROOT + 'download_xls/' + user_name
    mkdir_p(MEDIA_ROOT + 'download_xls')
    os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

    mkdir_p(path)
    os.popen('chmod 777 %s' % (path))
    filename = user_name + '_' + datime.now().strftime('%Y%m%d%H%M%S') + '.xls'

    titlelist = ["产品名称/ProductTitle","产品SKU/SKU","自定义编号/CustomerLabel","申报价值(USD)/DeclaredPrice",
                "英文申报名称/EnglishDeclaredName","中文申报名称/ChineseDeclaredName","申报币种/CurrencyCode",
                "海关编码/HSCode","货物类型/ProductsType","品类语言/CategoryLang","品类ID/CategoryID",
                "重量/Weight","长/Length","宽/Width","高/Height","货物属性/ContainBattery",]
    datalist = []
    datalist.append(titlelist)
    pathname = path  + '/' + filename
    for obj in paramlist:
        py_b_goods_obj = py_b_goods.objects.filter(SKU = obj[1]) #
        if py_b_goods_obj.exists():
            packinfo    = py_b_goods_obj[0].PackName
            del obj[4]
            obj.insert(4,py_b_goods_obj[0].AliasEnName)

            del obj[5]
            obj.insert(5,py_b_goods_obj[0].AliasCnName)

            infolist = re.findall(r'[0-9.*]+',packinfo)

            if infolist and infolist[0].find('*') != -1 and len(infolist[0].split('*')) >= 2:
                del obj[12]
                obj.insert(12,infolist[0].split('*')[0])

                del obj[13]
                obj.insert(13,infolist[0].split('*')[1])
        datalist.append(obj)
    myresult = generate_excel(datalist, pathname)
    if myresult['code'] == 0:
        os.popen(r'chmod 777 %s' %pathname)
        upload_to_oss_obj = upload_to_oss(BUCKETNAME_DOWNLOAD)
        uploadresult = upload_to_oss_obj.upload_to_oss(
            {'path': user_name, 'name': filename, 'byte': open(pathname), 'del': 1})
        if uploadresult['result'] != '':
            t_download_info.objects.create(appname = user_name + '/' + filename,abbreviation = u'备货需求表-'+ filename,
                                           updatetime = datime.now(),Belonger = user_name,Datasource='t_stocking_demand_list')

@app.task
def fba_product_registration_form_excel_task(paramlist,user_name):
    import re,os
    from Project.settings import BUCKETNAME_DOWNLOAD,MEDIA_ROOT
    from pyapp.models import b_goods as py_b_goods
    from brick.public.generate_excel import generate_excel
    from brick.public.create_dir import mkdir_p
    from brick.public.upload_to_oss import upload_to_oss
    from skuapp.table.t_download_info import t_download_info
    from datetime import datetime as datime

    path = MEDIA_ROOT + 'download_xls/' + user_name
    mkdir_p(MEDIA_ROOT + 'download_xls')
    os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

    mkdir_p(path)
    os.popen('chmod 777 %s' % (path))
    filename = user_name + '_' + datime.now().strftime('%Y%m%d%H%M%S') + '.xls'

    titlelist = ["产品名称/ProductTitle","产品SKU/SKU","自定义编号/CustomerLabel","申报价值(USD)/DeclaredPrice",
                "英文申报名称/EnglishDeclaredName","中文申报名称/ChineseDeclaredName","申报币种/CurrencyCode",
                "海关编码/HSCode","货物类型/ProductsType","品类语言/CategoryLang","品类ID/CategoryID",
                "重量/Weight","长/Length","宽/Width","高/Height","货物属性/ContainBattery",]
    datalist = []
    datalist.append(titlelist)
    pathname = path  + '/' + filename
    for obj in paramlist:
        py_b_goods_obj = py_b_goods.objects.filter(SKU = obj[1]) #
        if py_b_goods_obj.exists():
            packinfo    = py_b_goods_obj[0].PackName
            del obj[4]
            obj.insert(4,py_b_goods_obj[0].AliasEnName)

            del obj[5]
            obj.insert(5,py_b_goods_obj[0].AliasCnName)

            infolist = re.findall(r'[0-9.*]+',packinfo)

            if infolist and infolist[0].find('*') != -1 and len(infolist[0].split('*')) >= 2:
                del obj[12]
                obj.insert(12,infolist[0].split('*')[0])

                del obj[13]
                obj.insert(13,infolist[0].split('*')[1])
        datalist.append(obj)
    myresult = generate_excel(datalist, pathname)
    if myresult['code'] == 0:
        os.popen(r'chmod 777 %s' %pathname)
        upload_to_oss_obj = upload_to_oss(BUCKETNAME_DOWNLOAD)
        uploadresult = upload_to_oss_obj.upload_to_oss(
            {'path': user_name, 'name': filename, 'byte': open(pathname), 'del': 1})
        if uploadresult['result'] != '':
            t_download_info.objects.create(appname = user_name + '/' + filename,abbreviation = u'FBA备货需求表-'+ filename,
                                           updatetime = datime.now(),Belonger = user_name,Datasource='t_stocking_demand_fba')

from brick.joom.export_joom_wait_upload_excel import *
from brick.function.generate_random_title import get_coreWords_list
@app.task
def joom_export_excel(id_list, export_user, export_time, shopname, calculate_flag):
    """导出joom待铺货表格"""
    coreWordsList = get_coreWords_list()
    export_joom_wait_upload_excel(id_list, export_user, export_time, coreWordsList, shopname, calculate_flag)


from brick.joom.create_collection_box_from_wish import create_collection_box_from_wish
@app.task
def joom_info_from_wish(joom_id, user, time):
    """wish生成公共模板的同时生成joom采集箱信息"""
    create_collection_box_from_wish(joom_id, user, time)
import json
from brick.amazon.download_trackinfo_pdf import download_trackinfo_pdf
from brick.public.upload_to_oss import upload_to_oss
from brick.public.create_dir import *
from brick.public.clear_dir import *
@app.task
def download_trackInfo_pdf(params):
    from skuapp.table.t_download_info import t_download_info
    from datetime import datetime as dtime
    trackNumbers = params['trackNumbers']
    download_trackinfo_pdf_obj = download_trackinfo_pdf()
    upload_to_oss_obj = upload_to_oss(BUCKETNAME_DOWNLOAD)
    userName = params['userName'] + '/trackInfo'
    filePath = '/data/djangostack-1.9.7/apps/django/django_projects/Project/media/Amazon/IN/trackInfo/'
    clear_p(filePath)
    mkdir_p(filePath)
    for i in range(0, len(trackNumbers)):
        # pdfData = download_trackinfo_pdf_obj.get_each_trackinfo_pdf({'trackNumber': trackNumbers[i]})
        url = 'http://api.cnilink.com/v1.0.0/shpping/label?awb='
        req = urllib2.Request(url=url + trackNumbers[i])
        req.add_header("Content-Type", "application/json")
        req.add_header("AuthToken", "YWU0MDliYmIwZTExODA3MjNmMTFjMmNjOWIzMDM1MzI=")
        respons = urllib2.urlopen(req)
        responsData = respons.read()
        respons_ison = json.loads(responsData)
        labledata = respons_ison["info"]["labelUrl"]
        filename = str(i) + '.pdf'
        f = urllib2.urlopen(labledata)
        data = f.read()
        with open(filePath + filename, "wb") as code:
            code.write(data)

    filename = params['filename']
    download_trackinfo_pdf_obj.MergePDF({'filepath': filePath, 'outfile': filename, 'fileCount': len(trackNumbers)})
    upload_to_oss_obj.upload_to_oss({'path': userName, 'name': filename, 'byte': open(filePath + filename), 'del': 0})
    appname = u'%s/%s' %(userName,filename)
    t_download_info.objects.create(appname=appname, abbreviation=params['filename'],
                                   updatetime=dtime.now(), Belonger=params['userName'],
                                   Datasource='t_order_amazon_india')

from brick.amazon.generate_price_order import *
@app.task
def download_price_pdf(params):
    from skuapp.table.t_download_info import t_download_info
    from datetime import datetime as dtime
    orderNumbers = params['orderNumbers']
    generate_price_order_obj = generate_price_order()
    download_trackinfo_pdf_obj = download_trackinfo_pdf()
    upload_to_oss_obj = upload_to_oss(BUCKETNAME_DOWNLOAD)
    userName = params['userName'] + '/price'
    filePath = '/data/djangostack-1.9.7/apps/django/django_projects/Project/media/Amazon/IN/price/'
    clear_p(filePath)
    mkdir_p(filePath)
    for i in range(0, len(orderNumbers)):
        filename = str(i) + '.pdf'
        generate_price_order_obj.generate_price_info_pdf({'orderNumber': orderNumbers[i], 'filepath': filePath + filename})

    filename = params['filename']
    download_trackinfo_pdf_obj.MergePDF({'filepath': filePath, 'outfile': filename, 'fileCount': len(orderNumbers)})
    upload_to_oss_obj.upload_to_oss({'path': userName, 'name': filename, 'byte': open(filePath + filename), 'del': 0})
    appname = u'%s/%s' %(userName,filename)
    t_download_info.objects.create(appname=appname, abbreviation=params['filename'],
                                   updatetime=dtime.now(), Belonger=params['userName'],
                                   Datasource='t_order_amazon_india')

from brick.pydata.py_syn.py_information_by_b_goodslog import *
import pymssql
@app.task
def syn_py_info_b():
    sqlserver_conn = pymssql.connect(host='122.226.216.10', user='fancyqube', password='K120Esc1', database='ShopElf', port='18793')
    py_information_b_obj = py_information_by_b_goodslog(connection, sqlserver_conn)
    py_information_b_obj.py_synchronization_by_b_goodslog()
    
    # sku状态同步更新
    from brick.public.sku_status_change import sku_status_change
    sku_status_change()

#海鹰数据API
from brick.wish.Haiying_Data.get_data_from_haiying_task import get_data_from_haiying_task
@app.task
def get_data_from_haiying(pagnum):
    for i in range(pagnum):
        get_data_from_haiying_task.delay(i)

#海鹰数据小火苗
from brick.wish.Haiying_Data.get_data_from_haiying_task import get_data_from_haiying_original_trans
@app.task
def get_data_from_haiying_viewdata(pagnum):
    get_data_from_haiying_original_trans(pagnum)

# #海鹰数据API
# from brick.wish.Haiying_Data.delete_redis_key import get_data_from_haiying_task_delete
# @app.task
# def get_data_from_haiying_delete(pagnum):
#     for i in range(pagnum):
#         get_data_from_haiying_task_delete.delay(i)



@app.task
def generate_delivery_invoices(idlist,user_name):
    import xlwt,os
    from django.db import connection
    from skuapp.table.t_shipping_management import t_shipping_management
    from skuapp.table.t_stocking_demand_list import t_stocking_demand_list
    from brick.table.t_overseas_warehouse_information import t_overseas_warehouse_information
    from pyapp.models import b_goods as py_b_goods
    from Project.settings import SBBL,MEDIA_ROOT,BUCKETNAME_overseas_warehouse_cargo_infor_xls
    from brick.public.create_dir import mkdir_p
    from datetime import datetime as datime
    from brick.public.upload_to_oss import upload_to_oss

    path = MEDIA_ROOT + 'download_xls/' + user_name
    mkdir_p(MEDIA_ROOT + 'download_xls')
    os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

    mkdir_p(path)
    os.popen('chmod 777 %s' % (path))

    print 'path============================%s'%path
    for myid in idlist:
        t_shipping_management_obj = t_shipping_management.objects.filter(id = myid)
        t_overseas_warehouse_information_obj = t_overseas_warehouse_information(connection)
        if t_shipping_management_obj.exists():

            filename = user_name + '_' + datime.now().strftime('%Y%m%d%H%M%S') + '_' + str(myid) + '.xls'

            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
            style = xlwt.XFStyle()
            # 字体 宋体
            fnt = xlwt.Font()
            fnt.name = u'SimSun'
            style.font = fnt
            # 位置：居中
            alignment = xlwt.Alignment()  # Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style.alignment = alignment
            # 边框：实线
            borders = xlwt.Borders()
            borders.left = xlwt.Borders.THIN
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            style.borders = borders

            obj = t_overseas_warehouse_information_obj.get_overseas_warehouse_information(t_shipping_management_obj[0].Destination_warehouse)

            if obj:
                row = 0
                col = 0
                worksheet.write_merge(row, row + 0, col, col + 2, u'SHIPPER(发件人信息）', style)
                col = 3
                worksheet.write_merge(row, row + 0, col, col + 4, u'SHIP TO(收件人信息）', style)

                inforlist = [
                             {u'Contact Name/联系人姓名':['Luo Difei',obj[7]]},
                             {u'Company Name/公司名称':['Fancy',obj[8]]},
                             {u'Company Address(地址）':['NO.297,Qian Fang Road ',obj[1]]},
                             {u'City/城市':['Jin Hua',obj[2]]},
                             {u'StateProvince/洲省':['Zhe Jiang',obj[3]]},
                             {u'Postal Code(邮编）':['322200',obj[4]]},
                             {u'Country/国家':['China',obj[5]]},
                             {u'Telephone No/联系电话':['18072321653',obj[6]]},
                            ]
                for i in range(0,len(inforlist)):
                    for k,v in inforlist[i].items():
                        row = row + 1
                        col = 0
                        worksheet.write_merge(row, row + 0, col, col + 1, k, style)
                        col = 2
                        worksheet.write_merge(row, row + 0, col, col + 0, v[0], style)
                        col = 3
                        worksheet.write_merge(row, row + 0, col, col + 0, k, style)
                        col = 4
                        worksheet.write_merge(row, row + 0, col, col + 3, v[1], style)

                row = row + 1
                col = 0
                worksheet.write_merge(row, row + 0, col, col + 1, '', style)
                col = 2
                worksheet.write_merge(row, row + 0, col, col + 0, '', style)
                col = 3
                worksheet.write_merge(row, row + 0, col, col + 0, u'Odd number/原单号', style)
                col = 4
                worksheet.write_merge(row, row + 0, col, col + 3, u'%s'%t_shipping_management_obj[0].Warehouse_number, style)

                row = row + 1
                col = 0
                worksheet.write_merge(row, row + 0, col, col + 7, u'Cargo information/货 物 信 息', style)

                cargolist = [
                    [u'数量',u'计量单位/个/双',u'品名/Product Name',u'材质/Material',u'HS 编码',u'原产国',u'单价',u'总价'],
                ]
                pricenum = 0.0
                productskulist = t_shipping_management_obj[0].All_ProductSKU_Num.split(';')
                for prosku in productskulist:
                    if prosku.find('*') != -1:
                        py_b_goods_obj = py_b_goods.objects.filter(SKU=prosku.split('*')[0]).values('Unit','Material','CostPrice','AliasCnName','AliasEnName')
                        Unit      = ''
                        Material  = ''
                        CostPrice = 0.0
                        AliasCnName = ''
                        AliasEnName = ''
                        if py_b_goods_obj.exists():
                            Unit      = py_b_goods_obj[0]['Unit']
                            Material  = py_b_goods_obj[0]['Material']
                            CostPrice = py_b_goods_obj[0]['CostPrice']
                            AliasCnName = py_b_goods_obj[0]['AliasCnName']
                            AliasEnName = py_b_goods_obj[0]['AliasEnName']
                        price = float(CostPrice)/SBBL

                        pricenum = pricenum + (price * int(prosku.split('*')[1]))

                        skuinfo = [prosku.split('*')[1],Unit,AliasCnName + '/' + AliasEnName,Material,'','CN',
                                   '$' + '%.2f'%(price),
                                   '$' + '%.2f'%(price * int(prosku.split('*')[1]))]
                        cargolist.append(skuinfo)

                for cargo in cargolist:
                    row = row + 1
                    col = 0
                    for car in cargo:
                        worksheet.write_merge(row, row + 0, col, col + 0, car, style)
                        col = col + 1

                lastlist = [
                    [u'lump sum/总金额','$' + '%.2f'%(pricenum)],
                    [u'Number/件数',str(t_shipping_management_obj[0].BoxNum) + u'件'],
                    [u'Total Weight/总重量',str(t_shipping_management_obj[0].BoxWeight) + 'KG']
                ]
                col = 0
                row = row + 1
                channel = ''
                t_stocking_demand_list_obj = t_stocking_demand_list.objects.filter(Stocking_plan_number = t_shipping_management_obj[0].Stocking_plan_number.split('|')[0]).values('level')
                if t_stocking_demand_list_obj.exists():
                    if t_stocking_demand_list_obj[0]['level'].strip() == 'normal':
                        channel = u'船运'
                    elif t_stocking_demand_list_obj[0]['level'].strip() == 'urgent':
                        channel = u'空运'
                    else:
                        channel = u'指定物流'
                worksheet.write_merge(row, row + 2, col, col + 3, channel, style)
                for i in range(3):
                    col = col + 4
                    worksheet.write_merge(row, row + 0, col, col + 2, lastlist[i][0], style)
                    col = col + 3
                    worksheet.write_merge(row, row + 0, col, col + 0, lastlist[i][1], style)
                    row = row + 1
                    col = 0

            workbook.save(path + '/' + filename)

            upload_to_oss_obj = upload_to_oss(BUCKETNAME_overseas_warehouse_cargo_infor_xls)
            myresult = upload_to_oss_obj.upload_to_oss({'path':user_name,'name':filename,'byte':open(path + '/' + filename),'del':1})
            if myresult['result'] != '':
                t_shipping_management_obj.update(Invoice = myresult['result'])



@app.task
def import_excel_file(file_obj,user_name):
    import xlrd
    from skuapp.table.t_stocking_demand_list import t_stocking_demand_list
    from pyapp.models import b_goods as py_b_goods, B_Supplier as py_b_Supplier
    from datetime import datetime as dattime
    from skuapp.table.public import *
    import sys
    # sku   店铺sku   产品性质    数量  目的仓库    账号  站点  紧急程度    提交人 备注
    insertinto = []
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
    table = wb.sheets()[0]
    row = table.nrows
    result = {'errorcode':0,'errortext':u'导入成功'}
    strLine = ""
    try:
        for i in xrange(1, row):
            try:
                col = table.row_values(i)
                Stocking_plan_number = dattime.now().strftime('%Y%m%d%H%M%S') + '_' + str(i)
                ProductSKU = col[0].strip()
                ShopSKU = '%s'%col[1]
                if ShopSKU.find('.') != -1:
                    ShopSKU = ShopSKU.split('.')[0]
                ProductName = ''
                ProductImage = ''
                ProductPrice = 0.0
                ProductWeight = 0.0
                Supplier = ''
                Supplierlink = ''
                py_b_goods_objs = py_b_goods.objects.filter(SKU=ProductSKU)
                if py_b_goods_objs.exists():
                    ProductImage = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % py_b_goods_objs[0].SKU.replace(
                        'OAS-', '').replace('FBA-', '')
                    ProductName = py_b_goods_objs[0].GoodsName
                    ProductPrice = py_b_goods_objs[0].CostPrice
                    ProductWeight = py_b_goods_objs[0].Weight
                    Supplierlink = py_b_goods_objs[0].LinkUrl

                    py_b_Supplier_objs = py_b_Supplier.objects.filter(NID=py_b_goods_objs[0].SupplierID)
                    if py_b_Supplier_objs.exists():
                        Supplier = py_b_Supplier_objs[0].SupplierName

                Destination_warehouse = ''
                for warehouse in getChoices(ChoiceWarehouse):
                    if warehouse[1] is not None and str(col[4]).strip() == warehouse[1].strip():
                        Destination_warehouse = warehouse[0].strip()
                level = ''
                for lev in getChoices(ChoiceLevel):
                    if lev[1] is not None and str(col[7]).strip() == lev[1].strip():
                        level = lev[0].strip()
                nature = ''
                '''
                for each in getChoices(ChoiceProductnature):
                    if each[1] is not None and str(col[2]).strip() == each[1].strip():
                        nature = each[0].strip()
                        break
                '''
                # 产品性质
                nature = 'generalcargo'
                from brick.pydata.py_syn.py_conn import py_conn
                pyconn = py_conn()
                sqlserverInfo = pyconn.py_conn_database()
                if sqlserverInfo['errorcode'] != 0:
                    raise Exception('普元库链接失败，请重新提交;')
                else:
                    strSql = "select AttributeName from B_GoodsAttribute where GoodsID = (select nid from B_Goods where SKU='%s')" % (
                        ProductSKU)
                    sqlserverInfo['py_cursor'].execute(strSql)
                    returnResult = sqlserverInfo['py_cursor'].fetchone()
                    if returnResult:
                        if str(returnResult[0]).replace(";", "") == u"其余违禁品":
                            nature = 'contraband'
                        elif str(returnResult[0]).replace(";", "") == u"纯电池商品":
                            nature = 'pureelectric'
                        elif str(returnResult[0]).replace(";", "") == u"内置电池商品" or str(returnResult[0]).replace(";", "") == u"带电商品" or str(returnResult[0]).replace(";", "") == u"纽扣电池商品":
                            nature = 'withelectric'
                        elif str(returnResult[0]).replace(";", "") == u"粉末商品" or str(returnResult[0]).replace(";", "") == u"其余化妆品":
                            nature = 'powderpaste'
                        elif str(returnResult[0]).replace(";", "") == u"带磁商品":
                            nature = 'withmagnetism'
                        elif str(returnResult[0]).replace(";", "") == u"液体商品":
                            nature = 'liquid'
                        elif str(returnResult[0]).replace(";", "") == u"普货":
                            nature = 'generalcargo'
                        else:
                            nature = 'specialclass'
                    else:
                        #raise Exception('从普元未关联到产品特性，需要对该商品在普元录入商品特性后再提交,')
                        nature = 'generalcargo'
                pyconn.py_close_conn_database()
                AmazonFactory = 'no'
                if (col[11]).strip() == u'是' or (col[11]).strip() == u'yes':
                    AmazonFactory = 'yes'

                Stocking_quantity = 0
                #if str(col[2]).strip() != '':
                Stocking_quantity = col[3]
                Stocking_NewOrOld = ''
                if str(col[10]).strip() != '':
                    Stocking_NewOrOld = int(col[10])
                insertinto.append(t_stocking_demand_list(
                    Stocking_plan_number=Stocking_plan_number, Stock_plan_date=dattime.now(),
                    Demand_people=user_name,
                    ProductSKU=ProductSKU, ProductImage=ProductImage, ProductName=ProductName, ProductPrice=ProductPrice,
                    ProductWeight=ProductWeight,
                    Supplier=Supplier, Supplierlink=Supplierlink,
                    Buyer='',
                    Status=u'notgenerated', Stocking_quantity=Stocking_quantity, Destination_warehouse=Destination_warehouse,
                    AccountNum=col[5], Site=col[6], level=level,Product_nature=nature,
                    Remarks=col[9],ShopSKU=ShopSKU,neworold=Stocking_NewOrOld,AmazonFactory=AmazonFactory
                ))
            except Exception, ex:
                result['errorcode'] = -1
                result['errortext'] = '第%d行存在问题:Exception:%s, ex:%s，请修正后重新上传' % (i + 1, Exception, ex)
                break
        if result['errorcode'] == 0:
            t_stocking_demand_list.objects.bulk_create(insertinto)
    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = 'Exception = %s ex=%s,第%s行数据异常,请修改后重新上传。' % (Exception, ex,strLine)
    return result

@app.task
def import_fba_excel_file(file_obj,user_name):
    import xlrd
    from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
    from pyapp.models import b_goods as py_b_goods, B_Supplier as py_b_Supplier
    from skuapp.table.t_stocking_demand_fba_detail import t_stocking_demand_fba_detail
    from datetime import datetime as dattime
    from skuapp.table.public import *
    import sys
    from brick.classredis.classsku import classsku
    classskuObj = classsku()

    #商品sku(0) 店铺sku(1)   数量(2)  目的仓库(3)    账号(4)  紧急程度(5)  1-新品/2-补品(6)  亚马逊服装(7) 质检标志(8) 备注(9)
    insertinto = []
    insertSKU = []
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
    table = wb.sheets()[0]
    row = table.nrows
    result = {'errorcode':0,'errortext':u'导入成功'}
    strLine = ""
    try:
        for i in xrange(1, row):
            try:
                col = table.row_values(i)
                Stocking_plan_number = dattime.now().strftime('%Y%m%d%H%M%S') + '_' + str(i)
                ProductSKU = col[0].strip()
                ShopSKU = col[1].strip()
                ProductName = ''
                ProductImage = ''
                ProductPrice = 0.0
                ProductWeight = 0.0
                Supplier = ''
                Supplierlink = ''
                Buyer = ''
                #获取商品图片、商品名称、商品成本价、商品重量、供应商链接、供应商名
                py_b_goods_objs = py_b_goods.objects.filter(SKU=ProductSKU)
                if py_b_goods_objs.exists():
                    ProductImage = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % py_b_goods_objs[0].SKU.replace(
                        'OAS-', '').replace('FBA-', '')
                    ProductName = py_b_goods_objs[0].GoodsName
                    ProductPrice = py_b_goods_objs[0].CostPrice
                    ProductWeight = py_b_goods_objs[0].Weight
                    Supplierlink = py_b_goods_objs[0].LinkUrl
                    Buyer = py_b_goods_objs[0].Purchaser

                    py_b_Supplier_objs = py_b_Supplier.objects.filter(NID=py_b_goods_objs[0].SupplierID)
                    if py_b_Supplier_objs.exists():
                        Supplier = py_b_Supplier_objs[0].SupplierName
                #目的仓库
                Destination_warehouse = ''
                for warehouse in getChoices(ChoiceWarehouse):
                    if warehouse[1] is not None and str(col[3]).strip() == warehouse[1].strip():
                        Destination_warehouse = warehouse[0].strip()
                #紧急程度
                level = ''
                for lev in getChoices(ChoiceLevel):
                    if lev[1] is not None and str(col[5]).strip() == lev[1].strip():
                        level = lev[0].strip()
                # 产品性质
                nature = 'generalcargo'
                from brick.pydata.py_syn.py_conn import py_conn
                pyconn = py_conn()
                sqlserverInfo = pyconn.py_conn_database()
                if sqlserverInfo['errorcode'] != 0:
                    raise Exception('普元库链接失败，请重新提交;')
                else:
                    strSql = "select AttributeName from B_GoodsAttribute where GoodsID = (select nid from B_Goods where SKU='%s')" % (
                        ProductSKU)
                    sqlserverInfo['py_cursor'].execute(strSql)
                    returnResult = sqlserverInfo['py_cursor'].fetchone()
                    if returnResult:
                        if str(returnResult[0]).replace(";", "") == u"其余违禁品":
                            nature = 'contraband'
                        elif str(returnResult[0]).replace(";", "") == u"纯电池商品":
                            nature = 'pureelectric'
                        elif str(returnResult[0]).replace(";", "") == u"内置电池商品" or str(returnResult[0]).replace(";", "") == u"带电商品" or str(returnResult[0]).replace(";", "") == u"纽扣电池商品":
                            nature = 'withelectric'
                        elif str(returnResult[0]).replace(";", "") == u"粉末商品" or str(returnResult[0]).replace(";", "") == u"其余化妆品":
                            nature = 'powderpaste'
                        elif str(returnResult[0]).replace(";", "") == u"带磁商品":
                            nature = 'withmagnetism'
                        elif str(returnResult[0]).replace(";", "") == u"液体商品":
                            nature = 'liquid'
                        elif str(returnResult[0]).replace(";", "") == u"普货":
                            nature = 'generalcargo'
                        else:
                            nature = 'specialclass'
                    else:
                        #raise Exception('从普元未关联到产品特性，需要对该商品在普元录入商品特性后再提交,')
                        nature = 'generalcargo'
                pyconn.py_close_conn_database()

                AmazonFactory = 'no'
                if (col[7]).strip() == u'是' or (col[7]).strip() == u'yes':
                    AmazonFactory = 'yes'

                CheckFlag = '0'
                if (col[8]).strip() == u'抽检':
                    CheckFlag = '1'
                elif (col[8]).strip() == u'免检':
                    CheckFlag = '2'

                #采购数量、新/补品
                Stocking_quantity = 0
                if str(col[2]).strip() != '':
                    Stocking_quantity = col[2]
                Stocking_NewOrOld = ''
                if str(col[6]).strip() != '':
                    Stocking_NewOrOld = int(col[6])
                Number = classskuObj.get_number_by_sku(ProductSKU)
                Number = 0 if (Number is None or Number=='') else Number
                insertinto.append(t_stocking_demand_fba(
                    Stocking_plan_number=Stocking_plan_number, Stock_plan_date=dattime.now(),
                    Demand_people=user_name,
                    ProductSKU=ProductSKU, ProductImage=ProductImage, ProductName=ProductName, ProductPrice=ProductPrice,
                    ProductWeight=ProductWeight,
                    Supplier=Supplier, Supplierlink=Supplierlink,Buyer=Buyer,
                    Status='notgenpurchase', Stocking_quantity=Stocking_quantity,QTY=Stocking_quantity, Destination_warehouse=Destination_warehouse,
                    AccountNum=col[4], Site='', level=level,Product_nature=nature,
                    Remarks=col[9],ShopSKU=ShopSKU,neworold=Stocking_NewOrOld,AmazonFactory=AmazonFactory,Number=int(Number),isCheck=CheckFlag
                ))
                #sku 插入t_stocking_demand_fba_detail
                insertSKU.append(t_stocking_demand_fba_detail(ProductSKU=ProductSKU,Stocking_plan_number=Stocking_plan_number,CreateDate=dattime.now(),Status='notgenpurchase',AuditFlag=0))
            except Exception, ex:
                result['errorcode'] = -1
                result['errortext'] = '第%d行存在问题:Exception:%s, ex:%s，请修正后重新上传' % (i + 1, Exception, ex)
                break
        if result['errorcode'] == 0:
            t_stocking_demand_fba.objects.bulk_create(insertinto)
            t_stocking_demand_fba_detail.objects.bulk_create(insertSKU)
    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = 'Exception = %s ex=%s,第%s行数据异常,请修改后重新上传。' % (Exception, ex,strLine)
    return result

@app.task
def import_fbareject_excel_file(file_obj,user_name):
    import xlrd
    from skuapp.table.t_stocking_reject_fba import t_stocking_reject_fba
    from pyapp.models import b_goods as py_b_goods, B_Supplier as py_b_Supplier
    from datetime import datetime as dattime
    from skuapp.table.public import *
    import sys

    #sku    采购单号    退货数量    转仓/退货   备注
    insertinto = []
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
    table = wb.sheets()[0]
    row = table.nrows
    result = {'errorcode':0,'errortext':u'导入成功'}
    strLine = ""
    try:
        for i in xrange(1, row):
            try:
                col = table.row_values(i)
                RejectNumber = dattime.now().strftime('%Y%m%d%H%M%S') + '_' + str(i)
                ProductSKU = col[0].strip()
                PurchaseOrderNum = ''
                if str(col[1]).strip() != '':
                    PurchaseOrderNum = col[1].strip()
                else:
                    result['errorcode'] = -1
                    result['errortext'] = '第%d行采购单号为空，请补全后重新上传' % (i+1)
                    break
                ProductName = ''
                ProductImage = ''
                #获取商品图片、商品名称
                py_b_goods_objs = py_b_goods.objects.filter(SKU=ProductSKU)
                if py_b_goods_objs.exists():
                    ProductImage = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % py_b_goods_objs[0].SKU.replace(
                        'OAS-', '').replace('FBA-', '')
                    ProductName = py_b_goods_objs[0].GoodsName

                #退货数量
                RejectNum = 0
                if str(col[2]).strip() != '':
                    RejectNum = col[2]
                else:
                    result['errorcode'] = -1
                    result['errortext'] = '第%d行退货数量为空%s，请补全后重新上传' % (i + 1,col[2])
                    break
                #转退标志
                statusFlag='return'
                if str(col[3]).strip() == u'转仓':
                    statusFlag = 'turn'
                elif str(col[3]).strip() == u'退货':
                    statusFlag = 'return'
                else:
                    result['errorcode'] = -1
                    result['errortext'] = '第%d行转退标志为空，请补全后重新上传' % (i + 1)
                    break

                insertinto.append(t_stocking_reject_fba(
                    RejectNumber=RejectNumber, RejectDate=dattime.now(),
                    RejectMan=user_name,
                    ProductSKU=ProductSKU, ProductImage=ProductImage, ProductName=ProductName,PurchaseOrderNum=PurchaseOrderNum,
                    Status='reject',RejectStatus=statusFlag, RejectNum=RejectNum,isCheckTranReturn=0,
                    Remarks=col[4],
                ))
            except Exception, ex:
                result['errorcode'] = -1
                result['errortext'] = '第%d行存在问题:Exception:%s, ex:%s，请修正后重新上传' % (i + 1,Exception,ex)
                break
        if result['errorcode'] == 0:
            t_stocking_reject_fba.objects.bulk_create(insertinto)
    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = 'Exception = %s ex=%s,第%s行数据异常,请修改后重新上传。' % (Exception, ex,strLine)
    return result

@app.task
def import_excel_clothfactory_file(file_obj,user_name):
    import xlrd
    from django.db import connection
    from skuapp.table.t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
    from pyapp.models import b_goods as py_b_goods, B_Supplier as py_b_Supplier
    from datetime import datetime as dattime
    from skuapp.table.public import *
    import sys

    #商品SKU  建议采购数量  排单类型    采购员 备注
    insertinto = []
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
    table = wb.sheets()[0]
    row = table.nrows
    result = {'errorcode':0,'errortext':u'导入成功'}
    strLine = ""
    try:
        for i in xrange(1, row):
            try:
                col = table.row_values(i)
                ProductSKU = ''
                if str(col[0]).strip() != '':
                    ProductSKU = col[0].strip()
                else:
                    result['errorcode'] = -1
                    result['errortext'] = '第%d行商品SKU为空，请补全后重新上传' % (i+1)
                    break
                suggestNum = 0
                if str(col[1]).strip() != '':
                    suggestNum = col[1]
                #标志
                SpecialPurchaseFlag='firstorder'
                if str(col[2]).strip() == u'首单':
                    SpecialPurchaseFlag = 'firstorder'
                elif str(col[2]).strip() == u'定做':
                    SpecialPurchaseFlag = 'customermade'
                elif str(col[2]).strip() == u'其他' or str(col[2]).strip() == u'浦江仓库':
                    SpecialPurchaseFlag = 'other'
                elif str(col[2]).strip() == u'年底备货':
                    SpecialPurchaseFlag = 'endyearstock'
                elif str(col[2]).strip() == u'测试翻单':
                    SpecialPurchaseFlag = 'returnorder'
                else:
                    result['errorcode'] = -1
                    result['errortext'] = '第%d行排单类型为空，请修改排单类型后重新上传' % (i + 1)
                    break
                purchaser = ''
                if str(col[3]).strip() != '':
                    purchaser = col[3].strip()

                strSql = '''
                                SELECT
                                a.BmpUrl, a.SKU, a.TortInfo, a.GoodsStatus, a.Purchaser, a.SalerName2, a.SellCount1, a.SellCount2, a.SellCount3, a.UseNumber,
                                a.NotInStore as NotInStore, a.CostPrice,4 * a.SellCount1 - a.Number - a.NotInStore as SuggestNum,
                                a.hopeUseNum as hopeUseNum, a.UnPaiDNum, a.ReservationNum, a.Number, a.GoodsName, a.SupplierName, a.Model,
                                (a.hopeUseNum) / a.AverageNumber as SaleDay, a.CgCategory, a.AverageNumber,
                                if (((a.hopeUseNum) / a.AverageNumber) <= 15, 1, 2) as flag,a.SourceOSCode
                                FROM py_db.kc_currentstock_sku a  where SKU='%s'  and storeID=1
                            ''' % (ProductSKU)
                hqdb_cursor = connection.cursor()
                hqdb_cursor.execute(strSql)
                resultRecord = hqdb_cursor.fetchone()

                if resultRecord :
                    if purchaser == '':
                        purchaser = resultRecord[4]
                    OSCode = resultRecord[24]
                    if resultRecord[24] not in ['OS901', 'OS902', 'OS903', 'OS904', 'OS905', 'OS906', 'OS909']:
                        OSCode = 'OS905'
                    if SpecialPurchaseFlag == 'endyearstock':
                        OSCode = 'OS903'
                    insertinto.append(t_cloth_factory_dispatch_needpurchase(
                        SKU=ProductSKU, BmpUrl=resultRecord[0],TortInfo=resultRecord[2],goodsState = resultRecord[3],buyer=purchaser,
                        SalerName2=resultRecord[5],sevenSales = resultRecord[6],fifteenSales = resultRecord[7],thirtySales = resultRecord[8],
                        UseNumber=resultRecord[9], PurchaseNotInNum = resultRecord[10], goodsCostPrice = resultRecord[11],SuggestNum=suggestNum,ailableNum = resultRecord[13],
                        oosNum=resultRecord[14],occupyNum = resultRecord[15],stockNum = resultRecord[16],goodsName = resultRecord[17],girard = resultRecord[19],SaleDay = resultRecord[20],
                        goodsclass=resultRecord[21], AverageNumber = resultRecord[22],OSCode=OSCode, Supplier = u'广州工厂',currentState = '0', createDate = dattime.now(),
                        flag=9,remarkApply=col[4],SpecialPurchaseFlag=SpecialPurchaseFlag,GenRecordMan=user_name,GenRecordDate=dattime.now()
                    ))
                else:
                    result['errorcode'] = -1
                    result['errortext'] = '第%d行SKU关联数据存在问题，请联系IT解决' % (i + 1)
                    break
            except Exception, ex:
                result['errorcode'] = -1
                result['errortext'] = '第%d行存在问题:Exception:%s, ex:%s，请修正后重新上传' % (i + 1,Exception,ex)
                break
        if result['errorcode'] == 0:
            t_cloth_factory_dispatch_needpurchase.objects.bulk_create(insertinto)
    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = 'Exception = %s ex=%s,第%s行数据异常,请修改后重新上传。' % (Exception, ex,strLine)
    return result

@app.task
def import_ad_info_data_file(file_obj, user_name):
    import xlrd
    from xlrd import xldate_as_tuple
    from django.db import connection
    from skuapp.table.t_ad_info_reportform import t_ad_info_reportform
    from datetime import datetime as dattime
    from skuapp.table.public import *
    import sys
    from brick.pydata.py_syn.py_conn import py_conn
    import calendar
    import time
    from decimal import *

    day_now = time.localtime()
    day_begin = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)  # 月初肯定是1号
    wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
    day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)

    #普元链接
    py_connObj = py_conn()
    sqlconnInfo = py_connObj.py_conn_database()

    insertinto = []
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
    #xls_sheet = wb.sheet_by_index(0)
    table = wb.sheets()[0]
    row = table.nrows
    result = {'errorcode': 0, 'errortext': u'导入成功'}
    strLine = ""
    try:
        #开始删除本月已经导入的数据
        # 平台	卖家简称	ShopSKU	货币	花费	销售员	开始日期	结束日期
        for i in xrange(1, row):
            try:
                col = table.row_values(i)
                platName = col[0].lower()
                ShopSKU = str(col[2]).strip()
                #if ShopSKU.isdigit():
                #    ShopSKU = str(int(col[2])).strip()
                #    allInfo = allInfo + ShopSKU + ";"#
                # 获取广告费、费率代码、人民币
                pbfee = 0.0
                if str(col[4]).strip() != '':
                    pbfee = col[4]
                CurrencyCode = col[3]
                strCurrencySql = "select CURRENCYCODE,ExchangeRate from B_CurrencyCode(nolock) where CURRENCYCODE='%s' " % (
                    CurrencyCode)
                sqlconnInfo['py_cursor'].execute(strCurrencySql)
                result_CurrencyRate = sqlconnInfo['py_cursor'].fetchone()
                rmb = 0.0
                if result_CurrencyRate:
                    rmb = float(result_CurrencyRate[1]) * float(pbfee)

                if col[6]:
                    AdStartDate = str(dattime(*xldate_as_tuple(col[6], 0)))[:10]
                else:
                    AdStartDate = day_begin
                if col[7]:
                    AdEndDate = str(dattime(*xldate_as_tuple(col[7], 0)))[:10]
                else:
                    AdEndDate = day_end

                #判断shopsku是否已在表中，如果在表中费用累加
                t_ad_info_reportform_obj = t_ad_info_reportform.objects.filter(ShopSKU=ShopSKU).values_list('Fee','RMB','AdStartDate','AdEndDate')
                if t_ad_info_reportform_obj:
                    if str(AdStartDate) > str(t_ad_info_reportform_obj[0][2]):
                        AdStartDate = t_ad_info_reportform_obj[0][2]
                    if str(AdEndDate) < str(t_ad_info_reportform_obj[0][3]):
                        AdEndDate = t_ad_info_reportform_obj[0][3]
                    pbfee = float(pbfee) + float(t_ad_info_reportform_obj[0][0])
                    rmb = float(rmb) + float(t_ad_info_reportform_obj[0][1])
                    t_ad_info_reportform.objects.filter(ShopSKU=ShopSKU).update(Fee=pbfee,RMB=rmb,AdStartDate=AdStartDate,AdEndDate=AdEndDate)
                    continue
                SKU3 = ""
                SKU = ""
                if platName.lower() == 'ebay':
                    SKU3 =  ShopSKU.split("'")[-1]
                    strSqlSku = "select top 1 sku from P_TradeDt(nolock) where l_number='%s'" % (SKU3)
                    sqlconnInfo['py_cursor'].execute(strSqlSku)
                    result_SKU = sqlconnInfo['py_cursor'].fetchone()
                    if result_SKU:
                        SKU = result_SKU[0]
                else:
                    SKU3 = ShopSKU.split("+")[0].split("*")[0]
                    strSqlSku = "select top 1 sku from B_GoodsSKULinkShop(nolock) where shopsku='%s'" % (SKU3)
                    sqlconnInfo['py_cursor'].execute(strSqlSku)
                    result_SKU = sqlconnInfo['py_cursor'].fetchone()
                    if result_SKU:
                        SKU = result_SKU[0]

                #业绩归属人2
                salername1 = ""
                if SKU != '':
                    strSqlSalername1 = "select  salername from b_goods(nolock) where sku='%s'" % (SKU)
                    sqlconnInfo['py_cursor'].execute(strSqlSalername1)
                    result_Salername1 = sqlconnInfo['py_cursor'].fetchone()
                    if result_Salername1:
                        salername1 = result_Salername1[0]
                if col[6]:
                    AdStartDate = str(dattime(*xldate_as_tuple(col[6], 0)))[:10]
                else:
                    AdStartDate = day_begin
                if col[7]:
                    AdEndDate = str(dattime(*xldate_as_tuple(col[7], 0)))[:10]
                else:
                    AdEndDate = day_end
                insertinto.append(t_ad_info_reportform(
                    PlatName=platName, Saler=col[5], Salername1=salername1, ShopName=col[1],ShopSKU=ShopSKU,
                    CurrencyCode=CurrencyCode,Fee=pbfee,SKU=SKU,RMB=rmb,SKU3=SKU3,AdStartDate=AdStartDate, AdEndDate=AdEndDate,
                    StartDate=day_begin, EndDate=day_end,ImportMan=user_name,ImportTime=dattime.now()))
                t_ad_info_reportform.objects.bulk_create(insertinto)
                insertinto = []
            except Exception, ex:
                result['errorcode'] = -1
                result['errortext'] = '第%d行存在问题:Exception:%s, ex:%s，请修正后重新上传' % (i + 1, Exception, ex)
                #break
        if result['errorcode'] == 0:
            #wish 清空后再插入
            online_cursor = connection.cursor()
            strWishDelete = "delete from t_ad_info_reportform where PlatName='wish' and StartDate >='%s' and EndDate <='%s'"%(day_begin,day_end)
            online_cursor.execute(strWishDelete)
            strWishSql = '''
            insert into t_ad_info_reportform(PlatName,SKU,ShopSKU,SKU3,Salername1,ShopName,RMB,AdStartDate, AdEndDate,StartDate,EndDate)
            (select 'wish', productsku,l_number,l_number,SalerName1,suffix,sum(ifnull(pbspend,0)),min(closingdate),max(closingdate),'%s','%s' 
            from report_db.t_saler_profit_report_dd
            WHERE closingdate >='%s' and closingdate <='%s'
            and addressowner='wish' GROUP BY productsku,salername2,suffix
            HAVING sum(ifnull(pbspend,0)) > 0);
            '''%(day_begin,day_end,day_begin,day_end)
            online_cursor.execute(strWishSql)
            connection.commit()
            online_cursor.close()

            py_connObj.py_close_conn_database()
    except Exception, ex:
        py_connObj.py_close_conn_database()
        result['errorcode'] = -1
        result['errortext'] = 'Exception = %s ex=%s,第%s行数据异常,请修改后重新上传。' % (Exception, ex, strLine)

    return result

@app.task
def import_fba_sku_headcourse(file_obj, user_name):
    import xlrd
    from xlrd import xldate_as_tuple
    from django.db import connection
    from skuapp.table.t_stocking_demand_fba_sku_headcourse import t_stocking_demand_fba_sku_headcourse
    from datetime import datetime as dattime
    from skuapp.table.public import *
    import sys
    from brick.pydata.py_syn.py_conn import py_conn
    import calendar
    import time
    from decimal import *
    import re

    insertinto = []
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
    #xls_sheet = wb.sheet_by_index(0)
    table = wb.sheets()[0]
    row = table.nrows
    ncols = table.ncols
    result = {'errorcode': 0, 'errortext': u'导入成功'}
    strLine = ""
    try:
        # 平台	卖家简称	ShopSKU	货币	花费	销售员	开始日期	结束日期
        perRecordInfo = ""
        deliverList = ""
        batchlist = ""
        remarks = ""
        ALLInfo = ""
        nCountSku = 0
        '''
        http://blog.51cto.com/12573822/2048820
        colspan = {}
        if table.merged_cells:
            for item in table.merged_cells:
                # print 'item: ' + str(item)
                # 通过循环进行组合，从而得出所有的合并单元格的坐标
                for row in range(item[0], item[1]):
                    for col in range(item[2], item[3]):
                        # 合并单元格的首格是有值的，所以在这里进行了去重
                        if (row, col) != (item[0], item[2]):
                            colspan.update({(row, col): (item[0], item[2])})
        '''

        for i in xrange(0, row):
            try:

                col = table.row_values(i)
                oneCloumn = str(col[0]).strip()
                if u"清单号" in oneCloumn:
                    deliverList = str(col[1]).strip()
                elif  u"序号" in oneCloumn:
                    continue
                elif u"批次号" in oneCloumn:
                    batchlist = str(col[1]).strip()
                elif u"备注" in oneCloumn:
                    remarks = str(col[1]).strip()
                else:
                    if ncols < 13:
                        continue
                    nCountSku = nCountSku + 1
                    if perRecordInfo != "":
                        perRecordInfo = perRecordInfo + ","
                    perRecordInfo = perRecordInfo + "{\"sku\":\"" + str(col[1]).strip() + "\",\"GoodsName\":\""+str(col[2]).strip()+"\",\"ShopSKU\":\""+str(col[3]).strip()+"\",\"Asin\":\""+str(col[4]).strip()+\
                                    "\",\"BarCode\":\""+str(col[5]).strip()+"\",\"PlanDeliverNum\":\""+str(col[6]).strip()+\
                                    "\",\"SetNumber\":\""+str(col[7]).strip()+"\",\"PackSpec\":\""+str(col[8]).strip()+"\",\"ActDeliverNum\":\""+str(col[9]).strip()+"\",\"Position\":\""+str(col[10]).strip()+\
                                    "\",\"HeavyVolumePackage\":\""+str(col[11]).strip()+"\",\"Remark\":\""+re.sub(r'{}\[\]\"\'\r\n\t', "", str(col[12]).strip())+"\",\"id\":\""+str(nCountSku)+"\"}";
            except Exception, ex:
                result['errorcode'] = -1
                result['errortext'] = '第%d行存在问题:Exception:%s, ex:%s，请修正后重新上传' % (i + 1, Exception, ex)
        ALLInfo = "{\"deliverlist\":\"" + deliverList + "\",\"skuinfo\":[" + perRecordInfo + "],\"batchlist\":\"" + str(batchlist) + "\",\"remarks\":\"" + str(remarks) + "\"}"
        if result['errorcode'] == 0:
            t_stocking_demand_fba_sku_headcourse.objects.create(DeliverDate=time.strftime('%Y-%m-%d', time.localtime(time.time())),
                                                                ResponsibleMan=user_name,Shippinglist=str(ALLInfo),AddMan=user_name,AddTime=dattime.now(),DealStatus='salers')
    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = 'Exception = %s ex=%s,第%s行数据异常,请修改后重新上传。' % (Exception, ex, strLine)
    return result

@app.task
def import_fbw_excel_file(file_obj,user_name):
    import xlrd
    from skuapp.table.t_stocking_demand_fbw import t_stocking_demand_fbw
    from pyapp.models import b_goods as py_b_goods, B_Supplier as py_b_Supplier
    from datetime import datetime as dattime
    from skuapp.table.public import *
    # from brick.wish.wishlisting.refresh_fbw_flag import refresh_fbw_flag
    import sys
    from brick.classredis.classsku import classsku
    classskuObj = classsku()
    #目的仓库(0)   店铺(1)  ProductID(2)    SKU(3)  店铺SKU(4)  计划备货量(5)  FBW-US(6 )备注(7) 发货方式(8)   新老品(9)
    insertinto = []
    tmp = []
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
    table = wb.sheets()[0]
    row = table.nrows
    result = {'errorcode':0,'errortext':u'导入成功'}
    strLine = ""
    try:
        # refresh_fbw_list = []
        for i in xrange(1, row):
            try:
                col = table.row_values(i)
                Stocking_plan_number = dattime.now().strftime('%Y%m%d%H%M%S') + '_' + str(i)
                ProductSKU = col[3].strip()
                sellCount1 = classskuObj.get_sellcount1_by_sku(ProductSKU) #7天销量
                number = classskuObj.get_number_by_sku(ProductSKU)
                reservationnum = classskuObj.get_reservationnum_by_sku(ProductSKU)
                packInfo = classskuObj.get_packinfo_by_sku(ProductSKU)
                position = classskuObj.get_location_by_sku(ProductSKU)

                sellCount1 = 0 if (sellCount1 is None or sellCount1=='') else sellCount1
                number = number if (number is not None and  number!='') else 0
                reservationnum = reservationnum if (reservationnum is not None and reservationnum!='') else 0
                canSellCount = int(number)-int(reservationnum)
                packInfo = '' if packInfo is None else packInfo
                position = '' if position is None else position
                ShopSKU = str(col[4]).strip()
                ProductName = ''
                ProductImage = ''
                ProductPrice = 0.0
                ProductWeight = 0.0
                Supplier = ''
                Supplierlink = ''
                #获取商品图片、商品名称、商品成本价、商品重量、供应商链接、供应商名
                py_b_goods_objs = py_b_goods.objects.filter(SKU=ProductSKU)
                if py_b_goods_objs.exists():
                    ProductImage = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % py_b_goods_objs[0].SKU.replace(
                        'OAS-', '').replace('FBA-', '')
                    ProductName = py_b_goods_objs[0].GoodsName
                    ProductPrice = py_b_goods_objs[0].CostPrice
                    ProductWeight = py_b_goods_objs[0].Weight
                    Supplierlink = py_b_goods_objs[0].LinkUrl

                    py_b_Supplier_objs = py_b_Supplier.objects.filter(NID=py_b_goods_objs[0].SupplierID)
                    if py_b_Supplier_objs.exists():
                        Supplier = py_b_Supplier_objs[0].SupplierName
                #目的仓库
                Destination_warehouse = ''
                for warehouse in getChoices(ChoiceWarehouse):
                    if warehouse[1] is not None and str(col[0]).strip() == warehouse[1].strip():
                        Destination_warehouse = warehouse[0].strip()
                # 产品性质
                nature = 'generalcargo'
                from brick.pydata.py_syn.py_conn import py_conn
                pyconn = py_conn()
                sqlserverInfo = pyconn.py_conn_database()
                if sqlserverInfo['errorcode'] != 0:
                    raise Exception('普元库链接失败，请重新提交;')
                else:
                    strSql = "select AttributeName from B_GoodsAttribute where GoodsID = (select nid from B_Goods where SKU='%s')" % (
                        ProductSKU)
                    sqlserverInfo['py_cursor'].execute(strSql)
                    returnResult = sqlserverInfo['py_cursor'].fetchone()
                    if returnResult:
                        if str(returnResult[0]).replace(";", "") == u"其余违禁品":
                            nature = 'contraband'
                        elif str(returnResult[0]).replace(";", "") == u"纯电池商品":
                            nature = 'pureelectric'
                        elif str(returnResult[0]).replace(";", "") == u"内置电池商品" or str(returnResult[0]).replace(";", "") == u"带电商品" or str(returnResult[0]).replace(";", "") == u"纽扣电池商品":
                            nature = 'withelectric'
                        elif str(returnResult[0]).replace(";", "") == u"粉末商品" or str(returnResult[0]).replace(";", "") == u"其余化妆品":
                            nature = 'powderpaste'
                        elif str(returnResult[0]).replace(";", "") == u"带磁商品":
                            nature = 'withmagnetism'
                        elif str(returnResult[0]).replace(";", "") == u"液体商品":
                            nature = 'liquid'
                        elif str(returnResult[0]).replace(";", "") == u"普货":
                            nature = 'generalcargo'
                        else:
                            nature = 'specialclass'
                    else:
                        #raise Exception('从普元未关联到产品特性，需要对该商品在普元录入商品特性后再提交,')
                        nature = 'generalcargo'
                pyconn.py_close_conn_database()

                FBW_US = 'no'
                if str(col[6]).strip() == u'有':
                    FBW_US = 'have'
                deliver_way = 'normal'
                if str(col[8]).strip() == u'随机':
                    deliver_way = 'random'
                newold = 'old'
                if str(col[9]).strip() == u'新品':
                    newold = 'new'
                #采购数量
                Stocking_quantity = 0
                if str(col[5]).strip() != '':
                    Stocking_quantity = col[5]
                insertinto.append(t_stocking_demand_fbw(
                    Stocking_plan_number=Stocking_plan_number, Stock_plan_date=dattime.now(), ProductImage=ProductImage,Destination_warehouse=Destination_warehouse,
                    AccountNum=col[1],ProductID=col[2],
                    ProductSKU=ProductSKU,ShopSKU=ShopSKU,servenOrder=sellCount1,Stocking_quantity=Stocking_quantity,QTY=Stocking_quantity,
                    ProductPrice=ProductPrice,DemandMoney = int(Stocking_quantity)*float(ProductPrice),DeliverMoney=int(Stocking_quantity)*float(ProductPrice),
                    Remarks=col[7],Demand_people=user_name,FBW_US=FBW_US,canSellCount=canSellCount,Product_nature=nature,ProductName = ProductName,
                    ProductWeight = ProductWeight,packFormat=packInfo,position=position,OplogTime=dattime.now(),Status='notyet',deliver_way=deliver_way,newold=newold
                ))
                # refresh_fbw_list.append({'product_id': col[2], 'shopsku': ShopSKU, 'shopname': col[1]})
            except Exception, ex:
                result['errorcode'] = -1
                result['errortext'] = '第%d行存在问题:Exception:%s, ex:%s，请修正后重新上传' % (i + 1, Exception, ex)
                break
        if result['errorcode'] == 0:
            t_stocking_demand_fbw.objects.bulk_create(insertinto)
            #
            # for each in refresh_fbw_list:   # 刷新fbw备货数量
            #     refresh_fbw_flag(each['product_id'], each['shopsku'], each['shopname'], connection)  # 刷新fbw备货数量

    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = 'Exception = %s ex=%s,第%s行数据异常,请修改后重新上传%s。' % (Exception, ex,strLine,str(tmp))
    return result

@app.task
def import_excel_saler_profit_config_file(file_obj,user_name):
    import xlrd
    from skuapp.table.t_saler_profit_config import t_saler_profit_config
    from datetime import datetime as dattime
    #部门(0)  平台名称(1) 店铺名称（全称）(2) 业绩归属人(3)    统计月份(4)
    insertinto = []
    tmp = []
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
    table = wb.sheets()[0]
    row = table.nrows
    result = {'errorcode':0,'errortext':u'导入成功'}
    strLine = ""
    try:
        for i in xrange(1, row):
            try:
                col = table.row_values(i)
                insertinto.append(t_saler_profit_config(
                    Department=col[0], PlatformName=col[1], ShopName=col[2],SalerName=col[3],
                    StatisticsMonth=col[4],ImportMan=user_name,
                    ImportTime=dattime.now()
                ))
            except Exception, ex:
                result['errorcode'] = -1
                result['errortext'] = '第%d行存在问题:Exception:%s, ex:%s，请修正后重新上传' % (i + 1, Exception, ex)
                break
        if result['errorcode'] == 0:
            t_saler_profit_config.objects.bulk_create(insertinto)
    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = 'Exception = %s ex=%s,第%s行数据异常,请修改后重新上传%s。' % (Exception, ex,strLine,str(tmp))
    return result

@app.task
def generate_fba_delivery_invoices(idlist,user_name):
    import xlwt,os
    from django.db import connection
    from skuapp.table.t_stocking_demand_fba_deliver import t_stocking_demand_fba_deliver
    from skuapp.table.t_stocking_demand_fba import t_stocking_demand_fba
    from brick.table.t_overseas_warehouse_information import t_overseas_warehouse_information
    from pyapp.models import b_goods as py_b_goods
    from Project.settings import SBBL,MEDIA_ROOT,BUCKETNAME_overseas_warehouse_cargo_infor_xls
    from brick.public.create_dir import mkdir_p
    from datetime import datetime as datime
    from brick.public.upload_to_oss import upload_to_oss

    path = MEDIA_ROOT + 'download_xls/' + user_name
    mkdir_p(MEDIA_ROOT + 'download_xls')
    os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

    mkdir_p(path)
    os.popen('chmod 777 %s' % (path))

    for myid in idlist:
        t_stocking_demand_fba_deliver_obj = t_stocking_demand_fba_deliver.objects.filter(id = myid)
        t_overseas_warehouse_information_obj = t_overseas_warehouse_information(connection)
        if t_stocking_demand_fba_deliver_obj.exists():

            filename = user_name + '_' + datime.now().strftime('%Y%m%d%H%M%S') + '_' + str(myid) + '.xls'

            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
            style = xlwt.XFStyle()
            # 字体 宋体
            fnt = xlwt.Font()
            fnt.name = u'SimSun'
            style.font = fnt
            # 位置：居中
            alignment = xlwt.Alignment()  # Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style.alignment = alignment
            # 边框：实线
            borders = xlwt.Borders()
            borders.left = xlwt.Borders.THIN
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            style.borders = borders

            obj = t_overseas_warehouse_information_obj.get_overseas_warehouse_information(t_stocking_demand_fba_deliver_obj[0].Destination_warehouse)

            if obj:
                row = 0
                col = 0
                worksheet.write_merge(row, row + 0, col, col + 2, u'SHIPPER(发件人信息）', style)
                col = 3
                worksheet.write_merge(row, row + 0, col, col + 4, u'SHIP TO(收件人信息）', style)

                inforlist = [
                             {u'Contact Name/联系人姓名':['Luo Difei',obj[7]]},
                             {u'Company Name/公司名称':['Fancy',obj[8]]},
                             {u'Company Address(地址）':['NO.297,Qian Fang Road ',obj[1]]},
                             {u'City/城市':['Jin Hua',obj[2]]},
                             {u'StateProvince/洲省':['Zhe Jiang',obj[3]]},
                             {u'Postal Code(邮编）':['322200',obj[4]]},
                             {u'Country/国家':['China',obj[5]]},
                             {u'Telephone No/联系电话':['18072321653',obj[6]]},
                            ]
                for i in range(0,len(inforlist)):
                    for k,v in inforlist[i].items():
                        row = row + 1
                        col = 0
                        worksheet.write_merge(row, row + 0, col, col + 1, k, style)
                        col = 2
                        worksheet.write_merge(row, row + 0, col, col + 0, v[0], style)
                        col = 3
                        worksheet.write_merge(row, row + 0, col, col + 0, k, style)
                        col = 4
                        worksheet.write_merge(row, row + 0, col, col + 3, v[1], style)

                row = row + 1
                col = 0
                worksheet.write_merge(row, row + 0, col, col + 1, '', style)
                col = 2
                worksheet.write_merge(row, row + 0, col, col + 0, '', style)
                col = 3
                worksheet.write_merge(row, row + 0, col, col + 0, u'Odd number/原单号', style)
                col = 4
                worksheet.write_merge(row, row + 0, col, col + 3, u'%s'%t_stocking_demand_fba_deliver_obj[0].Warehouse_number, style)

                row = row + 1
                col = 0
                worksheet.write_merge(row, row + 0, col, col + 7, u'Cargo information/货 物 信 息', style)

                cargolist = [
                    [u'数量',u'计量单位/个/双',u'品名/Product Name',u'材质/Material',u'HS 编码',u'原产国',u'单价',u'总价'],
                ]
                pricenum = 0.0
                productskulist = t_stocking_demand_fba_deliver_obj[0].All_ProductSKU_Num.split(';')
                for prosku in productskulist:
                    if prosku.find('*') != -1:
                        py_b_goods_obj = py_b_goods.objects.filter(SKU=prosku.split('*')[0]).values('Unit','Material','CostPrice','AliasCnName','AliasEnName')
                        Unit      = ''
                        Material  = ''
                        CostPrice = 0.0
                        AliasCnName = ''
                        AliasEnName = ''
                        if py_b_goods_obj.exists():
                            Unit      = py_b_goods_obj[0]['Unit']
                            Material  = py_b_goods_obj[0]['Material']
                            CostPrice = py_b_goods_obj[0]['CostPrice']
                            AliasCnName = py_b_goods_obj[0]['AliasCnName']
                            AliasEnName = py_b_goods_obj[0]['AliasEnName']
                        price = float(CostPrice)/SBBL

                        pricenum = pricenum + (price * int(prosku.split('*')[1]))

                        skuinfo = [prosku.split('*')[1],Unit,AliasCnName + '/' + AliasEnName,Material,'','CN',
                                   '$' + '%.2f'%(price),
                                   '$' + '%.2f'%(price * int(prosku.split('*')[1]))]
                        cargolist.append(skuinfo)

                for cargo in cargolist:
                    row = row + 1
                    col = 0
                    for car in cargo:
                        worksheet.write_merge(row, row + 0, col, col + 0, car, style)
                        col = col + 1

                lastlist = [
                    [u'lump sum/总金额','$' + '%.2f'%(pricenum)],
                    [u'Number/件数',str(t_stocking_demand_fba_deliver_obj[0].BoxNum) + u'件'],
                    [u'Total Weight/总重量',str(t_stocking_demand_fba_deliver_obj[0].BoxWeight) + 'KG']
                ]
                col = 0
                row = row + 1
                channel = ''
                t_stocking_demand_fba_obj = t_stocking_demand_fba.objects.filter(Stocking_plan_number = t_stocking_demand_fba_deliver_obj[0].Stocking_plan_number.split('|')[0]).values('level')
                if t_stocking_demand_fba_obj.exists():
                    if t_stocking_demand_fba_obj[0]['level'].strip() == 'normal':
                        channel = u'船运'
                    elif t_stocking_demand_fba_obj[0]['level'].strip() == 'urgent':
                        channel = u'空运'
                    else:
                        channel = u'指定物流'
                worksheet.write_merge(row, row + 2, col, col + 3, channel, style)
                for i in range(3):
                    col = col + 4
                    worksheet.write_merge(row, row + 0, col, col + 2, lastlist[i][0], style)
                    col = col + 3
                    worksheet.write_merge(row, row + 0, col, col + 0, lastlist[i][1], style)
                    row = row + 1
                    col = 0

            workbook.save(path + '/' + filename)

            upload_to_oss_obj = upload_to_oss(BUCKETNAME_overseas_warehouse_cargo_infor_xls)
            myresult = upload_to_oss_obj.upload_to_oss({'path':user_name,'name':filename,'byte':open(path + '/' + filename),'del':1})
            if myresult['result'] != '':
                t_stocking_demand_fba_deliver_obj.update(Invoice = myresult['result'])

@app.task
def import_affiliate_excel_file(file_obj,user_name):
    import xlrd
    from reportapp.table.t_online_aliexpress_affiliate_rate import t_online_aliexpress_affiliate_rate as affiliate_model
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
    table = wb.sheets()[0]
    nrow = table.nrows
    result = {'errorcode': 0, 'errortext': u'导入成功'}
    try:
        insertinto = []
        pidlist = []
        if len(table.row_values(0)) != 9:
            raise Exception('Template error!')

        for i in range(1, nrow):
            try:
                row = table.row_values(i)
                ShopName = row[0].strip()
                ProductID = str(int(row[1]))
                Salesman = row[2].strip()
                Category = row[3].strip()
                IsAffiliateM = row[4].strip()
                if IsAffiliateM not in (u'是', u'否'):
                    raise TypeError(u'是否使用联盟营销 只能是(是, 否).')
                CRate = row[5]
                if float(CRate) >= 1.0:
                    raise TypeError('The commission rate should be less than 1')

                if isinstance(row[6], float):
                    JoinDate = xlrd.xldate.xldate_as_datetime(row[6], wb.datemode)
                else:
                    JoinDate = row[6]

                if isinstance(row[7], float):
                    ExitDate = xlrd.xldate.xldate_as_datetime(row[7], wb.datemode)
                else:
                    ExitDate = row[7]

                ActivityType = row[8].strip()

                insertinto.append(affiliate_model(ShopName=ShopName, Salesman=Salesman, Category=Category,
                                                  ProductID=ProductID, IsAffiliateM=IsAffiliateM, CRate=CRate,
                                                  JoinDate=JoinDate, ExitDate=ExitDate, UserName=user_name,
                                                  ActivityType=ActivityType)
                                  )

                pidlist.append(ProductID)
            except Exception, ex:
                result['errorcode'] = -1
                result['errortext'] = '解析第%d行时:Exception:%s，请修正后重新上传.' % (i + 1, repr(ex))
                break
        if result['errorcode'] == 0:
            affiliate_model.objects.filter(ProductID__in=pidlist).delete()  # 删除重复的，可以更新
            affiliate_model.objects.bulk_create(insertinto)
    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = 'Exception = %s,数据上传时异常,请检查后重新上传.' % (repr(ex),)

    return result

@app.task
def import_marketplan_excel_file(file_obj, user_name):
    import xlrd
    import datetime
    create_time = datetime.datetime.now().strftime('%Y-%m-%d')
    from skuapp.table.t_store_marketplan_execution_ebay import t_store_marketplan_execution_ebay as marketplan_model
    # 打开Excel文件读取数据 文件名以及路径，如果路径或者文件名有中文给前面加一个r拜师原生字符。
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())
    table = wb.sheets()[0]    # 通过索引顺序获取
    nrow = table.nrows        # 获取该sheet中的有效行数
    result = {'errorcode': 0, 'errortext': u'导入成功'}
    try:
        insertinto = []
        # table.row_values(rowx, start_colx=0, end_colx=None)  # 返回由该行中所有单元格的数据组成的列表
        if len(table.row_values(0)) != 5:
            raise Exception('Template error!')

        for i in range(1, nrow):
            try:
                row = table.row_values(i)
                platform = row[0].strip()
                shop_account = row[1].strip()
                product_code = str(int(row[2]))
                product_sku = row[3].strip()
                execution_count = row[4]

                insertinto.append(marketplan_model(createman=user_name, create_time=create_time, platform=platform,
                                                   shop_account=shop_account, product_code=product_code, product_sku=product_sku,
                                                   execution_count=execution_count
                                                   )
                                  )

            except Exception, ex:
                result['errorcode'] = -1
                result['errortext'] = '解析第%d行时:Exception:%s，请修正后重新上传.' % (i + 1, repr(ex))
                break
        if result['errorcode'] == 0:
            # model.objects.bulk_create(数据)  批量插入数据，django1.4之后加入的特性，比save性能更好
            marketplan_model.objects.bulk_create(insertinto)
    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = 'Exception = %s,数据上传时异常,请检查后重新上传.' % (repr(ex),)

    return result

@app.task
def import_SnL_excel_file(file_obj,user_name):
    from django.contrib import messages
    import xlrd
    from skuapp.table.t_amazon_SnL_record import t_amazon_SnL_record as SnL_modle
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
    table = wb.sheets()[0]
    nrow = table.nrows
    result = {'errorcode': 0, 'errortext': u'导入成功'}

    try:

        if len(table.row_values(0)) != 11:
            raise Exception('Template error!')
        insertinto = []
        splist = []

        for i in xrange(1, nrow):
            try:
                row = table.row_values(i)
                shopname = row[0].strip()
                seller = row[1].strip()
                sku = row[2].strip()
                fnsku = row[3].strip()
                asin = row[4].strip()
                productname = row[5].strip()
                SnL = row[6].strip()
                marketplace = row[7].strip()
                Price = row[8]
                SnL_Inventory = row[9]
                Non_SnL_Inventory = row[10]

                insertinto.append(SnL_modle(shopname=shopname,seller=seller,sku=sku,fnsku=fnsku,asin=asin,
                                            productname=productname,SnL=SnL,marketplace=marketplace,Price=Price,
                                            SnL_Inventory=SnL_Inventory,Non_SnL_Inventory=Non_SnL_Inventory

                                              ))
                splist.append((shopname, sku))

            except Exception, ex:
                result['errorcode'] = -1
                result['errortext'] = '解析第%d行时:Exception:%s，请修正后重新上传.' % (i + 1, repr(ex))
                break
        if result['errorcode'] == 0:
            for v in splist:
                SnL_modle.objects.filter(shopname=v[0], sku=v[1]).delete()

            SnL_modle.objects.bulk_create(insertinto)

    except Exception, ex:
        result['errorcode'] = -1
        result['errortext'] = 'Exception = %s,数据上传时异常,请检查后重新上传.' % (repr(ex),)

    return result
	
def get_shopsku_sku_excel(idlist,user_name,downid):
    import os
    from Project.settings import MEDIA_ROOT,BUCKETNAME_DOWNLOAD
    from brick.public.generate_excel import generate_excel
    from brick.public.upload_to_oss import upload_to_oss
    from datetime import datetime as datime
    from skuapp.table.t_use_productsku_apply_for_shopsku import t_use_productsku_apply_for_shopsku
    from skuapp.table.t_download_info import t_download_info
    from brick.public.create_dir import mkdir_p

    objs = t_use_productsku_apply_for_shopsku.objects.filter(id__in=idlist)
    path = MEDIA_ROOT + 'download_xls/' + user_name
    mkdir_p(MEDIA_ROOT + 'download_xls')
    os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
    mkdir_p(path)
    os.popen('chmod 777 %s' % (path))
    filename = user_name + '_' + datime.now().strftime('%Y%m%d%H%M%S') + '.xls'
    mysheetlist = [u'ProductSKU', u'ShopSKU', u'ShopName', u'PersonCode']
    datalist = [mysheetlist]
    for obj in objs:
        datalist.append([obj.ProductSKU,'%s' % obj.ShopSKU,obj.ShopName,user_name])
    genresult = generate_excel(datalist,path + '/' + filename)
    if genresult['code'] == 0:
        os.popen(r'chmod 777 %s' % (path + '/' + filename))
        upload_to_oss_obj = upload_to_oss(BUCKETNAME_DOWNLOAD)
        uploadresult = upload_to_oss_obj.upload_to_oss(
            {'path': user_name, 'name': filename, 'byte': open(path + '/' + filename), 'del': 1})
        if uploadresult['result'] != '':
            t_download_info.objects.filter(id=downid).update(appname=user_name + '/' + filename,
                                                             updatetime=datime.now())
            objs.update(EStatus='yes')
        else:
            objs.update(EStatus='error')
    else:
        objs.update(EStatus='error')
        
        
        
        
@app.task
def get_shopsku_sku_forthwith_excel(idlist,user_name):
    import os
    from Project.settings import MEDIA_ROOT,BUCKETNAME_XLS
    from brick.public.generate_excel import generate_excel
    from brick.public.upload_to_oss_forthwith import upload_to_oss_forthwith
    from datetime import datetime as datime
    from skuapp.table.t_use_productsku_apply_for_shopsku import t_use_productsku_apply_for_shopsku
    #from skuapp.table.t_download_info import t_download_info
    from brick.public.create_dir import mkdir_p

    objs = t_use_productsku_apply_for_shopsku.objects.filter(id__in=idlist)
    path = MEDIA_ROOT + 'download_xls/' + user_name
    mkdir_p(MEDIA_ROOT + 'download_xls')
    os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
    mkdir_p(path)
    os.popen('chmod 777 %s' % (path))
    filename = user_name + '_' + datime.now().strftime('%Y%m%d%H%M%S') + '.xls'
    mysheetlist = [u'ProductSKU', u'ShopSKU', u'ShopName', u'PersonCode']
    datalist = [mysheetlist]
    for obj in objs:
        datalist.append([obj.ProductSKU,'%s' % obj.ShopSKU,obj.ShopName,user_name])
        print 'datalist#$#$#$$$$$$$$$$$$$%s'%datalist
    genresult = generate_excel(datalist,path + '/' + filename)
    print 'genresult#$#$#$#$$$$$$$$$$$##＃＃＃%s' % genresult


    if genresult['code'] == 0:
        print '0000000000000000000000'
        os.popen(r'chmod 777 %s' % (path + '/' + filename))
        upload_to_oss_forthwith_obj = upload_to_oss_forthwith(BUCKETNAME_XLS)
        uploadresult = upload_to_oss_forthwith_obj.upload_to_oss_forthwith(
            {'path': user_name, 'name': filename, 'byte': open(path + '/' + filename), 'del': 1})
        print 'uploadresult--------------',uploadresult

        if uploadresult['result'] != '':
            objs.update(EStatus='yes')
        else:
            objs.update(EStatus='error')
    else:
        objs.update(EStatus='error')



@app.task
def  get_trackno_amazon_india(params):
        from django.db import connection
        from brick.amazon.get_info_api.api_order_apply_trackno_amazon_india import AMZTrackApiSchedule
        AMZTrackApiScheduleImp = AMZTrackApiSchedule(connection)
        i = 0
        result_code = {}
        this_code = {}
        for param in params:
            i += 1
            this_code = AMZTrackApiScheduleImp.start_apply(param)
            result_code['result%s' % i] = this_code
        if i > 1:
            return result_code
        else:
            return this_code

@app.task          
def wish_product_off_shelf_task(file_obj, now_time, first_name, reason):
    """wish商品上下架"""
    from brick.wish.wish_product_off_shelf import wish_product_shelf_enter
    wish_product_shelf_enter(file_obj, now_time, first_name, reason)


@app.task
def syn_Logistics_number(numlist):
    from django.db import connection
    from brick.table.cg_stockorderm import cg_stockorderm
    from skuapp.table.t_stocking_purchase_order import t_stocking_purchase_order

    objs = t_stocking_purchase_order.objects.filter(Single_number__in=numlist)
    cg_stockorderm_obj = cg_stockorderm(connection)
    for num in numlist:
        ali_log = cg_stockorderm_obj.get_Logistics_number_Single_number(num)
        if ali_log:
            objs.filter(Single_number=num).update(Ali_number=ali_log[0],LogisticsNumber=ali_log[1])



@app.task
def ebay_distribution(id,request_user):
    from django.db import connection
    from brick.ebay.ebay_distribution import ebay_unfold_distribution
    """ebay铺货数据处理"""
    ebay_unfold_distribution(id, connection, request_user)
    pass

@app.task
def wish_distribution_statistics_task():
    """wish铺货统计"""
    from brick.wish.wish_distribution_statistics import WishDistributionStatistics
    WishDistributionStatistics_obj = WishDistributionStatistics()
    result_params, sales_params, total_params = WishDistributionStatistics_obj.handle_data()
    WishDistributionStatistics_obj.insert_into_table(result_params, sales_params, total_params)


@app.task
def wish_order_syn_task():
    from brick.chart.wish_order_syn import wish_order_syn
    wish_order_syn()

@app.task
def saleman_registration_task():
    from brick.chart.saleman_registration import saleman_registration
    saleman_registration()
    
from brick.amazon.feed_Amazon_trackNo.feed_Amazon_trackNo import *
from brick.table.t_order_amazon_india import *
@app.task
def Amazon_india_auto_feed_trackNo():
    feed_Amazon_trackNo_tmp = feed_Amazon_trackNo(connection)
    t_order_amazon_india_tmp = t_order_amazon_india(connection)
    shopNames = t_order_amazon_india_tmp.get_Amazon_shopName_for_feed()
    order_item_infos = t_order_amazon_india_tmp.get_Amazon_order_id_for_feed()
    for shopName in shopNames:
        new_order_item_infos = []
        amazonOrderIds = []
        for order_item_info in order_item_infos:
            if order_item_info['ShopName'] == shopName['ShopName']:
                new_order_item_infos.append(order_item_info)
                amazonOrderIds.append(order_item_info['AmazonOrderId'])
        feed_dict = {'order_item_infos': new_order_item_infos, 'shopName': shopName['ShopName']}
        feed_Amazon_trackNo_tmp.deal_Amazon_trackNo_to_schedule(feed_dict)
        t_order_amazon_india_tmp.update_status_and_warning(amazonOrderIds)

@app.task
def refresh_trackinfo_by_CNI():
    from brick.table.t_order_track_info_amazon_india import  t_order_track_info_amazon_india
    from brick.amazon.get_info_api.refresh_amazon_india_trackinfo import AMZTrackApiSchedule
    t_order_track_info_amazon_india_Imp = t_order_track_info_amazon_india(connection)
    trackNumbers = t_order_track_info_amazon_india_Imp.get_trackNo_list()
    AMZTrackApiScheduleImp = AMZTrackApiSchedule()
    AMZTrackApiScheduleImp.searchTrackInfo(trackNumbers=trackNumbers)

@app.task
def update_trackinfo_warning():
    from brick.amazon.get_info_api import update_amazon_trackinfo_warning
    update_amazon_trackinfo_warning.update_warning_api()

@app.task
def order_out_of_stock_task(file_obj, now_time, first_name, plateform):
    from brick.chart.order_out_of_stock import order_out_of_stock
    order_out_of_stock(file_obj, now_time, first_name, plateform)
    

@app.task
def import_excel_file_paypal_tort(file_obj):
    from django.contrib import messages
    import xlrd
    from skuapp.table.paypal_tort import paypal_tort
    from skuapp.table.public import *
    import re

    insertinto = []
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里

    table = wb.sheets()[0]
    row = table.nrows

    try:
        for i in xrange(1, row):
            col = table.row_values(i)
            Brand = col[0].strip()
            GraphicTrademark = ''
            Site=col[2].strip()
            Category = col[3].strip()

            insertinto.append(paypal_tort(Brand=Brand,GraphicTrademark=GraphicTrademark,
                                                  Site=Site,Category=Category
            ))
        paypal_tort.objects.bulk_create(insertinto)
    except IOError:
        messages.error(request,"导入失败！")


@app.task
def import_excel_file_aliexpress(file_obj,user_name):
    import pymssql
    from django.contrib import messages
    import xlrd
    from skuapp.table.t_aliexpress_refund import t_aliexpress_refund
    from skuapp.table.public import *
    from datetime import datetime
    import  re
    # from django.db import connection
    insertinto = []
    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
    table = wb.sheets()[0]
    row = table.nrows
    try:
        result = {}
        db_conn = sqlserver_conn = pymssql.connect(host='122.226.216.10', user='fancyqube', password='K120Esc1',
                                                   database='ShopElf',
                                                   port='18794')
        if db_conn:
            cursor = db_conn.cursor()

            for i in xrange(1,row):
                col = table.row_values(i)
                ShopOrderNumber = str(col[1]).strip()
                CorrespondingSalesNumber = ''
                RefundsType=u'物流问题'
                AfterSaleType = u'物流问题'
                MainTableRemark = ''
                ShopSKU=''
                SKU = ''
                QuantityOfGoods = 1

                O_AmountOfMoney = str(col[6]).strip()
                AmountOfMoney  = O_AmountOfMoney.split('-')[1]
                L_NUMBER = str(col[3]).strip()
                FineMeterRemark=''
                RedirectCustomerServiceReason=u'W003-物流未收到'
                ShopName = ''
                ImportTime=''
                ExportTime=''

                cursor.execute(
                    "SELECT b.SKU FROM P_Trade a,P_TradeDt b WHERE a.NID = b.TradeNID AND a.ACK  = '%s' and b.L_NUMBER = '%s'" % (
                    ShopOrderNumber, L_NUMBER))

                t_sku_tmp = cursor.fetchone()
                if t_sku_tmp:
                    t_sku = t_sku_tmp[0]
                else:
                    t_sku=1
                SKU = t_sku
                
                if SKU == 1:
                    cursor.execute(
                    "SELECT b.SKU FROM P_Trade_His a,P_TradeDt_His b WHERE a.NID = b.TradeNID AND a.ACK  = '%s' and b.L_NUMBER = '%s'" % (
                    ShopOrderNumber, L_NUMBER))

                    t_sku_tmp = cursor.fetchone()
                    if t_sku_tmp:
                        t_sku = t_sku_tmp[0]
                    else:
                        t_sku=1
                    SKU = t_sku
                
                if SKU == 1:
                    cursor.execute(
                    "SELECT b.SKU FROM P_TradeUn a,P_TradeDtUn b WHERE a.NID = b.TradeNID AND a.ACK  = '%s' and b.L_NUMBER = '%s'" % (
                    ShopOrderNumber, L_NUMBER))

                    t_sku_tmp = cursor.fetchone()
                    if t_sku_tmp:
                        t_sku = t_sku_tmp[0]
                    else:
                        t_sku=None
                    SKU = t_sku


                if SKU:
                    insertinto.append(t_aliexpress_refund(
                        ShopOrderNumber=ShopOrderNumber, CorrespondingSalesNumber=CorrespondingSalesNumber,RefundsType=RefundsType,
                        AfterSaleType=AfterSaleType, MainTableRemark=MainTableRemark, ShopSKU=ShopSKU,SKU=SKU, QuantityOfGoods=QuantityOfGoods,
                        AmountOfMoney=AmountOfMoney,ImportTime=datetime.now(),ImportPerson=user_name,ExportState=u'未导出',
                        FineMeterRemark=FineMeterRemark, RedirectCustomerServiceReason=RedirectCustomerServiceReason
                    ))
                else:
                    print("没有对应的SKU！")


            t_aliexpress_refund.objects.bulk_create(insertinto)
        if cursor:
            cursor.close()
        result['errorcode'] = 1
        result['errortext'] = "SUCCESS"
    except pymssql.Error, e:
        result['errorcode'] = 26666
        result['errortext'] = "sqlserver Error:%s" %(str(e))
    except Exception as ex:
        result['errorcode'] = -1
        result['errortext'] = "other error:%s" %(str(ex))
    finally:
        db_conn.close()

    return result




# Wish店铺管理--按照listID同步数据、上架、下架
@app.task
def syndata_by_wish_api(list, flag, synname='', warehouse='STANDARD', opPerson=''):
    from django.db import connection
    from brick.wish.wish_store import Wish_Data_Syn,OnTheShelf_OR_LowerFrame, \
        download_excel_by_porductid, to_wait_publish, MainBatchUpdateShipping
    from brick.table.t_wish_store_oplogs import t_wish_store_oplogs
    from brick.table.t_online_info_wish import t_online_info_wish

    t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
    t_online_info_wish_obj = t_online_info_wish(connection)

    sResult = None
    if flag == 'syn':  # 同步数据
        sResult = Wish_Data_Syn(list, synname)
    elif flag == 'enable' or flag == 'disable':
        sResult = OnTheShelf_OR_LowerFrame(list, flag, synname)
    elif flag == 'download':
        sResult = download_excel_by_porductid(list, synname, warehouse)
    elif flag == 'topub':  # 现有链接转  待刊登
        sResult = to_wait_publish(list, synname, opPerson)
    elif flag == 'BU_Shipping':
        sResult = MainBatchUpdateShipping(list, synname, warehouse)

    if sResult:
        if sResult['Code'] == -1 and flag != 'download':
            t_online_info_wish_obj.UpdateWishStatusAD(list[1], '-2')  # 程序异常
            t_wish_store_oplogs_obj.updateStatusP(synname, list[1], 'error', sResult['messages'])
        if sResult['Code'] == -1 and flag == 'download':
            t_wish_store_oplogs_obj.updateStatusP(synname, synname, 'error', sResult['messages'])
        return sResult
        
        
@app.task        
def get_lazada_product(ip,appkey, appsecret,site,username):
    from brick.lazada.get_products_info import get_products_info
    get_products_info(ip, appkey, appsecret).get_products_by_site(site=site,username=username)


# def wish_en_dis(flag,params,obj,cwishapi_obj,classlisting_obj,classshopsku_obj,
#                 t_online_info_obj,sresult,comparison_obj,logobjs):
#     from django.db.models import F
#     import json
#     from django.db import connection
#     from brick.table.t_store_configuration_file import t_store_configuration_file
#     t_store_configuration_file_obj = t_store_configuration_file(connection)
#
#     if flag == 'enable':
#         Status = 'Enabled'
#         result = cwishapi_obj.enable_by_wish_api(params)
#     else:
#         Status = 'Disabled'
#         result = cwishapi_obj.disable_by_wish_api(params)
#
#     _content = eval(result._content)
#     if result.status_code == 200 and _content['code'] == 0:
#         obj.Status = Status
#         obj.save()
#         shopskulist = classlisting_obj.getShopSKUList(obj.ProductID)
#         if shopskulist is None:
#             shopskulist = []
#         for shopsku in shopskulist:
#             classshopsku_obj.setStatus(shopsku, Status)
#         t_online_info_obj.update_status_by_productid(Status, obj.ProductID)
#         sresult['Code'] = 1
#         t_store_configuration_file_obj.update_shopStatus('0', obj.ShopName)
#         if logobjs.exists():
#             logobjs.update(rNum=F('rNum') + 1)
#     else:
#         sresult['messages'] = '%s' % _content
#         if _content.get('code') == 2000 :
#             t_store_configuration_file_obj.update_shopStatus('-1', obj.ShopName)
#
#         BL = comparison_obj.get_bl_by_code(_content.get('code'))
#         if BL is None:
#             comparison_obj.insert_code_message(
#                 _content.get('code'), _content.get('message')
#             )
#             BL = _content.get('message')
#         if _content.get('code') is None:
#             BL = '%s' % _content
#         if logobjs.exists():
#             elogL = json.loads(logobjs[0].elogs)
#             elogL.append({'key': obj.ProductID, 'mag': BL})
#
#             logobjs.update(eNum=F('eNum') + 1, elogs=json.dumps(elogL))
#
#     return sresult
#
#
# def wish_syn(cwishapi_obj,params,t_online_info_obj,sresult,
#              logobjs,comparison_obj,obj,classlisting_obj):
#     import json
#     from brick.classredis.classlisting import classlisting
#     from django.db import connection
#     from django.db.models import F
#     from brick.table.t_store_configuration_file import t_store_configuration_file
#
#
#     t_store_configuration_file_obj = t_store_configuration_file(connection)
#
#     upresult = cwishapi_obj.update_wish_goods_data(params)
#     _content = eval(upresult._content)
#     if upresult.status_code == 200 and _content['code'] == 0:  # api 调用成功
#         myresult = t_online_info_obj.insertWishV2([_content.get('data', '')])  # 更新到t_online_info
#         sresult['Code'] = 1
#         t_store_configuration_file_obj.update_shopStatus('0', obj.ShopName)
#         if logobjs.exists():
#             logobjs.update(rNum=F('rNum') + 1)
#
#     else:  # 如果失败也更新一次redis下的所属店铺SKU
#         sresult['messages'] = '%s' % _content
#         if _content.get('code') == 2000 : # 店铺状态异常
#             t_store_configuration_file_obj.update_shopStatus('-1', obj.ShopName)
#
#         BL = comparison_obj.get_bl_by_code(_content.get('code'))
#         if BL is None:
#             comparison_obj.insert_code_message(
#                 _content.get('code'), _content.get('message')
#             )
#             BL = _content.get('message')
#         if _content.get('code') is None:
#             BL = '%s' % _content
#         if logobjs.exists():
#             elogL = json.loads(logobjs[0].elogs)
#             elogL.append({'key': obj.ProductID, 'mag': (u'%s'%BL).encode('utf-8')})
#
#             logobjs.update(eNum=F('eNum') + 1, elogs=json.dumps(elogL))
#
#         # 更新下 redis中shopskulist
#         classlisting_db = classlisting(db_conn=connection)
#         all_shopsku = classlisting_db.getShopSKUList(obj.ProductID)
#         classlisting_obj.setShopSKUList(obj.ProductID, '|'.join(all_shopsku))
#     return sresult

# Wish店铺管理--按店铺同步全量数据
@app.task
def syndata_by_wish_api_shopname(ShopName,flag):

    from django.db import connection
    from datetime import datetime
    from brick.wish.ShopOnlineInfo import F_EXE_SHOP_ONLINE_INFO
    from brick.classredis.classshopname import classshopname
    from django_redis import get_redis_connection
    redis_coon = get_redis_connection(alias='product')

    obj = {}
    obj['ShopName']         = ShopName
    obj['PlatformName']     = 'Wish'
    obj['CMDID']            = ['GetListOrders','GetShopSKUInfo']
    obj['ScheduleTime']     = datetime.now()
    obj['ActualBeginTime']  = datetime.now()
    obj['ActualEndTime']    = ''
    obj['Status']           = 0
    obj['ProcessingStatus'] = ''
    obj['Processed']        = 0
    obj['Successful']       = 0
    obj['WithError']        = 0
    obj['WithWarning']      = 0
    obj['TransactionID']    = ''
    obj['InsertTime']       = datetime.now()
    obj['UpdateTime']       = datetime.now()
    obj['Params']           = ''
    obj['Timedelta']        = 0
    obj['RetryCount']       = 0
    obj['pid']              = ''
    obj['cmdtext']          = ''
    obj['errorinfo']        = ''

    classshopname_obj = classshopname(redis_cnxn=redis_coon)
    if flag == 0:
        classshopname_obj.set_api_status_by_shopname(ShopName, u'正在(全量)刷新 时间较长')
    else:
        classshopname_obj.set_api_status_by_shopname(ShopName, u'正在(增量)刷新 稍稍等待')

    F_EXE_SHOP_ONLINE_INFO(connection, obj, flag)  # 0 全量更新 1 增量更新

    classshopname_obj.del_api_status_by_shopname(ShopName)
# 海外仓--获取物流单号
@app.task
def syn_Logistics_number(numlist):
    from django.db import connection
    from brick.table.cg_stockorderm import cg_stockorderm
    from skuapp.table.t_stocking_purchase_order import t_stocking_purchase_order

    objs = t_stocking_purchase_order.objects.filter(Single_number__in=numlist)
    cg_stockorderm_obj = cg_stockorderm(connection)
    for num in numlist:
        ali_log = cg_stockorderm_obj.get_Logistics_number_Single_number(num)
        if ali_log:
            objs.filter(Single_number=num).update(Ali_number=ali_log[0],LogisticsNumber=ali_log[1])

# Wish店铺管理--ShopSKU上下架
@app.task
def update_status_by_shopsku_func(shopsku,shopname,flag,flagname=''):
    from django.db import connection
    from brick.wish.wish_store import OnTheShelf_OR_LowerFrame_BY_ShopSKU
    from brick.table.t_wish_store_oplogs import t_wish_store_oplogs
    from brick.table.t_online_info_wish import t_online_info_wish
    from brick.table.t_online_info import t_online_info
    t_online_info_obj = t_online_info(shopname, connection)

    t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
    t_online_info_wish_obj = t_online_info_wish(connection)

    oResult = OnTheShelf_OR_LowerFrame_BY_ShopSKU(shopsku,shopname,flag,flagname)
    if oResult['Code'] == -1:
        proinfo = t_online_info_obj.get_listingid_by_shopname_shopsku(shopsku)
        if proinfo['errorcode'] == 0:
            return oResult
        t_online_info_wish_obj.UpdateWishStatusAD(proinfo['productid'], '-2')
        t_wish_store_oplogs_obj.updateStatusP(flagname, shopsku, 'error', oResult['messages'])

    return oResult

# 非正常产品下架、产品下架
@app.task
def product_and_bottom_shelf_func(par_list,user_name,flag):
    from django.db import connection
    from datetime import datetime as logtime
    from brick.table.t_wish_product_sku_upload_or_not_log import t_wish_product_sku_upload_or_not_log
    from skuapp.table.t_goods_shelves import t_goods_shelves

    if flag == 'enshopsku':
        status = 'Enabled'
    else:
        status = 'Disabled'

    t_wish_product_sku_upload_or_not_log_obj = t_wish_product_sku_upload_or_not_log(connection)
    for par in par_list:
        t_goods_shelves.objects.filter(id=par[0]).update(APIState='runing')
        api_result = update_status_by_shopsku_func(par[2], par[1], flag)
        result_status = ''
        if api_result['code'] == 0:
            t_goods_shelves.objects.filter(id=par[0]).update(APIState='nothing',Status=status,Error=api_result['content'])
            result_status = 'success'
        if api_result['code'] == 1:
            t_goods_shelves.objects.filter(id=par[0]).update(APIState='Error',Error=api_result['content'])
            result_status = 'error'

        log_par = {}
        log_par['SKU']     = par[3]
        log_par['ShopSKU'] = par[2]
        log_par['Type']    = flag
        log_par['Person']  = user_name
        log_par['Time']    = logtime.now()
        log_par['Status']  = result_status

        t_wish_product_sku_upload_or_not_log_obj.insert_data(log_par)

# Wish店铺管理--更新listID的详细信息
@app.task
def update_goods_information_by_wish_api(datadict,ShopName,flagname):
    from django.db import connection
    from brick.wish.wish_store import edit_GoodsInformation_by_ID
    from brick.table.t_wish_store_oplogs import t_wish_store_oplogs
    from brick.table.t_online_info_wish import t_online_info_wish

    t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)
    t_online_info_wish_obj = t_online_info_wish(connection)

    eResult = edit_GoodsInformation_by_ID(datadict,ShopName,flagname)
    if eResult['Code'] == -1:
        t_online_info_wish_obj.UpdateWishStatusAD(datadict['id'], '-2')
        t_wish_store_oplogs_obj.updateStatusP(flagname, datadict['id'], 'error', eResult['messages'])
    return eResult



@app.task
def amazon_product_refresh(shop_sku, refresh_type):
    import traceback
    try:
        from django.db import connection
        from brick.amazon.product_refresh.get_auth_info import GetAuthInfo
        from brick.amazon.product_refresh.generate_feed_xml import GenerateFeedXml
        from brick.amazon.product_refresh.put_refresh_message_to_rabbitmq import MessageToRabbitMq
        get_auth_info_ins = GetAuthInfo(connection)
        for key, value in shop_sku.items():
            auth_info = get_auth_info_ins.get_auth_info_by_shop_name(str(key))
            auth_info['table_name'] = 't_online_info_amazon'
            auth_info['update_type'] = refresh_type
            auth_info['product_list'] = value

            if refresh_type == 'load_product':
                feed_xml_ins = GenerateFeedXml(auth_info)
                feed_xml = feed_xml_ins.get_inventory_xml(value, 999)
            elif refresh_type == 'unload_product':
                feed_xml_ins = GenerateFeedXml(auth_info)
                feed_xml = feed_xml_ins.get_inventory_xml(value, 0)
            else:
                feed_xml = None

            auth_info['feed_xml'] = feed_xml
            put_message_ins = MessageToRabbitMq(auth_info, connection)
            put_message_ins.put_message(str(auth_info))
    except Exception as e:
            print e
            traceback.print_exc(file=open('/tmp/task.log', 'a'))

from brick.amazon.deal_with_amazon_upload import deal_with_amazon_upload
from brick.table.t_templet_amazon_wait_upload import t_templet_amazon_wait_upload
from brick.table.t_templet_amazon_published_variation import t_templet_amazon_published_variation
@app.task
def stitch_goods_info(params):
    amazon_upload_obj_id = params['obj_id']
    templet_amazon_upload_result_id = params['templet_amazon_upload_result_id']
    t_templet_amazon_wait_upload_obj = t_templet_amazon_wait_upload(connection)
    t_templet_amazon_published_variation_obj = t_templet_amazon_published_variation(connection)
    t_templet_amazon_wait_upload_goods = t_templet_amazon_wait_upload_obj.get_amazon_wait_upload_goods_info_by_id({'id': amazon_upload_obj_id})
    t_templet_amazon_published_variation_goods = t_templet_amazon_published_variation_obj.get_variation_info_by_publish_goods(
        {'parent_item_sku': t_templet_amazon_wait_upload_goods['productSKU'], 'prodcut_variation_id': t_templet_amazon_wait_upload_goods['prodcut_variation_id']}
    )
    paramMQ = {'templet_amazon_upload_result_id': templet_amazon_upload_result_id, 'templet_amazon_wait_upload_obj': t_templet_amazon_wait_upload_goods,
               'auth_info': params['auth_info'], 'MQ_dict': params['MQ_dict'], 'variation': params['variation'], 'skuCount': params['skuCount'],
               't_templet_amazon_published_variation_objs': t_templet_amazon_published_variation_goods, 'user': params['user'],
               'shopName': params['shops'], 'amazon_upload_obj_id': amazon_upload_obj_id, 'link_sku_list': params['link_sku_list']}
    deal_with_amazon_upload_obj = deal_with_amazon_upload(connection)
    deal_with_amazon_upload_obj.deal_with_amamzon_upload(paramMQ)

@app.task
def order_out_of_stock_statistics_task(start_date, end_date, username, schedule_name):
    from brick.chart.order_out_of_stock_statistics import order_out_of_stock_statistics
    order_out_of_stock_statistics(start_date, end_date, username, schedule_name)

@app.task
def update_joom_goods_category_task():
    from brick.joom.update_joom_goods_category import update_joom_goods_category
    update_joom_goods_category()

@app.task
def wish_order_profit_task():
    from brick.chart.wish_order_profit import wish_order_profit
    wish_order_profit()

@app.task
def amazon_reverse_collection(reverse_info):
    from django.db import connection
    from brick.amazon.get_info_api.get_product_info_by_url import GetProductInfoByUrl
    get_info_obj = GetProductInfoByUrl(connection)
    for info in reverse_info:
        pri_key_id = info[0]
        url = info[1]
        get_info_obj.read_amazon(pri_key_id, url)
        
@app.task
def wish_advertisement_statistics_task():
    from brick.chart.wish_advertisement_statistics import wish_advertisement_statistics
    wish_advertisement_statistics()

@app.task
def wish_product_off_shelf(sku, reason, original_param):
    """
    WISH商品下架
    :param sku: 店铺sku或者商品sku
    :param reason: 下架原因
    :param original_param: 参数
    :return:
    """
    import copy
    from brick.wish.wish_product_off_shelf import get_shopname_shopsku_info, disable_detail_processing
    try:
        # 未绑定情况下，使用shopsku+shopname下架
        if reason == 'wbd':
            param = copy.deepcopy(original_param)
            param[2] = sku[0]

            shopsku_infos = get_shopname_shopsku_info(sku, 'shopsku')
            print 'shopsku:%s-----shopsku_infos-----------%s' % (sku, str(shopsku_infos))

            disable_detail_processing(param, shopsku_infos, 'shopsku', reason)

        # 清仓或者可卖天数小于7的下架，使用productsku下架
        else:
            param = copy.deepcopy(original_param)
            param[1] = sku[0]

            shopsku_infos = get_shopname_shopsku_info(sku, 'productsku')
            print 'productsku:%s----shopsku_infos-----------%s' % (sku, str(shopsku_infos))

            disable_detail_processing(param, shopsku_infos, 'productsku', reason)
    except:
        pass

@app.task
def wish_product_on_shelf(sku, reason, original_param):
    """
    根据店铺sku进行上架
    :param sku:
    :param reason:
    :param original_param:
    :return:
    """
    import copy
    from brick.wish.wish_product_off_shelf import get_shopname_shopsku_info, disable_detail_processing
    try:
        param = copy.deepcopy(original_param)
        param[2] = sku[0]

        shopsku_infos = get_shopname_shopsku_info(sku, 'shopsku')
        print 'shopsku:%s-----shopsku_infos-----------%s' % (sku, str(shopsku_infos))

        disable_detail_processing(param, shopsku_infos, 'shopsku', reason)
    except:
        pass

@app.task
def wish_product_off_shelf_urgent(sku, reason, original_param):
    """
    紧急下架：shopsku+shopname下架 或者 productsku下架
    :param sku:
    :param reason:
    :param original_param:
    :return:
    """
    import copy
    from brick.wish.wish_product_off_shelf import get_shopname_shopsku_info, disable_detail_processing
    try:
        # 未绑定情况下，使用shopsku+shopname下架
        if reason == 'urgent_off_shopsku':
            param = copy.deepcopy(original_param)
            param[2] = sku[0]

            shopsku_infos = get_shopname_shopsku_info(sku, 'shopsku')
            print 'shopsku:%s-----shopsku_infos-----------%s' % (sku, str(shopsku_infos))

            disable_detail_processing(param, shopsku_infos, 'shopsku', reason)

        # 清仓或者可卖天数小于7的下架，使用productsku下架
        else:
            param = copy.deepcopy(original_param)
            param[1] = sku[0]

            shopsku_infos = get_shopname_shopsku_info(sku, 'productsku')
            print 'productsku:%s----shopsku_infos-----------%s' % (sku, str(shopsku_infos))

            disable_detail_processing(param, shopsku_infos, 'productsku', reason)
    except:
        pass

# Joom店铺管理--按照listID同步数据、上架、下架
@app.task
def syndata_by_joom_api(productidlist, shopname, flag):
    from brick.joom.Joom_Get_Products_Client import Joom_Get_Products_Client
    sresult = {'Code':0,'messages':''}
    for product_id in productidlist:
        if flag == 'syn':
            Joom_Get_Products_Client(shop_name=shopname, product_id=product_id, flag=0)
    sresult['Code'] = 1
    sresult['messages'] = u'正在更新'
    return sresult

# Joom店铺管理--按店铺同步全量数据
@app.task
def syndata_by_joom_api_shopname(ShopName, flag):
    from brick.joom.Joom_Get_Products_Client import Joom_Get_Products_Client
    from brick.classredis.classshopname import classshopname
    from django_redis import get_redis_connection
    redis_coon = get_redis_connection(alias='product')

    classshopname_obj = classshopname(redis_cnxn=redis_coon)
    if flag == 0:
        classshopname_obj.set_api_status_by_shopname(ShopName, u'正在(全量)刷新 时间较长')
    else:
        classshopname_obj.set_api_status_by_shopname(ShopName, u'正在(增量)刷新 稍稍等待')

    Joom_Get_Products_Client(shop_name=ShopName, flag=flag)

    classshopname_obj.del_api_status_by_shopname(ShopName)

# Joom店铺降价爆单检查
@app.task
def Joom_Recover_Monitor_Task():
    from brick.joom.Joom_Recover_Monitor import Joom_Recover_Monitor
    Joom_Recover_Monitor()

# Joom Get Products
@app.task
def Joom_Get_All_Shop_Products():
    from brick.joom.Joom_Get_Products_Client import Joom_Get_Products_Client
    Joom_Get_Products_Client(flag=1)

#库存量同步redis
@app.task   
def Batch_LoadAndImportData_task():
    from brick.pydata.py_redis.Batch_LoadAndImportData import Batch_LoadAndImportData
    get_info_obj = Batch_LoadAndImportData()
    get_info_obj.synSKUStatusAndAmount()

@app.task
def t_report_sales_daily_task():
    from brick.table.t_report_sales_daily import Sales_Report
    # 生成每日，周，月，服装体系 全平台 销量数据
    rep = Sales_Report()
    rep.getreport_daily()
    
    rep.closeconn()

@app.task
def wish_change_shipping_to_country(IdList):
    import json
    from django.db import connection

    from storeapp.models import t_online_info_wish_store
    from storeapp.models import t_add_variant_information
    from brick.wish.api.wishapi import cwishapi
    from brick.public.wish_change_shipping import change_shipping
    from brick.table.t_online_info import t_online_info
    from brick.table.t_config_online_amazon import t_config_online_amazon
    # from brick.table.t_add_variant_information import t_add_variant_information as wish_change_shipping

    changeObjs = t_add_variant_information.objects.filter(id__in=IdList,Sresult__isnull=True)

    cwishapi_obj = cwishapi()
    t_config_online_amazon_obj = t_config_online_amazon(connection)
    # wish_change_shipping_obj = wish_change_shipping(connection)

    for changeobj in changeObjs:
        # 国家列表
        countrys = json.loads(changeobj.Information).get('country',[])
        countrys_mo = json.loads(changeobj.Information).get('country_mo',[])
        infos = {}
        infos['country'] = countrys
        infos['country_mo'] = countrys_mo

        getTokenObjs = t_online_info_wish_store.objects.filter(ProductID=changeobj.ProductID).values('ShopName')
        if getTokenObjs.exists():
            shopname = getTokenObjs[0]['ShopName']
            infos['shopname'] = shopname

            auth_info = t_config_online_amazon_obj.getauthByShopName(shopname)
            getParam = {
                'access_token':auth_info['access_token'],
                'format':'json',
                'id': changeobj.ProductID,
            }

            GetShipingResult = cwishapi_obj.get_shipping_productid(getParam)
            _content_up = eval(GetShipingResult._content)
            if GetShipingResult.status_code == 200 and _content_up['code'] == 0:
                # # 获取原有设置的国际运费
                shippingList = _content_up['data']['ProductCountryAllShipping']['shipping_prices']
                for shipping in shippingList:
                    countrytmp = shipping['ProductCountryShipping']['country_code']
                    wish_express = shipping['ProductCountryShipping']['wish_express']
                    if countrytmp in countrys_mo:
                        infos[countrytmp] = {}
                        if shipping['ProductCountryShipping']['shipping_price'] == 'Use Product Shipping Price':
                            infos[countrytmp]['Shipping'] = '/'
                            flag = 0
                        else:
                            infos[countrytmp]['Shipping'] = shipping['ProductCountryShipping']['shipping_price']
                            flag = 1
                        #
                        t_online_info_obj = t_online_info(shopname, connection)
                        priceinfo = t_online_info_obj.get_maxpirce(changeobj.ProductID)
                        if priceinfo and priceinfo[1] is not None and priceinfo[1].strip() != '' and priceinfo[2] is not None and priceinfo[2].strip() != '':
                            Hprice = float(priceinfo[1])
                            Hshiping = float(priceinfo[2])

                            if flag == 0:
                                MaxVariablePrice = Hprice + Hshiping
                            else:
                                MaxVariablePrice = Hprice + float(infos[countrytmp]['Shipping'])

                            infos[countrytmp]['MaxVariablePrice'] = MaxVariablePrice

                            up = change_shipping().j_shipping(countrytmp, MaxVariablePrice)  # 运费增长差值 除去瑞典

                            up_SE = change_shipping().j_SE(countrytmp, MaxVariablePrice)  # 判断瑞典额外增加的值

                            if countrytmp in countrys and countrytmp != 'SE' : # 瑞典除外
                                infos[countrytmp]['NewShpping'] = (MaxVariablePrice - Hprice) + up
                            elif countrytmp == 'SE':
                                infos[countrytmp]['NewShpping'] = (MaxVariablePrice - Hprice) + up_SE
                            else:
                                infos[countrytmp]['NewShpping'] = '/'

                            if wish_express == 'True':
                                infos[countrytmp]['NewShpping'] = 'wish_express'

                        else:
                            changeObjs.filter(id=changeobj.id).update(Sresult='error',Content=u'该ProductID最高变体价格没找到')
                            continue
                    else:
                        print '不在选择的国家'

                changeObjs.filter(id=changeobj.id).update(
                    Information=json.dumps(infos), Sresult='0',
                )
            else:
                # 否则就是没有
                changeObjs.filter(id=changeobj.id).update(Sresult='error', Content=u'该ID的各国家运费获取失败')
                continue
        else:
            changeObjs.filter(id=changeobj.id).update(Sresult='error',Content=u'该ProductID没有找到归属店铺')
            continue


@app.task
def will_change_shipping(ID):
    import json
    from django.db import connection
    from brick.table.t_config_online_amazon import t_config_online_amazon
    t_config_online_amazon_obj = t_config_online_amazon(connection)
    from storeapp.models import t_add_variant_information
    from brick.wish.api.wishapi import cwishapi

    changeObjs = t_add_variant_information.objects.filter(id=ID, Sresult='0')
    for changeobj in changeObjs:
        Infostmp = json.loads(changeobj.Information)
        shopname = Infostmp.get('shopname', '')
        if shopname != '':

            auth_info = t_config_online_amazon_obj.getauthByShopName(shopname)
            param = {
                'access_token': auth_info['access_token'],
                'format': 'json',
                'id': changeobj.ProductID,
            }

            for country in Infostmp.get('country',[]):
                if Infostmp.get(country) and Infostmp[country]['NewShpping'] != '/' and Infostmp[country]['NewShpping'] != 'wish_express':
                    param[country] = Infostmp[country]['NewShpping']

            cwishapi_obj = cwishapi()
            rt = cwishapi_obj.change_shipping_by_(param)
            _content = eval(rt._content)
            status = '0'
            if rt.status_code == 200 and _content['code'] == 0:
                status = '2'
            else:
                status = 'error'

            changeObjs.filter(id=changeobj.id).update(
                Param=json.dumps(param), Content=json.dumps(_content),
                Sresult=status,
            )
        else:
            changeObjs.filter(id=changeobj.id).update(Sresult='error', Content=u'店铺名获取错误')




# Joom比价管理
@app.task
def joom_price_parity_by_mq(productid, shopname):
    from brick.joom.Joom_Change_Product_Price_Client import Joom_Price_Parity_Client
    sresult = Joom_Price_Parity_Client(ShopName=shopname, ProductID=productid)
    return sresult

# Joom同步对手信息
@app.task
def joom_competitor_update_by_webdriver(competitor_product_id, product_id):
    from joom_app.views import get_competitor_product_by_webdriver
    sresult = get_competitor_product_by_webdriver(competitor_product_id, product_id)
    return sresult

# Joom获取我方商品评分
@app.task
def joom_get_our_ratingvalue_by_webdriver(product_id):
    from joom_app.views import get_joom_product_ratingvalue_by_webdriver
    sresult = get_joom_product_ratingvalue_by_webdriver(product_id)
    return sresult

# JoomUpdate 7OrderNums
@app.task
def joom_update_products_sevenordernum():
    from brick.joom.joom_update_seven_orders import joom_update_seven_orders
    from brick.joom.joom_update_seven_orders import update_can_price_parity_status
    joom_update_seven_orders()
    update_can_price_parity_status()
    mymall_update_seven_orders_task()
    # from brick.mymall.mymall_update_seven_orders import mymall_update_seven_orders
    # mymall_update_seven_orders()
    # from brick.ebay.ebayapp_update_seven_orders import ebayapp_update_seven_orders
    # ebayapp_update_seven_orders()
    from brick.joom.update_joom_cate import update_joom_cate
    update_joom_cate()
    from brick.mymall.update_mymall_cate import update_mall_cate
    update_mall_cate()


@app.task
def upload_kc_data_task():
    from brick.table.upload_kc_data import upload_kc_data
    # 更新库存预警数据
    rep = upload_kc_data()
    rep.run()
    
@app.task
def exec_purchaser(purchaser):
    from brick.function.update_purchaser import update_purchaser
    obj_purchaser = update_purchaser()
    obj_purchaser.getdata(purchaser)
    
    
@app.task
def refresh_templet_listing_status_task():
    """
    更新wish铺货公共模板listing状态
    :return:
    """
    from brick.wish.refresh_templet_listing_status import refresh_templet_listing_status
    refresh_templet_listing_status()

@app.task
def aliexpress_import_products_task(salling_file='', disable_file='', shopname='', uploadfile_id='', import_user=''):
    # 速卖通导入商品数据
    from brick.aliexpress.aliexpress_import_products import aliexpress_import_products
    from brick.aliexpress.aliexpress_update_seven_orders import aliexpress_update_seven_orders_by_shopname, update_can_price_parity_status
    res = aliexpress_import_products(salling_file=salling_file, disable_file=disable_file, shopname=shopname, uploadfile_id=uploadfile_id, import_user=import_user)
    aliexpress_update_seven_orders_by_shopname(shopname)
    update_can_price_parity_status()
    return res


@app.task
def get_aliexpress_competitor_product_by_request_task(competitor_product_id, product_id):
    # 速卖通获取对手商品信息
    from aliexpress_app.views import get_aliexpress_competitor_product_by_request
    get_aliexpress_competitor_product_by_request(competitor_product_id, product_id)


@app.task
def get_aliexpress_product_ratingvalue_by_request_task(product_id):
    # 速卖通获取我方商品信息评分
    from aliexpress_app.views import get_aliexpress_product_ratingvalue_by_request
    get_aliexpress_product_ratingvalue_by_request(product_id)

@app.task
def aliexpress_update_seven_orders_task():
    # 速卖更新七天order数
    from brick.aliexpress.aliexpress_update_seven_orders import aliexpress_update_seven_orders, update_can_price_parity_status
    aliexpress_update_seven_orders()
    update_can_price_parity_status()


@app.task
def wish_generate_image_task():
    from brick.wish.wish_generate_image import generate_main_image
    generate_main_image()

@app.task
def update_wishpbdata_task():
    from brick.wish.WishPbDailyCatch import run_wishpb
    # 更新WISH广告数据
    run_wishpb()

@app.task
def mymall_update_seven_orders_task():
    # MyMall更新七天order数
    from brick.mymall.mymall_update_seven_orders import mymall_update_seven_orders
    mymall_update_seven_orders()

@app.task
def mymall_import_products_task(salling_file='', shopname='', uploadfile_id='', import_user=''):
    # 速卖通导入商品数据
    from brick.mymall.mymall_import_products import mymall_import_products
    from brick.mymall.mymall_update_seven_orders import mymall_update_seven_orders
    res = mymall_import_products(salling_file=salling_file, shopname=shopname, uploadfile_id=uploadfile_id, import_user=import_user)
    aliexpress_update_seven_orders_by_shopname(shopname)
    return res


@app.task
def batch_change_mymall_data_by_task(product_ids):
    # MyMall 批量修改价格和库存
    from mymall_app.views import batch_change_mymall_data
    batch_change_mymall_data(product_ids)


@app.task
def generate_amazon_india_fba_pdf(fba_sku, shopname,upload_path, timestamp):
    from django.db import connection
    from brick.table.t_shop_amazin_india import t_shop_amazon_india
    # t_shop_amazon_india_temp  = t_shop_amazon_india(connection)
    # company = t_shop_amazon_india_temp.get_company_by_shopname(shopname)
    skus = fba_sku.split(',')
    all_sku_list = []
    for sku in skus:
        print sku
        each_sku_dict = {}
        sku_dict = {}
        if ' ' in sku:
            all_skus = sku.split(' ')
            for each_sku in all_skus:
                count = 1
                final_sku = each_sku
                if '*' in each_sku:
                    final_sku = each_sku.split('*')[0]
                    count = each_sku.split('*')[1]
                sku_dict[final_sku] = count
        else:
            count = 1
            final_sku = sku
            if '*' in sku:
                final_sku = sku.split('*')[0]
                count = sku.split('*')[1]
            sku_dict[final_sku] = count
        each_sku_dict[sku] = sku_dict
        all_sku_list.append(each_sku_dict)
    generate_price_order_obj = generate_price_order()
    generate_price_order_obj.generate_fba_price_pdf(all_sku_list, upload_path, shopname, timestamp)



@app.task
def wish_to_publish(opnum, type, opkey):
    from brick.wish.wish_pub.wish_pub_start import arrange_params
    arrange_params(opnum, type, opkey)
    
import urllib2,urllib
api_url_start = 'http://47.100.224.71/'
@app.task
def refresh_online_info_by_ali_api(action_temp_id):
    # aliexpress全量刷新店铺商品信息
    api_url = api_url_start + 'api/product_get/'
    api_url += str(action_temp_id) + '/'
    req = urllib2.Request(api_url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()

@app.task
def enable_products_by_ali_api(action_temp_id):
    # aliexpress商品上架
    api_url = api_url_start + 'api/product_on/'
    api_url += str(action_temp_id) + '/'
    req = urllib2.Request(api_url)
    res_data = urllib2.urlopen(req, timeout=600)
    res = res_data.read()

@app.task
def disable_products_by_ali_api(action_temp_id):
    # aliexpress商品下架
    api_url = api_url_start + 'api/product_off/'
    api_url += str(action_temp_id) + '/'
    req = urllib2.Request(api_url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()

@app.task
def syn_products_by_ali_api(action_temp_id):
    # aliexpress同步商品信息
    api_url = api_url_start + 'api/product_info/'
    api_url += str(action_temp_id) + '/'
    req = urllib2.Request(api_url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()

@app.task
def edit_productSKU_stock_by_ali_api(action_temp_id):
    # aliexpress单SKU库存修改  stock_multedit
    # api_url = 'http://106.14.125.45:8012/api/sku_stock_edit/'
    api_url = api_url_start + 'api/stock_multedit/'
    api_url += str(action_temp_id) + '/'
    req = urllib2.Request(api_url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()

@app.task
def edit_productSKU_price_by_ali_api(action_temp_id):
    # aliexpress单SKU价格修改  price_edit
    # api_url = 'http://106.14.125.45:8012/api/price_edit/'
    api_url = api_url_start + 'api/price_edit/'
    api_url += str(action_temp_id) + '/'
    req = urllib2.Request(api_url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()

@app.task
def edit_product_by_ali_api(action_temp_id):
    # aliexpress修改商品信息
    api_url = api_url_start + 'api/sku_stock_edit/'
    api_url += str(action_temp_id) + '/'
    req = urllib2.Request(api_url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()

@app.task
def upload_product_by_ali_api(action_temp_id):
    # aliexpress商品刊登
    api_url = api_url_start + 'api/sku_stock_edit/'
    api_url += str(action_temp_id) + '/'
    req = urllib2.Request(api_url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()

@app.task
def upload_ebayapp_products(params):
    from brick.ebay.send_to_MQ import Send_to_MQ
    """
        params = [{
            'shopname':'$shopname',
            'Site':'$Site',
            'uploadtaskid':'$uploadtaskid',
        },
        ...
        ]
    """
    Send_to_MQ()
    smq = Send_to_MQ()
    smq.ebay_to_MQ({'upload_ebayapp_products': 'upload_ebayapp_products', 'body': params})


@app.task
def refresh_syn_ebayapp_shopdata(params):
    from brick.ebay.send_to_MQ import Send_to_MQ
    """
        params = [{
            'shopname':'$shopname',
            'synType':'$synType',
            'ItemID':'$ItemID',
        },
        ...
        ]
    """
    # params = [{'ShopName':shopname,},]
    Send_to_MQ()
    smq = Send_to_MQ()
    smq.ebay_to_MQ({'refresh_syn_ebayapp_shopdata': 'refresh_syn_ebayapp_shopdata', 'body': params})

@app.task
def relist_end_item_ebayapp(params):
    from brick.ebay.send_to_MQ import Send_to_MQ
    """
        params = [{
            'ShopName':'$ShopName',
            'ItemID':'$ItemID',
            'Type':'$Type',
            'Site':'$Site',
        },
        ...
        ]
    """
    Send_to_MQ()
    smq = Send_to_MQ()
    smq.ebay_to_MQ({'relist_end_item_ebayapp': 'relist_end_item_ebayapp', 'body': params})


@app.task
def create_report_supplier_t(month):
    from brick.pydata.py_syn.public import public
    try:
        onlinecon = MySQLdb.connect(user="by15161458383",passwd="K120Esc1",host="rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com",db="report_db",port=3306,charset='utf8')
        sqlcon = pymssql.connect(host='122.226.216.10', port=18794, user='sa', password='$%^AcB2@9!@#',database='ShopElf', charset='utf8')
    
        public_obj = public(sqlcon,onlinecon)
        result1 = public_obj.get_CG_StockOrderCount(month,sqlcon,onlinecon)
    except Exception,ex:
        messages.error(request,'%s_%s:%s'%(traceback.print_exc(),Exception,ex))
        pass
    onlinecon.close()
    sqlcon.close()
    


from brick.chart.wish_listing_refund_statistics import DbOperation, get_current_week
from brick.chart.get_wish_rating import get_product_rating
from django.db import connection
@app.task
def wish_listing_refund_statistics_task():
    """wish在线listing退款统计"""
    cur = connection.cursor()
    week_start, week_end = get_current_week()
    DbOperation_obj = DbOperation(cur)
    DbOperation_obj.update_refund_everyweek()
    # week_start = '2018-10-01'
    productid_list = DbOperation_obj.get_product_id()
    cur.close()
    for product_id in productid_list:
        process_rating.delay(product_id, week_start)


@app.task
def process_rating(product_id, week_start):
    import datetime
    cur_1 = connection.cursor()
    DbOperation_obj_1 = DbOperation(cur_1)

    rating = get_product_rating(product_id=product_id).get('rating', None)
    if rating is None:
        return
    DbOperation_obj_1.update_statistics(product_id=product_id, rating=rating)
    rating_record_dict = DbOperation_obj_1.judge_rating_record(product_id=product_id)
    if rating_record_dict:
        time_now = datetime.datetime.now()
        id = rating_record_dict['id']
        rating_dict = rating_record_dict['rating_dict']
        rating_dict[week_start] = rating
        param = (str(rating_dict), time_now, id)
        flag = 'update'
    else:
        rating_dict = {week_start: rating}
        param = (product_id, str(rating_dict))
        flag = 'insert'
    DbOperation_obj_1.change_rating_record(param=param, flag=flag)

    cur_1.execute('commit;')
    cur_1.close()

    print 'ProductID: %s ' % product_id


@app.task
def online_syn_to_puyuan_task(enter_id_list, optype, opnum, first_name, user_name):
    """online系统信息录入普源"""
    from brick.pydata.py_modify.product_entry import online_syn_to_puyuan

    if optype == 'add_sku':
        online_syn_to_puyuan(enter_id_list=enter_id_list, opnum=opnum, first_name=first_name, user_name=user_name)

@app.task
def online_modify_puyuan_task(modify_data_list, first_name, opnum):
    """online商品信息修改同步普源"""
    from brick.pydata.py_modify.product_modify import online_modify_puyuan
    online_modify_puyuan(modify_data_list, first_name, opnum)

@app.task
def online_sku_binding_puyuan_task(sku_link_data_list, opnum, opflag):
    """online系统新增、删除、修改绑定关系同步普源"""
    from brick.pydata.py_modify.sku_link_shopsku import online_sku_binding_add_puyuan, online_sku_binding_delete_puyuan, online_sku_binding_modify_puyuan
    if opflag == 'add':
        online_sku_binding_add_puyuan(sku_link_data_list=sku_link_data_list, opnum=opnum)
    elif opflag == 'delete':
        online_sku_binding_delete_puyuan(sku_link_data_list=sku_link_data_list, opnum=opnum)
    elif opflag == 'modify':
        online_sku_binding_modify_puyuan(sku_link_data_list=sku_link_data_list, opnum=opnum)

@app.task
def online_tort_syn_to_puyuan_task(tort_data_list, opnum, now_time, user_name):
    """online系统侵权信息同步普源"""
    from brick.pydata.py_modify.sku_tort import online_tort_syn_puyuan
    online_tort_syn_puyuan(tort_data_list=tort_data_list, opnum=opnum, now_time=now_time, user_name=user_name)

@app.task
def aliexpress_submitter_link_count():
    from brick.aliexpress.submitter_link_count import submitter_link_count
    
    req = submitter_link_count()
    req.insert_db()
    
@app.task
def wish_upload_shopname_task():
    """wish铺货店铺周订单、周销售额统计"""
    from brick.chart.wish_shop_order_sales import WishShopOrderSales
    from django.db import connection
    cur = connection.cursor()
    obj = WishShopOrderSales(cur)
    week_start, statistics_dict, shopname_infos = obj.get_statistics()
    obj.process_details(week_start, statistics_dict, shopname_infos)
    cur.close()
    connection.close()
    
@app.task
def update_ebayapp_price():
    from brick.ebay.update_shopee_price import update_ebayapp_price
    update_ebayapp_price()

@app.task
def ClearanceSale_auto_change_StopSale_task():
    """清仓状态且库存和销量均为零的SKU自动转为停售状态"""
    from brick.pydata.py_modify.ClearanceSale_auto_change_StopSale import main
    main()

@app.task
def online_modify_py_purchaser_task(modify_file, modify_name, modify_time, schedule_name):
    """批量修改SKU对应的采购员"""
    from brick.pydata.py_modify.purchaser_modify import modify_purchaser_batch
    modify_purchaser_batch(modify_file, modify_name, modify_time, schedule_name)

"""
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    :return: firstDay: 当月的第一天，datetime.date类型
              lastDay: 当月的最后一天，datetime.date类型
"""
def getMonthFirstDayAndLastDay(year=None, month=None):
    import calendar, datetime
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year
    if month:
        month = int(month)
    else:
        month = datetime.date.today().month
    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)
    # 获取当月的第一天
    firstDay = datetime.date(year=year, month=month, day=1)
    lastDay = datetime.date(year=year, month=month, day=monthRange)
    return firstDay.strftime('%d'), lastDay.strftime('%d')

@app.task
def get_saler_profit_data(selmonth):
    reload(sys)
    sys.setdefaultencoding('utf8')
    from brick.pydata.py_syn.py_conn import py_conn
    py_connObj = py_conn()
    sqlconnInfo = py_connObj.py_conn_database()
    cursor = connection.cursor()

    firstDay, lastDay = getMonthFirstDayAndLastDay(selmonth[:4], selmonth[5:7])
    # 获取普元汇率表变化
    strCurrencyCode = "select count(1),CURRENCYCODE from B_CurrencyCode_0814 where expdate>'%s' group by CURRENCYCODE HAVING count(1)>1" % (
                selmonth + '-' + lastDay + ' 00:00:00')
    sqlconnInfo['py_cursor'].execute(strCurrencyCode)
    result_CurrencyCode = sqlconnInfo['py_cursor'].fetchall()
    nMaxCurrencyCode = 1
    currencyCode = 'USD'
    dealnum = 0
    eff_exp_date = {}
    dicTmp = {}
    dicTmp['effdate'] = selmonth + '-01 00:00:00'
    if result_CurrencyCode:
        for row_result_CurrencyCode in result_CurrencyCode:
            if row_result_CurrencyCode[0] > nMaxCurrencyCode:
                currencyCode = row_result_CurrencyCode[1]
                nMaxCurrencyCode = row_result_CurrencyCode[0]
        strCurrencyCode = "select CONVERT(varchar(100), effdate, 120) from B_CurrencyCode_0814 where expdate>'%s' and CURRENCYCODE='%s' order by effdate asc" % (
            selmonth + '-31 00:00:00', currencyCode)
        sqlconnInfo['py_cursor'].execute(strCurrencyCode)
        result_effdate = sqlconnInfo['py_cursor'].fetchall()
        flag = 0
        for row_result_effdate in result_effdate:
            if flag == 0:
                flag += 1
                continue
            dicTmp['expdate'] = row_result_effdate[0]
            eff_exp_date['effexp' + str(dealnum)] = dicTmp
            dicTmp = {}
            dealnum += 1
            dicTmp['effdate'] = row_result_effdate[0]
    dicTmp['expdate'] = selmonth + '-' + lastDay + ' 23:59:59'
    eff_exp_date['effexp' + str(dealnum)] = dicTmp

    for i in range(len(eff_exp_date)):

        effDate = eff_exp_date['effexp' + str(i)]['effdate']
        expDate = eff_exp_date['effexp' + str(i)]['expdate']
        # 获取配置表数据
        strHQSql = "select SalerName,PlatformName,ShopName,Department from t_saler_profit_config where StatisticsMonth='%s'" % (
            selmonth)  # and SalerName='邢亚萍'
        cursor.execute(strHQSql)
        distinctSaler = cursor.fetchall()
        for row_distinctSaler in distinctSaler:
            '''
            print row_distinctSaler[0].encode('gb2312'), effDate, expDate
            strHQSql_Saler = "select ShopName,PlatformName from t_saler_profit_config where SalerName='%s' and StatisticsMonth='%s'" % (
            row_distinctSaler[0], selmonth)
            cursor.execute(strHQSql_Saler)
            tup_allShopName = cursor.fetchall()
            strShopName = ''
            platformName = ''
            for row_tup_allShopName in tup_allShopName:
                # list_allShopName.append(row_tup_allShopName[0].encode('gb2312'))
                strShopName = strShopName + row_tup_allShopName[0] + ','
                platformName = row_tup_allShopName[1]
            '''
            if len(row_distinctSaler) > 0:
                # 获取普元绩效数据
                strProcSql = "exec P_RP_C_FinancialProfit_SalerSHOPSKU_2_0831 '%s','%s','%s','','','','','0'" % (
                effDate, expDate, row_distinctSaler[2])
                sqlconnInfo['py_cursor'].execute(str(strProcSql))
                resultSalerProfit = sqlconnInfo['py_cursor'].fetchall()
                if resultSalerProfit:
                    strOnlineSql = "insert into t_saler_profit_reportform(ShopSKU,ProductSKU,StockAveragePrice,GoodsCode,ProductName,Model,Specifications,Style1,Style2," \
                                   "Category,Supplier,SalerName1,SalerName2,Purchaser,CreateDate,SaleNum,SaleVolume,BuyerPayFreight,SaleCost," \
                                   "Profit,EbayTransFee,PPCharge,ActualAmount,FreightCost,PackCost,RefundAmount,Salers) " \
                                   "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                    cursor.executemany(strOnlineSql, resultSalerProfit)
                    strUpdate = "update t_saler_profit_reportform set SalerName='%s',StatisticsMonth='%s',effdate='%s',expdate='%s',platform='%s',allShopName='%s',department='%s' where SalerName is NULL and StatisticsMonth is NULL" \
                                % (row_distinctSaler[0], selmonth, effDate, expDate,row_distinctSaler[1],row_distinctSaler[2],row_distinctSaler[3])
                    cursor.execute(strUpdate)
                    connection.commit()
    cursor.close()
    py_connObj.py_close_conn_database()

@app.task
def gen_execl_saler_profit_data(username,selmonth,filename):
    import xlwt, os
    from django.db import connection
    from Project.settings import SBBL, MEDIA_ROOT, BUCKETNAME_DOWNLOAD
    from brick.public.create_dir import mkdir_p
    from datetime import datetime as ddtime
    from brick.public.upload_to_oss import upload_to_oss
    from skuapp.table.t_saler_profit_reportform import t_saler_profit_reportform
    from skuapp.table.t_download_info import t_download_info

    import xlsxwriter
    datastyle = xlwt.XFStyle()
    datastyle.num_format_str = 'yyyy-mm-dd hh:mm:ss'
    path = MEDIA_ROOT + 'download_xls/' + username
    mkdir_p(MEDIA_ROOT + 'download_xls')
    os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

    mkdir_p(path)
    #os.popen('chmod 777 %s' % (path))

    workbook = xlsxwriter.Workbook(path+'/'+filename)
    sheet = workbook.add_worksheet('业绩销售报表2')

    sheetlist = [u'销售额',u'销售成本',u'ebay成交费',u'PP手续费',u'包装成本',u'运费成本',u'实收利润', u'退款金额',u'店铺SKU', u'SKU',
                 u'库存平均单价',u'采购员',u'供应商',u'规格', u'款式1', u'款式2',u'商品编码',u'商品创建时间',u'商品类别',u'商品名称',u'实得金额',
                 u'销售数量',u'销售员',u'型号',u'买家付运费',u'业绩归属人1', u'业绩归属人2',
                 u'业绩归属人', u'统计月份',u'汇率改变开始时间', u'汇率改变结束时间',u'部门',u'平台',u'店铺名称' ]
    row = 0
    for index, item in enumerate(sheetlist):
        sheet.write(row, index, item)
    t_saler_profit_reportform_objs = t_saler_profit_reportform.objects.filter(StatisticsMonth=selmonth)
    for obj in t_saler_profit_reportform_objs:
        row = row + 1
        column = 0
        sheet.write(row, column, obj.SaleVolume) # 销售额
        column = column + 1
        sheet.write(row, column, obj.SaleCost)  # 销售成本
        column = column + 1
        sheet.write(row, column, obj.EbayTransFee)  # ebay成交费
        column = column + 1
        sheet.write(row, column, obj.PPCharge)  # PP手续费
        column = column + 1
        sheet.write(row, column, obj.PackCost)  # 包装成本
        column = column + 1
        sheet.write(row, column, obj.FreightCost)  # 运费成本
        column = column + 1
        sheet.write(row, column, obj.Profit)  # 实收利润
        column = column + 1
        sheet.write(row, column, obj.RefundAmount)  # 退款金额
        column = column + 1
        sheet.write(row, column, obj.ShopSKU)  # 店铺SKU
        column = column + 1
        sheet.write(row, column, obj.ProductSKU)  # SKU

        column = column + 1
        sheet.write(row, column, obj.StockAveragePrice)  # 库存平均单价
        column = column + 1
        sheet.write(row, column, obj.Purchaser)  # 采购员
        column = column + 1
        sheet.write(row, column, obj.Supplier)  # 供应商
        column = column + 1
        sheet.write(row, column, obj.Specifications)  # 规格
        column = column + 1
        sheet.write(row, column, obj.Style1)  # 款式1
        column = column + 1
        sheet.write(row, column, obj.Style2)  # 款式2
        column = column + 1
        sheet.write(row, column, obj.GoodsCode)  # 商品编码
        column = column + 1
        sheet.write(row, column, obj.CreateDate)  # 商品创建时间
        column = column + 1
        sheet.write(row, column, obj.Category)  # 商品类别
        column = column + 1
        sheet.write(row, column, obj.ProductName)  # 商品名称
        column = column + 1
        sheet.write(row, column, obj.ActualAmount)  # 实得金额

        column = column + 1
        sheet.write(row, column, obj.SaleNum)  # 销售数量
        column = column + 1
        sheet.write(row, column, obj.Salers)  # 销售员
        column = column + 1
        sheet.write(row, column, obj.Model)  # 型号
        column = column + 1
        sheet.write(row, column, obj.BuyerPayFreight)  # 买家付运费
        column = column + 1
        sheet.write(row, column, obj.SalerName1)  # 业绩归属人1
        column = column + 1
        sheet.write(row, column, obj.SalerName2)  # 业绩归属人2

        column = column + 1
        sheet.write(row, column, obj.SalerName)  # 业绩归属人
        column = column + 1
        sheet.write(row, column, obj.StatisticsMonth)  # 统计月份
        column = column + 1
        sheet.write(row, column, str(obj.effdate))  # 生效时间
        column = column + 1
        sheet.write(row, column, str(obj.expdate))  # 失效时间
        column = column + 1
        sheet.write(row, column, obj.department)  # 部门
        column = column + 1
        sheet.write(row, column, obj.platform)  # 平台
        column = column + 1
        sheet.write(row, column, obj.allShopName)  # 店铺名称

    #workbook.save(path + '/' + filename)
    workbook.close()

    upload_to_oss_obj = upload_to_oss(BUCKETNAME_DOWNLOAD)
    myresult = upload_to_oss_obj.upload_to_oss(
        {'path': username, 'name': filename, 'byte': open(path + '/' + filename), 'del': 1})
    if myresult['errorcode'] == 0:
        appname = u'%s/%s' % (username, filename)
        t_download_info.objects.create(appname=appname, abbreviation=filename,
                                       updatetime=ddtime.now(), Belonger=username,
                                       Datasource='t_saler_profit_reportform')

    return myresult
    
@app.task
def update_profitrate_ebay_task():
    from brick.ebay.update_profitrate_ebay_listing_task import update_profitrate_ebay_listing_task
    from brick.ebay.update_profitrate_ebay_listing_task import update_profitrate_ebay_listing_task2
    curdateH = time.strftime('%H', time.localtime(time.time()))
    if curdateH > 20 or curdateH < 7:
        update_profitrate_ebay_listing_task()
    else:
        update_profitrate_ebay_listing_task2()

@app.task
def syn_shopee_data(shopname='', partner_id='', shopid='', opid='', flag=''):
    from brick.shopee.Shopee_info_all import update_shopee_info
    update_shopee_info(shopname, partner_id, shopid, flag, opid)
    
@app.task
def online_modify_py_possessman2_task(modify_file, modify_name, modify_time, schedule_name):
    """批量修改SKU对应的采购员"""
    from brick.pydata.py_modify.purchaser_modify import modify_possessman2_batch
    modify_possessman2_batch(modify_file, modify_name, modify_time, schedule_name)

@app.task
def py_getgongzi_report():
    import ConfigParser
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    import pymssql
    import MySQLdb
    from datetime import datetime, date, timedelta
    pyuanConn = pymssql.connect(host='122.226.216.10', port=18793, user='sa', password='$%^AcB2@9!@#',
                                database='ShopElf', charset='utf8')
    result = {}
    sqlcursor = pyuanConn.cursor()
    cur_conn = connection.cursor()
    try:
        # 格式化入参日期
        t = date.today()
        yesterday = t + timedelta(days=-1)
        sql = " delete from report_db.t_gongzi_report_m where makedate LIKE '%s%%'" % yesterday
        print sql
        cur_conn.execute(sql)
        cur_conn.execute("commit;")
        for i in range(1, 8):
            sql = "exec p_Query_GongZhiReport_hq %s,'%s','%s 23:59:59','',''" % (i, yesterday, yesterday)
            sqlcursor.execute(sql)
            sql1 = "insert into report_db.t_gongzi_report_m (postname,makedate,billnumber,sku,categoryname,personname,price,amount,money,typename,xs,goodsname,locationname,l_qty,logicswayname) " \
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            while True:
                objs = []
                objs = sqlcursor.fetchmany(5000)
                params = []
                for obj in objs:
                    if obj:
                        params.append(obj)
                cur_conn.executemany(sql1,params)
                cur_conn.execute("commit;")
                if len(objs) < 5000:
                    break
    except Exception, e:
        sqlcursor.close()
        cur_conn.close()
        pyuanConn.close()
        print repr(e)

    sqlcursor.close()
    cur_conn.close()
    pyuanConn.close()



@app.task
def virtual_overseas_warehouse_task():
    """eBay海外仓自动上下架任务"""
    from brick.ebay.virtual_overseas_warehouse import vow_shelf_enter
    vow_shelf_enter()
    
@app.task
def py_Syn_walmart_main_task():
    from brick.walmart.py_Syn_walmart import py_Syn_walmart_main
    py_Syn_walmart_main()
    
@app.task
def b_goods_sales_count_task():
    from brick.pydata.py_syn.b_goods_sales_count_syn import b_goods_sales_count_syn
    obj = b_goods_sales_count_syn()
    obj.deal_data() 
    
    

@app.task
def generate_track_info():
    """生成Wish运单状态"""
    from brick.wish.trackingmore.generate_track import main
    main()

@app.task
def refresh_track_info(datas=None):
    """刷新Wish运单状态"""
    from brick.wish.trackingmore.refresh_track import *
    refresh_track(datas)

@app.task
def aliexpress_auto_off_shelf_task():
    """aliexpress停售产品自动上下架"""
    from brick.aliexpress.aliexpress_auto_off_shelf import aliexpress_auto_off_shelf
    aliexpress_auto_off_shelf()

@app.task
def funmart_update_pro_qty():
    from funmart_app.function.FunMart_Pro_Update import update_products_and_quantity
    update_products_and_quantity()


@app.task
def ebay_vow_task_funnel_task():
    """ebay的虚拟海外仓任务漏斗"""
    from brick.ebay.ebay_vow_task_funnel import ebay_vow_task_funnel
    ebay_vow_task_funnel()


@app.task
def mall_platform_refund_sku_task(file_obj, user_name):
    import xlrd
    from xlrd import xldate_as_tuple
    import time
    from decimal import *
    from datetime import datetime as dattime

    wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 关键点在于这里
    # xls_sheet = wb.sheet_by_index(0)
    table = wb.sheets()[0]
    row = table.nrows
    result = {'errorcode': 0, 'errortext': u'导入成功'}

    from brick.pydata.py_syn.py_conn import py_conn
    py_connObj = py_conn()
    sqlconnInfo = py_connObj.py_conn_database()

    from django.db import connection
    conn_mysql = connection
    cursor_mysql = conn_mysql.cursor()

    Salesnumber = ''
    RefundType = u'其他'
    AfterSaleType = u'其他'
    Number = 1
    try:
        for i in xrange(1, row):
            try:
                col = table.row_values(i)
                OrderID = col[0]

                Date = str(dattime(*xldate_as_tuple(col[1], 0)))[:10]
                Money = col[2]
                Incoming = col[3]
                Store = col[4]
                import_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

                sql = """SELECT b.sku,a.suffix FROM P_Trade(nolock) a INNER JOIN p_tradedt(nolock) b on b.tradenid = a.nid  where a.ACK = %s"""
                args = (OrderID)
                sqlconnInfo['py_cursor'].execute(sql, args)
                skus = sqlconnInfo['py_cursor'].fetchall()

                sql = """SELECT b.sku,a.suffix  FROM P_Trade_His(nolock) a INNER JOIN P_TradeDt_His(nolock) b on b.tradenid = a.nid  where a.ACK = %s"""
                args = (OrderID)
                sqlconnInfo['py_cursor'].execute(sql, args)
                skus = skus + sqlconnInfo['py_cursor'].fetchall()

                if skus:
                    for sku_i in skus:
                        sku = sku_i[0]

                        sql = """INSERT into platform_refund_sku_match
                              (OrderID,Salesnumber,RefundType,AfterSaleType,SKU,Number,Money,Date,Incoming,Store,import_date)
                              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                        args = (OrderID, Salesnumber, RefundType, AfterSaleType, sku, Number, Money, Date, Incoming, Store,import_date)
                        cursor_mysql.execute(sql, args)
                        conn_mysql.commit()
                else:
                    sku = ''

                    sql = """INSERT into platform_refund_sku_match
                          (OrderID,Salesnumber,RefundType,AfterSaleType,SKU,Number,Money,Date,Incoming,Store,import_date)
                          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    args = (OrderID, Salesnumber, RefundType, AfterSaleType, sku, Number, Money, Date, Incoming, Store,import_date)
                    cursor_mysql.execute(sql, args)
                    conn_mysql.commit()
            except Exception, ex:

                result['errorcode'] = -1
                result['errortext'] = '第%d行存在问题:Exception:%s, ex:%s，请修正后重新上传' % (i + 1, Exception, ex)

    except:
        conn_mysql.rollback()
    conn_mysql.close()
    py_connObj.py_close_conn_database()
    return result
    
# Walmart店铺管理--按照sku同步数据、上架、下架
@app.task
def syndata_by_walmart_api(params, flag, opnum):
    from django.db import connection
    from walmart_app.views import syn_sku_walmart,relist_end_item
    from brick.table.t_wish_store_oplogs import t_wish_store_oplogs

    sResult = None
    if flag == 'syn':  # 同步数据
        sResult = syn_sku_walmart(params, opnum)
    elif flag == 'endItem':
        sResult = relist_end_item(params, 'endItem', opnum)
    elif flag == 'relistItem':
        sResult = relist_end_item(params, 'relistItem', opnum)

