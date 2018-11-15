# coding=utf-8
from django.utils.safestring import mark_safe
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect

class t_templet_aliexpress_wait_upload_Admin(object):
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
        st = ''
        if obj.Status == 'WAIT':
            st = u'正在处理'
        elif obj.Status == 'OK':
            st = u'已提交'
        elif obj.Status == 'NO':
            st = u'未提交'
        elif obj.Status == 'ERROR':
            st = u'数据错误'
        rt = u'创建人:%s<br>创建时间:<br>%s<br>更新人:%s<br>更新时间:<br>%s<br>提交状态:<br>%s<br>上传文件:<br>%s' \
             % (obj.CreateStaff, obj.CreateTime, obj.UpdateStaff, obj.UpdateTime, st, obj.ZipFile)
        return mark_safe(rt)
    show_info.short_description = u'&nbsp;&nbsp;&nbsp;采 集 信 息&nbsp;&nbsp;&nbsp;'

    list_display = ('id', 'ProductID', 'show_image', 'show_title', 'CoreWords', 'Type', 'Group', 'show_code', 'ShopName','Price', 'ShippingTemplet', 'Quantity', 'show_info')

    list_editable = ('ShopName',)

    actions = ['to_distribution','to_make_shopname']

    def to_distribution(self, request, queryset):
        time = datetime.now()
        user = request.user.first_name
        for obj in queryset:
            if obj.Status == 'OK':
                messages.error(request, u'ID是%s已经提交压缩，请勿重复提交！' % obj.id)
            elif (obj.ShopName == None) or (obj.ShopName == ''):
                messages.error(request, u'ID是%s店铺名不能为空，请核对后提交！' % obj.id)
            else:
                obj.Status = 'WAIT'
                obj.UpdateTime = time
                obj.UpdateStaff = user
                obj.save()

    to_distribution.short_description = u'生成压缩文件'
    
    def to_make_shopname(self, request, objs):
        time = datetime.now()
        user = request.user.first_name
        idList = []
        cateidlist = []
        for obj in objs:
            idList.append(str(obj.id))
            cateidlist.append(obj.Type)
        if len(set(cateidlist)) >= 2:
            messages.error(request,u'选中的商品类型不一致请重新选择。。。')
        else:
            return HttpResponseRedirect('/make_shopname/?myId=%s&cate=%s' % ('|'.join(idList),cateidlist[0]))
            
    to_make_shopname.short_description = u'填写铺货店铺'
    
    
    
    
    
    
    
    
    
    
    
    