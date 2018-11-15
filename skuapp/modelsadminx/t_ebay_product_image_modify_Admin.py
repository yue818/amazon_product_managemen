# coding=utf-8

# import oss2
# from datetime import datetime
# from django.contrib import messages
# from skuapp.table.t_templet_ebay_collection_box import t_templet_ebay_collection_box
# from skuapp.table.t_templet_public_ebay import t_templet_public_ebay

from django.utils.safestring import mark_safe
from skuapp.table.t_templet_ebay_variations import t_templet_ebay_variations


class t_ebay_product_image_modify_Admin(object):
    # plateform_distribution_navigation = True
    site_left_menu_flag_ebay = True

    def show_code(self, obj):
        rt = obj.sku
        t_templet_ebay_variations_objs = t_templet_ebay_variations.objects.filter(templetID=obj.id)
        if t_templet_ebay_variations_objs:
            rt = ''
            skuList = []
            for t_templet_ebay_variations_obj in t_templet_ebay_variations_objs:
                if t_templet_ebay_variations_obj:
                    sku = t_templet_ebay_variations_obj.variationSku
                    if sku not in skuList:
                        skuList.append(sku)
            i = 0
            for sku in skuList:
                if (i % 3) == 0:
                    rt += sku + ',<br/>'
                else:
                    rt += sku + ','
                i += 1
            rt = rt[:-1]
        return mark_safe(rt)
    show_code.short_description = u'商品编码'

    def show_image(self, obj):
        rt = ''
        imageUrls = obj.Images.split(',')
        for imageUrl in imageUrls:
            # imageUrl = imageUrl.replace('https://i.ebayimg.com','http://fancyqube-ebaypic.oss-cn-shanghai.aliyuncs.com/')
            rt += u'<img src="%s" style="width: 100px; height: 100px">&nbsp;&nbsp;' % (imageUrl)
        tt = "<br/><a id=show_all_image_%s>编辑</a><script>$('#show_all_image_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1000px','600px'],content:'/show_ebay_image/?myId=%s',end:function(){location.reload();}});});</script>" % \
            (obj.id, obj.id, obj.id)
        return mark_safe(rt + tt)
    show_image.short_description = u'主图'

    list_display = ('sku', 'show_image')

    list_display_links = ('',)

    # def get_list_queryset(self,):
    #     """显示可显示的，自己本人的"""
    #     request = self.request
    #     qs = super(t_ebay_product_image_modify_Admin, self).get_list_queryset()
    #     # if request.user.is_superuser:
    #     #     qs = qs
    #     # else:
    #     qs = qs.filter(CreateStaff = request.user.first_name).exclude(Flag=0)
    #     return qs
