# coding=utf-8

# from brick.ebay.ebay_column import insertdictk
from brick.ebay.get_format_string import get_format_string
# from brick.ebay.save_image_to_oss import save_image_to_oss
import xlrd
import copy

insertdictk = ['Site', 'Selleruserid', 'Category1', 'Category2', '`Condition`', 'ConditionBewrite', 'Quantity', 'LotSize',
                   'Duration', 'ReservePrice', 'BestOffer', '`BestOfferAutoAcceptPrice`', '`BestOfferAutoRefusedPrice`',
                   'AcceptPayment', 'PayPalEmailAddress',
                   'Location', 'LocationCountry', 'ReturnsAccepted', 'RefundOptions', 'ReturnsWithin',
                   'ReturnPolicyShippingCostPaidBy', 'ReturnPolicyDescription',
                   'GalleryType', 'Bold', 'PrivateListing', 'HitCounter', 'sku', 'PictureURL', 'Title', 'SubTitle',
                   'IbayCategory', 'StartPrice', 'BuyItNowPrice', 'other_itemnum',
                   'ShippingService1', 'ShippingServiceCost1', 'ShippingServiceAdditionalCost1', 'ShippingService2',
                   'ShippingServiceCost2', 'ShippingServiceAdditionalCost2',
                   'ShippingService3', 'ShippingServiceCost3', 'ShippingServiceAdditionalCost3', 'ShippingService4',
                   'ShippingServiceCost4', 'ShippingServiceAdditionalCost4',
                   'InternationalShippingService1', 'InternationalShippingServiceCost1',
                   'InternationalShippingServiceAdditionalCost1', 'InternationalShipToLocation1',
                   'InternationalShippingService2', 'InternationalShippingServiceCost2',
                   'InternationalShippingServiceAdditionalCost2', 'InternationalShipToLocation2',
                   'InternationalShippingService3', 'InternationalShippingServiceCost3',
                   'InternationalShippingServiceAdditionalCost3', 'InternationalShipToLocation3',
                   'InternationalShippingService4', 'InternationalShippingServiceCost4',
                   'InternationalShippingServiceAdditionalCost4', 'InternationalShipToLocation4',
                   'InternationalShippingService5', 'InternationalShippingServiceCost5',
                   'InternationalShippingServiceAdditionalCost5', 'InternationalShipToLocation5',
                   'DispatchTimeMax', 'ExcludeShipToLocation', 'StoreCategory1', 'StoreCategory2', 'IbayTemplate',
                   'IbayInformation', 'IbayComment', 'Description', '`Language`',
                   'IbayOnlineInventoryHold', 'IbayRelistSold', 'IbayRelistUnsold', 'IBayEffectType', 'IbayEffectImg',
                   'IbayCrossSelling', 'Variation', 'outofstockcontrol', 'EPID',
                   'ISBN', 'UPC', 'EAN', 'SecondOffer', 'ImmediatelyPay', 'Currency', 'LinkedPayPalAccount',
                   'MBPVCount', 'MBPVPeriod', 'MUISICount', 'MUISIPeriod', 'MaximumItemCount',
                   'MinimumFeedbackScore', 'Specifics1', 'Specifics2', 'Specifics3', 'Specifics4', 'Specifics5',
                   'Specifics6', 'Specifics7', 'Specifics8', 'Specifics9', 'Specifics10',
                   'Specifics11', 'Specifics12', 'Specifics13', 'Specifics14', 'Specifics15', 'Specifics16',
                   'Specifics17', 'Specifics18', 'Specifics19', 'Specifics20', 'Specifics21', 'Specifics22',
                   'Specifics23', 'Specifics24', 'Specifics25', 'Specifics26', 'Specifics27', 'Specifics28',
                   'Specifics29', 'Specifics30', 'Images', 'CreateTime', 'CreateStaff', 'UpdateTime', 'UpdateStaff',
                   'CoreWords', 'OssUrl', 'Flag', 'ExcelFile', '`Status`', 'variationSpecificsSet']

