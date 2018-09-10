#-*-coding:utf-8-*-
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from skuapp.table.t_templet_amazon_published_variation import *
from skuapp.table.t_templet_amazon_collection_box import t_templet_amazon_collection_box
import time,datetime


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_upload_result_Admin.py
 @time: 2017/12/16 9:53
"""
class t_templet_amazon_upload_result_Admin(object):
    # plateform_distribution_navigation = True
    # site_left_menu_flag = True
    amazon_site_left_menu_tree_flag = True
    search_box_flag = True
    
    def show_image(self, obj):
        if obj.main_image_url:
            rt = u'<img src="%s" style="width: 100px; height: 100px">&nbsp;&nbsp;' % (obj.main_image_url)
        else:
            main_image_url = ''
            main_image_urls = t_templet_amazon_published_variation.objects.filter(
                prodcut_variation_id=obj.prodcut_variation_id).values_list('main_image_url')
            if main_image_urls:
                main_image_url = main_image_urls[0][0]
            rt = u'<img src="%s" style="width: 100px; height: 100px">&nbsp;&nbsp;' % (main_image_url)
        return mark_safe(rt)

    show_image.short_description = u'主图'

    def show_product_sku(self, obj):
        count = 0
        sku_show = ''
        if obj.productSKU:
            for i in obj.productSKU:
                count += 1
                sku_show += i
                if count % 10 == 0:
                    sku_show += '<br>'
        return mark_safe(sku_show)
    show_product_sku.short_description = '商品SKU'

    def show_info(self, obj):
        """展示时间、人员信息"""
        st = ''
        if obj.status == 'SUCCESS':
            #     st = u'<font color="#FFCC33">正在处理</font>'
            # elif obj.Status == 'YES':
            st = u'<font color="#00BB00">刊登成功</font>'
        elif obj.status == 'FAILED':
            st = u'<font color="#66FF66">刊登失敗</font>'
        else:
            st = u'<font color="#FFCC33">正在刊登中</font>'
        rt = u'创建人:%s<br>创建时间:<br>%s<br>更新人:%s<br>更新时间:<br>%s<br>刊登状态:%s<br>' \
             % (obj.createUser, obj.createTime, obj.updateUser, obj.updateTime, st)
        return mark_safe(rt)

    show_info.short_description = u'&nbsp;&nbsp;&nbsp;采 集 信 息&nbsp;&nbsp;&nbsp;'


    def show_schedule(self, obj):
        """展示刊登店铺"""
        if obj.ShopSets == '' or obj.ShopSets is None:
            shops = ''
            num = 0
        else:
            shopList = obj.ShopSets.split(',')
            num = len(shopList)
            shops = ''
            for i in range(num):
                if (i + 1) % 10 == 0:
                    shops = shops + shopList[i] + '<br>'
                else:
                    shops = shops + shopList[i] + ','

        rt = '<span style="color: #0000FF;font-weight: 600">%d个</span>' % num
        rt = '(%s)目标店铺：%s<br>' % (rt, shops)

        state = obj.status
        if state == 'SUCCESS':
            rt = '%s<br><br><p style="color: #00BB00">%s</p>' % (rt, u'刊登成功')
        elif state == 'FAILED':
            rt = '%s<br><br><p style="color: #66FF66">%s</p>' % (rt, u'刊登失败')
        else:
            rt = '%s<br><br><p style="color: #FFCC33">%s</p>' % (rt, u'正在刊登中')

        return mark_safe(rt)
    show_schedule.short_description = u'&nbsp;&nbsp;刊登计划&nbsp;&nbsp;'

    def show_result(self, obj):
        rt = obj.resultInfo
        if obj.errorMessages:
            rt += ', Reason: '+obj.errorMessages[0:20]
        return mark_safe(rt)
    show_result.short_description = u'&nbsp;&nbsp;刊登结果&nbsp;&nbsp;'


    def show_variation_info(self,obj):
        """有变体展示变体信息，没有变体展示单体"""
        t_templet_amazon_published_variation_objs = t_templet_amazon_published_variation.objects.filter(
            prodcut_variation_id=obj.prodcut_variation_id)
        if t_templet_amazon_published_variation_objs:
            rt = '<table class="table table-condensed"><tr><td>类型</td><td>变体名</td><td>店铺SKU</td><td>包装数</td></tr>'
            for t_templet_amazon_published_variation_obj in t_templet_amazon_published_variation_objs[0:4]:
                variation_value = ''
                if t_templet_amazon_published_variation_obj.variation_theme == 'Color':
                    variation_value = t_templet_amazon_published_variation_obj.color_name
                if t_templet_amazon_published_variation_obj.variation_theme == 'Size':
                    variation_value = t_templet_amazon_published_variation_obj.size_name
                if t_templet_amazon_published_variation_obj.variation_theme == 'Size-Color':
                    variation_value = t_templet_amazon_published_variation_obj.size_name + '--' + \
                                      t_templet_amazon_published_variation_obj.color_name
                if t_templet_amazon_published_variation_obj.variation_theme == 'MetalType':
                    variation_value = t_templet_amazon_published_variation_obj.MetalType
                if t_templet_amazon_published_variation_obj.variation_theme == 'MetalType-Size':
                    variation_value = t_templet_amazon_published_variation_obj.MetalType + '--' + \
                                      t_templet_amazon_published_variation_obj.size_name
                rt += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(t_templet_amazon_published_variation_obj.variation_theme,
                       variation_value,t_templet_amazon_published_variation_obj.child_sku,
                        t_templet_amazon_published_variation_obj.item_quantity,)
            if len(t_templet_amazon_published_variation_objs) > 4:
                rt += '<tr><td><a id="more_id_%s">更多</a></td></tr></table>' % obj.id
                rt = u"%s<script>$('#more_id_%s').on('click',function()" \
                     u"{layer.open({type:2,skin:'layui-layer-lan',title:'全部变体信息'," \
                     u"fix:false,shadeClose: true,maxmin:true,area:['800px','400px'],btn: ['关闭页面']," \
                     u"content:'/t_templet_amazon_upload/?pvi=%s',});" \
                     u"});</script>" % (rt, obj.id, obj.prodcut_variation_id)
            else:
                rt += '</table>'
        else:
            rt = u"单体"
        return mark_safe(rt)

    show_variation_info.short_description =  mark_safe(u'<p style="color:#428BCA" align="center">单体/变体</p>')


    list_display = ('show_image', 'item_sku', 'show_product_sku', 'item_name', 'show_variation_info', 'show_schedule', 'show_info',)

    list_display_links = ('id')

    actions = ['copy_product_info']

    def copy_product_info(self, request, queryset):
        for obj in queryset:
            variation_obj = t_templet_amazon_published_variation.objects.filter(parent_item_sku=obj.productSKU, prodcut_variation_id=obj.prodcut_variation_id)
            prodcut_variation_id = int(time.time() * 1000)
            time_now = datetime.datetime.now()
            collection_box_new_obj = t_templet_amazon_collection_box()
            collection_box_new_obj.__dict__ = obj.__dict__
            collection_box_new_obj.prodcut_variation_id = prodcut_variation_id
            collection_box_new_obj.item_sku = None
            collection_box_new_obj.external_product_id = None
            collection_box_new_obj.ShopSets = None
            collection_box_new_obj.createUser = request.user.username
            collection_box_new_obj.createTime = time_now
            collection_box_new_obj.updateUser = request.user.username
            collection_box_new_obj.updateTime = time_now
            collection_box_new_obj.status = '1'
            collection_box_new_obj.can_upload = '-1'
            collection_box_new_obj.item_name = collection_box_new_obj.item_name.replace(obj.manufacturer, '', 1)
            collection_box_new_obj.id = None
            collection_box_new_obj.save()
            if variation_obj:
                for variation in variation_obj:
                    variation_new_obj = t_templet_amazon_published_variation()
                    variation_new_obj.__dict__ = variation.__dict__
                    variation_new_obj.prodcut_variation_id = prodcut_variation_id
                    variation_new_obj.parent_sku = None
                    variation_new_obj.child_sku = None
                    variation_new_obj.createUser = request.user.username
                    variation_new_obj.createTime = time_now
                    variation_new_obj.updateUser = request.user.username
                    variation_new_obj.updateTime = time_now
                    variation_new_obj.external_product_id = None
                    variation_new_obj.id = None
                    variation_new_obj.save()
        return HttpResponseRedirect('/Project/admin/skuapp/t_templet_amazon_collection_box/')
    copy_product_info.short_description = u'复制到草稿箱'

    def get_list_queryset(self,):
        qs = super(t_templet_amazon_upload_result_Admin, self).get_list_queryset()
        item_sku = self.request.GET.get('item_sku', '')
        productSKU = self.request.GET.get('productSKU', '')
        item_name = self.request.GET.get('item_name', '')
        updateUser = self.request.GET.get('updateUser', '')
        createTimeStart = self.request.GET.get('createTimeStart', '')
        createTimeEnd = self.request.GET.get('createTimeEnd', '')
        updateTimeStart = self.request.GET.get('updateTimeStart', '')
        updateTimeEnd = self.request.GET.get('updateTimeEnd', '')

        searchList = {'item_sku__exact': item_sku,'productSKU__exact': productSKU,
                      'item_name__contains': item_name,'updateUser__exact': updateUser,
                      'createTime__gte': createTimeStart, 'createTime__lt': createTimeEnd,
                      'updateTime__gte': updateTimeStart, 'createTime__lt':updateTimeEnd,
                      }
        if self.request.user.is_superuser:
            pass
        else:
            """显示可显示的，自己本人的"""
            searchList['createUser__exact'] = self.request.user.username
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        if v.find('Wish-') == -1:
                            v = 'Wish-' + v.zfill(4)
                    sl[k] = v
        if sl:
            qs = qs.filter(**sl)
        return qs