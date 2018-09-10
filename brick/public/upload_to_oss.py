# -*-coding:utf-8-*-

import oss2
from Project.settings import ACCESS_KEY_ID, ACCESS_KEY_SECRET, PREFIX, ENDPOINT, ENDPOINT_OUT

"""
 @desc:
 @author: yewangping
 @site:
 @software: PyCharm
 @file: upload_to_oss.py
 @time: 2017/12/21 16:39
"""


class upload_to_oss():
    def __init__(self, BUCKETNAME):
        self.bucketName = BUCKETNAME
        self.auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(self.auth, ENDPOINT, BUCKETNAME)
        # self.bucket = oss2.Bucket(self.auth, ENDPOINT_OUT, BUCKETNAME)
        self.bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)

    def upload_to_oss(self, params):
        result = {'errorcode': 0, 'errortext': '', 'params': params, 'result': ''}
        try:
            if params['del'] == 0:
                for object_info in oss2.ObjectIterator(self.bucket, prefix='%s' % params['path']):
                    self.bucket.delete_object(object_info.key)
            self.bucket.put_object(u'%s/%s' % (params['path'], params['name']), params['byte'])
            result['result'] = PREFIX + self.bucketName + '.' + ENDPOINT_OUT + '/' + params['path'] + '/' + params['name']
        except Exception, ex:
            result['errorcode'] = 1
            result['errortext'] = '%s:%s' % (Exception, ex)
        return result


class get_obj_from_oss():
    def __init__(self, BUCKETNAME):
        self.bucketName = BUCKETNAME
        self.auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(self.auth, ENDPOINT, BUCKETNAME)
        # self.bucket = oss2.Bucket(self.auth, ENDPOINT_OUT, BUCKETNAME)
        self.bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)

    def get_obj_from_oss(self, params):
        result = {'errorcode': 0, 'errortext': '', 'params': params, 'result': ''}
        try:
            for object_info in oss2.ObjectIterator(self.bucket, prefix='%s' % params['path']):
                print 'object_info.key: ', object_info.key
                print "params['name']", params['name']
                if object_info.key == (params['path'] + '/' + params['name']):
                    res_file = self.bucket.get_object(object_info.key)
                    result['result'] = res_file
        except Exception, ex:
            result['errorcode'] = 1
            result['errortext'] = '%s:%s' % (Exception, ex)
        return result
