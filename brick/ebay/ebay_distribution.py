# coding=utf-8

# import MySQLdb
# import BeautifulSoup
# from random import shuffle
# from django.contrib import messages
# from brick.classredis.classmainsku import classmainsku
# from brick.public.generate_shop_code import generate_code_func

import copy
from bs4 import BeautifulSoup
from random import choice, randint
from django.db.models import Max
from django_redis import get_redis_connection

from brick.ebay.send_to_MQ import Send_to_MQ
from brick.public.shopsku_apply import shopsku_apply
from brick.classredis.classshopsku import classshopsku
from skuapp.table.t_config_store_ebay import t_config_store_ebay
from skuapp.table.t_templet_ebay_wait_upload import t_templet_ebay_wait_upload
from skuapp.table.t_templet_ebay_upload_result import t_templet_ebay_upload_result


def get_upload_result_id(task_id):
    upload_result_id = t_templet_ebay_upload_result.objects.filter(taskid=task_id).aggregate(Max('id'))
    new_id = upload_result_id.get('id__max')
    return new_id


def insert_into_result(result_dict, tempcx):
    lm = ''
    lm_value = ''
    for k, v in result_dict.items():
        if k == 'sku_dict':
            continue
        if lm == '':
            lm = u'%s' % k
        elif lm != '':
            lm = u'%s,%s' % (lm, k)
        if lm_value == '':
            lm_value = u"\'%s\'" % str(v).replace("'", "`")
        elif lm_value != '':
            lm_value = u"%s,\'%s\'" % (lm_value, str(v).replace("'", "`"))
    sql = "insert into t_templet_ebay_upload_result ( %s ) values ( %s );" % (lm, lm_value)
    tempcur = tempcx.cursor()
    tempcur.execute(sql)
    tempcur.execute('commit;')
    tempcur.close()


def charProcess(Description):
    """处理商品描述图片"""
    soup = BeautifulSoup(Description, "lxml")
    if soup is None:
        return
    try:  # 获取page数据
        allimg = soup.html.find_all("img")
        if allimg:
            for obj in allimg:
                Description = Description.replace(obj, '')
    except:
        pass
    return Description


def get_core_list(client, CoreWords):
    """核心关键词库:"""
    CoreWordsList = []
    cur = client.cursor()
    sql_1 = 'select CoreWords from t_product_corewords'

    cur.execute(sql_1)
    for each in cur.fetchall():
        CoreWordsList.append(each[0])

    cur.close()
    return CoreWordsList


def getnewtitle(client, CoreWords, CoreWordsList, Title):
    """生成新的标题和关键标题词"""
    newtitleList = []
    cateList = [',', '|', '，']
    if CoreWords is not None:
        for eachCate in cateList:
            if CoreWords.encode('utf-8').find(eachCate) != -1:
                wordCate = eachCate
    try:
        newtitleList = CoreWords.split(wordCate)
    except:
        pass

    # 在title列表查询核心词是否存在，存在则暂时删除
    titleList = Title.split(' ')
    for CoreWords in newtitleList:
        if CoreWords in titleList:
            titleList.remove(CoreWords)
    # 在剔除核心词的CoreWords和title列表随机替换三个词

    for i in range(3):
        titleList[randint(0, len(titleList) - 1)] = choice(CoreWordsList)

    # 将替换之后的CoreWords和title列表和核心词列表整合
    newTitleList = newtitleList + titleList
    new_Title_str = ' '.join(newTitleList)
    # 判断新的标题字符长度是否超出80
    if len(new_Title_str) > 80:
        while len(" ".join(newTitleList)) > 80:
            newTitleList.pop()
        new_Title_str = ' '.join(newTitleList)

    return new_Title_str


