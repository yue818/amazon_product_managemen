# -*- coding: utf-8 -*-
import oss2
from Project.settings import *
from django.template import loader
import xadmin

from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
class t_product_downloadxls_Plugin(BaseAdminPlugin):
    downloadxls = False
    # 初始化方法根据 ``say_hello`` 属性值返回
    def init_request(self, *args, **kwargs):
        return bool(self.downloadxls)

    def block_results_top(self, context, nodes):
        #logger = logging.getLogger('sourceDns.webdns.views')
        #logger.error("context[user]=%s context=============%s nodes=%s"%(context['user'], context,nodes))

        downloadfiles = []
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(context['user'],context['user'])):
            downloadfiles.append('%s%s.%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,object_info.key))
        downloadfiles.reverse()
        nodes.append(loader.render_to_string('downloadxls.html', {'downloadfiles': downloadfiles}))




