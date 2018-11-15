# coding=utf-8
from django.utils.safestring import mark_safe
from datetime import datetime
from django.contrib import messages
from skuapp.table.t_templet_aliexpress_wait_upload import *
from skuapp.table.t_aliexpress_categories_code import *

class t_templet_public_aliexpress_Admin(object):
    plateform_distribution_navigation = True
    def show_image(self, obj):
        str = 'http://fancyqube-alipic.oss-cn-shanghai.aliyuncs.com/'
        if obj.Images is None:
            url = ''
        else:
            if '|' not in obj.Images:
                url = str + obj.Images.split(',')[0]
            else:
                image = obj.Images.split('|')[0]
                if ',' in image:
                    url = str + image.split(',')[0]
                else:
                    url = str + image
        rt = '<img src="%s" style="width: 150px;height: 150px">' % url
        return mark_safe(rt)

    show_image.short_description = u'主图'

    def show_code(self, obj):
        rt = ''
        codes = obj.ShopSKU.split(';')
        i = 1
        for code in codes:
            if rt == '':
                rt = '%s' % code
            else:
                if i%3 == 0:
                    rt = '%s,%s,<br>' % (rt, code)
                else:
                    rt = '%s%s' % (rt, code)
            i += 1
        return mark_safe(rt)
    show_code.short_description = u'商品编码'

    def show_title(self, obj):
        l = obj.Name.split(' ')
        aa = len(l)
        ll = ''
        rt = ''
        if aa <= 6:
            rt = u'%s%s' % (rt, obj.Name)
        elif aa > 6:
            newe_Title_list = []
            for i in range(0, len(l), 6):
                min_list = ''
                for a in l[i:i + 6]:
                    min_list = u'%s%s ' % (min_list, a)
                newe_Title_list.append(min_list)
            for newe_Title in newe_Title_list:
                ll = u'%s%s<br>' % (ll, newe_Title)
            rt = u'%s%s' % (rt, ll)
            return mark_safe(rt)
    show_title.short_description = u'标题'

    def show_info(self, obj):
        """展示时间、人员信息"""
        # if obj.Status == 'OPEN':
        #     st = u'<font color="#FFCC33">正在处理</font>'
        # elif obj.Status == 'YES':
        #     st = u'<font color="#FF3333">已提交</font>'
        # elif obj.Status == 'NO':
        #     st = u'<font color="#00BB00">未提交</font>'
        rt = u'创建人:%s<br>创建时间:<br>%s<br>更新人:%s<br>更新时间:<br>%s<br>上传文件:<br>%s' \
             % (obj.CreateStaff, obj.CreateTime, obj.UpdateStaff, obj.UpdateTime, obj.ZipFile)
        return mark_safe(rt)

    show_info.short_description = u'&nbsp;&nbsp;&nbsp; 模 板 信 息&nbsp;&nbsp;&nbsp;'

    list_display = ('id', 'ProductID', 'show_image', 'show_title', 'CoreWords', 'Type', 'Group', 'show_code', 'Price', 'ShippingTemplet', 'Quantity', 'show_info')

    actions = ['to_wait_upload']

    def get_shopname(self,param):
        """预生成目标店铺"""
        categories_code_obj = t_aliexpress_categories_code.objects.filter(GroupCode=param)
        result = ''
        if categories_code_obj.exists():
            shopname = categories_code_obj[0].ShopName
            current_shopnum = str(int(shopname.split('Ali-')[-1]))

            product_cate = categories_code_obj[0].ProductCate
            product_cate_objs = t_aliexpress_categories_code.objects.filter(ProductCate=product_cate)
            all_shopname = []

            if product_cate_objs.exists():
                for product_cate_obj in product_cate_objs:
                    temp_name = product_cate_obj.ShopName.split('Ali-')[-1]
                    all_shopname.append(str(int(temp_name)))

            if current_shopnum in all_shopname:
                all_shopname.remove(current_shopnum)
            result = ','.join(all_shopname)
        return result


    def to_wait_upload(self, request, queryset):
        time = datetime.now()
        user = request.user.first_name
        for obj in queryset:
            if obj.Status == 'YES':
                messages.error(request, u'ID是%s已经提交为公共模板，请勿重复提交！' % obj.id)
            else:
                wait_upload_obj = t_templet_aliexpress_wait_upload()
                wait_upload_obj.__dict__ = obj.__dict__
                wait_upload_obj.CreateTime = time
                wait_upload_obj.CreateStaffName = user
                wait_upload_obj.UpdateTime = time
                wait_upload_obj.UpdateStaff = user
                wait_upload_obj.Status = 'NO'
                wait_upload_obj.ShopName = self.get_shopname(obj.Group)
                wait_upload_obj.save()
                obj.Status = 'YES'
                obj.Flag = 0
                obj.save()
    to_wait_upload.short_description = u'转为待铺货'