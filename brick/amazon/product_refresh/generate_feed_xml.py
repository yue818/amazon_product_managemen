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
            time.sleep(0.001)
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
        """<?xml version="1.0" encoding="utf-8" ?>
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
                     </AmazonEnvelope>
        """
        doc = xml.dom.minidom.Document()

        # AmazonEnvelope
        amazon_envelope = doc.createElement('AmazonEnvelope')
        amazon_envelope.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        amazon_envelope.setAttribute('xsi:noNamespaceSchemaLocation', 'amzn-envelope.xsd')

        # Header
        header = doc.createElement('Header')
        # <DocumentVersion>1.01</DocumentVersion>
        document_version = doc.createElement('DocumentVersion')
        document_version_text = doc.createTextNode('1.01')
        document_version.appendChild(document_version_text)
        # <MerchantIdentifier>SellerId</MerchantIdentifier>
        merchant_identifier = doc.createElement('MerchantIdentifier')
        merchant_identifier_text = doc.createTextNode('%s' % self.auth_info['SellerId'])
        merchant_identifier.appendChild(merchant_identifier_text)
        header.appendChild(document_version)
        header.appendChild(merchant_identifier)

        # MessageType: <MessageType>Product</MessageType>
        message_type = doc.createElement('MessageType')
        message_type_text = doc.createTextNode('Product')
        message_type.appendChild(message_type_text)

        # PurgeAndReplace:
        purge_and_replace = doc.createElement('PurgeAndReplace')
        purge_and_replace_text = doc.createTextNode('false')
        purge_and_replace.appendChild(purge_and_replace_text)

        # Message
        message = doc.createElement('Message')
        message_id = doc.createElement('MessageID')
        message_id_text = doc.createTextNode('%s' % str(self.generate_message_id()))
        message_id.appendChild(message_id_text)
        message.appendChild(message_id)

        # OperationType: 部分修改
        operation_type = doc.createElement('OperationType')
        operation_type_text = doc.createTextNode('PartialUpdate')
        operation_type.appendChild(operation_type_text)
        message.appendChild(operation_type)

        product = doc.createElement('Product')
        message.appendChild(product)
        # SKU
        sku = doc.createElement('SKU')
        sku_text = doc.createTextNode(self.auth_info['seller_sku'])
        sku.appendChild(sku_text)
        product.appendChild(sku)

        # DescriptionData
        description_data = doc.createElement('DescriptionData')
        product.appendChild(description_data)
        title = doc.createElement('Title')
        title_text = doc.createTextNode(product_info_dic['item_name'])
        title.appendChild(title_text)
        description_data.appendChild(title)

        if product_info_dic.get('item_description', '').strip():
            description = doc.createElement('Description')
            description_text = doc.createTextNode(product_info_dic['item_description'])
            description.appendChild(description_text)
            description_data.appendChild(description)

        if product_info_dic.get('bullet_point1', '').strip():
            bullet_point1 = doc.createElement('BulletPoint')
            bullet_point1_text = doc.createTextNode(product_info_dic['bullet_point1'])
            bullet_point1.appendChild(bullet_point1_text)
            description_data.appendChild(bullet_point1)

        if product_info_dic.get('bullet_point2', '').strip():
            bullet_point2 = doc.createElement('BulletPoint')
            bullet_point2_text = doc.createTextNode(product_info_dic['bullet_point2'])
            bullet_point2.appendChild(bullet_point2_text)
            description_data.appendChild(bullet_point2)

        if product_info_dic.get('bullet_point3', '').strip():
            bullet_point3 = doc.createElement('BulletPoint')
            bullet_point3_text = doc.createTextNode(product_info_dic['bullet_point3'])
            bullet_point3.appendChild(bullet_point3_text)
            description_data.appendChild(bullet_point3)

        if product_info_dic.get('bullet_point4', '').strip():
            bullet_point4 = doc.createElement('BulletPoint')
            bullet_point4_text = doc.createTextNode(product_info_dic['bullet_point4'])
            bullet_point4.appendChild(bullet_point4_text)
            description_data.appendChild(bullet_point4)

        if product_info_dic.get('bullet_point5', '').strip():
            bullet_point5 = doc.createElement('BulletPoint')
            bullet_point5_text = doc.createTextNode(product_info_dic['bullet_point5'])
            bullet_point5.appendChild(bullet_point5_text)
            description_data.appendChild(bullet_point5)

        if product_info_dic.get('generic_keywords1', '').strip():
            generic_keyword = product_info_dic['generic_keywords1']
            if len(generic_keyword) >= 199:
                key_word1 = generic_keyword[0:130]
                key_word2 = generic_keyword[130:]
                if ' ' in key_word2:
                    keyword_temp = key_word2.split(' ')[0]
                    if keyword_temp:
                        key_word1 += keyword_temp
                        key_word2 = key_word2[len(keyword_temp) + 1:]
                    else:
                        key_word2 = key_word2[1:]
            else:
                key_word1 = generic_keyword
                key_word2 = None

            if key_word1:
                search_terms1 = doc.createElement('SearchTerms')
                search_terms1_text = doc.createTextNode(key_word1)
                search_terms1.appendChild(search_terms1_text)
                description_data.appendChild(search_terms1)

            if key_word2:
                search_terms2 = doc.createElement('SearchTerms')
                search_terms2_text = doc.createTextNode(key_word2)
                search_terms2.appendChild(search_terms2_text)
                description_data.appendChild(search_terms2)

        doc.appendChild(amazon_envelope)
        amazon_envelope.appendChild(header)
        amazon_envelope.appendChild(message_type)
        amazon_envelope.appendChild(purge_and_replace)
        amazon_envelope.appendChild(message)

        feed_xml = doc.toxml()
        return feed_xml

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