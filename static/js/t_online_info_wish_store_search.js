
var info = '';
var synurl = '';
var ACTIONSNAME = 'batch_update_shipping';
var ACTIONSTORTFLAG = 'TortWordsDealWith';
$(document).ready(function() {
    var divdown = document.getElementById('div_items');
    var shopss = document.getElementById('list_id');
    var synurl_div = document.getElementById('synurl_id');
    synurl = synurl_div.value;

    var node = divdown.nextSibling;
    var shop_list = eval(shopss.value);
    for (var s = 0; s < shop_list.length; s++) {
        info += '<div class="div_item" onmousemove="getnewcolor(this)" onmouseout="getoldcolor(this)" onClick="ChangeText(this);">' + shop_list[s] + '</div>';
    }
    divdown.innerHTML = info;
    divdown.parentNode.insertBefore(divdown, node);
    node = divdown.nextSibling;

    if (document.getElementById('q').value == 'Wish-0000') {
        document.getElementById('q').value = '搜索店铺...';
    }
    //弹出列表框
    $("#q").click(function () {
        $("#div_items").css('display', 'block');
        return false;
    });

    //隐藏列表框
    $("body").click(function () {
        $("#div_items").css('display', 'none');
    });

    //文本框输入
    $("#q").keyup(function () {
        var intext = document.getElementById('q');
        var inputtext = intext.value;
        if (inputtext != "") {
            var html = "";
            for (var i = 0; i < shop_list.length; i++) {
                if (shop_list[i].indexOf(inputtext) >= 0) {
                    html += '<div class="div_item"onmousemove="getnewcolor(this)" onmouseout="getoldcolor(this)" onClick="ChangeText(this);">'+ shop_list[i] +'</div>';
                }
            }
            if (html != "") {
                $("#div_items").show().html(html);
            } else {
                $("#div_items").hide().html("");
            }
        }else {
            $("#div_items").show().html(info);
        }
    });

    $('#'+ACTIONSNAME).attr('onclick', 'batch_update_shipping_entrance()');
    $('#'+ACTIONSTORTFLAG).attr('onclick', 'TortWordsDealWith_BatchRemarks()');
});

//移入移出效果
function getnewcolor(obj) {
    $(obj).css('background-color', '#1C86EE').css('color', 'white');
}

function getoldcolor(obj) {
    $(obj).css('background-color', 'white').css('color', 'black');
}
//项点击
function ChangeText(obj) {
    var value = $(obj).text();
    $("#q").val(value);
    $("#div_items").show().html('<div class="div_item" onmousemove="getnewcolor(this)" onmouseout="getoldcolor(this)" onClick="ChangeText(this);">'+ value +'</div>');
}

var fulllength = 0;
var partlength = 0;
var IntervalID = '';

function Get_Syn_Progress(rFlag) {

    $.getJSON(synurl+"&bar=0", function(result){
        if (result.resultCode == '3' && result.messages != 'Over'){
            if (rFlag == '0'){
                fulllength++ ;
                if (fulllength <= 98){
                    document.getElementById('full_bar_id').style.width = fulllength.toString() + '%';
                    document.getElementById('full_bar_span').innerText = '已经开始同步全量数据数据，时间等候较长，请稍等。。。' + '(' + fulllength.toString() + '%' + ')';
                }
                // if (fulllength == 99){
                //     fulllength = 0;
                // }
            }
            if (rFlag == '1'){
                partlength++ ;
                if (partlength <= 98){
                    document.getElementById('part_bar_id').style.width = partlength.toString() + '%';
                    document.getElementById('part_bar_span').innerText = '已经开始同步增量数据，请稍等。。。' + '(' + partlength.toString() + '%' + ')';
                }
                // if (partlength == 99){
                //     partlength = 0
                // }
            }
        }
        if (result.resultCode == '3' && result.messages == 'Over'){
            if (rFlag == '0'){
                document.getElementById('full_bar_id').style.width = '100%';
                document.getElementById('full_bar_span').innerText = '全量数据同步完成(100%)';
                document.getElementById('sub_full').style.display = 'none';
                document.getElementById('sub_refresh_full').style.display = '';
            }
            if (rFlag == '1'){
                document.getElementById('part_bar_id').style.width = '100%';
                document.getElementById('part_bar_span').innerText = '增量数据同步完成(100%)';
                document.getElementById('sub_part').style.display = 'none';
                document.getElementById('sub_refresh_part').style.display = '';
            }
            clearInterval(IntervalID);
        }
    });
}

