# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_config_wishapi_product_analyse_info_original_trans_Admin.py
 @time: 2018/6/15 8:53
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from datetime import datetime
from django.contrib import messages
from django.utils.safestring import mark_safe

class t_config_wishapi_product_analyse_info_original_trans_Admin(object):
    search_box_flag = True
    #wish_original_left_menu = True

    def GoodsInfo(self,obj):
        rating = obj.rating
        if obj.num_rating == 0:
            rating = 0
        rt = u'<p style="width:200px;"><strong>评分rating:</strong>%s <br><strong>rating_num:</strong>%s <br>' \
             u'</p>'% (rating,obj.num_rating)
        return mark_safe(rt)
    GoodsInfo.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">Rating</p>')

    def GoodsSale(self,obj):
        rt = u'<p style="width:200px;"><strong>前1~7天销量:</strong>%s <br><strong>前8~14天销量	:</strong>%s</p>'\
             % (obj.OrdersLast7Days,obj.OrdersLast7to14Days)
        return mark_safe(rt)
    GoodsSale.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">商品销量</p>')

    def show_Picture(self,obj) :
       # self.update_status(obj)
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(obj.SourcePicPath,obj.SourcePicPath,obj.SourcePicPath)
        return mark_safe(rt)
    show_Picture.short_description = mark_safe(u'<p style="width:120px;color:#428bca;" align="center">图片</p>')

    def show_Name_Pid(self, obj):
        rt = u'产品ID:<a href=" https://www.wish.com/c/%s" target="_blank">%s</a><br>标题:%s<br>PB(1:有 0:无 -1:未获取到):  %s' % (obj.product_id,obj.product_id,obj.Name,obj.is_promo)
        return mark_safe(rt)
    show_Name_Pid.short_description =mark_safe('<p style="width:50px">标题/产品ID/PB</p>')

    def show_fresh_info(self, obj):
        rt = u"<a id=update_applyInfo%s>点击转竞品调研</a><script>$('#update_applyInfo%s').on('click',function(){layer.open(" \
             u"{type:2,skin:'layui-layer-lan',title:'点击转竞品调研',fix:false,shadeClose: true,maxmin:true," \
             u"content:'/show_wish_refresh/?product_id=%s',end:function (){location.reload();}});});</script>" % (
             obj.product_id, obj.product_id, obj.product_id)
        return mark_safe(rt)
    show_fresh_info.short_description = u'转竞品调研'

    list_per_page = 20
    #Pid,Name,SourcePicPath,num_rating,rating,o_price,shipping,NumBought,ShelveDay,OrdersLast7Days,OrdersLast7to14Days,Op_time,op_flag,getboughtinfo
    list_display = ('show_Picture','show_Name_Pid','viewdata','ShelveDay','NumBought','GoodsInfo','Op_time','DealName','show_fresh_info')
    #list_editable = ('productNumbers',)
    list_editable = ('DealName')


    def get_list_queryset(self):
        request = self.request
        qs = super(t_config_wishapi_product_analyse_info_original_trans_Admin, self).get_list_queryset()
        qs = qs.filter(DealName__isnull=True)

        product_id = request.GET.get('product_id', '')
        Name = request.GET.get('Name', '')

        ShelveDayStart = request.GET.get('ShelveDayStart', '')
        ShelveDayEnd = request.GET.get('ShelveDayEnd', '')
        Op_timeStart = request.GET.get('Op_timeStart', '')
        Op_timeEnd = request.GET.get('Op_timeEnd', '')

        NumBoughtStart = request.GET.get('NumBoughtStart', '')
        NumBoughtEnd = request.GET.get('NumBoughtEnd', '')
        ratingStart = request.GET.get('ratingStart', '')
        ratingEnd = request.GET.get('ratingEnd', '')
        num_ratingStart = request.GET.get('num_ratingStart', '')
        num_ratingEnd = request.GET.get('num_ratingEnd', '')
        viewdataStart = request.GET.get('viewdataStart', '')
        viewdataEnd = request.GET.get('viewdataEnd', '')

        searchList = {'product_id': product_id,
                      'Name__icontains': Name,
                      'ShelveDay__gte': ShelveDayStart,
                      'ShelveDay__lt': ShelveDayEnd,
                      'Op_time__gte': Op_timeStart,
                      'Op_time__lt': Op_timeEnd,
                      'NumBought__gte': NumBoughtStart,
                      'NumBought__lt': NumBoughtEnd,
                      'rating__gte': ratingStart,
                      'rating__lt': ratingEnd,
                      'num_rating__gte': num_ratingStart,
                      'num_rating__lt': num_ratingEnd,
                      'viewdata__gte': viewdataStart,
                      'viewdata__lt': viewdataEnd,
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
                messages.error(request, u'输入的查询数据有问题！')

        return qs

