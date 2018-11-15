# -*- coding: utf-8 -*-

from xadmin.views import BaseAdminPlugin
from django.template import loader

from skuapp.table.t_online_info_wish import t_online_info_wish




class t_online_info_amazon_listing_plugin(BaseAdminPlugin):
    wish_store_plugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.wish_store_plugin)

    def block_search_cata_nav(self, context, nodes):
        ShopName = self.request.GET.get('ShopName')
        Title = self.request.GET.get('Title')
        SKU =  self.request.GET.get('SKU')
        asin1 = self.request.GET.get('asin1')
        ProductID=self.request.GET.get('ProductID')
        ShopSKU=self.request.GET.get('ShopSKU')
        ShopIP = self.request.GET.get('ShopIP')
        Price = self.request.GET.get('Price')

        Seller = self.request.GET.get('Seller')
        TortInfo = self.request.GET.get('TortInfo')
        DataSources = self.request.GET.get('DataSources')
        OperationState = self.request.GET.get('OperationState')
        Published = self.request.GET.get('Published')
        WishExpress = self.request.GET.get('WishExpress')
        is_promoted = self.request.GET.get('is_promoted')
        reviewState= self.request.Get.get('ReviewState')
        dataSources=self.request.GET.get('DataSources')



        search_hidden = ''
        search_hidden_id = 0
        if not ShopName:
            current_shop = ''
        elif ShopName:
            current_shop = ShopName[:8]
        if Title:
            search_hidden = Title
            search_hidden_id = 0
        if ShopSKU:
            search_hidden = ShopSKU
            search_hidden_id = 1
        if SKU:
            search_hidden = SKU
            search_hidden_id = 2

        if ProductID:
            search_hidden = ProductID
            search_hidden_id = 3
        if Seller:
            search_hidden = Seller
            search_hidden_id = 4

        if is_promoted == 'True':
            search_hidden = is_promoted
            search_hidden_id = 5
        else :
            search_hidden = is_promoted
            search_hidden_id = 6


        if reviewState == 'pending':
            search_hidden = reviewState
            search_hidden_id = 7
        elif  reviewState =='approved':
            search_hidden = reviewState
            search_hidden_id = 8
        elif reviewState == 'rejected':
            search_hidden = reviewState
            search_hidden_id = 9


        if TortInfo == 'WY':
            search_hidden = TortInfo
            search_hidden_id = 10
        elif TortInfo == 'Y':
            search_hidden = TortInfo
            search_hidden_id = 11

        elif TortInfo == 'N':
            search_hidden = TortInfo
            search_hidden_id = 12
        else:
            search_hidden = TortInfo
            search_hidden_id = 13

        if dataSources == 'UPLOAD':
            search_hidden = dataSources
            search_hidden_id = 14
        elif dataSources == 'NORMAL':
            search_hidden = dataSources
            search_hidden_id = 15
        else:
            search_hidden = dataSources
            search_hidden_id = 16







        nodes.append(loader.render_to_string('purchase_order_button.html',
                                             {
                                                 'ShopName':ShopName,
                                                 'ShopSKU': ShopSKU,
                                                 'ProductID': ProductID,
                                                 'SKU': SKU,
                                                 'ShopIP': ShopIP,
                                                 'Title': Title,
                                                 'Price': Price,
                                                 'Seller': Seller,
                                                 'TortInfo': TortInfo,
                                                 'DataSources': DataSources,
                                                 'OperationState': OperationState,
                                                 'Published': Published,
                                                 'WishExpress': WishExpress,
                                                 'is_promoted': is_promoted,
                                                 'dataSources':dataSources,
												 'reviewState':reviewState,
												 'search_hidden_id': search_hidden_id,
                                                 'search_hidden': search_hidden,




                                              }))