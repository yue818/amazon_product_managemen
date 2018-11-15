#-*-coding:utf-8-*-
from brick.table.t_product_upc_id_amazon import t_product_upc_id_amazon
from brick.amazon.stitch_MQ_body import stitch_MQ_body
from brick.amazon.schedule_to_MQ import schedule_to_MQ
from brick.table.t_shopsku_information_binding import t_shopsku_information_binding
from brick.table.t_templet_amazon_upload_result import t_templet_amazon_upload_result
from brick.table.t_templet_amazon_wait_upload import t_templet_amazon_wait_upload
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: deal_with_amazon_upload.py
 @time: 2018/2/13 10:10
"""   
class deal_with_amazon_upload():
    def __init__(self, db_conn):
        self.cnxn = db_conn

    def deal_with_amamzon_upload(self,paramsMQ):
        amazon_upload_obj_id = paramsMQ['amazon_upload_obj_id']
        templet_amazon_upload_result_id = paramsMQ['templet_amazon_upload_result_id']
        templet_amazon_wait_upload_obj = paramsMQ['templet_amazon_wait_upload_obj']
        seller_sku_list = [templet_amazon_wait_upload_obj['item_sku'],]
        auth_info = paramsMQ['auth_info']
        auth_info['amazon_upload_id'] = amazon_upload_obj_id
        auth_info['amazon_upload_result_id'] = templet_amazon_upload_result_id
        MQ_dict = paramsMQ['MQ_dict']
        # schedule_to_MQ_obj = schedule_to_MQ(MQ_dict['IP'], MQ_dict['MQPort'], MQ_dict['MQUser'], MQ_dict['MQPassword'])
        variation_objs = paramsMQ['t_templet_amazon_published_variation_objs']
        if variation_objs:
            for variation_obj in variation_objs:
                seller_sku_list.append(variation_obj['child_sku'])
        auth_info['seller_sku_list'] = seller_sku_list

        t_templet_amazon_upload_result_obj = t_templet_amazon_upload_result(self.cnxn)
        queueName = auth_info['IP'] + '_' + 'amazon_upload_toy'
        stitch_MQ_body_obj = stitch_MQ_body()
        result = stitch_MQ_body_obj.stitching_goods_info_to_body({'auth_info': auth_info, 'goods_upload': templet_amazon_wait_upload_obj,
                                                                  'variation': paramsMQ['variation'],
                                                                  't_templet_amazon_published_variation_objs': variation_objs,
                                                                  'skuCount': paramsMQ['skuCount']})

        schedule_to_MQ_obj = schedule_to_MQ(MQ_dict['IP'], MQ_dict['MQPort'], MQ_dict['MQUser'], MQ_dict['MQPassword'])
        result = schedule_to_MQ_obj.xml_to_MQ({'queueName': queueName, 'body': result['result']})
        if result['errorcode'] == -1:
            resultInfo = 'put into MQ failed'
            errorMessages = result['errortext']
            mqResponseInfo = 'put into MQ failed'
        else:
            resultInfo = ''
            if result['result']['resultIfo'] == True:
                t_templet_amazon_wait_upload_obj = t_templet_amazon_wait_upload(self.cnxn)
                t_templet_amazon_wait_upload_obj.update_status('OPEN', templet_amazon_wait_upload_obj['id'])
                mqResponseInfo = result['result']
                t_shopsku_information_binding_obj = t_shopsku_information_binding(self.cnxn)
                params = {'SKU': templet_amazon_wait_upload_obj['productSKU'], 'ShopSKU': templet_amazon_wait_upload_obj['item_sku'],
                          'Memo': paramsMQ['shopName'],
                          'Seller': paramsMQ['user'],
                          'Theway': 'Amazon upload'}
                link_sku_list = paramsMQ['link_sku_list']
                for link_sku in link_sku_list:
                    for k,v in link_sku.items():
                        params['SKU'] = k
                        params['ShopSKU'] = v
                        linkResult = t_shopsku_information_binding_obj.insert_into_shopsku_information_banding(params)
                        if linkResult['code'] == 0:
                            resultInfo += u'link goods_sku(%s) into shopSKU(%s) successful, ' % (k, v)
                        if linkResult['code'] == 1:
                            resultInfo += u'link goods_sku(%s) into shopSKU(%s)  failed, ' %(k, v)
                resultInfo += u'put goods(id: %s) into MQ successful' % templet_amazon_wait_upload_obj['id']

            else:
                resultInfo += u'put goods(id: %s) into MQ failed' % templet_amazon_wait_upload_obj['id']
                mqResponseInfo = ''
            errorMessages = queueName
        t_templet_amazon_upload_result_obj.updateStatus(
            {'status': 'UPLOAD', 'resultInfo': resultInfo, 'errorMessages': errorMessages,
             'mqResponseInfo': mqResponseInfo, 'id': templet_amazon_upload_result_id})


