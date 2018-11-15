# coding=utf-8


from skuapp.modelsadminx.t_online_info_wish_Admin import *
from skuapp.table.t_templet_joom_collection_box import t_templet_joom_collection_box
from skuapp.table.t_online_info import t_online_info
from datetime import datetime
from brick.classredis.classsku import classsku
classsku_obj = classsku()


def char_process(param):
    if param == None:
        result = ''
    else:
        result = param.replace('"', '`').replace("'", '`')

    result = result.replace("&#39;", "'").replace("&amp;", "&").replace("\\/", '/').replace("&quot;", '`')
    return result


def create_wish_collection_box(request, productID, MainSKU):
    """生成WISH采集箱"""
    if MainSKU == 'None':
        messages.info(request, '--------------------商品SKU未绑定！！！')
    elif ',' in MainSKU:
        messages.info(request, '--------------------组合链接不支持铺货！！！')
    collection_box_objs = t_templet_joom_collection_box.objects.filter(MainSKU=MainSKU)
    if collection_box_objs.exists():
        messages.error(request, '请勿重复采集MainSKU:%s' % MainSKU)
    else:
        online_info_objs = t_online_info.objects.filter(ProductID=productID).extra(select={'price':'Price+0'}).order_by('price')
        if online_info_objs.exists():
            Title = char_process(online_info_objs[0].Title)
            Description = char_process(online_info_objs[0].Description)
            Tags = char_process(online_info_objs[0].Tags)
            MainImage = online_info_objs[0].Image
            ExtraImages = online_info_objs[0].ExtraImages
            SrcProductID = online_info_objs[0].ProductID

            # 变体信息
            Variants = []
            # 普源SKU对应商品状态
            sku_state = {}
            # 克重、成本价, 数据格式是[{sku:{'cost_price':CostPrice, 'weight':Weight}}, ……]
            b_cost_weight = []

            for obj in online_info_objs:
                Variant = {}
                VariantDict = {}

                sku = obj.SKU
                st = classsku_obj.get_goodsstatus_by_sku(sku=sku)
                sku_state[sku] = st
                cost_weight = {
                    'cost_price': str(classsku_obj.get_price_by_sku(sku=sku)),
                    'weight': str(classsku_obj.get_weight_by_sku(sku=sku))
                }
                sku_cost_weight = {sku: cost_weight}
                b_cost_weight.append(sku_cost_weight)
                VariantDict['sku'] = obj.ShopSKU
                VariantDict['productSKU'] = obj.SKU
                if obj.ShopSKUImage is None:
                    VariantDict['main_image'] = ''
                else:
                    VariantDict['main_image'] = obj.ShopSKUImage.replace('\\', '')
                VariantDict['color'] = char_process(obj.Color)
                VariantDict['size'] = char_process(obj.Size)
                VariantDict['price'] = float(obj.Price)
                VariantDict['shipping'] = float(obj.Shipping)
                VariantDict['inventory'] = '9999'
                VariantDict['msrp'] = obj.msrp
                VariantDict['shipping_time'] = '7-25'
                VariantDict['format'] = 'json'
                VariantDict['parent_sku'] = ''
                if obj.Status == 'Enabled':
                    enabled = True
                else:
                    enabled = False
                VariantDict['enabled'] = enabled
                Variant['Variant'] = VariantDict
                Variants.append(Variant)
            time = datetime.now()
            user = request.user.first_name
            t_templet_joom_collection_box.objects.create(
                MainSKU=MainSKU, Title=Title, Description=Description, Tags=Tags, MainImage=MainImage,
                ExtraImages=ExtraImages, B_cost_weight=b_cost_weight, Variants=Variants, CreateTime=time, CreateStaff=user,
                Status='0', Source='COLLECT', UpdateTime=time, UpdateStaff=user, SrcProductID=SrcProductID,
                SkuState=sku_state
            )
            messages.info(request, 'MainSKU: %s采集成功' % MainSKU)


class t_templet_public_joom_listing_Admin(t_online_info_wish_Admin):
    plateform_distribution_navigation = True
    search_flag = False
    search_box_flag = True
    wish_listing_readonly_f = False
    wish_listing_secondplugin = False
    actions = ['do_action']

    def do_action(self, request, queryset):
        for obj in queryset.all():
            productID = obj.ProductID
            mainsku = obj.MainSKU
            create_wish_collection_box(self.request, productID, mainsku)
    do_action.short_description = u'采集箱'


    def show_orders7days(self,obj) :
        rt =  "<a id=show_orderlist_%s>日销量</a><script>$('#show_orderlist_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1000px','600px'],content:'/t_online_info_wish/order1day/?aID=%s',});});</script>"%(obj.id,obj.id,obj.ProductID)
        rt += '<br><br><a href="/create_wish_collection_box/?productID=%s&mainsku=%s&plate=joom">采集箱</a>' % (obj.ProductID, obj.MainSKU)
        return mark_safe(rt)
    show_orders7days.short_description = u'&nbsp;&nbsp;操&nbsp;作&nbsp;&nbsp;'