def ebay_unfold_distribution(id, client, request_user):
    """去铺货"""

    redis_conn = get_redis_connection(alias='product')

    classshopsku_obj = classshopsku(db_conn=client, redis_conn=redis_conn)

    keylist = [
        "Category1", "Category2", "`Condition`", "ConditionBewrite", "Quantity", "LotSize", "Duration",
        "ReservePrice", "BestOffer", "BestOfferAutoAcceptPrice", "BestOfferAutoRefusedPrice",
        "AcceptPayment", "PayPalEmailAddress", "Location", "LocationCountry", "ReturnsAccepted",
        "RefundOptions", "ReturnsWithin", "ReturnPolicyShippingCostPaidBy",
        "ReturnPolicyDescription", "GalleryType", "Bold", "PrivateListing", "HitCounter",
        "sku", "PictureURL", "Title", "SubTitle", "IbayCategory", "StartPrice", "BuyItNowPrice",
        "other_itemnum", "ShippingService1", "ShippingServiceCost1", "ShippingServiceAdditionalCost1",
        "ShippingService2", "ShippingServiceCost2", "ShippingServiceAdditionalCost2",
        "ShippingService3", "ShippingServiceCost3", "ShippingServiceAdditionalCost3",
        "ShippingService4", "ShippingServiceCost4", "ShippingServiceAdditionalCost4",
        "InternationalShippingService1", "InternationalShippingServiceCost1",
        "InternationalShippingServiceAdditionalCost1", "InternationalShipToLocation1",
        "InternationalShippingService2", "InternationalShippingServiceCost2",
        "InternationalShippingServiceAdditionalCost2", "InternationalShipToLocation2",
        "InternationalShippingService3", "InternationalShippingServiceCost3",
        "InternationalShippingServiceAdditionalCost3", "InternationalShipToLocation3",
        "InternationalShippingService4", "InternationalShippingServiceCost4",
        "InternationalShippingServiceAdditionalCost4", "InternationalShipToLocation4",
        "InternationalShippingService5", "InternationalShippingServiceCost5",
        "InternationalShippingServiceAdditionalCost5", "InternationalShipToLocation5",
        "DispatchTimeMax", "ExcludeShipToLocation", "StoreCategory1", "StoreCategory2",
        "IbayTemplate", "IbayInformation", "IbayComment", "Description", "`Language`",
        "IbayOnlineInventoryHold", "IbayRelistSold", "IbayRelistUnsold", "IBayEffectType",
        "IbayEffectImg", "IbayCrossSelling", "Variation", "outofstockcontrol",
        "EPID", "ISBN", "UPC", "EAN", "SecondOffer", "ImmediatelyPay", "Currency", "LinkedPayPalAccount",
        "MBPVCount", "MBPVPeriod", "MUISICount", "MUISIPeriod", "MaximumItemCount", "MinimumFeedbackScore",
        "Specifics1", "Specifics2", "Specifics3", "Specifics4", "Specifics5", "Specifics6", "Specifics7",
        "Specifics8", "Specifics9", "Specifics10", "Specifics11", "Specifics12", "Specifics13", "Specifics14",
        "Specifics15", "Specifics16", "Specifics17", "Specifics18", "Specifics19", "Specifics20", "Specifics21",
        "Specifics22", "Specifics23", "Specifics24", "Specifics25", "Specifics26", "Specifics27", "Specifics28",
        "Specifics29", "Specifics30", "CreateTime", "CreateStaff", "UpdateTime", "UpdateStaff", "OssUrl", "CoreWords",
        "Flag", "Status", "ExcelFile", "variationSpecificsSet", "Images", "ShopSets", "TimePlan", "Site", "Selleruserid", "Seller"
    ]

    cur = client.cursor()
    sql = "select Category1,Category2,`Condition`,ConditionBewrite,Quantity,LotSize,Duration,"\
        "ReservePrice,BestOffer,BestOfferAutoAcceptPrice,BestOfferAutoRefusedPrice,"\
        "AcceptPayment,PayPalEmailAddress,Location,LocationCountry,ReturnsAccepted,"\
        "RefundOptions,ReturnsWithin,ReturnPolicyShippingCostPaidBy,"\
        "ReturnPolicyDescription,GalleryType,Bold,PrivateListing,HitCounter,"\
        "sku,PictureURL,Title,SubTitle,IbayCategory,StartPrice,BuyItNowPrice,"\
        "other_itemnum,ShippingService1,ShippingServiceCost1,ShippingServiceAdditionalCost1,"\
        "ShippingService2,ShippingServiceCost2,ShippingServiceAdditionalCost2,"\
        "ShippingService3,ShippingServiceCost3,ShippingServiceAdditionalCost3,"\
        "ShippingService4,ShippingServiceCost4,ShippingServiceAdditionalCost4,"\
        "InternationalShippingService1,InternationalShippingServiceCost1,"\
        "InternationalShippingServiceAdditionalCost1,InternationalShipToLocation1,"\
        "InternationalShippingService2,InternationalShippingServiceCost2,"\
        "InternationalShippingServiceAdditionalCost2,InternationalShipToLocation2,"\
        "InternationalShippingService3,InternationalShippingServiceCost3,"\
        "InternationalShippingServiceAdditionalCost3,InternationalShipToLocation3,"\
        "InternationalShippingService4,InternationalShippingServiceCost4,"\
        "InternationalShippingServiceAdditionalCost4,InternationalShipToLocation4,"\
        "InternationalShippingService5,InternationalShippingServiceCost5,"\
        "InternationalShippingServiceAdditionalCost5,InternationalShipToLocation5,"\
        "DispatchTimeMax,ExcludeShipToLocation,StoreCategory1,StoreCategory2,"\
        "IbayTemplate,IbayInformation,IbayComment,Description,`Language`,"\
        "IbayOnlineInventoryHold,IbayRelistSold,IbayRelistUnsold,IBayEffectType,"\
        "IbayEffectImg,IbayCrossSelling,Variation,outofstockcontrol,"\
        "EPID,ISBN,UPC,EAN,SecondOffer,ImmediatelyPay,Currency,LinkedPayPalAccount,"\
        "MBPVCount,MBPVPeriod,MUISICount,MUISIPeriod,MaximumItemCount,MinimumFeedbackScore,"\
        "Specifics1,Specifics2,Specifics3,Specifics4,Specifics5,Specifics6,Specifics7,"\
        "Specifics8,Specifics9,Specifics10,Specifics11,Specifics12,Specifics13,Specifics14,"\
        "Specifics15,Specifics16,Specifics17,Specifics18,Specifics19,Specifics20,Specifics21," \
        "Specifics22,Specifics23,Specifics24,Specifics25,Specifics26,Specifics27,Specifics28," \
        "Specifics29,Specifics30,CreateTime,CreateStaff,UpdateTime,UpdateStaff,OssUrl,CoreWords,"\
        "Flag,`Status`,ExcelFile,variationSpecificsSet,Images,ShopSets,TimePlan,Site,Selleruserid,Seller" \
        " from t_templet_ebay_wait_upload where `Status`='OPEN' and id = %s ;"
    cur.execute(sql, (id,))

    objs = cur.fetchall()
    cur.close()
    sRes = {'code': -1, 'message': ''}
    for obj in objs:
        mydict = {}
        for i in range(0, len(obj)):
            mydict[keylist[i]] = obj[i]
        waitUploadList = []
        if mydict['ShopSets'] is not None and mydict['ShopSets'].strip() != '':
            for shopcode in mydict['ShopSets'].split(','):  # ebay 铺货目标店铺
                newdict = copy.deepcopy(mydict)

                try:
                    variation_obj = t_templet_ebay_wait_upload.objects.get(pk=id)
                except t_templet_ebay_wait_upload.DoesNotExist:
                    sRes['message'] = 't_templet_ebay_wait_upload id: %s is not Exist' % id
                    return sRes
                ExcelFile = variation_obj.ExcelFile
                Site = mydict['Site']
                newdict['ExcelFile'] = ExcelFile
                newdict['ShopName'] = shopcode

                try:
                    store_info_obj = t_config_store_ebay.objects.get(storeName=shopcode)
                    Seller = store_info_obj.storeOwner
                    shop_name = store_info_obj.ShopName
                    # Site = store_info_obj.siteID
                except t_config_store_ebay.DoesNotExist:
                    Seller = ''
                    shop_name = ''
                    # Site = mydict['Site']

                newdict['Seller'] = Seller

                variations = variation_obj.Variation

                shop_skus = list()
                if variations:
                    # 有变体信息
                    vars_info = eval(variations).get('Variation')
                    if vars_info:
                        for i in vars_info:
                            shop_sku = i.get('SKU')
                            if shop_sku:
                                shop_skus.append(shop_sku)
                else:
                    shop_sku = variation_obj.sku
                    shop_skus.append(shop_sku)

                if shop_skus:
                    for shop_sku in shop_skus:
                        if shop_sku.find('+') != -1:
                            sRes['message'] = 'Can not Publish combination shop sku.'
                            return sRes
                else:
                    sRes['message'] = 'This Product does not find shop sku.'
                    return sRes

                pro_skus = list()
                shop_pro_info = dict()
                for shop_sku in shop_skus:
                    if shop_sku.find('*') != -1:
                        ss = shop_sku.split('*')[0]
                    else:
                        ss = shop_sku
                    pro_sku = classshopsku_obj.getSKU(ss)
                    if not pro_sku:
                        sRes['message'] = 'Can not get product sku for shopsku: %s' % shop_sku
                        return sRes
                    pro_skus.append(pro_sku)
                    shop_pro_info[shop_sku] = pro_sku

                sku_dict = dict()
                if pro_skus:
                    product_skus = ','.join(pro_skus)
                    result = shopsku_apply(product_skus, shop_name, apply_type="SONSKUAPPLY", first_name=request_user)
                    if result['result'] == 'DEFEAT' or result.get('defeat_sku'):
                        sRes['message'] = result.get('error_info', '') + str(result.get('defeat_sku', ''))
                        return sRes
                    shop_sku_pro_info = result['success_sku']
                    db_sku_info = dict()
                    for i in shop_pro_info:
                        num = ''
                        if i.find('*') != -1:
                            num = i.split('*')[-1]
                        for j in shop_sku_pro_info:
                            if shop_pro_info[i] == shop_sku_pro_info[j]:
                                key = i
                                if num:
                                    value = j + '*' + num
                                else:
                                    value = j
                                sku_dict[key] = value
                                db_sku_info[shop_pro_info[i]] = j
                if sku_dict:
                    newdict['sku_dict'] = sku_dict
                else:
                    sRes['message'] = 'Apply New Shop SKU Falied.'
                    return sRes

                newdict['product_sku'] = db_sku_info.keys()
                newdict['shopsku'] = db_sku_info.values()

                # 核心标题
                CoreWordsList = get_core_list(client, newdict['CoreWords'])
                newdict['Title'] = getnewtitle(client, newdict['CoreWords'], CoreWordsList, newdict['Title'])
                newdict['Description'] = charProcess(newdict['Description'])
                newdict['Site'] = Site
                newdict['taskid'] = id

                waitUploaddict = {}
                waitUploaddict = newdict.copy()
                waitUploaddict['id'] = id

                insert_into_result(newdict, client)
                result_id = get_upload_result_id(newdict['taskid'])
                waitUploaddict['result_id'] = result_id
                waitUploadList.append(waitUploaddict)

        insert_into_MQ(id, waitUploadList)
        sRes['code'] = 0
        return sRes


def insert_into_MQ(id, waitUploadList):
    if waitUploadList is None and len(waitUploadList) == 0:
        return None

    mq_list = []
    for mq_dict in waitUploadList:
        skuinfo_store = {
            # 'taskid':mq_dict['id'],
            'uploadtaskid': id,
            'result_id': mq_dict['result_id'],
            'title': mq_dict['Title'],
            'shopname': mq_dict['ShopName'],
            'product_sku': mq_dict['product_sku'],
            'shopsku': mq_dict['shopsku'],
            'sku_dict': mq_dict['sku_dict'],
            'time': '120',
            'Site': mq_dict['Site'],
        }
        mq_list.append(skuinfo_store)

    smq = Send_to_MQ()
    smq.ebay_to_MQ({'ebay_publish_product': 'ebay_publish_product', 'body': mq_list})
