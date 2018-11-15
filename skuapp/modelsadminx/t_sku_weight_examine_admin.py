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
# import oss2
from django.contrib import messages
from django.db import connection
from brick.pydata.py_redis.py_SynRedis_tables import py_SynRedis_tables

from skuapp.table.t_product_information_modify import t_product_information_modify
from django.db import transaction

from xlwt import *
import os
import oss2
import re
from Project.settings import MEDIA_ROOT, ACCESS_KEY_ID, ACCESS_KEY_SECRET, ENDPOINT, ENDPOINT_OUT, BUCKETNAME_XLS
from brick.public.create_dir import mkdir_p
from brick.table.t_large_small_corresponding_cate import t_large_small_corresponding_cate

from pyapp.models import b_goods as py_b_goods
# from django_redis import get_redis_connection
# connRedis = get_redis_connection(alias='product')
# # from Project.settings import connRedis
#
# from storeapp.models import t_online_info_wish_store
# from skuapp.table.t_product_enter_ed import t_product_enter_ed
# from pyapp.models import b_goods as py_b_goods
# from brick.spider.get import readAliexpress
# from brick.classredis.classmainsku import classmainsku
# from brick.classredis.classsku import classsku
#
# classmainsku_obj = classmainsku(connection,connRedis)
# classsku_obj = classsku(connection,connRedis)
#
py_SynRedis_tables_obj = py_SynRedis_tables()
t_large_small_corresponding_cate_obj = t_large_small_corresponding_cate(connection)

def sku_attr(product_sku):
    try:
        cursor = connection.cursor()
        sql = "SELECT  a.VDesc, b.LocationName FROM (SELECT V, VDesc FROM t_sys_param WHERE Type = 316) a, " \
              "(SELECT LocationName,StoreID FROM py_db.kc_currentstock_sku WHERE SKU = %s) b " \
              "WHERE a.V = b.StoreID"
        cursor.execute(sql, (product_sku,))
        infors = cursor.fetchall()
        cursor.close()
        infor_list = None
        if len(infors) > 1:
            for infor in infors:
                if infor[-1] == u'浦江仓库':
                    infor_list=infor
                    break
            if not infor_list:
                infor_list = infors[0]
        elif len(infors) == 1:
            infor_list = infors[0]
        return {'errorcode': 1,'infor': infor_list}
    except Exception as e:
        return {'errorcode': -1,'errortext': u'%s' % e}


