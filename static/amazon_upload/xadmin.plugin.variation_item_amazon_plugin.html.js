$(document).ready(function () {
    var id_item_name_len = $('#id_item_name').val().length;
    var id_generic_keywords1_len = $('#id_generic_keywords1').val().length;
    $('#id_item_name').after('<span id="id_item_name_num">'+id_item_name_len+'/150</span>');
    $('#id_generic_keywords1').after('<span id="id_generic_keywords1_num">'+id_generic_keywords1_len+'/249</span>');

    //检测sku是否侵权
    $('#id_productSKU').blur(function () {
        var productSKU = $("#id_productSKU").val();
        if(productSKU) {
            var url = "/Project/admin/skuapp/t_templet_amazon_collection_box/check_sku_tortinfo/?productSKU=" + productSKU;
            $.getJSON(url, function(result){
                if (result.code == '1'){
                    if(result.data == '-1') {
                        if(document.getElementById("id_productSKU_tort")){
                            console.log(document.getElementById("id_productSKU_tort").innerText);
                            if(document.getElementById("id_productSKU_tort").innerText == ''){
                                $('#id_productSKU_tort').html('该商品SKU在Amazon存在侵权记录');
                            }
                        }else {
                            $('#id_productSKU').after('<span id="id_productSKU_tort" style="color: red">该商品SKU在Amazon存在侵权记录</span>');
                            console.log(result.tort_list);
                        }
                    }else {
                        if(document.getElementById("id_productSKU_tort")){
                            $('#id_productSKU_tort').html('');
                        }
                    }
                }else {
                    alert('异常:'+result.errortext);
                }
            });
        }else {
            if(document.getElementById("id_productSKU_tort")){
                $('#id_productSKU_tort').html('');
            }
        }
    });

    $('#id_product_description').blur(function () {
        var array = $("#id_product_description").val().split("\n");
        var stringText = '<p>';
        if(array[0].indexOf("<p>") >= 0){
            stringText = '';
        }
        for(i=0;i<array.length;i++){
            if((array[i].indexOf("<br />") >= 0)||(array[i].indexOf("</p>") >= 0)){
                if(array[i].indexOf("</p>") >= 0){
                    stringText += array[i];
                }else {
                    stringText += array[i] + '\n';
                }
            }else {
                stringText += array[i] + '<br />' + '\n';
            }
        }
        if(stringText.indexOf("</p>") < 0){
            stringText += '</p>';
        }

        // stringText = stringText.replace('<p>','').replace('</p>','');
        // stringText = '<p>' + stringText + '</p>';
        $('#id_product_description').innerHTML = stringText;
        $('#id_product_description').val(stringText);
    });
    $('#id_upload_product_type').readOnly=true;
    var feed_product_type = $('#feed_product_type').val();
    $('#select_id_feed_product_type').innerHTML = feed_product_type;

    var variation_type = $('#variantion_theme_selected').val();
    console.log(variation_type);
    if(variation_type){
        var $select_id_variation_theme = $('#select_id_variation_theme').selectize();
        $select_id_variation_theme[0].selectize.setValue(variation_type);
    }
});

function deal_product_description(stringText) {
    var string_text = "";
    var allparams = stringText.split('<br />');
    for(var i = 0; i < allparams.length; i++){
        if(i + 1 == allparams.length){
            string_text += allparams[i];
        }else {
            string_text += allparams[i] + "<br />\n";
        }
    }
    if(string_text.indexOf("<br> />")>0){
        string_text = string_text.replace("<br> />", '');
    }
    if(string_text.indexOf("</ p>")>0){
        string_text = string_text.replace("</ p>", '</p>');
    }
    return string_text
}

//计算字符串的实际长度（unicode转utf8）
function sizeof(str, charset){
    var total = 0, charCode, i, len;
    charset = charset ? charset.toLowerCase() : '';
    if(charset === 'utf-16' || charset === 'utf16'){
        for(i = 0, len = str.length; i < len; i++){
            charCode = str.charCodeAt(i);
            if(charCode <= 0xffff){
                total += 2;
            }else{
                total += 4;
            }
        }
    }else{
        for(i = 0, len = str.length; i < len; i++){
            charCode = str.charCodeAt(i);
            if(charCode <= 0x007f) {
                total += 1;
            }else if(charCode <= 0x07ff){
				total += 2;
			}else if(charCode <= 0xffff){
				total += 3;
            }else{
                total += 4;
            }
        }
    }
    return total;
}

$('#id_item_name').keyup(function () {
    var item_name = $('#id_item_name').val();
    var name_length = sizeof(item_name, 'utf8');
    $('#id_item_name_num').html(name_length+'/150');
});
$('#id_generic_keywords1').keyup(function () {
    caculate_length('id_generic_keywords1');
});


function caculate_length(id) {
    var item_name = $('#' + id).val();
    var name_length = sizeof(item_name, 'utf8');
    $('#'+id+'_num').html(name_length+'/249');
}

var tra = {"google": {"FR": "fr", "DE": "de"}, "baidu": {"FR": "fra", "DE": "deu"}};

function transaction_text(transaction_data) {

}

function transaction_single() {
    var id_text_transaction = $('#id_text_transaction').val();
    console.log("  aaaa:" + id_text_transaction + "aaaaaaa");
    if(id_text_transaction){
        var site = $('#searchSite').val();
        var tra_type = "google";
        var tra_to = '';
        var split_type = "=========";
        if(site == 'DE'){
            tra_to = 'de';
        }else if(site == 'FR'){
            tra_to = 'fr';
        }
        if(tra_to){
            $('#div_id_transaction_result').css("display", "block");
            $('#id_transaction_result').css("display", "block");
            $('#id_transaction_result').val("正在翻译中，请稍后...");
            var url = "/Project/admin/skuapp/t_templet_amazon_collection_box/transaction_text_amazon/?tra_type=google&tra_to="+tra_to+"&tra_data="+id_text_transaction;
            $.getJSON(url, function(result) {
                if (result.code == '1') {
                    $('#id_transaction_result').val(result.data.replace(split_type, ''));
                }else {
                    $('#id_transaction_result').val("翻译失败，原因: " + result.errortext);
                }
            });
        }else {
            if(site=='US'||site=='UK'){
                alert("此站点已经是英文，无需翻译");
            }else {
                alert("暂不支持翻译到"+site+"语系");
            }
        }
    }else {
        alert("翻译内容不能为空");
    }
}

