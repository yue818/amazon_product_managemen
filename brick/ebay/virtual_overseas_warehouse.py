# coding=utf-8

"""
description: eBay虚拟海外仓自动上下架
author: szc
"""


from skuapp.table.t_online_info_ebay import t_online_info_ebay
from skuapp.table.t_online_info_ebay_subsku import t_online_info_ebay_subsku
from app_djcelery.tasks import relist_end_item_ebayapp

# 真实海外仓 Lacation
ZSHWCL = [
    'Ottendorf-Okrilla', 'Rowland Heights,CA/Dayton,NJ', 'Rowland Heights, California', 'Dayton, New Jersey',
    'Dandenong', 'Walsall', 'Leicestershire'
]


def get_vow_details():
    """获取虚拟海外仓itemid基本信息"""
    itemid_list = []
    item_detail_dict = {}
    no_variations_item_detail_dict = {}
    t_online_info_ebay_objs = t_online_info_ebay.objects.exclude(Location__in=ZSHWCL).exclude(Country='CN').filter(
        status='Active', dostatus='doSuccess', isnormal='normal').values(
        'itemid', 'ShopName', 'site', 'isVariations', 'UseNumber', 'realavailable', 'Productstatus', 'SKU', 'sold', 'profitrate')

    for t_online_info_ebay_obj in t_online_info_ebay_objs:
        itemid = t_online_info_ebay_obj['itemid']
        shopname = t_online_info_ebay_obj['ShopName']
        site = t_online_info_ebay_obj['site']
        isV = t_online_info_ebay_obj['isVariations']
        isVariations = isV.lower() if isV else 'no'
        if isVariations == 'yes':
            itemid_list.append(itemid)
            item_detail_dict[itemid] = {
                'shopname': shopname,
                'site': site,
                'isVariations': isVariations
            }
        else:
            no_variations_item_detail_dict[itemid] = {
                'shopname': shopname,
                'site': site,
                'isVariations': isVariations,
                'SKU': t_online_info_ebay_obj['SKU'],
                'sold': t_online_info_ebay_obj['sold'],
                'Productstatus': t_online_info_ebay_obj['Productstatus'],
                'UseNumber': t_online_info_ebay_obj['UseNumber'],
                'realavailable': t_online_info_ebay_obj['realavailable'],
                'profitrate': t_online_info_ebay_obj['profitrate']
            }
    return itemid_list, item_detail_dict, no_variations_item_detail_dict


def get_param(item_id, sku, isVariations, sold, Quantity, ShopName, Site, vowOperation, Type, Operator):
    """格式化需要上下架的参数"""
    reviseData = [
        {
            'ItemID': item_id,
            'SKU': sku,
            'isVariations': isVariations,
            'realQuantity': sold + Quantity,
            'sold': sold,
            'Quantity': Quantity
        }
    ]

    param = {
        'ShopName': ShopName,
        'Site': Site,
        'vowOperation': vowOperation,
        'Type': Type,
        'Operator': Operator,
        'reviseData': reviseData
    }
    return param


