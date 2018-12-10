# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: plan_return.py
 @time: 2018/12/7 14:20
"""  
plan_return = {'CreateInboundShipmentPlanResult': {'InboundShipmentPlans': {'member': {'LabelPrepType': {'value': 'SELLER_LABEL'}, 'EstimatedBoxContentsFee': {'TotalUnits': {'value': '115'}, 'TotalFee': {'CurrencyCode': {'value': 'USD'}, 'Value': {'value': '17.25'}, 'value': '\n            '}, 'value': '\n          ', 'FeePerUnit': {'CurrencyCode': {'value': 'USD'}, 'Value': {'value': '0.15'}, 'value': '\n            '}}, 'Items': {'member': [{'SellerSKU': {'value': 'A!N!!#0232F04'}, 'FulfillmentNetworkSKU': {'value': 'X001FVBCN3'}, 'value': '\n            ', 'Quantity': {'value': '40'}}, {'SellerSKU': {'value': 'A!N!!#0272FBK'}, 'FulfillmentNetworkSKU': {'value': 'X001NZP2OB'}, 'value': '\n            ', 'Quantity': {'value': '30'}}, {'SellerSKU': {'value': 'A!N!!#0232F01'}, 'FulfillmentNetworkSKU': {'value': 'X001FVKKB3'}, 'value': '\n            ', 'Quantity': {'value': '25'}}, {'SellerSKU': {'value': 'P1X04DZ6YE8071'}, 'FulfillmentNetworkSKU': {'value': 'X001NX5LBH'}, 'value': '\n            ', 'Quantity': {'value': '20'}}], 'value': '\n          '}, 'ShipToAddress': {'StateOrProvinceCode': {'value': 'IL'}, 'City': {'value': 'Joliet'}, 'Name': {'value': 'MDW2'}, 'CountryCode': {'value': 'US'}, 'value': '\n          ', 'AddressLine1': {'value': '250 EMERALD DR'}, 'PostalCode': {'value': '60433-3280'}}, 'value': '\n        ', 'ShipmentId': {'value': 'FBA15FK1MPYH'}, 'DestinationFulfillmentCenterId': {'value': 'MDW2'}}, 'value': '\n      '}, 'value': '\n    '}, 'ResponseMetadata': {'RequestId': {'value': 'c8d92382-a505-4fff-af7d-d17e3d87e66a'}, 'value': '\n    '}, 'value': '\n  '}
shipment_plan = plan_return.get('CreateInboundShipmentPlanResult').get('InboundShipmentPlans').get('member')

plan_record_list = list()
plan_each_dict = dict()


def parse_plan(plan_dict):
    for key, val in plan_dict.items():
        if key == 'LabelPrepType':
            print 'label_prep:'
            print key, ':', val['value']
            print
        elif key == 'Items':
            print 'items:'
            member_obj = val['member']
            if isinstance(member_obj, list):
                for member_each in val['member']:
                    for each_key, each_val in member_each.items():
                        if each_key != 'value':
                            print each_key, ':', each_val['value']
            print
        elif key == 'ShipmentId':
            print 'ship_id:'
            print key,':', val['value']
            print
        elif key == 'DestinationFulfillmentCenterId':
            print 'center_id'
            print key, ':', val['value']
            print
        elif key == 'ShipToAddress':
            val.pop('value')
            print 'ship_to:'
            for ship_key, ship_val in val.items():
                print ship_key, ':', ship_val['value']
            print


if isinstance(shipment_plan, dict):
    ShipmentId = shipment_plan['ShipmentId']['value']
    LabelPrepType = shipment_plan['LabelPrepType']['value']
    DestinationFulfillmentCenterId = shipment_plan['DestinationFulfillmentCenterId']['value']
    ShipToAddress_StateOrProvinceCode = shipment_plan['ShipToAddress']['StateOrProvinceCode']['value']
    ShipToAddress_City = shipment_plan['ShipToAddress']['City']['value']
    ShipToAddress_Name = shipment_plan['ShipToAddress']['Name']['value']
    ShipToAddress_CountryCode = shipment_plan['ShipToAddress']['CountryCode']['value']
    ShipToAddress_AddressLine1 = shipment_plan['ShipToAddress']['AddressLine1']['value']
    ShipToAddress_PostalCode = shipment_plan['ShipToAddress']['PostalCode']['value']

    items_obj = shipment_plan['Items']['member']
    if isinstance(items_obj, list):
        for item_each in items_obj:
            SellerSKU = item_each['SellerSKU']['value']
            FulfillmentNetworkSKU = item_each['FulfillmentNetworkSKU']['value']
            Quantity = item_each['Quantity']['value']
            plan_record_list.append([ShipmentId, LabelPrepType, DestinationFulfillmentCenterId,
                                     ShipToAddress_StateOrProvinceCode, ShipToAddress_City, ShipToAddress_Name,
                                     ShipToAddress_CountryCode, ShipToAddress_AddressLine1,
                                     ShipToAddress_PostalCode, SellerSKU, FulfillmentNetworkSKU, Quantity])
    else:
        SellerSKU = items_obj['SellerSKU']['value']
        FulfillmentNetworkSKU = items_obj['FulfillmentNetworkSKU']['value']
        Quantity = items_obj['Quantity']['value']
        plan_record_list.append([ShipmentId, LabelPrepType, DestinationFulfillmentCenterId,
                                 ShipToAddress_StateOrProvinceCode, ShipToAddress_City, ShipToAddress_Name,
                                 ShipToAddress_CountryCode, ShipToAddress_AddressLine1,
                                 ShipToAddress_PostalCode, SellerSKU, FulfillmentNetworkSKU, Quantity])

    for i in plan_record_list:
        print i


    #
    # for key, val in shipment_plan.items():
    #     if key == 'LabelPrepType':
    #         print 'label_prep:'
    #         print key, ':', val['value']
    #         print
    #         plan_each_dict['LabelPrepType'] = val['value']
    #     elif key == 'Items':
    #         print 'items:'
    #         member_obj = val['member']
    #         if isinstance(member_obj, list):
    #             for member_each in val['member']:
    #                 for each_key, each_val in member_each.items():
    #                     if each_key != 'value':
    #                         print each_key, ':', each_val['value']
    #         else:
    #             pass
    #         print
    #     elif key == 'ShipmentId':
    #         print 'ship_id:'
    #         print key,':', val['value']
    #         print
    #     elif key == 'DestinationFulfillmentCenterId':
    #         print 'center_id'
    #         print key, ':', val['value']
    #         print
    #     elif key == 'ShipToAddress':
    #         val.pop('value')
    #         print 'ship_to:'
    #         for ship_key, ship_val in val.items():
    #             print ship_key, ':', ship_val['value']
    #         print
    #
