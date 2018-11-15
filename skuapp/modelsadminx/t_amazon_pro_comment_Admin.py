# -*-coding:utf-8-*-

from django.utils.safestring import mark_safe
from django.contrib import messages
from skuapp.table.t_amazon_pro_comment import t_amazon_pro_comment

class t_amazon_pro_comment_Admin(object):
    t_amazon_comment = True
    # search_box_flag = True
    comment_report = True

    def showImage(self, obj):
        rt = '<div style="position:relative; width:120px"><img src="%s" width="120" height="120" alt="无法显示" title="%s"/>' \
             '</div>' % (obj.imageurl,obj.imageurl)
        return mark_safe(rt)

    showImage.short_description = mark_safe('<p style="color:#428bca;text-align:left;width:90px">图片</p>')

    def showTime(self, obj):
        t = obj.comment_time[:10]
        rt = '<div style="color:black;text-align:left;width:90px">%s</div>' % (t,)
        return mark_safe(rt)

    showTime.short_description = mark_safe('<p style="color:#428bca;text-align:left;width:90px">评论时间</p>')

    list_display = (
    'showImage', 'title', 'asin', 'star', 'comment_title', 'customer', 'showTime', 'color', 'si', 'comment', 'other', 'get_time',)
    # list_filter = ('asin', 'title')

    def get_list_queryset(self):
        request = self.request
        qs = super(t_amazon_pro_comment_Admin, self).get_list_queryset()

        asin = request.GET.get('asin', '')

        searchList = {'asin__exact': asin,
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
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs



