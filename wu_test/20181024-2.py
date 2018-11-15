# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: 20181024-2.py
 @time: 2018/10/24 17:09
"""  
message_txt = '''
<Message>
    <MessageID>message_id</MessageID>
    <OperationType>Delete</OperationType>
    <Product>
      <SKU>seller_sku</SKU>
    </Product>
  </Message>
'''

seller_sku_list = ['99#7638:3808','99#7638:3807','99#7638:3806','99#7638:3805','99#7638:3803','99#7638:3804','99#7638:3834']

message_text_all = ''

for id, val in enumerate(seller_sku_list):
    message_text_all = message_text_all + message_txt.replace('message_id', str(id+1)).replace('seller_sku', val)

print message_text_all


for i in {1:1}, {2:2}:
    print i