#-*-coding:utf-8-*-
from skuapp.table.t_all_plateform_code_shopname import *
from skuapp.table.t_template_product_config_amazon import *
from skuapp.table.t_templet_amazon_wait_upload import *
from skuapp.table.t_config_shop_alias import *
from skuapp.table.t_templet_amazon_collection_box import *
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
from skuapp.table.t_config_apiurl_amazon import *
from skuapp.table.t_templet_config_amazon_published import *
from skuapp.table.t_sys_param import *
import urllib, json
from skuapp.table.t_template_product_config_amazon import *
from skuapp.table.t_config_online_amazon import *
from skuapp.table.t_templet_config_amazon_item_type_name import t_templet_config_amazon_item_type_name
from skuapp.table.t_templet_amazon_published_variation import t_templet_amazon_published_variation

from django.contrib import messages
from skuapp.table.t_config_amazon_template import *
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: variation_item_amazon_Plugin.py
 @time: 2017/12/18 15:30
"""
class variation_item_amazon_Plugin(BaseAdminPlugin):
    variation_item_amazon_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.variation_item_amazon_flag)

    def block_before_fieldsets(self, context, nodes):
        all_hide_params = ['item_sku', 'recommended_browse_nodes', 'external_product_id', 'external_product_id_type',
                           'item_name', 'homes_color', 'homes_size',
                           'manufacturer', 'part_number', 'feed_product_type', 'item_type',
                           'product_subtype', 'product_description', 'brand_name', 'update_delete',
                           'item_package_quantity', 'standard_price', 'sale_price', 'sale_from_date',
                           'sale_end_date', 'condition_type', 'quantity', 'merchant_shipping_group_name',
                           'bullet_point1', 'bullet_point2', 'bullet_point3', 'bullet_point4', 'bullet_point5',
                           'generic_keywords', 'main_image_url', 'other_image_url1', 'other_image_url2',
                           'other_image_url3', 'other_image_url4', 'other_image_url5', 'other_image_url6',
                           'other_image_url7', 'other_image_url8', 'fulfillment_center_id', 'model_name',
                           'warranty_description', 'variation_theme', 'model', 'mfg_minimum',
                           'mfg_minimum_unit_of_measure', 'swatch_image_url', 'department_name',
                           'fit_type', 'unit_count', 'unit_count_type', 'fulfillment_latency',
                           'display_dimensions_unit_of_measure', 'generic_keywords1', 'department_name1',
                           'department_name2', 'department_name3', 'department_name4', 'department_name5',
                           'material_type', 'metal_type', 'setting_type', 'ring_size', 'gem_type', 'item_shape',
                           'target_audience_keywords1', 'target_audience_keywords2', 'toy_color', 'jewerly_color',
                           'target_audience_keywords3', 'productSKU','clothing_size', 'clothing_color','number_of_pieces',
                           'item_weight','item_weight_unit','color_name_public','mrp','sleeve_type','item_type_name', 'season',
                           'material_composition', 'included_components', 'are_batteries_included',]
        sourceURL = str(context['request']).split("'")[1]
        all_params_in_url = sourceURL.split('/')
        obj_id = ''
        if all_params_in_url[len(all_params_in_url) - 2] == 'update':
            obj_id = all_params_in_url[len(all_params_in_url) - 3]
        to_url = sourceURL.split('/?')[0]
        url_params = sourceURL.split('/?')
        if to_url.endswith('/'):
            to_url += '?'
        else:
            to_url += '/?'
        groupRoot = ''
        RootID = ''
        recommended_browse_nodes_str = ''
        uploadProductType = ''
        feedPtype = ''
        itemType = ''
        ShopName = ''
        searchSite = ''
        shopAlias = ''
        item_type_name = ''
        template_ama = ''
        if obj_id:
            if all_params_in_url[len(all_params_in_url) - 4] == 't_templet_amazon_wait_upload':
                new_obj = t_templet_amazon_wait_upload.objects.filter(id=int(obj_id))[0]
            if all_params_in_url[len(all_params_in_url) - 4] == 't_templet_amazon_collection_box':
                new_obj = t_templet_amazon_collection_box.objects.filter(id=int(obj_id))[0]
            recommended_browse_nodes_str = new_obj.recommended_browse_nodes
            RootID = new_obj.recommended_browse_nodes_id
            itemType = new_obj.item_type
            uploadProductType = new_obj.upload_product_type
            feedPtype = new_obj.feed_product_type
            ShopName = new_obj.ShopSets
            item_type_name = new_obj.item_type_name
            template_ama = new_obj.merchant_shipping_group_name
            if recommended_browse_nodes_str:
                groupRoot = recommended_browse_nodes_str.split('>')[0]
        if len(url_params) > 1:
            for up in url_params[1].split('&'):
                gR = up.split('=')[0]
                if gR == 'groupRoot':
                    groupRoot = urllib.unquote(up.split('=')[1])
                if gR == 'RootID':
                    RootID = up.split('=')[1]
                if gR == 'recommended_browse_nodes':
                    recommended_browse_nodes_str = urllib.unquote(up.split('=')[1])
                if gR == 'uploadProductType':
                    uploadProductType = up.split('=')[1]
                if gR == 'feedPtype':
                    feedPtype = urllib.unquote(up.split('=')[1])
                if gR == 'itemType':
                    itemType = up.split('=')[1]
                if gR == 'ShopName':
                    ShopName = up.split('=')[1]
                if gR == 'searchSite':
                    searchSite = up.split('=')[1]
        if uploadProductType:
            showParams = eval(t_template_product_config_amazon.objects.filter(product_type=uploadProductType)[0].params)
            for showParam in showParams:
                if showParam in all_hide_params:
                    all_hide_params.remove(showParam);

        if itemType and 'puzzle' in itemType.lower():
            all_hide_params.remove('number_of_pieces')
        searchParams = {'groupRoot':'', 'group2':'', 'group3':'', 'group4':'', 'group5':'', 'group6':'',
                        'group7': '', 'group8':'',}
        searchKeys = ['groupRoot', 'group2', 'group3', 'group4', 'group5', 'group6', 'group7', 'group8']
        if recommended_browse_nodes_str:
            url_searchParams = recommended_browse_nodes_str.split('>')
            for i in range(0,len(url_searchParams)):
                searchParams[searchKeys[i]] = url_searchParams[i].replace('RBNAND', '&')
            recommended_browse_nodes_str = recommended_browse_nodes_str.replace('RBNAND', '&')
        else:
            all_hide_params = []
        sku_length = 0
        shipping_group_sites = {'US': 'Migrated Template', 'DE': 'Standardvorlage Amazon',
                                'FR': 'Modèle par défaut Amazon', 'UK': 'Migrated Template',
                                'AU': 'Migrated Template', 'IN': 'Migrated Template', 'IT': 'Modello Amazon predefinito', 'ES': 'Plantilla de Amazon', 'CA': '',}
        templates = []
        all_shop_names = []
        if searchSite:
            templates = [shipping_group_sites[searchSite]]
            if template_ama is None or template_ama.strip() == '':
                template_ama = shipping_group_sites[searchSite]
            all_shop_name = t_config_shop_alias.objects.filter(ShopName__contains=searchSite).values('ShopName')
            for each_shop_name in all_shop_name:
                all_shop_names.append(each_shop_name['ShopName'])
        else:
            all_shop_name = t_config_shop_alias.objects.values('ShopName')
            for each_shop_name in all_shop_name:
                all_shop_names.append(each_shop_name['ShopName'])

        if ShopName and ShopName[0:3] != '---':
            ShopName = t_config_online_amazon.objects.filter(shop_name=ShopName,site=searchSite)[0].Name
            shopAlias = t_config_shop_alias.objects.filter(ShopName=ShopName)[0].ShopAlias
            templates_amazon = t_config_amazon_template.objects.filter(shopName__exact=ShopName).values('template_name')
            if templates_amazon.exists():
                for template_amazon in templates_amazon:
                    templates.append(template_amazon['template_name'].replace("u'", "'"))
                templates = list(set(templates))
            t_all_plateform_code_shopname_objs = t_all_plateform_code_shopname.objects.filter(ShopName=ShopName).values('Length', 'CurrentNum')
            if t_all_plateform_code_shopname_objs.exists():
                sku_length += int(t_all_plateform_code_shopname_objs[0]['Length']) + len(str(t_all_plateform_code_shopname_objs[0]['CurrentNum']))
        if itemType == '' or itemType is None:
            itemType = t_config_apiurl_amazon.objects.filter(groupRoot=searchParams['groupRoot'],group2=searchParams['group2'],group3=searchParams['group3']
                                                             , group4=searchParams['group4'],group5=searchParams['group5'],group6=searchParams['group6']
                                                             , group7=searchParams['group7'],group8=searchParams['group8'])
            if itemType:
                itemType = itemType.values('item_type')[0]['item_type']
        if templates:
            templates = json.dumps(templates)
        product_types = {}
        all_product_types = []
        all_uploadProductTypes = []
        all_item_type_names = []
        t_template_product_config_amazon_objs = t_template_product_config_amazon.objects.filter(site='US')
        all_uploadProductType = t_template_product_config_amazon_objs.values('product_type')
        for each_uploadProductType in all_uploadProductType:
            all_uploadProductTypes.append(each_uploadProductType['product_type'])
        if uploadProductType and feedPtype:
            item_type_name_info = t_templet_config_amazon_item_type_name.objects.filter(product_type=uploadProductType, feed_product_type=feedPtype).values('item_type_name')
            if item_type_name_info:
                item_type_name_info = item_type_name_info[0]['item_type_name']
                if item_type_name_info:
                    all_item_type_names = eval(item_type_name_info)

        if uploadProductType:
            t_template_product_config_amazon_obj = t_template_product_config_amazon_objs.filter(product_type=uploadProductType)[0]
            if t_template_product_config_amazon_obj:
                feed_product_type = t_template_product_config_amazon_obj.feed_product_type
                if feed_product_type:
                    for fpt in eval(feed_product_type):
                        all_product_types.append(fpt)
                    feed_product_type = feed_product_type.replace('[', '').replace(']', '').replace("'", '')
                product_types[t_template_product_config_amazon_obj.product_type] = feed_product_type
        sourceURLs = sourceURL.split('/?')
        searchList = ['ShopName=','searchSite=', '_p_status=NO', '_p_status=FAILED']
        searchStr = ''
        if len(sourceURLs) >1:
            new_sourceURLs = sourceURLs[1].split('&')
            for new_search in searchList:
                for new_sourceURL in new_sourceURLs:
                    if new_search in new_sourceURL:
                        searchStr += new_sourceURL+'&'
        nodes.append(loader.render_to_string('select_product_type_amazon_Plugin.html',
                                             {'all_hide_params': all_hide_params, 'to_url': to_url, 'RootID': RootID, 'product_types': product_types,
                                              'groupRoot': groupRoot, 'recommended_browse_nodes_str': recommended_browse_nodes_str,'sourceURLs': sourceURL,
                                              'all_product_types': all_product_types, 'uploadProductType': uploadProductType, 'sourceURL': searchStr[:-1],
                                              'feedPtype': feedPtype, 'itemType': itemType, 'ShopName': ShopName, 'shopAlias': shopAlias, 'sku_length': sku_length,
                                              'all_uploadProductTypes': all_uploadProductTypes,'searchSite':searchSite, 'all_shop_names': all_shop_names,
                                              'item_type_name': item_type_name, 'all_item_type_names': all_item_type_names, 'templates': templates, 'template_ama': template_ama,}))

    def block_after_fieldsets(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]
        url_params = sourceURL.split('/?')
        feedPtype = ''
        all_params_in_url = sourceURL.split('/')
        update_flag = '0'
        uploadProductType = ''
        variantion_theme_selected = ''
        product_variations_tmp = []
        if all_params_in_url[len(all_params_in_url) - 2] == 'update':
            update_flag = '1'
            product_id = all_params_in_url[len(all_params_in_url) - 3]
            prodcut_variation_id = t_templet_amazon_collection_box.objects.filter(id=product_id)[0].prodcut_variation_id
            product_variations = t_templet_amazon_published_variation.objects.filter(prodcut_variation_id=prodcut_variation_id)

            for product_variation in product_variations:
                product_variation_dict = {}
                product_variation_dict['price'] = str(product_variation.price)
                product_variation_dict['main_image_url'] = str(product_variation.main_image_url)
                product_variation_dict['other_image_url1'] = str(product_variation.other_image_url1)
                product_variation_dict['other_image_url2'] = str(product_variation.other_image_url2)
                product_variation_dict['other_image_url3'] = str(product_variation.other_image_url3)
                product_variation_dict['other_image_url4'] = str(product_variation.other_image_url4)
                product_variation_dict['other_image_url5'] = str(product_variation.other_image_url5)
                product_variation_dict['other_image_url6'] = str(product_variation.other_image_url6)
                product_variation_dict['other_image_url7'] = str(product_variation.other_image_url7)
                product_variation_dict['other_image_url8'] = str(product_variation.other_image_url8)
                product_variation_dict['productSKU'] = str(product_variation.productSKU)
                product_variation_dict['color_name'] = str(product_variation.color_name)
                product_variation_dict['MetalType'] = str(product_variation.MetalType)
                product_variation_dict['size_name'] = str(product_variation.size_name)
                product_variation_dict['item_quantity'] = str(product_variation.item_quantity)
                product_variations_tmp.append(product_variation_dict)
            if product_variations.exists():
                variantion_theme_selected = product_variations[0].variation_theme
        if len(url_params) > 1:
            for up in url_params[1].split('&'):
                gR = up.split('=')[0]
                if gR == 'feedPtype':
                    feedPtype = urllib.unquote(up.split('=')[1])
                if gR == 'uploadProductType':
                    uploadProductType = up.split('=')[1]
        size_color_list = ["Hardware", "Tools", "MajorHomeAppliances", "OrganizersAndStorage"]
        color_list = ["LightsAndFixtures", "OfficePhone", "OfficePrinter", "OfficeScanner", "VoiceRecorder",
                      "PowersportsVehicle",
                      "Autooil", "CleaningOrRepairKit", "Autobattery", "WirelessAccessories",
                      "BrassAndWoodwindInstruments", "Guitars", "KeyboardInstruments",
                      "MiscWorldInstruments", "SoundAndRecordingEquipment"]
        color_metalType_list = ["FineOther", "FineEarring", "FineNecklaceBraceletAnklet", "FashionOther",
                                "FashionEarring", "FashionNecklaceBraceletAnklet"]
        jewelry_list = []
        size_metalType_list = ["FineRing", "FashionRing"]
        # 无变体的product_type
        no_variation_type = ["Antenna","AudioVideoAccessory","AVFurniture","BarCodeReader","CEBinocular","CECamcorder","CameraBagsAndCases","CEBattery","CEBlankMedia","CableOrAdapter","CECameraFlash","CameraLenses","CameraOtherAccessories","CameraPowerSupply","CarAlarm","CarAudioOrTheater","CarElectronics","CEDigitalCamera","DigitalPictureFrame","DigitalVideoRecorder","DVDPlayerOrRecorder","CEFilmCamera","GPSOrNavigationAccessory","GPSOrNavigationSystem","HandheldOrPDA","Headphones","HomeTheaterSystemOrHTIB","MediaPlayer","MediaPlayerOrEReaderAccessory","MediaStorage","MiscAudioComponents","Phone","PhoneAccessory","PhotographicStudioItems","PortableAudio","PortableAvDevice","PowerSuppliesOrProtection","RadarDetector","RadioOrClockRadio","ReceiverOrAmplifier","RemoteControl","Speakers","StereoShelfSystem","CETelescope","Television","Tuner","TVCombos","TwoWayRadio","VCR","CEVideoProjector","VideoProjectorsAndAccessories"]
        select_type = 0
        if feedPtype:
            if feedPtype in size_color_list:
                select_type = 1
            if feedPtype in color_list:
                select_type = 2
            if feedPtype in color_metalType_list:
                select_type = 3
            if feedPtype in jewelry_list:
                select_type = 4
            if feedPtype in size_metalType_list:
                select_type = 5
            if feedPtype in no_variation_type:
                select_type = -1
        if uploadProductType == 'ClothingAccessories':
            select_type = 6
        t_sys_param_objs = t_sys_param.objects.filter(Type=307).values('V', 'VDesc')
        variationItems = {}
        for t_sys_param_obj in t_sys_param_objs:
            variationItems[t_sys_param_obj['V']] = t_sys_param_obj['VDesc']
        sourceURLs = sourceURL.split('/?')
        searchList = ['ShopName=', 'searchSite=']
        searchStr = ''
        if len(sourceURLs) > 1:
            new_sourceURLs = sourceURLs[1].split('&')
            for new_search in searchList:
                for new_sourceURL in new_sourceURLs:
                    if new_search in new_sourceURL:
                        searchStr += new_sourceURL + '&'

        nodes.append(loader.render_to_string('variation_item_amazon_Plugin.html',
                                             {'variationItems': variationItems,'select_type': select_type,'update_flag': update_flag,
                                              'sourceURL': searchStr[:-1],'sourceURLs': sourceURL, 'variantion_theme_selected': variantion_theme_selected,
                                              'product_variations': product_variations_tmp}))