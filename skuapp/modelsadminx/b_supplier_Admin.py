# -*- coding: utf-8 -*-


from .t_product_Admin import *
from django.utils.safestring import mark_safe
from django.contrib import messages
from pyapp.models import B_Supplier, B_Person, B_SupplierCats
from brick.pydata.py_syn.public import public
from pyapp.table.b_supplier_purchaser_relationship import b_supplier_purchaser_relationship
from datetime import datetime
import re



class b_supplier_Admin(object):
    # downloadxls = True
    b_supplier_flag = True

    readonly = u'readonly="true"'
    disabled = u'disabled="disabled"'


    def show_used(self, obj):
        if obj.Used == '1':
            rr = u'checked="checked"'
        else:
            rr = u''
        rt = u"""<input type="checkbox" onchange="modify_supplier(this, 'Used_%s')" %s %s />""" % (obj.NID, rr, self.disabled)
        return mark_safe(rt)
    show_used.short_description = u'<span style="color: #428bca">停用</span>'


    def show_category(self, obj):
        cate_1 = obj.CategoryID
        cate_2 = obj.CategoryID2

        cate_1_obj = B_SupplierCats.objects.filter(NID=cate_1)
        cate_2_obj = B_SupplierCats.objects.filter(NID=cate_2)

        cate_1_name = ''
        if cate_1_obj.exists():
            cate_1_name = cate_1_obj[0].CategoryName
        cate_2_name = ''
        if cate_2_obj.exists():
            cate_2_name = cate_2_obj[0].CategoryName

        rt1 = u"""<select id="CategoryID_%s" class="s1" onfocus="cate_onfocus('CategoryID', '%s')" %s>
                    <option value="%s">%s</option></select>""" % (obj.NID, obj.NID, self.disabled, cate_1, cate_1_name)
        rt2 = u"""<select id="CategoryID2_%s" class="s1" onfocus="cate_onfocus('CategoryID2', '%s')" onchange="modify_supplier(this, 'CategoryID_%s')" %s>
                    <option value="%s">%s</option></select>""" % (obj.NID, obj.NID, obj.NID, self.disabled, cate_2, cate_2_name)

        rt = u'<table><tr><th class="th1">一级分类</th><th class="th2">%s</th></tr>' \
             u'<tr><th class="th1">二级分类</th><th class="th2">%s</th></tr>' \
             u'<tr><th class="th1"><span style="color:red">注:</span></th>' \
             u'<th class="th2"><span style="color:red">修改二级分类后系统保存</span></th></tr></table>' % (rt1, rt2)

        return mark_safe(rt)
    show_category.short_description = u'<span style="color: #428bca">一级分类/二级分类</span>'


    def show_name(self, obj):
        try:
            url = obj.URL if obj.URL else ''
            name = obj.SupplierName if obj.SupplierName else ''
            rt = u'<a href="%s" target="_blank" id="supplier_url_%s">%s</a>' % (url, obj.NID, name)

            name_html = u"""<input type="text" onchange="modify_supplier(this, 'SupplierName_%s')" value="%s"
                            class="p_input" id="SupplierName_%s" %s />""" % (obj.NID, name, obj.NID, self.readonly)
            url_html = u"""<input type="text" onchange="modify_supplier(this, 'URL_%s')" value="%s"
                            class="p_input" id="URL_%s" %s />""" % (obj.NID, url, obj.NID, self.readonly)

            rt = u'%s<br><br><table><tr><th class="th1">供应商名称</th><th class="th2">%s</th></tr>' \
                 u'<tr><th class="th1">供应商网址</th><th class="th2">%s</th></tr></table>' % (rt, name_html, url_html)
        except:
            rt = u'<a href="%s" target="_blank">%s</a>' % (obj.URL, obj.SupplierName)
        return mark_safe(rt)
    show_name.short_description = u'<span style="color: #428bca">供应商</span>'


    def show_contact_info(self, obj):
        try:
            link_man = obj.LinkMan if obj.LinkMan else ''
            office_phone = obj.OfficePhone.replace(u'固话：', '') if obj.OfficePhone else ''
            mobile = obj.Mobile.replace(u'手机号码：', '') if obj.Mobile else ''
            tbww = obj.MSN if obj.MSN else ''

            link_man_html = u"""<input type="text" onchange="modify_supplier(this, 'LinkMan_%s')" value="%s"
                                class="p_input" id="LinkMan_%s" %s />""" % (obj.NID, link_man, obj.NID, self.readonly)
            office_phone_html = u"""<input type="text" onchange="modify_supplier(this, 'OfficePhone_%s')" value="%s"
                                    class="p_input" id="OfficePhone_%s" %s />""" % (obj.NID, office_phone, obj.NID, self.readonly)
            mobile_html = u"""<input type="text" onchange="modify_supplier(this, 'Mobile_%s')" value="%s"
                                class="p_input" id="Mobile_%s" %s />""" % (obj.NID, mobile, obj.NID, self.readonly)
            tbww_html = u"""<input type="text" onchange="modify_supplier(this, 'MSN_%s')" value="%s"
                            class="p_input" id="MSN_%s" %s />""" % (obj.NID, tbww, obj.NID, self.readonly)

            rt = u'<table><tr><th class="th1">联系人</th><th class="th2">%s</th></tr>' \
                 u'<tr><th class="th1">办公电话</th><th class="th2">%s</th></tr>' \
                 u'<tr><th class="th1">联系方式</th><th class="th2">%s</th></tr>' \
                 u'<tr><th class="th1">淘宝旺旺</th><th class="th2">%s</th></tr></table>' % \
                 (link_man_html, office_phone_html, mobile_html, tbww_html)
        except:
            rt = u'联系人: %s<br>办公电话: %s<br>联系方式: %s<br>旺旺: %s' % (obj.LinkMan, obj.OfficePhone, obj.Mobile, obj.MSN)
        return mark_safe(rt)
    show_contact_info.short_description = u'<span style="color: #428bca">联系信息</span>'


    def show_address(self, obj):
        address = obj.Address if obj.Address else ''
        rt = u"""<textarea style="overflow:hidden;width:150px;height:100px"
        onchange="modify_supplier(this, 'Address_%s')" id="Address_%s" %s >%s</textarea>""" % (obj.NID, obj.NID, self.readonly, address)
        return mark_safe(rt)
    show_address.short_description = u'<span style="color: #428bca">地址</span>'


    def show_purchaser(self, obj):
        possessman2 = obj.PossessMan2 if obj.PossessMan2 else u'工号：'
        possessman2_html = u"""<input type="text" onchange="modify_supplier(this, 'PossessMan2_%s')" value="%s"
                                    class="p_input" style="width: 100px" id="PossessMan2_%s" %s />""" % (
        obj.NID, possessman2, obj.NID, self.readonly)
        rt = u'<table><tr><th class="th1">责任归属人2</th><th class="th2">%s</th></tr></table>' % possessman2_html

        if self.readonly:
            rt = u'%s<br><br>%s' % (obj.SupPurchaser, rt)
        else:
            rt = u"%s &nbsp;&nbsp;<a id=purchaser_%s>[修改采购]</a><script>$('#purchaser_%s').on('click',function(){" \
                 u"layer.open({type:2,skin:'layui-layer-lan',title:'修改采购',fix:false,shadeClose: true," \
                 u"maxmin:true,area:['800px','600px'],content:'/modify_purchaser/?nid=%s&action=search&supplier=%s'," \
                 u"end:function(){location.reload();}});});;</script><br><br>%s" % (obj.SupPurchaser, obj.NID, obj.NID, obj.NID, obj.SupplierName, rt)

            # purchaser_html = u"""<select id="SupPurchaser_%s" calss="s1" onfocus="purchaser_onfocus('SupPurchaser_%s')" ><option value="---">---</option></select>""" % (obj.NID, obj.NID)
            # cloth_html = u"""<select id="Cloth_%s" class="s1"><option value="---">---</option><option value="0">服装</option><option value="1">非服装</option></select>""" % obj.NID
            #
            # rt = u'%s<br><br><table><tr><th class="th1">是否服装</th><th class="th2">%s</th></tr>' \
            #      u'<tr><th class="th1">新采购员</th><th class="th2">%s</th></tr></table>' % (r1, cloth_html, purchaser_html)
        return mark_safe(rt)
    show_purchaser.short_description = u'<span style="color: #428bca">采购员/责任归属人2</span>'


    def show_create(self, obj):
        recorder = obj.Recorder if obj.Recorder else ''
        create_date = str(obj.CreateDate)[:10] if obj.CreateDate else ''
        rt = u'创建人: %s<br><br>创建日期: %s' % (recorder, create_date)
        return mark_safe(rt)
    show_create.short_description = u'<span style="color: #428bca">创建信息</span>'


    def show_memo(self, obj):
        memo = obj.Memo if obj.Memo else ''
        rt = u"""<textarea style="overflow:hidden;width:150px;height:100px"
        onchange="modify_supplier(this, 'Memo_%s')" id="Memo_%s" %s >%s</textarea>""" % (obj.NID, obj.NID, self.readonly, memo)
        return mark_safe(rt)
    show_memo.short_description = u'<span style="color: #428bca">备注</span>'


    list_display = (
        'NID', 'show_name', 'show_category', 'show_contact_info', 'show_address', 'show_memo',
        'show_purchaser', 'show_used', 'supplierLoginId', 'show_create', 'IsBlacklist'
    )
    list_editable = ['IsBlacklist']
    list_display_links = ('',)
    fields = (
        'Used', 'SupplierName', 'LinkMan', 'OfficePhone', 'Mobile', 'Address', 'URL', 'MSN', 'supplierLoginId', 'Memo',
        'Email', 'Account', 'FitCode', 'paytype', 'QQ', 'ArrivalDays', 'SupplierLevel', 'IsClothing'
    )
    form_layout = (
        Fieldset(u'供应商信息(*为必填项)',
                 Row('SupplierName', 'LinkMan'),
                 Row('Mobile', 'MSN'),
                 Row('supplierLoginId', 'URL'),
                 Row('Address', 'IsClothing'),
                 Row('Account', 'FitCode'),
                 Row('OfficePhone', 'ArrivalDays'),
                 Row('QQ', 'Email'),
                 Row('SupplierLevel', 'Used'),
                 Row('paytype'),
                 Row('Memo'),
                 css_class='unsort '
                 ),
    )
    list_per_page = 30
    actions = ['to_b_supplier_excel', ]

    def to_b_supplier_excel(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        # if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet(u'供应商信息')

        sheet.write(0, 0, u'所属类别')
        sheet.write(0, 1, u'编码')
        sheet.write(0, 2, u'停用')
        sheet.write(0, 3, u'名称')
        sheet.write(0, 4, u'简拼')
        sheet.write(0, 5, u'联系人')
        sheet.write(0, 6, u'办公电话')
        sheet.write(0, 7, u'手机')
        sheet.write(0, 8, u'地址')
        sheet.write(0, 9, u'公司账号')
        sheet.write(0, 10, u'网址')
        sheet.write(0, 11, u'QQ/MSN')
        sheet.write(0, 12, u'淘宝旺旺')
        sheet.write(0, 13, u'邮箱')
        sheet.write(0, 14, u'到货天数')
        sheet.write(0, 15, u'备注')

        # 写数据
        row = 0
        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row, column, qs.CategoryID)

            column = column + 1
            sheet.write(row, column, qs.SupplierCode)

            column = column + 1
            sheet.write(row, column, qs.Used)

            column = column + 1
            sheet.write(row, column, qs.SupplierName)

            column = column + 1
            sheet.write(row, column, qs.FitCode)

            column = column + 1
            sheet.write(row, column, qs.LinkMan)

            column = column + 1
            sheet.write(row, column, qs.OfficePhone)

            column = column + 1
            sheet.write(row, column, qs.Mobile)

            column = column + 1
            sheet.write(row, column, qs.Address)

            column = column + 1
            sheet.write(row, column, qs.Account)

            column = column + 1
            sheet.write(row, column, qs.URL)

            column = column + 1
            sheet.write(row, column, u'%s/%s' % (qs.QQ, qs.MSN))

            column = column + 1
            # sheet.write(row,column,qs.)

            column = column + 1
            sheet.write(row, column, qs.Email)

            column = column + 1
            sheet.write(row, column, qs.ArrivalDays)

            column = column + 1
            sheet.write(row, column, qs.Memo)

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket, prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))

        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username, filename) + u':成功导出,可点击Download下载到本地............................。')
    to_b_supplier_excel.short_description = u'导出供应商信息'

    def save_models(self):
        post = self.request.POST

        InputDate = CreateDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Recorder = self.request.user.first_name
        SupplierName = post.get('SupplierName', '')
        if not B_Supplier.objects.filter(SupplierName=SupplierName.strip()).exists():
            LinkMan = post.get('LinkMan', None)
            Mobile = post.get('Mobile', None)
            MSN = post.get('MSN', None)
            URL = post.get('URL', None)
            Address = post.get('Address', None)
            FitCode = post.get('FitCode', None)
            SupplierCode = post.get('SupplierCode', None)
            Account = post.get('Account', None)
            supplierLoginId = post.get('supplierLoginId', None)
            OfficePhone = post.get('OfficePhone', None)
            ArrivalDays = post.get('ArrivalDays', None)
            QQ = post.get('QQ', None)
            Email = post.get('Email', None)
            SupplierLevel = post.get('SupplierLevel', None)
            Used = post.get('Used', None)
            paytype = post.get('paytype', None)
            Memo = post.get('Memo', None)
            CategoryID = post.get('CategoryID', None)
            CategoryID2 = post.get('CategoryID2', None)
            SupPurchaser = post.get('SupPurchaser', None)
            SalerNameNew = post.get('SalerNameNew', None)
            IsClothing = post.get('IsClothing', None)
            other = post.get('other', '')
            PossessMan2 = post.get('PossessMan2', '')
            possessman_number = re.findall('(\d+)', PossessMan2)
            if possessman_number:
                PossessMan2 = u'工号：' + possessman_number[0]
            else:
                PossessMan2 = ''
            if supplierLoginId == '其它':
                if other == '':
                    messages.error(self.request, u'供应商来源选择 "其它" 时, 请手动填写！！！')
                else:
                    supplierLoginId = other

            Used = Used if Used else 0
            ArrivalDays = ArrivalDays if ArrivalDays else None
            SupplierLevel = SupplierLevel if SupplierLevel else None

            try:
                if ( not CategoryID ) or ( not CategoryID2 ) or ( not SupPurchaser ):
                    messages.error(self.request, u'一级分类、二级分类、采购人不能为空！！！')
                else:
                    # 生成供应商Code
                    if not SupplierCode:
                        b_objs = B_Supplier.objects.filter().values_list('SupplierCode', 'NID').order_by('-NID').first()
                        pre_SupplierCode = b_objs[0]
                        nid = b_objs[1]
                        if pre_SupplierCode:
                            code_list = re.findall('(\d+)', pre_SupplierCode)
                        else:
                            code_list = []
                        if code_list:
                            SupplierCode = int(code_list[0]) + 1
                        else:
                            SupplierCode = int(nid) + 1

                    supplier_info = {
                        'CategoryID': CategoryID2, 'SupplierCode': SupplierCode, 'SupplierName': SupplierName,
                        'FitCode': FitCode, 'LinkMan': LinkMan, 'Address': Address, 'OfficePhone': OfficePhone,
                        'Mobile': Mobile, 'Used': Used if Used else 0, 'Recorder': Recorder, 'InputDate': InputDate,
                        'Modifier': None, 'ModifyDate': None, 'Email': Email, 'QQ': QQ, 'MSN': MSN,
                        'ArrivalDays': ArrivalDays if ArrivalDays else 0, 'URL': URL, 'Memo': Memo, 'Account': Account,
                        'CreateDate': CreateDate, 'SupPurchaser': SupPurchaser, 'supplierLoginId': supplierLoginId,
                        'paytype': paytype, 'SalerNameNew': SalerNameNew
                    }

                    public_obj = public()
                    result = public_obj.syn_supplier_info(supplier_info)
                    if result['error_code'] != 0:
                        messages.error(self.request, result['error_info'])
                    else:
                        obj = self.model(
                            SupplierName=SupplierName, LinkMan=LinkMan, Mobile=Mobile, MSN=MSN, URL=URL,
                            Address=Address, FitCode=FitCode, SupplierCode=SupplierCode, Account=Account, Used=Used,
                            OfficePhone=OfficePhone, supplierLoginId=supplierLoginId, QQ=QQ, Email=Email,
                            paytype=paytype, ArrivalDays=ArrivalDays, Memo=Memo, CategoryID=CategoryID,
                            CategoryID2=CategoryID2, SupPurchaser=SupPurchaser, SalerNameNew=SalerNameNew,
                            SupplierLevel=SupplierLevel, PossessMan2=PossessMan2, InputDate=InputDate,
                            CreateDate=CreateDate, Recorder=Recorder, NID=result['return_id'], IsBlacklist=0
                        )
                        obj.save()

                        B_Person_obj = B_Person.objects.filter(PersonName=SupPurchaser)
                        if IsClothing == '2':
                            b_supplier_purchaser_relationship.objects.create(
                                SupplierID=int(obj.NID), PurchaserID=B_Person_obj[0].NID, EffectiveTime=InputDate,
                                Category=1, ModifyName=Recorder, ModifyTime=InputDate)
                            b_supplier_purchaser_relationship.objects.create(
                                SupplierID=int(obj.NID), PurchaserID=B_Person_obj[0].NID, EffectiveTime=InputDate,
                                Category=0, ModifyName=Recorder, ModifyTime=InputDate)
                        else:
                            b_supplier_purchaser_relationship.objects.create(
                                SupplierID=int(obj.NID), PurchaserID=B_Person_obj[0].NID, EffectiveTime=InputDate,
                                Category=IsClothing,  ModifyName=Recorder, ModifyTime=InputDate)
            except Exception, e :
                messages.error(self.request, u'保存时出错:  %s' % e)
        else:
            messages.error(self.request, u'供应商: "%s" 已存在' % SupplierName)


    def get_list_queryset(self):
        qs = super(b_supplier_Admin, self).get_list_queryset()

        if (self.request.user.username in ['zhouchunyan', 'chenbinbin']) or (self.request.user.is_superuser):
            self.readonly = u''
            self.disabled = u''

        request = self.request.GET
        purchaser = request.get('purchaser', '')
        salername = request.get('salername', '')
        recorder = request.get('recorder', '')
        supplier_id = request.get('supplier', '')
        category1_id = request.get('category1', '')
        category2_id = request.get('category2', '')

        searchList = {
            'SupPurchaser__contains': purchaser, 'SalerNameNew__exact': salername, 'Recorder__exact': recorder,
            'NID__exact': supplier_id, 'CategoryID__exact': category1_id, 'CategoryID2__exact': category2_id
        }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'Seller__exact':
                        v = '' if v == u'无' else v
                    if k == 'ShopName__exact':
                        if v.find('Wish-') == -1:
                            v = 'Wish-' + v.zfill(4)
                    sl[k] = v
        if sl:
            qs = qs.filter(**sl)
        return qs