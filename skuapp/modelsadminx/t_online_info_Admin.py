# -*- coding: utf-8 -*-
from Project.settings import *
from django.utils.safestring import mark_safe
class t_online_info_Admin(object):
    actions =  ['to_undercarriage','to_grounding']
    def modify_Inventory_Quantity(self, request, queryset,vQuantity):

        ShopNameSets = set(queryset.all().values_list('ShopName'))
        for ShopNameSet_i, ShopNameSet_v in enumerate(ShopNameSets):
            doc = Document()  #创建DOM文档对象
            AmazonEnvelope = doc.createElement('AmazonEnvelope') #创建根元素
            AmazonEnvelope.setAttribute('xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance")#设置命名空间
            AmazonEnvelope.setAttribute('xsi:noNamespaceSchemaLocation','amzn-envelope.xsd')#引用本地XML Schema
            doc.appendChild(AmazonEnvelope)

            #Header
            Header = doc.createElement('Header')
            DocumentVersion = doc.createElement('DocumentVersion')
            MerchantIdentifier = doc.createElement('MerchantIdentifier')
            DocumentVersion_text = doc.createTextNode('1.02')
            MerchantIdentifier_text  = doc.createTextNode('%s'%ShopNameSet_v)
            DocumentVersion.appendChild(DocumentVersion_text)
            MerchantIdentifier.appendChild(MerchantIdentifier_text)
            Header.appendChild(DocumentVersion)
            Header.appendChild(MerchantIdentifier)
            AmazonEnvelope.appendChild(Header)

            #MessageType
            MessageType = doc.createElement('MessageType')
            MessageType_text = doc.createTextNode('Inventory')
            MessageType.appendChild(MessageType_text)
            AmazonEnvelope.appendChild(MessageType)
            for MessageID_i, querysetid in enumerate(queryset.filter(ShopName='%s'%ShopNameSet_v)):
                #Message
                Message = doc.createElement('Message')
                MessageID = doc.createElement('MessageID')
                MessageID_text = doc.createTextNode('%s'%(MessageID_i+1))
                MessageID.appendChild(MessageID_text)
                Message.appendChild(MessageID)

                OperationType = doc.createElement('OperationType')
                OperationType_text = doc.createTextNode('Update')
                OperationType.appendChild(OperationType_text)
                Message.appendChild(OperationType)

                Inventory = doc.createElement('Inventory')
                SKU = doc.createElement('SKU')
                Quantity = doc.createElement('Quantity')
                SKU_text = doc.createTextNode(querysetid.ShopSKU)#('ESLI0402')
                Quantity_text  = doc.createTextNode('%s'%vQuantity)
                SKU.appendChild(SKU_text)
                Quantity.appendChild(Quantity_text)
                Inventory.appendChild(SKU)
                Inventory.appendChild(Quantity)
                Message.appendChild(Inventory)
                AmazonEnvelope.appendChild(Message)
            feed =  doc.toxml()

            t_api_schedule_ing_obj = t_api_schedule_ing(ShopName='%s'%ShopNameSet_v,PlatformName='Amazon',CMDID='AmazonUpdateInventory',ScheduleTime=datetime.now(),
                                                        Status ='0',InsertTime=datetime.now(),UpdateTime= datetime.now(), Timedelta=180,RetryCount=0,Params=feed)
            t_api_schedule_ing_obj.save()


    def to_grounding(self, request, queryset):
        self.modify_Inventory_Quantity(request,queryset,'999')
    to_grounding.short_description = u'一键上架'

    def to_undercarriage(self, request, queryset):
        self.modify_Inventory_Quantity(request,queryset,'33')
    to_undercarriage.short_description = u'一键下架'

    def get_product_link(self,obj) :
        return mark_safe('<a href=https://www.amazon.com/dp/%s>%s</a>'%(obj.ProductID,obj.ProductID))
    get_product_link.short_description = u'产品信息'
    def show_pic(self,obj) :
        #picUrl = u'%s%s.%s/%s.jpg'%(PREFIX,BUCKETNAME_PY,ENDPOINT_OUT,obj.SKU)
        picUrl =  obj.Image
        rt =  '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  '%(picUrl,picUrl,picUrl)
        return mark_safe(rt)
    show_pic.short_description = u'图片'
    list_per_page=20
    list_display=('id','show_pic','PlatformName','ProductID','get_product_link','Title','SKU','ShopSKU','Price','Quantity','ReviewState','Status','OfWishes','OfSales','LastUpdated','DateUploaded','RefreshTime','ShopName','ShopIP',)

    list_filter = ('PlatformName','Price','Quantity','ReviewState','Status','LastUpdated','DateUploaded')

    search_fields = ('id','PlatformName','ProductID','Title','SKU','ShopSKU','Price','Quantity','ShopName','ShopIP')
    fields =  ('id',)
