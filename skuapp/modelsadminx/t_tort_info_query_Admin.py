#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_query_Admin.py
 @time: 2018-05-16 15:15
"""
from django.utils.safestring import mark_safe
from Project.settings import *

class t_tort_info_query_Admin(object):
    t_tort_tree_menu_flag = True

    def show_ProductPicUrl(self, obj):
        url = u'%s%s.%s/%s/%s/%s' % (PREFIX, BUCKETNAME_TORT, ENDPOINT_OUT, 'aliexpress', obj.ID, str(obj.ProductPicUrl))
        alt = u'无法显示:%s,%s' % (obj.Site, obj.MainSKU)
        title = 'Site:%s,MainSKU:%s' % (obj.Site, obj.MainSKU)
        rt = '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  ' % (url, alt, title)
        return mark_safe(rt)

    show_ProductPicUrl.short_description = u'<span style="color: #428bca">产品图片</span>'

    def show_ReceiveDetail(self, obj):
        rt = u'<span >%s</span>' % obj.ReceiveDetail
        return mark_safe(rt)

    show_ReceiveDetail.short_description = u'<span style="color: #428bca">领用详细信息</span>'

    def show_Site(self, obj):
        return mark_safe(obj.Site)

    show_Site.short_description = mark_safe('<p style="color:#428bca;">侵权站点</p>')

    def show_Step(self, obj):

        dict_step = {0:u'已登记',1:u'待审核',2:u'严重侵权同步普源',3:u'一般侵权同步普源',4:u'不侵权',9:u'驳回申请',10:u'被删除', 11:u'严重侵权',12:u'一般侵权',}
        if obj.Step in dict_step:
            rt = u'<span>%s</span>' % dict_step[obj.Step]
        else:
            rt = u'<span>未知</span>'
        return mark_safe(rt)

    show_Step.short_description = u'<span style="color: #428bca">当前状态</span>'


    list_display = (
    'ID', 'show_ProductPicUrl', 'MainSKU', 'show_Site', 'show_Step', 'show_ReceiveDetail', 'StaffID', 'Intellectual',
    'Trademark', 'ComplainReason', 'IPRange', 'IPForbiddenSite', 'SourceUrl', 'Suggestion', 'SalerName2', 'Purchaser','ProductID')

    list_filter = ('Account', 'AccountStaffID', 'Site', 'MainSKU', 'Intellectual', 'Trademark', 'SalerName2', 'Purchaser', 'IPRange',
                     'IPForbiddenSite', 'UpdateTime', 'DealTime1', 'StaffID','ProductID')
    search_fields = ('Account', 'AccountStaffID', 'Site', 'MainSKU', 'ProductTitle', 'Intellectual', 'Trademark',
                   'ComplainReason', 'ListingTitle', 'ContactWay', 'SalerName2', 'Purchaser', 'IPRange',
                     'IPForbiddenSite', 'SourceUrl', 'Suggestion', 'StaffID','ProductID')


    def get_list_queryset(self):
        qs = super(t_tort_info_query_Admin, self).get_list_queryset()

        return qs.exclude(Step=20) # Step != 20