function transaction_all() {
    var item_name = $('#id_item_name').val();
    var id_bullet_point1 = $('#id_bullet_point1').val();
    var id_bullet_point2 = $('#id_bullet_point2').val();
    var id_bullet_point3 = $('#id_bullet_point3').val();
    var id_bullet_point4 = $('#id_bullet_point4').val();
    var id_bullet_point5 = $('#id_bullet_point5').val();
    var id_product_description = $('#id_product_description').val();
    var id_generic_keywords1 = $('#id_generic_keywords1').val();
    var id_list = ["id_item_name", "id_bullet_point1", "id_bullet_point2", "id_bullet_point3", "id_bullet_point4",
                    "id_bullet_point5", "id_product_description", "id_generic_keywords1"]
    if(item_name&&id_bullet_point1&&id_bullet_point2&&id_bullet_point3&&id_bullet_point4&&id_bullet_point5&&id_product_description&&id_generic_keywords1){
        var site = $('#searchSite').val();
        var array = id_product_description.split("\n");
        var new_id_product_description = '';
        for(i=0;i<array.length;i++){
            new_id_product_description += array[i];
        }
        new_id_product_description = new_id_product_description.replace(/<p>/g, ' 5185 ');
        new_id_product_description = new_id_product_description.replace(/<\/p>/g, ' 5186 ');
        new_id_product_description = new_id_product_description.replace(/<br \/>/g, ' 5187 ');
        if(new_id_product_description.indexOf("<strong>") > 0){
            new_id_product_description = new_id_product_description.replace(/<strong>/g, ' 5188 ');
            new_id_product_description = new_id_product_description.replace(/<\/strong>/g, ' 5189 ');
        }
        // console.log(new_id_product_description);


        var split_type = "=========";
        var tra_to = '';
        var transaction_data = item_name +split_type+ id_bullet_point1 +split_type+ id_bullet_point2 +split_type+ id_bullet_point3+
            split_type+ id_bullet_point4 +split_type+ id_bullet_point5 +split_type+ id_generic_keywords1 +split_type+ new_id_product_description;

        if(transaction_data.indexOf('&') > 0){
            transaction_data = transaction_data.replace(/&/g, ' 5190 ');
        }
        if(transaction_data.indexOf(';') > 0){
            transaction_data = transaction_data.replace(/;/g, ' 5191 ');
        }
        console.log(transaction_data);
        if(site == 'DE'){
            tra_to = 'de';
        }else if(site == 'FR'){
            tra_to = 'fr';
        }
        if(tra_to){
            $('#div_id_transaction_result').css("display", "block");
            $('#id_transaction_result').css("display", "block");
            $('#id_transaction_result').val("正在翻译中，请稍后...");
            var url = "/Project/admin/skuapp/t_templet_amazon_collection_box/transaction_text_amazon/?tra_type=google&tra_to="+tra_to+"&tra_data="+transaction_data;
            $.getJSON(url, function(result) {
                if (result.code == '1') {
                    var tra_result = result.data;
                    if(tra_result.indexOf('5190') > 0){
                        tra_result = tra_result.replace(/ 5190 /g, '&');
                    }
                    if(tra_result.indexOf('5191') > 0){
                        tra_result = tra_result.replace(/ 5191 /g, ';');
                    }
                    var tra_list = tra_result.split(split_type);
                    console.log(tra_list);
                    var error_info = 'transaction error';
                    var show_error = '';
                    if(tra_list[0] == error_info){
                        show_error += '产品标题翻译失败，';
                    }else {
                        $('#id_item_name').val(tra_list[0]);
                    }
                    if(tra_list[1] == error_info){
                        show_error += '产品描述1翻译失败，';
                    }else {
                        $('#id_bullet_point1').val(tra_list[1]);
                    }
                    if(tra_list[2] == error_info){
                        show_error += '产品描述2翻译失败，';
                    }else {
                        $('#id_bullet_point2').val(tra_list[2]);
                    }
                    if(tra_list[3] == error_info){
                        show_error += '产品描述3翻译失败，';
                    }else {
                        $('#id_bullet_point3').val(tra_list[3]);
                    }
                    if(tra_list[4] == error_info){
                        show_error += '产品描述4翻译失败，';
                    }else {
                        $('#id_bullet_point4').val(tra_list[4]);
                    }
                    if(tra_list[5] == error_info){
                        show_error += '产品描述5翻译失败，';
                    }else {
                        $('#id_bullet_point5').val(tra_list[5]);
                    }
                    if(tra_list[6] == error_info){
                        show_error += '关键词翻译失败，';
                    }else {
                        $('#id_generic_keywords1').val(tra_list[6]);
                    }
                    if(tra_list[7] == error_info){
                        show_error += '产品描述翻译失败，';
                    }else {
                        var des_text = tra_list[7];
                        console.log(des_text);
                        des_text = des_text.replace(/5185/g, '<p>');
                        des_text = des_text.replace(/5186/g, '</p>');
                        des_text = des_text.replace(/5187/g, '<br />');
                        if(des_text.indexOf("5188") > 0){
                            des_text = des_text.replace(/5188/g, '<strong>');
                            des_text = des_text.replace(/5189/g, '</strong>');
                        }
                        var string_text = deal_product_description(des_text);
                        $('#id_product_description').val(string_text);
                    }
                    if(show_error == ""){
                        show_error = "翻译成功";
                    }
                    $('#id_transaction_result').val(show_error);
                }else {
                    $('#id_transaction_result').val("翻译失败，原因: " + result.errortext);
                }
            });
        }else {
            if(site=='US'||site=='UK'){
                alert("此站点已经是英文，无需翻译");
            }else {
                alert("暂不支持翻译到"+site+"语系");
            }

        }
    }else {
        alert("翻译前请确认以下几点输入内容不为空：产品标题、产品描述、五点描述和关键词");
    }
}

function transaction_variation_info() {
    var colornames = [];
    var sizenames = [];
    var metaltypenames =[];
    var tra_data = "";
    var id_list = [];
    var split_type = "=========";
    var tra_to = '';
    if(document.getElementsByName("color_name")){
        $("input[name='color_name']").each(function () {
            colornames.push($(this).val());
        });
        for(var i=0; i<colornames.length; i++){
            var count = i +1;
            if(colornames[i]){
                id_list.push("id_color_name_" + count);
                tra_data += colornames[i] + split_type;
            }
        }
    }
    if(document.getElementsByName("size_name")){
        $("input[name='size_name']").each(function () {
            sizenames.push($(this).val());
        });
        for(var i=0; i<sizenames.length; i++){
            var count = i +1;
            if(sizenames[i]){
                id_list.push("id_size_name_" + count);
                tra_data += sizenames[i] + split_type;
            }
        }
    }
    if(document.getElementsByName("MetalType")){
        $("input[name='MetalType']").each(function () {
            metaltypenames.push($(this).val());
        });
        for(var i=0; i<metaltypenames.length; i++){
            var count = i +1;
            if(metaltypenames[i]){
                id_list.push("id_MetalType_" + count);
                tra_data += metaltypenames[i] + split_type;
            }
        }
    }
    var site = $('#searchSite').val();
    if(site == 'DE'){
        tra_to = 'de';
    }else if(site == 'FR'){
        tra_to = 'fr';
    }
    tra_data = tra_data.substring(0,tra_data.length-9);
    console.log(tra_data);
    if(tra_to){
        $('#div_id_transaction_result').css("display", "block");
        $('#id_transaction_result').css("display", "block");
        $('#id_transaction_result').val("正在翻译中，请稍后...");
        var url = "/Project/admin/skuapp/t_templet_amazon_collection_box/transaction_text_amazon/?tra_type=google&tra_to="+tra_to+"&tra_data="+tra_data;
        $.getJSON(url, function(result) {
            console.log(result.code);
            if (result.code == '1') {
                var tra_result = result.data;
                var tra_list = tra_result.split(split_type);
                var error_info = 'transaction error';
                var show_error = '';
                for(var i = 0; i < id_list.length; i++){
                    if(tra_list[i] == error_info){
                        show_error += id_list.replace("id_", "") + '翻译失败，';
                    }else {
                        $('#'+ id_list[i]).val(tra_list[i]);
                    }
                }
                if(show_error == ""){
                    show_error = "翻译成功";
                }
                $('#id_transaction_result').val(show_error);
            }else {
                $('#id_transaction_result').val("翻译失败，原因: " + result.errortext);
            }
        });
    }else {
        if(site=='US'||site=='UK'){
            alert("此站点已经是英文，无需翻译");
        }else {
            alert("暂不支持翻译到"+site+"语系");
        }

    }
}

