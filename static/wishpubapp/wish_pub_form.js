var colorlist = new Array();
var delshopskulsit = new Array();
var info = '';

$(document).ready(function() {
    var saveobj = document.getElementsByName('_save');
    for (var s=0;s<saveobj.length;s++){
        saveobj[s].type = 'button';
        saveobj[s].setAttribute('onclick','pub_to_submit("_save")');
    }

    var save_anotherobj = document.getElementById('save_and_another');
    save_anotherobj.type = 'button';
    save_anotherobj.setAttribute('onclick','pub_to_submit("_addanother")');
    var save_editobj = document.getElementById('save_and_editing');
    save_editobj.type = 'button';
    save_editobj.setAttribute('onclick','pub_to_submit("_continue")');

    var formobj = document.getElementById('t_templet_wish_publish_draft_form');
    formobj.setAttribute('autocomplete', 'off');

    // $('#id_tags_input').keyup(function(event) {
    // 　　if (event.keyCode == "13") {
    // 　　　　confirm_tags();
    // 　　}
    // });
    refresh_table();
    get_ePic();   // 刷新图片的删除按钮，并计算图片个数
    color_list();  // 计算color列表，计算增加color的下拉框选项

    $('#id_ShopName').attr('onchange', 'clearShopSKU(this)');
});

function refresh_table() {
    $("#VariantInfo").tableDnD({
        onDragClass: 'success',
        // onDrop:function(table,row){
        //   console.log('------');
        // }
    });
}

function color_list() {
    var selobjs = document.getElementsByName('colorlist');
    for (var i=0,j=selobjs.length;i<j;i++){
        colorlist.push(titleCase($.trim(selobjs[i].value)));
        info += '<div class="panel-body div_item" onmousemove="new_color(this)" onmouseout="old_color(this)" onClick="onChangeText(this);">'+ selobjs[i].value +'</div>';
    }
}

function change_color(self) {
    var itext = $.trim(self.value);
    var div_list = self.nextElementSibling;
    if (itext != "") {
        var html = "";
        for (var i = 0,j = colorlist.length; i < j; i++) {
            if (colorlist[i].toLowerCase().indexOf(itext.toLowerCase()) >= 0) {
                html += '<div class="panel-body div_item" onmousemove="new_color(this)" onmouseout="old_color(this)" onClick="onChangeText(this);">'+ colorlist[i] +'</div>';
            }
        }
        if (html != "") {
            $("#" + div_list.id).show().html(html);
        } else {
            $("#" + div_list.id).hide().html("");
        }
    }else {
        $("#" + div_list.id).show().html(info);
    }
}

 //移入移出效果
function new_color(obj) {
    $(obj).css('background-color', '#1C86EE').css('color', 'white');
}

function old_color(obj) {
    $(obj).css('background-color', 'white').css('color', 'black');
}

$("body").click(function () {
    $(".div_Color").css('display', 'none');
});

//弹出列表框
// $("#q").click(function () {
//     $("#div_items").css('display', 'block');
//     return false;
// });

// function show_all_color(self) {
//     var div_list = self.nextElementSibling;
//     $("#" + div_list.id).show().html(info);
// }

//项点击
function onChangeText(obj) {
    var value = $(obj).text();
    var ids = (obj.parentNode.id).split('_')[2];
    $("#id_color_"+ids).attr('value',value);
    $("#color_div_"+ids).show().html('<div class="panel-body div_item" onmousemove="new_color(this)" onmouseout="old_color(this)" onClick="onChangeText(this);">'+ value +'</div>');
}

// 小红点
function delete_flag() {
    $(".thumbnail").mouseenter(function () {
        $(this).find(".delete").show();

    });

    $(".thumbnail").mouseleave(function () {
        $(this).find(".delete").hide();
    });
}

//行删除
function to_del(obj) {
    var btn = $(obj).button('loading');

    var tableI = document.getElementById("VariantInfo");//找到要删除行所在的table
    var trI = obj.parentNode.parentNode;//我的button在tr下的td中，两次执行.parentNode操作，可以找到要删除的tr。

    var index = trI.rowIndex;//要删除的tr所在table中的index
    tableI.deleteRow(index);//执行删除
    get_ePic();

    refresh_table();
    setTimeout(function () { btn.button('reset'); },500);
}

