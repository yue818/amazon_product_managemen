# -*- coding: utf-8 -*-
from xadmin.layout import Fieldset,Row
from django.utils.safestring import mark_safe
from django.contrib import messages
from skuapp.table.t_all_plateform_code_shopname import t_all_plateform_code_shopname
from skuapp.table.t_use_productsku_apply_for_shopsku import t_use_productsku_apply_for_shopsku
from skuapp.table.t_shopsku_information_binding import t_shopsku_information_binding
from brick.public.generate_shop_code import *
from django.db import connection
from .t_product_Admin import *
from datetime import datetime as datime
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from brick.public.combination_sku import G_ZHSKU
import oss2
import re


class t_use_productsku_apply_for_shopsku_Admin(object):
    search_box_flag = True
    downloadxls = True
    shopsku_apply = True

    list_display   = ('id','ShopName','ApplyType','ProductSKU','ShopSKU','Applicant','ApplyTime','BStatus',)
    list_editable  = ('ProductSKU',)
    list_filter    = ('ApplyType','ApplyTime','BStatus','EStatus')
    search_fields =None
    fields =  ('ApplyType','InputText',)
    form_layout = (
        Fieldset(u'-------',
                    #Row('ShopName',),
                    Row('ApplyType',),
                    Row('InputText',),
                ))
                
    actions = ('to_banding','to_excel','to_exort_ed')
    def to_banding(self,request,objs):
        insertlist = []
        for obj in objs:
            if obj.BStatus == 'notyet':
                insertlist.append(t_shopsku_information_binding(SKU=obj.ProductSKU,ShopSKU=obj.ShopSKU,Filename = u'SKU申请',
                                                                PersonCode=obj.Applicant,Memo=obj.ShopName,Submitter=request.user.first_name,
                                                                SubmitTime = datime.now(),BindingStatus = 'wait'
                                                                ))
                obj.BStatus = 'already'
                obj.save()
        t_shopsku_information_binding.objects.bulk_create(insertlist)
    to_banding.short_description = u'确定进行绑定'


    def to_excel(self, request, objs):
        from xlwt import *
        from app_djcelery.tasks import get_shopsku_sku_forthwith_excel
        #path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #mkdir_p(MEDIA_ROOT + 'download_xls')
        #os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        idlist = []
        i = 0
        for obj in objs:
            if i >= 50000:
                break

            i = i + 1

            idlist.append(obj.id)
        filename = request.user.username + '_' + datime.now().strftime('%Y%m%d%H%M%S') + '.xls'

        get_shopsku_sku_forthwith_excel.delay(idlist, request.user.username)

        messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出，可点击Download下载到本地......................')
    to_excel.short_description = u'导出EXCEL(即时导出)'


    def to_exort_ed(self, request, objs):
        from app_djcelery.tasks import get_shopsku_sku_excel
        from skuapp.table.t_download_info import t_download_info
        from datetime import datetime as uptime

        idlist = []
        i = 0
        for obj in objs:
            if i >=2000:
                break
            obj.EStatus = 'wait'
            obj.save()

            i = i + 1

            idlist.append(obj.id)
        # infos = t_download_info.objects.create()
        filename = request.user.username + '_' + uptime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        infos = t_download_info.objects.create(abbreviation=u'店铺SKU申请导出-' + filename,
                                               updatetime=uptime.now(), Belonger=request.user.username,
                                               Datasource='t_use_productsku_apply_for_shopsku')

        get_shopsku_sku_excel.delay(idlist,request.user.username,infos.id)
        messages.success(request,u'正在导出，请稍后到 下载中心 下载文件。。。')
    to_exort_ed.short_description = u'导出EXCEL'



    def save_models(self):
        from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
        obj = self.new_obj
        request = self.request
        if obj.InputText is not None and obj.InputText.strip() != '' :
            proskulist = []
            codetype = ['|','，',',']
            coty = ','
            for code in codetype:
                if obj.InputText.find(code) != -1:
                    coty = code
            templist = obj.InputText.replace('\n','').replace('\r','').replace('\r\n','').split(coty) #['XMA0519WT','XMA0519RD','XMA0519PK']
            templist = [temp for temp in templist if temp]
            if obj.ApplyType is not None and obj.ApplyType.strip() == 'productsku':
                ProTemp = t_product_mainsku_sku.objects.filter(ProductSKU__in=templist)
                if len(set(templist)) != len(set(ProTemp.values_list('ProductSKU',flat=True))):
                    faultsku=set(templist)-set(ProTemp.values_list('ProductSKU',flat=True))
                    faultsku_str = [str(_) for _ in faultsku]
                    messages.error(request, u'填写的商品SKU:{}有误'.format(u",".join(faultsku_str)))
                    return
                for tmp in templist:
                    for prosku in ProTemp:
                        if prosku.ProductSKU == tmp:
                            proskulist.append([prosku.MainSKU,prosku.ProductSKU])
            elif obj.ApplyType is not None and obj.ApplyType.strip() == 'mainsku':
                ProTemp = t_product_mainsku_sku.objects.filter(MainSKU__in=templist)
                mainsku = []
                for prosku in ProTemp:
                    mainsku.append(prosku.MainSKU)
                    proskulist.append([prosku.MainSKU,prosku.ProductSKU])
                if len(set(templist)) != len(set(mainsku)):
                    faultmainsku=set(templist)-set(mainsku)
                    faultmainsku_str=[str(_) for _ in faultmainsku]
                    messages.error(request, u'填写的主SKU:{}有误'.format(u",".format(faultmainsku_str)))
                    return
            elif obj.ApplyType is not None and obj.ApplyType.strip() == 'combination':
                for temp in templist:
                    if temp.find('+') == -1 and temp.find('*') == -1:
                        messages.error(request, u'非组合产品不允许申请组合SKU:{}'.format(temp))
                        return
                    skulist = [ skutmp.split('\\')[0].split('*')[0] for skutmp in temp.split('+') if skutmp ]
                    SKUTempL = t_product_mainsku_sku.objects.filter(ProductSKU__in=skulist).values_list('ProductSKU',flat=True)
                    if len(set(SKUTempL)) != len(set(skulist)):
                        faultSKU=set(skulist)-set(SKUTempL)
                        faultSKU_str=[str(_) for _ in faultSKU]
                        messages.error(request, u'填写的用于组合的商品SKU:{}有误'.format(u",".join(faultSKU_str)))
                        return
                    cskuset = '+'.join(sorted(set([ skutmp for skutmp in temp.split('+') if skutmp ])))  # 商品SKU集合  +
                    ZHSKU = G_ZHSKU(cskuset,connection,request.user.first_name,request.user.username,datime.now())
                    if ZHSKU['code'] == 1:
                        messages.error(request, u'组合SKU申请错误，请稍后再试')
                        return
                    # if ZHSKU['code'] == 2:
                    #     messages.error(request, u'该组合SKU:%s 已经存在,对应的商品SKU组合为:%s'%(ZHSKU['ZHSKU'],cskuset))
                    #     return
                    ZHSKU = ZHSKU['ZHSKU']  # 生成的组合SKU
                    proskulist.append([None,ZHSKU])
                    messages.success(request, u'组合SKU申请成功，请稍后到“组合商品对应关系表”中查看组合关系，并确定组合商品名称')
            else:
                messages.error(request,u'申请类型 不可以为空！！！')
            obj.ShopName = request.POST.get('txt1','')
            t_store_configuration_file_objs = t_store_configuration_file.objects.filter()
            eflag= 0
            for t_store_configuration_file_obj in t_store_configuration_file_objs:
                if obj.ShopName == t_store_configuration_file_obj.ShopName:
                    eflag=1
                    break
            if eflag == 1:
                if proskulist and obj.ShopName is not None and obj.ShopName.strip() != '':
                    insertinto = []
                    tempdict = generate_code_func(connection,obj.ShopName,len(proskulist))
                    if tempdict['Code'] == 0:
                        Code = tempdict['result'][0]
                        Num  = tempdict['result'][1]
                        Num  = Num - len(proskulist)
                        for pro in proskulist:
                            if len(pro) == 2:  # 主SKU不存在就是说明该商品SKU不存在
                                Num = Num + 1
                                newshopsku = Code + str(Num).zfill(len(str(Num)))
                                insertinto.append(t_use_productsku_apply_for_shopsku(
                                    ShopName=obj.ShopName,ApplyType=obj.ApplyType,InputText=obj.InputText,
                                    ProductSKU=pro[-1],ShopSKU=newshopsku,BStatus = 'notyet',EStatus = 'never',
                                    MainSKU=pro[0],
                                    Applicant=request.user.first_name,ApplyTime=datime.now()
                                    ))
                        t_use_productsku_apply_for_shopsku.objects.bulk_create(insertinto)
                    else:
                        messages.error(request,u'同一时间有多人，同时申请同一店铺的店铺SKU,导致申请冲突，请稍后再试。。。。l = %s'%len(proskulist))
                else:
                    messages.error(request,u'请填写绑定店铺并确认输入信息有效！')
            else:
                messages.error(request,u'请填写完整的卖家简称！！！')
        else:
            messages.error(request,u'未填写需要绑定的 商品SKU。。。。。。')


    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_use_productsku_apply_for_shopsku_Admin, self).get_list_queryset()

        applyType = request.GET.get('applyType', '')  # 申请类型
        bStatus = request.GET.get('bStatus', '')  # 确认绑定状态

        ShopName = request.GET.get('ShopName', '')  # 卖家简称
        ShopName = ShopName.encode('utf-8')
        productSKU = request.GET.get('productSKU', '')  # 商品编码
        shopSKU = request.GET.get('shopSKU', '')  # 店铺子SKU
        shopSKU = re.split('[,，]', shopSKU.encode('utf-8'))
        applicant = request.GET.get('applicant', '')  # 申请人
        mainSKU = request.GET.get('mainSKU', '')  # 主SKU
        mainSKU = re.split('[,，]', mainSKU.encode('utf-8'))
        applyTimeStart = request.GET.get('applyTimeStart', '')  # 申请时间
        applyTimeEnd = request.GET.get('applyTimeEnd', '')

        searchList = {'ApplyType__exact': applyType, 'BStatus__exact': bStatus,
                      'ShopName__exact': ShopName, 'ProductSKU__exact': productSKU,
                      'ShopSKU__in': shopSKU, 'Applicant__exact': applicant,
                      'MainSKU__in': mainSKU,
                      'ApplyTime__gte': applyTimeStart, 'ApplyTime__lt': applyTimeEnd,
                      }

        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                v = [_.strip() for _ in v if _.strip()]
                if v :
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    #if k == 'ShopName__exact':
                        #v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')

        if request.user.is_superuser:
            return qs
        return qs.filter(Applicant=request.user.first_name)
        
        
        
        
        
        
        
        

    