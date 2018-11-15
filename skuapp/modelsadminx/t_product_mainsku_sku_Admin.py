# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku
from skuapp.table.B_PackInfo import B_PackInfo
from skuapp.table.t_product_enter_ed import t_product_enter_ed
from skuapp.table.t_sys_param import t_sys_param
from skuapp.table.public import *
from django.db.models import Q

ProfitRate_obj=t_sys_param.objects.filter(Type=39,Seq=1)
ExchangeRate_obj=t_sys_param.objects.filter(Type=40,Seq=1)

class t_product_mainsku_sku_Admin(object):
    def show_cost(self,obj):
        B_packinfo_objs=B_PackInfo.objects.filter(id=obj.PackNID)
        costprice=0
        if B_packinfo_objs.exists():
            for B_packinfo_obj in B_packinfo_objs:
                costprice=float(B_packinfo_obj.CostPrice)+float(obj.UnitPrice)
        else:
            costprice=obj.UnitPrice
        return costprice    
    show_cost.short_description = u'总成本价(¥)'  
    
    def show_pack_cost(self,obj):
        B_packinfo_objs=B_PackInfo.objects.filter(id=obj.PackNID)
        packprice=0
        if B_packinfo_objs.exists():
            for B_packinfo_obj in B_packinfo_objs:
                packprice=float(B_packinfo_obj.CostPrice)
        return packprice    
    show_pack_cost.short_description = u'包装价(¥)'

    def show_pack_weight(self,obj):
        B_packinfo_objs=B_PackInfo.objects.filter(id=obj.PackNID)
        packweight=0
        if B_packinfo_objs.exists():
            for B_packinfo_obj in B_packinfo_objs:
                packweight=float(B_packinfo_obj.Weight)
        return packweight    
    show_pack_weight.short_description = u'包装重量(g)'
    
    def show_weight(self,obj):
        B_packinfo_objs=B_PackInfo.objects.filter(id=obj.PackNID)
        AllWeight=0
        if B_packinfo_objs.exists():
            for B_packinfo_obj in B_packinfo_objs:
                AllWeight=float(B_packinfo_obj.Weight)+float(obj.Weight)
        else:
            AllWeight=obj.Weight
        return AllWeight    
    show_weight.short_description = u'总重量(g)' 
    
    def show_sku(self,obj):
        return str(obj.MainSKU)+str(obj.SKU)
    show_sku.short_description=u'SKU'
    
    def show_image(self,obj):
        t_product_enter_ed_objs=t_product_enter_ed.objects.filter(id=obj.pid)
        rt=''
        if t_product_enter_ed_objs.exists():
            Image_url=t_product_enter_ed_objs[0].SourcePicPath
            rt =  '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  '%(Image_url,Image_url,Image_url)
        return mark_safe(rt)
    show_image.short_description = u'图片'
    
    
    def show_other_message(self,obj):
        rt = u'Wish<br>%s<br>%s'%(ProfitRate_obj[0].V,ExchangeRate_obj[0].V)
        return mark_safe(rt)
    show_other_message.short_description=mark_safe(u'计价平台<br>利润率(%)<br>美元汇率')
    
    def show_price_sj(self,obj):
        rt="<a id=show_price_sj_%s>实际价格换算</a><script>$('#show_price_sj_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'价格换算',fix:false,shadeClose: true,maxmin:true,area:['700px','700px'],content:'/t_product_mainsku_sku/show_price_sj//?PackNID=%s&ID=%s',});});</script>"%(obj.id,obj.id,obj.PackNID,obj.id)
        return mark_safe(rt)
    show_price_sj.short_description=u'操作'
    
    def show_product_price(self,obj):
        cost = obj.UnitPrice 
        weight=obj.Weight            
        Dollar = 0.0
        if 0<weight and weight<300:
            Dollar=(float(weight)*0.1*0.85+float(cost))*100/float(ExchangeRate_obj[0].V)/(1-float(ProfitRate_obj[0].V)/100-0.06-0.1)
        elif weight is not None:
            Dollar=((float(weight)*0.1+8)*0.8+float(cost))*100/float(ExchangeRate_obj[0].V)/(1-float(ProfitRate_obj[0].V)/100-0.06-0.1)
        return Dollar
    show_product_price.short_description = u'产品美元价($)'
    
    def show_price(self,obj):
        B_packinfo_objs=B_PackInfo.objects.filter(id=obj.PackNID)
        costprice=0
        if B_packinfo_objs.exists():
            for B_packinfo_obj in B_packinfo_objs:
                costprice=float(B_packinfo_obj.CostPrice)+float(obj.UnitPrice)
        elif obj.UnitPrice is not None:
            costprice=float(obj.UnitPrice)
        cost = costprice 
        B_packinfo_objs=B_PackInfo.objects.filter(id=obj.PackNID)
        AllWeight=0
        if B_packinfo_objs.exists():
            for B_packinfo_obj in B_packinfo_objs:
                AllWeight=float(B_packinfo_obj.Weight)+float(obj.Weight)
        elif obj.Weight is not None:
            AllWeight=obj.Weight
        weight=AllWeight            
        Dollar = 0.0
        if 0<weight and weight<300:
            Dollar=(float(weight)*0.1*0.85+float(cost))*100/float(ExchangeRate_obj[0].V)/(1-float(ProfitRate_obj[0].V)/100-0.06-0.1)
        elif weight is not None:
            Dollar=((float(weight)*0.1+8)*0.8+float(cost))*100/float(ExchangeRate_obj[0].V)/(1-float(ProfitRate_obj[0].V)/100-0.06-0.1)
        return Dollar
    show_price.short_description = u'总美元价($)'

    def show_cost_message(self,obj):
    #包装价
        B_packinfo_objs=B_PackInfo.objects.filter(id=obj.PackNID)
        packprice=0
        if B_packinfo_objs.exists():
            for B_packinfo_obj in B_packinfo_objs:
                packprice=float(B_packinfo_obj.CostPrice)
        
    #总成本价
        B_packinfo_objs=B_PackInfo.objects.filter(id=obj.PackNID)
        costprice=0
        if B_packinfo_objs.exists():
            for B_packinfo_obj in B_packinfo_objs:
                costprice=float(B_packinfo_obj.CostPrice)+float(obj.UnitPrice)
        else:
            costprice=obj.UnitPrice
            
        rt = u'%s<br>%s<br>%s<br>'%(obj.UnitPrice,packprice,costprice)
        return mark_safe(rt)
    show_cost_message.short_description=mark_safe(u'产品成本价(¥)<br>包装价(¥)<br>总成本价(¥)')
    
    def show_weight_message(self,obj):
    #包装重量
        B_packinfo_objs=B_PackInfo.objects.filter(id=obj.PackNID)
        packweight=0
        if B_packinfo_objs.exists():
            for B_packinfo_obj in B_packinfo_objs:
                packweight=float(B_packinfo_obj.Weight)
    
    #总重量
        B_packinfo_objs=B_PackInfo.objects.filter(id=obj.PackNID)
        AllWeight=0
        if B_packinfo_objs.exists():
            for B_packinfo_obj in B_packinfo_objs:
                AllWeight=float(B_packinfo_obj.Weight)+float(obj.Weight)
        else:
            AllWeight=obj.Weight
            
        rt = u'%s<br>%s<br>%s<br>'%(obj.Weight,packweight,AllWeight)
        return mark_safe(rt)
    show_weight_message.short_description=mark_safe(u'产品重量(g)<br>包装重量(g)<br>总重量(g)')
    
    def show_price_message(self,obj):
    #总美元价
        B_packinfo_objs=B_PackInfo.objects.filter(id=obj.PackNID)
        costprice=0
        if B_packinfo_objs.exists():
            for B_packinfo_obj in B_packinfo_objs:
                costprice=float(B_packinfo_obj.CostPrice)+float(obj.UnitPrice)
        elif obj.UnitPrice is not None:
            costprice=float(obj.UnitPrice)
        cost = costprice 
        B_packinfo_objs=B_PackInfo.objects.filter(id=obj.PackNID)
        AllWeight=0
        if B_packinfo_objs.exists():
            for B_packinfo_obj in B_packinfo_objs:
                AllWeight=float(B_packinfo_obj.Weight)+float(obj.Weight)
        elif obj.Weight is not None:
            AllWeight=obj.Weight
        weight=AllWeight            
        Dollar = 0.0
        if 0<weight and weight<300:
            Dollar=(float(weight)*0.1*0.85+float(cost))*100/float(ExchangeRate_obj[0].V)/(1-float(ProfitRate_obj[0].V)/100-0.06-0.1)
        elif weight is not None:
            Dollar=((float(weight)*0.1+8)*0.8+float(cost))*100/float(ExchangeRate_obj[0].V)/(1-float(ProfitRate_obj[0].V)/100-0.06-0.1)
    
    #产品美元价
        product_cost = obj.UnitPrice 
        product_weight=obj.Weight            
        product_Dollar = 0.0
        if 0<product_weight and product_weight<300:
            product_Dollar=(float(product_weight)*0.1*0.85+float(product_cost))*100/float(ExchangeRate_obj[0].V)/(1-float(ProfitRate_obj[0].V)/100-0.06-0.1)
        elif product_weight is not None:
            product_Dollar=((float(product_weight)*0.1+8)*0.8+float(product_cost))*100/float(ExchangeRate_obj[0].V)/(1-float(ProfitRate_obj[0].V)/100-0.06-0.1)
        
        rt = u'%s<br>%s'%(product_Dollar,Dollar)
        return mark_safe(rt)
    show_price_message.short_description=mark_safe(u'产品美元价($ 不含包装)<br>总美元价($ 包含包装)')
    
    list_display=('id','show_sku','show_image','show_cost_message','show_weight_message','show_other_message','show_price_message','show_price_sj')
    search_fields=('MainSKU','SKU') 

        #def get_queryset(self, request):
    def get_list_queryset(self):
        request = self.request
        return super(t_product_mainsku_sku_Admin, self).get_list_queryset().filter(~Q(SKU = ''),~Q(SKU = None))
        #return qs.filter(StaffID = request.user.username)