// 增加
function add_Variant(data) {
    var Vv_num = document.getElementsByName('productsku').length;

    var tableI = document.getElementById("VariantInfo");

    var tnum = document.getElementsByName("color").length;

    var newTr = tableI.insertRow(-1);
    newTr.setAttribute('id', parseInt(tnum) + 1);

    var obj = JSON.parse(data);

    newTr.insertCell(0).innerHTML = '<div class="dropdown">' +
        '<a class="thumbnail dropdown-toggle" style="position: absolute; margin-left: 2px;" ondragstart="return false;" data-toggle="dropdown">' +
        '<img src="https://fancyqube-wish.oss-cn-shanghai.aliyuncs.com/Nobackground.png"' +
        ' id="id_vImg_' + (Vv_num + 1) + '_Show" width="30" height="30" class="img">' +
        '<input type="hidden" value="" name="v_Pic" id="id_vImg_' + (Vv_num + 1) + '">' +
        '</a>' +
        '<input type="file" id="id_vImg_up_' + (Vv_num + 1) + '" onchange="upload_Img(this,\'id_vImg_' + (Vv_num + 1) + '\');" style="display:none;" value="" ' +
        'accept="image/gif, image/jpeg, image/png, image/gif ">' +
        '<ul class="dropdown-menu">' +
        '<li><a onclick="javascrip:$(\'#id_vImg_up_'+(Vv_num + 1)+'\').click();">上传本地图</a></li>' +
        '<li><a onclick="webimgSelect(\'id_vImg_' + (Vv_num + 1) + '\');">选择网络图</a></li>' +
        '<li><a onclick="imgdelete(\'id_vImg_' + (Vv_num + 1) + '\');">删除图片</a></li>' +
        '</ul></div>';

    newTr.insertCell(1).innerHTML = '<input type="text" class="text-field admintextinputwidget form-control" value="'+ obj._productsku +'" name="productsku" onchange="javascrip:$(this).attr(\'value\',this.value);">';

    newTr.insertCell(2).innerHTML = '<input type="text" class="text-field admintextinputwidget form-control" value="'+ obj._shopsku +'" name="shopsku" onchange="javascrip:$(this).attr(\'value\',this.value);">';

    newTr.insertCell(3).innerHTML = '<input type="text" class="text-field admintextinputwidget form-control" value="'+ obj._size +'" name="size" onchange="javascrip:$(this).attr(\'value\',this.value);">';

    newTr.insertCell(4).innerHTML = '<input type="text" class="text-field admintextinputwidget form-control" value="'+ obj._color +'" name="color" onchange="javascrip:$(this).attr(\'value\',this.value);"' +
        ' id="id_color_'+(Vv_num + 1)+'" onkeyup="change_color(this)" ><div id="color_div_' + (Vv_num + 1) + '" class="panel panel-default div_Color"></div>';

    newTr.insertCell(5).innerHTML = '<input type="text" class="text-field admintextinputwidget form-control" value="'+ obj._msrp +'" name="msrp" onchange="javascrip:$(this).attr(\'value\',this.value);" onkeyup="value=value.replace(/[^\\d.]/g,\'\');">';

    newTr.insertCell(6).innerHTML = '<input type="text" class="text-field admintextinputwidget form-control" value="'+ obj._price +'" name="price" onchange="javascrip:$(this).attr(\'value\',this.value); " onkeyup="value=value.replace(/[^\\d.]/g,\'\'); change_price(this);">';

    newTr.insertCell(7).innerHTML = '<input type="text" class="text-field admintextinputwidget form-control" value="'+ obj._profitrate +'" name="profitrate" onchange="javascrip:$(this).attr(\'value\',this.value); " onkeyup="value=value.replace(/[^\\d.]/g,\'\'); change_profitrate(this);">';

    newTr.insertCell(8).innerHTML = '<input type="text" class="text-field admintextinputwidget form-control" value="'+ obj._kc +'" name="kc" onchange="javascrip:$(this).attr(\'value\',this.value);" onkeyup="value=value.replace(/[^\\d]/g,\'\'); ">';

    newTr.insertCell(9).innerHTML = '<input type="text"  placeholder="请将运费设置为同一值" class="text-field admintextinputwidget form-control" value="'+ obj._shipping +'" name="shipping" onchange="javascrip:$(this).attr(\'value\',this.value); " onkeyup="value=value.replace(/[^\\d.]/g,\'\'); change_price(this);">';

    newTr.insertCell(10).innerHTML = '<input type="text" class="text-field admintextinputwidget form-control" value="'+ obj._shippingtime +'" name="shippingtime" onchange="javascrip:$(this).attr(\'value\',this.value);"  onkeyup="value=value.replace(/[^\\d-]/g,\'\');">';

    newTr.insertCell(11).innerHTML = '<input type="button" class="btn btn-default" value="移除" name="delone" onclick="to_del(this)">';


}

// 增加变体
function add_V(itself) {
    var btn = $(itself).button('loading');

    var VData = {};
    VData['_productsku'] = '';
    VData['_shopsku'] = '';
    VData['_size'] = '';
    VData['_color'] = '';
    VData['_msrp'] = $('#id_MSRP').val();
    VData['_price'] = $('#id_Price').val();
    VData['_profitrate'] = $('#id_MainProfitRate').val();
    VData['_kc'] = $('#id_KC').val();
    VData['_shipping'] = $('#id_Shipping').val();
    VData['_shippingtime'] = $('#id_ShippingTime').val();
    add_Variant(JSON.stringify(VData));
    get_ePic();

    refresh_table();
    setTimeout(function () { btn.button('reset'); },300);
}

