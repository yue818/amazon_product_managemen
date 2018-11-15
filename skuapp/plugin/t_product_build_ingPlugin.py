# -*- coding: utf-8 -*-


import xadmin

from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from skuapp.table.B_PackInfo import  *
from skuapp.table.t_product_mainsku_sku  import *

class t_product_build_ingPlugin(BaseAdminPlugin):
    say_hello = False
    object_id = 0
    # 初始化方法根据 ``say_hello`` 属性值返回
    def init_request(self, *args, **kwargs):
        return bool(self.say_hello)
    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.t_product_mainsku_sku.html.js')])
        return media
    def block_after_fieldsets(self, context, nodes):
        #logger = logging.getLogger('sourceDns.webdns.views')
        #logger.error(" context=%s nodes=%s"%(context,nodes))

        #logger.error("original.Name=%s original=%s opts= %s object_id =%s context=%s nodes=%s"%(context['original'].Name,context['original'],context['opts'],context['object_id'],context,nodes))


        #大类信息

        #包装规格
        B_PackInfos =u'请选择包装规格'
        PackNID = 0
        try:
            if context['original']  is  not None :
                B_PackInfo_obj = B_PackInfo.objects.get(id__exact=context['original'].PackNID)
                PackNID   = B_PackInfo_obj.id
                B_PackInfos = u'NID=%s  规格=%s 价格(¥元)=%s 重量(g)=%s'%(B_PackInfo_obj.id,B_PackInfo_obj.PackName,B_PackInfo_obj.CostPrice,B_PackInfo_obj.Weight)
        except:
            pass

        packings = B_PackInfo.objects.all().order_by('PackName')
        nodes.append(loader.render_to_string('packing.html', {'packings': packings ,'B_PackInfos':B_PackInfos,'PackNID':PackNID}))

        #加载子SKU信息
        t_product_mainsku_sku_objs = None
        t_product_mainsku_sku_objs_count =0
        if context['original']  is  not None :
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=context['object_id']).order_by('SKU')
            t_product_mainsku_sku_objs_count = t_product_mainsku_sku_objs.count()
        nodes.append(loader.render_to_string('t_product_mainsku_sku.html', {'t_product_mainsku_sku_objs': t_product_mainsku_sku_objs,'t_product_mainsku_sku_objs_count': t_product_mainsku_sku_objs_count}))


    #def block_before_fieldsets(self, context, nodes):
        #logger = logging.getLogger('sourceDns.webdns.views')
        #logger.error("original.Name=%s original=%s opts= %s object_id =%s context=%s nodes=%s"%(context['original'].Name,context['original'],context['opts'],context['object_id'],context,nodes))

        #return  "<div class='info'>Hello xaaaaaaaaaaaa</div>"

