# -*- coding: utf-8 -*-

import t_api_schedule_ing_wish_upload
# params  是一个字典
# result 也是一个字典
#单个product upload
def run(params):
    print 'billtest.py:%s'%params
    #TODO ....
    #def mainmain(objs,auth_info):
    resultstatus = ''
    errorinfo = ''
    bandlist = []
    try:
        if objs[3].strip() == 'UPLOAD' and objs[18].strip() != ''and objs[18] is not None:
            params = eval(objs[18])
            rt_add,bandlist1 = WISH_GOODS_UPLOAD_API(params['first'],auth_info['access_token'],objs[1])
            #rt_variant_add_status = []
            bandlist.append(bandlist1)
            rt_add_content = eval(rt_add._content)
            # print 'rt_add_content=%s'%rt_add_content
            if rt_add.status_code == 200 and rt_add_content['code'] == 0:
                if len(params['second']['product'])>=1:
                    # print 'Start the variant..........'
                    bandlist2 = WISH_VARIANT_GOODS_ADD_API(params['second'],auth_info['access_token'],objs[1])
                    bandlist = bandlist + bandlist2
                resultstatus = 'SUCCESS'
            else:
                resultstatus = 'DEFEAT'
                errorinfo = u'%s'%rt_add_content
    except Exception,ex:
        errorinfo = u'%s:%s'%(Exception,ex)
        resultstatus = 'DEFEAT'

    return [resultstatus,errorinfo,objs,bandlist]
    result =  {'errorcode':0,'errortext':'aaaaaaaaaaaaaaaaaaaa','params':params}
    return result