// 按照主SKU生成变体
function get_Variant(itself) {
    var btn = $(itself).button('loading');

    var msrp = $('#id_MSRP').val();
    var price = $('#id_Price').val();
    var shipping = $('#id_Shipping').val();
    var shippingTime = $('#id_ShippingTime').val();
    var kc = $('#id_KC').val();
    var mProfitRate = $('#id_MainProfitRate').val();
    var mainsku = $('#id_MainSKU').val();

    var setprice = 0;
    if (mProfitRate == ''){
        if (price != ''){setprice = setprice + parseFloat(price)}
        if (shipping != ''){setprice = setprice + parseFloat(shipping)}
    }
    if(parseInt(setprice) == 0){setprice = '';}
    // console.log(setprice);
    var url = '/get_all_productsku_by_mainsku/?mainsku='+mainsku+'&profitrate='+mProfitRate+'&setprice='+setprice;
    // console.log(url);
    if (mainsku != ''){
        $.getJSON(url, function(result){
            if (result.resultCode == '0'){
                var sku_list = result.skuresult;
                var color_list = result.colorresult;
                var price_list = result.priceresult;
                var rate_list = result.rateresult;
                var size_list = result.sizeresult;
                for (var i=0; i<sku_list.length;i++){
                    var VData = {};
                    VData['_productsku'] = sku_list[i];
                    VData['_shopsku'] = '';
                    VData['_size'] = size_list[i];
                    VData['_color'] = color_list[i];
                    VData['_msrp'] = msrp;

                    if (mProfitRate != ''){
                        if (price_list[i] == ''){
                            VData['_price'] = '';
                            VData['_shipping'] = '';
                        }else {
                            VData['_price'] = (price_list[i]-1).toFixed(2);
                            VData['_shipping'] = 1;   //运费 永远是 1
                        }
                        VData['_profitrate'] = mProfitRate;
                    }else if (mProfitRate == '' && (price != '' || shipping != '')){
                        VData['_price'] = price;
                        VData['_shipping'] = shipping;
                        if (rate_list[i] == ''){
                            VData['_profitrate'] = '';
                        }else {
                            VData['_profitrate'] = rate_list[i].toFixed(2);
                        }
                    }else {
                        VData['_price'] = '';
                        VData['_shipping'] = '';
                        VData['_profitrate'] = '';
                    }

                    VData['_kc'] = kc;
                    VData['_shippingtime'] = shippingTime;
                    add_Variant(JSON.stringify(VData));
                    refresh_table();

                }
                get_ePic();
            }else {
                alert('处理异常，请联系it人员处理。messages:' + result.messages);
                console.log('处理异常，请联系it人员处理。messages:' + result.messages);
            }
        });
    }else {
        alert('请填写主SKU。');
    }

    setTimeout(function () { btn.button('reset'); },1500);
}

// 生成店铺SKU
function getShopSKU(itself) {
    var btn = $(itself).button('loading');

    var obj = document.getElementById("id_ShopName");
    var index = obj.selectedIndex;
    var shopname = obj.options[index].text;

    var ss_obj = document.getElementsByName('shopsku');
    var ps_obj = document.getElementsByName('productsku');
    var ps_list = new Array();
    var psa_list = new Array();
    for (var pi=0;pi<ps_obj.length;pi++){
        if (ss_obj[pi].value == ''){
            if (ps_obj[pi].value != '') {
                ps_list.push($.trim(ps_obj[pi].value));
            }
            psa_list.push($.trim(ps_obj[pi].value));
        }else {
            psa_list.push('');
        }
    }
    if (shopname && ps_list){
        $.getJSON('/get_shopsku/?flag=0&shopname='+shopname+'&sku='+ps_list.join(','), function(result){
            if (result.resultCode == '0'){
                var ashopskulist = new Array();
                for (var ps=0;ps<ps_list.length;ps++){
                    for (var s_key in result.skuresult){
                        if ($.trim(result.skuresult[s_key]) == $.trim(ps_list[ps]) && ashopskulist.indexOf($.trim(s_key)) == -1){
                            var ids = psa_list.indexOf($.trim(ps_list[ps]));
                            if (ids != -1){
                                psa_list.splice(ids,1,'');
                                // ss_obj[ids].value=s_key;
                                ss_obj[ids].setAttribute('value',$.trim(s_key));
                                ss_obj[ids].value = $.trim(s_key);
                                ashopskulist.push($.trim(s_key));
                            }
                        }
                    }
                }
                // 店铺主SKU的生成
                var parentsku_dom = document.getElementById('id_ParentSKU');
                if (!parentsku_dom.value && ashopskulist.length > 0){
                    ashopskulist.sort(function(num1,num2){
                        return num2-num1;
                    });
                    parentsku_dom.setAttribute('value',ashopskulist[0]);
                    parentsku_dom.value = ashopskulist[0];
                }
            }else {
                alert('处理异常，请联系it人员处理。messages:' + result.messages);
                console.log('处理异常，请联系it人员处理。messages:' + result.messages);
            }
        });
    }
    if (!shopname) {
        alert('请选择店铺名称。。');
    }
    if (!ps_list){
        alert('请填写商品SKU。。');
    }
    setTimeout(function () { btn.button('reset'); },1000);
}

// 删除店铺SKU
function clearShopSKU(itself) {
    var btn = $(itself).button('loading');

    var ss_obj = document.getElementsByName('shopsku');
    for (var s=0;s<ss_obj.length;s++){
        if (ss_obj[s].value != ''){
            delshopskulsit.push(ss_obj[s].value);
            ss_obj[s].value = '';
        }
    }
    $('#id_ParentSKU').val('');

    setTimeout(function () { btn.button('reset'); },500);
}


// 刷新图片相关
function get_ePic() {
    delete_flag();
    pic_num('');
}

