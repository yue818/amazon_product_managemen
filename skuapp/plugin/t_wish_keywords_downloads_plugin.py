# -*- coding: utf-8 -*-
import oss2
from Project.settings import *
from django.template import loader
from xadmin.views import BaseAdminPlugin

class t_wish_keywords_downloads_plugin(BaseAdminPlugin):
    wish_key_words = False
    # 初始化方法根据 ``say_hello`` 属性值返回
    def init_request(self, *args, **kwargs):
        return bool(self.wish_key_words)

    def block_results_top(self, context, nodes):
        downloadfiles = []
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT_OUT,BUCKETNAME_XLS)
        if self.model._meta.model_name == 't_wish_keywords':
            for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%('wishkeywords',context['user'])):
                downloadfiles.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,object_info.key))
        elif self.model._meta.model_name == 't_online_info_ebay_listing':
            for object_info in oss2.ObjectIterator(bucket, prefix='%s/%s_' % ('ebay_excel', context['user'])):
                downloadfiles.append('%s%s.%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, object_info.key))
        nodes.append(loader.render_to_string('downloadxls.html', {'downloadfiles': downloadfiles}))




