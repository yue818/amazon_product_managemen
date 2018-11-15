# -*- coding: utf-8 -*-
from .t_product_Admin import *
import oss2
from Project.settings import *
from skuapp.table.B_PackInfo import *
import math
from datetime import datetime
from skuapp.table.t_product_pic_completion import t_product_pic_completion
from skuapp.table.t_product_photograph import t_product_photograph
from skuapp.table.t_product_photo_ing import t_product_photo_ing
from skuapp.table.t_product_develop_ed import t_product_develop_ed
from skuapp.table.t_product_art_ing import t_product_art_ing

class t_product_enter_ing_Admin(t_product_Admin):
    downloadxls = True

    actions = ['to_enter_ed_enter_ing', 'to_not_pass_enter_ing','to_recycle', '_complete_to_write_puyuan']
    def delete_models(self, queryset):
        from skuapp.table.Delete_Log_model import Delete_Log_Model
        from django.forms.models import model_to_dict
        import datetime
        insert_list=[]
        fmt_str_list=[]
        for obj in queryset:
            result=obj.delete()
            if result[0]==1:
                params=model_to_dict(obj)
                for k,v in params.items():
                    if isinstance(v, datetime.datetime):
                        v = v.strftime('%Y-%m-%d %H:%M:%S')
                    fmt_str=r'"{}":"{}"'.format(str(k),str(v))
                    fmt_str_list.append(fmt_str)
                delete_content='{'+','.join(fmt_str_list)+'}'
                sku=params.get('MainSKU')
                insert_row=Delete_Log_Model(actiontime=datetime.datetime.now(),username=self.user,sku=sku,where=self.model_name,delete_content=delete_content)
                insert_list.append(insert_row)
        try:
            Delete_Log_Model.objects.bulk_create(insert_list)
        except:
            pass


    def to_not_pass_enter_ing(self, request, queryset):

        for querysetid in queryset.all():
            obj = t_product_build_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username

            obj.PZStaffName = request.user.username
            obj.LRStaffName = request.user.first_name

            t_product_oplog_objs = t_product_oplog.objects.filter(pid = querysetid.id,StepID='JZL')[0:1]
            if t_product_oplog_objs.exists():
                obj.StaffID= t_product_oplog_objs[0].OpID
            obj.save()

            #修改操作记录
            t_product_oplog.objects.filter(pid = querysetid.id,StepID='JZL').update(MainSKU  = '',EndTime = datetime.now())
            querysetid.delete()

    to_not_pass_enter_ing.short_description = u'审核不通过'

    def to_recycle(self, request, queryset):
        for obj in queryset:
            try:
                t_product_photograph.objects.filter(MainSKU=obj.MainSKU).delete()
                t_product_photo_ing.objects.filter(MainSKU=obj.MainSKU).delete()
                t_product_develop_ed.objects.filter(MainSKU=obj.MainSKU).delete()
                t_product_art_ing.objects.filter(MainSKU=obj.MainSKU).delete() 
            except Exception as e:
                raise e
        super(t_product_enter_ing_Admin, self).to_recycle(request, queryset)
    to_recycle.short_description = u'扔进回收站'
    def to_exort_ed_enter_ing(self, request, queryset):
        from xlwt import *
        from skuapp.table.public import getChoices,ChoiceCategory2,ChoiceStorehouse
        from skuapp.table.t_base import getChoicesuser

        Category2 = getChoices(ChoiceCategory2)

        all_storehouse = getChoices(ChoiceStorehouse)

        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet('sku')

        for index,item in enumerate(XLS_FIELDS):
            sheet.write(0,index,item)

        #写数据
        row = 0

        for qs in queryset:
            shouse = qs.Storehouse
            for storehouse in all_storehouse:
                if qs.Storehouse == storehouse[0]:
                    shouse = storehouse[1]
            #根据主SKU查找子sku
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid =  qs.id)

            for  mainsku_sku_obj in t_product_mainsku_sku_objs :
                row = row +1
                column = 0
                sheet.write(row,column,u'add') #A 操作类型

                column = column +1
                if qs.MainSKU == mainsku_sku_obj.SKU :
                    sheet.write(row,column,'%s'%(qs.MainSKU)) #B 商品编码
                else:
                    sheet.write(row,column,'%s%s'%(qs.MainSKU,mainsku_sku_obj.SKU)) #B 商品编码

                column = column +1
                if qs.MainSKU == mainsku_sku_obj.SKU :
                    sheet.write(row,column,'%s'%(qs.MainSKU)) #C SKU
                else:
                    sheet.write(row,column,'%s%s'%(qs.MainSKU,mainsku_sku_obj.SKU)) #C SKU


                column = column +1
                sheet.write(row,column,u'否') #D 多款式

                column = column +1
                sheet.write(row,column,u'否') #E 是否有样品

                column = column +1
                #sheet.write(row,column,1) #F 样品数量

                column = column +1
                sheet.write(row,column,qs.LargeCategory) #G 大类名称

                column = column +1
                catt = None
                for cate in Category2:
                    if cate[0] == qs.SmallCategory:
                        catt = cate[1]
                        break
                if catt is None:
                    catt = qs.SmallCategory
                sheet.write(row, column, catt)  # H 小类名称

                column = column +1
                #sheet.write(row,column,qs.Name) #I 商品名称
                wjp = ''
                if qs.ContrabandAttribute and qs.ContrabandAttribute != u'普货':
                    if qs.SmallCategory != u'手表': #手表特殊
                        wjp = u'-违禁品'
                PrepackMark = qs.PrepackMark
                if PrepackMark is None:
                    PrepackMark=''
                sheet.write(row,column,u'%s%s-%s%s'%(PrepackMark,qs.Name2,mainsku_sku_obj.SKUATTRS,wjp)) #I 商品名称


                column = column +1
                sheet.write(row,column,u'正常') #J 当前状态

                column = column +1
                sheet.write(row,column,qs.Material) #K 材质

                column = column +1
                #sheet.write(row,column,'%s'%(qs.LWH) ) #L 规格


                column = column +1
                sheet.write(row,column, '%s'%(qs.SupplierArtNO)) #M 型号

                column = column +1
                #sheet.write(row,column, u'款式' ) #N 款式

                column = column +1
                sheet.write(row,column, 'fancyqube' ) #O 品牌

                column = column +1
                sheet.write(row,column, qs.Unit) #P 单位

                column = column +1
                #zxbzs = 1
                #if qs.Unit ==u'对':
                #    zxbzs = 2
                #sheet.write(row,column, zxbzs ) #Q 最小包装数
                sheet.write(row,column, mainsku_sku_obj.MinPackNum )

                column = column +1

                weight = 0
                if  qs.Weight is not None and qs.Weight >0:
                    weight = qs.Weight
                if  mainsku_sku_obj.Weight is not None and mainsku_sku_obj.Weight >0:
                    weight = mainsku_sku_obj.Weight

                PackNID= mainsku_sku_obj.PackNID
                if PackNID <=0 :
                    PackNID = qs.PackNID

                B_PackInfo_obj = B_PackInfo.objects.filter(id__exact = PackNID)
                if B_PackInfo_obj.exists():
                    weight = weight + int(B_PackInfo_obj[0].Weight)

                sheet.write(row,column,u'%s'%(weight)) #R 重量(G)
                """
                t_sys_packing_obj = None
                t_sys_packing2_obj = None
                if qs.PackingID_id is not None :
                    t_sys_packing_obj  = t_sys_packing.objects.get(id__exact = qs.PackingID_id)
                    if  t_sys_packing_obj is not None and t_sys_packing_obj.Weight is not None  :
                        weight = weight + t_sys_packing_obj.Weight

                #附加包装
                if qs.PackingID2Num is not None and qs.PackingID2Num > 0 and qs.PackingID2_id is not None:
                    t_sys_packing2_obj  = t_sys_packing2.objects.get(id__exact = qs.PackingID2_id)
                    if  t_sys_packing2_obj is not None  and t_sys_packing2_obj.Weight is not None and qs.PackingID2Num is not None :
                        weight = weight + t_sys_packing2_obj.Weight * qs.PackingID2Num
                sheet.write(row,column,u'%s'%(weight)) #R 重量(G)
                """

                column = column +1
                #sheet.write(row,column, ) #S 采购渠道

                column = column +1
                sheet.write(row,column,qs.SupplierID ) #T 供应商名称

                column = column +1
                #先找子sku有没有
                dj = qs.UnitPrice
                if  mainsku_sku_obj.UnitPrice is not None and mainsku_sku_obj.UnitPrice >0:
                    dj = mainsku_sku_obj.UnitPrice
                sheet.write(row,column,dj ) #U 成本单价(元)  就是单价 子SKU简单覆盖

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #V 批发价格(美元)

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #W 零售价格(美元)

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #X 最低售价(美元)

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #Y 最高售价(美元)

                column = column +1
                #sheet.write(row,column,qs.UnitPrice ) #Z 市场参考价(美元)

                column = column +1
                sheet.write(row,column,u'%s \n %s \n %s '%(mainsku_sku_obj.DressInfo,qs.Remark,qs.LWH)) #AA 备注

                column = column +1
                sheet.write(row,column,qs.ReportName2 ) #AB 中文申报名

                column = column +1
                sheet.write(row,column,qs.ReportName ) #AC 英文申报名

                column = column +1
                if dj is None:
                    dj =0 # math.ceil(2.3)
                sheet.write(row,column,int(math.ceil(float(dj)/SBBL)))   #AD 申报价值(美元)

                column = column +1
                sheet.write(row,column,'CN' ) #AE 原产国代码

                column = column +1
                sheet.write(row,column,'China' ) #AF 原产国

                column = column +1
                #sheet.write(row,column,100 ) #AG 库存上限

                column = column +1
                #sheet.write(row,column,5 ) #AH 库存下限

                column = column +1
                #sheet.write(row,column,qs.StaffID ) #AI 业绩归属人1
                t_product_oplog_obj1=t_product_oplog.objects.filter(pid=qs.id,StepID='KF')[0:1]

                t_product_oplog_obj2=t_product_oplog.objects.filter(pid=qs.id,StepID='JZL')[0:1]
                # mdf by wangzy 20180402 任务-503 保留调研员为业绩归属人
                #修改相同的业绩归属人1和2
                '''
                if  t_product_oplog_obj1.exists() and t_product_oplog_obj2.exists() and t_product_oplog_obj1[0].OpName != t_product_oplog_obj2[0].OpName:
                    sheet.write(row,column,t_product_oplog_obj1[0].OpName)
                            #AI 业绩归属人1
                '''
                sheet.write(row, column, qs.DYStaffName)  # AJ 业绩归属人2
                column = column +1
                #sheet.write(row,column,qs.StaffID )
                #mdf by wangzy 20180308
                #if t_product_oplog_obj2.exists() :
                #    sheet.write(row,column,t_product_oplog_obj2[0].OpName) #AJ 业绩归属人2
                if qs.YJGS2StaffName != '' and qs.YJGS2StaffName is not None:
                    sheet.write(row, column, getChoicesuser(qs.YJGS2StaffName))  # AJ 业绩归属人2
                elif t_product_oplog_obj2.exists() :
                    sheet.write(row, column, t_product_oplog_obj2[0].OpName)  # AJ 业绩归属人2



                column = column +1
                gg = ''
                if B_PackInfo_obj.exists():
                    gg =  B_PackInfo_obj[0].PackName
                sheet.write(row,column,gg ) #AK 包装规格
                """
                #包装1 14*14快递袋2g+3层起泡沫6g
                if t_sys_packing_obj is not None :
                    if t_sys_packing_obj.PackName == u'共济膜信封':
                        gg = gg + u'%s%s%sg'%(t_sys_packing_obj.PackStandard,t_sys_packing_obj.PackName,round(t_sys_packing_obj.Weight,1))
                    else:
                        gg = gg + u'%s%s%dg'%(t_sys_packing_obj.PackStandard,t_sys_packing_obj.PackName,round(t_sys_packing_obj.Weight))

               #附加包装
                if t_sys_packing2_obj is not None :
                    if t_sys_packing2_obj.Unit == u'层':
                        gg = gg + u'+%s%s%s%dg'%(qs.PackingID2Num,t_sys_packing2_obj.Unit,t_sys_packing2_obj.PackName,round(qs.PackingID2Num*t_sys_packing2_obj.Weight))
                    else:
                        gg = gg + u'+%s%s%s%s%dg'%(t_sys_packing2_obj.PackStandard,t_sys_packing2_obj.PackName,qs.PackingID2Num,t_sys_packing2_obj.Unit,round(qs.PackingID2Num*t_sys_packing2_obj.Weight))

                sheet.write(row,column,gg ) #AK 包装规格
                """
                column = column +1
                sheet.write(row,column,qs.UpdateTime.strftime('%Y-%m-%d') ) #AL 开发日期

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AM SKU款式1

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AN SKU款式2

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AO SKU款式3

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AP SKU描述

                column = column +1
                #sheet.write(row,column,qs.UpdateTime ) #AQ 图片URL

                column = column +1
                sheet.write(row,column,qs.Buyer ) #AR 采购员

                column = column +1
                sheet.write(row,column, shouse) #AS 发货仓库

                column = column +1
                sheet.write(row,column,qs.OrderDays ) #AT 采购到货天数

                column = column +1
                #计算内包装成本
                cb = 0
                if B_PackInfo_obj.exists():
                    cb = cb + B_PackInfo_obj[0].CostPrice
                sheet.write(row,column,u'%s'%(cb) ) #AU 内包装成本
                """
                #包装1
                if t_sys_packing_obj is not None and t_sys_packing_obj.Price is not None:
                    cb = cb + t_sys_packing_obj.Price
                #附加包装
                if t_sys_packing2_obj is not None and t_sys_packing2_obj.Price is not None and  qs.PackingID2Num is not None:
                    cb = cb + t_sys_packing2_obj.Price * qs.PackingID2Num

                sheet.write(row,column,u'%s'%(cb) ) #AU 内包装成本
                """
                #任务：411-网页URL1只提取主链接  mdf by wangzy 20180307
                column = column +1
                #sheet.write(row,column, u'%s;%s;'%(qs.SupplierPUrl1,qs.SupplierPUrl2)) #AV 网页URL 填写 供应商URL
                sheet.write(row, column, u'%s;' % (qs.SupplierPUrl1))  # AV 网页URL 填写 供应商URL

                column = column +1
                # sheet.write(row,column,'') #AW 网页URL2

                column = column +1
                #sheet.write(row,column, qs.SupplierPUrl2 ) #AX 网页URL3

                column = column +1
                #sheet.write(row,column,u'待定' ) #AY 最低采购价格

                column = column +1
                #sheet.write(row,column,u'待定' ) #AZ 海关编码

                column = column +1
                sheet.write(row,column,qs.StockAlarmDays ) #BA 库存预警销售周期

                column = column +1
                sheet.write(row,column,qs.MinOrder ) #BB 采购最小订货量

                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BC 内盒长
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BD 内盒宽
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BE 内盒高
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BF 内盒毛重
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BG 内盒净重
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BH 外箱长
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BI 外箱宽
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BJ 外箱高
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BK 外箱毛重
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BL 外箱净重
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BM 商品URL
                column = column +1
                #sheet.write(row,column,qs.MinOrder ) #BN 包装事项

                column = column +1
                #sheet.write(row,column,qs.Electrification ) #BO 是否带电

                column = column +1
                sheet.write(row,column,u'正常' ) #BP 商品SKU状态

                column = column +1
                #sheet.write(row,column,u'正常' ) #BQ 工号权限

                column = column +1
                #sheet.write(row,column,u'正常' ) #BR 季节

                column = column +1
                #sheet.write(row,column,qs.Powder ) #BS 是否粉末

                column = column +1
                #sheet.write(row,column,qs.Liquid ) #BT 是否液体

                column = column +1
                #sheet.write(row,column,u'正常' ) #BU 责任归属人1

                column = column +1
                sheet.write(row,column,qs.possessMan2 ) #BV 责任归属人2

                column = column +1  #BW 商品属性

                sheet.write(row,column,qs.ContrabandAttribute if qs.ContrabandAttribute else '')
                # if qs.ContrabandAttribute == '普货':
                #     sheet.write(row, column, u'普货')
                # elif qs.ContrabandAttribute == '一类特货':
                #     sheet.write(row, column, u'一类特货')
                # elif qs.ContrabandAttribute == '二类特货':
                #     sheet.write(row, column, u'二类特货')
                # elif qs.ContrabandAttribute == '三类特货':
                #     sheet.write(row, column, u'三类特货')
                # elif qs.ContrabandAttribute == '四类特货':
                #     sheet.write(row, column, u'四类特货')
                # elif qs.ContrabandAttribute == '五类特货':
                #     sheet.write(row, column, u'五类特货')
                # elif qs.ContrabandAttribute == '六类特货':
                #     sheet.write(row, column, u'六类特货')
                # elif qs.ContrabandAttribute == '七类特货':
                #     sheet.write(row, column, u'七类特货')

                column = column +1
                #sheet.write(row,column, ) #BX 包装难度系数
                    
                column = column +1
                #sheet.write(row,column,u'正常' ) #BY 店铺名称
                column = column +1
                #sheet.write(row,column,u'正常' ) #BZ UPC码
                column = column +1
                #sheet.write(row,column,u'正常' ) #CA ASIN码
                # 任务：411-网页URL1只提取主链接  mdf by wangzy 20180308
                column = column +1
                #sheet.write(row,column,u'正常' ) #CB 网页URL4
                sheet.write(row,column, u'%s;%s;'%(qs.SupplierPUrl1,qs.SupplierPUrl2)) #AV 网页URL 填写 供应商URL
                column = column +1
                #sheet.write(row,column,u'正常' ) #CC 网页URL5
                column = column +1
                #sheet.write(row,column,u'正常' ) #CD 网页URL6
                column = column +1
                #sheet.write(row,column,u'正常' ) #CE 店铺运费
                column = column +1
                #sheet.write(row,column,u'正常' ) #CF 包装材料重量
                column = column +1
                #sheet.write(row,column,u'正常' ) #CG 汇率
                column = column +1
                #sheet.write(row,column,u'正常' ) #CH 物流公司价格
                column = column +1
                #sheet.write(row,column,u'正常' ) #CI 交易费
                column = column +1
                #sheet.write(row,column,u'正常' ) #CJ 毛利率
                column = column +1
                #sheet.write(row,column,u'正常' ) #CK 计算售价



        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' +  filename)
        os.popen(r'chmod 777 %s'%(path + '/' +  filename))

        #上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        #删除现有的
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(request.user.username,request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s'%(request.user.username,filename),open(path + '/' +  filename))

        messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。' )
    to_exort_ed_enter_ing.short_description = u'导出EXCEL'

    def to_enter_ed_enter_ing(self, request, queryset):
        for querysetid in queryset.all():
            obj = t_product_enter_ed()
            obj.__dict__ = querysetid.__dict__
            obj.id = querysetid.id
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.LRTime = datetime.now()
            obj.LRStaffName = request.user.first_name
            try:
                del obj.auditnote
            except Exception:
                pass
            piccomplete=t_product_pic_completion.objects.filter(MainSKU=querysetid.MainSKU,pid=querysetid.id)
            if piccomplete:
                #2完成实拍 3完成制作
                if piccomplete[0].YNphoto==u'0':
                    obj.MGProcess=2
                elif piccomplete[0].YNphoto==u'1':
                    obj.MGProcess=3
                obj.MGStaffName = piccomplete[0].MGStaffName
                obj.MGTime = piccomplete[0].MGTime
                obj.PZStaffName = piccomplete[0].PZStaffName
                obj.PZTime = piccomplete[0].PZTime
            
            obj.onebuOperation = '0'
            obj.twobuOperation = '0'
            obj.threebuOperation = '0'
            obj.fourbuOperation = '0'
            obj.fivebuOperation = '0'
            obj.sixbuOperation = '0'
            obj.sevenbuOperation = '0'
            obj.eightbuOperation = '0'
            obj.ninebuOperation = '0'
            obj.tenbuOperation = '0'
            obj.elevenbuOperation = '0'
            obj.twelvebuOperation = '0'
            obj.thirteenbuOperation = '0'

            obj.save()
            # if rt == '0':
            #     message.info("商品信息添加成功")
            # if rt == '1':
            #     message.error("商品信息添加失败")

            # if querysetid.YNphoto == '0':#实拍
            #     photo_obj = t_product_photograph()
            #     photo_obj.__dict__ = querysetid.__dict__
            #     photo_obj.id = querysetid.id
            #     photo_obj.CreateTime = datetime.now()
            #     photo_obj.CreateStaffName = request.user.first_name
            #     photo_obj.StaffID= request.user.username
            #     photo_obj.LRTime = datetime.now()
            #     photo_obj.LRStaffName = request.user.first_name
            #     photo_obj.PZRemake = '1'
            #     #photo_obj.MGProcess = '0'
            #     photo_obj.PZTimeing = querysetid.JZLTime
            #     photo_obj.PZStaffNameing = querysetid.JZLStaffName
            #     photo_obj.SampleState = 'notyet'
            #     photo_obj.pid = querysetid.id
            #     photo_obj.save()
            #
            # elif querysetid.YNphoto == '1':#制作
            #     MG_obj = t_product_develop_ed()
            #     MG_obj.__dict__ = querysetid.__dict__
            #     MG_obj.id = querysetid.id
            #     MG_obj.CreateTime = datetime.now()
            #     MG_obj.CreateStaffName = request.user.first_name
            #     MG_obj.StaffID= request.user.username
            #     MG_obj.LRTime = datetime.now()
            #     MG_obj.LRStaffName = request.user.first_name
            #     MG_obj.PZRemake = None
            #     MG_obj.PZTimeing = None
            #     MG_obj.PZStaffNameing = None
            #     MG_obj.SampleState = None
            #     MG_obj.pid = querysetid.id
            #     #MG_obj.MGProcess = '1'
            #
            #     MG_obj.save()

            #elif querysetid.YNphoto == '2':#待换图

            end_t_product_oplog(request,querysetid.MainSKU,'LR',querysetid.Name2,querysetid.id)
            #begin_t_product_oplog(request,querysetid.MainSKU,'BMLY',querysetid.Name2,querysetid.id)
            querysetid.delete()

    to_enter_ed_enter_ing.short_description = u'录入完成'


    # def _complete_to_write_puyuan(self, request, queryset):
    #     from brick.pydata.py_modify.product_entry import online_syn_to_puyuan
    #     success_id, error_dict = online_syn_to_puyuan(queryset=queryset, request=request)
    #     if error_dict:
    #         for k, v in error_dict.items():
    #             messages.error(request, u'%s: %s' % (k, v))
    #     if success_id:
    #         messages.info(request, u'id: %s同步成功' % ','.join(success_id))
    # _complete_to_write_puyuan.short_description = u'录入完成(同步普源)'

    def _complete_to_write_puyuan(self, request, objs):
        from datetime import datetime
        from brick.table.t_operation_log_online_syn_py import t_operation_log_online_syn_py
        from app_djcelery.tasks import online_syn_to_puyuan_task
        from django.db import connection
        operation_log_obj = t_operation_log_online_syn_py(DBConn=connection)

        first_name = request.user.first_name
        user_name = request.user.username
        now_time = datetime.now()

        sResult = {'rcode': '0', 'messages': ''}  # 初始状态
        opnum = 'add_sku_%s_%s' % (now_time.strftime('%Y%m%d%H%M%S'), user_name)
        try:
            param = {}  # 操作日志的参数
            param['OpNum']=opnum
            param['OpKey'] = objs.values_list("MainSKU",flat=True)
            param['OpType']='add_sku'
            param['Status']='runing'
            param['ErrorInfo']=''
            param['OpPerson']=request.user.first_name
            param['OpTime']=now_time
            param['OpStartTime']=now_time
            param['OpEndTime']=None
            param['aNum']=len(objs)
            param['rNum']=0
            param['eNum']=0

            enter_id_list = []
            iResult = operation_log_obj.createLog(param)
            assert iResult['errorcode'] == 0, "insert log error."
            for obj in objs:
                enter_id_list.append(int(obj.id))
            online_syn_to_puyuan_task.delay(
                enter_id_list=enter_id_list, optype='add_sku', opnum=opnum, first_name=first_name, user_name=user_name
            )
            sResult['rcode'] = 1
            sResult['KEY'] = opnum
        except Exception, ex:
            sResult['rcode'] = -1
            sResult['messages'] = '%s:%s' % (Exception, ex)
        return HttpResponse(json.dumps(sResult))

    _complete_to_write_puyuan.short_description = u'录入完成(同步普源)'






    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id,StepID='JZL',MainSKU=obj.MainSKU).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'



    def show_PackName(self,obj) :
        rt = ''
        PackNID= obj.PackNID
        if PackNID <=0 :
            return rt
        B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
        if B_PackInfo_obj is not None:
            rt =  B_PackInfo_obj.PackName
        return rt
    show_PackName.short_description = u'包装规格'

    def show_CostPrice(self,obj) :
        rt = ''
        PackNID= obj.PackNID
        if PackNID <=0 :
            return rt
        B_PackInfo_obj = B_PackInfo.objects.get(id__exact = PackNID)
        if B_PackInfo_obj is not None:
            rt =  B_PackInfo_obj.CostPrice
        return rt
    show_CostPrice.short_description = u'内包装成本'

    def show_Remark(self,obj) :
        return mark_safe(u'【%s】<br>%s<br>%s<br>%s'%(obj.LWH,obj.Remark,obj.SupplierPUrl1,obj.SupplierPUrl2 ))
    show_Remark.short_description = u'备注'

    def show_wjp(self,obj) :
        rt = obj.ContrabandAttribute if obj.ContrabandAttribute <> '普货' else ''
        # if obj.ContrabandAttribute == '普货':
        #     rt = u'普货'
        # if obj.ContrabandAttribute == '一类特货':
        #     rt = u'一类特货'
        # elif obj.ContrabandAttribute == '二类特货':
        #     rt = u'二类特货'
        # elif obj.ContrabandAttribute == '三类特货':
        #     rt = u'三类特货'
        # elif obj.ContrabandAttribute == '四类特货':
        #     rt = u'四类特货'
        # elif obj.ContrabandAttribute == '五类特货':
        #     rt = u'五类特货'
        # elif obj.ContrabandAttribute == '六类特货':
        #     rt = u'六类特货'
        # elif obj.ContrabandAttribute == '七类特货':
        #     rt = u'七类特货'
        return rt
    show_wjp.short_description = u'违禁品'

    def show_name2(self,obj) :
        PrepackMark = obj.PrepackMark
        if PrepackMark is None:
            PrepackMark=''
        Name2 = obj.Name2
        if obj.ContrabandAttribute and obj.ContrabandAttribute != u'普货':
            if obj.SmallCategory != u'手表': #手表特殊
                wjp = u'-违禁品'
                return u'%s%s%s'%(Name2,wjp,PrepackMark)
        return u'%s%s'%(Name2,PrepackMark)
    show_name2.short_description = mark_safe(u'商品<br>名称<br>(中文)')


    list_display= ('id','JZLTime','JZLStaffName','show_SourcePicPath2','MainSKU','Buyer','possessMan2','SpecialRemark','PrepackMark','show_skulist','LargeCategory','SmallCategory','show_name2','Material','SupplierArtNO','Unit','MinPackNum','SupplierID','Keywords','ReportName','ReportName2','show_oplog','show_wjp','show_Remark','auditnote')
    #list_display_links= ('id','SourcePicPath2',)#,'MainSKU','LargeCategory','SmallCategory','Name2','Material','SupplierArtNO','Unit','MinPackNum','SupplierID','Keywords2','Keywords',)
    list_editable=('SpecialRemark','Buyer','possessMan2','auditnote')
    readonly_fields = ('id','SourcePicPath','SourcePicPath2','Pricerange','OrdersLast7Days',)
    #search_fields=('id','MainSKU','Name2','StaffID',)
    #list_filter = ('UpdateTime',)


    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.StaffID = request.user.username
        obj.save()