// 图片上传
function upload_Img(self,f_num,f) {
    f = f || '1';  // 默认为 ’1‘
    var p_num = epic_num() + vpic_num();
    // 图片上传等待
    var i = '';
    var formFile = new FormData();
    var action = "";
    if (f == '1' || f == 'eImg'){  // '1' 表示是 单个文件上传的  主图和变体图
        var fileObj = self.files[0];
        if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
           alert("请选择图片");
           return;
        }
        if (f_num != 'id_MainPic' && f != 'eImg'){
            var selfval = $('#'+f_num).val();
            if ((selfval == '' && p_num + 1 > 20) || (selfval != '' && p_num > 20)){
                alert('选择图片数过多，与已有图 总数超过20，请仔细核对！');
                return
            }
        }
        action = "/wish_pub_save_image/?imageflag="+f_num+'&f=0' ;
        formFile.append("action", action);
        formFile.append("PIC", fileObj); //加入文件对象
    }
    else if (f == 'm'){   // 'm' 表示是 多图片上传 附图上传
        if (self.files.length <= 0){
            return
        }
        if (p_num + self.files.length > 20){
            alert('选择图片数过多，与已有图 总数超过20，请仔细核对！');
            return
        }
        action = "/wish_pub_save_image/?imageflag="+f_num+'&f='+self.files.length ;
        formFile.append("action", action);
        for (var sf=0;sf<self.files.length;sf++){
            formFile.append("PIC_"+sf, self.files[sf]); //加入文件对象
        }
    }

    $.ajax({
        url: action,
        data: formFile,
        type: "Post",
        dataType: "json",
        cache: false,//上传文件无需缓存
        processData: false,//用于对data参数进行序列化处理 这里必须false
        contentType: false, //必须
        beforeSend: function () {
            i = ityzl_SHOW_LOAD_LAYER();
        },
        success: function (result) {
            if (result.Code == '1'){
                if (f == '1' || f == 'eImg'){  //  主图和变体图;  f='eImg' 时： 换附图
                    document.getElementById(f_num+"_Show").src = $.trim(result.PicPath);
                    $("#"+f_num).val($.trim(result.PicPath));
                }
                else if (f == 'm'){   //  附图上传
                    var pardiv = document.getElementById('ePic_All');
                    for (var p=0;p<result.PicPath.length;p++){
                        var poDiv = show_eImg(result.PicPath[p]);
                        pardiv.appendChild(poDiv);
                    }
                }
                ityzl_CLOSE_LOAD_LAYER(i);
                ityzl_SHOW_TIP_LAYER();
                pic_num(f_num);
                console.log(JSON.stringify(result));
            }else {
                alert('错误信息：' + JSON.stringify(result));
                ityzl_CLOSE_LOAD_LAYER(i);
                console.log(JSON.stringify(result));
            }
        },
        error:function (XMLHttpRequest, textStatus, errorThrown) {
            alert('错误信息：' + XMLHttpRequest.responseText); //获取的信息即是异常中的Message
            console.log('错误信息：' + XMLHttpRequest.responseText); //获取的信息即是异常中的Message
            ityzl_CLOSE_LOAD_LAYER(i);
        }
    });
    cleanFile(self.id);
}

// 附图上传成功 返回显示集
function show_eImg(imgurl) {
    var pm = epic_num() + 1;
    var poDiv = document.createElement('div');
    poDiv.id = "id_div_" + pm;
    poDiv.style = "float:left;margin-left: 5px";
    poDiv.setAttribute('class',"form-group");
    poDiv.setAttribute('ondragover',"allowDrop(event)");
    poDiv.setAttribute('draggable',"true");
    poDiv.setAttribute('ondragstart',"to_drag(event,this)");
    poDiv.setAttribute('ondrop',"to_drop(event,this)");

    poDiv.innerHTML =
        '<div class="controls " style="float:none;" align="center">' +
        '<div class="thumbnail"  style="height: 170px;width: 150px">'+
        '<img src="'+$.trim(imgurl)+'"' +
        ' onclick="javascrip:$("#id_upImg_"'+pm+').click();" id="id_value_' + pm + '_Show" ' +
        ' style="width: 120px; height: 120px" class="img"/>' +
        '<input type="file" id="id_upImg_' + pm + '" onchange="upload_Img(this, \'id_value_\''+pm+', \'eImg\');" style="display:none;" value=""' +
        ' accept="image/gif, image/jpeg, image/png, image/gif ">' +
        '<input type="hidden" value="'+$.trim(imgurl)+'" name="e_Pic" id="id_value_' + pm + '">' +
        '<div class="caption"><a onclick="change_main_image(\''+pm+'\')">设为主图</a>' +
        '<a style="margin-left: 5px" onclick="delete_eImg(\''+pm+'\')">删除</a></div>' +
        '</div>'+
        '</div>';
    return poDiv
}


function cleanFile(f_num) {
    var file = document.getElementById(f_num);
    // for IE, Opera, Safari, Chrome
    if (file.outerHTML) {
        file.outerHTML = file.outerHTML;
    } else { // FF(包括3.5)
        file.value = "";
    }
}


// 主图，变体图 图片删除 右上小红点
function imgdelete(f_num) {
    document.getElementById(f_num+'_Show').src = "http://ou3qh0g46.bkt.clouddn.com/fancyqube.jpg";
    $("#" + f_num).val("");
    pic_num(f_num);
}

// 附图删除
function delete_eImg(id_div) {
    var divdom = document.getElementById('id_div_'+id_div);
    divdom.parentNode.removeChild(divdom);
    pic_num('');
}


// 附图数量
function epic_num() {
    var ePic = document.getElementsByName("e_Pic");
    return ePic.length
}

// 变体图数量
function vpic_num() {
    var i = 0;
    var vpic = document.getElementsByName("v_Pic");
    for (var n=0;n<vpic.length;n++){
        if (vpic[n].value != ''){
            i = i + 1;
        }
    }
    return i
}

