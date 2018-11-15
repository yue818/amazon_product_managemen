#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_image_Admin.py
 @time: 2018-05-09 17:33
"""
from django.utils.safestring import mark_safe
from Project.settings import *

class t_tort_info_image_Admin(object):

    t_tort_tree_menu_flag = True

    def show_image(self, obj):
        detail = obj.detail.split(':')
        rt = ''
        for dl in detail:
            try:
                d = dl.split(';')

                url = u'%s%s.%s/%s/%s/%s' % (PREFIX, BUCKETNAME_TORT, ENDPOINT_OUT, 'aliexpress', d[0], str(d[3]))
                id_ = d[0]
                alt = u'%s,%s'%(d[1], d[2])
                title = 'Site:%s,MainSKU:%s'%(d[1], d[2])

                rt = u'%s<img id="img_%s", src="%s" width="120" height="120" alt = "%s"  title="%s"  />' \
                     u'<style>img{cursor: pointer; transition: all 0.8s;} ' \
                     u'img:hover{transform: scale(2);}</style>  ' \
                     u"<script>$('#img_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
                     u"title:'侵权相关信息',fix:false,shadeClose: true,maxmin:true,area:['800px','300px']," \
                     u"content:'/t_tort_info_image_info/?ID=%s',});});</script>"% (rt, id_, url, alt, title, id_, id_)
            except:
                pass

        return mark_safe(rt)

    show_image.short_description = u'<span style="color:#428bca;text-align:center">侵权产品图片列表</span>'

    list_display = ('show_image',)
    list_display_links = ('ID')
    list_per_page = 100