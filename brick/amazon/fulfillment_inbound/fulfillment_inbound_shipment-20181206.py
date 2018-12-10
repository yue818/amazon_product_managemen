# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: fulfillment_inbound_shipment-20181206.py
 @time: 2018/12/6 10:02
"""
from mws import InboundShipments
import pymysql
import datetime
import logging
import logging.handlers
import traceback


# 按天记录日志
log_day = datetime.datetime.now().strftime("%Y%m%d")
log_file_name = 'fba_inbound_' + log_day + '.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_file_name,
                    filemode='a')
logging.handlers.RotatingFileHandler(log_file_name,
                                     maxBytes=20 * 1024 * 1024,
                                     backupCount=10)


class FbaInbound:
    def __init__(self, auth_info_inbound, data_base_inbound):
        """
        from_addr = dict()
        from_addr['name'] = 'Anjun'  # 1
        from_addr['address_1'] = 'Jiadingqu Antingzhen Xiechunlu 1300nong 3hao Aqu'  # 1
        # from_addr['address_2'] = 'address_2'  # 0
        from_addr['city'] = 'Shanghai'  # 1
        # from_addr['district_or_county'] = 'district_or_county'  # 0
        from_addr['state_or_province'] = 'Shanghai'  # 0
        from_addr['postal_code'] = '201804'  # 0
        from_addr['country'] = 'CN'  # 0

        """
        self.auth_info = auth_info_inbound
        self.inbound_public = InboundShipments(self.auth_info['AWSAccessKeyId'],
                                               self.auth_info['SecretKey'],
                                               self.auth_info['SellerId'],
                                               self.auth_info['ShopSite'],
                                               from_address=self.auth_info['from_address']
                                               )
        self.data_base = data_base_inbound
        self.db_conn = pymysql.connect(self.data_base['HOST'],
                                       self.data_base['USER'],
                                       self.data_base['PASSWORD'],
                                       self.data_base['NAME'],
                                       charset='utf8')

    def close_db_conn(self):
        try:
            if self.db_conn:
                self.db_conn.close()
        except Exception as close_db_ex:
            logging.error('Class  FbaInbound close db connection failed!  %s' % close_db_ex)
            logging.error('Detailed reason:\n%s' % traceback.format_exc())

    def create_inbound_plan(self):
        """
        items= list()
        item_each = dict()

        item_each['sku'] = 'sku'  # 1
        item_each['quantity'] = 'quantity'  # 1
        item_each['quantity_in_case'] = 'quantity_in_case'
        item_each['asin'] = 'asin'
        item_each['condition'] = 'condition'

        items.append(item_each)

        """
        try:
            inbound_plan = self.inbound_public.create_inbound_shipment_plan(items=self.auth_info['items'],
                                                                            country_code=self.auth_info['ShopSite'],
                                                                            label_preference=self.auth_info['label_preference'])
            print inbound_plan
            logging.debug('inboudn_plan_return:\n%s' % inbound_plan)
            print '--'*20
            print inbound_plan._response_dict
            logging.debug('inboudn_plan_return dict:\n%s' % inbound_plan._response_dict)
        except Exception as inbound_plan_ex:
            print inbound_plan_ex
            logging.error('create inbound plan error:\n%s' % traceback.format_exc())

    def create_inboud(self, shipment_id, shipment_name, destination_center_id, items, shipment_status='WORKING',
                      case_required=False, box_contents_source='FEED'):
        inbound_result = self.inbound_public.create_inbound_shipment(shipment_id=shipment_id,
                                                                     shipment_name=shipment_name,
                                                                     destination=destination_center_id,
                                                                     items=items,
                                                                     shipment_status=shipment_status,
                                                                     label_preference=self.auth_info['label_preference'],
                                                                     case_required=case_required,
                                                                     box_contents_source=box_contents_source
                                                                     )
        print inbound_result

    def update_inboud(self, shipment_id, shipment_name, destination_center_id, items, shipment_status,
                      case_required=False, box_contents_source='Feed'):
        update_result = self.inbound_public.update_inbound_shipment(shipment_id=shipment_id,
                                                                    shipment_name=shipment_name,
                                                                    destination=destination_center_id,
                                                                    items=items,
                                                                    shipment_status=shipment_status,
                                                                    label_preference=self.auth_info['label_preference'],
                                                                    case_required=case_required,
                                                                    box_contents_source=box_contents_source)
        print update_result

    def put_transport_content(self):
        pass


if __name__ == '__main__':
    auth_info = dict(
        SellerId='A3S018PDA7TP7T',
        MarketplaceId='ATVPDKIKX0DER',
        SecretKey='9DI61uHN2sG1KvhRlpJgNTzeEfhlK/G3kUZ5tH+l',
        AWSAccessKeyId='AKIAJA5YS3V5RM5EKPKQ',
        ShopSite='US',
        label_preference='SELLER_LABEL',
        from_address=dict(
            name='Anjun',
            address_1='Jiadingqu Antingzhen Xiechunlu 1300nong 3hao Aqu',
            city='Shanghai',
            state_or_province='Shanghai',
            postal_code='201804',
            country='CN',
        ),
        items=[dict(sku='P1X04DZ6YE8071', quantity='20'),
               dict(sku='A!N!!#0272FBK', quantity='30',),
               dict(sku='A!N!!#0232F01', quantity='25', ),
               dict(sku='A!N!!#0232F04', quantity='40', ),
               ]
    )

    data_base = dict(
        HOST='rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        NAME='hq_db',
        PORT='3306',
        USER='by15161458383',
        PASSWORD='K120Esc1')
    inbound_obj = FbaInbound(auth_info, data_base)
    inbound_obj.create_inbound_plan()
    inbound_obj.close_db_conn()
