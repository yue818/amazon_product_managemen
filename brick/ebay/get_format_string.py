# coding=utf-8

from brick.function.get_time_stamp import get_time_stamp


def get_format_string(param):
    """
    处理表格中字符串或者数字
    :param param: 表格内容
    :return: 处理后的表格内容
    """
    result = param
    try:
        if isinstance(param, float):
            rt = str(param)
            if rt.split('.')[-1] == '0':
                result = rt.split('.')[0]
        else:
            if "'" in result:
                result = result.replace("'", "`")
    except Exception, e:
        print '%s' % get_time_stamp(), e
    return result