function refresh_shopnsme_data(rFlag) {
    $.getJSON(synurl+"&flag=" + rFlag, function(result){
        if (result.resultCode == '0'){
            IntervalID = setInterval('Get_Syn_Progress('+ rFlag + ')',500);
        }else {
            if (rFlag == '0'){
                document.getElementById('full_bar_span').innerText = '数据刷新错误！请联系IT部门。';
                document.getElementById('full_bar').style.display = 'none';
            }
            if (rFlag == '1'){
                document.getElementById('part_bar_span').innerText = '数据刷新错误！请联系IT部门。';
                document.getElementById('part_bar').style.display = 'none';
            }
        }
    });
}

// Refresh_Ajax() 弹出框调用api，并显示进度条  # 0 全量更新  # 1 增量更新
function Refresh_Ajax_full(rFlag) { //全量刷新
    if (rFlag == '0'){ // 全量更新
        document.getElementById('full_bar_span').innerText = '已经开始同步全量数据数据，时间等候较长，请稍等。。。';
        document.getElementById('full_bar').style.display = '';
    }
    if (rFlag == '1'){ // 增量更新
        document.getElementById('part_bar_span').innerText = '已经开始同步增量数据，请稍等。。。';
        document.getElementById('part_bar').style.display = '';
    }
    refresh_shopnsme_data(rFlag); // 正式开始同步刷新数据
}

function onclick_refresh_page() {
    location.reload();
}


function static_refresh(url) {
    $.getJSON(url, function(result){
        if (result.resultCode == '1'){
            alert(result.messages);
            var r = confirm(result.messages + "！\n是否刷新页面？");
            if (r==true){
                location.reload();
            }else{
                return;
            }
        }else {
            alert('异常:'+result.messages);
        }
    });
}

function change_shopsku(flag) {
    var all_shopsku_info = document.getElementsByName('shopskucheck');
    var checkinfo = new Array();
    for (var i=0;i<all_shopsku_info.length;i++){
        if (all_shopsku_info[i].checked){
            var id = all_shopsku_info[i].id;
            var val = $('#'+id).parent().parent().parent().find("td").eq(4).text();
            var info = [id.split('_').pop(),val];
            // alert('val==='+val);
            checkinfo.push(info);
        }
    }
    // alert('checkinfo==='+checkinfo);
    // checkinfo 包含了需要上下架的店铺SKU和归属店铺
    if (checkinfo.length >= 1){
        submit_shopsku_update(JSON.stringify(checkinfo),flag);
    }else {
        alert('请选择要进行上下架的记录');
    }
}

function ityzl_SHOW_LOAD_LAYER(){
    return parent.layer.msg('努力修改中...', {icon: 16,shade: [0.5, '#f5f5f5'],scrollbar: false,offset: '50%', time:10000000}) ;
}
function ityzl_CLOSE_LOAD_LAYER(index){
    parent.layer.close(index);
}
function ityzl_SHOW_TIP_LAYER(text){
    parent.layer.msg(text,{time: 5000,offset: '30%'});
}

function submit_shopsku_update(data,flag) {
    var i;
    var token = document.getElementsByName('csrfmiddlewaretoken')[0];
    // 这里开始调取api
    $.ajax({
        url: "/up_dis_by_wish_api_shopsku/?flag="+flag,
        type: "POST",
        dataType: "json",
        data: {
            csrfmiddlewaretoken: token.value,
            alldata: data
        },
        beforeSend: function () {
            i = ityzl_SHOW_LOAD_LAYER();
        },
        success: function (sresult) {
            if (sresult.code == 0) {
                ityzl_CLOSE_LOAD_LAYER(i);
                var r = confirm(sresult.content + "\n是否刷新页面？");
                if (r==true){
                    location.reload();
                }else{
                    return;
                }
                // ityzl_SHOW_TIP_LAYER(sresult.content);
            } else if (sresult.code == -1){
                ityzl_CLOSE_LOAD_LAYER(i);
                ityzl_SHOW_TIP_LAYER('传参错误！请联系IT相关人员。\n messages:' + sresult.messages);
            }else {
                ityzl_CLOSE_LOAD_LAYER(i);
                ityzl_SHOW_TIP_LAYER('错误，请联系IT相关人员。');
                console.log(JSON.stringify(sresult));
            }
        },
        error:function (XMLHttpRequest, textStatus, errorThrown) {
            ityzl_CLOSE_LOAD_LAYER(i);
            ityzl_SHOW_TIP_LAYER('错误信息：' + XMLHttpRequest.responseText);//获取的信息即是异常中的Message
            console.log('错误信息：' + XMLHttpRequest.responseText)
       }
    });
}

