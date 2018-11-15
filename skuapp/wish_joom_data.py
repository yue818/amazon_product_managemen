# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_online_info import t_online_info
import logging
from django.forms import TextInput, Textarea
from skuapp.table.t_online_info_wish import *
from skuapp.table.t_store_configuration_file import *
from skuapp.table.t_ShopName_ParentSKU import t_ShopName_ParentSKU
import requests
from django.contrib import messages
import re
import logging
import random

logger = logging.getLogger('sourceDns.webdns.views')
#获取tag标签内容
def GET_TAGS(Tags):
    if Tags.find('|') != -1 and Tags is not None:
        tags = ''
        for tag_l in Tags.split('|'):
            tag_ll = tag_l.split('name:')
            if tags == '':
                tags = u'%s'%tag_ll[1]
            else:
                tags = u'%s,%s'%(tags,tag_ll[1])
        return tags
    else:
        return Tags
    
#Parent_SKU
def GET_PARENT_SKU(ShopName):
    t_ShopName_ParentSKU_ParentSKU_objs = t_ShopName_ParentSKU.objects.values('ParentSKU').filter(ShopName__contains = ShopName)
    if t_ShopName_ParentSKU_ParentSKU_objs.exists():
        Parent_SKU_list =  re.split(r'(\d+)',t_ShopName_ParentSKU_ParentSKU_objs[0]['ParentSKU'])
        Parent_SKU = u'%s%s'%(Parent_SKU_list[0],str(int(Parent_SKU_list[1])+1).zfill(len(Parent_SKU_list[1])))
        
        t_ShopName_ParentSKU.objects.filter(ShopName__contains = ShopName).update(ParentSKU=Parent_SKU)
        
    elif not t_ShopName_ParentSKU_ParentSKU_objs.exists():
        t_online_info_ParentSKUs = t_online_info.objects.values('ParentSKU').filter(ShopName = ShopName)
        if t_online_info_ParentSKUs.exists():
            ParentSKU_head = []
            ParentSKU_list = []
            for t_online_info_ParentSKU in t_online_info_ParentSKUs:
                ParentSKU_l = re.split(r'(\d+)',t_online_info_ParentSKU['ParentSKU'])
                ParentSKU_head.append(ParentSKU_l[0])
                ParentSKU_list.append(int(str(int(ParentSKU_l[1])+1).zfill(len(ParentSKU_l[1]))))

            Parent_SKU = u'%s%s%s'%(random.sample(set(ParentSKU_head),1)[0],'A',max(ParentSKU_list))
            
        elif not t_online_info_ParentSKUs.exists():
            randoms = random.sample('abcdefghijklmnopqrstuvwxyz',4)
            randomsku = randoms[0]+randoms[1]+randoms[2]+randoms[3]
            Parent_SKU = u'%sA0001'%(randomsku.upper())  #创造 一个全新的 Parent_SKU
            
        t_ShopName_ParentSKU_objs = t_ShopName_ParentSKU()
        t_ShopName_ParentSKU_objs.ShopName = ShopName
        t_ShopName_ParentSKU_objs.ParentSKU= Parent_SKU
        t_ShopName_ParentSKU_objs.save()
    return Parent_SKU
    

#shopsku
def GET_SHOPSKU(Parent_SKU,SKU,number):
    ShopSKU = u'%s%d'%(Parent_SKU,number)
    t_online_info_ShopSKU_list_f = re.split(r'(\d+)',SKU)
    for i in range(2,len(t_online_info_ShopSKU_list_f)):
        ShopSKU = u'%s%s'%(ShopSKU,t_online_info_ShopSKU_list_f[i])
    logger.error("ShopSKU===================%s"%(ShopSKU))
    return ShopSKU

