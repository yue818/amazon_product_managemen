#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: set_val.py
 @time: 2018-02-26 15:23
"""
from django import template
import logging

register = template.Library()


class SetVarNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


class VarAddOneNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        try:
            value = template.Variable(self.var_name).resolve(context)
            context[self.var_name] = str(int(value) + 1)
        except template.VariableDoesNotExist:
            value = ""

        return ''


def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    logging.info('len(parts)=' + str(len(parts)))
    if len(parts) == 2:
        content = parts[1]
        if content[len(content) - 2:len(content)] == '++':
            var_name = content[:len(content) - 2]
            return VarAddOneNode(var_name)
        else:
            return u""
    elif len(parts) == 4:
        return SetVarNode(parts[1], parts[3])
    else:
        raise template.TemplateSyntaxError(u"'set' 标签必须是这种样式:  {% set <var_name>  = <var_value> %}")


register.tag('set', set_var)