# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: 20181112.py
 @time: 2018/11/12 11:15
"""  
h = u'<br><a onclick="enable_id_%s(\'%s\')"title="对整个listing做上架操作">上架</a>' % (111, 2222,) + \
                   u"<script>function enable_id_%s(listingid) {to_lock(1);layer.confirm(listingid + '  请问确定要进行上架吗？'," \
                   u"{btn: ['确定','算了'],btn1:function(){static_refresh('/syndata_by_wish_api/?enable='+listingid)},end:function(){to_lock(0);}});}" \
                   u"</script>" % 111

print h