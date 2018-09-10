#-*-coding:utf-8-*-
import oss2
from Project.settings import ACCESS_KEY_ID,ACCESS_KEY_SECRET,PREFIX,ENDPOINT,ENDPOINT_OUT

"""  
 @desc:  
 @author:  
 @site: 
 @software: PyCharm
 @file: upload_to_oss.py
 @time: 2017/12/21 16:39
"""

class upload_to_oss_forthwith():
    def __init__(self, BUCKETNAME):
        self.bucketName = BUCKETNAME
        self.auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(self.auth, ENDPOINT, BUCKETNAME)
        self.bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)


    def upload_to_oss_forthwith(self, params):
        result = {'errorcode':0,'errortext':'','params':params, 'result': ''}

        num = 4
        filelist = []
        for file in oss2.ObjectIterator(self.bucket, prefix='%s' % params['path']):
            filelist.append(file.key)
        length = len(filelist)
        if length > num:
            for key in filelist:
                self.bucket.delete_object(key)
                length = length - 1
                if length == num:
                    break

        self.bucket.put_object(u'%s/%s' % (params['path'],params['name']),params['byte'])
        result['result'] = PREFIX + self.bucketName + '.' + ENDPOINT_OUT + '/' + params['path'] + '/' + params['name']

        return result