function sele_Change() {
    var variationItem = $('#select_id_variation_theme').val();
    variation_type = variationItem;
    if(variationItem != 0){
        $('#auto_add_variation').show();
        $('#auto_add_variation_name').show();
        $('#addItems_span').show();
        $('#add_images_parent').hide();
    }else {
        $('#add_images_parent').show();
        $('#auto_add_variation').hide();
        $('#auto_add_variation_name').hide();
        $('#addItems_span').hide();
        $('#div_id_color_name').hide();
        $('#div_id_size_name').hide();
        $('#div_id_size_color').hide();
        $('#div_id_MetalType').hide();
        $('#div_id_size_MetalType').hide();
    }
    if(variationItem=='Color'){
        show_first_color_div(childSkulist);
        $('#div_id_color_name').show();
        $('#div_id_size_name').hide();
        $('#div_id_size_color').hide();
        $('#div_id_MetalType').hide();
        $('#div_id_size_MetalType').hide();
        $('#div_id_MetalType_color').hide();
    }
    if(variationItem=='Size'){
        show_first_size_div(childSkulist);
        $('#div_id_size_name').show();
        $('#div_id_color_name').hide();
        $('#div_id_size_color').hide();
        $('#div_id_MetalType').hide();
        $('#div_id_size_MetalType').hide();
        $('#div_id_MetalType_color').hide();
    }
    if(variationItem=='Size-Color'){
        show_first_size_color(childSkulist);
        $('#div_id_size_color').show();
        $('#div_id_size_name').hide();
        $('#div_id_color_name').hide();
        $('#div_id_MetalType').hide();
        $('#div_id_size_MetalType').hide();
        $('#div_id_MetalType_color').hide();
    }
    if(variationItem=='MetalType'){
        show_first_MetalType_div(childSkulist);
        $('#div_id_size_color').hide();
        $('#div_id_size_name').hide();
        $('#div_id_color_name').hide();
        $('#div_id_MetalType').show();
        $('#div_id_size_MetalType').hide();
        $('#div_id_MetalType_color').hide();
    }
    if(variationItem=='Color-MetalType'){
        show_first_MetalType_color(childSkulist);
        $('#div_id_size_color').hide();
        $('#div_id_size_name').hide();
        $('#div_id_color_name').hide();
        $('#div_id_MetalType').hide();
        $('#div_id_size_MetalType').hide();
        $('#div_id_MetalType_color').show();
    }
    if(variationItem=='MetalType-Size'){
        show_first_size_MetalType(childSkulist);
        $('#div_id_size_color').hide();
        $('#div_id_size_name').hide();
        $('#div_id_color_name').hide();
        $('#div_id_MetalType').hide();
        $('#div_id_size_MetalType').show();
        $('#div_id_MetalType_color').hide();
    }
}

function add_images(count){
    var productSKU = $('#id_productSKU').val();
    if(productSKU=='' || productSKU == null){
        alert('请先输入有效的商品SKU!');
        return
    }
    var ShopSets = $('#select_id_ShopSets').val();
    if(ShopSets=='0'){
        alert('请先选择刊登店铺!');
        return
    }
    var postURL = '/add_amazon_images/?productSKU=' + productSKU;
    var variationItem = $('#select_id_variation_theme').val();
    if(variationItem != 0){
        var td = event.srcElement; // 通过event.srcelement 获取激活事件的对象 td
        var productItemSku = $('#id_product_sku_'+count).val();
        if(productItemSku=='' || productItemSku == null){
            alert('请先输入有效的变体商品SKU!');
            return
        }
        postURL += '&productItemSku=' + productItemSku;
    }
    var sourceURL = $('#sourceURL').val();
    postURL += '&' + sourceURL;
    layer.open({
        type:2,
        skin:'layui-layer-lan',
        title:'查看全部',
        fix:false,
        shadeClose: true,
        maxmin:true,
        area:['1000px','600px'],
        content:postURL,
        btn: ['确定'],
        yes: function(index){
            //当点击‘确定’按钮的时候，获取弹出层返回的值
            var res = window["layui-layer-iframe" + index].callbackdata();
            //打印返回的值，看是否有我们想返回的值。
            if(count == 0){
                document.getElementById('id_image_main').value = res.image_ur_str;
            }else {
                document.getElementById('id_image_'+count).value = res.image_ur_str;
                document.getElementById('add_images_'+count).style.background = '#555555';
            }
            console.log(res.image_ur_str);
            //最后关闭弹出层
            layer.close(index);
        },
        cancel: function(){
            //右上角关闭回调
        }
    });
}

function copyIMG(idx) {
    var count = idx + 1;
    var tab = document.getElementById("mytable");
    //表格行数
    var rows = tab.rows;
    var last_id = -1;
    for(var i = 0; i < rows.length; i++){
        var id = rows[i].id;
        if(id == count){
            break;
        }
        last_id = id;
    }
    console.log('copy last id: ' + last_id);
    if(last_id == -1){
        alert('无效按钮');
    }else {
        var image_url = document.getElementById('id_image_'+last_id).value;
        if(image_url) {
            document.getElementById('id_image_'+count).value = image_url;
            document.getElementById('add_images_'+count).style.background = '#555555';
        }else {
            alert('请先上传上一个变体的图片！');
        }
    }
}

