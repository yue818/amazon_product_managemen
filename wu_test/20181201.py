import json
import datetime
import chardet

body = '{"AWSAccessKeyId": "AKIAIN6U324UAKUYAE6A", "ShopName": "AMZ-0156-BW-US/PJ", "IP": "123.207.173.162", "feed_xml": "<?xml version=\\"1.0\\" ?><AmazonEnvelope xmlns:xsi=\\"http://www.w3.org/2001/XMLSchema-instance\\" xsi:noNamespaceSchemaLocation=\\"amzn-envelope.xsd\\"><Header><DocumentVersion>1.01</DocumentVersion><MerchantIdentifier>A3920THQ6R6GRF</MerchantIdentifier></Header><MessageType>Product</MessageType><PurgeAndReplace>false</PurgeAndReplace><Message><MessageID>1543659786540</MessageID><OperationType>PartialUpdate</OperationType><Product><SKU>ZNOC4VXYQ5469*6</SKU><DescriptionData><Title>Firtink 6 Pack Hooks Hanger Stainless Steel Hook Organizer Self Adhesive Multi-purpose Tool of Storage for Towel Robe Kitchen Bathroom Accessories(Thick double hook)</Title><Description>&lt;p&gt;&lt;b&gt;Use Tips:&lt;/b&gt;&lt;br /&gt;&lt;br /&gt; 1. Please clean the wall and keep it dry before installation.&lt;br /&gt; 2. Please wait for 24 hours before hanging the items for better effect.&lt;br /&gt;&lt;br /&gt;&lt;b&gt;Satisfaction Guarantee:&lt;/b&gt;&lt;br /&gt;&lt;br /&gt; If you have any doubts about the product, please contact us and we will reply you at the first time. If for any reason you\xe2\x80\x99re unhappy with your purchase, we will refund your money or provide you with a new product.&lt;br /&gt;&lt;br /&gt;&lt;/p&gt;</Description></DescriptionData></Product></Message></AmazonEnvelope>", "seller_sku": "ZNOC4VXYQ5469*6", "SecretKey": "38h63HY0Odcamjf9VlrSekxyrZZ12xmigLKcNHwt", "table_name": "t_online_info_amazon", "ShopSite": "US", "product_info_dic": {"item_name": "Firtink 6 Pack Hooks Hanger Stainless Steel Hook Organizer Self Adhesive Multi-purpose Tool of Storage for Towel Robe Kitchen Bathroom Accessories(Thick double hook)", "item_description": "<p><b>Use Tips:</b><br /><br /> 1. Please clean the wall and keep it dry before installation.<br /> 2. Please wait for 24 hours before hanging the items for better effect.<br /><br /><b>Satisfaction Guarantee:</b><br /><br /> If you have any doubts about the product, please contact us and we will reply you at the first time. If for any reason you\xe2\x80\x99re unhappy with your purchase, we will refund your money or provide you with a new product.<br /><br /></p>"}, "ShopIP": "123.207.173.162", "SellerId": "A3920THQ6R6GRF", "update_type": "product_info_modify", "MarketplaceId": "ATVPDKIKX0DER"}'



data = body.split('||')

auth_info = json.loads(data[0], encoding='utf-8')
# print  auth_info['product_info_dic']

if auth_info['update_type'] == 'product_info_modify':
            set_sql = ''.encode('utf-8')
            for key, val in auth_info['product_info_dic'].items():
                set_sql += key + '="' + val + '",'

            sql = "update %s set %s deal_result = 'Success',  updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                  % (auth_info['table_name'], set_sql, datetime.datetime.now(), auth_info['ShopName'], auth_info['seller_sku'])
            print 'sql is:%s' % sql