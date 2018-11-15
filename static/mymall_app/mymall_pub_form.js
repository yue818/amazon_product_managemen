

$(document).ready(function() {
    get_ePic()

    // var save_ = document.getElementById("save");
    // alert('id=='+save_.id);
    // save_.onclick = function() {b1(id);};
});
//
// function b1(id) {
//     alert('id=='+id);
// }



function to_del(obj) {
    var tableI = document.getElementById("VariantInfo");//找到要删除行所在的table
    var trI = obj.parentNode.parentNode;//我的button在tr下的td中，两次执行.parentNode操作，可以找到要删除的tr。

    var index = trI.rowIndex;//要删除的tr所在table中的index
    tableI.deleteRow(index);//执行删除
    get_ePic();
}

function add_Variant(data) {
    var Vv_num = document.getElementsByName('productsku').length;

    var tableI = document.getElementById("VariantInfo");
    var newTr = tableI.insertRow(-1);

    var obj = JSON.parse(data);

    var imgTD = newTr.insertCell(0);
    imgTD.innerHTML = '<img id="id_vPic_' + (Vv_num + 1) + '" src="http://ou3qh0g46.bkt.clouddn.com/fancyqube.jpg"'+
                     ' width="35" height="35"'+
                     ' alt = "http://ou3qh0g46.bkt.clouddn.com/fancyqube.jpg"'+
                     ' title="http://ou3qh0g46.bkt.clouddn.com/fancyqube.jpg"' +
                     ' data-toggle="modal" data-target="#upload_image" onclick="change_vPic(\'v_' + (Vv_num + 1) + '\')"/>' +
                     '<input type="hidden" value="" name="vPic" id="vPic_' + (Vv_num + 1) + '">';

    var imgTD = newTr.insertCell(1);
    imgTD.innerHTML = '<input type="text" value="'+ obj._productsku +'" name="productsku">';

    var imgTD = newTr.insertCell(2);
    imgTD.innerHTML = '<input type="text" value="'+ obj._shopsku +'" name="shopsku"' + ' onkeyup="this.value=this.value.replace(/[\\r\\n\\t\\ ]/g, \'\')"' + ' >';

    var imgTD = newTr.insertCell(3);
    imgTD.innerHTML = '<input type="text" value="'+ obj._size +'" name="size">';

    var imgTD = newTr.insertCell(4);
    imgTD.innerHTML = '<input type="text" value="'+ obj._color +'" name="color">';

    var imgTD = newTr.insertCell(5);
    imgTD.innerHTML = '<input type="text" value="'+ obj._msrp +'" name="msrp"' + ' onblur="checknum(this.value)" onkeyup="this.value=this.value.replace(/[\\r\\n\\t\\ ]/g, \'\')"' + ' >';

    var imgTD = newTr.insertCell(6);
    imgTD.innerHTML = '<input type="text" value="'+ obj._price +'" name="price"' + ' onblur="checknum(this.value)" onkeyup="this.value=this.value.replace(/[\\r\\n\\t\\ ]/g, \'\')"' + ' >';

    var imgTD = newTr.insertCell(7);
    imgTD.innerHTML = '<input type="text" value="'+ obj._kc +'" name="kc"' + ' onblur="checknum(this.value)" onkeyup="this.value=this.value.replace(/[\\r\\n\\t\\.\\ ]/g, \'\')"' + ' >';

    var imgTD = newTr.insertCell(8);
    imgTD.innerHTML = '<input type="text" value="'+ obj._shipping +'" name="shipping"' + ' onblur="checknum(this.value)" onkeyup="this.value=this.value.replace(/[\\r\\n\\t\\ ]/g, \'\')"' + ' >';

    var imgTD = newTr.insertCell(9);
    imgTD.innerHTML = '<input type="text" value="'+ obj._shippingtime +'" name="shippingtime">';

    var imgTD = newTr.insertCell(10);
    imgTD.innerHTML = '<input type="button" class="btn btn-default" value="移除" name="delone" onclick="to_del(this)">';

}

