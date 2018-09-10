# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: prettify.py
 @time: 2018-04-27 14:34
"""  
from bs4 import BeautifulSoup
html_text = ''' 
<?xml version="1.0" ?><AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd"><Header><DocumentVersion>1.01</DocumentVersion><MerchantIdentifier>ARBNA8Y4OL6TV</MerchantIdentifier></Header><MessageType>Product</MessageType><PurgeAndReplace>false</PurgeAndReplace><Message><MessageID>2</MessageID><OperationType>Update</OperationType><Product><SKU>B969W10175</SKU><StandardProductID><Type>UPC</Type><Value>763564206508</Value></StandardProductID><Condition><ConditionType>New</ConditionType></Condition><ItemPackageQuantity>1</ItemPackageQuantity><NumberOfItems>1</NumberOfItems><DescriptionData><Title>Bohonan art_test333</Title><Brand>Bohonan</Brand><Description>&lt;p&gt;1&lt;br /&gt;\r\n&lt;/p&gt;</Description><BulletPoint>1</BulletPoint><BulletPoint>1</BulletPoint><BulletPoint>1</BulletPoint><BulletPoint>1</BulletPoint><BulletPoint>1</BulletPoint><ItemDimensions><Length unitOfMeasure='CM'>1</Length><Width unitOfMeasure='CM'>1</Width><Height unitOfMeasure='CM'>1</Height></ItemDimensions><Manufacturer>Bohonan</Manufacturer><MfrPartNumber>B969W10175</MfrPartNumber><SearchTerms>1</SearchTerms><SearchTerms>1</SearchTerms><SearchTerms>1</SearchTerms><SearchTerms>1</SearchTerms><SearchTerms>1</SearchTerms><ItemType>pet-toys</ItemType><TargetAudience>boys</TargetAudience><TargetAudience>girls</TargetAudience><TargetAudience>unisex-children</TargetAudience><RecommendedBrowseNode>2975540011</RecommendedBrowseNode><MerchantShippingGroupName>Migrated Template</MerchantShippingGroupName></DescriptionData><ProductData><Arts><ProductType><FineArt><ArtworkType>11</ArtworkType><Artist>van gogh</Artist><ArtistBiography>12</ArtistBiography><ArtworkMedium>13</ArtworkMedium><Date>1960-05-17T09:00:00</Date><FrameMaterial>9</FrameMaterial><Framed>true</Framed><FramedHeight unitOfMeasure='CM'>10</FramedHeight><FramedWidth unitOfMeasure='CM'>10</FramedWidth><FramedDepth unitOfMeasure='CM'>5</FramedDepth><SaleType>14</SaleType></FineArt></ProductType></Arts></ProductData></Product></Message></AmazonEnvelope>
'''
soup = BeautifulSoup(html_text, 'lxml')

print soup.prettify()

