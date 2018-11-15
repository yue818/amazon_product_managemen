# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_online_info import t_online_info
from skuapp.table.t_config_online_amazon import t_config_online_amazon
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from skuapp.table.t_ShopName_ParentSKU import t_ShopName_ParentSKU
from skuapp.table.t_distribution_product_to_store import t_distribution_product_to_store
from skuapp.table.t_shopsku_information_binding import t_shopsku_information_binding
from pyapp.models import b_goodsskulinkshop as py_b_goodsskulinkshop
from pyapp.models import b_goodssku as py_b_goodssku
from datetime import datetime
import datetime as datime
import logging
from django.contrib import messages
import re
import requests
import random
import string

from skuapp.table.t_online_info_wish import t_online_info_wish
import csv
from skuapp.table.t_api_schedule_ing import t_api_schedule_ing
from django.utils.safestring import mark_safe
from skuapp.modelsadminx.t_online_info_wish_Admin import t_online_info_wish_Admin
from skuapp.table.t_distribution_product_to_store_result import t_distribution_product_to_store_result as store_result
from skuapp.table.t_sys_param import t_sys_param
from pyapp.models import b_goods as py_b_goods
from skuapp.table.t_distribution_product_to_store_temp import t_distribution_product_to_store_temp as store_temp

from django.db.models import Q  
from  Project.settings import SQLSERVERDB
logger = logging.getLogger('sourceDns.webdns.views')
rate = t_sys_param.objects.filter(Type=40,Seq=1)[0].V  # 美元兑人民币汇率
from skuapp.table.t_tort_aliexpress import t_tort_aliexpress
import os
import oss2
from Project.settings import MEDIA_ROOT
from .t_product_Admin import *
import traceback
from skuapp.table.t_upload_shopname import t_upload_shopname
from skuapp.table.t_distribution_template_table import t_distribution_template_table
from skuapp.table.t_distribution_template_table_temp import t_distribution_template_table_temp


