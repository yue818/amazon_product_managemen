# coding=utf-8
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages
from skuapp.table.t_Large_Small_Corresponding_Cate import t_Large_Small_Corresponding_Cate

class Large_Small_Plugin(BaseAdminPlugin):
    Large_Small_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.Large_Small_flag)

    def block_after_fieldsets(self, context, nodes):
        from skuapp.table.t_Large_Small_Corresponding_Cate import t_Large_Small_Corresponding_Cate
        from skuapp.table.t_product_build_ing import t_product_build_ing

        Large_objs = t_Large_Small_Corresponding_Cate.objects.values_list('LCode', 'LargeClass').distinct().order_by('LargeClass')
        Small_objs = t_Large_Small_Corresponding_Cate.objects.values_list('SCode', 'SmallClass').distinct().order_by('SmallClass')

        build_objs = self.model.objects.filter(id=context.get('object_id',None)).values('LargeCategory','SmallCategory')
        Large_look = ''
        Large_value = ''

        Small_look = ''
        Small_value = ''
        if build_objs.exists():
            for Large_obj in Large_objs:
                if Large_obj[0] == build_objs[0]['LargeCategory']:
                    Large_look = Large_obj[1]
                    Large_value = Large_obj[0]
            for Small_obj in Small_objs:
                if Small_obj[0] == build_objs[0]['SmallCategory']:
                    Small_look = Small_obj[1]
                    Small_value = Small_obj[0]
        nodes.append(loader.render_to_string('Large_Small_Html.html',
                                             {'Large_look': Large_look,'Large_value':Large_value,
                                              'Small_look':Small_look,'Small_value':Small_value}))



