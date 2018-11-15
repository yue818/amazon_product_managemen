#-*-coding:utf-8-*-

u"""
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: wish_pub_start.py
 @time: 2018-04-10 19:55
"""
import json
from django.db import connection

from brick.table.t_wish_store_oplogs import t_wish_store_oplogs
from .to_pub import to_pub
from brick.wish.wish_api_before.token_verification import verb_token
from wishpubapp.table.t_templet_wish_publish_result import t_templet_wish_publish_result

from .wish_image_upload import wish_image_upload

from brick.wish.wish_store import Wish_Data_Syn, MainBatchUpdateShipping
from wishpubapp.table.t_templet_wish_country_shipping import t_templet_wish_country_shipping


# 刊登之后，可以直接刷新
def PostRefresh(paramlist):
    sResult = Wish_Data_Syn(paramlist)
    if not sResult['Code'] == 1:
        raise Exception('Synchronous refresh error! Product id: {}, {}'.format(paramlist[1], sResult['messages']))


# 应用运费模板设置
def ApplicationShippingForm(paramlist, templet_id):
    if templet_id:
        templet_obj = t_templet_wish_country_shipping.objects.get(id=templet_id)
        paramlist.append(templet_obj.Description.replace('add', '_add'))

        mResult = MainBatchUpdateShipping(paramlist, '', 'STANDARD')
        if not mResult['Code'] == 1:
            raise Exception('Application shipping template error! Product id: {}, {}'.format(paramlist[1],mResult['messages']))
    else:
        print 'No national shipping template was selected! '



def arrange_params(opnum, type, opkey):
    t_wish_store_oplogs_obj = t_wish_store_oplogs(connection)

    result_objs = t_templet_wish_publish_result.objects.filter(pid=opkey,Status='waiting')
    param, shopname, parentsku, ShippingTempletID = '', '', '', ''
    try:
        if result_objs.exists():
            result_obj = result_objs[0]
            shopname = result_obj.ShopName

            auth_info = verb_token(shopname[:9], connection)
            assert auth_info['errorcode'] == 1, auth_info['errortext']

            pubdata = {}  # 用于刊登的数据 集合
            pubdata['id'] = opkey

            uResult = wish_image_upload(result_obj.MainImage, auth_info)
            assert uResult['errorcode'] == 1, '%s'% uResult['errortext']
            pubdata['main_image'] = uResult['image_url']  # 产品主图

            pubdata['first'] = {}
            pubdata['first']['url'] = 'https://merchant.wish.com/api/v2/product/add'

            pubdata['first']['product'] = {}
            pubdata['first']['product']['access_token']  = auth_info['access_token']
            pubdata['first']['product']['format']  = 'json'
            pubdata['first']['product']['enabled'] = True
            pubdata['first']['product']['name']    = result_obj.Title
            pubdata['first']['product']['tags']          = result_obj.Tags
            pubdata['first']['product']['description']   = result_obj.Description

            maininfo = json.loads(result_obj.MainInfo)
            parentsku = maininfo.get('ParentSKU')
            pubdata['first']['product']['parent_sku'] = parentsku
            ShippingTempletID = maininfo.get('CountryShipping', '')

            epiclist = []
            for epic in result_obj.ExtraImages.split('|'):
                if epic.strip() != '':
                    euResult = wish_image_upload(epic, auth_info)
                    assert euResult['errorcode'] == 1, euResult['errortext']
                    epiclist.append(euResult['image_url'])

            pubdata['first']['product']['extra_images'] = '|'.join(epiclist)  # 产品附图

            v_datas = json.loads(result_obj.Variants)

            if len(v_datas) >= 1:
                v_data = v_datas[0]
                if not parentsku:
                    pubdata['first']['product']['parent_sku'] = v_data.get('ShopSKU')

                assert v_data.get('ShopSKU'), u'店铺SKU不能为空'
                pubdata['first']['product']['sku']            = v_data.get('ShopSKU')
                pubdata['first']['product']['main_image']     = v_data.get('vPic')
                pubdata['first']['product']['color']          = v_data.get('Color')
                pubdata['first']['product']['size']           = v_data.get('Size')
                pubdata['first']['product']['msrp']           = v_data.get('Msrp')
                pubdata['first']['product']['price']          = v_data.get('Price')
                pubdata['first']['product']['inventory']      = v_data.get('Kc')
                pubdata['first']['product']['shipping']       = v_data.get('Shipping')
                pubdata['first']['product']['shipping_time']  = v_data.get('Shippingtime')

                if v_data.get('vPic'):
                    uvResult = wish_image_upload(v_data.get('vPic'), auth_info)
                    assert uvResult['errorcode'] == 1, uvResult['errortext']
                    pubdata['first']['product']['main_image'] = uvResult['image_url']  # 第一变体图

                pubdata['second'] = {}
                pubdata['second']['url'] = 'https://merchant.wish.com/api/v2/variant/add'

                pubdata['second']['product'] = []
                for i in range(1,len(v_datas)):
                    v_d = v_datas[i]
                    v_dict = {}
                    v_dict['access_token']  = auth_info['access_token']
                    v_dict['format']        = 'json'
                    v_dict['parent_sku']    = pubdata['first']['product']['parent_sku']

                    assert v_d.get('ShopSKU'), u'店铺SKU不能为空'
                    v_dict['sku']           = v_d.get('ShopSKU')
                    v_dict['main_image']    = v_d.get('vPic')
                    v_dict['enabled']       = True
                    v_dict['color']         = v_d.get('Color')
                    v_dict['size']          = v_d.get('Size')
                    v_dict['msrp']          = v_d.get('Msrp')
                    v_dict['price']         = v_d.get('Price')
                    v_dict['inventory']     = v_d.get('Kc')
                    # v_dict['shipping']      = v_d.get('Shipping')   10.8以后不再允许创建变体时设置运费
                    v_dict['shipping_time'] = v_d.get('Shippingtime')

                    if v_d.get('vPic'):
                        vuResult = wish_image_upload(v_d.get('vPic'), auth_info)
                        assert vuResult['errorcode'] == 1, vuResult['errortext']
                        v_dict['main_image'] = vuResult['image_url']  # 各变体图

                    pubdata['second']['product'].append(v_dict)

            param = json.dumps(pubdata)

            print '================' + param
        if param:
            # 在这里调用刊登函数
            pResult = to_pub(param, opkey)
            assert pResult['errorcode'] == 1, u'errortext:{}; param:{}'.format(pResult['errortext'], param)
            try:
                ApplicationShippingForm([shopname[:9], pResult['productid']], ShippingTempletID)  # 应用模板数据
                PostRefresh([shopname[:9], pResult['productid'], parentsku])  # 刷新链接到本地
            except Exception as er:
                applyerror = u'Published is successful! BUT, {}'.format(er)
                try:
                    PostRefresh([shopname[:9], pResult['productid'], parentsku])  # 刷新链接到本地
                except Exception as error:
                    if u'{}'.format(er) != u'{}'.format(error):
                        applyerror = applyerror + u'{}'.format(error)

                raise Exception(applyerror)
        else:
            raise Exception('param===%s;' % param)

        result_objs.update(param=param,Status='success',result=pResult['productid'])
        t_wish_store_oplogs_obj.updateStatusP(opnum,opkey,'over','')
    except Exception, e:
        errortext = u'%s:%s' % (Exception, e)
        if '\u' in errortext:
            try:
                errortext = errortext.decode("unicode_escape")
            except:
                pass
        result_objs.update(param='', Status='error', result=errortext)
        t_wish_store_oplogs_obj.updateStatusP(opnum, opkey, 'error', errortext)








