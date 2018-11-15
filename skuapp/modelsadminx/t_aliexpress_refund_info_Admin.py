# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from datetime import datetime
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field, Div, FormActions, Submit, Button, ButtonHolder, InlineRadios, Reset, StrictButton, HTML, Hidden, Alert

class t_aliexpress_refund_info_Admin(object):    

    show_aliexpress_refund_info = True
    
    list_filter = ('ShopOrderNumber','ShopName','ProductSKU','Country','ClosingDate','Sale_price','Refund_price','Paypal_Account','dj_user','Refund_reason','Refund_id','Remarks','Update_time')
    search_fields = ('ShopOrderNumber','ShopName','ProductSKU','Country','Sale_price','Refund_price','Paypal_Account','dj_user','Refund_reason','Refund_id','Remarks')
    list_display = ('id','ShopOrderNumber','ShopName','ProductSKU','Country','ClosingDate','Sale_price','Refund_price','Paypal_Account','dj_user','Refund_reason','Refund_id','Remarks','Update_time')
    list_editable = ('Refund_id','Remarks')
    fields = ('id','ShopOrderNumber','ShopName','ProductSKU','Country','ClosingDate','Sale_price','Refund_id','Refund_price','Paypal_Account','Refund_reason','Update_time')
    #readonly_fields = ('ShopName','ProductSKU','Country','ClosingDate','Sale_price')
    form_layout = (
        Fieldset(u'查询条件',
                Row('ShopOrderNumber'),
                css_class = 'unsort '
        ),
        Fieldset(u'普源实时查询内容',
                Row('ProductSKU','ShopName'),
                Row('Country','Sale_price'),
                Row('ClosingDate'),
                css_class = 'unsort '
        ),
        Fieldset(u'人工填写内容',
                Row('Refund_id','Refund_price'),
                Row('Paypal_Account','Refund_reason'),
                Row('Update_time'),
                css_class = 'unsort '
        ),
    )
    def save_models(self):
        obj = self.new_obj
        obj.Update_time = datetime.now()
        obj.dj_user = self.request.user.username
        obj.save()

    
    
    
           
    