def get_wish_data(ProductID,ShopName):
    params = {}
    t_online_info_objs = t_online_info.objects.filter(ProductID = ProductID)
    Parent_SKU = GET_PARENT_SKU(ShopName)
    if t_online_info_objs.exists() :
        first_dict['url'] = 'https://merchant.wish.com/api/v2/product/add'
        first_product_dict = {
            #'access_token': access_token_value,
            'format': 'json',
            'name': t_online_info_objs[0].Title,
            'description': t_online_info_objs[0].Description,#描述
            'tags': GET_TAGS(t_online_info_objs[0].Tags),#标签
            'sku': GET_SHOPSKU(Parent_SKU,t_online_info_objs[0].SKU,0),
            'inventory': 99999,
            'price': float(t_online_info_objs[0].Price.split('.')[0][1:]),
            'shipping': float(t_online_info_objs[0].Shipping.split('.')[0][1:]),
            'main_image': t_online_info_objs[0].Image,
            'color': t_online_info_objs[0].Color,
            'size': t_online_info_objs[0].Size,
            'msrp': float(t_online_info_objs[0].msrp.split('.')[0][1:]),
            'shipping_time': t_online_info_objs[0].ShippingTime,#运输时间
            'parent_sku': Parent_SKU,
            'extra_images': t_online_info_objs[0].ExtraImages,#副图
            
            'productSKU':t_online_info_objs[0].SKU, #商品SKU
        }
        
        first_dict['product'] = first_product_dict
        
        params['first'] = first_dict
        
    second_product_list = []
    for i in range(1,len(t_online_info_objs)) :
        second_product_dict = {}
        
        second_product_dict = {
                #'access_token': access_token_value,
                'format': 'json',
                'parent_sku': Parent_SKU,
                'sku': GET_SHOPSKU(Parent_SKU,t_online_info_objs[i].SKU,i),
                'inventory': 99999,#库存 默认 9999
                'price': float(t_online_info_objs[i].Price.split('.')[0][1:]),#价格
                'shipping': float(t_online_info_objs[i].Shipping.split('.')[0][1:]),#运费
                'color': t_online_info_objs[i].Color,#颜色
                'size': t_online_info_objs[i].Size,#尺寸
                'msrp': float(t_online_info_objs[i].msrp.split('.')[0][1:]),#标签价
                'shipping_time': t_online_info_objs[i].ShippingTime,#运输时间
                
                'productSKU':t_online_info_objs[i].SKU, #商品SKU
        }
            
        second_product_list.append(second_product_dict)
    second_dict['product'] = second_product_list
    second_dict['url'] = 'https://merchant.wish.com/api/v2/variant/add'#变体URL
    params['second'] = second_dict

    json_str = str(params)
    
    return json_str
    
    
def get_joom_data(ProductID,ShopName):
    params = {}
    first_dict = {}
    first_product_dict = {}
    t_online_info_objs = t_online_info_publish_joom.objects.filter(ProductID = ProductID)
    Parent_SKU = GET_PARENT_SKU(ShopName)
    if t_online_info_objs.exists() :
        first_dict['url'] = 'https://api-merchant.joom.com/api/v2/product/add'
        first_product_dict = {
            #'access_token': access_token_value,
            'format': 'json',
            'name': t_online_info_objs[0].Title[0:90],
            'description': t_online_info_objs[0].Description,#描述
            'tags': GET_TAGS(t_online_info_objs[0].Tags),#标签
            'sku': GET_SHOPSKU(Parent_SKU,t_online_info_objs[0].SKU,0),
            'inventory': 99999,
            'price': float(t_online_info_objs[0].Price.split('.')[0][1:]),
            'shipping': float(t_online_info_objs[0].Shipping.split('.')[0][1:]),
            'main_image': t_online_info_objs[0].Image,
            'color': t_online_info_objs[0].Color,
            'size': t_online_info_objs[0].Size,
            'msrp': float(t_online_info_objs[0].msrp.split('.')[0][1:]),
            'shipping_time': t_online_info_objs[0].ShippingTime,#运输时间
            'parent_sku': Parent_SKU,
            'extra_images': t_online_info_objs[0].ExtraImages,#副图
            
            'productSKU':t_online_info_objs[0].SKU, #商品SKU
        }
        
        first_dict['product'] = first_product_dict
        
        params['first'] = first_dict
        
    second_product_list = []
    second_product_dict = {}
    second_dict = {}
    for i in range(1,len(t_online_info_objs)) :
        second_product_dict = {}
        
        second_product_dict = {
                #'access_token': access_token_value,
                'format': 'json',
                'parent_sku': Parent_SKU,
                'sku': GET_SHOPSKU(Parent_SKU,t_online_info_objs[i].SKU,i),
                'inventory': 99999,#库存 默认 9999
                'price': float(t_online_info_objs[i].Price.split('.')[0][1:]),#价格
                'shipping': float(t_online_info_objs[i].Shipping.split('.')[0][1:]),#运费
                'color': t_online_info_objs[i].Color,#颜色
                'size': t_online_info_objs[i].Size,#尺寸
                'msrp': float(t_online_info_objs[i].msrp.split('.')[0][1:]),#标签价
                'shipping_time': t_online_info_objs[i].ShippingTime,#运输时间
                
                'productSKU':t_online_info_objs[i].SKU, #商品SKU
        }
            
        second_product_list.append(second_product_dict)
    second_dict['product'] = second_product_list
    second_dict['url'] = 'https://api-merchant.joom.com/api/v2/variant/add' #变体URL
    params['second'] = second_dict

    json_str = str(params)
    
    return json_str