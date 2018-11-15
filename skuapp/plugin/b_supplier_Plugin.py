# coding=utf-8


from xadmin.views import BaseAdminPlugin
from django.template import loader
from pyapp.models import B_Supplier, b_supplier_category, B_Person
# from sqlapp.models import b_person as B_Person
import json
from pyapp.table.b_supplier_category_link_purchaser import b_supplier_category_link_purchaser


def get_supplier():
    supplier = []
    supplier_infos = B_Supplier.objects.filter().values_list('NID', 'SupplierName')
    for supplier_info in supplier_infos:
        temp_dict_1 = {'supplier_id': supplier_info[0], 'supplier': supplier_info[1]}
        supplier.append(temp_dict_1)
    return supplier

def get_person():
    """获取人员信息"""
    person = []
    person_infos = B_Person.objects.filter().values_list('NID', 'PersonName')
    for person_info in person_infos:
        temp_dict_2 = {'person_id': person_info[0], 'person': person_info[1]}
        person.append(temp_dict_2)
    return person


def get_purchaser():
    category_link_purchaser = {}
    objs = b_supplier_category_link_purchaser.objects.filter().values_list('CategoryID', 'Purchaser')
    for obj in objs:
        if category_link_purchaser.has_key(obj[0]):
            category_link_purchaser[obj[0]].append(obj[1])
        else:
            category_link_purchaser[obj[0]] = [obj[1]]
    return category_link_purchaser


def get_category():
    """获取供应商一级分类、二级分类"""
    first_category = {}
    second_category = {}
    cate_objs = b_supplier_category.objects.all()
    for cate_obj in cate_objs:
        first_category[cate_obj.FirstCategoryID] = cate_obj.FirstCategoryName
        if second_category.get(cate_obj.FirstCategoryID, ''):
            second_category[cate_obj.FirstCategoryID] = dict(
                second_category[cate_obj.FirstCategoryID], **{cate_obj.SecondCategoryID: cate_obj.SecondCategoryName}
            )
        else:
            if cate_obj.SecondCategoryID:
                second_category[cate_obj.FirstCategoryID] = {cate_obj.SecondCategoryID: cate_obj.SecondCategoryName}
            else:
                second_category[cate_obj.FirstCategoryID] = {}
    return first_category, second_category


class b_supplier_Plugin(BaseAdminPlugin):
    b_supplier_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.b_supplier_flag)


    def block_after_fieldsets(self, context, nodes):
        if self.request.get_full_path().find('/add') >= 0:
            user = self.request.user.first_name
            person_data = get_person()
            category_link_purchaser = get_purchaser()
            first_category, second_category = get_category()
            nodes.append(loader.render_to_string(
                'b_supplier_Plugin.html',
                {
                    'person_data': person_data, 'page': 'add', 'username': user,'first_category': first_category,
                    'second_category': json.dumps(second_category), 'first_category2': json.dumps(first_category),
                    'category_link_purchaser': json.dumps(category_link_purchaser)
                }
            ))


    def block_search_cata_nav(self, context, nodes):
        if self.request.get_full_path().find('/add') == -1:
            params = dict(self.request.GET.items())

            purchaser_id = params.get('purchaser', '')
            salername_id = params.get('salername', '')
            recorder_id = params.get('recorder', '')
            supplier_id = params.get('supplier', '')
            category1_id = params.get('category1', '')
            category2_id = params.get('category2', '')

            supplier_data = get_supplier()
            person_data = get_person()
            first_category, second_category = get_category()
            nodes.append(loader.render_to_string(
                'b_supplier_Plugin.html',
                {
                    'supplier_data': json.dumps(supplier_data), 'person_data': json.dumps(person_data),
                    'first_category': json.dumps(first_category), 'second_category': json.dumps(second_category),
                    'purchaser_id': purchaser_id, 'salername_id': salername_id, 'recorder_id': recorder_id,
                    'supplier_id': supplier_id, 'category1_id': category1_id, 'category2_id': category2_id
                }
            ))