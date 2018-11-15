# -*- coding: utf-8 -*-


from django.utils.safestring import mark_safe
from skuapp.table.t_product_mainsku_pic import t_product_mainsku_pic
from django.contrib import messages


class t_product_image_modify_Admin(object):

    plateform_distribution_navigation = True

    def show_info(self, obj):
        plateform = self.request.GET.get('plateform', '')
        rr = u'%s' % obj.MainSKU

        if plateform == 'wish':
            if obj.UpdateFlag == 1:
                rr = u'%s<br><br><span style="color:blue;">图片更新<span' % rr
        else:
            if obj.UpdateFlagJoom == 1:
                rr = u'%s<br><br><span style="color:blue;">图片更新<span' % rr
        return mark_safe(rr)
    show_info.short_description = u'<span style="color: #428bca">主SKU</span>'


    def show_all_image(self,obj):
        plateform = self.request.GET.get('plateform', '')
        if plateform == 'wish':
            ImageTemp = t_product_mainsku_pic.objects.filter(MainSKU=obj.MainSKU, Flag=1)
        else:
            ImageTemp = t_product_mainsku_pic.objects.filter(MainSKU=obj.MainSKU, FlagJoom=1)

        if ImageTemp.exists():
            rt = u'<table>'
            for temp in ImageTemp:
                pic = temp.WishPic.replace('original', 'medium')
                rt = '%s<img src="%s"  width="160" height="160"/>&nbsp;'%(rt,pic)
            rt = u"%s</table>" % rt
        else:
            rt = u'主图未维护,请点击 '
        tt =  "<a id=show_all_image_%s>编辑</a><script>$('#show_all_image_%s').on('click',function(){layer.open(" \
              "{type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1200px','800px']," \
              "content:'/t_product_image_modify/all_image/?code=%s&plateform=%s',end:function(){location.reload();" \
              "var now_url='/remove_wish_pic_update_flag/?main_sku=%s&plateform=%s';var xhr=new XMLHttpRequest();xhr.open('get',now_url);" \
              "xhr.send();}});});</script>"%(obj.id, obj.id, obj.MainSKU, plateform, obj.MainSKU, plateform)
        return mark_safe(rt+tt)
    show_all_image.short_description = u'<span style="color: #428bca">图片</span>'

    list_display= ('id','show_info','show_all_image',)
    list_display_links = ('',)
    search_fields = ('MainSKU',)
    list_filter = ('MainSKU', 'UpdateFlag', 'UpdateFlagJoom')

            
            
            
            
            
            
            
            