class t_sku_weight_examine_admin(object):
    search_box_flag = True
    show_prompt_develop = True
    downloadxls = True

    def show_Image(self,obj) :
        url =u'%s'%(obj.product_image)
        rt = '<img src="%s" width="110" height="110">' \
             '</img>'%(url,)
        return mark_safe(rt)
    show_Image.short_description = u'商品图片'

    def show_sku_attr(self,obj):
        if obj.examine_status == '0':  # 未完成的 会去 查询
            # infor = [{'SKU': obj.product_sku, 'SKUKEY': ['Number', 'ReservationNum']}]
            # sInfors = py_SynRedis_tables_obj.BatchReadRedis(infor)
            # # raise Exception(sInfors)
            # Number = 0
            # if sInfors[0]['SKUKEY'][0]:
            #     Number = int(sInfors[0]['SKUKEY'][0])
            # ReservationNum = 0
            # if sInfors[0]['SKUKEY'][1]:
            #     ReservationNum = int(sInfors[0]['SKUKEY'][1])
            # CanUseNum = Number - ReservationNum
            #
            # if obj.canuse_num != CanUseNum:  #  不知道会不会挂掉
            #     obj.canuse_num = CanUseNum
            #     obj.save()

            sResult = sku_attr(obj.product_sku)
            rt = ''
            if sResult['errorcode'] == 1 and sResult['infor']:
                rt = u'仓库：%s <br> 库位：%s' % (sResult['infor'][0], sResult['infor'][1])
            elif sResult['errorcode'] == -1:
                rt = u'库位查询错误：%s' % sResult['errortext']

            rt = rt + u'<br> 可用数量：%s' % obj.canuse_num
        else:
            rt = u'<div style="background:green;color:white">已完成</div>'

        return mark_safe(rt)
    show_sku_attr.short_description = u'库/位/可用数量'

    def show_name(self,obj) :
        rt =u'商品名称：%s' % obj.product_name
        rt = rt + u'<br>供应商名称：%s' % obj.supplier_name
        rt = rt + u'<br>大类名称：%s' % self.del_None(obj.product_lcate)
        rt = rt + u'<br>小类代码：%s' % self.del_None(obj.product_scate)
        return mark_safe(rt)
    show_name.short_description = u'名称信息'

    def del_None(self,col):
        rt = col
        if not col:
            rt = ''
        return rt

    def show_infors(self,obj) :
        read = ''
        show_text = u'style="color: red;"> <- 请输入产品测量裸重'
        if obj.examine_status == '1':
            read = 'readonly'
            show_text = u'style="color: green;">'
        rt = '<table>'
        rt = u'%s<tr><th>价格：</th><th><input value="%s" type="text" %s title="%s"/></th></tr> ' % \
             (rt, self.del_None(obj.product_price), 'readonly', self.del_None(obj.product_price))
        rt = u'%s<tr><th>调研克重(g)：</th><th><input value="%s" type="text" %s title="%s"/></th></tr> ' % \
             (rt, self.del_None(obj.survey_weight), 'readonly', self.del_None(obj.survey_weight))
        rt = u'%s<tr><th>包装克重(g)：</th><th><input value="%s" type="text" %s title="%s"/></th></tr> ' % \
             (rt, self.del_None(obj.packinfo_weight), 'readonly', self.del_None(obj.packinfo_weight))
        rt = u'%s<tr><th>测量克重(g)：</th><th><input value="" type="text" %s title="请输入产品测量裸重" ' \
             u'onchange="to_change_weight(\'%s\',\'%s\',this.value,\'t_sku_weight_examine\',\'%s\')"/></th>' \
             u'<th><span %s</span></th></tr> ' % \
             (rt, read,obj.id,'examine_weight',obj.packinfo_weight,show_text)
        rt = u'%s<tr><th>真实克重(g)：</th><th><input value="%s" type="text" %s title="%s" id="%s"/></th><th><span id="%s"></span></th></tr> ' % \
             (rt,self.del_None(obj.examine_weight),'readonly',self.del_None(obj.examine_weight),str(obj.id),str(obj.id) + '_examine_weight')

        rt = rt + '</table>'

        return mark_safe(rt)
    show_infors.short_description = u'价格/克重信息'

    def show_person_time(self,obj) :
        rt = u'审核申请人：%s' % obj.create_person
        rt = rt + u'<br>审核申请时间：%s' % obj.create_time
        rt = rt + u'<br>审核人：%s' % obj.auditor
        rt = rt + u'<br>审核时间：%s' % obj.examine_time
        return mark_safe(rt)
    show_person_time.short_description = u'操作人/时间信息'


    list_display = ('id','show_Image','show_name','product_sku','show_sku_attr','show_infors','examine_status','show_person_time',)
    list_editable = ('examine_weight',)

    fields = ('product_mainsku',)



    actions = ['to_excel','to_check']

    def to_excel(self, request, objs):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        # if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet(u'克重审核')

        XLS_FIELDS = [u'商品SKU',u'仓库',u'库位',u'可用数量',u'调研克重',u'真实克重']

        for index, item in enumerate(XLS_FIELDS):
            sheet.write(0, index, item)

        # 写数据
        row = 0
        for obj in objs:
            row = row + 1
            column = 0
            sheet.write(row, column, obj.product_sku)  # A 商品SKU

            sResult = sku_attr(obj.product_sku)
            if sResult['errorcode'] == 1 and sResult.get('infor'):
                column = column + 1
                sheet.write(row, column, sResult.get('infor')[0])  # B 仓库

                column = column + 1
                sheet.write(row, column, sResult.get('infor')[1])  # C 库位
            else:
                column = column + 1
                # sheet.write(row, column, ck)  # B 仓库

                column = column + 1
                # sheet.write(row, column, kw)  # C 库位

            infor = [{'SKU': obj.product_sku, 'SKUKEY': ['Number', 'ReservationNum']}]
            sInfors = py_SynRedis_tables_obj.BatchReadRedis(infor)
            Number = 0
            if sInfors[0]['SKUKEY'][0]:
                Number = int(sInfors[0]['SKUKEY'][0])
            ReservationNum = 0
            if sInfors[0]['SKUKEY'][1]:
                ReservationNum = int(sInfors[0]['SKUKEY'][1])
            CanUseNum = Number - ReservationNum

            column = column + 1
            sheet.write(row, column, CanUseNum)  # D 可用数量

            column = column + 1
            sheet.write(row, column, obj.survey_weight)  # E 调研克重

            column = column + 1
            sheet.write(row, column, obj.examine_weight)  # F 真实克重


        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))

        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。')

    to_excel.short_description = u'导出表格'

    def to_check(self, request, objs):
        try:
            insertinto = []
            transaction.set_autocommit(False)
            for obj in objs.filter(examine_status='0',examine_weight__isnull=False).exclude(examine_weight=0):
                obj.auditor = request.user.first_name
                obj.examine_time = datetime.now()
                obj.examine_status = '1'
                obj.canuse_num = None

                slist = re.findall(r'[0-9]+|[a-z-]+|[A-Z-|]+', '{}'.format(obj.product_sku))
                if len(slist) >= 2:
                    bemainsku = '%s%s' % (slist[0], slist[1])
                else:
                    bemainsku = ''.join(slist)

                details = {}
                details[obj.product_sku] = {'Weight': [u'重量(G)', '{}'.format(obj.survey_weight), '{}'.format(obj.examine_weight), u'', u'更改商品信息']}

                py_b_goods_objs = py_b_goods.objects.filter(SKU=obj.product_sku)
                if not py_b_goods_objs.exists():
                    raise Exception(u'b_goods中没有找到相关数据，SKU：{}'.format(obj.product_sku))

                Keywords = py_b_goods_objs[0].AliasEnName
                Keywords2 = py_b_goods_objs[0].AliasCnName
                material = py_b_goods_objs[0].Material
                dev_date = py_b_goods_objs[0].DevDate

                gResult = t_large_small_corresponding_cate_obj.getLargeClassBySmallClass(obj.product_scate)
                if gResult['code'] != 1:
                    raise Exception(gResult['errortext'])
                small_category = gResult['smallclass']
                input_box = obj.product_sku

                insertinto.append(
                    t_product_information_modify(
                        MainSKU=bemainsku, Details=details, SKU=obj.product_sku, Name2=obj.product_name, Keywords=Keywords,
                        Keywords2=Keywords2, SourcePicPath2=obj.product_image, Material=material, DevDate=dev_date,
                        LargeCategory=obj.product_lcate, SmallCategory=small_category, InputBox=input_box, XGcontext='',
                        Mstatus='DLQ',
                        Select=3, SQTimeing=datetime.now(), Source=u'普源信息', SQStaffNameing=request.user.first_name
                    )
                )
                obj.save()
            t_product_information_modify.objects.bulk_create(insertinto)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            messages.error(request, u'%s' % e)

    to_check.short_description = u'审核完成'

    def save_models(self):
        obj = self.new_obj
        request = self.request
        old_obj = None
        if obj is None or obj.id is None or obj.id <=0:
            pass
        else:
            old_obj = self.model.objects.get(pk=obj.pk)

        if not obj.product_mainsku:
            messages.error(request, u'对不起！商品SKU不可以为空！')
            return

        try:
            mlist = re.findall(r'[0-9]+|[a-z]+|[A-Z|]+|[-]', obj.product_mainsku)
            product_scate = mlist[0]  # 小类
            lResult = t_large_small_corresponding_cate_obj.getLargeClassBySmallClass(product_scate)
            product_lcate = lResult.get('largecode')

            product_image_list = request.POST.getlist('product_image', [])
            product_sku_list = request.POST.getlist('product_sku', [])
            product_name_list = request.POST.getlist('product_name', [])
            survey_weight_list = request.POST.getlist('survey_weight', [])
            packinfo_weight_list = request.POST.getlist('packinfo_weight', [])
            product_price_list = request.POST.getlist('product_price', [])
            supplier_name_list = request.POST.getlist('supplier_name', [])

            datalist = []
            for i in range(len(product_sku_list)):
                datalist.append(
                    self.model(
                        product_image=product_image_list[i],product_mainsku = obj.product_mainsku,
                        product_sku=product_sku_list[i],product_name = product_name_list[i],
                        survey_weight=survey_weight_list[i],supplier_name = supplier_name_list[i],
                        create_person=request.user.first_name,create_time = datetime.now(),
                        examine_weight=None,examine_status = '0',  # 未审核
                        auditor=None,examine_time = None,product_price=product_price_list[i],
                        packinfo_weight=packinfo_weight_list[i],product_scate=product_scate,
                        product_lcate=product_lcate
                    )
                )

            self.model.objects.bulk_create(datalist)
        except Exception as e:
            messages.error(request, u'%s' % e)

    def get_list_queryset(self,):
        request = self.request
        qs = super(t_sku_weight_examine_admin, self).get_list_queryset()

        try:
            wait_updates = self.model.objects.filter(examine_status='0')
            infors = []
            for wait_update in  wait_updates:
                infors.append({'SKU': wait_update.product_sku, 'SKUKEY': ['Number', 'ReservationNum']})

            sInfors = py_SynRedis_tables_obj.BatchReadRedis(infors)
            for sInfor in sInfors:
                Number = 0
                if sInfor['SKUKEY'][0]:
                    Number = int(sInfor['SKUKEY'][0])
                ReservationNum = 0
                if sInfor['SKUKEY'][1]:
                    ReservationNum = int(sInfor['SKUKEY'][1])
                wait_updates.filter(product_sku=sInfor['SKU']).update(canuse_num=Number - ReservationNum)
        except Exception as error:
            messages.error(request, u'{}'.format(error))

        seachfilter={}
        seachexclude = {}

        productsku = request.GET.get('productsku')
        if productsku:
            seachfilter['product_sku'] = productsku

        productname = request.GET.get('productname')
        if productname:
            seachfilter['product_name__contains'] = productname

        e_status = request.GET.get('e_status')
        if e_status:
            seachfilter['examine_status'] = e_status

        submiter = request.GET.get('submiter')
        if submiter:
            seachfilter['create_person'] = submiter

        checkman = request.GET.get('checkman')
        if checkman:
            seachfilter['auditor'] = checkman

        a_timeStart = request.GET.get('a_timeStart')
        if a_timeStart:
            seachfilter['create_time__gte'] = a_timeStart

        a_timeEnd = request.GET.get('a_timeEnd')
        if a_timeEnd:
            seachfilter['create_time__lt'] = a_timeEnd

        checktimeStart = request.GET.get('checktimeStart')
        if checktimeStart:
            seachfilter['examine_time__gte'] = checktimeStart

        checktimeEnd = request.GET.get('checktimeEnd')
        if checktimeEnd:
            seachfilter['examine_time__lt'] = checktimeEnd

        catelist = [u'001.时尚女装', u'002.时尚男装', u'021.泳装', u'024.童装', u'025.内衣']

        cloth = request.GET.get('cloth')
        if cloth == '1':  # 服装
            seachfilter['product_lcate__in'] = catelist
        if cloth == '0':  # 非服装
            seachexclude['product_lcate__in'] = catelist

        canusenumStart = request.GET.get('canusenumStart')
        if canusenumStart:
            seachfilter['canuse_num__gte'] = int(canusenumStart)

        canusenumEnd = request.GET.get('canusenumEnd')
        if canusenumEnd:
            seachfilter['canuse_num__lt'] = int(canusenumEnd)

        try:
            qs = qs.filter(**seachfilter).exclude(**seachexclude)
        except Exception as e:
            messages.error(request, u'%s' % e)

        return qs




