class t_distribution_product_to_store_Admin(object):
    downloadxls = True
    select_checkbox_flag = True
    search_box_flag = True

    def show_picture(self,obj) :
        url = obj.Image.replace('-original','-medium')
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(url,url,url)
        return mark_safe(rt)
    show_picture.short_description = u'图片'

    def show_submit(self,obj) :
        if obj.SubStatus == '1':
            SubStatus = u'未铺货'
        else:
            SubStatus = u'已铺货'

       # if obj.Submitter == '1':
          #  Submitter = u'自己'
       # else:
        #    Submitter = u'全部'

        if obj.Type == '1':
            Type = u'全部铺货'
        elif obj.Type == '2':
            Type = u'更改铺货'
        elif obj.Type == '3':
            Type = u'原样铺货'
        elif obj.Type == '4':
            Type = u'已有数据铺货'
        else:
            Type = u'未选择'
        rt = u'提交人:%s<br>提交时间:<br>%s<br>提交状态:%s<br>铺货类型:%s'%(obj.Submitter,obj.SubTime,SubStatus,Type)
        rt = "%s<br><a id='Implementation_plan_id_%s'>查看执行计划</a><script>$('#Implementation_plan_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看执行计划',fix:false,shadeClose: true,maxmin:true,area:['600px','700px'],content:'/t_distribution_product_to_store/upload_Implementation_plan/?getapiingid=%s',btn:['关闭页面']});});</script>"%(rt,obj.id,obj.id,obj.id)
        return mark_safe(rt)
    show_submit.short_description = u'提交人/时间/状态'

    def show_shopName_seller(self, obj):
        rt = ''
        rt = u'%s卖家简称:<br>%s<br>店长/销售员:%s<br>产品ID:<br>%s' % (rt, obj.ShopName, obj.Seller, obj.ProductID)
        return mark_safe(rt)
    show_shopName_seller.short_description = u'卖家简称/店长/销售员/产品ID'

    def show_operation(self, obj):
        rt = '<a href="/Project/admin/skuapp/t_online_info_wish/?_p_MainSKU=%s&wishID=%s"  target="_blank">更换ProductID</a>' % (obj.csvSKU,obj.id)
        return mark_safe(rt)
    show_operation.short_description = u'操作'

    def show_SKU_list(self,obj) :
        rt='<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1">' \
           '<tr bgcolor="#C00"><th style="text-align:center">子SKU</th><th style="text-align:center">子SKU状态</th>' \
           '<th style="text-align:center">店铺SKU</th><th style="text-align:center">库存量</th>' \
           '<th style="text-align:center">参考价格</th><th style="text-align:center">原价格</th><th style="text-align:center">标签价</th>' \
           '<th style="text-align:center">运费</th><th style="text-align:center">运输时间</th>' \
           '<th style="text-align:center">上下架</th></tr>'
        if store_temp.objects.filter(NID=obj.id).exists():
            shopName = store_temp.objects.filter(NID=obj.id)[0].ShopName
        else:
            shopName = ''
        store_temp_objs = store_temp.objects.values('SKU','ShopSKU','Quantity','Price','Status','msrp','ShippingTime','Shipping','oldPrice').filter(NID=obj.id,ShopName=shopName)
        i = 0
        for store_temp_obj in store_temp_objs:
            if i < 5:
                st = py_b_goods.objects.filter(SKU=store_temp_obj['SKU'])
                if st.exists():
                    st = st[0].GoodsStatus
                else:
                    st = u'未知'
                if store_temp_obj['Status'] =='Enabled':
                    tt = '上架'
                else:
                    tt = '下架'
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%\
                     (rt,store_temp_obj['SKU'],st,store_temp_obj['ShopSKU'],store_temp_obj['Quantity'],store_temp_obj['Price'],store_temp_obj['oldPrice'],
                      store_temp_obj['msrp'],store_temp_obj['Shipping'],store_temp_obj['ShippingTime'],tt)
                i = i + 1
        rt = '%s<tr><td><a id="link_id_%s">点击修改</a></td></tr>'%(rt,obj.id)
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1200px','700px'],content:'/wish_change/?abc=%s',btn:['关闭页面'],end:function(){location.reload();}});});</script>"%(rt,obj.id,obj.id)
        return mark_safe(rt)
    show_SKU_list.short_description = mark_safe('<p align="center"> 子SKU</p>')

    def show_csvSKU_status(self,obj):
        csvsku = obj.csvSKU
        rt = '<div class="box" style="width: 80px;height: 30px;text-align: center;line-height: 30px;border-radius: 4px">%s</div>' % csvsku
        tort_objs = t_tort_aliexpress.objects.filter(MainSKU=csvsku)
        if tort_objs.exists():
            tortSiteList = []
            for tort_obj in tort_objs:
                tort_site = tort_obj.Site
                tortSiteList.append(tort_site)
            if 'Wish' in tortSiteList:
                site = 'Wish仿品'
                rt = '%s<br><div class="box" style="width: 80px;height: 30px;background-color: #FF3333;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(rt,site)
            else:
                site = '其他仿品'
                rt = '%s<br><div class="box" style="width: 80px;height: 30px;background-color: #FFCC33;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(rt,site)
        else:
            site = '非仿品'
            rt = '%s<br><div class="box" style="width: 80px;height: 30px;background-color: #66FF66;text-align: center;line-height: 30px;border-radius: 4px">%s</div>' % (rt, site)
        return mark_safe(rt)
    show_csvSKU_status.short_description = u'SKU及侵权状态'

    def show_csvShop1(self,obj):
        shopList = obj.csvShop1.split(',')
        rt = ''
        for i in range(len(shopList)):
            if (i + 1) % 10 == 0:
                rt = rt + shopList[i] + '<br>'
            else:
                rt = rt + shopList[i] + ','
        up = u"<a id='show_update_shopname_id_%s'>点击修改</a><script>$('#show_update_shopname_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'请修改铺货目标店铺',fix:false,shadeClose: true,maxmin:true,area:['900px','500px'],content:'/to_wish_store_distribution/?id=%s',btn:['关闭页面'],end:function(){location.reload();}});});</script>"%(obj.id,obj.id,obj.id)
        return mark_safe(u'%s<br><br><br>%s'%(rt[:-1],up))
    show_csvShop1.short_description = u'csv内店铺'

    def show_id(self,obj):
        if obj.SubStatus == '1':
            if obj.Type == None:
                rt = '<font color="#FF3333">%s</font>'%(obj.id)
            else:
                rt = '<font color="#FFE007">%s</font>' % (obj.id)
        else:
            rt = '<font color="#00BB00">%s</font>'%(obj.id)
        return mark_safe(rt)
    show_id.short_description = u'ID'

    list_display = ('show_id','show_picture','ShopNum','TimeInterval','StartTime','EndTime','show_csvSKU_status','show_csvShop1','show_submit','show_shopName_seller',
                    'Title','Description','Tags','show_SKU_list','Remarks','Orders7Days','OfSales','show_operation',)
    list_filter = ('id','csvSKU','Orders7Days','ProductID','Submitter','SubTime','SubStatus','Type')
    search_fields = ('id','csvSKU','ProductID','Submitter','SubStatus',)
    list_editable = ('Title','Description','Tags','Remarks','ShopNum','TimeInterval','StartTime','EndTime',)
    fields = ('FileName','FileName2')

    actions = ['all_goods_distribution','change_goods_distribution',
               'original_goods_distribution','to_distribution','to_excel','Generate_shop','Become_a_template']

    def Become_a_template(self,request,objs):
        for obj in objs:
            cou = t_distribution_template_table.objects.filter(pid=obj.id).count()
            if cou<=0:
                template_obj                   = t_distribution_template_table()
                template_obj.__dict__          = obj.__dict__
                template_obj.TemplateCreator   = self.request.user.first_name
                template_obj.TemplateCreatTime = datetime.now()
                template_obj.TemplateModifier   = self.request.user.first_name
                template_obj.TemplateModifyTime = datetime.now()
                template_obj.pid                = obj.id
                template_obj.Status             = None
                template_obj.FileName           = None
                template_obj.csvShop1           = None
                template_obj.csvShop2           = None
                template_obj.csvShop3           = None
                template_obj.FileName2          = None
                template_obj.Type               = None
                template_obj.ShopNum            = None
                template_obj.TimeInterval       = None
                template_obj.StartTime          = None
                template_obj.EndTime            = None
                template_obj.apiingid           = None

                temp_obj = store_temp.objects.filter(NID=obj.id)
                if temp_obj.exists():
                    shopName = temp_obj[0].ShopName
                else:
                    shopName = ''
                store_temp_objs = temp_obj.filter(ShopName=shopName)
                for store_temp_obj in store_temp_objs:
                    # messages.error(self.request,'.....................')
                    template_temp_obj             = t_distribution_template_table_temp()
                    template_temp_obj.__dict__    = store_temp_obj.__dict__
                    template_temp_obj.TemplateCreator   = self.request.user.first_name
                    template_temp_obj.TemplateCreatTime = datetime.now()
                    template_temp_obj.TemplateModifier   = self.request.user.first_name
                    template_temp_obj.TemplateModifyTime = datetime.now()
                    template_temp_obj.save()

                template_obj.save()
            else:
                messages.error(self.request,u'该模版已经存在！')
    Become_a_template.short_description = u'设为模版'

    def Generate_shop(self,request,objs):
        for obj in objs:
            if obj.ShopNum is not None and obj.ShopNum != 0:
                ShopName_list = []
                t_upload_shopname_objs = t_upload_shopname.objects.values('ShopName')
                for t_upload_shopname_obj in t_upload_shopname_objs:
                    ShopName_list.append(t_upload_shopname_obj['ShopName'][-4:])
                Shop_list =random.sample(ShopName_list, obj.ShopNum)
                t_distribution_product_to_store.objects.filter(id=obj.id).update(csvShop1=','.join(Shop_list))
                self.insert_into_temp(','.join(Shop_list),obj,t_online_info.objects.filter(ProductID=obj.ProductID))
    Generate_shop.short_description = u'根据铺货店铺数量生成店铺'

    # 根据CSV提供的SKU找到七天ORDER最大的商品ID
    def get_productID(self,SKU):
        t_online_info_wish_objs = t_online_info_wish.objects.filter(MainSKU=SKU).order_by('-Orders7Days').order_by('-OfSales')
        if len(t_online_info_wish_objs) != 0:
            productID = t_online_info_wish_objs[0].ProductID
        else:
            productID = ''
        return productID


    def insert_into_temp(self,csvShop1,store_obj,t_online_info_objs):
        for shop in csvShop1.split(','):
            # i=i+1
            # messages.error(self.request, '3333333333333333____%s'%i)
            shopName = self.get_shopName(shop)
            parentSKU = self.get_parent_SKU(shopName)
            NID = store_obj.id
            for each in t_online_info_objs:
                i = 0
                ShopSKU = self.get_shopSKU(parentSKU,each.SKU,i,each.ShopSKU)
                i += 1
                # 处理价格，价格为空取None，否则取浮点型
                if each.Price == None:
                    Price = None
                else:
                    Price = float(each.Price.split('$')[-1])  # 价格
                # 处理吊牌价，数据为空取售价与运费之和的三倍
                if (each.msrp == None) or (each.msrp.strip() == '') or (int(float(each.msrp.split('$')[-1])) == 0):
                    if each.Shipping == None:
                        shipping = 0
                    else:
                        shipping = float(each.Shipping.split('$')[-1])
                    if each.Price == None:
                        Price = 0
                    else:
                        Price = float(each.Price.split('$')[-1])
                    msrp = float((Price + shipping) * 3)
                else:
                    msrp = float(each.msrp.split('$')[-1])  # 标签价
                # 处理运费
                if (each.Shipping == None) or (each.Shipping.strip() == ''):
                    Shipping = None
                else:
                    Shipping = float(each.Shipping.split('$')[-1])  # 运费
                store_temp.objects.create(NID=NID,ProductID=each.ProductID,SKU=each.SKU,ShopSKU=ShopSKU,
                                          Status=each.Status,Price=Price,Quantity=each.Quantity,
                                          ParentSKU=each.ParentSKU,msrp=msrp,oldPrice=Price,
                                          Color=each.Color,Size=each.Size,Shipping=Shipping,
                                         ShippingTime=each.ShippingTime,ShopName=shopName)


    # 保存数据
    def save_models(self):
        obj = self.new_obj
        request = self.request
        try:
            if obj.FileName is not None and str(obj.FileName).strip() != '':
                i = 0
                for row in csv.reader(obj.FileName):
                    if i < 1:
                        i = i + 1
                        continue
                    i = i + 1
                    # messages.error(request,'row---%s'%row)
                    if row[0].strip() != '':
                        csvSKU   = row[0]
                         # 主SKU
                        ShopNum = None
                        if row[1].strip() != '':
                            ShopNum      = row[1] # 店铺数
                        csvShop1 = None
                        if row[2].strip() != '':
                            csvShop1     = row[2] # 铺货店铺
                        TimeInterval = None
                        if row[3].strip() != '':
                            TimeInterval = row[3] # 铺货间隔时间
                        StartTime = None
                        if row[4].strip() != '':
                            # messages.error(request,'row[4]--%s'%row[4])
                            # StartTime = '2017/11/8'
                            StartTime = datetime.strptime(row[4].strip(), "%Y-%m-%d") # 铺货开始时间
                        EndTime = None
                        if row[5].strip() != '':
                            # messages.error(request,'row[5]--%s'%row[5])
                            # EndTime = '2017/11/9'
                            EndTime = datetime.strptime(row[5].strip(), "%Y-%m-%d") # 铺货结束时间
                        # messages.error(request,'StartTime---%s;EndTime---%s'%(StartTime,EndTime))
                        Submitter = request.user.first_name
                        SubTime = datetime.now()
                        SubStatus = '1'
                        ProductID = self.get_productID(row[0])
                        # messages.error(request,'ProductID---%s'%ProductID)

                        t_online_info_wish_objs = t_online_info_wish.objects.filter(ProductID=ProductID)
                        # messages.error(self.request, '11111111111111111111111111')
                        if t_online_info_wish_objs.exists():
                            Image = t_online_info_wish_objs[0].Image
                            ShopName = t_online_info_wish_objs[0].ShopName
                            Seller = t_online_info_wish_objs[0].Seller
                            Title = t_online_info_wish_objs[0].Title
                            if Title is not None:
                                Title = self.get_str(t_online_info_wish_objs[0].Title).decode('unicode_escape')
                            Orders7Days = t_online_info_wish_objs[0].Orders7Days
                            OfSales = t_online_info_wish_objs[0].OfSales

                            t_online_info_objs = t_online_info.objects.filter(ProductID=ProductID)
                            if t_online_info_objs.exists():
                                Description = t_online_info_objs[0].Description
                                if Description is not None:
                                    Description = self.get_str(t_online_info_objs[0].Description).decode('unicode_escape')
                                # 处理Tags，去掉'|' 和 'name:'
                                Tags = t_online_info_objs[0].Tags
                                if Tags is not None:
                                    Tags = self.get_str(t_online_info_objs[0].Tags).decode('unicode_escape')
                                if Tags == None:
                                    Tags = ''
                                else:
                                    if '|' not in Tags:
                                        Tags = Tags
                                    else:
                                        for eachTags in Tags.split('|'):
                                            tag_except_name = eachTags.split('name:')[1]
                                            if Tags == '':
                                                Tags = u'%s' % tag_except_name
                                            else:
                                                Tags = u'%s,%s' % (Tags, tag_except_name)
                                ExtraImages = t_online_info_objs[0].ExtraImages
                                # messages.error(self.request, '11111111111111111111111111')
                                # messages.error(self.request, '%s-%s-%s-%s-%s-%s'%(csvSKU,ShopNum,csvShop1,TimeInterval,type(StartTime),type(EndTime)))
                                store_obj = t_distribution_product_to_store.objects.create(csvSKU=csvSKU,csvShop1=csvShop1,Submitter=Submitter,
                                                                               SubTime=SubTime,SubStatus=SubStatus,ProductID=ProductID,
                                                                               Image=Image,ShopName=ShopName,Seller=Seller,Title=Title,
                                                                               Orders7Days=Orders7Days,OfSales=OfSales,
                                                                               Description=Description,Tags=Tags,ExtraImages=ExtraImages,
                                                                               ShopNum=ShopNum,TimeInterval=TimeInterval,StartTime=StartTime,
                                                                               EndTime=EndTime)
                                # messages.error(self.request, '22222222222222222222222222')
                                # i=0
                                if csvShop1 is not None and csvShop1.strip() != '':
                                    self.insert_into_temp(csvShop1,store_obj,t_online_info_objs)
                            else:
                                messages.error(self.request, 'SKU: %s未找到合适商品-1' % csvSKU)
                        else:
                            messages.error(self.request,'SKU: %s未找到合适商品-2'% csvSKU)

            if obj.FileName2 is not None and str(obj.FileName2).strip() != '':
                    Submitter = request.user.first_name
                    SubTime = datetime.now()

                    # 第一次遍历CSV文件，枚举所有 店铺名+父SKU
                    name_SKU_list = []
                    i = 0
                    for row in csv.reader(obj.FileName2):
                        if i < 1:
                            i += 1
                            continue
                        i += 1

                        shopName = row[0]
                        parent = row[1]
                        name_SKU = shopName + '+' + parent
                        if name_SKU not in name_SKU_list:
                            name_SKU_list.append(name_SKU)

                        dict1 = {}
                        for item in name_SKU_list:
                            dict2 = {}
                            for eachShop in item.split('+')[0].split(','):
                                shopName = self.get_shopName(eachShop)
                                dict2[eachShop] = self.get_parent_SKU(shopName)
                            dict1[item] = dict2

                    # 第二次遍历CSV文件，将相同的 店铺名+父SKU 合并成一条记录插入到数据库
                    j = 0
                    for row in csv.reader(obj.FileName2):
                        if j < 1:
                            j += 1
                            continue
                        j += 1

                        shopName = row[0]
                        parent = row[1]
                        SKU = row[2]
                        csvSKU = re.split(r'(\d+)',SKU)[0] + re.split(r'(\d+)',SKU)[1]
                        shopSKU = row[3]
                        Title = row[4]
                        Description = row[5]
                        Tags = row[6]
                        msrp = row[7]
                        color = row[8]
                        size = row[9]
                        oldprice = row[10]
                        shipping = row[11]
                        inventory = row[12]
                        shippingTime = row[13]
                        Image = row[14]
                        variationImage = row[15]

                        extraImage = ''
                        for i in range(16, 30):
                            if row[i] == '':
                                continue
                            else:
                                if extraImage == '':
                                    extraImage += row[i]
                                else:
                                    extraImage = extraImage + '|' + row[i]

                        name_SKU = shopName + '+' + parent

                        if name_SKU in name_SKU_list:
                            name_SKU_list.remove(name_SKU)


                            store_obj = t_distribution_product_to_store.objects.create(csvSKU=csvSKU, csvShop1=shopName,
                                                                                       Submitter=Submitter,SubTime=SubTime,
                                                                                       SubStatus='1',Image=Image,
                                                                                       Title=Title,ExtraImages=extraImage,
                                                                                       Description=Description, Tags=Tags,
                                                                                       Type='4')
                            NID = store_obj.id
                            for shopName in shopName.split(','):
                                i = 0
                                ShopName = self.get_shopName(shopName)
                                parentSKU = dict1[name_SKU][shopName]
                                shopSKU = self.get_shopSKU(parentSKU,SKU,i,shopSKU)
                                store_temp.objects.create(NID=NID,SKU=SKU, ShopSKU=shopSKU,Quantity=inventory,Color=color,Size=size,
                                                          ParentSKU=parentSKU, msrp=msrp, oldPrice=oldprice,Shipping=shipping,
                                                          ShippingTime=shippingTime, ShopName=ShopName,
                                                          VariationImage=variationImage,Status='Enabled',Price=1)
                                i += 1
                        else:
                            for shopName in shopName.split(','):
                                i = 0
                                ShopName = self.get_shopName(shopName)
                                parentSKU = dict1[name_SKU][shopName]
                                shopSKU = self.get_shopSKU(parentSKU, SKU, i, shopSKU)
                                # messages.error(request, 'ShopName---------%s' % ShopName)
                                # messages.error(request, 'parentSKU---------%s' % parentSKU)
                                # messages.error(request, 'shopSKU---------%s' % shopSKU)
                                NID = store_temp.objects.filter(ParentSKU=parentSKU,ShopName=ShopName)[0].NID
                                # messages.error(request,'NID---------%s'%NID)
                                store_temp.objects.create(NID=NID, SKU=SKU, ShopSKU=shopSKU, Quantity=inventory, Color=color,
                                                          Size=size,VariationImage=variationImage,Status='Enabled',Price=1,
                                                          ParentSKU=parentSKU, msrp=msrp, oldPrice=oldprice, Shipping=shipping,
                                                          ShippingTime=shippingTime, ShopName=ShopName,)
                                i += 1

        except Exception, ex:
            logger.error('%s============================%s' % (Exception, ex))
            # messages.error(request, '%s============================%s============%s' % (Exception, ex,traceback.print_exc()))

    # 生成shopname
    def get_shopName(self,shopname):
        shopcode = re.findall(r'[0-9]',shopname)
        code = ''.join(shopcode)
        new_shopname = 'Wish-%s'%(code.zfill(4))
        # num = len(shopname)
        # if num == 1:
            # shopName = 'Wish-000' + shopname
        # elif num == 2:
            # shopName = 'Wish-00' + shopname
        # elif num == 3:
            # shopName = 'Wish-0' + shopname
        # else:
            # shopName = 'Wish-' + shopname
        return new_shopname

    # 生成parent_sku
    def get_parent_SKU(self, ShopName):
        t_ShopName_ParentSKU_ParentSKU_objs = t_ShopName_ParentSKU.objects.values('ParentSKU').filter(ShopName=ShopName)
        if t_ShopName_ParentSKU_ParentSKU_objs.exists():
            Parent_SKU_list = re.split(r'(\d+)', t_ShopName_ParentSKU_ParentSKU_objs[0]['ParentSKU'])
            Parent_SKU = u'%s%s' % (
                Parent_SKU_list[0], str(int(Parent_SKU_list[1]) + 1).zfill(len(Parent_SKU_list[1])))

            t_ShopName_ParentSKU.objects.filter(ShopName=ShopName).update(ParentSKU=Parent_SKU)

        elif not t_ShopName_ParentSKU_ParentSKU_objs.exists():
            t_online_info_ParentSKUs = t_online_info.objects.values('ParentSKU').filter(ShopName=ShopName[0:9])
            if t_online_info_ParentSKUs.exists():
                ParentSKU_head = []
                ParentSKU_list = []
                for t_online_info_ParentSKU in t_online_info_ParentSKUs:
                    ParentSKU_l = re.split(r'(\d+)', t_online_info_ParentSKU['ParentSKU'])
                    if len(ParentSKU_l) >= 2:
                        ParentSKU_head.append(ParentSKU_l[0])
                        ParentSKU_list.append(int(str(int(ParentSKU_l[1]) + 1).zfill(len(ParentSKU_l[1]))))
                    else:
                        ParentSKU_head.append(t_online_info_ParentSKU['ParentSKU'])
                        ParentSKU_list.append('00001')
                Parent_SKU = u'%s%s%s' % (random.sample(set(ParentSKU_head), 1)[0], 'A', max(ParentSKU_list))

            elif not t_online_info_ParentSKUs.exists():

                # Parent_SKU = u'%sA0001' % ShopName[10:14].upper()
                randChar = ''
                for i in range(4):
                    randChar += random.choice(string.ascii_uppercase)
                randNum = str(random.randint(100000, 999999))
                Parent_SKU = u'%s%s' % (randChar, randNum)

            t_ShopName_ParentSKU_objs = t_ShopName_ParentSKU()
            t_ShopName_ParentSKU_objs.ShopName = ShopName
            t_ShopName_ParentSKU_objs.ParentSKU = Parent_SKU
            t_ShopName_ParentSKU_objs.save()
        return Parent_SKU

    # 生成shopsku
    def get_shopSKU(self, Parent_SKU, SKU, number, shopsku):
        ShopSKU = u'%s%d' % (Parent_SKU, number)
        t_online_info_ShopSKU_list_f = re.split(r'(\d+)', SKU)
        for i in range(2, len(t_online_info_ShopSKU_list_f)):
            ShopSKU = u'%s%s' % (ShopSKU, t_online_info_ShopSKU_list_f[i])
        logger.error("ShopSKU===================%s" % (ShopSKU))
        if '*' in shopsku:
            ShopSKU = ShopSKU + '*' + shopsku.split('*')[-1]
        return ShopSKU

    # 判断商品是否已在该店铺内存在
    def goods_exits_in_shopName(self, SKU, ShopName):
        t_online_info_SKU_objs = t_online_info.objects.filter(ShopName=ShopName, SKU__contains=SKU)
        if len(t_online_info_SKU_objs) == 0:
            return False
        else:
            return True

    # 根据出现次数计算售价
    def change_price(self, SKU, percent):
        '''如果在b_goods表根据SKU查询到数据，则计算售价，否则售价为零'''
        b_goods_objs = py_b_goods.objects.filter(SKU=SKU)
        if b_goods_objs.exists():
            weight = b_goods_objs[0].Weight
            cost = b_goods_objs[0].CostPrice

            if 0 < weight and weight < 300:
                Dollar = (float(weight) * 0.1 * 0.85 + float(cost)) * 100 / float(rate) / (
                1 - float(percent) / 100 - 0.06 - 0.1)
            elif weight is not None:
                Dollar = ((float(weight) * 0.1 + 8) * 0.8 + float(cost)) * 100 / float(rate) / (
                1 - float(percent) / 100 - 0.06 - 0.1)

            listDollsr = str(round(Dollar, 3)).split('.')
            intPart = int(listDollsr[0])
            floatPart = int(listDollsr[1])
            if intPart <= 1:
                money = 2
            else:
                if floatPart >= 400:
                    money = intPart + 1
                else:
                    money = intPart
            money = float(money)
        else:
            money = 0
        return money

    # 从普源库查找商品状态
    def get_goodsStatus(self, SKU):
        b_goods_objs = py_b_goods.objects.filter(SKU=SKU)
        if b_goods_objs.exists():
            goodsStatus = b_goods_objs[0].GoodsStatus
            if (goodsStatus == U'正常') or (goodsStatus == U'在售'):
                return True
            else:
                return False
        else:
            return False

    # 判断链接是否过于复杂
    def judge_sku_num(self, productID):
        skuList = []
        objs = t_online_info.objects.filter(ProductID=productID)
        if objs.exists():
            for obj in objs:
                if obj.SKU != '':
                    skuList.append(obj.SKU)

        skuSet = set(skuList)
        for item in skuSet:
            if skuList.count(item) > 3:
                result = True
                break
            else:
                result = False
        return result

    # 执行插入指令表操作
    def insert_into_schedule(self, shopName,ScheduleTime, params):
        insert_result = t_api_schedule_ing.objects.create(ShopName=shopName, PlatformName='Wish', CMDID='UPLOAD',
                                          ScheduleTime=ScheduleTime, InsertTime=datetime.now(), Params=params, Processed=0,
                                          Successful=0, WithError=0, WithWarning=0, Status=0)
        return insert_result

    # 执行插入到结果表
    def insert_into_result(self, each,ScheduleTime, shopName, result_status, params=None, Parent_SKU=None):
        time = datetime.now()
        obj = store_result.objects.create(PlatformName='Wish', PID=each.id, SKU=each.csvSKU, ShopName=shopName,
                                          Submitter=each.Submitter, SubTime=time, Status=result_status,
                                          Params=params,Type=each.Type,ParentSKU=Parent_SKU,ScheduleTime=ScheduleTime)
        return obj.id

    # 替换文中不能转义的字符
    def get_str(self,string):
        string = string.replace("&#39;","'").replace("&amp;","&").replace("\\/",'/').replace("&quot;",'"')
        return string

    # 获取params参数
    def get_info(self,id,shopname):
        params = {'first':{'url': 'https://merchant.wish.com/api/v2/product/add'},
                  'second':{'url': 'https://merchant.wish.com/api/v2/variant/add'},
                  }

        store_objs = t_distribution_product_to_store.objects.filter(id=id)
        store_temp_objs = store_temp.objects.filter(NID=id,ShopName=shopname).order_by('oldPrice','Quantity')

        main_image = store_objs[0].Image

        description = store_objs[0].Description
        name = store_objs[0].Title
        tags = store_objs[0].Tags
        extra_images = store_objs[0].ExtraImages

        product = []

        for i in range(len(store_temp_objs)):
            parent_sku = store_temp_objs[i].ParentSKU
            size = store_temp_objs[i].Size
            shipping_time = store_temp_objs[i].ShippingTime
            shipping = store_temp_objs[i].Shipping
            color = store_temp_objs[i].Color
            msrp = store_temp_objs[i].msrp
            format = 'json'
            productSKU = store_temp_objs[i].SKU
            inventory = store_temp_objs[i].Quantity
            price = store_temp_objs[i].oldPrice
            sku = store_temp_objs[i].ShopSKU
            if store_temp_objs[i].Status == 'Enabled':
                enabled = True
            else:
                enabled = False

            product.append({'size':size,'shipping_time':shipping_time,'shipping':shipping,'color':color,
                          'parent_sku':parent_sku,'msrp':msrp,'format':format,'productSKU':productSKU,
                          'inventory':inventory,'price':price,'sku':sku,'enabled':enabled})
        if product:
            product[0]['main_image'] = main_image
            product[0]['description'] = description
            product[0]['name'] = name
            product[0]['tags'] = tags
            product[0]['extra_images'] = extra_images

            params['first']['product'] = product[0]
            params['second']['product'] = product[1:]

        return params

    # 全部铺货
    def all_goods_distribution(self,request,queryset):
        """全部铺货：什么都不改变，如果普源有库存，则直接上架，如果没库存则默认不上架"""
        for obj in queryset:
            if obj.csvShop1 is not None and obj.csvShop1.strip() != '':
                shopList = obj.csvShop1.split(',')
                for eachShop in shopList:
                    shopName = self.get_shopName(eachShop)
                    parentSKU = self.get_parent_SKU(shopName)

                    store_temp_obj = store_temp.objects.filter(NID=obj.id,ShopName=shopName)
                    store_temp_obj.update(ParentSKU=parentSKU)
                    for i in range(len(store_temp_obj)):
                        # 从普源判断是否有库存，如果有库存则上架
                        if self.get_goodsStatus(store_temp_obj[i].SKU):
                            status = 'Enabled'
                        else:
                            status = 'Disabled'

                        shopSKU = self.get_shopSKU(parentSKU, store_temp_obj[i].SKU, i, store_temp_obj[i].ShopSKU)
                        store_temp.objects.filter(id=store_temp_obj[i].id).update(ShopSKU=shopSKU, Status=status)
                    t_distribution_product_to_store.objects.filter(id=obj.id).update(Type='1')
            else:
                messages.error(self.request,u'请填写铺货目标店铺')
    all_goods_distribution.short_description = u'全部铺货'

    # 更改铺货
    def change_goods_distribution(self,request,queryset):
        """改库存价格铺货：更改库存和价格，如果普源有库存，则直接上架，如果没库存则默认不上架"""
        for obj in queryset:
            if obj.csvShop1 is not None and obj.csvShop1.strip() != '':
                shopList = obj.csvShop1.split(',')
                for eachShop in shopList:
                    shopName = self.get_shopName(eachShop)
                    parentSKU = self.get_parent_SKU(shopName)

                    store_temp_obj = store_temp.objects.filter(NID=obj.id,ShopName=shopName).order_by('-oldPrice')
                    store_temp_obj.update(ParentSKU=parentSKU)

                    sku_first = []
                    sku_second = []
                    for i in range(len(store_temp_obj)):
                        # 从普源判断是否有库存，如果有库存则上架
                        if self.get_goodsStatus(store_temp_obj[i].SKU):
                            status = 'Enabled'
                        else:
                            status = 'Disabled'
                        # 根据子SKU出现的次数，重新计算价格和库存
                        if store_temp_obj[i].SKU not in sku_first:
                            percent = 20
                            sku_first.append(store_temp_obj[i].SKU)
                            inventory = 9999
                            # 出现两次
                        elif store_temp_obj[i].SKU not in sku_second:
                            percent = 5
                            sku_second.append(store_temp_obj[i].SKU)
                            inventory = 20
                            # 出现三次
                        else:
                            percent = -30
                            inventory = 3

                        price = self.change_price(store_temp_obj[i].SKU,percent)

                        # 如果计算后的price不为零，需要减去运费
                        if price != 0:
                            if store_temp_obj[i].Shipping == None:
                                price = price
                            else:
                                price = price - float(store_temp_obj[i].Shipping)
                                if price <= 0:
                                    price = store_temp_obj[i].Price
                        # 如果计算后的price为零，则取最原始的价格
                        else:
                            price = store_temp_obj[i].Price

                        shopSKU = self.get_shopSKU(parentSKU,store_temp_obj[i].SKU,i,store_temp_obj[i].ShopSKU)

                        store_temp.objects.filter(id=store_temp_obj[i].id).update(Price=price,
                                                                        ShopSKU=shopSKU,Quantity=inventory,Status=status)
                t_distribution_product_to_store.objects.filter(id=obj.id).update(Type='2')
            else:
                messages.error(self.request,u'请填写铺货目标店铺')
    change_goods_distribution.short_description = u'更改铺货'

    # 原样铺货
    def original_goods_distribution(self,request,queryset):
        """原样铺货：更改库存和价格，如果普源有库存，则根据原状态上下架，如果没库存则默认不上架"""
        for obj in queryset:
            if obj.csvShop1 is not None and obj.csvShop1.strip() != '':
                shopList = obj.csvShop1.split(',')
                for eachShop in shopList:
                    shopName = self.get_shopName(eachShop)
                    parentSKU = self.get_parent_SKU(shopName)

                    store_temp_obj = store_temp.objects.filter(NID=obj.id,ShopName=shopName).order_by('-oldPrice')
                    store_temp_obj.update(ParentSKU=parentSKU)

                    sku_first = []
                    sku_second = []
                    for i in range(len(store_temp_obj)):
                        # 从普源判断是否有库存，如果有库存且原状态是'Enabled'状态，则上架
                        if (self.get_goodsStatus(store_temp_obj[i].SKU)) and (store_temp_obj[i].Status == 'Enabled'):
                            status = 'Enabled'
                        else:
                            status = 'Disabled'
                        # 根据子SKU出现的次数，重新计算价格和库存
                        if store_temp_obj[i].SKU not in sku_first:
                            percent = 20
                            sku_first.append(store_temp_obj[i].SKU)
                            inventory = 9999
                            # 出现两次
                        elif store_temp_obj[i].SKU not in sku_second:
                            percent = 5
                            sku_second.append(store_temp_obj[i].SKU)
                            inventory = 20
                            # 出现三次
                        else:
                            percent = -30
                            inventory = 3
                        price = self.change_price(store_temp_obj[i].SKU,percent)

                        # 如果计算后的price不为零，需要减去运费
                        if price != 0:
                            if store_temp_obj[i].Shipping == None:
                                price = price
                            else:
                                price = price - float(store_temp_obj[i].Shipping)
                                if price <= 0:
                                    price = store_temp_obj[i].Price
                        # 如果计算后的price为零，则取最原始的价格
                        else:
                            price = store_temp_obj[i].Price

                        shopSKU = self.get_shopSKU(parentSKU,store_temp_obj[i].SKU,i,store_temp_obj[i].ShopSKU)
                        store_temp.objects.filter(id=store_temp_obj[i].id).update(Price=price,
                                                                        ShopSKU=shopSKU,Quantity=inventory,Status=status)
                t_distribution_product_to_store.objects.filter(id=obj.id).update(Type='3')
            else:
                messages.error(self.request,u'请填写铺货目标店铺')
    original_goods_distribution.short_description = u'原样铺货'

    # 进行铺货
    def to_distribution(self,request,queryset):
        for obj in queryset:
            Interval = 0.0
            if obj.Type is not None and obj.csvShop1 is not None and obj.csvShop1.strip() != '':
                shopList = obj.csvShop1.split(',') # 得到所有的铺货目标店铺 代码
                time = datime.datetime.now()
                if obj.TimeInterval is not None:
                    Interval = obj.TimeInterval

                elif obj.StartTime is not None and obj.EndTime is not None:
                    DayInterval = (obj.EndTime-obj.StartTime).days + 1 # 天数
                    Interval = round(DayInterval*24/len(shopList),2) # 间隔小时

                result_id_list = self.insert_into(shopList,obj,Interval,time) # 返回 插入指令计划表 的ID
                queryset.filter(id = obj.id).update(apiingid=','.join(result_id_list),SubStatus = '2')
                # obj.apiingid=','.join(result_id_list)
                # obj.SubStatus = '2'
                # obj.save()
            else:
                messages.error(request,'铺货类型为空,或铺货目标店铺为空')
    to_distribution.short_description = u'执行铺货'

    # ((datetime.datetime.now()-datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M"))
    def insert_into(self,shopList,obj,Interval,time):
        insert_result_id = []
        for i in range(0, len(shopList)):
            Inval = float(Interval)*(random.uniform(0.8,1.2)) + (float(Interval)*i)
            ScheduleTime = (time+datime.timedelta(hours=Inval)).strftime("%Y-%m-%d %H:%M:%S")
            shopName = self.get_shopName(shopList[i])
            if not self.goods_exits_in_shopName(obj.csvSKU, shopName):
                result_1 = store_result.objects.filter(SKU=obj.csvSKU,ShopName=shopName,Status='6')
                result_2 = store_result.objects.filter(SKU=obj.csvSKU,ShopName=shopName)
                if (result_1.exists()) or (not result_2.exists()):
                    result_status = '7'
                    params = self.get_info(obj.id, shopName)
                    ID = self.insert_into_result(obj,ScheduleTime, shopName, result_status, params,params['first']['product']['parent_sku'])
                    params['id'] = ID
                    insert_result = self.insert_into_schedule(shopName,ScheduleTime,params)
                    insert_result_id.append('%s-%s'%(insert_result.id,ID))
                else:
                    result_status = '2'
                    ID = self.insert_into_result(obj,ScheduleTime,shopName, result_status)
            else:
                result_status = '3'
                ID = self.insert_into_result(obj,ScheduleTime,shopName, result_status)
        return insert_result_id

    def to_excel(self,request,queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('store')
        sheet.write(0, 0, u'铺货ID')
        sheet.write(0, 1, u'提交人')
        sheet.write(0, 2, u'提交时间')
        sheet.write(0, 3, u'提交状态')
        sheet.write(0, 4, u'csv内SKU')
        sheet.write(0, 5, u'csv内店铺')
        sheet.write(0, 6, u'卖家简称')
        sheet.write(0, 7, u'7天order数')
        sheet.write(0, 8, u'总销量')
        sheet.write(0, 9, u'产品标题')
        sheet.write(0, 10, u'产品ID')

        # 写数据
        row = 0

        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row, column, qs.id)

            column = column + 1
            sheet.write(row, column, qs.Submitter)

            column = column + 1
            sheet.write(row, column, qs.SubTime)

            column = column + 1
            sheet.write(row, column, qs.SubStatus)

            column = column + 1
            sheet.write(row, column, qs.csvSKU)

            column = column + 1
            sheet.write(row, column, qs.csvShop1)

            column = column + 1
            sheet.write(row, column, qs.ShopName)

            column = column + 1
            sheet.write(row, column, qs.Orders7Days)

            column = column + 1
            sheet.write(row, column, qs.OfSales)

            column = column + 1
            sheet.write(row, column, qs.Title)

            column = column + 1
            sheet.write(row, column, qs.ProductID)


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


    def get_list_queryset (self,):
        request = self.request
        qs = super(t_distribution_product_to_store_Admin,self).get_list_queryset()
        csvSKU = request.GET.get('csvSKU','')
        ProductID = request.GET.get('ProductID','')
        Ster = request.GET.get('Submitter','')
        SubmitterName = request.GET.get('SubmitterName','')
        if Ster == '1':#自己
            Submitter = request.user.first_name
            #SubmitterName=''
        else:
            Submitter = SubmitterName

        SubStatus = request.GET.get('SubStatus','')
        Type = request.GET.get('Type','')
        SubTimeStart = request.GET.get('SubTimeStart', '')
        SubTimeEnd = request.GET.get('SubTimeEnd', '')


        searchList = {'csvSKU__exact':csvSKU,'ProductId__exact':ProductID,'Submitter__exact':Submitter,
                      'SubStatus__exact':SubStatus,'Type__exact':Type, 'SubTime__gte': SubTimeStart, 'SubTime__lte': SubTimeEnd,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:

            qs = qs.filter(**sl)    
  
        return qs

       
      