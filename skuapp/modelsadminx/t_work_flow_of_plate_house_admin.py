#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_work_flow_of_plate_house_admin.py
 @time: 2018/6/12 19:47
"""
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from Project.settings import *
from datetime import datetime, timedelta
import os, oss2
from django.contrib import messages
from django.db import connection
from django_redis import get_redis_connection
connRedis = get_redis_connection(alias='product')
# from Project.settings import connRedis
from django.contrib.auth.models import User
from storeapp.models import t_online_info_wish_store
from skuapp.table.t_product_enter_ed import t_product_enter_ed
from pyapp.models import b_goods as py_b_goods
from brick.spider.get import readAliexpress
from brick.classredis.classmainsku import classmainsku
from brick.classredis.classsku import classsku
from brick.public.create_dir import mkdir_p
from skuapp.table.t_supply_chain_production_basic_permission import t_supply_chain_production_basic_permission

classmainsku_obj = classmainsku(db_cnxn=connection)
classsku_obj = classsku(db_cnxn=connection)

def get_price_weight_pylink_by_mainsku(mainsku):
    price = None
    weight = None
    py_link = None
    purchaser = None
    sizelist = []
    skulist = classmainsku_obj.get_sku_by_mainsku(mainsku)
    if skulist:
        for sku in skulist:
            price = classsku_obj.get_price_by_sku(sku)
            weight = classsku_obj.get_weight_by_sku(sku)
            if price or weight:
                break

        sizelist = [s.split('-')[-1] for s in skulist]

        py_objs = py_b_goods.objects.filter(SKU__in=skulist, Used=0, GoodsStatus__in=[u'正常',u'在售'])
        for py_obj in py_objs:
            py_link = py_obj.LinkUrl
            purchaser = py_obj.Purchaser

            if py_link or purchaser:
                break

    return price, weight, py_link,  ','.join(sorted(set(sizelist))), purchaser


class t_work_flow_of_plate_house_admin(object):
    search_box_flag = True
    show_prompt_develop = True
    downloadxls = True
    t_supply_chain_production_basic_flag=True
    progress_tracking_plugin = True
    def show_Image(self,obj) :
        url =u'%s'%(obj.image)
        rt = '<img src="%s" width="150" height="150" alt = "%s" title="%s">' \
             '</img>'%(url,url,url)
        return mark_safe(rt)
    show_Image.short_description = u'图片'

    def show_Link(self,obj) :
        rt = u'反向链接：<a title="%s" href="%s" target="_blank">%s...</a>' % (obj.urllink,self.del_None(obj.urllink), self.del_None(obj.urllink)[:20])
        rt = u'%s</br>1688链接：<a title="%s" href="%s" target="_blank">%s...</a>' % (rt, obj.linkali,self.del_None(obj.linkali), self.del_None(obj.linkali)[:20])
        return mark_safe(rt)
    show_Link.short_description = u'链接'

    def show_time(self,obj) :
        rt = u'需求提交时间：%s' % obj.submittime

        if obj.proflag == '1':
            rt = u'%s</br><span style="color:red">确定面辅料完成时间：%s</span>' % (rt, obj.determinetime)
        else:
            rt = u'%s</br>确定面辅料完成时间：%s' % (rt, obj.determinetime)
        if obj.proflag == '2':
            rt = u'%s</br><span style="color:red">纸样样衣完成时间：%s</span>' % (rt, obj.patterntime)
        else:
            rt = u'%s</br>纸样样衣完成时间：%s' % (rt, obj.patterntime)
        if obj.proflag == '3':
            rt = u'%s</br><span style="color:red">审核样衣完成时间：%s</span>' % (rt, obj.examinetime)
        else:
            rt = u'%s</br>审核样衣完成时间：%s' % (rt, obj.examinetime)
        if obj.proflag == '4':
            rt = u'%s</br><span style="color:red">报价完成时间：%s</span>' % (rt, obj.checktime)
        else:
            rt = u'%s</br>报价完成时间：%s' % (rt, obj.checktime)
        if obj.proflag == '5':
            rt = u'%s</br><span style="color:red">跟单领取时间：%s</span>' % (rt, obj.documentarytime)
        else:
            rt = u'%s</br>跟单领取时间：%s' % (rt, obj.documentarytime)
        if obj.proflag == '6':
            rt = u'%s</br><span style="color:red">发货完成时间：%s</span>' % (rt, obj.ok_time)
        else:
            rt = u'%s</br>最终完成时间：%s' % (rt, obj.ok_time)

        return mark_safe(rt)
    show_time.short_description = u'操作时间信息'

    def show_warning(self,obj) :
        rt = u'<div style="background:green;color:white">正在进行中</div>'
        if obj.proflag == '1' and (obj.submittime + timedelta(days=2)).strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
            rt = u'<div style="background:red;color:white">确定面辅料-超时</div>'
        elif obj.proflag == '2' and (obj.determinetime + timedelta(days=3)).strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
            rt = u'<div style="background:red;color:white">纸样样衣-超时</div>'
        elif obj.proflag == '3' and (obj.patterntime + timedelta(days=0)).strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
            rt = u'<div style="background:red;color:white">审核样衣-超时</div>'
        elif obj.proflag == '4' and (obj.examinetime + timedelta(days=0)).strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
            rt = u'<div style="background:red;color:white">报价-超时</div>'
        elif obj.proflag == '5' and (obj.checktime + timedelta(days=0)).strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
            rt = u'<div style="background:red;color:white">跟单领取-超时</div>'
        elif obj.proflag == '6' and (obj.documentarytime + timedelta(days=7)).strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
            rt = u'<div style="background:red;color:white">发货完成-超时</div>'
        elif obj.proflag == '7':
            rt = u'<div style="background:green;color:white">完成</div>'

        return mark_safe(rt)
    show_warning.short_description = u'超时告警'

    def del_None(self,col):
        rt = col
        if not col:
            rt = ''
        return rt

    def show_infors(self,obj) :
        read = '' if self.request.user.is_superuser or (obj.proflag < '7' and self.request.user.first_name == ('{}'.format(obj.checkman)).strip()) \
            else 'readonly'

        rt = '<table>'
        rt = u'%s<tr><th>供应链成本：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
             u'<tr><th>供应链克重：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt,self.del_None(obj.price),obj.id,'price',read,self.del_None(obj.price),str(obj.id)+'_price',
              self.del_None(obj.weight),obj.id,'weight',read,self.del_None(obj.weight),str(obj.id)+'_weight',)

        rt = u'%s<tr><th>面料数量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt,self.del_None(obj.num),obj.id,'num',read,self.del_None(obj.num),str(obj.id)+'_num')

        rt = u'%s<tr><th>剪版费用：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.shearplate), obj.id, 'shearplate', read, self.del_None(obj.shearplate), str(obj.id) + '_shearplate')
        rt = u'%s<tr><th>报价备注：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.priceremark), obj.id, 'priceremark', read, self.del_None(obj.priceremark), str(obj.id) + '_priceremark')

        rt = rt + '</table>'

        return mark_safe(rt)
    show_infors.short_description = u'报价信息'

    def show_needsinfors(self,obj) :
        read = '' if obj.proflag < '7' and (self.request.user.is_superuser or self.request.user.first_name == ('{}'.format(obj.submiter)).strip()) \
            else 'readonly'

        rt = '<table>'
        rt = u'%s<tr><th>1688成本：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
             u'<tr><th>1688克重：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt,self.del_None(obj.aliprice),obj.id,'aliprice',read,self.del_None(obj.aliprice),str(obj.id)+'_aliprice',
              self.del_None(obj.aliweight),obj.id,'aliweight',read,self.del_None(obj.aliweight),str(obj.id)+'_aliweight')

        rt = u'%s<tr><th>正常售价：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt,self.del_None(obj.normalprice),obj.id,'normalprice',read,self.del_None(obj.normalprice),str(obj.id)+'_normalprice')

        rt = u'%s<tr><th>需要颜色：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr>' \
             u'<tr><th>卖点或配件：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr>' % \
             (rt,self.del_None(obj.color),obj.id,'color',read,self.del_None(obj.color),str(obj.id)+'_color',
              self.del_None(obj.keynote),obj.id,'keynote',read,self.del_None(obj.keynote),str(obj.id)+'_keynote')

        rt = u'%s<tr><th>需求备注：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.subreamrk), obj.id, 'subreamrk', read,self.del_None(obj.subreamrk), str(obj.id) + '_subreamrk')

        rt = u'%s<tr><th>普元尺码号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.pysize), obj.id, 'pysize', read,self.del_None(obj.pysize), str(obj.id) + '_pysize')

        rt = u'%s<tr><th>套用版本：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.paraphrase_version), obj.id, 'paraphrase_version', read, self.del_None(obj.paraphrase_version), str(obj.id) + '_paraphrase_version')

        rt = rt + '</table>'

        return mark_safe(rt)
    show_needsinfors.short_description = u'需求信息'

    def show_maninfors(self,obj) :
        userID = [each.id for each in User.objects.filter(groups__id__in=[56])]

        read, read2, read3 = 'readonly', 'readonly', 'readonly'
        if self.request.user.is_superuser or  (obj.proflag < '6' and self.request.user.id in userID):
            read = ''

        if self.request.user.is_superuser or (obj.proflag < '7' and (self.request.user.id in userID
            or self.request.user.first_name == ('{}'.format(obj.merchandiser)).strip())):
            read2 = ''

        if self.request.user.is_superuser or (obj.proflag < '6' and (self.request.user.id in userID
            or self.request.user.first_name == ('{}'.format(obj.checkman)).strip())):
            read3 = ''

        rt = '<table>'
        rt = u'%s<tr><th>采购员：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.cgperson), obj.id, 'cgperson', 'readonly', self.del_None(obj.cgperson),str(obj.id) + '_cgperson')

        rt = u'%s<tr><th>需求提交人：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.submiter), obj.id, 'submiter', 'readonly', self.del_None(obj.submiter), str(obj.id) + '_submiter')

        rt = u'%s<tr><th>核价员：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th> </tr>' \
             u'<tr><th>纸样师：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt,self.del_None(obj.checkman),obj.id,'checkman',read,self.del_None(obj.checkman),str(obj.id)+'_checkman',
              self.del_None(obj.patternman),obj.id,'patternman',read,self.del_None(obj.patternman),str(obj.id)+'_patternman')

        rt = u'%s<tr><th>跟单员：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt,self.del_None(obj.merchandiser),obj.id,'merchandiser',read3,self.del_None(obj.merchandiser),str(obj.id)+'_merchandiser')

        rt = u'%s<tr><th>发货信息：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'0\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.shippinginformation), obj.id, 'shippinginformation', read2, self.del_None(obj.shippinginformation),str(obj.id) + '_shippinginformation')

        rt = rt + '</table>'

        return mark_safe(rt)
    show_maninfors.short_description = u'人员信息'

    def show_manage(self, obj):
        request=self.request
        user=request.user.username
        if t_supply_chain_production_basic_permission.objects.filter(username=user).exists() or request.user.is_superuser:
            button_dis=''
        else:
            button_dis='disabled="disabled"'
        script="""function button_click(objid) {
                    $.get('t_work_flow_of_plate_house_button_click/?id='+objid,function (data,status) {
                        let flag=data.flag;
                        let msg='';
                        let response_msg=data.msg;
                        if (flag===1){
                            openmodel(response_msg,1);
                        }else if (flag===2){
                            console.log(response_msg);
                            openmodel(response_msg,2);
                        }else{
                            msg='供应链款基础资料增加失败!'
                            let errmsg=data.errmsg;
                            alert(msg+errmsg)
                        }
                        
                    })
        
    }"""
        rt = u'主SKU:%s<br/><br/>' % obj.mainsku
        rt = "%s<a id=translation_%s>转服装定做</a></br></br><button id='button_%s' %s type='button' onclick='button_click(%s)'>转基础资料</button>" \
             "<script>$('#translation_%s').on('click',function()" \
             "{layer.open({type:2,skin:'layui-layer-lan',title:'转服装定做',fix:false,shadeClose: true,maxmin:true,area:['420px','250px']," \
             '''content:"/t_work_flow/selectSKU/?id=%s&mainsku=%s",});});''' \
             "%s</script>" % (rt, obj.id,obj.id,button_dis,obj.id,obj.id, obj.id, obj.mainsku,script)


        return mark_safe(rt)

    show_manage.short_description = u'主SKU/操作'

    list_display = ('id','show_Image','show_manage','show_needsinfors','show_infors','show_maninfors','show_warning','show_time','show_Link')
    # search_fields = ('id','image','keynote','color','mainsku','price','weight','num','submiter','checkman',
    #                  'patternman','examineman','merchandiser','urllink','linkali')
    # list_filter = ('submittime','checktime','patterntime','examinetime','documentarytime')
    list_editable = ('keynote','color','price','weight','num',)

    fields = ('mainsku','urllink','keynote','color','normalprice','image')

    form_layout = (
        Fieldset(u'需求信息填写',
                 Row('urllink','normalprice', 'image'),
                 Row('mainsku','color', 'keynote'),
                 css_class='unsort '
                 ),
        )


    actions = ['to_check', 'to_pattern', 'to_examine','to_offer','to_merchand', 'to_excel', 'to_ok']

    def to_check(self, request, objs): # 纸样师
        for obj in objs.filter(proflag='1'):
            if not (obj.patternman and obj.patternman != request.user.first_name):
                obj.patternman = request.user.first_name
                obj.determinetime = datetime.now()
                obj.proflag = '2'
                obj.save()

    to_check.short_description = u'确定面辅料完成'

    def to_pattern(self, request, objs): # 纸样师
        for obj in objs.filter(proflag='2', patternman= request.user.first_name):
            obj.patterntime = datetime.now()
            obj.proflag = '3'
            obj.save()

    to_pattern.short_description = u'纸样样衣完成'

    def to_examine(self, request, objs): # 核价员
        for obj in objs.filter(proflag='3'):
            if not (obj.checkman and obj.checkman != request.user.first_name):
                obj.checkman = request.user.first_name
                obj.examinetime = datetime.now()
                obj.proflag = '4'
                obj.save()

    to_examine.short_description = u'审核样衣完成'

    def to_offer(self, request, objs): # 核价员
        for obj in objs.filter(proflag='4', checkman=request.user.first_name):
            obj.checktime = datetime.now()
            obj.proflag = '5'
            obj.save()

    to_offer.short_description = u'报价完成'

    def to_merchand(self, request, objs): # 跟单员
        for obj in objs.filter(proflag='5'):
            if not (obj.merchandiser and obj.merchandiser != request.user.first_name):
                obj.merchandiser = request.user.first_name
                obj.documentarytime = datetime.now()
                obj.proflag = '6'
                obj.save()

    to_merchand.short_description = u'跟单领取'

    def to_ok(self, request, objs): # 跟单员
        for obj in objs.filter(proflag='6',merchandiser=request.user.first_name):
            obj.ok_time = datetime.now()
            obj.proflag = '7'
            obj.save()

    to_ok.short_description = u'发货完成'

    def to_excel(self, request, queryset):
        from xlwt import *

        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('sku')

        FIELDS = [
            u'需求提交时间', u'主SKU', u'核价员', u'剪版费用', u'备注', u'正常售价',
            u'跟单员', u'供应链成本', u'供应链克重', u'纸样师', u'纸样样衣完成时间',
            u'报价完成时间', u'跟单领取时间', u'发货信息', u'套用版本'
        ]

        for index, item in enumerate(FIELDS):
            sheet.write(0, index, item)

        # 写数据
        row = 0

        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row, column, u'{}'.format(qs.submittime))  # A 需求提交时间

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.mainsku))  # B 主SKU

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.checkman))  # C 核价员

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.shearplate))  # D 剪版费用

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.priceremark))  # E 备注

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.normalprice))  # F 正常售价

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.merchandiser))  # G 跟单员

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.aliprice))  # H 供应链成本

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.aliweight))  # I 供应链克重

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.patternman))  # J 纸样师

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.patterntime))  # K 纸样样衣完成时间

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.checktime))  # L 报价完成时间

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.documentarytime))  # M 跟单领取完成时间

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.shippinginformation))  # N 发货信息

            column = column + 1
            sheet.write(row, column, u'{}'.format(qs.paraphrase_version))  # O 套用版本

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,
                                               prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))

        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                    filename) + u':成功导出,可点击Download下载到本地............................。')

    to_excel.short_description = u'导出EXCEL'

    def save_models(self):
        obj = self.new_obj
        old_obj = None
        if obj is None or obj.id is None or obj.id <=0:
            pass
        else:
            old_obj = self.model.objects.get(pk=obj.pk)

        try:
            obj.save()

            if obj.mainsku:
                obj.aliprice, obj.aliweight, obj.linkali, obj.pysize, obj.cgperson = get_price_weight_pylink_by_mainsku(obj.mainsku)

            if not obj.linkali:
                linkali_list = t_product_enter_ed.objects.filter(MainSKU=obj.mainsku).values_list('SupplierPUrl1',flat=True)
                for linkali in linkali_list:
                    if linkali:
                        obj.linkali = linkali
                        break

            obj.submiter = self.request.user.first_name
            obj.submittime = datetime.now()
            obj.proflag = '1'
            obj.save()
        except Exception, e:
            messages.error(self.request, u'%s:%s' % (Exception, e))


    def get_list_queryset(self,):
        request = self.request
        qs = super(t_work_flow_of_plate_house_admin, self).get_list_queryset()

        seachdict = {}

        mainsku = request.GET.get('mainsku')
        if mainsku:
            seachdict['mainsku'] = mainsku

        proflag = request.GET.get('proflag')
        if proflag == '7':
            seachdict['proflag'] = proflag
        if proflag == '-1':
            seachdict['proflag__in'] = ['1', '2', '3', '4', '5','6']

        proflagtmp = request.GET.get('proflagtmp')
        if proflagtmp and not seachdict.has_key('proflag'):
            seachdict['proflag'] = proflagtmp

        submiter = request.GET.get('submiter')
        if submiter:
            seachdict['submiter'] = submiter

        id = request.GET.get('id')
        if id:
            seachdict['id'] = id

        checkman = request.GET.get('checkman')
        if checkman:
            seachdict['checkman'] = checkman

        patternman = request.GET.get('patternman')
        if patternman:
            seachdict['patternman'] = patternman

        merchandiser = request.GET.get('merchandiser')
        if merchandiser:
            seachdict['merchandiser'] = merchandiser

        submittimeStart = request.GET.get('submittimeStart')
        if submittimeStart:
            seachdict['submittime__gte'] = submittimeStart

        submittimeEnd = request.GET.get('submittimeEnd')
        if submittimeEnd:
            seachdict['submittime__lt'] = submittimeEnd

        determinetimeStart = request.GET.get('determinetimeStart')
        if determinetimeStart:
            seachdict['determinetime__lt'] = determinetimeStart

        determinetimeEnd = request.GET.get('determinetimeEnd')
        if determinetimeEnd:
            seachdict['determinetime__lt'] = determinetimeEnd

        checktimeStart = request.GET.get('checktimeStart')
        if checktimeStart:
            seachdict['checktime__gte'] = checktimeStart

        checktimeEnd = request.GET.get('checktimeEnd')
        if checktimeEnd:
            seachdict['checktime__lt'] = checktimeEnd

        patterntimeStart = request.GET.get('patterntimeStart')
        if patterntimeStart:
            seachdict['patterntime__gte'] = patterntimeStart

        patterntimeEnd = request.GET.get('patterntimeEnd')
        if patterntimeEnd:
            seachdict['patterntime__lt'] = patterntimeEnd

        examinetimeStart = request.GET.get('examinetimeStart')
        if examinetimeStart:
            seachdict['examinetime__gte'] = examinetimeStart

        examinetimeEnd = request.GET.get('examinetimeEnd')
        if examinetimeEnd:
            seachdict['examinetime__lt'] = examinetimeEnd

        documentarytimeStart = request.GET.get('documentarytimeStart')
        if documentarytimeStart:
            seachdict['documentarytime__gte'] = documentarytimeStart

        documentarytimeEnd = request.GET.get('documentarytimeEnd')
        if documentarytimeEnd:
            seachdict['documentarytime__lt'] = documentarytimeEnd

        if seachdict:
            try:
                qs = qs.filter(**seachdict)
            except Exception, e:
                messages.error(request, u'%s:%s' % (Exception, e))

        return qs




















