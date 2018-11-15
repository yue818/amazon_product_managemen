# -*- coding: utf-8 -*-
class t_helpAdmin(object):

    list_display   =('StepID','Stepdescription','HelpContent')
    list_editable  = ('StepID','Stepdescription','HelpContent')
    search_fields   =('StepID','Stepdescription','HelpContent')
    list_filter   =('StepID','Stepdescription','HelpContent')
    #readonly_fields =('StepID','Stepdescription','HelpContent')
    list_display_links = ('id',)