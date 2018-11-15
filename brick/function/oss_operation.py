# coding=utf-8

"""

OSS文件服务器相关操作：连接OSS，上传文件到OSS

"""
import oss2


PREFIX = 'http://'
ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
# ENDPOINT = 'vpc100-oss-cn-shanghai.aliyuncs.com'
ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'


class oss_operation(object):

    def __init__(self, BUCKETNAME):
        """
        生成bucket连接对象
        """
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME)

    def save_file_to_oss(self, file_obj, now_time, user_name):
        """
        保存文件到OSS上，并返回OSS文件路径
        :param file_obj: 文件对象
        :param now_time: datetime.datetime.now()对象
        :param user_name: 用户姓名拼音
        :return: oss_file_path：OSS文件路径
        """
        filename = user_name + '_' + now_time.strftime('%Y%m%d%H%M%S') + '.xls'

        # 删除现有的
        for object_info in oss2.ObjectIterator(self.bucket, prefix='%s/%s_' % (user_name, user_name)):
            self.bucket.delete_object(object_info.key)

        oss_file_path = user_name + '/' + filename
        self.bucket.put_object('%s/%s' % (user_name, filename),file_obj)

        return oss_file_path









