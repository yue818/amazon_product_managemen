# -*- coding: utf-8 -*-
from .t_product_Admin import *
#16)    已录入商品信息 v_product_enter_ed
class v_product_enter_ed_Admin(t_product_Admin):
    actions = ['to_copy']
    def to_copy(self, request, queryset): #
        for querysetid in queryset.all():


            obj = t_product_build_ing()
            obj.__dict__ = querysetid.__dict__
            obj.id = self.get_id()
            obj.MainSKU = ''
            obj.CreateTime = datetime.now()
            obj.CreateStaffName = request.user.first_name
            obj.StaffID= request.user.username
            obj.save()

        messages.success(request, u'复制成果！您复制的产品已发送到‘建资料’步骤。')
    to_copy.short_description = u'复制-该款产品'

    def show_SourcePicPath(self,obj) :
        #return '<img src="{}"  width="100" height="100"  alt = "{}"  title="{}"  />  '
        rt =  '<img src="%s"  width="80" height="80"  alt = "%s"  title="%s"  />  '%(obj.SourcePicPath,obj.SourcePicPath,obj.SourcePicPath)
        return mark_safe(rt)

    show_SourcePicPath.short_description = u'调研图'

    def show_SourcePicPath2(self,obj) :
        #return '<img src="{}"  width="100" height="100"  alt = "{}"  title="{}"  />  '
        rt =  '<img src="%s"  width="80" height="80"  alt = "%s"  title="%s"  />  '%(obj.SourcePicPath2,obj.SourcePicPath2,obj.SourcePicPath2)
        return mark_safe(rt)
    show_SourcePicPath2.short_description = u'供货商图'
    def show_oplog(self,obj) :
        rt = ''
        t_product_oplog_objs = t_product_oplog.objects.filter(pid=obj.id).order_by('id')
        for t_product_oplog_obj in t_product_oplog_objs:
            rt = u'%s%s:%s,'%(rt,t_product_oplog_obj.StepName,t_product_oplog_obj.OpName)
        return rt
    show_oplog.short_description = u'操作历史'

    def show_urls(self,obj) :
        rt = ''
        t_product_enter_ed_objs = t_product_enter_ed.objects.filter(id=obj.id)
        for t_product_enter_ed_obj in t_product_enter_ed_objs:
            rt = u'%s反向: %s<br>供货商: %s,'%(rt,t_product_enter_ed_obj.SourceURL,t_product_enter_ed_obj.SupplierPUrl1)
        return mark_safe(rt)
    show_urls.short_description = u'链接信息'




    #list_display= ('id','T','CreateTime','CreateStaffName','SourcePicPath2','MainSKU','show_skulist','UpdateTime','StaffID','Name2','fromT','show_oplog',)
    list_display= ('id','DYTime','DYStaffName','JZLTime','JZLStaffName','show_SourcePicPath','show_SourcePicPath2','MainSKU','show_skulist','Name2','Keywords','Keywords2','Pricerange','SupplierPDes','SpecialSell','SpecialRemark','show_urls',)
    list_per_page=50



# 分组表单
    fields = ('SourceURL','OrdersLast7Days','Keywords','Keywords2','SpecialRemark',
              'Pricerange','ShelveDay','Name','Tags', #u'调研结果',
              'SupplierPUrl1','SupplierPDes','SupplierID', # u'开发结果',
              'UnitPrice','Weight','SpecialSell', #u'询价结果',
              'Name2','Material','Unit','MinOrder','SupplierArtNO',
              'SupplierPColor','SupplierPUrl2','OrderDays','StockAlarmDays','LWH',
              'SupplierContact','Storehouse','ReportName','ReportName2','MinPackNum',#建资料
              'Electrification','Powder','Liquid','Magnetism',  #u'违禁品',
              'Remark', #备注
              'MainSKU', #主SKU
              'DYTime','DYStaffName','DYSHTime','DYSHStaffName','XJTime','XJStaffName','KFTime','KFStaffName','JZLTime','JZLStaffName',
              'PZTime','PZStaffName','MGTime','MGStaffName','LRTime','LRStaffName'
              )

    form_layout = (
        Fieldset(u'调研结果',
                    Row('SourceURL','OrdersLast7Days','Pricerange'),
                    Row('Keywords','Keywords2','Tags'),
                    Row('ShelveDay','Name','SpecialRemark'),
                    css_class = 'unsort '
                ),
        Fieldset(u'开发&询价',
                    Row('SupplierPUrl1','SupplierPDes','SupplierID'),
                    Row('UnitPrice','Weight','SpecialSell'),
                    css_class = 'unsort  '
                ),
        Fieldset(u'建资料',
                    Row('Name2','Material','Unit'),
                    Row('MinOrder','SupplierArtNO', 'SupplierPColor'),
                    Row('SupplierPUrl2','OrderDays','StockAlarmDays'),
                    Row('LWH', 'SupplierContact','Storehouse'),
                    Row('ReportName','ReportName2','MinPackNum'),
                    css_class = 'unsort '
                ),
        Fieldset(u'违禁品',
                    Row('Electrification','Powder','Liquid','Magnetism'),
                    css_class = 'unsort '
                ),
        Fieldset(u'备注信息',
                    Row('Remark'),
                    css_class = 'unsort '
                ),
        Fieldset(u'主SKU信息',
                    Row('MainSKU'),
                    css_class = 'unsort '
                ),

                  )
    show_detail_fields = ['id']

    logger = logging.getLogger('sourceDns.webdns.views')