function add_V() {
    var VData = {};
    VData['_productsku'] = '';
    VData['_shopsku'] = '';
    VData['_size'] = '';
    VData['_color'] = '';
    VData['_msrp'] = '';
    VData['_price'] = '';
    VData['_kc'] = '';
    VData['_shipping'] = '';
    VData['_shippingtime'] = '';
    add_Variant(JSON.stringify(VData));
    get_ePic();
}

// 按照主SKU生成变体
function get_Variant() {
    var msrp = document.getElementById("id_MSRP");
    var price = document.getElementById("id_Price");
    var shipping = document.getElementById("id_Shipping");
    var shippingTime = document.getElementById("id_ShippingTime");
    var kc = document.getElementById("id_KC");
    var mainsku = document.getElementById("id_MainSKU");

    if (mainsku.value != ''){
        $.getJSON('/mymallapp/get_all_productsku/?mainsku='+mainsku.value, function(result){
            if (result.resultCode == '0'){
                var sku_list = result.skuresult;
                for (var i=0; i<sku_list.length;i++){
                    var VData = {};
                    VData['_productsku'] = sku_list[i];
                    VData['_shopsku'] = '';
                    VData['_size'] = '';
                    VData['_color'] = '';
                    VData['_msrp'] = msrp.value;
                    VData['_price'] = price.value;
                    VData['_kc'] = kc.value;
                    VData['_shipping'] = shipping.value;
                    VData['_shippingtime'] = shippingTime.value;
                    add_Variant(JSON.stringify(VData));
                }
                get_ePic();
            }else {
                alert('处理异常，请联系it人员处理。');
            }
        });
    }else {
        alert('请填写主SKU。');
    }
}

function getShopSKU() {
    var obj = document.getElementById("id_ShopName");
    var index = obj.selectedIndex;
    var shopname = obj.options[index].text;

    var ss_obj = document.getElementsByName('shopsku');
    var productsku_obj = document.getElementsByName('productsku');
    var num = ss_obj.length;
    var proskus = ''
    for (var i=0;i<num;i++) {
        proskus = proskus + ',' + productsku_obj[i].value
    }
    if (shopname){
        $.getJSON('/mymallapp/get_shopsku/?shopname='+shopname+'&num='+num+'&productskus='+proskus, function(result){
            if (result.resultCode == '0'){
                // var shopsku_str = JSON.stringify(result.skuresult);
                // alert(shopsku_str);
                // return result.skuresult;
                for (var ss=0;ss<num;ss++){
                    pro_sku = productsku_obj[ss].value
                    ss_obj[ss].value=result.skuresult[pro_sku];
                }
            }else {
                alert('生成店铺SKU异常，请联系it人员处理。');
            }
        });
    }else {
        alert('请选择店铺名称。。');
    }
}


function get_ePic() {
    // 变体数量
    var V_num = document.getElementsByName('productsku').length;

    var eP_num = document.getElementsByName('ePic').length;
    // for (var eP=1;eP<=20;eP++){
    //     if (document.getElementsByName('ePic_'){
    //         eP_num ++;
    //     }
    // }
    // alert('eP_num='+eP_num);
    if (V_num>=20){
        del_ePic(eP_num,0)
    } else if (V_num+eP_num>20){
        var cNum = V_num+eP_num-20;// 这是附图多出来的
        del_ePic(eP_num,eP_num-cNum)
    } else if (V_num+eP_num<20){
        var c_Num = 20-(V_num+eP_num);// 这是附图少的数量
        var Div_add = document.getElementById('div_id_ePic_'+eP_num.toString());
        var node=Div_add.nextSibling;
        for (var n=eP_num+1;n<=(20-V_num);n++){
            var m = n.toString();
            var oDiv = document.createElement('div');
            oDiv.id = "div_id_ePic_"+ m;
            oDiv.className = "form-group col-sm-1";
            oDiv.innerHTML = '<label for="id_ePic'+ m +'" class="control-label " style="float:left;width: 120px;padding-top: 22px !important;text-align: right">'+
                            '附图'+ m +'<span class="asteriskField">*</span>'+
                            '</label>'+
                            '<div class="controls " style="float:left;">'+
                                '<img id="id_ePic_'+ m +'" src="http://ou3qh0g46.bkt.clouddn.com/fancyqube.jpg"' +
                                ' width="120" height="120"' +
                                ' alt = "http://ou3qh0g46.bkt.clouddn.com/fancyqube.jpg"' +
                                ' title="http://ou3qh0g46.bkt.clouddn.com/fancyqube.jpg"' +
                                ' data-toggle="modal" data-target="#upload_image" onclick="change_vPic(\'e_'+ m +'\')"/>'+
                                '<input type="hidden" value="" name="ePic" id="ePic_'+ m +'">'+
                            '</div>';
            Div_add.parentNode.insertBefore(oDiv, node);
            Div_add = document.getElementById('div_id_ePic_'+m);
            node=Div_add.nextSibling;
        }
    }
}