// 计算变体数量和附图总数
function pic_num(f_num) {
    // 获取变体和附图的总数量
    var i = vpic_num() + epic_num();
    var v_num = document.getElementsByName("productsku");

    $("#v_num").text(v_num.length);
    $("#pic_num").text(i);
}


function ityzl_SHOW_LOAD_LAYER(){
    return parent.layer.msg('努力修改中，请稍等...', {icon: 16,shade: [0.5, '#f5f5f5'],scrollbar: false,offset: '50%', time:100000}) ;
}
function ityzl_CLOSE_LOAD_LAYER(index){
    parent.layer.close(index);
}
function ityzl_SHOW_TIP_LAYER(){
    parent.layer.msg('修改完成！',{time: 1000,offset: '50%'});
}

// 标签生成事件
function confirm_tags() {
    var tagtmp = document.getElementById('id_tags_input');
    var tagval = $.trim(tagtmp.value);
    if (tagval == ''){
        alert('请输入标签！');
        return
    }
    var tag_num_tmp = document.getElementById('tags_num');
    var tag_num = parseInt(tag_num_tmp.innerText);
    // if (tag_num >= 10){
    //     alert('标签数量已经10个了，不能继续添加！');
    //     tagtmp.value = '';
    //     return
    // }
    var tag_list_tmp = tagval.split(',');
    // if (tag_num+tag_list_tmp.length > 10){
    //     alert('输入的标签个数太多！');
    //     return
    // }
    var taglist = document.getElementsByName('tags');
    for (var i=0;i<taglist.length;i++){
        var idx = tag_list_tmp.indexOf(taglist[i].value);
        if(idx != -1){
            alert('输入的标签已经存在！重复！tag: '+taglist[i].value);
            return
        }
    }
    var oClearList = document.getElementById('Tags_List');
    var infor = '';
    var t_num = 0;
    for (var tn=0;tn<tag_list_tmp.length;tn++){
        if ($.trim(tag_list_tmp[tn])){  // 排除
            t_num += 1;
            infor += '<div class="selectedInfor selectedShow" ' +
                    'ondragover="allowDrop(event)" draggable="true" ondragstart="to_drag(event,this,\'tag\')" ondrop="to_drop(event,this,\'tag\')">' +
                    '<input type="hidden" id="id_tags_' + (tag_num+t_num) + '" name="tags" readonly="readonly" value="' + tag_list_tmp[tn] + '"/>' +
                    '<span style="font-size:5px">' + tag_list_tmp[tn] + '</span><em onclick="cancel_tags(\'' + (tag_num+t_num) + '\')"></em>' +
                    '</div>';
        }
    }

    oClearList.innerHTML = oClearList.innerHTML + infor;
    tag_num_tmp.innerText = tag_num+t_num;
    tagtmp.value = '';
}

// 标签单个删除
function cancel_tags(numb) {
    var dt_Div = document.getElementById('id_tags_' + numb);
    var parent_dt_Div = dt_Div.parentNode;
    parent_dt_Div.parentNode.removeChild(parent_dt_Div);

    var tag_num_tmp = document.getElementById('tags_num');
    tag_num_tmp.innerText = parseInt(tag_num_tmp.innerText)-1;
}


// 保存
function pub_to_submit(subname) {
    var obj = document.getElementById("id_ShopName");
    var index = obj.selectedIndex;
    var shopname = obj.options[index].text;
    if (!shopname){
        alert('请输入店铺名称！');
        document.getElementById("mask").style.display = "none";
        return
    }
    var ps_obj = document.getElementsByName('productsku');
    if (ps_obj.length < 1){
        alert('请至少增加一条变体！');
        document.getElementById("mask").style.display = "none";
        return
    }

    if (delshopskulsit){
        $.getJSON('/get_shopsku/?flag=1&shopsku='+escape(delshopskulsit.join(',')), function(result){
            if (result.resultCode == '-1'){
                alert('处理异常，请联系it人员处理。messages:' + JSON.stringify(result));
                console.log('处理异常，请联系it人员处理。messages:' + JSON.stringify(result));
                document.getElementById("mask").style.display = "none";
                return
            }
        });
    }
    if  (!of_check()){
        document.getElementById("mask").style.display = "none";
        return
    }
    // alert('没问题');
    var myform=$('#t_templet_wish_publish_draft_form'); //得到form对象
    var tmpInput=$("<input type='text' name='" + subname + "'/>");
    tmpInput.attr("value", subname);
    myform.append(tmpInput);
    myform.submit();
}

// 标签一键清空
function clear_tags() {
    var oClearList = document.getElementById('Tags_List');
    oClearList.innerHTML = '';
    var tag_num_tmp = document.getElementById('tags_num');
    tag_num_tmp.innerText = 0;
}

// 附图 主图 替换事件
function change_main_image(index) {
    var mainpic = document.getElementById('id_MainPic_Show'); // 主图
    var main_image_url = $.trim(mainpic.src);
    var mainpic_value = document.getElementById('id_MainPic');
    var main_image_value = $.trim(mainpic_value.value);

    var epic = document.getElementById('id_value_'+index+'_Show');
    var eimage_url = $.trim(epic.src);
    var epic_value = document.getElementById('id_value_'+index);
    var eimage_value = $.trim(epic_value.value);

    if (eimage_value == ''){
        alert('主图不能为空！');
        return
    }

    epic.src = main_image_url;
    epic_value.value = main_image_value;

    mainpic.src = eimage_url;
    mainpic_value.value = eimage_value;
}