function viewIMG(idx) {
    var image_url = document.getElementById('id_image_'+idx).value;
    var product_sku = document.getElementById('id_product_sku_'+idx).value;
    var inhtml = '';
    if(image_url){
        image_url = image_url.replace(/u'/g,"'").replace(/'/g, '"');
        image_url = JSON.parse(image_url);
        // console.log(image_url.main_image_url);
        inhtml = '<div><table id="mytable" class="border1"><tr class="tr1" style="height: 30px;">' +
            '<td style="width: 200px;">主图：<img src="'+image_url.main_image_url+'" width="150" /></td></tr>' +
            '<tr class="tr1" style="height: 30px;"><td style="width: 200px;">附图1：<img src="'+image_url.other_image_url1+'" width="150" /></td>' +
            '<td style="width: 200px;">附图2：<img src="'+image_url.other_image_url2+'" width="150" /></td>' +
            '<td style="width: 200px;">附图3：<img src="'+image_url.other_image_url3+'" width="150" /></td>' +
            '<td style="width: 200px;">附图4：<img src="'+image_url.other_image_url4+'" width="150" /></td></tr>' +
            '<tr class="tr1" style="height: 30px;"><td style="width: 200px;">附图5：<img src="'+image_url.other_image_url5+'" width="150" /></td>' +
            '<td style="width: 200px;">附图6：<img src="'+image_url.other_image_url6+'" width="150" /></td>' +
            '<td style="width: 200px;">附图7：<img src="'+image_url.other_image_url7+'" width="150" /></td>' +
            '<td style="width: 200px;">附图8：<img src="'+image_url.other_image_url8+'" width="150" /></td></tr>' +
            '</table></div>';
        layer.open({
            type: 1,
            skin:'layui-layer-lan',
            title: product_sku + '图片预览',
            fix:false,
            shadeClose: true,
            // shade: false,
            maxmin: true, //开启最大化最小化按钮
            area: ['893px', '600px'],
            content: inhtml,
            btn: ['关闭页面'],
            yes: function(index){
                layer.close(index);
            },
            cancel: function(){
                //右上角关闭回调
            },
            end:function (){
                
            }
        });
    }else {
        alert('请先上传图片！');
    }
}

function del(obj) {
    var tableI = document.getElementById("mytable");//找到要删除行所在的teble
    var trI = obj.parentNode.parentNode;//我的button在tr下的td中，两次执行.parentNode操作，可以找到要删除的tr。

    var index = trI.rowIndex;//要删除的tr所在table中的index
    tableI.deleteRow(index);//执行删除
}

function show_old_variation(){
    console.log(product_variations.length);
    var htext = "";
    for(var i = 0; i < product_variations.length; i++){
        var product_variation = product_variations[i];
        var count = i + 1;
        htext += '<tr id="'+count+'" class="tr1" style="height: 30px;">';
        if(variation_type.indexOf("Color") > -1 ){
            htext += '<td><label id="id_color_name" class="control-label requiredField">颜色名<span class="asteriskField">*</span></label></td>' +
                '<td><input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text" value="'+product_variation['color_name']+'"/></td>';
        }
        if(variation_type.indexOf("MetalType") > -1 ){
            htext += '<td><label id="id_MetalType" class="control-label requiredField">材 料<span class="asteriskField">*</span></label></td>' +
                '<td><input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" value="'+product_variation['MetalType']+'"/></td>';
        }
        if(variation_type.indexOf("Size") > -1 ){
            htext += '<td><label id="id_size_name" class="control-label requiredField">尺寸名<span class="asteriskField">*</span></label></td>' +
                '<td><input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text" value="'+product_variation['size_name']+'"/></td>';
        }
        var img_dict = "";
        if(product_variation['other_image_url8']||product_variation['main_image_url']||product_variation['other_image_url2']
            ||product_variation['other_image_url3']||product_variation['other_image_url1']||product_variation['other_image_url6']
        ||product_variation['other_image_url7']||product_variation['other_image_url4']||product_variation['other_image_url5']){
            var img_dict = "{'other_image_url8': '"+product_variation['other_image_url8']+"', 'main_image_url': '"+product_variation['main_image_url']+"', " +
                            "'other_image_url2': '"+product_variation['other_image_url2']+"','other_image_url3': '"+product_variation['other_image_url3']+"', " +
                            "'other_image_url1': '"+product_variation['other_image_url1']+"', 'other_image_url6': '"+product_variation['other_image_url6']+"'," +
                            "'other_image_url7': '"+product_variation['other_image_url7']+"', 'other_image_url4': '"+product_variation['other_image_url4']+"', " +
                            "'other_image_url5': '"+product_variation['other_image_url5']+"'}";
        }
        htext += '<td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td>' +
    '                   <td><input class="text-field admintextinputwidget form-control" id="id_product_sku_'+count+'" maxlength="200" value="'+product_variation['productSKU']+'" name="product_SKU" type="text" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td>' +
            '<td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" value="'+product_variation['price']+'" type="number" onkeyup="onlyNonNegative(this)"/></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td>' +
            '<td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="'+product_variation['item_quantity']+'" onkeyup="onlyNumNegative(this)"/></td>';
        if(img_dict){
            htext += '<td><input type="button" id="add_images_'+count+'" class="btn btn-primary" value="上传图片" onclick="add_images('+count+')" style="background: #555555"/>';
        }else {
            htext += '<td><input type="button" id="add_images_'+count+'" class="btn btn-primary" value="上传图片" onclick="add_images('+count+')"/>';
        }
        htext += '<input type="hidden" id="id_image_'+count+'" name="variation_images" value="'+ img_dict +'" /></td>';
        if(i != 0) {
                    htext += '<td><input type="button" id="copy_image_'+count+'" class="btn btn-primary" value="同上" onclick="copyIMG('+ i +')" /></td>' +
                        '<td><input type="button" id="view_image_'+count+'" class="btn btn-primary" value="预览" onclick="viewIMG('+ count +')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
                else {
                    htext += '<td><input type="button" id="view_image_'+count+'" class="btn btn-primary" value="预览" onclick="viewIMG('+ count +')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
    }
    return htext
}

function show_first_size_div(childSkulist) {
    var htext = '<table id="mytable" class="border1">';
    var product_variation_count = 0;
    if(product_variations.length>0){
        product_variation_count = product_variations.length;
        htext += show_old_variation();
        for(var i = 0; i < childSkulist.length; i++) {
            var param_value = childSkulist[i];
            var count = i + 1 + product_variation_count;
            htext += '<tr id="'+count+'" class="tr1" style="height: 30px;"><td><label id="id_size_name" class="control-label requiredField">\n' +
    '                        尺寸名<span class="asteriskField">*</span></label></td>\n' +
    '                    <td><input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text" value="'+param_value['productSize']+'"/></td>' +
    '                    <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td>' +
    '                   <td><input class="text-field admintextinputwidget form-control" id="id_product_sku_'+count+'" maxlength="200" name="product_SKU" type="text" value="'+param_value['productSKU']+'" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)"/></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)"/></td>' +
    '                   <td><input type="button" id="add_images_'+count+'" class="btn btn-primary" value="上传图片" onclick="add_images('+count+')" /><input type="hidden" id="id_image_'+count+'" name="variation_images" value="" /></td>';
            if(count != 1) {
                htext += '<td><input type="button" id="copy_image_'+count+'" class="btn btn-primary" value="同上" onclick="copyIMG('+ i +')" /></td>' +
                    '<td><input type="button" id="view_image_'+count+'" class="btn btn-primary" value="预览" onclick="viewIMG('+ count +')" /></td>' +
                    '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
            }
            else {
                htext += '<td><input type="button" id="view_image_'+count+'" class="btn btn-primary" value="预览" onclick="viewIMG('+ count +')" /></td>' +
                    '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
            }
        }
    }
    else {
        if(childSkulist.length < 1) {
            count = 1;
            htext += '<tr id="1" class="tr1" style="height: 30px;"><td><label id="id_size_name" class="control-label requiredField">\n' +
    '                        尺寸名<span class="asteriskField">*</span></label></td>\n' +
    '                    <td><input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text"/></td>' +
    '                    <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td>' +
    '                   <td><input class="text-field admintextinputwidget form-control" id="id_product_sku_'+count+'" maxlength="200" name="product_SKU" type="text" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)"/></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)"/></td>' +
    '                   <td><input type="button" id="add_images_'+count+'" class="btn btn-primary" value="上传图片" onclick="add_images('+count+')" /><input type="hidden" id="id_image_'+count+'" name="variation_images" value="" /></td>';
            htext += '<td><input type="button" id="view_image_'+count+'" class="btn btn-primary" value="预览" onclick="viewIMG('+ count +')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
        }else {
            for(var i = 0; i < childSkulist.length; i++) {
                var param_value = childSkulist[i];
                var count = i + 1;
                htext += '<tr id="'+count+'" class="tr1" style="height: 30px;"><td><label id="id_size_name" class="control-label requiredField">\n' +
        '                        尺寸名<span class="asteriskField">*</span></label></td>\n' +
        '                    <td><input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text" value="'+param_value['productSize']+'"/></td>' +
        '                    <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td>' +
        '                   <td><input class="text-field admintextinputwidget form-control" id="id_product_sku_'+count+'" maxlength="200" name="product_SKU" type="text" value="'+param_value['productSKU']+'" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
        '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)"/></td>' +
        '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)"/></td>' +
        '                   <td><input type="button" id="add_images_'+count+'" class="btn btn-primary" value="上传图片" onclick="add_images('+count+')" /><input type="hidden" id="id_image_'+count+'" name="variation_images" value="" /></td>';
                if(i != 0) {
                    htext += '<td><input type="button" id="copy_image_'+count+'" class="btn btn-primary" value="同上" onclick="copyIMG('+ i +')" /></td>' +
                        '<td><input type="button" id="view_image_'+count+'" class="btn btn-primary" value="预览" onclick="viewIMG('+ count +')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
                else {
                    htext += '<td><input type="button" id="view_image_'+count+'" class="btn btn-primary" value="预览" onclick="viewIMG('+ count +')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
            }
        }
    }
    // console.log(childSkulist);
    // console.log(childSkulist.length);

    htext += '</table>';
    document.getElementById("div_id_MetalType_color").innerHTML = ''
    document.getElementById("div_id_size_MetalType").innerHTML = ''
    document.getElementById("div_id_MetalType").innerHTML = ''
    document.getElementById("div_id_color_name").innerHTML = ''
    document.getElementById("div_id_size_color").innerHTML = ''
    document.getElementById("div_id_size_name").innerHTML = htext;
}

function show_first_color_div(childSkulist) {
    var htext = '<table id="mytable" class="border1">';
    var product_variation_count = 0;
    if(product_variations.length>0) {
        product_variation_count = product_variations.length;
        htext += show_old_variation();
        for (var i = 0; i < childSkulist.length; i++) {
            var param_value = childSkulist[i];
            var count = i + 1 + product_variation_count;
            htext += '<tr id="'+count+'" class="tr1" style="height: 30px;"><td><label id="id_color_name" class="control-label requiredField">\n' +
                '                        颜色名<span class="asteriskField">*</span></label></td>\n' +
                '                    <td><input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text"/></td>' +
                '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" ' +
                '                       id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" type="text" value="' + param_value['productSKU'] + '" onblur="check_sku_tortInfo(this.id,this.value)" /></td><td><label id="id_size_name" class="control-label requiredField">' +
                '                   价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
                '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
                '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
            if (count != 1) {
                htext += '<td><input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + i + ')" /></td>' +
                    '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                    '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
            }
            else {
                htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                    '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
            }
        }
    }
    else {
        if(childSkulist.length < 1) {
            count = 1;
            htext += '<tr id="1" class="tr1" style="height: 30px;"><td><label id="id_color_name" class="control-label requiredField">\n' +
    '                        颜色名<span class="asteriskField">*</span></label></td>\n' +
    '                    <td><input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text"/></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" ' +
                '       maxlength="200" name="product_SKU" type="text" onblur="check_sku_tortInfo(this.id,this.value)" /></td><td><label id="id_size_name" class="control-label requiredField">' +
    '                   价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
            htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
        }else {
            for (var i = 0; i < childSkulist.length; i++) {
                var param_value = childSkulist[i];
                var count = i + 1;
                htext += '<tr id="'+count+'" class="tr1" style="height: 30px;"><td><label id="id_color_name" class="control-label requiredField">\n' +
                    '                        颜色名<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text"/></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" ' +
                    '                       id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" type="text" value="' + param_value['productSKU'] + '" onblur="check_sku_tortInfo(this.id,this.value)" /></td><td><label id="id_size_name" class="control-label requiredField">' +
                    '                   价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
                    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
                if (i != 0) {
                    htext += '<td><input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + i + ')" /></td>' +
                        '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
                else {
                    htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
            }
        }
    }

    htext += '</table>';
    document.getElementById("div_id_MetalType_color").innerHTML = ''
    document.getElementById("div_id_size_MetalType").innerHTML = ''
    document.getElementById("div_id_MetalType").innerHTML = ''
    document.getElementById("div_id_size_color").innerHTML = ''
    document.getElementById("div_id_size_name").innerHTML = ''
    document.getElementById("div_id_color_name").innerHTML = htext;
}

function show_first_size_color(childSkulist) {
    var htext = '<table id="mytable" class="border1">';
    var product_variation_count = 0;
    if(product_variations.length>0) {
        product_variation_count = product_variations.length;
        htext += show_old_variation();
        for (var i = 0; i < childSkulist.length; i++) {
                var param_value = childSkulist[i];
                var count = i + 1 + product_variation_count;
                htext += '<tr id="'+count+'" class="tr1" style="height: 30px;"><td><label id="id_color_name" class="control-label requiredField">\n' +
                    '                        颜色名<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text" /></td>\n' +
                    '                    <td><label id="id_size_name" class="control-label requiredField">尺寸名<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text"  value="' + param_value['productSize'] + '"/></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" ' +
                    '                       maxlength="200" name="product_SKU" type="text" value="' + param_value['productSKU'] + '" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
                    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
                if (count != 1) {
                    htext += '<td><input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + i + ')" /></td>' +
                        '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
                else {
                    htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
            }
    }else {
        if(childSkulist.length < 1) {
            count = 1;
            htext += '<tr id="1" class="tr1" style="height: 30px;"><td><label id="id_color_name" class="control-label requiredField">\n' +
    '                        颜色名<span class="asteriskField">*</span></label></td>\n' +
    '                    <td><input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text" /></td>\n' +
    '                    <td><label id="id_size_name" class="control-label requiredField">尺寸名<span class="asteriskField">*</span></label></td>\n' +
    '                    <td><input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" type="text" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
            htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
        }else {
            for (var i = 0; i < childSkulist.length; i++) {
                var param_value = childSkulist[i];
                var count = i + 1;
                htext += '<tr id="'+count+'" class="tr1" style="height: 30px;"><td><label id="id_color_name" class="control-label requiredField">\n' +
                    '                        颜色名<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text" /></td>\n' +
                    '                    <td><label id="id_size_name" class="control-label requiredField">尺寸名<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text"  value="' + param_value['productSize'] + '"/></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" ' +
                    '                       maxlength="200" name="product_SKU" type="text" value="' + param_value['productSKU'] + '" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
                    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
                if (i != 0) {
                    htext += '<td><input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + i + ')" /></td>' +
                        '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
                else {
                    htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
            }
        }
    }

    htext += '</table>';
    document.getElementById("div_id_MetalType_color").innerHTML = ''
    document.getElementById("div_id_size_MetalType").innerHTML = ''
    document.getElementById("div_id_MetalType").innerHTML = ''
    document.getElementById("div_id_size_name").innerHTML = ''
    document.getElementById("div_id_color_name").innerHTML = ''
    document.getElementById("div_id_size_color").innerHTML = htext;
}

function show_first_MetalType_div(childSkulist) {
    var htext = '<table id="mytable" class="border1">';
    var product_variation_count = 0;
    if(product_variations.length>0) {
        product_variation_count = product_variations.length;
        htext += show_old_variation();
        for (var i = 0; i < childSkulist.length; i++) {
                var param_value = childSkulist[i];
                var count = i + 1 + product_variation_count;
                htext += '<tr id="'+count+'" class="tr1" style="height: 30px;"><td><label id="id_MetalType" class="control-label requiredField">\n' +
                    '                        材 料<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" ' +
                    '                       maxlength="200" name="product_SKU" type="text" value="' + param_value['productSKU'] + '" onblur="check_sku_tortInfo(this.id,this.value)" /></td><td><label id="id_size_name" class="control-label requiredField">' +
                    '                   价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
                    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
                if (count != 1) {
                    htext += '<td><input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + i + ')" /></td>' +
                        '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
                else {
                    htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
            }
    }else {
        if(childSkulist.length < 1) {
            count = 1;
            htext += '<tr id="1" class="tr1" style="height: 30px;"><td><label id="id_MetalType" class="control-label requiredField">\n' +
    '                        材 料<span class="asteriskField">*</span></label></td>\n' +
    '                    <td><input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" ' +
                '           maxlength="200" name="product_SKU" type="text" onblur="check_sku_tortInfo(this.id,this.value)" /></td><td><label id="id_size_name" class="control-label requiredField">' +
    '                   价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price" name="variation_price_'+count+'" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
            htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
        }else {
            for (var i = 0; i < childSkulist.length; i++) {
                var param_value = childSkulist[i];
                var count = i + 1;
                htext += '<tr id="'+count+'" class="tr1" style="height: 30px;"><td><label id="id_MetalType" class="control-label requiredField">\n' +
                    '                        材 料<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" ' +
                    '                       maxlength="200" name="product_SKU" type="text" value="' + param_value['productSKU'] + '" onblur="check_sku_tortInfo(this.id,this.value)" /></td><td><label id="id_size_name" class="control-label requiredField">' +
                    '                   价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
                    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
                if (i != 0) {
                    htext += '<td><input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + i + ')" /></td>' +
                        '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
                else {
                    htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
            }
        }
    }

    htext += '</table>';
    document.getElementById("div_id_size_color").innerHTML = ''
    document.getElementById("div_id_size_name").innerHTML = ''
    document.getElementById("div_id_color_name").innerHTML = ''
    document.getElementById("div_id_MetalType_color").innerHTML = ''
    document.getElementById("div_id_size_MetalType").innerHTML = ''
    document.getElementById("div_id_MetalType").innerHTML = htext;
}

function show_first_size_MetalType(childSkulist) {
    var htext = '<table id="mytable" class="border1">';
    var product_variation_count = 0;
    if(product_variations.length>0) {
        product_variation_count = product_variations.length;
        htext += show_old_variation();
        for (var i = 0; i < childSkulist.length; i++) {
                var param_value = childSkulist[i];
                var count = i + 1 + product_variation_count;
                htext += '<tr id="'+count+'" class="tr1" style="height: 30px;"><td><label id="id_MetalType" class="control-label requiredField">\n' +
                    '                        材 料<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" /></td>\n' +
                    '                    <td><label id="id_size_name" class="control-label requiredField">尺寸名<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text"  value="' + param_value['productSize'] + '"/></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" ' +
                    '                       maxlength="200" name="product_SKU" type="text" value="' + param_value['productSKU'] + '" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
                    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
                if (count != 1) {
                    htext += '<td><input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + i + ')" /></td>' +
                        '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
                else {
                    htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
            }
    }else {
        if(childSkulist.length < 1) {
            count = 1;
            htext += '<tr id="1" class="tr1" style="height: 30px;"><td><label id="id_MetalType" class="control-label requiredField">\n' +
    '                        材 料<span class="asteriskField">*</span></label></td>\n' +
    '                    <td><input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" /></td>\n' +
    '                    <td><label id="id_size_name" class="control-label requiredField">尺寸名<span class="asteriskField">*</span></label></td>\n' +
    '                    <td><input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" type="text" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
            htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
        }else {
            for (var i = 0; i < childSkulist.length; i++) {
                var param_value = childSkulist[i];
                var count = i + 1;
                htext += '<tr id="'+count+'" class="tr1" style="height: 30px;"><td><label id="id_MetalType" class="control-label requiredField">\n' +
                    '                        材 料<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" /></td>\n' +
                    '                    <td><label id="id_size_name" class="control-label requiredField">尺寸名<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text"  value="' + param_value['productSize'] + '"/></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" ' +
                    '                       maxlength="200" name="product_SKU" type="text" value="' + param_value['productSKU'] + '" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
                    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
                if (i != 0) {
                    htext += '<td><input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + i + ')" /></td>' +
                        '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
                else {
                    htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
            }
        }
    }

    htext += '</table>';
    document.getElementById("div_id_MetalType").innerHTML = ''
    document.getElementById("div_id_size_color").innerHTML = ''
    document.getElementById("div_id_size_name").innerHTML = ''
    document.getElementById("div_id_color_name").innerHTML = ''
    document.getElementById("div_id_MetalType_color").innerHTML = ''
    document.getElementById("div_id_size_MetalType").innerHTML = htext;
}

function show_first_MetalType_color(childSkulist) {
    var htext = '<table id="mytable" class="border1">';
    var product_variation_count = 0;
    if(product_variations.length>0) {
        product_variation_count = product_variations.length;
        htext += show_old_variation();
        for (var i = 0; i < childSkulist.length; i++) {
                var param_value = childSkulist[i];
                var count = i + 1 + product_variation_count;
                htext += '<tr id="'+count+'" class="tr1" style="height: 30px;"><td><label id="id_color_name" class="control-label requiredField">\n' +
                    '                        颜色名<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text" /></td>\n' +
                    '                    <td><label id="id_MetalType" class="control-label requiredField">材 料<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" ' +
                    '                       type="text" value="' + param_value['productSKU'] + '" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
                    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
                if (count != 1) {
                    htext += '<td><input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + i + ')" /></td>' +
                        '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
                else {
                    htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
            }
    }else {
        if(childSkulist.length < 1) {
            count = 1;
            htext += '<tr id="1" class="tr1" style="height: 30px;"><td><label id="id_color_name" class="control-label requiredField">\n' +
    '                        颜色名<span class="asteriskField">*</span></label></td>\n' +
    '                    <td><input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text" /></td>\n' +
    '                    <td><label id="id_MetalType" class="control-label requiredField">材 料<span class="asteriskField">*</span></label></td>\n' +
    '                    <td><input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" type="text" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
            htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
        }else {
            for (var i = 0; i < childSkulist.length; i++) {
                var param_value = childSkulist[i];
                var count = i + 1;
                htext += '<tr id="'+count+'" class="tr1" style="height: 30px;"><td><label id="id_color_name" class="control-label requiredField">\n' +
                    '                        颜色名<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text" /></td>\n' +
                    '                    <td><label id="id_MetalType" class="control-label requiredField">材 料<span class="asteriskField">*</span></label></td>\n' +
                    '                    <td><input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label></td><td><input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" ' +
                    '                       type="text" value="' + param_value['productSKU'] + '" onblur="check_sku_tortInfo(this.id,this.value)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" /></td>' +
                    '                   <td><label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label></td><td><input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" /></td>' +
                    '                   <td><input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" /><input type="hidden" id="id_image_' + count + '" name="variation_images" value="" /></td>';
                if (count != 1) {
                    htext += '<td><input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + i + ')" /></td>' +
                        '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
                else {
                    htext += '<td><input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" /></td>' +
                        '<td><input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" /></td></tr>';
                }
            }
        }
    }

    htext += '</table>';
    document.getElementById("div_id_MetalType").innerHTML = ''
    document.getElementById("div_id_size_MetalType").innerHTML = ''
    document.getElementById("div_id_size_color").innerHTML = ''
    document.getElementById("div_id_size_name").innerHTML = ''
    document.getElementById("div_id_color_name").innerHTML = ''
    document.getElementById("div_id_MetalType_color").innerHTML = htext;
}

function add_table_tr(new_childSkulist) {
    var displayFlag1 = document.getElementById("div_id_size_name").style.display;
    var displayFlag2 = document.getElementById("div_id_color_name").style.display;
    var displayFlag3 = document.getElementById("div_id_size_color").style.display;
    var displayFlag4 = document.getElementById("div_id_MetalType").style.display;
    var displayFlag5 = document.getElementById("div_id_size_MetalType").style.display;
    var displayFlag6 = document.getElementById("div_id_MetalType_color").style.display;
    var tableI = document.getElementById("mytable");
    var tab = document.getElementById("mytable");
    //表格行数
    var rows = tab.rows.length ;
    var last_id = $("#mytable").find("tr:last").attr('id');
    console.log(last_id);
    if(last_id){
        rows = parseInt(last_id);
    }else {
        rows = 0;
    }
    var count = rows + 1;
    for(var i = 0; i < new_childSkulist.length; i++) {
        var newTr = tableI.insertRow(-1);
        newTr.setAttribute('id',count);
        var param_value = new_childSkulist[i];
        if (displayFlag1 != "none") {
            var imgTD = newTr.insertCell(0);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">尺寸名<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(1);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text" value="'+param_value['productSize']+'"/>';
            var imgTD = newTr.insertCell(2);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(3);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" type="text" value="'+param_value['productSKU']+'" onblur="check_sku_tortInfo(this.id,this.value)" />';
            var imgTD = newTr.insertCell(4);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(5);
            imgTD.innerHTML = '<input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" />';
            var imgTD = newTr.insertCell(6);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(7);
            imgTD.innerHTML = '<input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" />';
            var imgTD = newTr.insertCell(8);
            imgTD.innerHTML = '<input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" />' +
                '<input type="hidden" id="id_image_' + count + '" name="variation_images" value="" />';
            var imgTD = newTr.insertCell(9);
            imgTD.innerHTML = '<input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + rows + ')" />';
            var imgTD = newTr.insertCell(10);
            imgTD.innerHTML = '<input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" />';
            var imgTD = newTr.insertCell(11);
            imgTD.innerHTML = '<input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" />';
        }
        if (displayFlag2 != "none") {
            var imgTD = newTr.insertCell(0);
            imgTD.innerHTML = '<label id="id_color_name" class="control-label requiredField">颜色名<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(1);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text" />';
            var imgTD = newTr.insertCell(2);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(3);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" type="text" value="'+param_value['productSKU']+'" onblur="check_sku_tortInfo(this.id,this.value)" />';
            var imgTD = newTr.insertCell(4);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(5);
            imgTD.innerHTML = '<input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" />';
            var imgTD = newTr.insertCell(6);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(7);
            imgTD.innerHTML = '<input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" />';
            var imgTD = newTr.insertCell(8);
            imgTD.innerHTML = '<input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" />' +
                '<input type="hidden" id="id_image_' + count + '" name="variation_images" value="" />';
            var imgTD = newTr.insertCell(9);
            imgTD.innerHTML = '<input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + rows + ')" />';
            var imgTD = newTr.insertCell(10);
            imgTD.innerHTML = '<input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" />';
            var imgTD = newTr.insertCell(11);
            imgTD.innerHTML = '<input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" />';
        }
        if (displayFlag3 != "none") {
            var imgTD = newTr.insertCell(0);
            imgTD.innerHTML = '<label id="id_color_name" class="control-label requiredField">颜色名<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(1);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text" />';
            var imgTD = newTr.insertCell(2);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">尺寸名<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(3);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text" value="'+param_value['productSize']+'"/>';
            var imgTD = newTr.insertCell(4);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(5);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" type="text" value="'+param_value['productSKU']+'" onblur="check_sku_tortInfo(this.id,this.value)" />';
            var imgTD = newTr.insertCell(6);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(7);
            imgTD.innerHTML = '<input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" />';
            var imgTD = newTr.insertCell(8);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(9);
            imgTD.innerHTML = '<input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" />';
            var imgTD = newTr.insertCell(10);
            imgTD.innerHTML = '<input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" />' +
                '<input type="hidden" id="id_image_' + count + '" name="variation_images" value="" />';
            var imgTD = newTr.insertCell(11);
            imgTD.innerHTML = '<input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + rows + ')" />';
            var imgTD = newTr.insertCell(12);
            imgTD.innerHTML = '<input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" />';
            var imgTD = newTr.insertCell(13);
            imgTD.innerHTML = '<input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" />';
        }
        if (displayFlag4 != "none") {
            var imgTD = newTr.insertCell(0);
            imgTD.innerHTML = '<label id="id_MetalType" class="control-label requiredField">材 料<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(1);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" />';
            var imgTD = newTr.insertCell(2);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(3);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" type="text" value="'+param_value['productSKU']+'" onblur="check_sku_tortInfo(this.id,this.value)" />';
            var imgTD = newTr.insertCell(4);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(5);
            imgTD.innerHTML = '<input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" />';
            var imgTD = newTr.insertCell(6);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(7);
            imgTD.innerHTML = '<input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" />';
            var imgTD = newTr.insertCell(8);
            imgTD.innerHTML = '<input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" />' +
                '<input type="hidden" id="id_image_' + count + '" name="variation_images" value="" />';
            var imgTD = newTr.insertCell(9);
            imgTD.innerHTML = '<input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + rows + ')" />';
            var imgTD = newTr.insertCell(10);
            imgTD.innerHTML = '<input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" />';
            var imgTD = newTr.insertCell(11);
            imgTD.innerHTML = '<input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" />';
        }
        if (displayFlag5 != "none") {
            var imgTD = newTr.insertCell(0);
            imgTD.innerHTML = '<label id="id_MetalType" class="control-label requiredField">材 料<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(1);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" />';
            var imgTD = newTr.insertCell(2);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">尺寸名<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(3);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_size_name_'+count+'" maxlength="32" name="size_name" type="text" value="'+param_value['productSize']+'"/>';
            var imgTD = newTr.insertCell(4);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(5);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" type="text" value="'+param_value['productSKU']+'" onblur="check_sku_tortInfo(this.id,this.value)" />';
            var imgTD = newTr.insertCell(6);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(7);
            imgTD.innerHTML = '<input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" />';
            var imgTD = newTr.insertCell(8);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(9);
            imgTD.innerHTML = '<input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" />';
            var imgTD = newTr.insertCell(10);
            imgTD.innerHTML = '<input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" />' +
                '<input type="hidden" id="id_image_' + count + '" name="variation_images" value="" />';
            var imgTD = newTr.insertCell(11);
            imgTD.innerHTML = '<input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + rows + ')" />';
            var imgTD = newTr.insertCell(12);
            imgTD.innerHTML = '<input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" />';
            var imgTD = newTr.insertCell(13);
            imgTD.innerHTML = '<input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" />';
        }
        if (displayFlag6 != "none") {
            var imgTD = newTr.insertCell(0);
            imgTD.innerHTML = '<label id="id_color_name" class="control-label requiredField">颜色名<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(1);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_color_name_'+count+'" maxlength="32" name="color_name" type="text" />';
            var imgTD = newTr.insertCell(2);
            imgTD.innerHTML = '<label id="id_MetalType" class="control-label requiredField">材 料<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(3);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_MetalType_'+count+'" maxlength="32" name="MetalType" type="text" />';
            var imgTD = newTr.insertCell(4);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">商品SKU<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(5);
            imgTD.innerHTML = '<input class="text-field admintextinputwidget form-control" id="id_product_sku_' + count + '" maxlength="200" name="product_SKU" type="text" value="'+param_value['productSKU']+'" onblur="check_sku_tortInfo(this.id,this.value)" />';
            var imgTD = newTr.insertCell(6);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">价格<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(7);
            imgTD.innerHTML = '<input class="numberinput form-control" id="id_variation_price_'+count+'" name="variation_price" step="0.01" type="number" onkeyup="onlyNonNegative(this)" />';
            var imgTD = newTr.insertCell(8);
            imgTD.innerHTML = '<label id="id_size_name" class="control-label requiredField">包装数<span class="asteriskField">*</span></label>';
            var imgTD = newTr.insertCell(9);
            imgTD.innerHTML = '<input class="numberinput form-control" id="id_item_quantity_'+count+'" name="item_quantity" step="1" type="number" value="1" onkeyup="onlyNumNegative(this)" />';
            var imgTD = newTr.insertCell(10);
            imgTD.innerHTML = '<input type="button" id="add_images_' + count + '" class="btn btn-primary" value="上传图片" onclick="add_images(' + count + ')" />' +
                '<input type="hidden" id="id_image_' + count + '" name="variation_images" value="" />';
            var imgTD = newTr.insertCell(11);
            imgTD.innerHTML = '<input type="button" id="copy_image_' + count + '" class="btn btn-primary" value="同上" onclick="copyIMG(' + rows + ')" />';
            var imgTD = newTr.insertCell(12);
            imgTD.innerHTML = '<input type="button" id="view_image_' + count + '" class="btn btn-primary" value="预览" onclick="viewIMG(' + count + ')" />';
            var imgTD = newTr.insertCell(13);
            imgTD.innerHTML = '<input type="button" id="addItems" class="btn btn-primary" value="删除" onclick="del(this)" />';
        }
        count += 1;
        rows += 1;
    }
}

function add_items() {
    var new_childSkulist = [];
    var productSKU = $('#id_product_main_sku').val();

    if(productSKU) {
        var url = "/Project/admin/skuapp/t_templet_amazon_collection_box/get_childSKU_by_mainSKU/?productSKU=" + productSKU;
        $.getJSON(url, function(result){
            if (result.code == '1'){
                // console.log(result.data);
                new_childSkulist = result.data;
                if(childSkulist.length == 0) {
                    childSkulist = result.data;
                }else {
                    childSkulist = childSkulist.concat(new_childSkulist);
                }
                // console.log('aaaaaaa:'+childSkulist);
                // console.log('bbbbbbbb:'+new_childSkulist);
                add_table_tr(new_childSkulist);
                if(document.getElementById("addItems_tort")){
                    $('#addItems_tort').html('');
                }
            }else if (result.code == '0'){
                if(document.getElementById("addItems_tort")){
                    if(document.getElementById("addItems_tort").innerText == ''){
                        $('#addItems_tort').html('该商品SKU在Amazon存在侵权记录');
                    }
                }else {
                    $('#addItems').after('<span id="addItems_tort" style="color: red">该商品SKU在Amazon存在侵权记录</span>');
                    console.log(result.tort_list);
                }
            }else {
                alert('异常:'+result.errortext);
            }
        });
    }else {
        new_childSkulist = [{"productSKU": "", "productSize": ""}];
        add_table_tr(new_childSkulist);
        if(document.getElementById("addItems_tort")){
            $('#addItems_tort').html('');
        }
    }
}

function check_sku_tortInfo(id,sku) {
    if(sku) {
        var url = "/Project/admin/skuapp/t_templet_amazon_collection_box/check_sku_tortinfo/?productSKU=" + sku;
        $.getJSON(url, function(result){
            if (result.code == '1'){
                if(result.data == '-1') {
                    if(document.getElementById(id+"_tort")){
                        if(document.getElementById(id+"_tort").innerText == ''){
                            $('#'+id+'_tort').html('侵权');
                        }
                    }else {
                        $('#' + id).after('<span id="'+id+'_tort" style="color: red">侵权</span>');
                        console.log(result.tort_list);
                    }
                }else {
                    if(document.getElementById(id+"_tort")){
                        $('#'+id+'_tort').html('');
                    }
                }
            }else {
                alert('异常:'+result.errortext);
            }
        });
    }else {
        if(document.getElementById(id+"_tort")){
            $('#'+id+'_tort').html('');
        }
    }

}

function onlyNonNegative(obj) {
    obj.value = obj.value.replace(/[^\d.]/g,"");  //清除“数字”和“.”以外的字符
    obj.value = obj.value.replace(/\.{2,}/g,"."); //只保留第一个. 清除多余的
    obj.value = obj.value.replace(".","$#$").replace(/\./g,"").replace("$#$",".");
    obj.value = obj.value.replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3');//只能输入两个小数
    if(obj.value.indexOf(".")< 0 && obj.value !=""){//以上已经过滤，此处控制的是如果没有小数点，首位不能为类似于 01、02的金额
        obj.value= parseFloat(obj.value);
    }
    console.log(obj.value);
}

function onlyNumNegative(obj) {
    obj.value = obj.value.replace(/[^\d]/g,"");  //清除“数字”和“.”以外的字符
    if(obj.value !=""){//以上已经过滤，此处控制的是如果没有小数点，首位不能为类似于 01、02的金额
        obj.value= parseFloat(obj.value);
    }
}