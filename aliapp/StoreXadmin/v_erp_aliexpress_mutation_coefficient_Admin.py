

#-*-coding:utf-8-*-
class v_erp_aliexpress_mutation_coefficient_Admin(object):
    search_box_flag = True
    list_display_links = ('',)
    list_display=['product_id','sales','lastweek_sales','wow_sales','wow_rate','owner_member_id','shopName','cata_zh','submitter','week']
    mutation_coefficient_flag=True

    def get_list_queryset(self):
        request=self.request
        product_id=request.GET.get('product_id','')
        cata_zh=request.GET.get('category','')
        shopName=request.GET.get('shopname','')
        submitter=request.GET.get('submitter','')
        week=request.GET.get('week','')

        qs = super(v_erp_aliexpress_mutation_coefficient_Admin, self).get_list_queryset()
        if product_id:
            product_id_list=product_id.split(',')
        else:
            product_id_list=[]
        if submitter:
            submitter_list=submitter.split(',')
        else:
            submitter_list=[]
        if shopName:
            shopname_list = shopName.split(',')
        else:
            shopname_list = []
        searchList={'product_id__in':product_id_list,'week__exact':week,'submitter__in':submitter_list,'shopname__in':shopname_list,'cata_zh__exact':cata_zh}
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            # try:
            qs = qs.filter(**sl)
            # except Exception, ex:

        return qs