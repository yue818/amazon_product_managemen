# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: delete_old_api_file.py
 @time: 2018-05-02 9:48
"""  
import oss2
ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
BUCKETNAME_APIVERSION = 'fancyqube-apiversion'


auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_APIVERSION)
bucket.delete_object('amazon_upload_product-20180414b.exe')