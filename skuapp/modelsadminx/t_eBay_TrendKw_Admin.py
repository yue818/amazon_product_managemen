#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_eBay_TrendKw_Admin.py
 @time: 2018-08-03 9:37
"""
from django.utils.safestring import mark_safe
from django.contrib import messages

class t_eBay_TrendKw_Admin(object):
    search_box_flag = True

    def show_pic(self, obj):

        dataurl = 'https://explore.ebay.com/story?id=%s' % (obj.id, )

        rt = '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s" />' % (obj.ImgUrl, u'无法显示', obj.TrendTitle)
        rt = u'%s <br\><p style="text-align: center"><a href="%s" target="_blank">数据源址</a></p>' %(rt, dataurl)

        return mark_safe(rt)
    show_pic.short_description = mark_safe('<p style="color:#428bca;text-align:center">图片</p>')

    list_display_links = ('id',)
    list_display = ('show_pic', 'TrendDate', 'TrendSite', 'TrendTitle', 'TrendDesc', 'BurstKw', 'TrendSearches',)

    def get_list_queryset(self):
        request = self.request
        qs = super(t_eBay_TrendKw_Admin, self).get_list_queryset()

        TrendTitle = request.GET.get('TrendTitle', '')
        TrendSite = request.GET.get('TrendSite', '')
        TrendDate_Start = request.GET.get('TrendDate_Start', '')
        TrendDate_End = request.GET.get('TrendDate_End', '')
        Searches_Start = request.GET.get('Searches_Start', '')
        Searches_End = request.GET.get('Searches_End', '')

        searchList = {'TrendSite__exact': TrendSite,
                      'TrendTitle__icontains': TrendTitle,
                      'TrendDate__gte': TrendDate_Start,
                      'TrendDate__lt': TrendDate_End,
                      }

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有误！')

        # 字符转整数的调整
        wherestr = ''
        if Searches_Start != '':
            wherestr = "cast(replace(trendsearches,',','') as SIGNED)>=%s" % Searches_Start
        if Searches_End != '':
            if wherestr == '':
                wherestr = "cast(replace(trendsearches,',','') as SIGNED)<=%s" % Searches_End
            else:
                wherestr = "cast(replace(trendsearches,',','') as SIGNED) between %s and %s" % (Searches_Start, Searches_End,)

        if wherestr != '':
            qs = qs.extra(where=[wherestr])

        ordercol = request.GET.get('o', '')
        if 'TrendSearches' in ordercol:
            ordercol = ordercol.replace('TrendSearches', 'TrendSearches1').split('.')
            qs = qs.extra(select={'TrendSearches1': "cast(replace(trendsearches,',','') as SIGNED)"}).order_by(
                *ordercol)

        return qs