function isHidden(oDiv){
  var vDiv = document.getElementById(oDiv);
  vDiv.style.display = (vDiv.style.display == 'none')?'block':'none';
}


function to_seach_shopname() {
    var qval = document.getElementById("q");

    if (qval.value == '搜索店铺...'){
        location.reload();
    }else {
        $('#seach_shopname').submit();
    }
}



function setExpressType(sel, id) {
    $.getJSON('/wish_store_management/change_wish_express_type/?id=' + id + '&value=' + sel.value, function(result){
        var type_show = document.getElementById(id);
        if (result.resultCode == '-1'){
            console.log('异常:'+result.messages);
            type_show.style.color = 'red';
            type_show.innerText = "修改失败";
        }
        if (result.resultCode == '1'){
            type_show.style.color = 'green';
            type_show.innerText = "修改成功";
        }
    });
}



function batch_update_shipping_entrance() {
    if (!check_box_num()){
        alert('请选择需要修改的数据！');
        return null;
    }

    $('#model_id_batch_update_shipping').modal({backdrop: 'static', keyboard: false});
    click_num_prompt();
}


function show_seach_country(self) {
    var all_countrys = document.getElementsByName('countryname');
    for (var i=0,j=all_countrys.length;i<j;i++){
        var ptrdom = all_countrys[i].parentNode.parentNode.parentNode;
        if ($.trim(self.value) != '' && all_countrys[i].innerText.indexOf($.trim(self.value)) == -1){
            $(ptrdom).css('display', 'none');
        }else {
            $(ptrdom).css('display', '');
        }
    }
}

function set_shipping_price(self) {
    var td_next = self.parentNode.nextElementSibling;
    var price_dom = $(td_next).find('input')[0];
    if (self.value == 'True' || self.value == '0'){
        $(price_dom).attr('value','');
        $(price_dom).attr('disabled','disabled');
    }else {
        $(price_dom).removeAttr('disabled');
    }
}

function check_box_num() {
    var checkboxs = document.getElementsByName('_selected_action');
    var checklist = new Array();
    for (var i=0,j=checkboxs.length;i<j;i++){
        if (checkboxs[i].checked){
            checklist.push(1);
        }
    }
    if (checklist.length >= 1){return true;}else {return false;}
}


function click_num_prompt() {
    var selectnum = document.getElementById('select_num');
    var selectnumall = document.getElementById('select_num_all');

    var prompt_span = document.getElementById('id_prompt_span');

    if (selectnum.style.display == 'none' && selectnumall.style.display != 'none'){
        prompt_span.innerText = selectnumall.innerText;
    }else {
        prompt_span.innerText = selectnum.innerText;
    }
}


