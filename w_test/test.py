# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: test.py
 @time: 2018-04-29 10:36
"""

#
# def get_prime():
#     for n in range(2, 10):
#         print 'inside n:', n
#         for x in range(2, n):
#             # print 'x now is:', x
#             print 'break:', n
#             if n % x == 0:
#                 print n, 'equals', x, '*', n/x
#                 break
#         else:
#             print 'else:', n
#             print
#             print n, 'is a prime number'
#     else:
#         print 'outside n:', n
#
#
# def fib(n):
#     print n
#     a, b = 0, 1
#     while b < n:
#         a, b = b, a+b
#         print b
#
# fib(10)

#
# def f(a, list_arg=[]):
#     print type(a)
#     list_arg.append(a)
#     print list_arg
#
#
# f(1)
# f('c')

# templist = "XMA0519WT,XMA0519RD,,XMA0519PK,XMA0519RD".replace('\n','').replace('\r','').replace('\r\n','').split(',')
# print templist
# temp_list = [temp for temp in templist if temp]
# print temp_list
#
# temp_set = set(temp_list)
# print temp_set

# lambor_tools = dict()
# for key, val in lambor_tools.items():
#     print key, val
#
# import re
# p = re.compile('abc*')

# import pymysql as MySQLdb
# DATABASES = dict()
#
#
# def retry_conn_mysql(self, db_conn, count):
#     if count > 3:
#         return db_conn
#     count += 1
#
#     try:
#         db_conn.ping()
#     except:
#         try:
#             db_conn = MySQLdb.connect(DATABASES['HOST'],
#                                       DATABASES['USER'],
#                                       DATABASES['PASSWORD'],
#                                       DATABASES['NAME'],
#                                       charset="utf8")
#             print 'reConnect mysql db success!!!!'
#             return db_conn
#         except Exception as e:
#             error = 'reConnect mysql db error %s' % e
#             print error
#             self.retry_conn_mysql(db_conn, count)


# def getskueach(db_conn, shopsku):
#     skusor = db_conn.cursor()
#     skusor.execute("select SKU from py_db.b_goodsskulinkshop WHERE ShopSKU = %s ;", (shopsku,))
#     obj = skusor.fetchone()
#     if obj:
#         sku = obj[0]
#     else:
#         skusor.execute("select SKU from py_db.b_goods WHERE SKU = %s ;", (shopsku,))
#         skuobj = skusor.fetchone()
#         if skuobj:
#             sku = skuobj[0]
#     skusor.close()
#     return sku
#
#
# def getSKU(shopsku):
#     if shopsku:
#         shopsku = shopsku.strip()
#     sku = None
#     skulist = []
#     for shopskutmp in shopsku.split('+'):
#         newshopsku = shopskutmp.split('*')[0].split('\\')[0]
#         sku = getskueach(db_conn, newshopsku.strip())
#         if sku:
#             skulist.append(sku)
#     if skulist:
#         sku = '+'.join(skulist)
#     return sku

# import time
# import datetime
#
# start = datetime.datetime.now()
#
# end = datetime.datetime.now()
#
#
# time_diff =  (end - start).seconds
# print time_diff
# print type(time_diff)

import zlib
# s = '''1111111111111111111111111111111111111111111111'''
# zlib_s = zlib.compress(s)
#
# zlib_s='�34$  ��'
# print zlib_s
# # zlib_s = '''eJztWG1v2zYQ/j5g/4EzhqEfYsvvdTxVhVNnqZs69SKnaTcMAS2dLS4SKZBUbafbf9+R8ovk5qUbtm8DEli6O949d7w7HvW5om6zSp9U/Mm02ex0LitHpKIg
# # jkHeIOcmZkoj+9fKzbNn333/ud973utWfkOZwbU/CAJQ6hzWo9BoGJyPBqNJZ9r68PF0ej24fv16ODDa/EikFzQBKzP+pVqvd5rVExEJTnn1yncmb4wUTeid
# # 4DdZGgsa3jCjsdepHyNnNDErG41erXdca7RbtUanblZ8opJRzQRHdt3YgUCCRjhGfBx+fHPSm6aD0zenjL3zF710efbhYvXq9PlVlH7s/RIlx2+zaGkUZWkw
# # ChWu+vznF0AkqCzWJTy+jc7G58uTi0HvY/vd2+70vdE1pvIWdBrTADYS0/eT4fno/EN9eHpZ+fOPP9yXqyQmn0AqhP6i0qjVK+Sl5w6s2VP+CWKRAkEZrvor
# # xV5UIq3TvuMsl8vaslUTcuE06/WG82H81g8iSGiVcaUpD6BCUL7PhQm2ShFBzn8rAhumF+jaHa/CxkRtpcKK574GGoL03KEIsgS4fp8D8xBXw3UOqe4YZBBR
# # rkchUtmc4dJSDFznHgnX2VoZY8LQBUzXKXgTKcIs0GbFnuhOMrmAAQ8vwQbRm9NYgesckreadg+jodfotJqtNiZou11v7tQiw32XgrQxsDau0pBq1Fmmuhs8
# # nuufX3mFdHcdQ3B9jHFIZbgRM2pzbZNXrpNreE/jDLzn3Van2261Os02rs1pqOPL5a8ED5m2Yd09WkUXsHSdMqnw7rkjDcmEBrfo3c8ZhprptYebdR/ZvciS
# # Gch3c8NURqpMcIegAslSo3hINUWnmI7B29Qn6RKjkZzQMGFcC078KNMoEIjgVpGLdYykPfOExjF5zRYR8VOAsMhhMmSgrIQiS6YjciaBaoJxmbEYoRKMDxlm
# # cvs6FzLXN5WUccYX5HSFqcUUkLN1Qn5imuMGkzNMdoy/Be2eSFSyxe46+WvRRe+HWP+Y/rDQP5oHpaXgC/P2E0LJsNb7huzs6eZ1Joljnr/9hpBTrFuyAE00
# # k+ifmJNYKINNFcMijNQcsCTVEUHnpRBzLVJkSJJxLAQyy1QE6iU51D+NmCIK9QcCaziPU5fIPOlNISIjFsZ0yaAW5BYgJToCMtvFfIGhQXlMBJ4ZjPAJOGFz
# # kjJAZIRKMOi1QbUUkhOR6dq9gPCPWlTob4LtkFkQam+qRsZY34adSkhYlhAErFCOJFhp2KbjI4utBNrYXxp2auJzRGLMG02WYH9MMqRCYnLEcERCkxYx2JzA
# # jFsQqx1/MwW1gyBOI1jnuoUJ9TyLy2YLwVRW4T5gsdk4VSN+xvTOHuOhwB8DCANkn1HBGq3bYDm7bLonrbAKAmyBef99Mrmq5JWJa5+MdzH+Yj+qGOk8on0y
# # yWN8j4zP7qBPBilGdlXDBFrZ/+ckSA6Eq+TaxrtPOt3Fk+5smgsZ8SDOQgifcqg7CVS5YRQl8HQpFKZ7kuGxqicCt8L72g3AEi+sKqnYYmU5VtJNEYtJ0E1i
# # 7nP3ESXX/zSFHtF5WCnbCsmLfWGboio1xXDXFJ+ohEes+qaYjNy+JRdcIgG2+hkYJWHukEAs0gxUNnUtDGxJKWh7BB1aGlOezWlgWqjct98S1R3P5YRKnR8/
# # 5fO1zHJ9oDhCTEHi+fQvHzxFn9eCw6q8saWXuNxlCQUpcN95qY3hwV5AW4JeXHuoa45xjfAcuDU9+a7Emt23QWqDVqpSKmJTxtnvUDSGQ0ezCB4B+rTxveuY
# # ARDQkvrfGeV37Gt84HbXFkLgGb6NQEnggXWbsn/EhQcWbo8Uk96liGQHW/+QZbNva5YcSD8CxGzQA7pu2e1MlIwiJUtLlCj+GlSb2B3AMAOdnRV3q6rFVfl8
# # mA+TU4rTtB5kWBk4pHgzsUb2AfFQaMFk/LRUxnFAW1WDiMWhBP6l/CWiSbBz4vFxIsVSwYUIwWu1G8edY5xO72fvrh1+xNIU29iZFJm9VHpjtsAhHrdpCgmm
# # qJnrHxYuHTn5uLuZx/MX2yXVjmiDte2cZ0KE6H+R5eZXwWsqcdDU6+JxNomBYpbbqYxpbPZ445Lx2mzZQ0uQtzHvlEA5u4uJs7v0OOXrovf/tXJ3gxwhEEx+
# # uf4PLpaddr399y+WO0QPXS13t7VO3XX2VzensPD/rf+qLwosgP9g27vteveffE9gRvFTXxNQiASZxGYZrF9UrvxhxWvWmsfFLwZWj7P9fTAT/gLNyA64'''
# print type(zlib_s)
# # print zlib_s
# # print len(s)
# # print len(zlib_s)
# ss = zlib.decompress(zlib_s)
# print ss
#
# import time
#
#
# while 1:
#     print  int(time.time() * 1000)
#     time.sleep(0.001)
#
#
# ll = '''Contenu: 1 collier de sirène
#
# Les dimensions sont les suivantes:
#
# H01-premier couche 30cm, deuxième couche 35cm, chaîne d'extension 7cm
#
# H02-Pendentif est d'environ 1.7 * 2.3cm, la longueur de la chaîne est de 45 + 5cm
#
# H03-pendentif est d'environ 5 * 6cm, longueur de la chaîne est de 47 + 6cm
#
# H04-pendentif environ 4 * 4cm chaîne longueur 47 cm + 5cm
#
# H05-premier couche 40cm, deuxième couche 50cm, chaîne d'extension 5cm
#
# H06-pendentif: écaille de poisson 1.2 * 1.2cm queue de poisson 1.7 * 1.6cm chaîne longueur 45cm
#
# Conception:
#
# H01-Velours coréen créatif multi-couche queue de sirène court collier
#
# H02-Ouvert Mermaid Luminous Pendentif Collier
#
# H03-Retro Silver Beach Bohemian sirène queue pendentif collier
#
# H04-Multicolore paillettes sirène queue de poisson collier
#
# H05-Double Mermaid Fishtail Collier en cristal violet
#
# H06-Double couche de sirène écailles de poisson / collier pendentif en queue de poisson
#
# Soins des bijoux:
#
# 1. Les bijoux sont souvent remplacés, tous les accessoires doivent être enlevés avant de se baigner ou de nager
#
# 2. Placer dans un petit bijoux séparé de boîte à bijoux pour éviter de se frotter l'un contre l'autre
#
# 3. Nettoyez les bijoux de temps en temps, utilisez une brosse fine et douce pour essuyer la surface des bijoux, de sorte que les bijoux enlève les taches de surface
# '''
# print len(ll)

import xml.dom.minidom
import time


def get_price_xml_multi(sku_price_list, currency_type='USD'):
    doc = xml.dom.minidom.Document()
    AmazonEnvelope = doc.createElement('AmazonEnvelope')
    AmazonEnvelope.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
    AmazonEnvelope.setAttribute('xsi:noNamespaceSchemaLocation', 'amzn-envelope.xsd')
    doc.appendChild(AmazonEnvelope)

    Header = doc.createElement('Header')
    DocumentVersion = doc.createElement('DocumentVersion')
    MerchantIdentifier = doc.createElement('MerchantIdentifier')
    DocumentVersion_text = doc.createTextNode('1.01')
    MerchantIdentifier_text = doc.createTextNode('%s' % 'SellerId')
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

sku_price_list =[{u'_((!${:10075': 10.32}]
feed = get_price_xml_multi(sku_price_list, 'USD')
print feed