// 选择网络图 事件
function webimgSelect(f_num) {
    var p_num = epic_num() + vpic_num();
    var selftmp = document.getElementById(f_num);
    if (selftmp.value == ''){
        p_num += 1;
    }

    if (p_num > 20){
        alert('变体图和附图的总个数不能超过20个！');
        return
    }

    $('#vimage_id').val(f_num);

    var eimages = document.getElementsByName('e_Pic');
    var showInfo = '';
    for (var i=0,j=eimages.length;i<j;i++){
        if(eimages[i].value != ''){
            showInfo += '<div class="col-md-3" style="float: left"><a class="thumbnail">' +
                '<img src="' + $.trim(eimages[i].value) + '" alt="通用的占位符缩略图" width="240" height="240" ondblclick="v_change(this)">' +
                '</a></div>'
        }
    }
    document.getElementById('row_show_id').innerHTML = showInfo;

    $('#show_image').modal({backdrop: 'static', keyboard: false});
}

// 变体图选择 双击事件
function v_change(self) {
    var eimgid = document.getElementById('vimage_id');

    document.getElementById(eimgid.value +'_Show').src = $.trim(self.src);
    $("#" + eimgid.value).val($.trim(self.src));

    document.getElementById('model_close').click();
    pic_num(eimgid.value)
}

// 变体图 选择的 浮动框 关闭事件
$(function () {
    $('#show_image').on('hide.bs.modal', function () {
        $('#vimage_id').val('');
        document.getElementById('row_show_id').innerHTML = '';

        document.getElementById('input_image_url').value = '';
        document.getElementById('show_urlpic').src = '';
        document.getElementById('show_div').style.display = 'none';
    })
});

// 输入图片URL预览
function preview_url() {
    var imagetmp = document.getElementById('input_image_url');
    if (imagetmp.value == ''){
        alert('请输入完整的图片URL');
        return
    }
    document.getElementById('show_urlpic').src = $.trim(imagetmp.value);
    document.getElementById('show_div').style.display = '';
}


// 图片拖拽功能
function allowDrop(ev)
{
    ev.preventDefault();
}

var srcdiv = null;
var domdiv = null;

function to_drag(ev,divdom)
{
    srcdiv = $(divdom).parent();
    domdiv = divdom;
    // srcdiv=divdom;
    // ev.dataTransfer.setData("text/html",divdom.innerHTML);
}

function to_drop(ev,divdom)
{
    ev.preventDefault();
    if(srcdiv[0] == $(divdom).parent()[0] && domdiv != divdom){
        $(divdom).before(domdiv);
        // srcdiv.innerHTML = divdom.innerHTML;
        // divdom.innerHTML = ev.dataTransfer.getData("text/html");
        delete_flag();
    }
    srcdiv = null;
    domdiv = null;
}



// 主利润率 变化函数
function change_main_profitrate(self) {
    var productsku = document.getElementsByName('productsku');
    var price_dom = document.getElementsByName('price');
    var profitrate_dom = document.getElementsByName('profitrate');
    var shipping_dom = document.getElementsByName('shipping');

    var productsku_list = new Array();
    for (var i=0,j=productsku.length;i<j;i++) {
        if ($.trim(productsku[i].value) != '') {
            productsku_list.push($.trim(productsku[i].value));
        }
    }
    if (productsku_list.length && self.value != ''){
        $.getJSON('/t_templet_wish_publish_draft/change_profitrate/?productsku_list='+productsku_list.join(',')+'&profitrate='+self.value, function (result) {
            if (result.code == 1){
                for (var i=0,j=productsku.length;i<j;i++){
                    for (var x=0,y=result.sku_price_list.length;x<y;x++){
                        if (productsku[i].value == result.sku_price_list[x].sku ){
                            price_dom[i].value = (result.sku_price_list[x].price -1).toFixed(2) ;
                            price_dom[i].setAttribute('value', (result.sku_price_list[x].price -1).toFixed(2));

                            shipping_dom[i].value = 1 ;
                            shipping_dom[i].setAttribute('value', 1);

                            profitrate_dom[i].value = self.value ;
                            profitrate_dom[i].setAttribute('value', self.value)
                        }
                    }
                }
            }else {
                console.log('错误：'+result.errortext);
                alert('错误：'+result.errortext)
            }
        })
    }else if (self.value == ''){
        change_main_price(self);
        // for (var a=0,b=productsku.length;a<b;a++){
        //     price_dom[a].value = '' ;
        //     price_dom[a].setAttribute('value', '');
        //
        //     shipping_dom[a].value = '' ;
        //     shipping_dom[a].setAttribute('value', '');
        //
        //     profitrate_dom[a].value = self.value;
        //     profitrate_dom[a].setAttribute('value', self.value);
        // }
    }
}

// 子利润率 变化函数
function change_profitrate(self) {
    var productsku = $(self).parent().parent().find("input[name='productsku']");
    var price_dom = $(self).parent().parent().find("input[name='price']");
    var profitrate_dom = $(self).parent().parent().find("input[name='profitrate']");
    var shipping_dom = $(self).parent().parent().find("input[name='shipping']");

    var productsku_list = new Array();
    if ($.trim(productsku.val()) != ''){
        productsku_list.push($.trim(productsku.val()));
    }

    if (productsku_list.length && self.value != ''){
        $.getJSON('/t_templet_wish_publish_draft/change_profitrate/?productsku_list='+productsku_list.join(',')+'&profitrate='+self.value, function (result) {
            if (result.code == 1){
                price_dom.val((result.sku_price_list[0].price -1).toFixed(2)) ;
                price_dom.attr('value', (result.sku_price_list[0].price -1).toFixed(2));

                shipping_dom.val(1);
                shipping_dom.attr('value', 1);
            }else {
                console.log('错误：'+result.errortext);
                alert('错误：'+result.errortext)
            }
        })
    }else if (self.value == ''){
        price_dom.val('');
        price_dom.attr('value', '');

        shipping_dom.val('');
        shipping_dom.attr('value', '');
    }
}

