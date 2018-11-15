# -*- coding: utf-8 -*-
from skuapp.table.t_aliexpress_service_division_analysis import t_aliexpress_service_division_analysis
from xadmin.layout import Fieldset, Row
import re
from django.forms import ModelForm,forms


class Permission(ModelForm):
    def clean_field_name(self):
        data = self.cleaned_data['Productid']
        if not data:  # 如果data不满足满足条件
            raise forms.ValidationError('data is invalid')
        return data

    class Meta:
        model = t_aliexpress_service_division_analysis
        fields = '__all__'




id_pattern = re.compile('.*/(?P<id>\d+)/update/?')

class t_aliexpress_service_division_analysis_Admin(object):
    form=Permission
    importfile_aliexpress_plugin = True
    list_display = ['Seller_Name','Productid', 'Category', 'Discolored', 'Disputes_rate_standard', 'DSRcolored',
                    'DSR_description_standard',
                    'Status', 'Handler_status', 'Importuser', 'Inputdatetime', 'Remark', ]
    list_editable = ['Handler_status',]
    actions = ['handlerstatus_modify']
    search_fields = ['Importuser', 'Category', 'Seller_Name', 'Disputes_rate', 'DSR_description', 'Status',
                     'Handler_status','Productid',]
    list_filter = ['Handler_status', 'Seller_Name']
    list_display_links = ('Remark',)
    fields = ('Remark', 'Handler_status')
    form_layout = (
        Fieldset(u'备注',
                    Row('Remark', ),
                    Row('Handler_status', ),
                    css_class = 'unsort '
                )
                  )
    #form = t_aliexpress_service_division_analysis

    # def get_readonly_fields(self):
    #     """编辑权限设置，本人只能编辑备注"""
    #     request = self.request
    #     matcher = re.match(id_pattern, request.path)
    #     if matcher:
    #         id = matcher.groupdict().get('id')
    #         try:
    #             if request.user.first_name == t_aliexpress_service_division_analysis.objects.filter(id=id)[:1][0].Importuser:
    #                 self.readonly_fields = ['Disputes_rate', 'DSR_description', 'Productid', 'Category', 'Discolored',
    #                                         'Disputes_rate_standard', 'DSRcolored', 'DSR_description_standard',
    #                                         'Status', 'Seller_Name', 'Importuser', 'Inputdatetime']
    #         except Exception:
    #             pass
    #     return self.readonly_fields


    readonly_fields = ['Disputes_rate', 'DSR_description', 'Productid', 'Category', 'Discolored',
                       'Disputes_rate_standard',
                       'DSRcolored', 'DSR_description_standard', 'Status', 'Seller_Name','Importuser','Inputdatetime']

    def handlerstatus_modify(self, request, queryset):
        for qs in queryset.all():
            if not qs.Handler_status:
                Handler_status = True
                t_aliexpress_service_division_analysis.objects.filter(id=qs.id).update(Handler_status=Handler_status)

    handlerstatus_modify.short_description = u'完成处理'
