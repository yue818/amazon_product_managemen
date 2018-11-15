# -*-coding:utf-8 -*-
from skuapp.table.t_product_suvering import t_product_suvering
from skuapp.views import show_data_by_user
from django.utils.safestring import mark_safe
from django.contrib import messages


class t_product_survering_admin(object):
    suring_plugin = True
    search_box_flag = True

    # sku_count = True

    fields = ()
    list_display = (
    'show_sourcepic_path','suvering_time', 'show_Name_Pid', 'category', 'price',
    'sale_time', 'sale_number', 'show_ratingnum','show_edit_suvering_is','show_edit_getinfo_cate','show_variants','show_edit_getinfo_remark','show_edit_link_1688', 'getinfo_time','getinfo_status',
    'saler','show_fresh_info')

    # def show_rating_details(self, obj):
    #     rt = '点击查看评论详情'
    #     return mark_safe(rt)
    # show_rating_details.short_description = u'评论详情'

    # def show_Name_Pid(self, obj):
    #     if obj.PB == 0:
    #         ispb = u'否'
    #     elif obj.PB == 1:
    #         ispb = u'是'
    #     else:
    #         ispb = u'未获取到广告'
    #     title_r = obj.title
    #     if title_r is None:
    #         title_r = u'未获取到标题'
    #     rt = u'标题:<br>%s<br>产品ID:<a href=" https://www.wish.com/c/%s" target="_blank">%s</a><br>是否有PB:%s' % (title_r, obj.product_id, obj.product_id,ispb)
    #     return mark_safe(rt)
    # show_Name_Pid.short_description = u'标题/产品ID/是否有PB'
    def del_None(self, col):
        rt = col
        if not col:
            rt = ''
        return rt

    def show_Name_Pid(self, obj):
        input_id = str(obj.id)

        # if obj.PB == 0:
        #     ispb = u'否'
        # elif obj.PB == 1:
        #     ispb = u'是'
        # else:
        #     ispb = obj.PB
        if obj.status == 1:
            if 'www.' in obj.product_id:
                rt = u'产品ID:None<br>产品URL:<a href="%s" target="_blank">%s</a><br>标题:%s<br>PB(1:有 0:无 -1:未获取到):  %s' % (obj.product_id, obj.product_id, obj.title, obj.PB)

            else:
                rt = u'产品ID:<a href=" https://www.wish.com/c/%s" target="_blank">%s</a><br>产品URL:None<br>标题:%s<br>PB(1:有 0:无 -1:未获取到):  %s' %(obj.product_id, obj.product_id, obj.title, obj.PB)

        else:
            rt = u'产品ID:<a href=" https://www.wish.com/c/%s" target="_blank">%s</a>' \
                 u'产品URL:<a href="%s" target="_blank">%s</a>' \
                 u'<br>标题:<input type="text" style="width:180px" id="title_%s" value="%s" />' \
                 u'<script>$(document).ready(function(){$("#title_%s").blur(function(){var title = $("#title_%s").val();' \
                 u'{$.ajax({url:"/show_edit_jp_info_tile/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
                 u'dataType: "json",data:{"title":title,"id":"%s"},' \
                 u'success:function(data, textStatus, jqXHR){if(data == "1"){document.getElementById("title_%s").text="success";}},' \
                 u'error:function(jqXHR, textStatus, errorThrown){ alert("failed")}});}}); ' \
                 u'}); </script>' % ( obj.product_id,obj.product_id,obj.product_url,obj.product_url,input_id, str(obj.title), input_id,input_id,input_id, input_id)
            rt = rt + u'<br>PB(1:有 0:无 -1:未获取到):<input type="text" style="width:90px" id="pb_%s" value="%s" />' \
                 u'<script>$(document).ready(function(){$("#pb_%s").blur(function(){var pb = $("#pb_%s").val();' \
                 u'{$.ajax({url:"/show_edit_jp_info_pb/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",' \
                 u'dataType: "json",data:{"pb":pb,"id":"%s"},' \
                 u'success:function(data, textStatus, jqXHR){if(data == "1"){document.getElementById("pb_%s").text="success";}},' \
                 u'error:function(jqXHR, textStatus, errorThrown){ alert("failed")}});}}); ' \
                 u'}); </script>' % ( input_id,obj.PB, input_id,input_id,input_id, input_id)
        return mark_safe(rt)
    show_Name_Pid.short_description =mark_safe('<p style="width:200px">标题/产品ID/PB</p>')


    def show_ratingnum(self, obj):
        rt = u'rating_num:%s<br>7daysrating_num:%s<br>rating:%s<br>小火苗:%s' % (obj.comment_number, obj.sevenratingnum, obj.point,obj.little_flames)
        return mark_safe(rt)
    show_ratingnum.short_description = u'ratings'

    # def show_title(self, obj):
    #     rt = u'<p width="10">%s</p>' %(obj.title)
    #     return mark_safe(rt)
    # #show_title.short_description = u'标题'
    # show_title.short_description = mark_safe(u'<p "width:20">标题</p>')

    def show_sourcepic_path(self, obj):
        rt = '<img src="%s"  width="120" height="120"/>' % (obj.sourcepic_path)
        return mark_safe(rt)
    show_sourcepic_path.short_description = u'图片'

    def show_fresh_info(self, obj):
        if 'www.' in obj.product_id:
            rt = u"<a id=update_applyInfo%s>点击刷新</a><script>$('#update_applyInfo%s').on('click',function(){layer.open(" \
                 u"{type:2,skin:'layui-layer-lan',title:'点击刷新',fix:false,shadeClose: true,maxmin:true," \
                 u"content:'/show_wish_refresh/?product_id=%s',end:function (){location.reload();}});});</script>" % (
                     obj.id, obj.id, obj.product_id)
        else:
            rt = u"<a id=update_applyInfo%s>点击刷新</a><script>$('#update_applyInfo%s').on('click',function(){layer.open(" \
                 u"{type:2,skin:'layui-layer-lan',title:'点击刷新',fix:false,shadeClose: true,maxmin:true," \
                 u"content:'/show_wish_refresh/?product_id=%s',end:function (){location.reload();}});});</script>" % (
                     obj.product_id, obj.product_id, obj.product_id)
        return mark_safe(rt)
    show_fresh_info.short_description = u'刷新信息'

    def show_variants(self, obj):
        rt = u"<a id=show_applyInfo%s>点击查看评论(最多50条)</a><script>$('#show_applyInfo%s').on('click',function(){layer.open(" \
             u"{type:2,skin:'layui-layer-lan',title:'点击查看评论(最多50条)',fix:false,shadeClose: true,maxmin:true," \
             u"area:['1200px','800px'],content:'/show_wish_variant_jp/?product_id=%s'});});</script>" % (obj.id,obj.id,obj.product_id)
        return mark_safe(rt)
    show_variants.short_description = u'<span style="color: #428bca">评论详情</span>'

    def show_edit_suvering_is(self, obj):
        rt = u'<textarea onchange="to_change_work(\'%s\',\'%s\',this.value,' \
             u'\'t_product_suvering\')" title="%s" style="height:120px;width:100px;resize:none;">%s</textarea>' \
             u'<span id="%s"></span>'%(obj.id, 'suvering_is', self.del_None(obj.suvering_is),
                                       self.del_None(obj.suvering_is), str(obj.id)+'_suvering_is')
        return mark_safe(rt)
    show_edit_suvering_is.short_description = u'调研结果'

    def show_edit_getinfo_cate(self, obj):
        rt = u'<textarea onchange="to_change_work(\'%s\',\'%s\',this.value,' \
             u'\'t_product_suvering\')" title="%s" style="height:120px;width:100px;resize:none;">%s</textarea>' \
             u'<span id="%s"></span>'%(obj.id, 'getinfo_cate', self.del_None(obj.getinfo_cate),
                                       self.del_None(obj.getinfo_cate), str(obj.id)+'_getinfo_cate')
        return mark_safe(rt)
    show_edit_getinfo_cate.short_description = u'调研分类'

    def show_edit_link_1688(self, obj):
        rt = u'<textarea onchange="to_change_work(\'%s\',\'%s\',this.value,' \
             u'\'t_product_suvering\')" title="%s" style="height:120px;width:120px;resize:none;">%s</textarea>' \
             u'<span id="%s"></span>'%(obj.id, 'link_1688', self.del_None(obj.link_1688),
                                       self.del_None(obj.link_1688), str(obj.id)+'_link_1688')
        return mark_safe(rt)
    show_edit_link_1688.short_description = u'1688链接'

    def show_edit_getinfo_remark(self, obj):
        rt = u'<textarea onchange="to_change_work(\'%s\',\'%s\',this.value,' \
             u'\'t_product_suvering\')" title="%s" style="height:120px;width:120px;resize:none;">%s</textarea>' \
             u'<span id="%s"></span>'%(obj.id, 'getinfo_remark', self.del_None(obj.getinfo_remark),
                                       self.del_None(obj.getinfo_remark), str(obj.id)+'_getinfo_remark')
        return mark_safe(rt)
    show_edit_getinfo_remark.short_description = u'调研备注'

    list_editable = ('link', 'saler', 'show_title', 'price', 'sale_number', 'rank','getinfo_remark', 'getinfo_cate','sale_time','link_1688','suvering_is')

    def get_list_queryset(self):
        request = self.request
        qs = super(t_product_survering_admin, self).get_list_queryset()
        result = show_data_by_user(request,'t_product_suvering')
        if result == 0:
            qs = qs.filter(saler=request.user.username)
        product_id = request.GET.get('product_id', '')
        saler = request.GET.get('saler', '')
        getinfo_cate = request.GET.get('getinfo_cate', '')
        PB = request.GET.get('PB', '')
        status = request.GET.get('status', '')
        title = request.GET.get('title', '')
        suvering_timeStart = request.GET.get('suvering_timeStart', '')
        suvering_timeEnd = request.GET.get('suvering_timeEnd', '')
        sale_timeStart = request.GET.get('sale_timeStart', '')
        sale_timeEnd = request.GET.get('sale_timeEnd', '')
        getinfo_remark = request.GET.get('getinfo_remark','')
        searchList = {'product_id__exact': product_id,
                      'saler__exact': saler,
                      'getinfo_cate__exact': getinfo_cate,
                      'PB__exact': PB,
                      'suvering_time__gte': suvering_timeStart,
                      'suvering_time__lt': suvering_timeEnd,
                      'sale_time__gte': sale_timeStart,
                      'sale_time__lt': sale_timeEnd,
                      'status__exact': status,
                      'title__contains': title,
                      'getinfo_remark__contains':getinfo_remark,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    #  v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        return qs