// 主价格 运费变化函数
function change_main_price(self) {
    var mProfitRate = $('#id_MainProfitRate').val();
    if (mProfitRate != ''){
        return
    }
    var setprice = 0;

    var Main_Shipping = $('#id_Shipping').val();
    if (Main_Shipping != ''){setprice = setprice + parseFloat(Main_Shipping);}
    var Main_Price = $('#id_Price').val();
    if (Main_Price != ''){setprice = setprice + parseFloat(Main_Price);}
    if (parseInt(setprice) == 0){setprice=''}

    var productsku = document.getElementsByName('productsku');
    var price_dom = document.getElementsByName('price');
    var profitrate_dom = document.getElementsByName('profitrate');
    var shipping_dom = document.getElementsByName('shipping');

    var productsku_list = new Array();
    for (var i=0,j=productsku.length;i<j;i++){
        if ($.trim(productsku[i].value) != ''){
            productsku_list.push($.trim(productsku[i].value));
        }
    }

    if (productsku_list.length && setprice != '') {
        $.getJSON('/t_templet_wish_publish_draft/change_profitrate/?productsku_list=' + productsku_list.join(',') + '&setprice=' + setprice, function (result) {
            if (result.code == 1) {
                for (var i = 0, j = productsku.length; i < j; i++) {
                    for (var x = 0, y = result.sku_profitrate_list.length; x < y; x++) {
                        if (productsku[i].value == result.sku_profitrate_list[x].sku) {
                            price_dom[i].value = Main_Price;
                            price_dom[i].setAttribute('value', Main_Price);

                            shipping_dom[i].value = Main_Shipping;
                            shipping_dom[i].setAttribute('value', Main_Shipping);

                            profitrate_dom[i].value = result.sku_profitrate_list[x].profitrate;
                            profitrate_dom[i].setAttribute('value', result.sku_profitrate_list[x].profitrate)
                        }
                    }
                }
            }else {
                console.log('错误：'+result.errortext);
                alert('错误：'+result.errortext)
            }
        })
    }else if (setprice == ''){
        for (var a = 0, b = productsku.length; a < b; a++) {
            price_dom[a].value = Main_Price;
            price_dom[a].setAttribute('value', Main_Price);

            shipping_dom[a].value = Main_Shipping;
            shipping_dom[a].setAttribute('value', Main_Shipping);

            profitrate_dom[a].value = '';
            profitrate_dom[a].setAttribute('value', '')
        }
    }
}

// 子价格 运费变化函数
function change_price(self) {
    // var index_dom = self.parentNode.parentNode;
    // var index = index_dom.id-1;

    var productsku = $(self).parent().parent().find("input[name='productsku']");
    var price_dom = $(self).parent().parent().find("input[name='price']");
    var profitrate_dom = $(self).parent().parent().find("input[name='profitrate']");
    var shipping_dom = $(self).parent().parent().find("input[name='shipping']");

    var productsku_list = new Array();

    if ($.trim(productsku.val()) != ''){
        productsku_list.push($.trim(productsku.val()));
    }

    var setprice = 0;
    if (shipping_dom.val() != ''){setprice = setprice + parseFloat(shipping_dom.val());}
    if (price_dom.val() != ''){setprice = setprice + parseFloat(price_dom.val());}
    if (parseInt(setprice) == 0){setprice='';}

    if (productsku_list.length && setprice != '') {
        $.getJSON('/t_templet_wish_publish_draft/change_profitrate/?productsku_list=' + productsku_list.join(',') + '&setprice=' + setprice, function (result) {
            if (result.code == 1) {
                profitrate_dom.val(result.sku_profitrate_list[0].profitrate);
                profitrate_dom.attr('value', result.sku_profitrate_list[0].profitrate);
            }else {
                console.log('错误：'+result.errortext);
                alert('错误：'+result.errortext)
            }
        })
    }else if (setprice == ''){
        profitrate_dom.val('');
        profitrate_dom[index].attr('value', '');
    }
}

// 正则 将字符串每个 单词首字母大写 输出
function titleCase(str) {
   return str.toLowerCase().replace(/(?:^|\s)[a-z]/g, function (s) {
      return s.toUpperCase();
   });
}

