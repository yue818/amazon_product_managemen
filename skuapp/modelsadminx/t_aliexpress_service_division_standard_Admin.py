class t_aliexpress_service_division_standard_Admin(object):
    list_display = ['Check_level', 'Primary_category', 'Second_category', 'Third_category', 'Fourth_category',
                    'DSR_description', 'Disputes_rate', 'DSR_increase', 'Dis_decrease','Importdatetime']
    search_list = ['Primary_category', 'Second_category', 'Third_category', 'Fourth_category',]
    list_filter = ['Primary_category']
    list_editable = ['DSR_description', 'Disputes_rate', 'DSR_increase', 'Dis_decrease',]