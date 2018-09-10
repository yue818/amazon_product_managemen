#-*-coding:utf-8-*-


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_published_variation.py
 @time: 2018/2/13 9:12
"""   
class t_templet_amazon_published_variation():
    def __init__(self, db_cnxn=None):
        self.cnxn = db_cnxn

    def get_variation_info_by_publish_goods(self, params):
        shocur = self.cnxn.cursor()
        shocur.execute("select relationship_type,variation_theme,parent_sku,child_sku,price,main_image_url,"
                       "other_image_url1,other_image_url2,other_image_url3,other_image_url4,other_image_url5,"
                       "other_image_url6,other_image_url7,other_image_url8,parent_item_sku,productSKU,parent_child,"
                       "color_name,MetalType,color_map,size_name,size_map,external_product_id,item_quantity "
                       "from t_templet_amazon_published_variation  where parent_item_sku = %s and "
                       "prodcut_variation_id = %s ;",(params['parent_item_sku'],params['prodcut_variation_id']))
        t_templet_amazon_published_variation_objs = shocur.fetchall()
        t_templet_amazon_published_variations = []
        for t_templet_amazon_published_variation_obj in t_templet_amazon_published_variation_objs:
            if t_templet_amazon_published_variation_obj:
                t_templet_amazon_published_variation = {}
                t_templet_amazon_published_variation['relationship_type'] = t_templet_amazon_published_variation_obj[0]
                t_templet_amazon_published_variation['variation_theme'] = t_templet_amazon_published_variation_obj[1]
                t_templet_amazon_published_variation['parent_sku'] = t_templet_amazon_published_variation_obj[2]
                t_templet_amazon_published_variation['child_sku'] = t_templet_amazon_published_variation_obj[3]
                t_templet_amazon_published_variation['price'] = t_templet_amazon_published_variation_obj[4]
                t_templet_amazon_published_variation['main_image_url'] = t_templet_amazon_published_variation_obj[5]
                t_templet_amazon_published_variation['other_image_url1'] = t_templet_amazon_published_variation_obj[6]
                t_templet_amazon_published_variation['other_image_url2'] = t_templet_amazon_published_variation_obj[7]
                t_templet_amazon_published_variation['other_image_url3'] = t_templet_amazon_published_variation_obj[8]
                t_templet_amazon_published_variation['other_image_url4'] = t_templet_amazon_published_variation_obj[9]
                t_templet_amazon_published_variation['other_image_url5'] = t_templet_amazon_published_variation_obj[10]
                t_templet_amazon_published_variation['other_image_url6'] = t_templet_amazon_published_variation_obj[11]
                t_templet_amazon_published_variation['other_image_url7'] = t_templet_amazon_published_variation_obj[12]
                t_templet_amazon_published_variation['other_image_url8'] = t_templet_amazon_published_variation_obj[13]
                t_templet_amazon_published_variation['parent_item_sku'] = t_templet_amazon_published_variation_obj[14]
                t_templet_amazon_published_variation['productSKU'] = t_templet_amazon_published_variation_obj[15]
                t_templet_amazon_published_variation['parent_child'] = t_templet_amazon_published_variation_obj[16]
                t_templet_amazon_published_variation['color_name'] = t_templet_amazon_published_variation_obj[17]
                t_templet_amazon_published_variation['MetalType'] = t_templet_amazon_published_variation_obj[18]
                t_templet_amazon_published_variation['color_map'] = t_templet_amazon_published_variation_obj[19]
                t_templet_amazon_published_variation['size_name'] = t_templet_amazon_published_variation_obj[20]
                t_templet_amazon_published_variation['size_map'] = t_templet_amazon_published_variation_obj[21]
                t_templet_amazon_published_variation['external_product_id'] = t_templet_amazon_published_variation_obj[22]
                t_templet_amazon_published_variation['item_quantity'] = t_templet_amazon_published_variation_obj[23]
                t_templet_amazon_published_variations.append(t_templet_amazon_published_variation)
        shocur.close()
        return t_templet_amazon_published_variations