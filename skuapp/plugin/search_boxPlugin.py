# coding=utf-8

from xadmin.views import BaseAdminPlugin
from django.template import loader
from urllib import unquote
from skuapp.table.search_box_plugin import *
from Project.settings import *
from django.contrib import messages
from skuapp.table.t_report_sales_daily import *
from skuapp.table.t_report_sales_daily_byShopName import *
import MySQLdb
from skuapp.table.b_goodsskulinkshop import *
from skuapp.table.t_task_trunk import *
from skuapp.table.t_wish_screenshot import *
from collections import OrderedDict
from skuapp.table.t_use_productsku_apply_for_shopsku import t_use_productsku_apply_for_shopsku
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from django.db import connection
import json


from skuapp.table.t_product_suvering import t_product_suvering


class search_boxPlugin(BaseAdminPlugin):
    search_box_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.search_box_flag)

    def getParam(self, searchKey, searchParams,newUrl):
        searchParam = ''
        for each in searchParams:
            paramf = each.split("=")[0]
            if searchKey == paramf:
                uu = each + '&'
                newUrl = newUrl.replace(uu, '')
                searchParam = unquote(each.split('=')[1])
        paramList = {'newUrl': newUrl, 'searchParam': searchParam}
        return  paramList

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]
        #begin 用于控制选择页数后，再按过滤条件查询(查询结果如果小于之前选择业务报错)
        strUrl = sourceURL
        if "?" in sourceURL:
            mainUrl = sourceURL.split("?")[0]
            strUrl = mainUrl + '?'
            conditionsAllParam = sourceURL.split("?")[1]
            conditionsParam = conditionsAllParam.split("&")
            for row in conditionsParam:
                if len(row)>=2 and row[:2] == 'p=':
                    continue
                strUrl = strUrl + row + '&'
            if strUrl[-1] == "&":
                sourceURL = strUrl[:-1]
        #end

        StepID_objs = u'%s' % context['request']
        AAA = self.model._meta.model_name
        ShopNameData = ""
        SupplierData = ""
        cat_Dic = {}
        if AAA == 't_product_b_goods':
            db_connShopName = connection
            if db_connShopName:
                cursor = db_connShopName.cursor()
                cursor.execute("select DISTINCT Memo from py_db.b_goodsskulinkshop WHERE Memo != ''")
                ShopNameDataTmp = cursor.fetchall()
                for ShopNameData_obj in ShopNameDataTmp:
                    ShopNameData = ShopNameData + ShopNameData_obj[0].replace('u','') + ","
                ShopNameData = ShopNameData.split(",")
                
                cursor.execute("select CategoryParentName,CategoryName from b_goodscats where CategoryParentID!='0'")
                rts = cursor.fetchall()
                if rts:
                    for rt in rts:
                        cat_Dic["zy"+rt[0].replace(".","_")] = []
                    for rt in rts:
                        b_goodslist = cat_Dic.get("zy"+rt[0].replace(".","_"))
                        b_goodslist.append(rt[1])
                if cursor:
                    cursor.close()


        shopNData = ""
        if AAA == 't_use_productsku_apply_for_shopsku':
            shop_set = t_store_configuration_file.objects.values_list('ShopName', flat=True)
            shopNData = ','.join(list(shop_set))

        #     db_connshopN = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'],DATABASES['default']['PASSWORD'], DATABASES['default']['NAME'])
        #     if db_connshopN:
        #         cursor = db_connshopN.cursor()
        #         cursor.execute("select DISTINCT ShopName from t_use_productsku_apply_for_shopsku WHERE ShopName != ''")
        #         shopNDataTmp = cursor.fetchall()
        #         for shopNData_obj in shopNDataTmp:
        #             shopNData = shopNData + shopNData_obj[0] + ","
        #         shopNData = shopNData.split(",")
        #         if cursor:
        #             cursor.close()
        #         db_connshopN.close()

                
        shopNameOfficialData = ""
        if AAA == 't_wish_screenshot':
            db_connshopNameOfficialData = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'],DATABASES['default']['PASSWORD'], DATABASES['default']['NAME'])
            if db_connshopNameOfficialData:
                cursor = db_connshopNameOfficialData.cursor()
                cursor.execute("select DISTINCT shopNameOfficial from t_wish_screenshot WHERE shopNameOfficial != ''")
                shopNameOfficialDataTmp = cursor.fetchall()
                for shopNameOfficialData_obj in shopNameOfficialDataTmp:
                    shopNameOfficialData = shopNameOfficialData + shopNameOfficialData_obj[0] + ","
                shopNameOfficialData = shopNameOfficialData.split(",")
                if cursor:
                    cursor.close()
                db_connshopNameOfficialData.close()
        
        ShNameData = ""
        if AAA == 't_report_sales_daily' or AAA=='t_report_sales_daily_byshopname':
            cursor = connection.cursor()
            cursor.execute("select DISTINCT ShopName from t_report_sales_daily_byShopName WHERE  ShopName != ''")
            ShNameDataTmp = cursor.fetchall()
            ShNameData = [t[0].encode('utf-8') for t in ShNameDataTmp]
            cursor.close()
        
        #Task_handlerData = ""
        Create_manData = ""
        #IdentifierData = ""
        if AAA == 't_task_trunk':
            db_Create_manData = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'],DATABASES['default']['PASSWORD'], DATABASES['default']['NAME'])
            if db_Create_manData:
                cursor = db_Create_manData.cursor()
                cursor.execute("select DISTINCT Create_man from t_task_trunk WHERE Create_man != ''")
                Create_manDataTmp = cursor.fetchall()
                for Create_manData_obj in Create_manDataTmp:
                    Create_manDataData = Create_manData + Create_manData_obj[0] + ","
                Create_manData = Create_manData.split(",")
                if cursor:
                    cursor.close()
                db_Create_manData.close()

        config_path = STATIC_ROOT + 'search_box_plugin_config.txt'
        cfile = open(config_path)
        lines = cfile.readlines()
        inputs1 = []
        inputs_id1 = []
        inputs2 = []
        inputs_id2 = []
        for line in lines:
            if line is None or line.strip() == '':
                continue
            if '{' not in line:
                continue
            search_dict = eval(line)                                 #转换为字典  因为有{ }         [ ] ==> 列表    ( ) ==> 元组
            if search_dict['model_name'] == AAA:                     #model_name等于访问的网址
                if search_dict['inputs'] == '1':
                    if search_dict['selection'] == 5:
                        if '[' in search_dict['defult_value1']:
                            search_dict['defult_value1'] = eval(search_dict['defult_value1'])
                    elif  '{' in search_dict['defult_value1']:
                        if AAA == 't_product_suvering' and search_dict['id_name'] == 'saler' and search_dict['id'] == '3':
                            salers_tmp = t_product_suvering.objects.values('saler')
                            salersdict = {}
                            for obj in salers_tmp :
                                if obj['saler']:
                                    salersdict[obj['saler']] = obj['saler']
                            search_dict['defult_value1'] = salersdict
                        elif AAA == 't_product_suvering' and search_dict['id_name'] == 'getinfo_cate' and search_dict['id'] == '7':
                            getinfo_cate_tmp = t_product_suvering.objects.values("getinfo_cate")
                            getinfo_catedict = {}
                            for obj in getinfo_cate_tmp :
                                if obj['getinfo_cate']:
                                    getinfo_catedict[obj['getinfo_cate']] = obj['getinfo_cate']
                            search_dict['defult_value1'] = getinfo_catedict
                        else:
                            search_dict['defult_value1'] = eval(search_dict['defult_value1'])
                        search_dict['defult_value1'] = OrderedDict(sorted(search_dict['defult_value1'].items(),key=lambda  item:item[0]))
                    inputs1.append(search_dict)
                    inputs_id1.append(search_dict['id'])
                else:
                    inputs2.append(search_dict)
                    inputs_id2.append(search_dict['id'])

        newUrl = sourceURL
        if "?" in sourceURL:
            newUrl += "&"
            condition = newUrl.split("?")[1]
            conditions = condition.split("&")
            count_params = []
            count_filters = []
            for condition_i in conditions:
                if condition_i is not None and condition_i.strip() != '':
                    count_filters.append(condition_i)
                    count_params.append(condition_i.split("=")[0])

            for input1 in inputs1:
                if input1['urlname1'] in count_params:
                    paramList1 = self.getParam(input1['urlname1'], count_filters, newUrl)
                    newUrl = paramList1['newUrl']
                    input1['value1'] = paramList1['searchParam']
            for input2 in inputs2:
                if input2['urlname1'] in count_params or input2['urlname2'] in count_params:
                    paramList1 = self.getParam(input2['urlname1'], count_filters, newUrl)
                    newUrl = paramList1['newUrl']
                    input2['value1'] = paramList1['searchParam']
                    if input2['urlname2'] is not None and input2['urlname2'].strip() != '':
                        paramList2 = self.getParam(input2['urlname2'], count_filters, newUrl)
                        newUrl = paramList2['newUrl']
                        input2['value2'] = paramList2['searchParam']
                        if input2['isDate']==1:
                            import datetime
                            endTime = paramList2['searchParam']
                            if endTime is not None and endTime.strip() != '':
                                date_time = datetime.datetime.strptime(endTime, '%Y-%m-%d')
                                date_time = date_time + datetime.timedelta(days = -1)
                                input2['value2'] = str(date_time).split(' ')[0]
        else:
            newUrl += "?"

        warning = {'code': 0, 'messages' : ''}
        if self.model._meta.model_name in ['t_work_flow_of_plate_house', ]:
            warning = {
                'code': 1,
                'messages': '超时告警规则: </br>1、确定面辅料:需求提出后两天内完成</br>2、纸样样衣:确定面辅料后三天内完成</br>3、审核样衣、报价、跟单领取:均于当天完成</br>4、发货完成:需要跟单员在确定跟单领取后7天内完成'
            }
        if self.model._meta.model_name in ['t_work_battledore',]:
            warning = {
                'code': 1,
                'messages': '超时告警规则: </br>1、确定面辅料:需求提出后两天内完成</br>2、纸样样衣:确定面辅料后三天内完成</br>3、审核样衣、报价:均于当天完成'
            }

        nodes.append(
            loader.render_to_string('search_box_plugin.html',
                 {'newUrl': newUrl, 'inputs1': inputs1, 'inputs2': inputs2,
                  'inputs_id1': inputs_id1, 'inputs_id2': inputs_id2, 'ShopNameData':ShopNameData,
                  'SupplierData':SupplierData, 'shopNData':shopNData,'Create_manData':Create_manData,
                  'AAA':AAA,'cat_Dic':cat_Dic,'shopNameOfficialData':shopNameOfficialData,
                  'ShNameData': ShNameData,
                  'warning':warning
                  }
            )
        )