// 提交验证函数
function of_check() {
    var mainimage = $('#id_MainPic').val();
    if (mainimage == ''){
        alert('主图不能为空！');
        return false
    }
    var tags = document.getElementsByName('tags');
    if (tags.length <= 0){
        alert('标签不能为空！');
        return false
    }

    if ($('#id_torttitle_flag').val() == '1'){
        var r=confirm("标题中不能有侵权词！ 是否依然保存？")
        if (r==true){
            return true
        }else{
            return false
        }
    }

    var product_skus = document.getElementsByName('productsku');
    var shopskus = document.getElementsByName('shopsku');
    var colors = document.getElementsByName('color');
    var sizes = document.getElementsByName('size');
    var shippingtimes = document.getElementsByName('shippingtime');
    var kcs = document.getElementsByName('kc');
    var prices = document.getElementsByName('price');
    var shippings = document.getElementsByName('shipping');
    var msrps = document.getElementsByName('msrp');

    var tmp_list = [];
    var check_shopsku_list = [];
    for (var i=0,j=product_skus.length;i<j;i++){
        var each_shopsku = $.trim(shopskus[i].value);
        if (each_shopsku == ''){
            alert('店铺SKU不能为空！');
            return false
        }
        var check_shopsku_index = check_shopsku_list.indexOf(each_shopsku);
        if (check_shopsku_index != -1){
            alert('店铺SKU不能重复！ '+ each_shopsku);
            return false
        }else {
            check_shopsku_list.push(each_shopsku);
        }

        if (j > 1 && ($.trim(colors[i].value) == '' && $.trim(sizes[i].value) == '')){
            alert('多变体时，变体的颜色和尺寸不能同时为空！');
            return false
        }

        if ($.trim(colors[i].value) != ''){
            var input_color_list = colors[i].value.split('&');
            for (var x=0,y=input_color_list.length;x<y;x++){
                if (input_color_list[x] != ''){
                    var color_tmp = titleCase($.trim(input_color_list[x]));
                    var index = $.inArray(color_tmp,colorlist);
                    // console.log(index);
                    if (index  == -1){
                        alert(colors[i].value + ' 该颜色值不在WISH接受范围');
                        return false
                    }
                }else if (input_color_list[x] == ''){
                    alert(colors[i].value + ' 该颜色值不在WISH接受范围');
                    return false
                }
            }
        }

        var tmp = 'size: ' + titleCase($.trim(sizes[i].value)) + ', color: ' + titleCase($.trim(colors[i].value));
        var in_index = $.inArray(tmp, tmp_list);
        if (in_index  != -1){
            alert(JSON.stringify(tmp) + ' 该颜色，尺寸值对重复！');
            return false
        }else {
            tmp_list.push(tmp);
        }
        
        if (shippings[i].value == ''){
            alert('运费不能为空!');
            return false
        }

        if (shippingtimes[i].value == ''){
            alert('运输时间不能为空!');
            return false
        }else{
            var time = shippingtimes[i].value.split('-');
            if (time.length != 2 || time.indexOf('') != -1){
                alert('运输时间格式不对！ 例：10-25');
                return false
            }else if (parseInt(time[0]) <= 2 || parseInt(time[1]) < parseInt(time[0]) + 5) {
                alert('运输时间不能小于2天，且上限必须在下限之后至少5天！');
                return false
            }
        }
        if (kcs[i].value == '' || parseInt(kcs[i].value) > 500000){
            alert('库存不能为空，且最大值不能超过 500000  ！');
            return false
        }

        if (prices[i].value == '' || parseInt(prices[i].value) > 100000){
            alert('价格不能为空，且最大值不能超过 100000  ！');
            return false
        }
        if (parseInt(prices[i].value) > parseInt(msrps[i].value)){
            alert('标签价不能低于售价！');
            return false
        }
        if (parseInt(shippings[i].value) > 1000){
            alert('运费最大值不能超过 1000  ！');
            return false
        }
    }

    return true
}

// 小更新按钮
function to_update(str) {
    if (str == 'MSRP'){
        var msrp_val = $('#id_MSRP').val();
        var MSRPs = document.getElementsByName('msrp');
        for (var i=0,j=MSRPs.length;i<j;i++){
            MSRPs[i].value = msrp_val;
        }
    }else if (str == 'Kc'){
        var kc_val = $('#id_KC').val();
        var kcs = document.getElementsByName('kc');
        for (var x=0,y=kcs.length;x<y;x++){
            kcs[x].value = kc_val;
        }
    }else if (str == 'shippingTime'){
        var shippingtime_val = $('#id_ShippingTime').val();
        var shippingtimes = document.getElementsByName('shippingtime');
        for (var a=0,b=shippingtimes.length;a<b;a++){
            shippingtimes[a].value = shippingtime_val;
        }
    }else if (str == 'Price' || str == 'Shipping'){
        $('#id_MainProfitRate').val('');
        var self = document.getElementById('id_MainProfitRate');
        change_main_price(self);
    }
}


function to_clean_up(str) {
    if (str == 'size'){
        var sizes = document.getElementsByName('size');
        for (var i=0,j=sizes.length;i<j;i++){
            sizes[i].value = '';
        }
    }
    if (str == 'color'){
        var colors = document.getElementsByName('color');
        for (var a=0,b=colors.length;a<b;a++){
            colors[a].value = '';
        }
    }
}


function to_check_title(self) {
    $.getJSON('/check_title/?title=' + encodeURI(self.value), function (result) {
        if (result.resultCode == 0){
            var warning_text = '';
            if (result.tort_flag == '1'){
                $('#id_torttitle_flag').val('1');
                warning_text = warning_text + '注意*：有侵权词('+result.tort_words+') <br>';
            }else {
                $('#id_torttitle_flag').val('0');
            }
            if (result.gray_flag == '1'){
                warning_text = warning_text + '注意*：有灰度词('+result.gray_words+')';
            }
            document.getElementById('id_title_warning').innerHTML = warning_text;

        }else {
            alert('错误：' + result.errorText);
            console.log('错误：' + result.errorText);
        }
    });
}





