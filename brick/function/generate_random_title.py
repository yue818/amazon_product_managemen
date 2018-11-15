# coding=utf-8

"""
生成替换关键词后的新标题
"""

from random import randint, choice, shuffle
from django.db import connection

def get_coreWords_list():
    """核心关键词库"""
    coreWordsList = []

    cur = connection.cursor()
    sql = 'select CoreWords from t_product_corewords'

    cur.execute(sql)
    for each in cur.fetchall():
        coreWordsList.append(each[0])

    cur.close()
    return coreWordsList


def get_new_title(coreWordsList, coreWords, title):
    """生成新的标题和关键词"""
    coreWordsTempList = []
    cateList = [',', '|', '，']

    # 查找核心词里的分割方式，根据分割方式生成列表
    if coreWords is not None:
        for eachCate in cateList:
            if coreWords.encode('utf-8').find(eachCate) != -1:
                wordCate = eachCate
    try:
        coreWordsTempList = coreWords.split(wordCate)
    except:
        pass

    # 在title列表查询核心词是否存在，存在则暂时删除
    titleList = title.split(' ')
    for CoreWord in coreWordsTempList:
        if CoreWord in titleList:
            titleList.remove(CoreWord)

    # 在剔除核心词的tags和title列表随机替换三个词
    for i in range(3):
        titleList[randint(0, len(titleList) - 1)] = choice(coreWordsList)

    # 将替换之后的tags和title列表和核心词列表整合
    newTitleList = coreWordsTempList + titleList

    # 打乱列表顺序
    shuffle(newTitleList)
    newTitle = ' '.join(newTitleList)
    return newTitle