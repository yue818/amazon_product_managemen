# coding=utf-8
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages

class Three_Grade_Classification_Of_Clothing_Plugin(BaseAdminPlugin):
    Three_Class_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.Three_Class_flag)

    def block_after_fieldsets(self, context, nodes):
        from skuapp.table.t_Three_Grade_Classification_Of_Clothing import t_Three_Grade_Classification_Of_Clothing
        from skuapp.table.t_product_develop_ing import t_product_develop_ing

        one = ''
        two = ''
        three = ''
        develop_objs = self.model.objects.filter(id=context.get('object_id',None)).values('ClothingSystem1','ClothingSystem2','ClothingSystem3')
        if develop_objs.exists():
            one = develop_objs[0]['ClothingSystem1']
            two = develop_objs[0]['ClothingSystem2']
            three = develop_objs[0]['ClothingSystem3']
        nodes.append(loader.render_to_string('Three_Grade_Classification_Of_Clothing.html',
                                             {'one':one,'two':two,'three':three}))



