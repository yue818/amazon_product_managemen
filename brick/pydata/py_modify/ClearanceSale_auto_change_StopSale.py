# coding=utf-8


from datetime import datetime
from skuapp.table.t_product_information_modify import t_product_information_modify
from pyapp.table.kc_currentstock_sku import kc_currentstock_sku
from pyapp.models import b_goods, b_goodscats


DESCRIPTION = u'库存和销量为零，清仓自动转停售，无需审核'

def main():
    all_sku_dict = {}

    kc_currentstock_sku_objs = kc_currentstock_sku.objects.filter(GoodsStatus=u'清仓', Number=0, SellCount1=0).values('MainSKU', 'SKU').order_by('MainSKU')
    if kc_currentstock_sku_objs.exists():
        for kc_currentstock_sku_obj in kc_currentstock_sku_objs:
            mainsku = str(kc_currentstock_sku_obj['MainSKU'])
            sonsku = str(kc_currentstock_sku_obj['SKU'])
            if all_sku_dict.get(mainsku, ''):
                all_sku_dict[mainsku].append(sonsku)
            else:
                all_sku_dict[mainsku] = [sonsku]

    for main_sku , sku_list in all_sku_dict.items():
        goods_name = ''
        alias_en_name = ''
        alias_cn_name = ''
        source_path = ''
        material = ''
        dev_date = None
        large_category = ''
        small_category = ''
        details = {}
        input_box = ','.join(sku_list)

        modify_sku = ''
        exists_flag = 0
        for sku in sku_list:
            b_goods_objs = b_goods.objects.filter(SKU=sku)
            if b_goods_objs.exists() and exists_flag == 0:
                goods_name = b_goods_objs[0].GoodsName
                alias_en_name = b_goods_objs[0].AliasEnName
                alias_cn_name = b_goods_objs[0].AliasCnName
                material = b_goods_objs[0].Material
                dev_date = b_goods_objs[0].DevDate
                category_code = b_goods_objs[0].CategoryCode
                source_path = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % sku.replace('OAS-','').replace('FBA-', '')

                if len(category_code) >= 3:
                    b_goodscats_objs = b_goodscats.objects.filter(CategoryCode='|'.join(category_code))
                    if b_goodscats_objs.exists():
                        if category_code[2].strip() != '':
                            large_category = b_goodscats_objs[0].CategoryParentName
                            small_category = b_goodscats_objs[0].CategoryName
                        else:
                            large_category = b_goodscats_objs[0].CategoryName
                modify_sku = sku
                exists_flag = 1

            details[sku] = {u'GoodsStatus': [u'当前状态', u'清仓', u'停售(无需审核)', DESCRIPTION, u'停售(无需审核)']}

        t_product_information_modify.objects.create(
            MainSKU=main_sku, Details=details, SKU=modify_sku, Name2=goods_name, Keywords=alias_en_name,
            Keywords2=alias_cn_name, SourcePicPath2=source_path, Material=material, DevDate=dev_date,
            LargeCategory=large_category, SmallCategory=small_category, InputBox=input_box, XGcontext='', Mstatus='DLQ',
            Select=23, SQTimeing=datetime.now(), Source=u'普源信息', SQStaffNameing=u'系统'
        )