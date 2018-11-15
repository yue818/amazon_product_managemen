# coding=utf-8


from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging
logger = logging.getLogger('sourceDns.webdns.views')
from django.contrib import messages


class py_searchPlugin(BaseAdminPlugin):
    py_search_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.py_search_flag)

    def block_search_cata_nav(self, context, nodes):
        request = self.request
        GET = request.GET
        queryDict = {}
        queryDict['SKU'] = GET.get('sku', '')
        queryDict['GoodsName'] = GET.get('name', '')
        GoodsStatus = GET.get('state', '')
        Cate1 = GET.get('cate1', '0')
        Cate2 = GET.get('cate2', '0')

        category = {'0|1|':u'时尚男装', '0|2|':u'时尚女装', '0|7|':u'深圳3C电子产品',
                    '0|9|':u'时尚包包', '0|13|':u'饰品&手表', '0|17|':u'时尚鞋', '0|18|':u'海外仓产品',
                    '0|19|':u'广州电子产品', '0|23|':u'婚庆用品', '0|24|':u'家居', '0|25|':u'儿童用品',
                    '0|27|':u'服装配饰', '0|28|':u'健康美容', '0|29|':u'玩具', '0|30|':u'其他',
                    '0|33|':u'户外用品', '0|34|':u'办公文教用品', '0|44|':u'DIY工具', '0|45|':u'汽配',
                    '0|50|':u'杂货', '0|68|':u'浦江3C', '0|102|':u'工业', '0|103|':u'媒体',
                    '0|110|':u'动漫及电影周边', '0|111|':u'违禁品', '0|116|':u'圣诞礼品', '0|117|':u'创意产品，侵权',
                    '0|122|':u'乐器及配件', '0|123|':u'已删除', '0|124|':u'舞会派对'}

        dict1 = { u'在售':{'name':u'在售'}, u'正常':{'name':u'正常'}, u'清仓':{'name':u'清仓'},
                  u'组合':{'name':u'组合'}, u'临时下架':{'name':u'临时下架'},u'售完下架': {'name': u'售完下架'},
                  u'处理库尾':{'name':u'处理库尾'}, u'暂停销售':{'name':u'暂停销售'}, u'自动创建':{'name':u'自动创建'} }

        stateList = [u'在售', u'正常', u'清仓', u'组合', u'临时下架', u'售完下架', u'处理库尾',
                     u'暂停销售', u'自动创建']
        for each in stateList:
            if each in GoodsStatus:
                dict1[each]['state'] = 'checked'
            else:
                dict1[each]['state'] = ''

        selectDict = {}
        selectDict['cate1'] = Cate1
        selectDict['cate2'] = Cate2
        if Cate1 == '0':
            selectDict['text1'] = '全部分类'
        else:
            selectDict['text1'] = category[Cate1]
        if Cate2 == '0':
            selectDict['text2'] = '全部'
        else:
            selectDict['text2'] = ''

        nodes.append(loader.render_to_string('py_search.html',{'query':queryDict, 'stateDict':dict1,
                                                               'category':category,'choice':selectDict} ,
                                             context_instance=RequestContext(self.request)))
