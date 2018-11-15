# coding=utf-8


from django.db import connection


def select_from_collection_box():
    cur = connection.cursor()
    sql = 'select id, variants from t_templet_joom_collection_box WHERE cate is NULL ORDER BY id'
    cur.execute(sql)
    infos = cur.fetchall()
    cur.close()
    return infos


def select_from_b_goods(sku):
    cur = connection.cursor()
    sql = 'select CategoryCode from py_db.b_goods WHERE sku=\"%s\"; ' % sku.replace('\\', '\\\\')
    print 'sql-----%s' % sql
    cur.execute(sql)
    cate_info = cur.fetchone()
    cur.close()
    return cate_info


def update_collection_box(now_id, cate):
    cur = connection.cursor()
    sql = 'update t_templet_joom_collection_box set cate=%s WHERE id=%s'
    cur.execute(sql, (cate, now_id))
    cur.execute('commit;')
    cur.close()


def update_joom_goods_category():
    infos = select_from_collection_box()
    for info in infos:
        now_id = int(info[0])
        print '--------------%s' % now_id
        variants_str = info[1]
        if variants_str:
            variants_list = eval(variants_str)
            for variants in variants_list:
                variant = variants.get('Variant', '')
                sku = variant.get('productSKU', '')
                print 'productSKU---------%s' % sku
                if sku:
                    cate_info = select_from_b_goods(sku)
                    if cate_info:
                        cate_list = cate_info[0].split('|')
                        if len(cate_list) == 1:
                            continue
                        cate = cate_list[0] + '|' + cate_list[1] + '|'
                        print '-------------%s' % cate
                        update_collection_box(now_id, cate)
                        break