def vow_off_shelf(itemid_list, item_detail_dict, no_variations_item_detail_dict):
    """虚拟海外仓下架"""
    vowOperation = 'off'
    Type = 'endItemSKU'
    Operator = 'system'
    Quantity = 0

    # 存在变体的虚拟海外仓下架
    ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(itemid__in=itemid_list).values(
        'sold', 'itemid', 'subSKU', 'UseNumber', 'realavailable', 'productstatus')
    params_list = []
    if ebay_subsku_objs.exists():
        for ebay_subsku_obj in ebay_subsku_objs:
            off_flag = 0
            if ebay_subsku_obj['UseNumber'] is not None:
                if (ebay_subsku_obj['productstatus'] in ['2', '3', '4']) and (ebay_subsku_obj['realavailable'] > 0):
                    off_flag = 1
                if (ebay_subsku_obj['UseNumber'] <= 0) and (ebay_subsku_obj['realavailable'] > 0):
                    off_flag = 1
            if off_flag == 1:
                item_id = ebay_subsku_obj['itemid']
                sold = int(ebay_subsku_obj['sold']) if ebay_subsku_obj['sold'] else 0
                sku = ebay_subsku_obj['subSKU']

                item_info = item_detail_dict.get(item_id, '')
                if item_info:
                    param = get_param(
                        item_id=item_id, sku=sku, isVariations=item_info['isVariations'], sold=sold, Quantity=Quantity,
                        ShopName=item_info['shopname'], Site=item_info['site'], vowOperation=vowOperation, Type=Type,
                        Operator=Operator
                    )
                    params_list.append(param)
        relist_end_item_ebayapp(params=params_list)

    # 不存在变体的虚拟海外仓下架
    params_list_2 = []
    for key, val in no_variations_item_detail_dict.items():
        off_flag = 0
        if val['UseNumber']:
            if (val['Productstatus'] in ['2', '3', '4']) and (val['realavailable'] > 0):
                off_flag = 1
            if (val['UseNumber'] <= 0) and (val['realavailable'] > 0):
                off_flag = 1
        if off_flag == 1:
            sold = int(val['sold']) if val['sold'] else 0
            param_2 = get_param(
                item_id=key, sku=val['SKU'], isVariations=val['isVariations'], sold=sold, Quantity=Quantity,
                ShopName=val['shopname'], Site=val['site'], vowOperation=vowOperation, Type=Type, Operator=Operator
            )
            params_list_2.append(param_2)
    if params_list_2:
        relist_end_item_ebayapp(params=params_list_2)


def vow_on_shelf(itemid_list, item_detail_dict, no_variations_item_detail_dict):
    """虚拟海外仓上架"""
    vowOperation = 'on'
    Type = 'ReListItemSKU'
    Operator = 'system'

    # 存在变体的虚拟海外仓上架
    ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(
        UseNumber__gt=0, realavailable__lte=0, productstatus=1, profitrate__gt=0, profitrate__isnull=False,
        itemid__in=itemid_list
    ).values('sold', 'itemid', 'subSKU', 'realavailable')
    params_list = []
    if ebay_subsku_objs.exists():
        for ebay_subsku_obj in ebay_subsku_objs:
            item_id = ebay_subsku_obj['itemid']
            sold = int(ebay_subsku_obj['sold']) if ebay_subsku_obj['sold'] else 0
            sku = ebay_subsku_obj['subSKU']
            realavailable = ebay_subsku_obj['realavailable'] if ebay_subsku_obj['realavailable'] else 0

            item_info = item_detail_dict.get(item_id, '')
            if item_info:
                quantity = realavailable + 1 if realavailable > 0 else 5
                param = get_param(
                    item_id=item_id, sku=sku, isVariations=item_info['isVariations'], sold=sold, Quantity=quantity,
                    ShopName=item_info['shopname'], Site=item_info['site'], vowOperation=vowOperation, Type=Type,
                    Operator=Operator
                )
                params_list.append(param)
        relist_end_item_ebayapp(params=params_list)

    # 不存在变体的虚拟海外仓下架
    params_list_2 = []
    for key, val in no_variations_item_detail_dict.items():
        if (val['Productstatus'] == '1') and (val['UseNumber'] > 0) and (val['realavailable'] <= 0) and (val['profitrate'] > 0):
            sold = int(val['sold']) if val['sold'] else 0
            quantity = val['realavailable'] + 1 if val['realavailable'] > 0 else 5
            param_2 = get_param(
                item_id=key, sku=val['SKU'], isVariations=val['isVariations'], sold=sold, Quantity=quantity,
                ShopName=val['shopname'], Site=val['site'], vowOperation=vowOperation, Type=Type, Operator=Operator
            )
            params_list_2.append(param_2)
    if params_list_2:
        relist_end_item_ebayapp(params=params_list_2)


def vow_shelf_enter():
    """虚拟海外仓上下架入口"""
    itemid_list, item_detail_dict, no_variations_item_detail_dict = get_vow_details()
    if itemid_list:
        vow_off_shelf(itemid_list, item_detail_dict, no_variations_item_detail_dict)
        vow_on_shelf(itemid_list, item_detail_dict, no_variations_item_detail_dict)