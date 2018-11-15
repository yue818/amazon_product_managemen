# -*- coding: utf-8 -*-
import sys
import oss2
import time
import traceback


PREFIX = 'http://'

class find_oss_file():
    def __init__(self):
        pass

    # ossinfo { # ossinfo ={ACCESS_KEY_ID,ACCESS_KEY_SECRET，ENDPOINT，BUCKETNAME_XLS}
    # timerange 时间毫秒值
    # urlload 文件目录
    def findfile(self, ossinfo, urlload):
        try:
            result = {}
            urlDict = {}
            urlList = []
            auth = oss2.Auth(ossinfo['ACCESS_KEY_ID'], ossinfo['ACCESS_KEY_SECRET'])
            bucket = oss2.Bucket(auth, ossinfo['ENDPOINT_OUT'], ossinfo['BUCKETNAME_XLS'])
            for filename in oss2.ObjectIterator(bucket, prefix='%s/'%urlload):
                sourceURL = PREFIX + ossinfo['BUCKETNAME_XLS'] + '.' + ossinfo['ENDPOINT_OUT'] +'/'+ filename.key
                sourceTime = filename.last_modified
                if sourceTime in urlDict.keys():
					#最多保证10个相同时间的路径不覆盖
                    sourceTime += 0.1
                urlDict[sourceTime] = sourceURL
            newurl = sorted(urlDict.items(), key=lambda asd: asd[0], reverse=True)
            for u in newurl:
                urlList.append(u[1])
            result['fileurl'] = urlList
            result['errorcode'] = 0
            return result
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result

