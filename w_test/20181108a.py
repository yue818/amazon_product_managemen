# -*- coding:utf-8 -*-

"""
 @desc:
 @author: wuchongxiang
 @site:
 @software: PyCharm
 @file: 20181108a.py
 @time: 2018/11/8 16:14
"""
product_list = ['(!$4${4$1802033333333333333333333', '(!$4${4$180201', '(!$4${4$2']
error_list = list()
error_desc_dict = dict()
res = {'Header': {'MerchantIdentifier': {'value': 'A34SE6EB7V1VZJ'}, 'DocumentVersion': {'value': '1.02'}, 'value': '\n\t\t'}, 'Message': {'ProcessingReport': {'Result': [{'AdditionalInfo': {'SKU': {'value': '(!$4${4$1802022222222222'}, 'value': '\n\t\t\t\t\t'}, 'ResultDescription': {'value': "We're unable to complete your request because this SKU is not in the Amazon catalog. If this was a deleted SKU, wait 24 hours before resubmitting it. If you tried to add this SKU to the Amazon catalog before, check your data and correct any errors before resubmitting. "}, 'value': '\n\t\t\t\t', 'ResultMessageCode': {'value': '13013'}, 'MessageID': {'value': '1'}, 'ResultCode': {'value': 'Error'}}, {'AdditionalInfo': {'SKU': {'value': '(!$4${4$180181111111111111111'}, 'value': '\n\t\t\t\t\t'}, 'ResultDescription': {'value': "We're unable to complete your request because this SKU is not in the Amazon catalog. If this was a deleted SKU, wait 24 hours before resubmitting it. If you tried to add this SKU to the Amazon catalog before, check your data and correct any errors before resubmitting. "}, 'value': '\n\t\t\t\t', 'ResultMessageCode': {'value': '13013'}, 'MessageID': {'value': '2'}, 'ResultCode': {'value': 'Error'}}, {'AdditionalInfo': {'SKU': {'value': '(!$4${4$1802033333333333333333333'}, 'value': '\n\t\t\t\t\t'}, 'ResultDescription': {'value': "We're unable to complete your request because this SKU is not in the Amazon catalog. If this was a deleted SKU, wait 24 hours before resubmitting it. If you tried to add this SKU to the Amazon catalog before, check your data and correct any errors before resubmitting. "}, 'value': '\n\t\t\t\t', 'ResultMessageCode': {'value': '13013'}, 'MessageID': {'value': '3'}, 'ResultCode': {'value': 'Error'}}], 'DocumentTransactionID': {'value': '91401017843'}, 'ProcessingSummary': {'MessagesProcessed': {'value': '3'}, 'MessagesWithWarning': {'value': '0'}, 'MessagesSuccessful': {'value': '0'}, 'value': '\n\t\t\t\t', 'MessagesWithError': {'value': '3'}}, 'value': '\n\t\t\t', 'StatusCode': {'value': 'Complete'}}, 'value': '\n\t\t', 'MessageID': {'value': '1'}}, 'noNamespaceSchemaLocation': {'namespace': 'http://www.w3.org/2001/XMLSchema-instance', 'value': 'amzn-envelope.xsd'}, 'MessageType': {'value': 'ProcessingReport'}, 'value': '\n\t'}
# res = {'Header': {'MerchantIdentifier': {'value': 'A34SE6EB7V1VZJ'}, 'DocumentVersion': {'value': '1.02'}, 'value': '\n\t\t'}, 'Message': {'ProcessingReport': {'Result': {'AdditionalInfo': {'SKU': {'value': '(!$4${4$1802033333333333333333333'}, 'value': '\n\t\t\t\t\t'}, 'ResultDescription': {'value': "We're unable to complete your request because this SKU is not in the Amazon catalog. If this was a deleted SKU, wait 24 hours before resubmitting it. If you tried to add this SKU to the Amazon catalog before, check your data and correct any errors before resubmitting. "}, 'value': '\n\t\t\t\t', 'ResultMessageCode': {'value': '13013'}, 'MessageID': {'value': '3'}, 'ResultCode': {'value': 'Error'}}, 'DocumentTransactionID': {'value': '91411017843'}, 'ProcessingSummary': {'MessagesProcessed': {'value': '1'}, 'MessagesWithWarning': {'value': '0'}, 'MessagesSuccessful': {'value': '0'}, 'value': '\n\t\t\t\t', 'MessagesWithError': {'value': '1'}}, 'value': '\n\t\t\t', 'StatusCode': {'value': 'Complete'}}, 'value': '\n\t\t', 'MessageID': {'value': '1'}}, 'noNamespaceSchemaLocation': {'namespace': 'http://www.w3.org/2001/XMLSchema-instance', 'value': 'amzn-envelope.xsd'}, 'MessageType': {'value': 'ProcessingReport'}, 'value': '\n\t'}

result_obj = res.get('Message').get('ProcessingReport').get('Result')

if isinstance(result_obj, list):
    for val in result_obj:
        err_desc = val.get('ResultDescription').get('value')
        sku = val.get('AdditionalInfo').get('SKU').get('value')
        error_desc_dict[sku] = err_desc
        error_list.append(sku)
elif isinstance(result_obj, dict):
    sku = result_obj.get('AdditionalInfo').get('SKU').get('value')
    err_desc = result_obj.get('ResultDescription').get('value')
    error_list.append(sku)
    error_desc_dict[sku] = err_desc


product_list = list(set(product_list) - set(error_list))
print error_list
print product_list
print error_desc_dict
print error_desc_dict.get('111111111', 'default')

