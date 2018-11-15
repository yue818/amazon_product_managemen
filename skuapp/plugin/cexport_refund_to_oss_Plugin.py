# coding=utf-8

from xadmin.views import BaseAdminPlugin
from django.template import loader
from brick.function.find_oss_file import *
import oss2

ossinfo = {'ACCESS_KEY_ID': 'LTAIH6IHuMj6Fq2h', 'ACCESS_KEY_SECRET': 'N5eWsbw8qBkMfPREkgF2JnTsDASelM', 'ENDPOINT_OUT': 'oss-cn-shanghai.aliyuncs.com', 'BUCKETNAME_XLS': 'fancyqube-download'}

class cexport_refund_to_oss_Plugin(BaseAdminPlugin):
    cexport_oss = False

    def init_request(self, *args, **kwargs):
        return bool(self.cexport_oss)

    # def get_media(self, media):
    #     media.add_js([self.static('xadmin/js/xadmin.plugin.cexportoss.js')])
    #     return media


    def block_search_cata_nav(self, context, nodes):
        URL = []
        find_oss_file_obj = find_oss_file()
        result = find_oss_file_obj.findfile(ossinfo=ossinfo, urlload='refund')
        if result['errorcode'] == 0:
            URL = result['fileurl']
        nodes.append(loader.render_to_string('cexport_refund_to_oss.html', {'URL': URL[:3]}))

