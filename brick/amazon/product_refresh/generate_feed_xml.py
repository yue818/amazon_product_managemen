# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: vps_feed_xml.py
 @time: 2018-02-07 15:41
"""
import uuid
import time
import xml.dom.minidom

submit_type = {'inventory': '_POST_INVENTORY_AVAILABILITY_DATA_',
               'price': '_POST_PRODUCT_PRICING_DATA_',
               'product': '_POST_PRODUCT_DATA_',
               'image': '_POST_PRODUCT_IMAGE_DATA_'}


class GenerateFeedXml:
    def __init__(self, auth_info):
        self.auth_info = auth_info
        pass

    @staticmethod
    def generate_message_id():
        """
         生成唯一的messageid供feed使用

        """
        #message_id = uuid.uuid4()
        # message_id = 111111111111
        message_id = int(time.time() * 1000)
        return message_id

    def get_inventory_xml(self, product_sku_list, quantity):
        submit_data_inventory = '''<?xml version="1.0" encoding="utf-8" ?>
                      <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
                              <Header>
                                <DocumentVersion>1.01</DocumentVersion>
                                <MerchantIdentifier>SellerId</MerchantIdentifier>
                              </Header>
                              <MessageType>Inventory</MessageType>
                              <PurgeAndReplace>false</PurgeAndReplace>
                              inventory_info_placeholder
                      </AmazonEnvelope>'''

        inventory_xml = '''
                   <Message>
                     <MessageID>feed_message_id</MessageID>
                     <OperationType>Update</OperationType>
                     <Inventory>
                       <SKU>product_sku</SKU>
                       <Quantity>product_quantity</Quantity>
                     </Inventory>
                   </Message>
                   '''
        inventory_xml_all = ''
        for product_sku in product_sku_list:
            message_id = self.generate_message_id()
            inventory_xml_tmp = inventory_xml.replace('feed_message_id', str(message_id))
            inventory_xml_tmp = inventory_xml_tmp.replace('product_sku', product_sku)
            inventory_xml_tmp = inventory_xml_tmp.replace('product_quantity', str(quantity))
            inventory_xml_all = inventory_xml_all + inventory_xml_tmp

        submit_data_inventory = submit_data_inventory.replace('SellerId', self.auth_info['SellerId'])
        submit_data_inventory = submit_data_inventory.replace('inventory_info_placeholder', inventory_xml_all)

        return submit_data_inventory

    def get_price_xml(self, sku, standard_price, currency_type='USD', start_date=None, end_date=None, sale_price=None):
        """
         时间格式：2018-02-06T08:00:00+00:00
        """
        submit_data_price = '''<?xml version="1.0" encoding="utf-8" ?>
        <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
           <Header>
             <DocumentVersion>1.01</DocumentVersion>
             <MerchantIdentifier>SellerId</MerchantIdentifier>
           </Header>
           <MessageType>Price</MessageType>
           <Message>
             <MessageID>feed_message_id</MessageID>
               <Price>
                 <SKU>product_sku</SKU>
                 <StandardPrice currency="Currency_type">standard_price</StandardPrice>
                 sale_info_placeholder
           </Price>
          </Message>
        </AmazonEnvelope>'''

        message_id = self.generate_message_id()

        if sale_price is not None and str(sale_price).strip() != '':
            sale_info = ''' 
            <Sale>
               <StartDate>%s</StartDate>
               <EndDate>%s</EndDate>
               <SalePrice currency="Currency_type">%s</SalePrice>
             </Sale>
             ''' %(start_date, end_date, sale_price)
        else:
            sale_info = ''

        submit_data_price = submit_data_price.replace('SellerId', self.auth_info['SellerId'])
        submit_data_price = submit_data_price.replace('feed_message_id', str(message_id))
        submit_data_price = submit_data_price.replace('product_sku', sku)
        submit_data_price = submit_data_price.replace('sale_info_placeholder', sale_info)
        submit_data_price = submit_data_price.replace('Currency_type', currency_type)
        submit_data_price = submit_data_price.replace('standard_price', standard_price)

        return submit_data_price

    def get_price_xml_multi(self, sku_price_list, currency_type='USD'):
        doc = xml.dom.minidom.Document()
        AmazonEnvelope = doc.createElement('AmazonEnvelope')
        AmazonEnvelope.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        AmazonEnvelope.setAttribute('xsi:noNamespaceSchemaLocation', 'amzn-envelope.xsd')
        doc.appendChild(AmazonEnvelope)

        Header = doc.createElement('Header')
        DocumentVersion = doc.createElement('DocumentVersion')
        MerchantIdentifier = doc.createElement('MerchantIdentifier')
        DocumentVersion_text = doc.createTextNode('1.01')
        MerchantIdentifier_text = doc.createTextNode('%s' % self.auth_info['SellerId'])
        DocumentVersion.appendChild(DocumentVersion_text)
        MerchantIdentifier.appendChild(MerchantIdentifier_text)
        Header.appendChild(DocumentVersion)
        Header.appendChild(MerchantIdentifier)
        AmazonEnvelope.appendChild(Header)

        MessageType = doc.createElement('MessageType')
        MessageType_text = doc.createTextNode('Price')
        MessageType.appendChild(MessageType_text)
        AmazonEnvelope.appendChild(MessageType)

        # Message
        for sku_price in sku_price_list:
            for sku, price in sku_price.items():
                time.sleep(0.001)
                timeStamp = int(time.time() * 1000)

                Message = doc.createElement('Message')
                MessageID = doc.createElement('MessageID')
                MessageID_text = doc.createTextNode('%s' % timeStamp)
                MessageID.appendChild(MessageID_text)
                Message.appendChild(MessageID)
                Price = doc.createElement('Price')
                SKU = doc.createElement('SKU')
                SKU_text = doc.createTextNode(sku)
                SKU.appendChild(SKU_text)
                Price.appendChild(SKU)
                StandardPrice = doc.createElement('StandardPrice')
                StandardPrice.setAttribute('currency', currency_type)
                StandardPrice_text = doc.createTextNode(str(price))
                StandardPrice.appendChild(StandardPrice_text)
                Price.appendChild(StandardPrice)
                Message.appendChild(Price)
                AmazonEnvelope.appendChild(Message)

        feed = doc.toxml()
        return feed

    def get_product_xml(self, product_info_dic):
        submit_data_product = '''<?xml version="1.0" encoding="utf-8" ?>
            <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
              <Header>
                <DocumentVersion>1.01</DocumentVersion>
                <MerchantIdentifier>SellerId</MerchantIdentifier>
              </Header>
              <MessageType>Product</MessageType>
              <PurgeAndReplace>false</PurgeAndReplace>
              <Message>
                <MessageID>message_id</MessageID>
                <OperationType>Update</OperationType>
                <Product>
                  <SKU>seller_sku</SKU>
                  <Condition><ConditionType>New</ConditionType></Condition>
                  <DescriptionData>
                          <Title>product_title</Title>
                          <Description>product_description</Description>
                          <BulletPoint>bullet_point1</BulletPoint>
                          <BulletPoint>bullet_point2</BulletPoint>
                          <BulletPoint>bullet_point3</BulletPoint>
                          <BulletPoint>bullet_point4</BulletPoint>
                          <BulletPoint>bullet_point5</BulletPoint>
                          <SearchTerms>generic_keywords1</SearchTerms>
                          <SearchTerms>generic_keywords2</SearchTerms>
                          <SearchTerms>generic_keywords3</SearchTerms>
                          <SearchTerms>generic_keywords4</SearchTerms>
                          <SearchTerms>generic_keywords5</SearchTerms>
                  </DescriptionData>
                    </Product>
              </Message>
             </AmazonEnvelope>'''
        message_id = self.generate_message_id()
        submit_data_product = submit_data_product.replace('SellerId', self.auth_info['SellerId'])
        submit_data_product = submit_data_product.replace('message_id', str(message_id))
        submit_data_product = submit_data_product.replace('seller_sku', product_info_dic['seller_sku'])
        submit_data_product = submit_data_product.replace('product_title', product_info_dic['item_name'])
        submit_data_product = submit_data_product.replace('product_description', product_info_dic['product_description'])
        submit_data_product = submit_data_product.replace('product_title', product_info_dic['item_name'])
        submit_data_product = submit_data_product.replace('bullet_point1', product_info_dic['bullet_point1'])
        submit_data_product = submit_data_product.replace('bullet_point2', product_info_dic['bullet_point2'])
        submit_data_product = submit_data_product.replace('bullet_point3', product_info_dic['bullet_point3'])
        submit_data_product = submit_data_product.replace('bullet_point4', product_info_dic['bullet_point4'])
        submit_data_product = submit_data_product.replace('bullet_point5', product_info_dic['bullet_point5'])
        submit_data_product = submit_data_product.replace('generic_keywords1', product_info_dic['generic_keywords1'])
        submit_data_product = submit_data_product.replace('generic_keywords2', product_info_dic['generic_keywords2'])
        submit_data_product = submit_data_product.replace('generic_keywords3', product_info_dic['generic_keywords3'])
        submit_data_product = submit_data_product.replace('generic_keywords4', product_info_dic['generic_keywords4'])
        submit_data_product = submit_data_product.replace('generic_keywords5', product_info_dic['generic_keywords5'])

        return submit_data_product

    def get_image_xml(self, auth_info_image):
        submit_data_image = '''<?xml version="1.0" encoding="utf-8" ?> 
        <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
            <Header>
              <DocumentVersion>1.01</DocumentVersion> 
              <MerchantIdentifier>SellerId</MerchantIdentifier> 
            </Header>
              <MessageType>ProductImage</MessageType> 
            <Message>
              <MessageID>message_id</MessageID> 
              <OperationType>Update</OperationType> 
                <ProductImage>
                  <SKU>seller_sku</SKU> 
                  <ImageType>Main</ImageType> 
                  <ImageLocation>image_url</ImageLocation> 
              </ProductImage>
            </Message>
        </AmazonEnvelope>'''
        message_id = self.generate_message_id()
        submit_data_image = submit_data_image.replace('SellerId', self.auth_info['SellerId'])
        submit_data_image = submit_data_image.replace('message_id', str(message_id))
        submit_data_image = submit_data_image.replace('seller_sku', self.auth_info['seller_sku'])
        submit_data_image = submit_data_image.replace('image_url', auth_info_image['pic_url'])
        return submit_data_image