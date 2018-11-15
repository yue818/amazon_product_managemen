# coding=utf-8

from django.utils.safestring import mark_safe
import oss2
from datetime import datetime
from skuapp.table.t_templet_aliexpress_collection_box import *
from django.contrib import messages
from skuapp.table.t_templet_public_aliexpress import *
from skuapp.table.t_templet_aliexpress_collection_box import *
from pyapp.models import b_goodsskulinkshop
from skuapp.table.t_tort_aliexpress import *
import re

PREFIX = 'http://'
ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
ENDPOINT = 'vpc100-oss-cn-shanghai.aliyuncs.com'
# ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
BUCKETNAME = 'fancyqube-alizip'

class t_templet_aliexpress_collection_box_Admin(object):
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
        rt = '<a href="/show_aliexpress_image/?myId=%s" target="_blank"><img src="%s" style="width:150px;height:150px"></a>' % (obj.id, url)
        return mark_safe(rt)
    show_image.short_description = u'主图'

    def show_code(self, obj):
        rt = ''
        codes = obj.ShopSKU.split(';')
        i = 1
        for code in codes:
            if rt == '':
                rt = '%s,' % code
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
        if obj.Status == 'OPEN':
            st = u'<font color="#FFCC33">正在处理</font>'
        elif obj.Status == 'YES':
            st = u'<font color="#FF3333">已提交</font>'
        elif obj.Status == 'NO':
            st = u'<font color="#00BB00">未提交</font>'
        rt = u'创建人:%s<br>创建时间:<br>%s<br>更新人:%s<br>更新时间:<br>%s<br>提交状态:%s<br>上传文件:<br>%s' \
             % (obj.CreateStaff, obj.CreateTime, obj.UpdateStaff, obj.UpdateTime, st, obj.ZipFile)
        return mark_safe(rt)
    show_info.short_description = u'&nbsp;&nbsp;&nbsp;采 集 信 息&nbsp;&nbsp;&nbsp;'

    def show_warning(self, obj):
        st = self.show_tort(obj)

        if obj.Flag == 100:
            rt = u'<div class="box" style="width: 100px;height: 30px;background-color: #FF3333;text-align: center;line-height: 30px;border-radius: 4px">属性错误</div>'
        else:
            rt = u'<div class="box" style="width: 100px;height: 30px;background-color: #66FF66;text-align: center;line-height: 30px;border-radius: 4px">未发现错误</div>'

        rt = u'%s<br>%s<br><br><a id="link_id_%s">点击修改</a>' % (st, rt, obj.id)
        rt = u"%s<script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
             u"title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','700px']," \
             u"content:'/show_aliexpress_warning/?warning_id=%s',btn:['关闭页面'],end:function()" \
             u"{location.reload();}});});</script>" % (rt, obj.id, obj.id)
        return mark_safe(rt)
    show_warning.short_description = u'自定义属性预警'

    def show_tort(self, obj):
        rt = u'<div class="box" style="width: 100px;height: 30px;background-color: #66FF66;text-align: center;line-height: 30px;border-radius: 4px">非仿品</div>'

        if obj.ShopSKU is None:
            pass
        else:
            shopsku = obj.ShopSKU.split(';')[0]

            sku = ''
            mainsku = ''
            try:
                sku = b_goodsskulinkshop.objects.filter(ShopSKU=shopsku)[0].SKU
                tempList = re.split(r'(\d+)', sku)
                if len(tempList) == 1:
                    mainsku = tempList[0]
                else:
                    mainsku = tempList[0] + tempList[1]

                tort_obj = t_tort_aliexpress.objects.filter(Site='Aliexpress', MainSKU=mainsku)
                if tort_obj.exists():
                    rt = u'<div class="box" style="width: 100px;height: 30px;background-color: #FF3333;text-align: center;line-height: 30px;border-radius: 4px">仿品</div>'
            except:
                pass
        return rt



    list_display = ('id', 'show_warning', 'show_image', 'show_title', 'CoreWords', 'Type', 'Group', 'show_code', 'Price', 'ShippingTemplet', 'Quantity', 'show_info')

    list_display_links = ('id')

    fields = ('ZipFile',)

    list_editable = ('CoreWords',)

    actions = ['to_public_templet']

    def save_models(self):
        obj = self.new_obj
        request = self.request

        user = request.user.username
        time = datetime.now()
        userName = request.user.first_name

        filename = request.user.username + '_' + time.strftime('%Y%m%d%H%M%S') + '.zip'
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME)
        bucket.put_object('%s/%s' % (user, filename), obj.ZipFile)
        url = user + '/' + filename
        t_templet_aliexpress_collection_box.objects.create(OssUrl=url, CreateTime=time, CreateStaff=userName,Flag=1,
                                                           UpdateTime=time, UpdateStaff=userName, Status='OPEN',
                                                           ZipFile=obj.ZipFile)

    def to_public_templet(self, request, queryset):
        time = datetime.now()
        user = request.user.first_name
        for obj in queryset:
            if obj.Status == 'YES':
                messages.error(request, u'ID是%s已经提交为公共模板，请勿重复提交！' % obj.id)
            elif obj.Flag == 100:
                messages.error(request, u'ID是%s的商品自定义属性错误，请修改后提交！' % obj.id)
            else:
                public_aliexpress_obj = t_templet_public_aliexpress()
                public_aliexpress_obj.__dict__ = obj.__dict__
                public_aliexpress_obj.CreateTime = time
                public_aliexpress_obj.CreateStaffName = user
                public_aliexpress_obj.UpdateTime = time
                public_aliexpress_obj.UpdateStaff = user
                public_aliexpress_obj.Status = ''
                public_aliexpress_obj.save()
                obj.Status = 'YES'
                # obj.Flag = 0
                obj.save()
    to_public_templet.short_description = u'转为公共模板'


    def get_list_queryset(self,):
        request = self.request
        qs = super(t_templet_aliexpress_collection_box_Admin, self).get_list_queryset()
        qs = qs.exclude(Flag=0)
        # if request.user.is_superuser:
        #     qs = qs
        # else:
        # qs = qs.filter(CreateStaff = request.user.first_name).exclude(Flag=0)
        return qs