new_insertdictk=copy.copy(insertdictk)
new_insertdictk.insert(insertdictk.index('MinimumFeedbackScore'),'listingcategory_id')
def read_excel(file_obj, client, first_name, now_time):
    """
    读取eBay采集箱上传的Excel文档
    :param file_obj: Excel文件对象
    :param client: 数据库连接
    :param first_name: 用户中文名
    :param now_time: 用户提交Excel的时间
    """
    create_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    tempList = [create_time, first_name, create_time, first_name, '', '', 1, file_obj, 'NO']
    variationList = ['',]

    # 直接读取Excel数据流
    data = xlrd.open_workbook(filename=None, file_contents=file_obj.read())

    table = data.sheets()[0]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    flag = True if ncols == 130 else False
    cur = client.cursor()
    for rownum in range(1, nrows):
        try:
            signleInfoList = []
            row = table.row_values(rownum)
            if row:
                # 传递参数到上传图片函数，获取处理后的图片地址和详细描述
                PictureURL = get_format_string(row[29])
                allPicUrls = PictureURL.split('\n')
                allPicUrls_str = ','.join(allPicUrls)
                # ebay_url_list = allPicUrls

                for i in range(1,ncols):
                    if i == 3:
                        continue
                    elif i == 28:
                        sku = str(row[i]).split('\\')[0]
                        signleInfoList.append(sku)
                    elif i == 83:
                        try:
                            signleInfoList.append(deal_varitions(eval(str(row[i]).replace("'", "`")), client))
                        except:
                            signleInfoList.append('')
                    else:
                        signleInfoList.append(get_format_string(row[i]))

                    # if i == 83:
                    #     variation = str(row[i])
                    #     if variation is not None and variation.strip()!= '':
                    #         for each in eval(variation).get('Pictures'):
                    #             try:
                    #                 ebay_url = each["VariationSpecificPictureSet"]["PictureURL"]
                    #                 if ebay_url is not None:
                    #                     ebay_url_list += ebay_url
                    #             except:
                    #                 pass

                signleInfoList.append(allPicUrls_str)

            # 将图片上传到OSS
            # save_image_to_oss(ebay_url_list)

            signleInfoList += tempList
            signleInfoList += variationList
            if flag:
                lk = ','.join(new_insertdictk)
            else :
                lk = ','.join(insertdictk)
            lv = ''
            for i in range(0,len(signleInfoList)):
                if lv == '':
                    lv = '\"%s\"'%str(signleInfoList[i]).encode('utf-8').replace("'","`").replace('"',"'")
                else:
                    lv = '%s,\"%s\"'%(lv,str(signleInfoList[i]).encode('utf-8').replace("'","`").replace('"',"'"))
            sql = 'insert into t_templet_ebay_collection_box (%s) VALUES (%s) ;'%(lk,lv)
            logging.debug('sql:===================================================================== %s' % sql)
            cur.execute(sql)
            cur.execute('commit ;')
        except:
            cur = client.cursor()
    cur.close()


def deal_varitions(infos, client):
    variations = infos.get('Variation', '')
    cur = client.cursor()

    if variations == '':
        return
    else:
        for variation in variations:
            sku = variation.get('SKU', '')
            if sku == '':
                return
            else:
                sku_list = sku.split('+')
                new_sku = ''
                for sku_param in sku_list:
                    sku_part = sku_param.split('*')[0].split('\\')[0]
                    try:
                        num_part = sku_param.split('*')[1].split('\\')[0]
                    except:
                        num_part = ''

                    productSKU_sql = 'select NID from py_db.b_goods WHERE SKU=\"%s\"; ' % sku_part
                    cur.execute(productSKU_sql)
                    b_goods_info = cur.fetchone()
                    if b_goods_info is not None:
                        if new_sku == '':
                            new_sku = sku_part + '*' + num_part if num_part != '' else  sku_part
                        else:
                            new_sku = new_sku + '+' + sku_part + '*' + num_part if num_part != '' else  new_sku + '+' + sku_part
                    else:
                        shopSKU_sql = 'select SKU from py_db.b_goodsskulinkshop WHERE ShopSKU=\"%s\"; ' % sku_part
                        cur.execute(shopSKU_sql)
                        b_goodsskulinkshop_info = cur.fetchone()
                        if b_goodsskulinkshop_info is not None:
                            if new_sku == '':
                                new_sku = b_goodsskulinkshop_info[0] + '*' + num_part if num_part != '' else  b_goodsskulinkshop_info[0]
                            else:
                                new_sku = new_sku + '+' + b_goodsskulinkshop_info[0] + '*' + num_part if num_part != '' else  new_sku + '+' + b_goodsskulinkshop_info[0]
                        else:
                            if new_sku == '':
                                new_sku = ''
                variation['SKU'] = new_sku

    cur.close()
    return str(infos).replace("'",'"')