function batch_update_shipping_func() {
    var Tmp_dom = document.getElementsByName('countrycode');
    var dom_lenght = Tmp_dom.length;

    var datalist = new Array();
    for (var i=0;i<dom_lenght;i++){
        var datadict = {};
        var name_list = ['countrycode', 'shipping_type', 'shipping_value', 'WishExpress', 'enabled'];

        var country_name = document.getElementsByName('countryname')[i];
        var country_code = document.getElementsByName('countrycode')[i];
        if (!country_code.checked){
            continue
        }
        datadict['country'] = country_code.value;
        var wish_express = document.getElementsByName('WishExpress')[i];
        if (wish_express.checked){
            datadict['wish_express']   = 'true';
        }else {
            datadict['wish_express']   = 'false';
        }

        var country_enabled = document.getElementsByName('enabled')[i];
        if (country_enabled.checked){
            datadict['enabled']   = 'true';
        }else {
            datadict['enabled']   = 'false';
        }

        var shipping_type = document.getElementsByName('shipping_type')[i];
        var shipping_price = document.getElementsByName('shipping_value')[i];
        if (shipping_type.value == 'IOOV'){
            if (shipping_price.value == ''){
                alert('请输入需要增加的运费值！');
                continue
            }else {
                datadict['_add'] = shipping_price.value;
            }
        }else if (shipping_type.value == 'False') {
            if (shipping_price.value == ''){
                alert('请输入需要增加的运费值！');
                continue
            }else {
                datadict['price'] = shipping_price.value;
            }
        }else {
            datadict['use_product_shipping'] = 'true';
            datadict['price'] = '1';
        }
        datalist.push(datadict);
    }

    if (JSON.stringify(datalist) != '[]'){
        console.log(datalist);
        $('#action').val(ACTIONSNAME);
        to_sub_form(JSON.stringify(datalist));
    }else {
        alert('无运费修改！');
        return null
    }
}


function return_selected(obj) {
    var opts = obj.getElementsByTagName('option');
    for (var a in opts) {
        if (opts[a].defaultSelected) {
            return opts[a].value;
        }
    }
    return ''
}


function to_sub_form(jsontext) {
    var model_info = document.getElementById('id_prompt_span');
    model_info.innerHTML = model_info.innerHTML + '<span id="zt">正在进行操作，请稍等。。。</span>';
    var model_text = document.getElementById('id_prompt_text');
    model_text.innerHTML = '';

    var myform=$('#changelist-form'); //得到form对象
    var tmpInput=$("<input type='text' name='update_data_json_str'/>");
    tmpInput.attr("value", jsontext);
    myform.append(tmpInput);

    var csrftoken = getCookieqq('csrftoken');
    $.ajax({
        url: "",
        data: myform.serialize(),
        type: "POST",
        dataType: "json",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            $('#brPress_id').val('1');
            $('#sub_part').attr('disabled', 'disabled');
        },
        success: function (result) {
            if (result.rcode == '1'){
                console.log(result);
                document.getElementById('div_id_progress').style.display = '';
                document.getElementById('div_id_table').style.display = 'none';
                refresh_process(result.KEY, 'id_prompt_text', 'id_progress');  // 进程查询关键字， 日志显示ID，进度条ID
            }else {
                alert(result.messages);
            }
        },
        error:function (XMLHttpRequest, textStatus, errorThrown) {
            alert('错误信息：' + XMLHttpRequest.responseText); //获取的信息即是异常中的Message
            console.log('错误信息：' + XMLHttpRequest.responseText); //获取的信息即是异常中的Message
            clearInterval(id);
            $('#brPress_id').val('0');
        }
    });
}


$(function () {
    $('#model_id_batch_update_shipping').on('hide.bs.modal', function () {
        // alert('嘿，我听说您喜欢模态框...');
        var brP = document.getElementById('brPress_id');
        if (brP.value == '1'){
            alert("操作没有完成不能关闭");
            return false
        }
        document.getElementById('id_progress').style.width = '0%';
        document.getElementById('div_id_progress').style.display = 'none';
        document.getElementById('div_id_table').style.display = '';
        var model_info = document.getElementById('id_prompt_span');
        model_info.innerText = '';
        var model_text = document.getElementById('id_prompt_text');
        model_text.innerText = '';
        clearInterval(id);
        location.reload();
    })
});


function TortWordsDealWith_BatchRemarks() {
    if (!check_box_num()){
        alert('请选择需要修改的数据！');
        return null;
    }

    $('#idFor_BatchRemarks').modal({backdrop: 'static', keyboard: false});
}


function to_batch_update_tort_remark() {
    $('#action').val(ACTIONSTORTFLAG);

    var myform=$('#changelist-form'); //得到form对象
    var tmptext=$('<input name="batch_remark_text">');
    tmptext.attr("value", $('#batch_remark_id').val());
    myform.append(tmptext);

    $('#idFor_BatchRemarks').modal('hide');
    $.do_action(ACTIONSTORTFLAG, '修改侵权词处理标记');
}






