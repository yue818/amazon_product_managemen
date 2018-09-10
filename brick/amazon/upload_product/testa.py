# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: testa.py
 @time: 2018/8/3 13:58
"""
goods_upload_obj = dict()
goods_upload_obj['generic_keywords1'] = 'lehrer geschenk fnkdor stanzschablonen stanzschablonen scrapbook zubehör schablonen schablonen kinder stanzformen scrapbook papier scrapbook schablone schablone scrapbook stanzschablonen blumen stanzschablonen weihnachten stanzschablonen hochzeit'
if len(goods_upload_obj['generic_keywords1']) >= 199:
    key_word1 = goods_upload_obj['generic_keywords1'][0:130]
    key_word2 = goods_upload_obj['generic_keywords1'][130:]
    if ' ' in key_word2:
        keyword_temp = key_word2.split(' ')[0]
        if keyword_temp:
            key_word1 += keyword_temp
            key_word2 = key_word2.replace(keyword_temp + ' ', '')
        else:
            key_word2 = key_word2[1:]
else:
    key_word1 = goods_upload_obj['generic_keywords1']
    key_word2 = None

print len(key_word1)
print key_word1
print len(key_word2)
print key_word2