# -*- coding: utf-8 -*-
# editer: 孙健

# 根据 URL 的request请求参数，显示自定义Button
# 数据格式：
# 'modelname': {
#     'full_path': 'no request field url',
#     'filter_button': [
#         {
#             'request_key': 'request field, can no field',
#             'request_value': 'request value',
#             'del_button': [
#                 'need to delete button name, there is a list',
#             ],
#         }
#     ]
# }

FILTER_BUTTON_CONFIG = {
    't_joom_price_parity': {
        'full_path': '/Project/admin/joom_app/t_joom_price_parity/',
        'filter_button': [
            {
                'request_key': '',
                'request_value': '',
                'del_button': [
                    'batch_joom_competitor_products',
                    'set_joom_product_price_parity_status_wait',
                    'set_joom_product_price_parity_status_no',
                    'set_joom_product_price_parity_status_todo',
                    'batch_joom_price_parity',
                ],
            },
            {
                'request_key': 'priceParity_Status',
                'request_value': 'ALL',
                'del_button': [
                    'batch_joom_price_parity',
                    'set_joom_product_price_parity_status_todo'
                ],
            },
            {
                'request_key': 'priceParity_Status',
                'request_value': 'WAIT',
                'del_button': [
                    'set_joom_product_price_parity_status_wait',
                    'batch_joom_price_parity'
                ],
            },
            {
                'request_key': 'priceParity_Status',
                'request_value': 'NO',
                'del_button': [
                    'set_joom_product_price_parity_status_no',
                    'batch_joom_price_parity',
                    'set_joom_product_price_parity_status_todo'
                ],
            },
            {
                'request_key': 'priceParity_Status',
                'request_value': 'TODO',
                'del_button': [
                    'set_joom_product_price_parity_status_todo',
                    'set_joom_product_price_parity_status_no'
                ],
            },
            {
                'request_key': 'priceParity_Status',
                'request_value': 'SUCCESS',
                'del_button': [
                    'set_joom_product_price_parity_status_no',
                    'batch_joom_price_parity',
                    'set_joom_product_price_parity_status_todo',
                ],
            },
            {
                'request_key': 'priceParity_Status',
                'request_value': 'FAILED',
                'del_button': [
                    'set_joom_product_price_parity_status_no',
                    'batch_joom_price_parity',
                    'set_joom_product_price_parity_status_todo',
                ],
            },
        ]
    },
    't_aliexpress_price_parity': {
        'full_path': '/Project/admin/aliexpress_app/t_aliexpress_price_parity/',
        'filter_button': [
            {
                'request_key': '',
                'request_value': '',
                'del_button': [
                    'batch_joom_competitor_products',
                    'set_joom_product_price_parity_status_wait',
                    'set_joom_product_price_parity_status_no',
                    'set_joom_product_price_parity_status_todo',
                    'batch_joom_price_parity',
                ],
            },
            {
                'request_key': 'priceParity_Status',
                'request_value': 'ALL',
                'del_button': [
                    'batch_joom_price_parity',
                    'set_joom_product_price_parity_status_todo'
                ],
            },
            {
                'request_key': 'priceParity_Status',
                'request_value': 'WAIT',
                'del_button': [
                    'set_joom_product_price_parity_status_wait',
                    'batch_joom_price_parity'
                ],
            },
            {
                'request_key': 'priceParity_Status',
                'request_value': 'NO',
                'del_button': [
                    'set_joom_product_price_parity_status_no',
                    'batch_joom_price_parity',
                    'set_joom_product_price_parity_status_todo'
                ],
            },
            {
                'request_key': 'priceParity_Status',
                'request_value': 'TODO',
                'del_button': [
                    'set_joom_product_price_parity_status_todo',
                    'set_joom_product_price_parity_status_no'
                ],
            },
            {
                'request_key': 'priceParity_Status',
                'request_value': 'SUCCESS',
                'del_button': [
                    'set_joom_product_price_parity_status_no',
                    'batch_joom_price_parity',
                    'set_joom_product_price_parity_status_todo',
                ],
            },
            {
                'request_key': 'priceParity_Status',
                'request_value': 'FAILED',
                'del_button': [
                    'set_joom_product_price_parity_status_no',
                    'batch_joom_price_parity',
                    'set_joom_product_price_parity_status_todo',
                ],
            },
        ]
    },
    't_mymall_template_publish': {
        'full_path': '/Project/admin/mymall_app/t_mymall_template_publish/',
        'filter_button': [
            {
                'request_key': '',
                'request_value': '',
                'del_button': [
                    'to_pub',
                    'set_published_failed_to_success',
                    'set_published_falied_to_todo',
                    'set_published_success_to_falied',
                ],
            },
            {
                'request_key': 'PublishResult',
                'request_value': 'TODO',
                'del_button': [
                    'set_published_failed_to_success',
                    'set_published_falied_to_todo',
                    'set_published_success_to_falied',
                ],
            },
            {
                'request_key': 'PublishResult',
                'request_value': 'DONE',
                'del_button': [
                    'to_pub',
                    'set_published_failed_to_success',
                    'set_published_falied_to_todo',
                    'set_published_success_to_falied',
                ],
            },
            {
                'request_key': 'PublishResult',
                'request_value': 'SUCCESS',
                'del_button': [
                    'to_pub',
                    'set_published_failed_to_success',
                    'set_published_falied_to_todo',
                ],
            },
            {
                'request_key': 'PublishResult',
                'request_value': 'FAILED',
                'del_button': [
                    'to_pub',
                    'set_published_success_to_falied',
                ],
            },
        ]
    },
    't_online_info_walmart_publish': {
        'full_path': '/Project/admin/walmart_app/t_online_info_walmart_publish/',
        'filter_button': [
            {
                'request_key': '',
                'request_value': '',
                'del_button': [
                    'batch_upload',
                ],
            },
            {
                'request_key': 'feedStatus',
                'request_value': 'RECEIVED',
                'del_button': [
                    'batch_upload',
                ],
            },
            {
                'request_key': 'feedStatus',
                'request_value': 'INPROGRESS',
                'del_button': [
                    'batch_upload',
                ],
            },
            {
                'request_key': 'feedStatus',
                'request_value': 'ERROR',
                'del_button': [
                    'batch_upload',
                ],
            },
            {
                'request_key': 'feedStatus',
                'request_value': 'PROCESSED',
                'del_button': [
                    'batch_upload',
                ],
            },
        ]
    }
}


# 根据 URL 的request请求参数，显示自定义页面列表项目
# 数据格式：
# 'modelname': {
#     'full_path': 'no request field url',
#     'filter_field': [
#         {
#             'request_key': 'request field, can no field',
#             'request_value': 'request value',
#             'del_field': [
#                 'need to delete field name in list_display, there is a list',
#             ],
#         }
#     ]
# }

FILTER_FIELD_CONFIG = {
    't_joom_price_parity': {
        'full_path': '/Project/admin/joom_app/t_joom_price_parity/',
        'filter_field': [
            {
                'request_key': 'priceParity_Status',
                'request_value': 'ALL',
                'del_field': [
                    'show_Competitor_image',
                    'competitor_ProductID',
                    'show_competitor_price_range',
                    'show_competitor_Orders7Days',
                    'priceParity_Remarks',
                    'Options',
                ],
            },
        ]
    }
}
