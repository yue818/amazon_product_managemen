# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.contrib import messages
from skuapp.table.t_config_apiurl_asin_cf import *
from urllib import urlencode
from datetime import datetime


class t_config_apiurl_asin_cf_Admin(object):
    list_per_page = 50

    def show_SmallImage(self, obj):
        url = u'%s' % (obj.SmallImage)
        rt = '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  ' % (url, url, url)
        return mark_safe(rt)

    show_SmallImage.short_description = u'图片'

    def show_asin_urls(self, obj):
        rt = ''
        asin_objs = t_config_apiurl_asin_cf.objects.filter(id=obj.id)
        for asin_obj in asin_objs:
            rt_url = u'https://www.amazon.com/dp/%s' % asin_obj.ASIN
            rt = u'%s<a href="%s"target="_blank">%s</a>' % (rt, rt_url, asin_obj.ASIN)
        return mark_safe(rt)

    show_asin_urls.short_description = u'ASIN'

    def show_ranklist(self, obj):

        t_config_apiurl_asin_cf_objs = t_config_apiurl_asin_cf.objects.filter(ASIN=obj.ASIN)
        if t_config_apiurl_asin_cf_objs[0].Rank is not None and t_config_apiurl_asin_cf_objs[0].Rank.strip() != '':
            rt_tr = '<table  style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">类目</th>'
            tt = ''
            rank = ''
            Rank_objs = t_config_apiurl_asin_cf_objs[0].Rank
            Rank_dict = eval(Rank_objs)
            a = 0
            for Rank_k, Rank_v in Rank_dict.iteritems():
                rt_tr_k_obj = '<td>%s</td>' % Rank_k
                t = 0
                Rank_v_obj = ''
                for Rank in Rank_v:
                    t = t + 1
                    Rank_v_obj = '%s<td>%s</td>' % (Rank_v_obj, Rank)
                rank = '<tr bgcolor="#FFFFFF">%s%s</tr>%s' % (rt_tr_k_obj, Rank_v_obj, rank)
                a = t
            i = 0
            while i < a:
                i = i + 1
                tt = '%s<th style="text-align:center">->Rank%d</th>' % (tt, i)
            title = '%s%s</tr>' % (rt_tr, tt)
            ii = '%s%s</table>' % (title, rank)
        else:
            ii = ''
        return mark_safe(ii)

    show_ranklist.short_description = mark_safe('<p align="center"> Rank信息</p>')

    def show_rank(self, obj):
        rt = u"<a id=show_rank_%s>查看</a><script>$('#show_rank_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'历史排名',fix:false,shadeClose: true,maxmin:true,area:['1000px','600px'],content:'/t_config_apiurl_asin/show_rank/?ASIN=%s',});});</script>" % (
        obj.id, obj.id, obj.ASIN)
        return mark_safe(rt)

    show_rank.short_description = u'历史排名'

    def show_group1_urls(self, obj):
        rt_url = u'<a href="/Project/admin/skuapp/t_config_apiurl_asin/?%s">%s</a>' % (
        urlencode({'_p_group1__exact': obj.group1}), obj.group1)
        return mark_safe(rt_url)

    show_group1_urls.short_description = u'一级分类'

    def show_group2_urls(self, obj):
        rt_url = u'<a href="/Project/admin/skuapp/t_config_apiurl_asin_cf/?%s">%s</a>' % (
        urlencode({'_p_group1__exact': obj.group1, '_p_group2__exact': obj.group2}), obj.group2)
        return mark_safe(rt_url)

    show_group2_urls.short_description = u'二级分类'

    list_display = (
    'id', 'show_SmallImage', 'Collar', 'Remarks', 'show_asin_urls', 'Rank', 'show_rank', 'Status', 'Title', 'Serial',
    'ListPrice', 'UplsitTime', 'RefreshTime', 'Added_Time', 'show_group1_urls', 'show_group2_urls', 'group3', 'group4',
    'group5')
    list_editable = None
    search_fields = (
    'id', 'ASIN', 'URL', 'Status', 'Collar', 'DealName', 'Title', 'Brand', 'Feature', 'ListPrice', 'SmallImage',
    'ProductGroup', 'Error', 'Serial', 'Rank', 'group1', 'group2', 'group3', 'group4', 'group5')
    list_filter = (
    'URL', 'Status', 'UplsitTime', 'RefreshTime', 'Title', 'Brand', 'Collar', 'YNEnabled', 'DealName', 'DealTime',
    'Feature', 'ProductGroup', 'Error', 'Serial', 'Rank', 'group1', 'group2', 'group3', 'group4', 'group5')
    readonly_fields = (
    'id', 'SmallImage', 'ProductGroup', 'ASIN', 'URL', 'Status', 'Collar', 'Title', 'Brand', 'ListPrice', 'UplsitTime',
    'RefreshTime', 'Feature', 'Error', 'Serial', 'Rank', 'group1', 'group2', 'group3', 'group4', 'group5')
    list_display_links = ('id',)


    def get_list_queryset(self, ):
        request = self.request
        return  super(t_config_apiurl_asin_cf_Admin, self).get_list_queryset().filter(category=u'nocloth').filter(Collar=u'duplication')
        

        


