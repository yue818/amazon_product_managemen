# coding=utf-8

# import oss2
# from skuapp.table.t_templet_public_ebay import t_templet_public_ebay
# from skuapp.table.t_templet_ebay_collection_box import t_templet_ebay_collection_box

import datetime

from random import randint
from django.contrib import messages
from django.utils.safestring import mark_safe

from ebayapp.table.t_config_site_ebay import t_config_site_ebay
from skuapp.table.t_templet_ebay_variations import t_templet_ebay_variations
from skuapp.table.t_templet_ebay_wait_upload import t_templet_ebay_wait_upload


class t_templet_public_ebay_Admin(object):
    # plateform_distribution_navigation = True
    site_left_menu_flag_ebay = True
    search_box_flag = True

    list_display = ('id', 'show_image', 'show_site', 'Selleruserid', 'sku', 'Title', 'show_variation', 'CoreWords', 'UsedNum', 'show_info')

    list_display_links = ('',)

    actions = ['to_wait_upload']

    def show_image(self, obj):
        imageUrl = obj.Images.split(',')[0]  # .split('?')[0]
        # imageUrl = imageUrl.replace('https://i.ebayimg.com','http://fancyqube-ebaypic.oss-cn-shanghai.aliyuncs.com')
        rt = u'<img src="%s" style="width: 150px; height: 150px">&nbsp;&nbsp;' % (imageUrl)
        return mark_safe(rt)

    show_image.short_description = u'<p align="center"style="color:#428bca;">主图</p>'

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

    show_code.short_description = u'<p align="center"style="color:#428bca;">商品编码</p>'

    def show_site(self, obj):
        try:
            rt = t_config_site_ebay.objects.get(siteID=obj.Site).siteName
        except:
            rt = str(obj.Site)

        return mark_safe(rt)

    show_site.short_description = u'<p align="center"style="color:#428bca;">站点</p>'

    def show_variation(self, obj):
        """展示修改变体信息"""
        rt = u'<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1">' \
             u'<tr bgcolor="#C00"><th style="text-align:center">SKU</th><th style="text-align:center">价格</th>' \
             u'<th style="text-align:center">数量</th><th style="text-align:center">颜色</th>' \
             u'<th style="text-align:center">尺寸</th>'

        if obj.Variation:
            variation_list = eval(obj.Variation).get("Variation", '')
            if variation_list != '':
                i = 0
                for variation in variation_list:
                    if i < 5:
                        sku = variation.get('SKU', '')
                        price = variation.get('StartPrice', '')
                        quantity = variation.get('Quantity', '')

                        color = ''
                        size = ''
                        VariationSpecifics = variation.get('VariationSpecifics', '')
                        if VariationSpecifics != '':
                            NameValueList = VariationSpecifics.get('NameValueList', '')
                            if NameValueList != '':
                                for each in NameValueList:
                                    if 'Color' in each.values():
                                        color = each.get('Value', '')
                                    if 'Size' in each.values():
                                        size = each.get('Value', '')

                        rt = u'%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' % \
                             (rt, sku, price, quantity, color, size)
                    else:
                        break
                    i += 1
        else:
            sku = obj.sku
            price = obj.StartPrice
            quantity = obj.Quantity
            color = ''
            size = ''
            rt = u'%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' % \
                (rt, sku, price, quantity, color, size)

        rt = '%s<tr><td><a id="link_id_%s">点击查看</a></td></tr>' % (rt, obj.id)
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
             "title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1200px','700px']," \
             "content:'/show_ebay_variation/?public=%s&flag=ebay',btn:['关闭页面']});});</script>" % (rt, obj.id, obj.id)

        return mark_safe(rt)

    show_variation.short_description = u'<p align="center"style="color:#428bca;">变体信息</p>'

    def show_info(self, obj):
        """展示时间、人员信息"""
        st = ''
        if obj.Status == 'OPEN':
            st = u'<font color="#FFCC33">正在处理</font>'
        elif obj.Status == 'YES':
            st = u'<font color="#FF3333">已提交</font>'
        elif obj.Status == 'NO':
            st = u'<font color="#00BB00">未提交</font>'
        rt = u'创建人:%s<br>创建时间:<br>%s<br>更新人:%s<br>更新时间:<br>%s<br>提交状态:%s<br>上传文件:<br>%s' \
             % (obj.CreateStaff, obj.CreateTime, obj.UpdateStaff, obj.UpdateTime, st, obj.ExcelFile)
        return mark_safe(rt)

    show_info.short_description = u'<p align="center"style="color:#428bca;">采集信息</p>'

    def to_wait_upload(self, request, queryset):
        time = datetime.datetime.now()
        format_time = datetime.datetime.strptime(str(time).split('.')[0], '%Y-%m-%d %H:%M:%S')
        user = request.user.first_name
        for obj in queryset:
            plan = {'interval': ''}

            Inval = randint(1, 500)
            plan['start'] = (format_time + datetime.timedelta(minutes=Inval)).strftime("%Y-%m-%d %H:%M:%S")
            wait_upload_obj = t_templet_ebay_wait_upload()
            wait_upload_obj.__dict__ = obj.__dict__
            wait_upload_obj.CreateTime = time
            wait_upload_obj.CreateStaffName = user
            wait_upload_obj.UpdateTime = time
            wait_upload_obj.UpdateStaff = user
            wait_upload_obj.Status = 'NO'
            wait_upload_obj.ShopSets = ''
            wait_upload_obj.TimePlan = plan
            wait_upload_obj.ShippingTempID = None
            wait_upload_obj.save()
            obj.Status = 'YES'
            obj.Flag = 0
            obj.UsedNum += 1
            obj.save()

    to_wait_upload.short_description = u'转为待铺货'

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_templet_public_ebay_Admin, self).get_list_queryset()
        id = request.GET.get('id', '')
        Title = request.GET.get('Title', '')
        Site = request.GET.get('Site', '')
        Selleruserid = request.GET.get('Selleruserid', '')

        Status = request.GET.get('Status', '')
        sku = request.GET.get('sku', '')
        CreateStaff = request.GET.get('CreateStaff', '')
        UpdateStaff = request.GET.get('UpdateStaff', '')

        CreateTime_Start = request.GET.get('CreateTime_Start', '')
        CreateTime_End = request.GET.get('CreateTime_End', '')
        UpdateTime_Start = request.GET.get('UpdateTime_Start', '')
        UpdateTime_End = request.GET.get('UpdateTime_End', '')

        searchList = {'id__exact': id, 'Title__contains': Title, 'Site__exact': Site, 'Selleruserid__exact': Selleruserid,
                      'Status__exact': Status, 'sku__exact': sku,
                      'CreateStaff__exact': CreateStaff, 'UpdateStaff__exact': UpdateStaff,
                      'CreateTime__gte': CreateTime_Start, 'CreateTime__lt': CreateTime_End,
                      'UpdateTime__gte': UpdateTime_Start, 'UpdateTime__lt': UpdateTime_End,
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
            except Exception:
                messages.error(request, u'输入的查询数据有问题！')
        return qs
