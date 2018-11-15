#-*-coding:utf-8-*-


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_wait_upload.py
 @time: 2018/2/13 9:41
"""
class t_templet_amazon_wait_upload():
    def __init__(self, db_conn=None):
        self.cnxn = db_conn

    def get_amazon_wait_upload_goods_info_by_id(self, params):
        shocur = self.cnxn.cursor()
        shocur.execute("select upload_product_type,recommended_browse_nodes,recommended_browse_nodes_id,dataFromUrl,item_sku,"
                       "external_product_id,external_product_id_type,item_name,manufacturer,part_number,feed_product_type,item_type,"
                       "product_subtype,product_description,brand_name,update_delete,item_package_quantity,standard_price,sale_price,"
                       "sale_from_date,sale_end_date,condition_type,quantity,merchant_shipping_group_name,bullet_point1,bullet_point2,"
                       "bullet_point3,bullet_point4,bullet_point5,generic_keywords,main_image_url,other_image_url1,other_image_url2,"
                       "other_image_url3,other_image_url4,other_image_url5,other_image_url6,other_image_url7,other_image_url8,fulfillment_center_id,"
                       "model_name,warranty_description,variation_theme,model,mfg_minimum,mfg_minimum_unit_of_measure,swatch_image_url,department_name,"
                       "fit_type,unit_count,unit_count_type,fulfillment_latency,display_dimensions_unit_of_measure,generic_keywords1,generic_keywords2,"
                       "generic_keywords3,generic_keywords4,generic_keywords5,department_name1,department_name2,department_name3,department_name4,"
                       "department_name5,material_type,metal_type,setting_type,ring_size,gem_type,target_audience_keywords1,target_audience_keywords2,"
                       "target_audience_keywords3,productSKU,status,prodcut_variation_id,id,ShopSets,clothing_size,clothing_color,toy_color,jewerly_color,"
                       "item_shape, homes_color, homes_size,number_of_pieces,item_weight,item_weight_unit,color_name_public,sleeve_type,mrp,item_type_name,"
                       "season, material_composition,included_components,are_batteries_included  "
                       "from t_templet_amazon_wait_upload where id = %s ;", (params['id'],))
        t_tempet_amazon_wait_upload_obj = shocur.fetchone()
        t_tempet_amazon_wait_upload = {}
        if t_tempet_amazon_wait_upload_obj:
            t_tempet_amazon_wait_upload['upload_product_type'] = t_tempet_amazon_wait_upload_obj[0]
            t_tempet_amazon_wait_upload['recommended_browse_nodes'] = t_tempet_amazon_wait_upload_obj[1]
            t_tempet_amazon_wait_upload['recommended_browse_nodes_id'] = t_tempet_amazon_wait_upload_obj[2]
            t_tempet_amazon_wait_upload['dataFromUrl'] = t_tempet_amazon_wait_upload_obj[3]
            t_tempet_amazon_wait_upload['item_sku'] = t_tempet_amazon_wait_upload_obj[4]
            t_tempet_amazon_wait_upload['external_product_id'] = t_tempet_amazon_wait_upload_obj[5]
            t_tempet_amazon_wait_upload['external_product_id_type'] = t_tempet_amazon_wait_upload_obj[6]
            t_tempet_amazon_wait_upload['item_name'] = t_tempet_amazon_wait_upload_obj[7]
            t_tempet_amazon_wait_upload['manufacturer'] = t_tempet_amazon_wait_upload_obj[8]
            t_tempet_amazon_wait_upload['part_number'] = t_tempet_amazon_wait_upload_obj[9]
            t_tempet_amazon_wait_upload['feed_product_type'] = t_tempet_amazon_wait_upload_obj[10]
            t_tempet_amazon_wait_upload['item_type'] = t_tempet_amazon_wait_upload_obj[11]
            t_tempet_amazon_wait_upload['product_subtype'] = t_tempet_amazon_wait_upload_obj[12]
            t_tempet_amazon_wait_upload['product_description'] = t_tempet_amazon_wait_upload_obj[13]
            t_tempet_amazon_wait_upload['brand_name'] = t_tempet_amazon_wait_upload_obj[14]
            t_tempet_amazon_wait_upload['update_delete'] = t_tempet_amazon_wait_upload_obj[15]
            t_tempet_amazon_wait_upload['item_package_quantity'] = t_tempet_amazon_wait_upload_obj[16]
            t_tempet_amazon_wait_upload['standard_price'] = t_tempet_amazon_wait_upload_obj[17]
            t_tempet_amazon_wait_upload['sale_price'] = t_tempet_amazon_wait_upload_obj[18]
            t_tempet_amazon_wait_upload['sale_from_date'] = t_tempet_amazon_wait_upload_obj[19]
            t_tempet_amazon_wait_upload['sale_end_date'] = t_tempet_amazon_wait_upload_obj[20]
            t_tempet_amazon_wait_upload['condition_type'] = t_tempet_amazon_wait_upload_obj[21]
            t_tempet_amazon_wait_upload['quantity'] = t_tempet_amazon_wait_upload_obj[22]
            t_tempet_amazon_wait_upload['merchant_shipping_group_name'] = t_tempet_amazon_wait_upload_obj[23]
            t_tempet_amazon_wait_upload['bullet_point1'] = t_tempet_amazon_wait_upload_obj[24]
            t_tempet_amazon_wait_upload['bullet_point2'] = t_tempet_amazon_wait_upload_obj[25]
            t_tempet_amazon_wait_upload['bullet_point3'] = t_tempet_amazon_wait_upload_obj[26]
            t_tempet_amazon_wait_upload['bullet_point4'] = t_tempet_amazon_wait_upload_obj[27]
            t_tempet_amazon_wait_upload['bullet_point5'] = t_tempet_amazon_wait_upload_obj[28]
            t_tempet_amazon_wait_upload['generic_keywords'] = t_tempet_amazon_wait_upload_obj[29]
            t_tempet_amazon_wait_upload['main_image_url'] = t_tempet_amazon_wait_upload_obj[30]
            t_tempet_amazon_wait_upload['other_image_url1'] = t_tempet_amazon_wait_upload_obj[31]
            t_tempet_amazon_wait_upload['other_image_url2'] = t_tempet_amazon_wait_upload_obj[32]
            t_tempet_amazon_wait_upload['other_image_url3'] = t_tempet_amazon_wait_upload_obj[33]
            t_tempet_amazon_wait_upload['other_image_url4'] = t_tempet_amazon_wait_upload_obj[34]
            t_tempet_amazon_wait_upload['other_image_url5'] = t_tempet_amazon_wait_upload_obj[35]
            t_tempet_amazon_wait_upload['other_image_url6'] = t_tempet_amazon_wait_upload_obj[36]
            t_tempet_amazon_wait_upload['other_image_url7'] = t_tempet_amazon_wait_upload_obj[37]
            t_tempet_amazon_wait_upload['other_image_url8'] = t_tempet_amazon_wait_upload_obj[38]
            t_tempet_amazon_wait_upload['fulfillment_center_id'] = t_tempet_amazon_wait_upload_obj[39]
            t_tempet_amazon_wait_upload['model_name'] = t_tempet_amazon_wait_upload_obj[40]
            t_tempet_amazon_wait_upload['warranty_description'] = t_tempet_amazon_wait_upload_obj[41]
            t_tempet_amazon_wait_upload['variation_theme'] = t_tempet_amazon_wait_upload_obj[42]
            t_tempet_amazon_wait_upload['model'] = t_tempet_amazon_wait_upload_obj[43]
            t_tempet_amazon_wait_upload['mfg_minimum'] = t_tempet_amazon_wait_upload_obj[44]
            t_tempet_amazon_wait_upload['mfg_minimum_unit_of_measure'] = t_tempet_amazon_wait_upload_obj[45]
            t_tempet_amazon_wait_upload['swatch_image_url'] = t_tempet_amazon_wait_upload_obj[46]
            t_tempet_amazon_wait_upload['department_name'] = t_tempet_amazon_wait_upload_obj[47]
            t_tempet_amazon_wait_upload['fit_type'] = t_tempet_amazon_wait_upload_obj[48]
            t_tempet_amazon_wait_upload['unit_count'] = t_tempet_amazon_wait_upload_obj[49]
            t_tempet_amazon_wait_upload['unit_count_type'] = t_tempet_amazon_wait_upload_obj[50]
            t_tempet_amazon_wait_upload['fulfillment_latency'] = t_tempet_amazon_wait_upload_obj[51]
            t_tempet_amazon_wait_upload['display_dimensions_unit_of_measure'] = t_tempet_amazon_wait_upload_obj[52]
            t_tempet_amazon_wait_upload['generic_keywords1'] = t_tempet_amazon_wait_upload_obj[53]
            t_tempet_amazon_wait_upload['generic_keywords2'] = t_tempet_amazon_wait_upload_obj[54]
            t_tempet_amazon_wait_upload['generic_keywords3'] = t_tempet_amazon_wait_upload_obj[55]
            t_tempet_amazon_wait_upload['generic_keywords4'] = t_tempet_amazon_wait_upload_obj[56]
            t_tempet_amazon_wait_upload['generic_keywords5'] = t_tempet_amazon_wait_upload_obj[57]
            t_tempet_amazon_wait_upload['department_name1'] = t_tempet_amazon_wait_upload_obj[58]
            t_tempet_amazon_wait_upload['department_name2'] = t_tempet_amazon_wait_upload_obj[59]
            t_tempet_amazon_wait_upload['department_name3'] = t_tempet_amazon_wait_upload_obj[60]
            t_tempet_amazon_wait_upload['department_name4'] = t_tempet_amazon_wait_upload_obj[61]
            t_tempet_amazon_wait_upload['department_name5'] = t_tempet_amazon_wait_upload_obj[62]
            t_tempet_amazon_wait_upload['material_type'] = t_tempet_amazon_wait_upload_obj[63]
            t_tempet_amazon_wait_upload['metal_type'] = t_tempet_amazon_wait_upload_obj[64]
            t_tempet_amazon_wait_upload['setting_type'] = t_tempet_amazon_wait_upload_obj[65]
            t_tempet_amazon_wait_upload['ring_size'] = t_tempet_amazon_wait_upload_obj[66]
            t_tempet_amazon_wait_upload['gem_type'] = t_tempet_amazon_wait_upload_obj[67]
            t_tempet_amazon_wait_upload['target_audience_keywords1'] = t_tempet_amazon_wait_upload_obj[68]
            t_tempet_amazon_wait_upload['target_audience_keywords2'] = t_tempet_amazon_wait_upload_obj[69]
            t_tempet_amazon_wait_upload['target_audience_keywords3'] = t_tempet_amazon_wait_upload_obj[70]
            t_tempet_amazon_wait_upload['productSKU'] = t_tempet_amazon_wait_upload_obj[71]
            t_tempet_amazon_wait_upload['status'] = t_tempet_amazon_wait_upload_obj[72]
            t_tempet_amazon_wait_upload['prodcut_variation_id'] = t_tempet_amazon_wait_upload_obj[73]
            t_tempet_amazon_wait_upload['id'] = t_tempet_amazon_wait_upload_obj[74]
            t_tempet_amazon_wait_upload['ShopSets'] = t_tempet_amazon_wait_upload_obj[75]
            t_tempet_amazon_wait_upload['clothing_size'] = t_tempet_amazon_wait_upload_obj[76]
            t_tempet_amazon_wait_upload['clothing_color'] = t_tempet_amazon_wait_upload_obj[77]
            t_tempet_amazon_wait_upload['toy_color'] = t_tempet_amazon_wait_upload_obj[78]
            t_tempet_amazon_wait_upload['jewerly_color'] = t_tempet_amazon_wait_upload_obj[79]
            t_tempet_amazon_wait_upload['item_shape'] = t_tempet_amazon_wait_upload_obj[80]
            t_tempet_amazon_wait_upload['homes_color'] = t_tempet_amazon_wait_upload_obj[81]
            t_tempet_amazon_wait_upload['homes_size'] = t_tempet_amazon_wait_upload_obj[82]
            t_tempet_amazon_wait_upload['number_of_pieces'] = t_tempet_amazon_wait_upload_obj[83]
            t_tempet_amazon_wait_upload['item_weight'] = t_tempet_amazon_wait_upload_obj[84]
            t_tempet_amazon_wait_upload['item_weight_unit'] = t_tempet_amazon_wait_upload_obj[85]
            t_tempet_amazon_wait_upload['color_name_public'] = t_tempet_amazon_wait_upload_obj[86]
            t_tempet_amazon_wait_upload['sleeve_type'] = t_tempet_amazon_wait_upload_obj[87]
            t_tempet_amazon_wait_upload['mrp'] = t_tempet_amazon_wait_upload_obj[88]
            t_tempet_amazon_wait_upload['item_type_name'] = t_tempet_amazon_wait_upload_obj[89]
            t_tempet_amazon_wait_upload['season'] = t_tempet_amazon_wait_upload_obj[90]
            t_tempet_amazon_wait_upload['material_composition'] = t_tempet_amazon_wait_upload_obj[91]
            t_tempet_amazon_wait_upload['included_components'] = t_tempet_amazon_wait_upload_obj[92]
            t_tempet_amazon_wait_upload['are_batteries_included'] = t_tempet_amazon_wait_upload_obj[93]

        shocur.close()
        return t_tempet_amazon_wait_upload

    def update_status(self, status,id):
        shocur = self.cnxn.cursor()
        shocur.execute("update t_templet_amazon_wait_upload set status=%s where id=%s;",(status,id))
        shocur.execute("commit;")
        shocur.close()

