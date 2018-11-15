from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext

class t_supply_chain_production_basic_plugin(BaseAdminPlugin):
    t_supply_chain_production_basic_flag=False

    def init_request(self, *args, **kwargs):
        return bool(self.t_supply_chain_production_basic_flag)

    def block_search_cata_nav(self, context, nodes):

        if self.model._meta.model_name == 't_work_flow_of_plate_house':
            nodes.append(loader.render_to_string('t_work_flow_of_plate_house_openmodel.html', {},context_instance=RequestContext(self.request)))
        else:
            nodes.append(loader.render_to_string('supply_chain_production_base.html',{}, context_instance=RequestContext(self.request)))