function del_ePic(num,t_num) {
    for (var d=num;d>t_num;d--){
        // alert('d===='+d.toString());
        var dP_Div = document.getElementById('div_id_ePic_'+d.toString());
        dP_Div.parentNode.removeChild(dP_Div);
    }
}

function change_vPic(num) {
    // alert('----'+num);
    $("#modal_hidden_id").val(num);
}

function upload_Img() {
    // alert('0000000000');
    var imgFlagTmp = document.getElementById('modal_hidden_id');
    var ImgFlag = imgFlagTmp.value;

    var fileObj = document.getElementById("id_upload_img").files[0]; // js 获取文件对象
    if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
       alert("请选择图片");
       return;
    }
    var obj = document.getElementById("id_ShopName");
    var index = obj.selectedIndex;
    var shopname = obj.options[index].text;

    if (shopname) {
        // alert('111111111');
        var formFile = new FormData();
        formFile.append("action", "/mymallapp/mymall_pub_save_image/?imageflag="+ImgFlag+'&shopname='+shopname);
        formFile.append("PIC", fileObj); //加入文件对象

        //第一种  XMLHttpRequest 对象
        //var xhr = new XMLHttpRequest();
        //xhr.open("post", "/Admin/Ajax/VMKHandler.ashx", true);
        //xhr.onload = function () {
        //    alert("上传完成!");
        //};
        //xhr.send(formFile);

        //第二种 ajax 提交

        var data = formFile;
        $.ajax({
           url: "/mymallapp/mymall_pub_save_image/?imageflag="+ImgFlag+'&shopname='+shopname,
           data: data,
           type: "Post",
           dataType: "json",
           cache: false,//上传文件无需缓存
           processData: false,//用于对data参数进行序列化处理 这里必须false
           contentType: false, //必须
           success: function (result) {
                if (result.Code == '0'){
                    // alert("===="+result.PicPath);
                    var picTmp = {};
                    if(ImgFlag=='0'){ //主图上传
                        picTmp = document.getElementById('id_Pic_0');
                        $("#id_MainPic").val(result.PicPath);
                    }else if (ImgFlag.indexOf('v_') == 0){ //变体图
                        var vIdx = ImgFlag.split('_')[1];
                        picTmp = document.getElementById('id_vPic_'+vIdx);
                        $("#vPic_"+vIdx).val(result.PicPath);
                    }else if (ImgFlag.indexOf('e_') == 0){ //附图
                        var eIdx = ImgFlag.split('_')[1];
                        picTmp = document.getElementById('id_ePic_'+eIdx);
                        $("#ePic_"+eIdx).val(result.PicPath);
                    }
                    if (picTmp){
                        picTmp.src = result.PicPath;
                        picTmp.alt = result.PicPath;
                        picTmp.title = result.PicPath;
                    }
                    $('#upload_image').modal('hide')
                }else {
                    alert(result.PicPath);
                }
           },
           error:function (XMLHttpRequest, textStatus, errorThrown) {
               alert('错误信息：' + XMLHttpRequest.responseText); //获取的信息即是异常中的Message
           }
        });
        cleanFile();
    }else{
        alert('请选择店铺名称。。')
    }
}

function cleanFile() {
    var file = document.getElementById("id_upload_img");
    // for IE, Opera, Safari, Chrome
    if (file.outerHTML) {
        file.outerHTML = file.outerHTML;
    } else { // FF(包括3.5)
        file.value = "";
    }
}













