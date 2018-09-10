#-*-coding:utf-8-*-
import xml.dom.minidom
import time,json,datetime
from brick.public import local2utcTime
from skuapp.table.t_config_apiurl_amazon import *
import logging
import logging.handlers
import datetime
"""  
 @desc:  
 @author: yewangping叶王平
 @site: 
 @software: PyCharm
 @file: stitch_MQ_body.py
 @time: 2017/12/23 8:34
"""

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='/tmp/test_rabbitmq.log',
                    filemode='a')

logging.handlers.RotatingFileHandler('/tmp/test_rabbitmq.log',
                                     maxBytes=100 * 1024 * 1024,
                                     backupCount=10)

class stitch_MQ_body():
    def __init__(self):
        pass

    def is_Toys(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        Toys = doc.createElement('Toys')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        ProductType = doc.createElement('ProductType')
        # ProductType_child = doc.createElement(toy_upload_obj.feed_product_type)
        ToysAndGames = doc.createElement('ToysAndGames')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        Size = doc.createElement('Size')
        SizeMap = doc.createElement('SizeMap')
        CountryString = doc.createElement('CountryString')
        AgeRecommendation = doc.createElement('AgeRecommendation')
        MinimumManufacturerAgeRecommended = doc.createElement('MinimumManufacturerAgeRecommended')
        MinimumManufacturerAgeRecommended.setAttribute('unitOfMeasure', str(goods_upload_obj['mfg_minimum_unit_of_measure']))

        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if variation_theme == 'Size-Color':
                variation_theme = 'SizeColor'
            VariationTheme_text = doc.createTextNode(variation_theme)

        if params['parent_child'] == 'child':
            Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
            ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
            Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
            SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])

        CountryString_text = doc.createTextNode('EN')
        MinimumManufacturerAgeRecommended_text = doc.createTextNode(goods_upload_obj['mfg_minimum'])

        if params['variation'] == 1:
            Parentage.appendChild(Parentage_text)
            VariationTheme.appendChild(VariationTheme_text)

        if params['parent_child'] == 'child':
            Color.appendChild(Color_text)
            ColorMap.appendChild(ColorMap_text)
            Size.appendChild(Size_text)
            SizeMap.appendChild(SizeMap_text)

        CountryString.appendChild(CountryString_text)
        # ManufacturerWarrantyDescription.appendChild(ManufacturerWarrantyDescription_text)
        MinimumManufacturerAgeRecommended.appendChild(MinimumManufacturerAgeRecommended_text)

        if params['variation'] == 1:
            VariationData.appendChild(Parentage)
            VariationData.appendChild(VariationTheme)

        if params['parent_child'] == 'child' and goods_upload_variation_obj['color_name']:
            ToysAndGames.appendChild(Color)
            ToysAndGames.appendChild(ColorMap)
        else:
            if goods_upload_obj['toy_color']:
                Color_text = doc.createTextNode(goods_upload_obj['toy_color'])
                ColorMap_text = doc.createTextNode(goods_upload_obj['toy_color'])
                Color.appendChild(Color_text)
                ColorMap.appendChild(ColorMap_text)
                ToysAndGames.appendChild(Color)
                ToysAndGames.appendChild(ColorMap)
        ToysAndGames.appendChild(CountryString)
        ProductType.appendChild(ToysAndGames)
        AgeRecommendation.appendChild(MinimumManufacturerAgeRecommended)
        if params['variation'] == 1:
            Toys.appendChild(VariationData)
        Toys.appendChild(ProductType)
        Toys.appendChild(AgeRecommendation)

        if goods_upload_obj['item_type'] and 'puzzle' in goods_upload_obj['item_type'].lower():
            pieces_node = doc.createElement('NumberOfPieces')
            pieces_node_text = doc.createTextNode(str(goods_upload_obj['number_of_pieces']))
            pieces_node.appendChild(pieces_node_text)
            Toys.appendChild(pieces_node)

        if params['variation'] == 1:
            if params['parent_child'] == 'child' and goods_upload_variation_obj['size_name']:
                Toys.appendChild(Size)
                Toys.appendChild(SizeMap)
        return Toys

    def is_Home(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        Home = doc.createElement('Home')
        ProductType = doc.createElement('ProductType')
        Parentage = doc.createElement('Parentage')
        VariationData = doc.createElement('VariationData')
        VariationTheme = doc.createElement('VariationTheme')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        Size = doc.createElement('Size')
        SizeMap = doc.createElement('SizeMap')
        Material = doc.createElement('Material')
        ProductType_child = doc.createElement(goods_upload_obj['feed_product_type'])
        if goods_upload_obj['homes_color']:
            ColorMap_text = doc.createTextNode(goods_upload_obj['homes_color'])
            ColorMap.appendChild(ColorMap_text)
            Color_text = doc.createTextNode(goods_upload_obj['homes_color'])
            Color.appendChild(Color_text)
        if goods_upload_obj['homes_size']:
            Size_text = doc.createTextNode(goods_upload_obj['homes_size'])
            SizeMap_text = doc.createTextNode(goods_upload_obj['homes_size'])
            Size.appendChild(Size_text)
            SizeMap.appendChild(SizeMap_text)
        if params['parent_child'] == 'child' and goods_upload_variation_obj['color_map']:
            ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
            ColorMap.appendChild(ColorMap_text)
            Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
            Color.appendChild(Color_text)

        if goods_upload_obj['feed_product_type'] == 'SeedsAndPlants':
            ProductType_child_param = doc.createElement('AgeRangeDescription')
            ProductType_child_param_text = doc.createTextNode('Over three years old')
            ProductType_child_param.appendChild(ProductType_child_param_text)
        elif goods_upload_obj['feed_product_type'] == 'Art':
            ProductType_child_param = doc.createElement('PieceCount')
            ProductType_child_param_text = doc.createTextNode('1')
            ProductType_child_param.appendChild(ProductType_child_param_text)
        else:
            ProductType_child_param = doc.createElement('NumberOfSets')
            ProductType_child_param_text = doc.createTextNode('1')
            ProductType_child_param.appendChild(ProductType_child_param_text)
        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            VariationTheme_text = doc.createTextNode(goods_upload_variation_obj['variation_theme'])
        if params['parent_child'] == 'child' and goods_upload_variation_obj['size_name']:
            Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
            SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])
            Size.appendChild(Size_text)
            SizeMap.appendChild(SizeMap_text)
        if params['variation'] == 1:
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(VariationTheme)
            if params['parent_child'] == 'child':
                if goods_upload_variation_obj['size_name'] or goods_upload_obj['homes_size']:
                    VariationData.appendChild(Size)
                if goods_upload_variation_obj['color_name'] or goods_upload_obj['homes_color']:
                    VariationData.appendChild(Color)
                    ProductType_child.appendChild(ColorMap)
        else:
            if goods_upload_obj['homes_size']:
                VariationData.appendChild(Size)
            if goods_upload_obj['homes_color']:
                VariationData.appendChild(Color)
                ProductType_child.appendChild(ColorMap)
        if goods_upload_obj['material_type']:
            Material_text = doc.createTextNode(goods_upload_obj['material_type'])
            Material.appendChild(Material_text)
            ProductType_child.appendChild(Material)
        ProductType_child.appendChild(ProductType_child_param)
        ProductType.appendChild(ProductType_child)
        Home.appendChild(ProductType)
        if params['variation'] == 1:
            Home.appendChild(Parentage)
            Home.appendChild(VariationData)
        else:
            if goods_upload_obj['homes_color']:
                Home.appendChild(VariationData)
        if params['parent_child'] == 'child':
            if goods_upload_variation_obj['size_name']:
                Home.appendChild(SizeMap)
        return Home

    def is_ClothingAccessories(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        ClothingAccessories = doc.createElement('ClothingAccessories')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        Size = doc.createElement('Size')
        Color = doc.createElement('Color')
        VariationTheme = doc.createElement('VariationTheme')
        ClassificationData = doc.createElement('ClassificationData')
        DepartmentName = doc.createElement('Department')
        Theme = doc.createElement('Theme')
        ColorMap = doc.createElement('ColorMap')
        SizeMap = doc.createElement('SizeMap')

        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if variation_theme == 'Size-Color':
                variation_theme = 'SizeColor'
            VariationTheme_text = doc.createTextNode(variation_theme)
        if params['parent_child'] == 'child':
            Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
            Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
            SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])
            ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
            ColorMap.appendChild(ColorMap_text)
            Color.appendChild(Color_text)
            Size.appendChild(Size_text)
            SizeMap.appendChild(SizeMap_text)

        if params['variation'] == 1:
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            if params['parent_child'] == 'child':
                if goods_upload_variation_obj['size_name']:
                    VariationData.appendChild(Size)
                if goods_upload_variation_obj['color_name']:
                    VariationData.appendChild(Color)
            VariationData.appendChild(VariationTheme)
            ClothingAccessories.appendChild(VariationData)
        else:
            clothing_color_text = doc.createTextNode(goods_upload_obj['clothing_color'])
            clothing_size_text = doc.createTextNode(goods_upload_obj['clothing_size'])
            clothing_colorMap_text = doc.createTextNode(goods_upload_obj['clothing_color'])
            clothing_sizeMap_text = doc.createTextNode(goods_upload_obj['clothing_size'])
            ColorMap.appendChild(clothing_colorMap_text)
            Color.appendChild(clothing_color_text)
            Size.appendChild(clothing_size_text)
            SizeMap.appendChild(clothing_sizeMap_text)
            VariationData.appendChild(Size)
            VariationData.appendChild(Color)
            ClothingAccessories.appendChild(VariationData)
        DepartmentName_text = doc.createTextNode(goods_upload_obj['department_name1'])
        DepartmentName.appendChild(DepartmentName_text)
        ClassificationData.appendChild(DepartmentName)
        if params['variation'] == 1:
            if params['parent_child'] == 'child':
                if goods_upload_variation_obj['color_name']:
                    ClassificationData.appendChild(ColorMap)
                if goods_upload_variation_obj['size_name']:
                    ClassificationData.appendChild(SizeMap)
        else:
            ClassificationData.appendChild(ColorMap)
            ClassificationData.appendChild(SizeMap)
        Theme_text = doc.createTextNode('well done')
        Theme.appendChild(Theme_text)
        ClassificationData.appendChild(Theme)
        ClothingAccessories.appendChild(ClassificationData)
        return ClothingAccessories

    def is_HomeImprovement(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        HomeImprovement = doc.createElement('HomeImprovement')
        ProductType = doc.createElement('ProductType')
        ProductType_child = doc.createElement(goods_upload_obj['feed_product_type'])
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        Size = doc.createElement('Size')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        SellerWarrantyDescription = doc.createElement('SellerWarrantyDescription')
        SellerWarrantyDescription_text = doc.createTextNode('Be careful')
        SellerWarrantyDescription.appendChild(SellerWarrantyDescription_text)
        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            VariationTheme_text = doc.createTextNode(goods_upload_variation_obj['variation_theme'])
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            VariationData.appendChild(VariationTheme)
            ProductType_child.appendChild(VariationData)
            if params['parent_child'] == 'child':
                Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                ColorMap.appendChild(ColorMap_text)
                Color.appendChild(Color_text)
                Size.appendChild(Size_text)
                if goods_upload_variation_obj['size_name']:
                    ProductType_child.appendChild(Size)
                if goods_upload_variation_obj['color_name']:
                    ProductType_child.appendChild(Color)
                    ProductType_child.appendChild(ColorMap)
        ProductType_child.appendChild(SellerWarrantyDescription)
        ProductType.appendChild(ProductType_child)
        HomeImprovement.appendChild(ProductType)
        return HomeImprovement

    def is_Jewelry(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        item_shape_need_list = ['Watch','FashionNecklaceBraceletAnklet','FashionEarring',
                                'FashionOther','FineNecklaceBraceletAnklet','FineEarring','FineOther']
        Jewelry = doc.createElement('Jewelry')
        ProductType = doc.createElement('ProductType')
        Color = doc.createElement('Color')
        Size = doc.createElement('Size')
        SizeMap = doc.createElement('SizeMap')
        ColorMap = doc.createElement('ColorMap')
        DepartmentName = doc.createElement('DepartmentName')
        ProductType_child = doc.createElement(goods_upload_obj['feed_product_type'])
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        Stone = doc.createElement('Stone')
        GemType = doc.createElement('GemType')
        RingSize = doc.createElement('RingSize')
        MetalType = doc.createElement('MetalType')
        Material = doc.createElement('Material')
        ItemShape = doc.createElement('ItemShape')
        SellerWarrantyDescription = doc.createElement('SellerWarrantyDescription')
        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if goods_upload_obj['feed_product_type'] == 'Watch':
                if variation_theme == 'Size':
                    variation_theme = 'SizeName'
                if variation_theme == 'Size-Color':
                    variation_theme = 'SizeName-ColorName'
                VariationTheme_text = doc.createTextNode(variation_theme)
                VariationTheme.appendChild(VariationTheme_text)
                Parentage.appendChild(Parentage_text)
                VariationData.appendChild(Parentage)
                VariationData.appendChild(VariationTheme)
                ProductType_child.appendChild(VariationData)
            else:
                if variation_theme == 'Size-Color':
                    variation_theme = 'Color-RingSize'
                if 'Size' in variation_theme:
                    variation_theme = variation_theme.replace('Size', 'RingSize')
                VariationTheme_text = doc.createTextNode(variation_theme)
                VariationTheme.appendChild(VariationTheme_text)
                Parentage.appendChild(Parentage_text)
                VariationData.appendChild(Parentage)
                VariationData.appendChild(VariationTheme)
                if params['parent_child'] == 'child' and goods_upload_variation_obj['size_name']:
                    RingSize_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                    RingSize.appendChild(RingSize_text)
                    VariationData.appendChild(RingSize)
                if params['parent_child'] == 'child' and goods_upload_variation_obj['MetalType']:
                    MetalType_text = doc.createTextNode(goods_upload_variation_obj['MetalType'])
                    MetalType.appendChild(MetalType_text)
                    VariationData.appendChild(MetalType)
                elif params['parent_child'] == 'child' and goods_upload_obj['metal_type']:
                    MetalType_text = doc.createTextNode(goods_upload_obj['metal_type'])
                    MetalType.appendChild(MetalType_text)
                    VariationData.appendChild(MetalType)
                ProductType_child.appendChild(VariationData)
        else:
            if goods_upload_obj['metal_type']:
                Parentage_text = doc.createTextNode('child')
                Parentage.appendChild(Parentage_text)
                VariationData.appendChild(Parentage)
                VariationTheme_text = doc.createTextNode('MetalType')
                VariationTheme.appendChild(VariationTheme_text)
                VariationData.appendChild(VariationTheme)
                MetalType_text = doc.createTextNode(goods_upload_obj['metal_type'])
                MetalType.appendChild(MetalType_text)
                VariationData.appendChild(MetalType)
            ProductType_child.appendChild(VariationData)
        if goods_upload_obj['material_type']:
            Material_text = doc.createTextNode(goods_upload_obj['material_type'])
            Material.appendChild(Material_text)
            if goods_upload_obj['feed_product_type'] != 'Watch':
                ProductType_child.appendChild(Material)
        GemType_text = doc.createTextNode('NA')
        GemType.appendChild(GemType_text)
        Stone.appendChild(GemType)
        if goods_upload_obj['feed_product_type'] != 'Watch':
            ProductType_child.appendChild(Stone)
        SellerWarrantyDescription_text = doc.createTextNode('be careful')
        SellerWarrantyDescription.appendChild(SellerWarrantyDescription_text)
        ProductType_child.appendChild(SellerWarrantyDescription)

        if goods_upload_obj['feed_product_type'] != 'Watch':
            if goods_upload_obj['jewerly_color']:
                ColorMap_text = doc.createTextNode(goods_upload_obj['jewerly_color'])
                ColorMap.appendChild(ColorMap_text)
                Color_text = doc.createTextNode(goods_upload_obj['jewerly_color'])
                Color.appendChild(Color_text)
            if params['parent_child'] == 'child' and goods_upload_variation_obj['color_map']:
                ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                ColorMap.appendChild(ColorMap_text)
                Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                Color.appendChild(Color_text)
        else:
            if goods_upload_obj['jewerly_color']:
                Color_text = doc.createTextNode(goods_upload_obj['jewerly_color'])
                Color.appendChild(Color_text)
            if params['parent_child'] == 'child' and goods_upload_variation_obj['color_map']:
                Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                Color.appendChild(Color_text)
        DepartmentName_text = doc.createTextNode(goods_upload_obj['department_name1'])
        DepartmentName.appendChild(DepartmentName_text)
        if goods_upload_obj['feed_product_type'] != 'Watch':
            if params['parent_child'] == 'child' and goods_upload_variation_obj['color_name']:
                ProductType_child.appendChild(ColorMap)
            else:
                if goods_upload_obj['jewerly_color']:
                    ProductType_child.appendChild(ColorMap)
        ProductType_child.appendChild(DepartmentName)
        if goods_upload_obj['feed_product_type'] in item_shape_need_list:
            if goods_upload_obj['item_shape']:
                ItemShape_text = doc.createTextNode(goods_upload_obj['item_shape'])
                ItemShape.appendChild(ItemShape_text)
                ProductType_child.appendChild(ItemShape)
        ProductType.appendChild(ProductType_child)
        Jewelry.appendChild(ProductType)
        if params['parent_child'] == 'child' and goods_upload_variation_obj['color_name']:
            Jewelry.appendChild(Color)
        else:
            if goods_upload_obj['jewerly_color']:
                Jewelry.appendChild(Color)
        if params['parent_child'] == 'child' and goods_upload_variation_obj['size_name']:
            Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
            SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])
            Size.appendChild(Size_text)
            SizeMap.appendChild(SizeMap_text)
            Jewelry.appendChild(Size)
            Jewelry.appendChild(SizeMap)
        return Jewelry

    def is_ProductClothing(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        ProductClothing = doc.createElement('Clothing')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        Size = doc.createElement('Size')
        Color = doc.createElement('Color')
        VariationTheme = doc.createElement('VariationTheme')
        ClassificationData = doc.createElement('ClassificationData')
        Theme = doc.createElement('Theme')
        ClothingType = doc.createElement('ClothingType')
        DepartmentName = doc.createElement('Department')
        ColorMap = doc.createElement('ColorMap')
        SizeMap = doc.createElement('SizeMap')
        MaterialComposition = doc.createElement('MaterialComposition')
        Season = doc.createElement('Season')
        FitType = doc.createElement('FitType')
        MaterialType = doc.createElement('MaterialType')
        SleeveType = doc.createElement('SleeveType')

        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if variation_theme == 'Size-Color':
                variation_theme = 'SizeColor'
            VariationTheme_text = doc.createTextNode(variation_theme)
        if params['parent_child'] == 'child':
            color_name = goods_upload_variation_obj['color_name']
            size_name = goods_upload_variation_obj['size_name']
            if color_name == '':
                color_name = '*'
            if size_name == '':
                size_name = '*'
            Color_text = doc.createTextNode(color_name)
            Size_text = doc.createTextNode(size_name)
            SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])
            ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])

            # FitType_text = doc.createTextNode(goods_upload_variation_obj['fit_type'])
            # MaterialType_text = doc.createTextNode(goods_upload_variation_obj['MetalType'])
            # SleeveType_text = doc.createTextNode(goods_upload_variation_obj['sleeve_type'])
            if goods_upload_obj['fit_type']:
                FitType_text = doc.createTextNode(goods_upload_obj['fit_type'])
                FitType.appendChild(FitType_text)
            if goods_upload_obj['material_type']:
                MaterialType_text = doc.createTextNode(goods_upload_obj['material_type'])
                MaterialType.appendChild(MaterialType_text)
            if goods_upload_obj['sleeve_type']:
                SleeveType_text = doc.createTextNode(goods_upload_obj['sleeve_type'])
                SleeveType.appendChild(SleeveType_text)
            if goods_upload_obj['material_composition']:
                MaterialComposition_text = doc.createTextNode(goods_upload_obj['material_composition'])
                MaterialComposition.appendChild(MaterialComposition_text)
            if goods_upload_obj['season']:
                Season_text = doc.createTextNode(goods_upload_obj['season'])
                Season.appendChild(Season_text)
            ColorMap.appendChild(ColorMap_text)
            Color.appendChild(Color_text)
            Size.appendChild(Size_text)
            SizeMap.appendChild(SizeMap_text)

        if params['variation'] == 1:
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            if params['parent_child'] == 'child':
                VariationData.appendChild(Size)
                VariationData.appendChild(Color)
            VariationData.appendChild(VariationTheme)
            ProductClothing.appendChild(VariationData)
        else:
            clothing_color_text = doc.createTextNode(goods_upload_obj['clothing_color'])
            clothing_size_text = doc.createTextNode(goods_upload_obj['clothing_size'])
            clothing_colorMap_text = doc.createTextNode(goods_upload_obj['clothing_color'])
            clothing_sizeMap_text = doc.createTextNode(goods_upload_obj['clothing_size'])

            if goods_upload_obj['fit_type']:
                clothing_fit_type_text = doc.createTextNode(goods_upload_obj['fit_type'])
                FitType.appendChild(clothing_fit_type_text)
            if goods_upload_obj['material_type']:
                clothing_material_type_text = doc.createTextNode(goods_upload_obj['material_type'])
                MaterialType.appendChild(clothing_material_type_text)
            if goods_upload_obj['sleeve_type']:
                clothing_sleeve_type_text = doc.createTextNode(goods_upload_obj['sleeve_type'])
                SleeveType.appendChild(clothing_sleeve_type_text)
            if goods_upload_obj['material_composition']:
                MaterialComposition_text = doc.createTextNode(goods_upload_obj['material_composition'])
                MaterialComposition.appendChild(MaterialComposition_text)
            if goods_upload_obj['season']:
                Season_text = doc.createTextNode(goods_upload_obj['season'])
                Season.appendChild(Season_text)
            ColorMap.appendChild(clothing_colorMap_text)
            Color.appendChild(clothing_color_text)
            Size.appendChild(clothing_size_text)
            SizeMap.appendChild(clothing_sizeMap_text)
            VariationData.appendChild(Size)
            VariationData.appendChild(Color)
            ProductClothing.appendChild(VariationData)

        ClothingType_text = doc.createTextNode(goods_upload_obj['product_subtype'])
        ClothingType.appendChild(ClothingType_text)
        ClassificationData.appendChild(ClothingType)
        DepartmentName_text = doc.createTextNode(goods_upload_obj['department_name1'])
        DepartmentName.appendChild(DepartmentName_text)
        ClassificationData.appendChild(DepartmentName)
        if params['variation'] == 1:
            if params['parent_child'] == 'child':
                if goods_upload_variation_obj['color_name']:
                    ClassificationData.appendChild(ColorMap)
                if goods_upload_obj['material_composition']:
                    ClassificationData.appendChild(MaterialComposition)
                if goods_upload_obj['season']:
                    ClassificationData.appendChild(Season)
                if goods_upload_obj['sleeve_type']:
                    ClassificationData.appendChild(SleeveType)
                if goods_upload_variation_obj['size_name']:
                    ClassificationData.appendChild(SizeMap)
                if goods_upload_obj['fit_type']:
                    ClassificationData.appendChild(FitType)
                if goods_upload_obj['material_type']:
                    ClassificationData.appendChild(MaterialType)
        else:
            if goods_upload_obj['clothing_color']:
                ClassificationData.appendChild(ColorMap)
            if goods_upload_obj['material_composition']:
                ClassificationData.appendChild(MaterialComposition)
            if goods_upload_obj['season']:
                ClassificationData.appendChild(Season)
            if goods_upload_obj['sleeve_type']:
                ClassificationData.appendChild(SleeveType)
            if goods_upload_obj['clothing_size']:
                ClassificationData.appendChild(SizeMap)
            if goods_upload_obj['fit_type']:
                ClassificationData.appendChild(FitType)
            if goods_upload_obj['material_type']:
                ClassificationData.appendChild(MaterialType)
        Theme_text = doc.createTextNode('well done')
        Theme.appendChild(Theme_text)
        ClassificationData.appendChild(Theme)
        ProductClothing.appendChild(ClassificationData)
        return ProductClothing

    def is_Beauty(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        Beauty = doc.createElement('Beauty')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        SellerWarrantyDescription = doc.createElement('SellerWarrantyDescription')
        Color = doc.createElement('Color')
        Size = doc.createElement('Size')
        SizeMap = doc.createElement('SizeMap')
        ColorMap = doc.createElement('ColorMap')
        UnitCount = doc.createElement('UnitCount')
        UnitCount.setAttribute('unitOfMeasure',str(goods_upload_obj['unit_count_type']))
        ProductType_child = doc.createElement(goods_upload_obj['feed_product_type'])
        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            VariationTheme_text = doc.createTextNode(goods_upload_variation_obj['variation_theme'])
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            VariationData.appendChild(VariationTheme)
            if params['parent_child'] == 'child':
                Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                ColorMap.appendChild(ColorMap_text)
                Color.appendChild(Color_text)
                Size.appendChild(Size_text)
                if goods_upload_variation_obj['size_name']:
                    VariationData.appendChild(Size)
                if goods_upload_variation_obj['color_name']:
                    VariationData.appendChild(Color)
                    VariationData.appendChild(ColorMap)
            ProductType_child.appendChild(VariationData)
        UnitCount_text = doc.createTextNode(goods_upload_obj['unit_count'])
        UnitCount.appendChild(UnitCount_text)
        SellerWarrantyDescription_text = doc.createTextNode('be careful')
        SellerWarrantyDescription.appendChild(SellerWarrantyDescription_text)
        ProductType_child.appendChild(UnitCount)
        ProductType_child.appendChild(SellerWarrantyDescription)
        if params['variation'] == 1:
            if params['parent_child'] == 'child':
                if goods_upload_variation_obj['size_name']:
                    SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                    SizeMap.appendChild(SizeMap_text)
                    ProductType_child.appendChild(SizeMap)
        ProductType.appendChild(ProductType_child)
        Beauty.appendChild(ProductType)
        return Beauty

    def is_PetSupplies(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        PetSupplies = doc.createElement('PetSupplies')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        ColorSpecification = doc.createElement('ColorSpecification')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        SellerWarrantyDescription = doc.createElement('SellerWarrantyDescription')
        Size = doc.createElement('Size')
        SizeMap = doc.createElement('SizeMap')
        ProductType_child = doc.createElement(goods_upload_obj['feed_product_type'])
        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if variation_theme == 'Size-Color':
                variation_theme = 'SizeColor'
            VariationTheme_text = doc.createTextNode(variation_theme)
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            VariationData.appendChild(VariationTheme)
            ProductType_child.appendChild(VariationData)
            if params['parent_child'] == 'child':
                Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])
                ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                SizeMap.appendChild(SizeMap_text)
                ColorMap.appendChild(ColorMap_text)
                Color.appendChild(Color_text)
                Size.appendChild(Size_text)
                if goods_upload_variation_obj['color_name']:
                    ColorSpecification.appendChild(Color)
                    ColorSpecification.appendChild(ColorMap)
                    ProductType_child.appendChild(ColorSpecification)
        SellerWarrantyDescription_text = doc.createTextNode('so wondful')
        SellerWarrantyDescription.appendChild(SellerWarrantyDescription_text)
        ProductType_child.appendChild(SellerWarrantyDescription)
        if params['variation'] == 1:
            if params['parent_child'] == 'child':
                if goods_upload_variation_obj['size_name']:
                    ProductType_child.appendChild(Size)
                    ProductType_child.appendChild(SizeMap)
        ProductType.appendChild(ProductType_child)
        PetSupplies.appendChild(ProductType)
        return PetSupplies

    def is_Health(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        Health = doc.createElement('Health')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        Size = doc.createElement('Size')
        SizeMap = doc.createElement('SizeMap')
        UnitCount = doc.createElement('UnitCount')
        UnitCount.setAttribute('unitOfMeasure',str(goods_upload_obj['unit_count_type']))
        PrimaryIngredientCountryOfOrigin = doc.createElement('PrimaryIngredientCountryOfOrigin')
        ProductType_child = doc.createElement(goods_upload_obj['feed_product_type'])
        if goods_upload_obj['feed_product_type'] != 'PrescriptionDrug':
            if params['variation'] == 1:
                if params['parent_child'] == 'parent':
                    Parentage_text = doc.createTextNode('parent')
                else:
                    Parentage_text = doc.createTextNode('child')
                VariationTheme_text = doc.createTextNode(goods_upload_variation_obj['variation_theme'])
                VariationTheme.appendChild(VariationTheme_text)
                Parentage.appendChild(Parentage_text)
                VariationData.appendChild(Parentage)
                VariationData.appendChild(VariationTheme)
                if params['parent_child'] == 'child':
                    Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                    Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                    ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                    SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])
                    ColorMap.appendChild(ColorMap_text)
                    Color.appendChild(Color_text)
                    Size.appendChild(Size_text)
                    SizeMap.appendChild(SizeMap_text)
                    if goods_upload_variation_obj['size_name']:
                        VariationData.appendChild(Size)
                        VariationData.appendChild(SizeMap)
                    if goods_upload_variation_obj['color_name']:
                        VariationData.appendChild(Color)
                        VariationData.appendChild(ColorMap)
                ProductType_child.appendChild(VariationData)
            UnitCount_text = doc.createTextNode(goods_upload_obj['unit_count'])
            UnitCount.appendChild(UnitCount_text)
            ProductType_child.appendChild(UnitCount)
            PrimaryIngredientCountryOfOrigin_text = doc.createTextNode('US')
            PrimaryIngredientCountryOfOrigin.appendChild(PrimaryIngredientCountryOfOrigin_text)
            ProductType_child.appendChild(PrimaryIngredientCountryOfOrigin)
        ProductType.appendChild(ProductType_child)
        Health.appendChild(ProductType)
        return Health

    def is_Lighting(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        Lighting = doc.createElement('Lighting')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        CountryOfOrigin = doc.createElement('CountryOfOrigin')
        ProductType_child = doc.createElement(goods_upload_obj['feed_product_type'])
        if goods_upload_obj['feed_product_type'] == 'LightsAndFixtures':
            if params['variation'] == 1:
                if params['parent_child'] == 'parent':
                    Parentage_text = doc.createTextNode('parent')
                else:
                    Parentage_text = doc.createTextNode('child')
                VariationTheme_text = doc.createTextNode(goods_upload_variation_obj['variation_theme'])
                VariationTheme.appendChild(VariationTheme_text)
                Parentage.appendChild(Parentage_text)
                VariationData.appendChild(Parentage)
                VariationData.appendChild(VariationTheme)
                ProductType_child.appendChild(VariationData)
                if params['variation'] == 1:
                    if params['parent_child'] == 'child':
                        Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                        ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                        ColorMap.appendChild(ColorMap_text)
                        Color.appendChild(Color_text)
                        if goods_upload_variation_obj['color_name']:
                            ProductType_child.appendChild(Color)
                            ProductType_child.appendChild(ColorMap)
        elif goods_upload_obj['feed_product_type'] == 'LightingAccessories':
            Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
            ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
            ColorMap.appendChild(ColorMap_text)
            Color.appendChild(Color_text)
            if goods_upload_variation_obj['color_name']:
                ProductType_child.appendChild(Color)
                ProductType_child.appendChild(ColorMap)

        CountryOfOrigin_text = doc.createTextNode('US')
        CountryOfOrigin.appendChild(CountryOfOrigin_text)
        ProductType_child.appendChild(CountryOfOrigin)
        ProductType.appendChild(ProductType_child)
        Lighting.appendChild(ProductType)
        return Lighting

    def is_ThreeDPrinting(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        ThreeDPrinting = doc.createElement('ThreeDPrinting')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        Color = doc.createElement('ColorName')
        ColorMap = doc.createElement('ColorMap')
        Size = doc.createElement('SizeName')
        ItemFirmnessDescription = doc.createElement('ItemFirmnessDescription')
        ItemFirmnessDescription_text = doc.createTextNode('Pretty strong')
        ItemFirmnessDescription.appendChild(ItemFirmnessDescription_text)
        ProductType_text = doc.createTextNode(goods_upload_obj['feed_product_type'])
        ProductType.appendChild(ProductType_text)
        ThreeDPrinting.appendChild(ProductType)
        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if 'Color' in goods_upload_variation_obj['variation_theme']:
                variation_theme = variation_theme.replace('Color', 'ColorName')
            if 'Size' in goods_upload_variation_obj['variation_theme']:
                variation_theme = variation_theme.replace('Size', 'SizeName')
            VariationTheme_text = doc.createTextNode(variation_theme)
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            VariationData.appendChild(VariationTheme)
            ThreeDPrinting.appendChild(VariationData)
            if params['parent_child'] == 'child':
                Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                ColorMap.appendChild(ColorMap_text)
                Color.appendChild(Color_text)
                Size.appendChild(Size_text)
                if goods_upload_variation_obj['color_name']:
                    ThreeDPrinting.appendChild(Color)
                    ThreeDPrinting.appendChild(ColorMap)
                if goods_upload_variation_obj['size_name']:
                    ThreeDPrinting.appendChild(Size)
        ThreeDPrinting.appendChild(ItemFirmnessDescription)
        return ThreeDPrinting

    def is_ToysBaby(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        ToysBaby = doc.createElement('ToysBaby')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        Size = doc.createElement('Size')
        SizeMap = doc.createElement('SizeMap')
        AgeRecommendation = doc.createElement('AgeRecommendation')
        MinimumManufacturerAgeRecommended = doc.createElement('MinimumManufacturerAgeRecommended')
        MinimumManufacturerAgeRecommended.setAttribute('unitOfMeasure', str(goods_upload_obj['mfg_minimum_unit_of_measure']))
        ProductType_child_text = doc.createTextNode(goods_upload_obj['feed_product_type'])

        MinimumManufacturerAgeRecommended_text = doc.createTextNode(goods_upload_obj['mfg_minimum'])
        MinimumManufacturerAgeRecommended.appendChild(MinimumManufacturerAgeRecommended_text)
        AgeRecommendation.appendChild(MinimumManufacturerAgeRecommended)
        ProductType.appendChild(ProductType_child_text)
        ToysBaby.appendChild(ProductType)
        ToysBaby.appendChild(AgeRecommendation)

        if goods_upload_obj['item_type'] and 'puzzle' in goods_upload_obj['item_type'].lower():
            pieces_node = doc.createElement('NumberOfPieces')
            pieces_node_text = doc.createTextNode(str(goods_upload_obj['number_of_pieces']))
            pieces_node.appendChild(pieces_node_text)
            ToysBaby.appendChild(pieces_node)

        if goods_upload_obj['feed_product_type'] == 'BabyProducts':
            if params['variation'] == 1:
                if params['parent_child'] == 'parent':
                    Parentage_text = doc.createTextNode('parent')
                else:
                    Parentage_text = doc.createTextNode('child')
                variation_theme = goods_upload_variation_obj['variation_theme']
                if variation_theme == 'SizeColor':
                    variation_theme = 'Size-Color'
                VariationTheme_text = doc.createTextNode(variation_theme)
                VariationTheme.appendChild(VariationTheme_text)
                Parentage.appendChild(Parentage_text)
                VariationData.appendChild(Parentage)
                VariationData.appendChild(VariationTheme)
                ToysBaby.appendChild(VariationData)
                if params['parent_child'] == 'child':
                    Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                    Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                    ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                    SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])
                    ColorMap.appendChild(ColorMap_text)
                    Color.appendChild(Color_text)
                    Size.appendChild(Size_text)
                    SizeMap.appendChild(SizeMap_text)
                    if goods_upload_variation_obj['size_name']:
                        ToysBaby.appendChild(Size)
                        ToysBaby.appendChild(SizeMap)
                    if goods_upload_variation_obj['color_name']:
                        ToysBaby.appendChild(Color)
                        ToysBaby.appendChild(ColorMap)
            else:
                Color_text = doc.createTextNode('1')
                ColorMap_text = doc.createTextNode('1')
                ColorMap.appendChild(ColorMap_text)
                Color.appendChild(Color_text)
                ToysBaby.appendChild(Color)
                ToysBaby.appendChild(ColorMap)
        return ToysBaby

    def is_Office(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        ProductType_child_list = ['BarCode', 'Calculator', 'InkToner', 'MultifunctionDevice', 'OfficeElectronics', 'OfficePhone',
                                  'OfficePrinter', 'OfficeScanner', 'VoiceRecorder']
        Office = doc.createElement('Office')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        ColorSpecification = doc.createElement('ColorSpecification')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        MfrWarrantyDescriptionLabor = doc.createElement('MfrWarrantyDescriptionLabor')
        Size = doc.createElement('Size')
        SizeMap = doc.createElement('SizeMap')
        ProductType_child = doc.createElement(goods_upload_obj['feed_product_type'])
        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if variation_theme == 'Size-Color':
                variation_theme = 'SizeColor'
            VariationTheme_text = doc.createTextNode(variation_theme)
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            VariationData.appendChild(VariationTheme)
            ProductType_child.appendChild(VariationData)
            if params['parent_child'] == 'child':
                ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                ColorMap.appendChild(ColorMap_text)
                Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                Color.appendChild(Color_text)
                if goods_upload_variation_obj['color_name']:
                    if goods_upload_obj['feed_product_type'] not in ProductType_child_list:
                        ColorSpecification.appendChild(Color)
                        ColorSpecification.appendChild(ColorMap)
                        ProductType_child.appendChild(ColorSpecification)
                    else:
                        ProductType_child.appendChild(Color)
        else:
            Color_text = doc.createTextNode('1')
            ColorMap_text = doc.createTextNode('1')
            ColorMap.appendChild(ColorMap_text)
            Color.appendChild(Color_text)
            if goods_upload_obj['feed_product_type'] not in ProductType_child_list:
                ColorSpecification.appendChild(Color)
                ColorSpecification.appendChild(ColorMap)
                ProductType_child.appendChild(ColorSpecification)
            else:
                ProductType_child.appendChild(Color)
        if goods_upload_obj['item_type_name']:
            ItemTypeName = doc.createElement('ItemTypeName')
            ItemTypeName_text = doc.createTextNode(goods_upload_obj['item_type_name'])
            ItemTypeName.appendChild(ItemTypeName_text)
            ProductType_child.appendChild(ItemTypeName)
        ProductType.appendChild(ProductType_child)
        Office.appendChild(ProductType)
        if goods_upload_obj['warranty_description']:
            MfrWarrantyDescriptionLabor_text = doc.createTextNode(goods_upload_obj['warranty_description'])
            MfrWarrantyDescriptionLabor.appendChild(MfrWarrantyDescriptionLabor_text)
            Office.appendChild(MfrWarrantyDescriptionLabor)
        if params['variation'] == 1:
            if params['parent_child'] == 'child':
                Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])
                Size.appendChild(Size_text)
                SizeMap.appendChild(SizeMap_text)
                if goods_upload_variation_obj['size_name']:
                    Office.appendChild(Size)
                    Office.appendChild(SizeMap)
        return Office

    def is_Sports(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        Sports = doc.createElement('Sports')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        ItemTypeName = doc.createElement('ItemTypeName')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        Size = doc.createElement('Size')
        SizeMap = doc.createElement('SizeMap')
        SellerWarrantyDescription = doc.createElement('SellerWarrantyDescription')
        ProductType_text = doc.createTextNode(goods_upload_obj['feed_product_type'])
        ProductType.appendChild(ProductType_text)
        Sports.appendChild(ProductType)
        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if variation_theme == 'Size-Color':
                variation_theme = 'ColorSize'
            VariationTheme_text = doc.createTextNode(variation_theme)
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            VariationData.appendChild(VariationTheme)
            if params['parent_child'] == 'child':
                Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                Color.appendChild(Color_text)
                Size.appendChild(Size_text)
                if goods_upload_variation_obj['color_name']:
                    VariationData.appendChild(Color)
                if goods_upload_variation_obj['size_name']:
                    VariationData.appendChild(Size)
            Sports.appendChild(VariationData)
            ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
            SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])
            ColorMap.appendChild(ColorMap_text)
            SizeMap.appendChild(SizeMap_text)
            if goods_upload_variation_obj['color_name']:
                Sports.appendChild(ColorMap)
        if goods_upload_obj['item_type_name']:
            ItemTypeName_text = doc.createTextNode(goods_upload_obj['item_type_name'])
            ItemTypeName.appendChild(ItemTypeName_text)
            Sports.appendChild(ItemTypeName)
        SellerWarrantyDescription_text = doc.createTextNode('Please keep it properly')
        SellerWarrantyDescription.appendChild(SellerWarrantyDescription_text)
        Sports.appendChild(SellerWarrantyDescription)
        if params['variation'] == 1 and goods_upload_variation_obj['size_name']:
            Sports.appendChild(SizeMap)
        return Sports

    def is_LuxuryBeauty(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        LuxuryBeauty = doc.createElement('LuxuryBeauty')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        UnitCount = doc.createElement('UnitCount')
        UnitCount.setAttribute('unitOfMeasure',str(goods_upload_obj['unit_count_type']))
        ColorSpecification = doc.createElement('ColorSpecification')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        Size = doc.createElement('Size')
        EachUnitCount = doc.createElement('EachUnitCount')
        ProductType_text = doc.createTextNode(goods_upload_obj['feed_product_type'])
        ProductType.appendChild(ProductType_text)
        LuxuryBeauty.appendChild(ProductType)
        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if 'Color' in goods_upload_variation_obj['variation_theme']:
                variation_theme = variation_theme.replace('Color', 'ColorName')
            if 'Size' in goods_upload_variation_obj['variation_theme']:
                variation_theme = variation_theme.replace('Size', 'SizeName')
            VariationTheme_text = doc.createTextNode(variation_theme)
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            UnitCount_text = doc.createTextNode(goods_upload_obj['unit_count'])
            UnitCount.appendChild(UnitCount_text)
            VariationData.appendChild(VariationTheme)
            LuxuryBeauty.appendChild(VariationData)
            LuxuryBeauty.appendChild(UnitCount)
            if params['parent_child'] == 'child':
                Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                ColorMap.appendChild(ColorMap_text)
                Color.appendChild(Color_text)
                Size.appendChild(Size_text)
                if goods_upload_variation_obj['color_name']:
                    ColorSpecification.appendChild(Color)
                    ColorSpecification.appendChild(ColorMap)
                    LuxuryBeauty.appendChild(ColorSpecification)
                if goods_upload_variation_obj['size_name']:
                    LuxuryBeauty.appendChild(Size)
        EachUnitCount_text = doc.createTextNode('1')
        EachUnitCount.appendChild(EachUnitCount_text)
        LuxuryBeauty.appendChild(EachUnitCount)
        return LuxuryBeauty

    def is_Furniture(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        Furniture = doc.createElement('Furniture')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        SpecialFeatures = doc.createElement('SpecialFeatures')
        Style = doc.createElement('Style')
        FrameColor = doc.createElement('FrameColor')
        ProductType_text = doc.createTextNode(goods_upload_obj['feed_product_type'])
        ProductType.appendChild(ProductType_text)
        Furniture.appendChild(ProductType)
        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if 'Color' in goods_upload_variation_obj['variation_theme']:
                variation_theme = variation_theme.replace('Color', 'ColorName')
            if 'Size' in goods_upload_variation_obj['variation_theme']:
                variation_theme = variation_theme.replace('Size', 'SizeName')
            VariationTheme_text = doc.createTextNode(variation_theme)
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            VariationData.appendChild(VariationTheme)
            Furniture.appendChild(VariationData)

        SpecialFeatures_text = doc.createTextNode('maybe you can Divergent thinking')
        SpecialFeatures.appendChild(SpecialFeatures_text)
        Furniture.appendChild(SpecialFeatures)
        if params['variation'] == 1:
            if params['parent_child'] == 'child':
                Style_name = goods_upload_variation_obj['color_name']
                FrameColor_name = goods_upload_variation_obj['color_name']
                if goods_upload_variation_obj['size_name']:
                    FrameColor_name = ''
                    Style_name = goods_upload_variation_obj['size_name']
                Style_text = doc.createTextNode(Style_name)
                Style.appendChild(Style_text)
                FrameColor_text = doc.createTextNode(FrameColor_name)
                FrameColor.appendChild(FrameColor_text)
                if Style_name:
                    Furniture.appendChild(Style)
                if FrameColor_name:
                    Furniture.appendChild(FrameColor)
        return Furniture

    def is_AutoAccessory(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        AutoAccessory = doc.createElement('AutoAccessory')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        ColorSpecification = doc.createElement('ColorSpecification')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        Size = doc.createElement('Size')
        SizeMap = doc.createElement('SizeMap')
        WarrantyDescription = doc.createElement('WarrantyDescription')
        ProductType_child = doc.createElement(goods_upload_obj['feed_product_type'])
        if goods_upload_obj['feed_product_type'] == 'Autochemical':
            WarrantyDescription_text = doc.createTextNode('Save it properly')
            WarrantyDescription.appendChild(WarrantyDescription_text)
            ProductType_child.appendChild(WarrantyDescription)
        else:
            if params['variation'] == 1:
                if params['parent_child'] == 'parent':
                    Parentage_text = doc.createTextNode('parent')
                else:
                    Parentage_text = doc.createTextNode('child')
                variation_theme = goods_upload_variation_obj['variation_theme']
                if variation_theme == 'SizeColor':
                    variation_theme = 'Size-Color'
                VariationTheme_text = doc.createTextNode(variation_theme)
                VariationTheme.appendChild(VariationTheme_text)
                Parentage.appendChild(Parentage_text)
                VariationData.appendChild(Parentage)
                VariationData.appendChild(VariationTheme)
                ProductType_child.appendChild(VariationData)
                if params['parent_child'] == 'child':
                    Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                    Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                    ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                    SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])
                    ColorMap.appendChild(ColorMap_text)
                    Color.appendChild(Color_text)
                    Size.appendChild(Size_text)
                    SizeMap.appendChild(SizeMap_text)
                    if goods_upload_variation_obj['color_name']:
                        ColorSpecification.appendChild(Color)
                        ColorSpecification.appendChild(ColorMap)
                        ProductType_child.appendChild(ColorSpecification)
                    if goods_upload_variation_obj['size_name']:
                        ProductType_child.appendChild(Size)
                        ProductType_child.appendChild(SizeMap)
            else:
                Color_text = doc.createTextNode('1')
                ColorMap_text = doc.createTextNode('1')
                ColorMap.appendChild(ColorMap_text)
                Color.appendChild(Color_text)
                ColorSpecification.appendChild(Color)
                ColorSpecification.appendChild(ColorMap)
                ProductType_child.appendChild(ColorSpecification)
        ProductType.appendChild(ProductType_child)
        AutoAccessory.appendChild(ProductType)
        return AutoAccessory

    def is_Wireless(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        Wireless = doc.createElement('Wireless')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        Keywords = doc.createElement('Keywords')
        ProductType_child = doc.createElement(goods_upload_obj['feed_product_type'])
        if goods_upload_obj['feed_product_type'] == 'WirelessAccessories':
            if params['variation'] == 1:
                if params['parent_child'] == 'parent':
                    Parentage_text = doc.createTextNode('parent')
                else:
                    Parentage_text = doc.createTextNode('child')
                variation_theme = goods_upload_variation_obj['variation_theme']
                VariationTheme_text = doc.createTextNode(variation_theme)
                VariationTheme.appendChild(VariationTheme_text)
                Parentage.appendChild(Parentage_text)
                VariationData.appendChild(Parentage)
                VariationData.appendChild(VariationTheme)
                ProductType_child.appendChild(VariationData)
                if params['parent_child'] == 'child':
                    Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                    ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                    ColorMap.appendChild(ColorMap_text)
                    Color.appendChild(Color_text)
                    if goods_upload_variation_obj['color_name']:
                        ProductType_child.appendChild(Color)
                        ProductType_child.appendChild(ColorMap)
        Keywords_text = doc.createTextNode('Wireless')
        Keywords.appendChild(Keywords_text)
        ProductType_child.appendChild(Keywords)
        ProductType.appendChild(ProductType_child)
        Wireless.appendChild(ProductType)
        return Wireless

    def is_MusicalInstruments(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        MusicalInstruments = doc.createElement('MusicalInstruments')
        ProductType = doc.createElement('ProductType')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        ColorSpecification = doc.createElement('ColorSpecification')
        Color = doc.createElement('Color')
        ColorMap = doc.createElement('ColorMap')
        Size = doc.createElement('Size')
        SizeMap = doc.createElement('SizeMap')
        SellerWarrantyDescription = doc.createElement('SellerWarrantyDescription')
        ProductType_child = doc.createElement(goods_upload_obj['feed_product_type'])
        if params['variation'] == 1:
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if variation_theme == 'Size-Color':
                variation_theme = 'SizeColor'
            VariationTheme_text = doc.createTextNode(variation_theme)
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            VariationData.appendChild(VariationTheme)
            ProductType_child.appendChild(VariationData)
            if params['parent_child'] == 'child':
                Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                SizeMap.appendChild(SizeMap_text)
                ColorMap.appendChild(ColorMap_text)
                Color.appendChild(Color_text)
                Size.appendChild(Size_text)
                if goods_upload_variation_obj['color_name']:
                    ColorSpecification.appendChild(Color)
                    ColorSpecification.appendChild(ColorMap)
                    ProductType_child.appendChild(ColorSpecification)
                if goods_upload_variation_obj['size_name']:
                    ProductType_child.appendChild(Size)
                    ProductType_child.appendChild(SizeMap)
        SellerWarrantyDescription_text = doc.createTextNode('be careful')
        SellerWarrantyDescription.appendChild(SellerWarrantyDescription_text)
        ProductType_child.appendChild(SellerWarrantyDescription)
        ProductType.appendChild(ProductType_child)
        MusicalInstruments.appendChild(ProductType)
        return MusicalInstruments

    def is_Baby(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        # https://images-na.ssl-images-amazon.com/images/G/01/rainier/help/xsd/release_1_9/Baby.xsd
        Baby = doc.createElement('Baby')
        ProductType = doc.createElement('ProductType')
        BabyProducts = doc.createElement('BabyProducts')
        VariationData = doc.createElement('VariationData')
        Parentage = doc.createElement('Parentage')
        VariationTheme = doc.createElement('VariationTheme')
        Color = doc.createElement('ColorMap')
        ColorMap = doc.createElement('ColorName')
        Size = doc.createElement('SizeMap')
        SizeMap = doc.createElement('SizeName')

        MinimumManufacturerAgeRecommended = doc.createElement('MinimumManufacturerAgeRecommended')
        MinimumManufacturerAgeRecommended.setAttribute('unitOfMeasure', str(goods_upload_obj['mfg_minimum_unit_of_measure']))
        MinimumManufacturerAgeRecommended_text = doc.createTextNode(goods_upload_obj['mfg_minimum'])
        MinimumManufacturerAgeRecommended.appendChild(MinimumManufacturerAgeRecommended_text)

        UnitCount = doc.createElement('UnitCount')
        UnitCount.setAttribute('unitOfMeasure', str(goods_upload_obj['unit_count_type']))
        UnitCount_text = doc.createTextNode(goods_upload_obj['unit_count'])
        UnitCount.appendChild(UnitCount_text)

        ProductType.appendChild(BabyProducts)
        Baby.appendChild(ProductType)

        if goods_upload_obj['feed_product_type'] == 'BabyProducts':
            if params['variation'] == 1: #多体
                # 变体信息：<VariationData><Parentage>？</Parentage><VariationTheme>？</VariationTheme></VariationData>
                if params['parent_child'] == 'parent':
                    Parentage_text = doc.createTextNode('parent')
                else:
                    Parentage_text = doc.createTextNode('child')
                variation_theme = goods_upload_variation_obj['variation_theme']
                if variation_theme == 'Size-Color':
                    variation_theme = 'SizeColor'
                VariationTheme_text = doc.createTextNode(variation_theme)
                VariationTheme.appendChild(VariationTheme_text)
                Parentage.appendChild(Parentage_text)
                VariationData.appendChild(Parentage)
                VariationData.appendChild(VariationTheme)

                if params['parent_child'] == 'child': #变体包含区分变体信息
                    Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                    Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                    ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                    SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])
                    ColorMap.appendChild(ColorMap_text)
                    Color.appendChild(Color_text)
                    Size.appendChild(Size_text)
                    SizeMap.appendChild(SizeMap_text)
                    # 1.ColorMap,ColorName
                    if goods_upload_variation_obj['color_name']:
                        BabyProducts.appendChild(Color)
                        BabyProducts.appendChild(ColorMap)
                    # 2.MinimumManufacturerAgeRecommended
                    BabyProducts.appendChild(MinimumManufacturerAgeRecommended)
                    # 3.VariationData
                    BabyProducts.appendChild(VariationData)
                    # 4.SizeMap,SizeName
                    if goods_upload_variation_obj['size_name']:
                        BabyProducts.appendChild(Size)
                        BabyProducts.appendChild(SizeMap)
                    # 5.UnitCount
                    BabyProducts.appendChild(UnitCount)
                else: #主体
                    BabyProducts.appendChild(MinimumManufacturerAgeRecommended)
                    BabyProducts.appendChild(VariationData)
                    BabyProducts.appendChild(UnitCount)
            else: #单体
                BabyProducts.appendChild(MinimumManufacturerAgeRecommended)
                BabyProducts.appendChild(UnitCount)
        return Baby

    def is_Luggage(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        # https://images-na.ssl-images-amazon.com/images/G/01/rainier/help/xsd/release_1_9/Luggage.xsd

        # ProductType
        # VariationData
        #     Parentage
        #     VariationTheme
        # ColorMap
        # Size
        # Color
        # SizeMap

        Luggage = doc.createElement('Luggage')

        #ProductType部分
        ProductType = doc.createElement('ProductType')
        ProductType_child_text = doc.createTextNode(goods_upload_obj['feed_product_type'])
        ProductType.appendChild(ProductType_child_text)
        Luggage.appendChild(ProductType)

        if params['variation'] == 1:
            #VariationData部分
            VariationData = doc.createElement('VariationData')
            Parentage = doc.createElement('Parentage')
            VariationTheme = doc.createElement('VariationTheme')
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if variation_theme == 'Size-Color':
                variation_theme = 'ColorSize'
            VariationTheme_text = doc.createTextNode(variation_theme)
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            VariationData.appendChild(VariationTheme)
            Luggage.appendChild(VariationData)

        #区分变体信息部分
        ColorMap = doc.createElement('ColorMap')
        Size = doc.createElement('Size')
        Color = doc.createElement('Color')
        SizeMap = doc.createElement('SizeMap')
        if params['variation'] == 1: #多体
            if params['parent_child'] == 'child': #变体包含区分变体信息
                Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                SizeMap_text = doc.createTextNode(goods_upload_variation_obj['size_map'])
                ColorMap.appendChild(ColorMap_text)
                Color.appendChild(Color_text)
                Size.appendChild(Size_text)
                SizeMap.appendChild(SizeMap_text)
                # 4个信息出现的先后顺序为ColorMap、Size、Color、SizeMap
                if goods_upload_variation_obj['color_name']:
                    if goods_upload_variation_obj['size_name']:
                        Luggage.appendChild(ColorMap)
                        Luggage.appendChild(Size)
                        Luggage.appendChild(Color)
                        Luggage.appendChild(SizeMap)
                    else:
                        Luggage.appendChild(ColorMap)
                        Luggage.appendChild(Color)
                else:
                    if goods_upload_variation_obj['size_name']:
                        Luggage.appendChild(Size)
                        Luggage.appendChild(SizeMap)
                    else:
                        pass
            else: #主体
                pass
        else: #单体
            Color_text = doc.createTextNode(goods_upload_obj['color_name_public'])
            ColorMap_text = doc.createTextNode(goods_upload_obj['color_name_public'])
            ColorMap.appendChild(ColorMap_text)
            Color.appendChild(Color_text)
            Luggage.appendChild(ColorMap)
            Luggage.appendChild(Color)
        return Luggage

    def is_CE(self, params, doc, goods_upload_obj, goods_upload_variation_obj):
        # 可以创建变体的product_type
        variation_types = ['ConsumerElectronics','KindleAccessories','KindleEReaderAccessories','KindleFireAccessories']
        CE = doc.createElement('CE')

        # ProductType部分
        ProductType = doc.createElement('ProductType')
        feed_product_type = doc.createElement(goods_upload_obj['feed_product_type'])
        ProductType.appendChild(feed_product_type)
        CE.appendChild(ProductType)

        # if params['variation'] == 1 and goods_upload_obj['feed_product_type'] in variation_types:
        if params['variation'] == 1:
            # VariationData部分
            VariationData = doc.createElement('VariationData')
            Parentage = doc.createElement('Parentage')
            VariationTheme = doc.createElement('VariationTheme')
            if params['parent_child'] == 'parent':
                Parentage_text = doc.createTextNode('parent')
            else:
                Parentage_text = doc.createTextNode('child')
            variation_theme = goods_upload_variation_obj['variation_theme']
            if variation_theme == 'SizeColor':
                variation_theme = 'Size-Color'
            VariationTheme_text = doc.createTextNode(variation_theme)
            VariationTheme.appendChild(VariationTheme_text)
            Parentage.appendChild(Parentage_text)
            VariationData.appendChild(Parentage)
            VariationData.appendChild(VariationTheme)
            feed_product_type.appendChild(VariationData)

            Color = doc.createElement('Color')
            ColorMap = doc.createElement('ColorMap')
            Size = doc.createElement('Size')

            if params['parent_child'] == 'child':
                Color_text = doc.createTextNode(goods_upload_variation_obj['color_name'])
                ColorMap_text = doc.createTextNode(goods_upload_variation_obj['color_map'])
                Size_text = doc.createTextNode(goods_upload_variation_obj['size_name'])
                Color.appendChild(Color_text)
                ColorMap.appendChild(ColorMap_text)
                Size.appendChild(Size_text)

                if goods_upload_variation_obj['color_name']:
                    CE.appendChild(Color)
                    CE.appendChild(ColorMap)
                if goods_upload_variation_obj['size_name']:
                    CE.appendChild(Size)
            else:
                pass
        return CE

    def products_to_xml(self, params=None, upc_id=None):
        logging.debug('time-p1 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        goods_upload_obj = params['goods_upload']
        time.sleep(0.001)
        timeStamp = int(time.time() * 1000)
        logging.debug('time-timeStamp is: %s' % timeStamp)
        doc = params['doc']
        goods_upload_variation_obj = params['goods_upload_variation_obj']

        # Message
        Message = doc.createElement('Message')
        MessageID = doc.createElement('MessageID')
        MessageID_text = doc.createTextNode('%s' % timeStamp)
        MessageID.appendChild(MessageID_text)
        Message.appendChild(MessageID)

        OperationType = doc.createElement('OperationType')
        OperationType_text = doc.createTextNode('Update')
        OperationType.appendChild(OperationType_text)
        Message.appendChild(OperationType)
        # Product
        Product = doc.createElement('Product')
        SKU = doc.createElement('SKU')
        logging.debug('time-p2 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if params['parent_child'] != 'parent':
            StandardProductID = doc.createElement('StandardProductID')
            StandardProductID_Type = doc.createElement('Type')
            StandardProductID_Value = doc.createElement('Value')
        logging.debug('time-p3 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        Condition = doc.createElement('Condition')
        ConditionType = doc.createElement('ConditionType')
        ItemPackageQuantity = doc.createElement('ItemPackageQuantity')
        NumberOfItems = doc.createElement('NumberOfItems')
        DescriptionData = doc.createElement('DescriptionData')
        Title = doc.createElement('Title')
        Brand = doc.createElement('Brand')
        Description = doc.createElement('Description')
        BulletPoint1 = doc.createElement('BulletPoint')
        BulletPoint2 = doc.createElement('BulletPoint')
        BulletPoint3 = doc.createElement('BulletPoint')
        BulletPoint4 = doc.createElement('BulletPoint')
        BulletPoint5 = doc.createElement('BulletPoint')
        Manufacturer = doc.createElement('Manufacturer')
        MfrPartNumber = doc.createElement('MfrPartNumber')
        SearchTerms1 = doc.createElement('SearchTerms')
        SearchTerms2 = doc.createElement('SearchTerms')
        SearchTerms3 = doc.createElement('SearchTerms')
        SearchTerms4 = doc.createElement('SearchTerms')
        SearchTerms5 = doc.createElement('SearchTerms')
        ItemType = doc.createElement('ItemType')
        TargetAudience1 = doc.createElement('TargetAudience')
        TargetAudience2 = doc.createElement('TargetAudience')
        TargetAudience3 = doc.createElement('TargetAudience')
        RecommendedBrowseNode = doc.createElement('RecommendedBrowseNode')
        MerchantShippingGroupName = doc.createElement('MerchantShippingGroupName')
        ProductData = doc.createElement('ProductData')
        logging.debug('time-p4 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if params['parent_child'] == 'child':
            sku_text = goods_upload_variation_obj['child_sku']
            if goods_upload_variation_obj['item_quantity'] != '1':
                sku_text += '*' + str(goods_upload_variation_obj['item_quantity'])
        else:
            sku_text = goods_upload_obj['item_sku']
            if goods_upload_obj['item_package_quantity'] != '1':
                sku_text += '*' + str(goods_upload_obj['item_package_quantity'])
        logging.debug('time-p4 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        SKU_text = doc.createTextNode(sku_text)
        StandardProductID_Type_text = doc.createTextNode(goods_upload_obj['external_product_id_type'])
        if params['variation'] != 1:
            upc_id = goods_upload_obj['external_product_id']
        else:
            if params['parent_child'] == 'child':
                upc_id = goods_upload_variation_obj['external_product_id']
        if upc_id:
            StandardProductID_Value_text = doc.createTextNode(upc_id)
        logging.debug('time-p5 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ConditionType_text = doc.createTextNode(goods_upload_obj['condition_type'])
        ItemPackageQuantity_text = doc.createTextNode(goods_upload_obj['item_package_quantity'])
        numberOfItems = int(goods_upload_obj['item_package_quantity'])
        NumberOfItems_text = doc.createTextNode(str(numberOfItems))
        Title_text = doc.createTextNode(goods_upload_obj['item_name'])
        if params['parent_child'] == 'child':
            Title_text = doc.createTextNode(goods_upload_obj['item_name'] + '(' + goods_upload_variation_obj['MetalType'] + ' ' + goods_upload_variation_obj['size_name'] + ' ' + goods_upload_variation_obj['color_name'] + ')')
        Brand_text = doc.createTextNode(goods_upload_obj['brand_name'])
        Description_text = doc.createTextNode(goods_upload_obj['product_description'])
        BulletPoint1_text = doc.createTextNode(goods_upload_obj['bullet_point1'])
        BulletPoint2_text = doc.createTextNode(goods_upload_obj['bullet_point2'])
        BulletPoint3_text = doc.createTextNode(goods_upload_obj['bullet_point3'])
        BulletPoint4_text = doc.createTextNode(goods_upload_obj['bullet_point4'])
        BulletPoint5_text = doc.createTextNode(goods_upload_obj['bullet_point5'])
        SearchTerms1_text = doc.createTextNode(goods_upload_obj['generic_keywords1'])
        SearchTerms2_text = doc.createTextNode(goods_upload_obj['generic_keywords2'])
        SearchTerms3_text = doc.createTextNode(goods_upload_obj['generic_keywords3'])
        SearchTerms4_text = doc.createTextNode(goods_upload_obj['generic_keywords4'])
        SearchTerms5_text = doc.createTextNode(goods_upload_obj['generic_keywords5'])
        MerchantShippingGroupName_text = doc.createTextNode(goods_upload_obj['merchant_shipping_group_name'])
        Manufacturer_text = doc.createTextNode(goods_upload_obj['manufacturer'])
        if params['parent_child'] != 'child':
            MfrPartNumber_text = doc.createTextNode(goods_upload_obj['item_sku'])
        else:
            MfrPartNumber_text = doc.createTextNode(goods_upload_variation_obj['child_sku'])
        RecommendedBrowseNode_text = doc.createTextNode(goods_upload_obj['recommended_browse_nodes_id'])

        SKU.appendChild(SKU_text)
        logging.debug('time-p6 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if params['parent_child'] != 'parent':
            StandardProductID_Type.appendChild(StandardProductID_Type_text)
            StandardProductID_Value.appendChild(StandardProductID_Value_text)
            StandardProductID.appendChild(StandardProductID_Type)
            StandardProductID.appendChild(StandardProductID_Value)
        ConditionType.appendChild(ConditionType_text)
        Condition.appendChild(ConditionType)
        ItemPackageQuantity.appendChild(ItemPackageQuantity_text)
        NumberOfItems.appendChild(NumberOfItems_text)
        Title.appendChild(Title_text)
        Brand.appendChild(Brand_text)
        Description.appendChild(Description_text)
        BulletPoint1.appendChild(BulletPoint1_text)
        BulletPoint2.appendChild(BulletPoint2_text)
        BulletPoint3.appendChild(BulletPoint3_text)
        BulletPoint4.appendChild(BulletPoint4_text)
        BulletPoint5.appendChild(BulletPoint5_text)
        Manufacturer.appendChild(Manufacturer_text)
        MfrPartNumber.appendChild(MfrPartNumber_text)
        SearchTerms1.appendChild(SearchTerms1_text)
        SearchTerms2.appendChild(SearchTerms2_text)
        SearchTerms3.appendChild(SearchTerms3_text)
        SearchTerms4.appendChild(SearchTerms4_text)
        SearchTerms5.appendChild(SearchTerms5_text)
        if goods_upload_obj['target_audience_keywords1']:
            TargetAudience1_text = doc.createTextNode(goods_upload_obj['target_audience_keywords1'])
            TargetAudience1.appendChild(TargetAudience1_text)
        if goods_upload_obj['target_audience_keywords2']:
            TargetAudience2_text = doc.createTextNode(goods_upload_obj['target_audience_keywords2'])
            TargetAudience2.appendChild(TargetAudience2_text)
        if goods_upload_obj['target_audience_keywords3']:
            TargetAudience3_text = doc.createTextNode(goods_upload_obj['target_audience_keywords3'])
            TargetAudience3.appendChild(TargetAudience3_text)
        RecommendedBrowseNode.appendChild(RecommendedBrowseNode_text)
        MerchantShippingGroupName.appendChild(MerchantShippingGroupName_text)
        logging.debug('time-p7 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        DescriptionData.appendChild(Title)
        DescriptionData.appendChild(Brand)
        DescriptionData.appendChild(Description)
        DescriptionData.appendChild(BulletPoint1)
        DescriptionData.appendChild(BulletPoint2)
        DescriptionData.appendChild(BulletPoint3)
        DescriptionData.appendChild(BulletPoint4)
        DescriptionData.appendChild(BulletPoint5)
        DescriptionData.appendChild(Manufacturer)
        DescriptionData.appendChild(MfrPartNumber)

        DescriptionData.appendChild(SearchTerms1)
        DescriptionData.appendChild(SearchTerms2)
        DescriptionData.appendChild(SearchTerms3)
        DescriptionData.appendChild(SearchTerms4)
        DescriptionData.appendChild(SearchTerms5)
        if goods_upload_obj['item_type']:
            ItemType_text = doc.createTextNode(goods_upload_obj['item_type'])
            ItemType.appendChild(ItemType_text)
            DescriptionData.appendChild(ItemType)
        if goods_upload_obj['target_audience_keywords1']:
            DescriptionData.appendChild(TargetAudience1)
        if goods_upload_obj['target_audience_keywords2']:
            DescriptionData.appendChild(TargetAudience2)
        if goods_upload_obj['target_audience_keywords3']:
            DescriptionData.appendChild(TargetAudience3)
        DescriptionData.appendChild(RecommendedBrowseNode)
        DescriptionData.appendChild(MerchantShippingGroupName)
        if params['product_type'] == 'Luggage':
            ItemWeight = doc.createElement('ItemWeight')
            ItemWeight.setAttribute('unitOfMeasure', str(goods_upload_obj['item_weight_unit']))
            ItemWeightText = doc.createTextNode(goods_upload_obj['item_weight'])
            ItemWeight.appendChild(ItemWeightText)
            DescriptionData.appendChild(ItemWeight)

        logging.debug('time-p8 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        product_data = ''
        # Toys,Home,ClothingAccessories,HomeImprovement,Jewelry,ProductClothing,Beauty,PetSupplies,Health,Lighting,
        # ThreeDPrinting,ToysBaby,Office,Sports,LuxuryBeauty,Furniture,AutoAccessory,Wireless,MusicalInstruments
        if params['product_type'] == 'Toys':
            product_data = self.is_Toys(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'Home':
            product_data = self.is_Home(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'ClothingAccessories':
            product_data = self.is_ClothingAccessories(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'HomeImprovement':
            product_data = self.is_HomeImprovement(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'Jewelry':
            product_data = self.is_Jewelry(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'ProductClothing':
            product_data = self.is_ProductClothing(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'Beauty':
            product_data = self.is_Beauty(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'PetSupplies':
            product_data = self.is_PetSupplies(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'Health':
            product_data = self.is_Health(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'Lighting':
            product_data = self.is_Lighting(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'ThreeDPrinting':
            product_data = self.is_ThreeDPrinting(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'ToysBaby':
            product_data = self.is_ToysBaby(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'Office':
            product_data = self.is_Office(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'Sports':
            product_data = self.is_Sports(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'LuxuryBeauty':
            product_data = self.is_LuxuryBeauty(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'Furniture':
            product_data = self.is_Furniture(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'AutoAccessory':
            product_data = self.is_AutoAccessory(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'Wireless':
            product_data = self.is_Wireless(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'MusicalInstruments':
            product_data = self.is_MusicalInstruments(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'Baby':
            product_data = self.is_Baby(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'Luggage':
            product_data = self.is_Luggage(params, doc, goods_upload_obj, goods_upload_variation_obj)
        elif params['product_type'] == 'CE':
            product_data = self.is_CE(params, doc, goods_upload_obj, goods_upload_variation_obj)
        if product_data:
            ProductData.appendChild(product_data)
        logging.debug('time-p9 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        Product.appendChild(SKU)
        if params['parent_child'] != 'parent':
            Product.appendChild(StandardProductID)
        Product.appendChild(Condition)
        Product.appendChild(ItemPackageQuantity)
        Product.appendChild(NumberOfItems)
        Product.appendChild(DescriptionData)
        Product.appendChild(ProductData)

        Message.appendChild(Product)
        logging.debug('time-p10 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return Message

    def local_time_to_utc_str(self, local_time):
        date_time = datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
        utc_tran = local2utcTime.local2utc(date_time).strftime("%Y-%m-%dT%H:%M:%SZ")
        utc_time_str = str(utc_tran)
        return utc_time_str

    def product_price_to_xml(self, params):
        logging.debug('time-pr1 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        goods_upload_obj = params['goods_upload']
        time.sleep(0.001)
        timeStamp = int(time.time() * 1000)
        logging.debug('time-timeStamp is: %s' % timeStamp)
        doc = params['doc']
        goods_upload_variation_obj = params['goods_upload_variation_obj']

        # Message
        Message = doc.createElement('Message')
        MessageID = doc.createElement('MessageID')
        MessageID_text = doc.createTextNode('%s' % timeStamp)
        MessageID.appendChild(MessageID_text)
        Message.appendChild(MessageID)

        OperationType = doc.createElement('OperationType')
        OperationType_text = doc.createTextNode('Update')
        OperationType.appendChild(OperationType_text)
        Message.appendChild(OperationType)
        # Price
        sale_sites = {'US': 'USD', 'DE': 'EUR', 'FR': 'EUR', 'UK': 'GBP', 'AU': 'AUD', 'IN': 'INR'}
        site = goods_upload_obj['ShopSets'].split('-')[-1].split('/')[0]
        Price = doc.createElement('Price')
        SKU = doc.createElement('SKU')
        StandardPrice = doc.createElement('StandardPrice')
        StandardPrice.setAttribute('currency',sale_sites[site])
        Sale = doc.createElement('Sale')
        StartDate = doc.createElement('StartDate')
        EndDate = doc.createElement('EndDate')
        SalePrice = doc.createElement('SalePrice')
        SalePrice.setAttribute('currency',sale_sites[site])
        MaximumRetailPrice = doc.createElement('MaximumRetailPrice')
        MaximumRetailPrice.setAttribute('currency',sale_sites[site])
        logging.debug('time-pr2 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        MRP_text = doc.createTextNode('')
        if goods_upload_obj['mrp']:
            MRP_text = doc.createTextNode(goods_upload_obj['mrp'])
            MaximumRetailPrice.appendChild(MRP_text)

        if params['parent_child'] == 'child':
            sku_text = goods_upload_variation_obj['child_sku']
            standard_price = goods_upload_variation_obj['price']
            if goods_upload_variation_obj['item_quantity'] != '1':
                sku_text += '*' + str(goods_upload_variation_obj['item_quantity'])
        else:
            sku_text = goods_upload_obj['item_sku']
            standard_price = goods_upload_obj['standard_price']
            if goods_upload_obj['item_package_quantity'] != '1':
                sku_text += '*' + str(goods_upload_obj['item_package_quantity'])
        SKU_text = doc.createTextNode(sku_text)
        StandardPrice_text = doc.createTextNode(standard_price)
        logging.debug('time-pr3 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if params['variation'] == 0:
            if goods_upload_obj['sale_from_date'] and goods_upload_obj['sale_end_date']:
                SalePrice_text = doc.createTextNode(goods_upload_obj['sale_price'])
                startDate = self.local_time_to_utc_str(str(goods_upload_obj['sale_from_date']))
                StartDate_text = doc.createTextNode(startDate)
                endDate = self.local_time_to_utc_str(str(goods_upload_obj['sale_end_date']))
                EndDate_text = doc.createTextNode(endDate)
        logging.debug('time-pr4 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        SKU.appendChild(SKU_text)
        StandardPrice.appendChild(StandardPrice_text)
        if params['variation'] == 0:
            if goods_upload_obj['sale_from_date'] and goods_upload_obj['sale_end_date']:
                StartDate.appendChild(StartDate_text)
                EndDate.appendChild(EndDate_text)
                SalePrice.appendChild(SalePrice_text)
                Sale.appendChild(StartDate)
                Sale.appendChild(EndDate)
                Sale.appendChild(SalePrice)

        Price.appendChild(SKU)
        Price.appendChild(StandardPrice)
        logging.debug('time-pr5 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if goods_upload_obj['mrp']:
            Price.appendChild(MaximumRetailPrice)
        if params['variation'] == 0:
            if goods_upload_obj['sale_from_date'] and goods_upload_obj['sale_end_date']:
                Price.appendChild(Sale)

        Message.appendChild(Price)
        logging.debug('time-pr6 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return Message

    def product_inventory_to_xml(self, params):
        logging.debug('time-inv1 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        goods_upload_obj = params['goods_upload']
        time.sleep(0.001)
        timeStamp = int(time.time() * 1000)
        logging.debug('time-timeStamp is: %s' % timeStamp)
        doc = params['doc']
        goods_upload_variation_obj = params['goods_upload_variation_obj']

        # Message
        Message = doc.createElement('Message')
        MessageID = doc.createElement('MessageID')
        MessageID_text = doc.createTextNode('%s' % timeStamp)
        MessageID.appendChild(MessageID_text)
        Message.appendChild(MessageID)

        OperationType = doc.createElement('OperationType')
        OperationType_text = doc.createTextNode('Update')
        OperationType.appendChild(OperationType_text)
        Message.appendChild(OperationType)

        # Inventory
        Inventory = doc.createElement('Inventory')
        SKU = doc.createElement('SKU')
        Quantity = doc.createElement('Quantity')
        FulfillmentLatency = doc.createElement('FulfillmentLatency')
        logging.debug('time-inv2 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if params['parent_child'] == 'child':
            sku_text = goods_upload_variation_obj['child_sku']
            if goods_upload_variation_obj['item_quantity'] != '1':
                sku_text += '*' + str(goods_upload_variation_obj['item_quantity'])
        else:
            sku_text = goods_upload_obj['item_sku']
            if goods_upload_obj['item_package_quantity'] != '1':
                sku_text += '*' + str(goods_upload_obj['item_package_quantity'])
        SKU_text = doc.createTextNode(sku_text)
        Quantity_text = doc.createTextNode(goods_upload_obj['quantity'])

        SKU.appendChild(SKU_text)
        Quantity.appendChild(Quantity_text)

        Inventory.appendChild(SKU)
        Inventory.appendChild(Quantity)
        logging.debug('time-inv3 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if goods_upload_obj['fulfillment_latency']:
            FulfillmentLatency_text = doc.createTextNode(goods_upload_obj['fulfillment_latency'])
            FulfillmentLatency.appendChild(FulfillmentLatency_text)
            Inventory.appendChild(FulfillmentLatency)

        Message.appendChild(Inventory)
        logging.debug('time-inv4 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return Message

    def product_relationship_to_xml(self, params):
        logging.debug('time-rela1 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        goods_upload_obj = params['goods_upload']
        time.sleep(0.001)
        timeStamp = int(time.time() * 1000)
        logging.debug('time-timeStamp is: %s' % timeStamp)
        doc = params['doc']
        goods_upload_variation_obj = params['goods_upload_variation_obj']

        # Message
        Message = doc.createElement('Message')
        MessageID = doc.createElement('MessageID')
        MessageID_text = doc.createTextNode('%s' % timeStamp)
        MessageID.appendChild(MessageID_text)
        Message.appendChild(MessageID)

        OperationType = doc.createElement('OperationType')
        OperationType_text = doc.createTextNode('Update')
        OperationType.appendChild(OperationType_text)
        Message.appendChild(OperationType)
        # Relationship
        Relationship = doc.createElement('Relationship')
        ParentSKU = doc.createElement('ParentSKU')
        Relation = doc.createElement('Relation')
        SKU = doc.createElement('SKU')
        Type = doc.createElement('Type')
        logging.debug('time-rela2 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        parentSKU_text = goods_upload_obj['item_sku']
        sku_text = goods_upload_variation_obj['child_sku']
        if goods_upload_variation_obj['item_quantity'] != '1':
            sku_text += '*' + str(goods_upload_variation_obj['item_quantity'])
        if goods_upload_obj['item_package_quantity'] != '1':
            parentSKU_text += '*' + str(goods_upload_obj['item_package_quantity'])
        ParentSKU_text = doc.createTextNode(parentSKU_text)
        SKU_text = doc.createTextNode(sku_text)
        Type_text = doc.createTextNode('Variation')

        ParentSKU.appendChild(ParentSKU_text)
        SKU.appendChild(SKU_text)
        Type.appendChild(Type_text)
        Relation.appendChild(SKU)
        Relation.appendChild(Type)

        Relationship.appendChild(ParentSKU)
        Relationship.appendChild(Relation)

        Message.appendChild(Relationship)
        logging.debug('time-rela3 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return Message

    def get_xml(self, params):
        logging.debug('time-a is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        doc = xml.dom.minidom.Document()
        AmazonEnvelope = doc.createElement('AmazonEnvelope')
        AmazonEnvelope.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        AmazonEnvelope.setAttribute('xsi:noNamespaceSchemaLocation', 'amzn-envelope.xsd')
        doc.appendChild(AmazonEnvelope)
        # Header
        Header = doc.createElement('Header')
        DocumentVersion = doc.createElement('DocumentVersion')
        MerchantIdentifier = doc.createElement('MerchantIdentifier')
        DocumentVersion_text = doc.createTextNode('1.01')
        MerchantIdentifier_text = doc.createTextNode('%s' % params['auth_info']['SellerId'])
        DocumentVersion.appendChild(DocumentVersion_text)
        MerchantIdentifier.appendChild(MerchantIdentifier_text)
        Header.appendChild(DocumentVersion)
        Header.appendChild(MerchantIdentifier)
        AmazonEnvelope.appendChild(Header)
        params['doc'] = doc
        logging.debug('time-b is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        t_templet_amazon_published_variation_objs = params['t_templet_amazon_published_variation_objs']

        # MessageType
        MessageType = doc.createElement('MessageType')
        MessageType_text = doc.createTextNode(params['productType'])
        MessageType.appendChild(MessageType_text)
        AmazonEnvelope.appendChild(MessageType)
        # PurgeAndReplace
        PurgeAndReplace = doc.createElement('PurgeAndReplace')
        PurgeAndReplace_text = doc.createTextNode('false')
        PurgeAndReplace.appendChild(PurgeAndReplace_text)
        AmazonEnvelope.appendChild(PurgeAndReplace)
        params['goods_upload_variation_obj'] = ''
        Message = ''
        logging.debug('time-c is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        params['parent_child'] = ''
        if params['variation'] == 1:
            params['parent_child'] = 'parent'
            params['goods_upload_variation_obj'] = t_templet_amazon_published_variation_objs[0]
        logging.debug('time-d is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if params['productType'] == 'Product':
            if params['variation'] == 1:
                Message = self.products_to_xml(params=params)
            else:
                Message = self.products_to_xml(params=params)
        logging.debug('time-e is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if params['productType'] == 'Price':
            Message = self.product_price_to_xml(params)
        if params['productType'] == 'Inventory':
            Message = self.product_inventory_to_xml(params)
        if params['productType'] != 'Relationship':
            AmazonEnvelope.appendChild(Message)
        if params['variation'] == 1:
            params['parent_child'] = 'child'
            for i in range(0, len(t_templet_amazon_published_variation_objs)):
                params['goods_upload_variation_obj'] = t_templet_amazon_published_variation_objs[i]
                if params['productType'] == 'Product':
                    Message = self.products_to_xml(params)
                if params['productType'] == 'Price':
                    Message = self.product_price_to_xml(params)
                if params['productType'] == 'Inventory':
                    Message = self.product_inventory_to_xml(params)
                if params['productType'] == 'Relationship':
                    Message = self.product_relationship_to_xml(params)
                AmazonEnvelope.appendChild(Message)
        feed = doc.toxml()
        return feed

    def stitching_goods_info_to_body(self, params):
        logging.debug('time7-1 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        result = {'errorcode': 0, 'errortext': '', 'params': params, 'result': ''}
        varation = params['variation']
        upcIds = {}

        if params['t_templet_amazon_published_variation_objs']:
            logging.debug('time7-2 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            for t_templet_amazon_published_variation_obj in params['t_templet_amazon_published_variation_objs']:
                sku_text = t_templet_amazon_published_variation_obj['child_sku']
                if t_templet_amazon_published_variation_obj['item_quantity'] != '1':
                    sku_text += '*' + str(t_templet_amazon_published_variation_obj['item_quantity'])
                upcIds[t_templet_amazon_published_variation_obj['productSKU'].strip()] = sku_text
            logging.debug('time7-3 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        auth_info = params['auth_info']
        goods_upload_obj = params['goods_upload']
        auth_info['variation'] = varation
        auth_info['upcIds'] = upcIds
        auth_info['sku'] = goods_upload_obj['productSKU'].strip()
        params['product_type'] = goods_upload_obj['upload_product_type']
        rtstring = json.dumps(auth_info)
        logging.debug('time7-4 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        params['productType'] = 'Product'
        feed = self.get_xml(params)
        logging.debug('time7-5 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        rtstring += '||' + feed

        params['productType'] = 'Inventory'
        feed = self.get_xml(params)
        logging.debug('time7-6 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        rtstring += '||' + feed

        params['productType'] = 'Price'
        feed = self.get_xml(params)
        logging.debug('time7-7 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        rtstring += '||' + feed
        if params['variation'] == 1:
            params['productType'] = 'Relationship'
            feed = self.get_xml(params)

            rtstring += '||' + feed
        logging.debug('time7-8 is: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        result['result'] = rtstring
        return result

