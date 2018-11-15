# -*- coding: utf-8 -*-

from brick.pricelist.calculate_price import calculate_price
import MySQLdb

DATABASES = {
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1',
    'PORT': '3306',
}


def getsiteshop(db_conn):
    result = {'code':0,'data':''}
    try:
        cursor = db_conn.cursor()
        sql = "select itemid,title,startprice,realavailable,Productsku,isVariations from t_online_info_ebay;"
        cursor.execute(sql)
        datasrc = cursor.fetchall()
        cursor.close()
        result['data'] = datasrc
        print 'getsiteshop success'
    except Exception:
        result['code'] = -1
    return result

def get_info_ebay_subSKU(db_conn,itemid):
    result = {'code': 0, 'data': ''}
    try:
        cursor = db_conn.cursor()
        sql = "select itemid,startprice,realavailable,productsku,subSKU from t_online_info_ebay_subsku where itemid='%s';" % itemid
        cursor.execute(sql)
        datasrc = cursor.fetchall()
        cursor.close()
        result['data'] = datasrc
        print 'getsubitem success'
    except Exception:
        result['code'] = -1
    return result


def update_online_ebay(db_conn,itemid,priceparams):
    try:
        cursor = db_conn.cursor()
        sql = "update t_online_info_ebay set shopeePhilippines='%s',shopeeThailand='%s', shopeeSingapore='%s',shopeeIndonesia='%s'," \
              "shopeeMalaysia='%s',shopeeVietnam='%s' where itemid='%s';" % (priceparams['MY_calculate_price'],priceparams['PH_calculate_price'],priceparams['VNM_calculate_price'],
                 priceparams['THA_calculate_price'],priceparams['SG_calculate_price'],priceparams['INA_calculate_price'],itemid)
        cursor.execute(sql)
        cursor.close()
        print 'update_online_ebay success'
    except Exception:
        pass

def update_online_ebay_subsku(db_conn,itemid,subSKU,priceparams):
    try:
        cursor = db_conn.cursor()
        sql = "update t_online_info_ebay_subsku set shopeePhilippines='%s',shopeeThailand='%s', shopeeSingapore='%s',shopeeIndonesia='%s'," \
              "shopeeMalaysia='%s',shopeeVietnam='%s' where itemid='%s' and subSKU='%s';" % (priceparams['MY_calculate_price'],priceparams['PH_calculate_price'],priceparams['VNM_calculate_price'],
                 priceparams['THA_calculate_price'],priceparams['SG_calculate_price'],priceparams['INA_calculate_price'],itemid,subSKU)
        cursor.execute(sql)
        cursor.close()
        print 'update_online_ebay success'
    except Exception:
        pass

def update_ebayapp_price():
    try:
        db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'],
                                  charset="utf8")
        print db_conn
    except Exception as e:
        error = 'Connect mysql db error %s' % e
        print error

    site_result = getsiteshop(db_conn=db_conn)
    if site_result['code'] <> 0:
        print 'select t_online_info_ebay error'
        return 'error'
    site_datas = site_result['data']
    for site_data in site_datas:
        try:
            itemid = site_data[0]
            # title = site_data[1]
            # currentprice = site_data[2]
            # realavailable = site_data[3]
            Productsku = site_data[4]
            isVariations = site_data[5]
            # site = site_data[6]
            # shopName = site_data[7]
            if isVariations == 'NO':
                priceparams= {}
                ncalculate_price_obj = calculate_price(str(Productsku))
                MY_calculate_result = ncalculate_price_obj.calculate_selling_price(profitRate=40,platformCountryCode='SHOPEE',DestinationCountryCode='MY')
                priceparams['MY_calculate_price'] = MY_calculate_result['sellingPrice_destination']

                PH_calculate_result = ncalculate_price_obj.calculate_selling_price(profitRate=40,platformCountryCode='SHOPEE',DestinationCountryCode='PH')
                priceparams['PH_calculate_price'] = PH_calculate_result['sellingPrice_destination']

                VNM_calculate_result = ncalculate_price_obj.calculate_selling_price(profitRate=40,platformCountryCode='SHOPEE',DestinationCountryCode='VNM')
                priceparams['VNM_calculate_price'] =VNM_calculate_result['sellingPrice_destination']

                THA_calculate_result = ncalculate_price_obj.calculate_selling_price(profitRate=40,platformCountryCode='SHOPEE',DestinationCountryCode='THA')
                priceparams['THA_calculate_price'] = THA_calculate_result['sellingPrice_destination']

                SG_calculate_result = ncalculate_price_obj.calculate_selling_price(profitRate=40,platformCountryCode='SHOPEE',DestinationCountryCode='SG')
                priceparams['SG_calculate_price'] = SG_calculate_result['sellingPrice_destination']

                INA_calculate_result = ncalculate_price_obj.calculate_selling_price(profitRate=40,platformCountryCode='SHOPEE',DestinationCountryCode='INA')
                priceparams['INA_calculate_price'] = INA_calculate_result['sellingPrice_destination']

                update_online_ebay(db_conn=db_conn,itemid=itemid,priceparams=priceparams)
            elif isVariations == 'YES':
                sub_reuslt = get_info_ebay_subSKU(db_conn=db_conn, itemid=itemid)
                if sub_reuslt['code'] == 0:
                    sub_items = sub_reuslt['data']
                    for sub_item in sub_items:
                        # sstartprice = sub_item[1]
                        # srealavailable = sub_item[2]
                        try:
                            sproductsku = sub_item[3]
                            subSKU= sub_item[4]
                            ycalculate_price_obj = calculate_price(str(sproductsku))
                            MY_calculate_result = ycalculate_price_obj.calculate_selling_price(profitRate=40, platformCountryCode='SHOPEE',DestinationCountryCode='MY')
                            priceparams['MY_calculate_price'] = MY_calculate_result['sellingPrice_destination']

                            PH_calculate_result = ycalculate_price_obj.calculate_selling_price(profitRate=40,platformCountryCode='SHOPEE',DestinationCountryCode='PH')
                            priceparams['PH_calculate_price'] = PH_calculate_result['sellingPrice_destination']

                            VNM_calculate_result = ycalculate_price_obj.calculate_selling_price(profitRate=40,platformCountryCode='SHOPEE',DestinationCountryCode='VNM')
                            priceparams['VNM_calculate_price'] = VNM_calculate_result['sellingPrice_destination']

                            THA_calculate_result = ycalculate_price_obj.calculate_selling_price(profitRate=40, platformCountryCode='SHOPEE',DestinationCountryCode='THA')
                            priceparams['THA_calculate_price'] = THA_calculate_result['sellingPrice_destination']

                            SG_calculate_result = ycalculate_price_obj.calculate_selling_price(profitRate=40,platformCountryCode='SHOPEE',DestinationCountryCode='SG')
                            priceparams['SG_calculate_price'] = SG_calculate_result['sellingPrice_destination']

                            INA_calculate_result = ycalculate_price_obj.calculate_selling_price(profitRate=40,platformCountryCode='SHOPEE',DestinationCountryCode='INA')
                            priceparams['INA_calculate_price'] = INA_calculate_result['sellingPrice_destination']
                            update_online_ebay_subsku(db_conn=db_conn,itemid=itemid,subSKU=subSKU,priceparams=priceparams)
                        except:
                            continue
        except Exception,ex:
            continue
