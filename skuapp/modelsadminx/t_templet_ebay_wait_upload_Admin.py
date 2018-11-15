# coding=utf-8

# import oss2
# from datetime import datetime
# from app_djcelery.tasks import ebay_distribution
# from skuapp.table.t_templet_ebay_collection_box import t_templet_ebay_collection_box
# from skuapp.table.t_templet_ebay_wait_upload import t_templet_ebay_wait_upload

from django.db import connection
from django.contrib import messages
from django.utils.safestring import mark_safe

from brick.ebay.ebay_distribution import ebay_unfold_distribution as eub

from ebayapp.table.t_config_site_ebay import t_config_site_ebay
from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
from skuapp.table.t_templet_ebay_variations import t_templet_ebay_variations


class t_templet_ebay_wait_upload_Admin(object):
    # plateform_distribution_navigation = True
    site_left_menu_flag_ebay = True
    search_box_flag = True

    list_display = ('id', 'show_image', 'show_site', 'Selleruserid', 'show_code', 'Title', 'show_variation', 'CoreWords', 'show_schedule', 'show_info')

    list_display_links = ('id')

    actions = ['ebay_unfold_distribution']

    def show_image(self, obj):
        imageUrl = obj.Images.split(',')[0]  # .split('?')[0]
        # imageUrl = imageUrl.replace('https://i.ebayimg.com','http://fancyqube-ebaypic.oss-cn-shanghai.aliyuncs.com')
        rt = '<a href="/show_ebay_image/?myId=%s" target="_blank"><img src="%s" style="width:150px;height:150px"></a>' % (obj.id, imageUrl)
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
        """展示变体信息"""
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

        rt = u'%s<tr><td><a id="link_id_%s">点击修改</a></td></tr>' % (rt, obj.id)
        rt = u"%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
             u"title:'修改页面',fix:false,shadeClose: true,maxmin:true,area:['1200px','700px']," \
             u"content:'/show_ebay_variation/?upload=%s&flag=ebay',btn:['关闭页面'],end:function()" \
             u"{location.reload();}});});</script>" % (rt, obj.id, obj.id)

        return mark_safe(rt)

    show_variation.short_description = u'<p align="center"style="color:#428bca;">变体信息</p>'

    def show_schedule(self, obj):
        """展示铺货店铺、开始时间、结束时间"""
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

        if obj.TimePlan is None:
            start = ''
            interval = ''
        else:
            schedule = eval(obj.TimePlan)
            start = schedule['start']
            interval = schedule['interval']

        rt = '<span style="color: #0000FF;font-weight: 600">%d个</span>' % num
        rt = '(%s)目标店铺：%s<br>开始时间：%s<br>时间间隔：%s' % (rt, shops, start, interval)
        rt = "%s<br><br><a id='write_plan_id_%s'>修改执行计划</a>" \
             "<script>$('#write_plan_id_%s').on('click',function(){layer.open(" \
             "{type:2,skin:'layui-layer-lan',title:'执行计划',fix:false,shadeClose: true," \
             "maxmin:true,area:['1600px','800px']," \
             "content:'/modify_ebay_schedule/?myId=%s',btn:['关闭页面'],end:function()" \
             "{location.reload();}});});</script>" \
             % (rt, obj.id, obj.id, obj.id)

        state = obj.Status
        if state == 'NO':
            rt = '%s<br><br><p style="color: #FF3333">%s</p>' % (rt, u'未铺货')
        elif state == 'YES':
            rt = '%s<br><br><p style="color: #66FF66">%s</p>' % (rt, u'已铺货')
        else:
            rt = '%s<br><br><p style="color: #FFCC33">%s</p>' % (rt, u'在展开')

        return mark_safe(rt)
    show_schedule.short_description = u'<p align="center"style="color:#428bca;">定时铺货计划</p>'

    def show_info(self, obj):
        """展示时间、人员信息"""
        # if obj.Status == 'OPEN':
        #     st = u'<font color="#FFCC33">正在处理</font>'
        # elif obj.Status == 'YES':
        #     st = u'<font color="#FF3333">已提交</font>'
        # elif obj.Status == 'NO':
        #     st = u'<font color="#00BB00">未提交</font>'
        rt = u'创建人:%s<br>创建时间:<br>%s<br>更新人:%s<br>更新时间:<br>%s<br>上传文件:<br>%s' \
             % (obj.CreateStaff, obj.CreateTime, obj.UpdateStaff, obj.UpdateTime, obj.ExcelFile)
        return mark_safe(rt)
    show_info.short_description = u'<p align="center"style="color:#428bca;">采集信息</p>'

    def ebay_unfold_distribution(self, request, queryset):
        """去铺货"""

        for obj in queryset:
            shop = obj.ShopSets
            if (obj.Status == 'YES') or (obj.Status == 'OPEN'):
                messages.error(request, '铺货ID: %s已铺货或正在展开铺货' % obj.id)
                continue
            elif not shop:
                messages.error(request, '请确认铺货店铺不为空再铺货!')
            else:
                obj.Status = 'OPEN'
                obj.save()

                # ebay_distribution.delay(obj.id, request.user.first_name)
                try:
                    res = eub(obj.id, connection, request.user.first_name)
                except Exception as e:
                    res['code'] = -1
                    res['message'] = repr(e)
            if res['code'] == 0:
                messages.success(request, u'铺货id: %s 铺货成功' % obj.id)
            else:
                messages.error(request, res['message'])

    ebay_unfold_distribution.short_description = u'执行定时铺货'

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_templet_ebay_wait_upload_Admin, self).get_list_queryset()
        id = request.GET.get('id', '')
        Title = request.GET.get('Title', '')
        Site = request.GET.get('Site', '')
        Selleruserid = request.GET.get('Selleruserid', '')
        PayPalEmailAddress = request.GET.get('PayPalEmailAddress', '')

        Status = request.GET.get('Status', '')
        sku = request.GET.get('sku', '')
        code = request.GET.get('code', '')
        CreateStaff = request.GET.get('CreateStaff', '')
        UpdateStaff = request.GET.get('UpdateStaff', '')

        CreateTime_Start = request.GET.get('CreateTime_Start', '')
        CreateTime_End = request.GET.get('CreateTime_End', '')
        UpdateTime_Start = request.GET.get('UpdateTime_Start', '')
        UpdateTime_End = request.GET.get('UpdateTime_End', '')

        # sku查询
        MainSKU_List = []
        if sku:
            for t_product_mainsku_sku_obj in t_product_mainsku_sku.objects.filter(ProductSKU=sku).values('MainSKU'):
                MainSKU_List.append(t_product_mainsku_sku_obj['MainSKU'])

        # 编码查询
        ids = []
        if id:
            ids.append(id)
        if code:
            flag = '0'
            for cs in code.split(','):
                for t_templet_ebay_variations_obj in t_templet_ebay_variations.objects.filter(variationSku=cs).values('templetID'):
                    flag = '1'
                    if t_templet_ebay_variations_obj['templetID'] not in ids:
                        ids.append(t_templet_ebay_variations_obj['templetID'])
            if flag == '0':
                if code not in MainSKU_List:
                    MainSKU_List.append(code)
        searchList = {'id__in': ids, 'Title__contains': Title, 'Site__exact': Site, 'Selleruserid__exact': Selleruserid,
                      'PayPalEmailAddress__exact': PayPalEmailAddress, 'Status__exact': Status, 'sku__in': MainSKU_List,
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
