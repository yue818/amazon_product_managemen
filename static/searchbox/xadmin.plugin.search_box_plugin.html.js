
$(document).ready(function(){
    var countFor = document.getElementsByName('count');
    var input_id1 = document.getElementsByName('input_id1');
    for(var i = 0; i < countFor.length; i++){
        var idx = input_id1[i].value
        var sel = document.getElementById('select' + idx).value;
        var dvalue = document.getElementById('dvalue' + idx).value;
        var nameid = document.getElementById('id_' + idx).value;
        if(sel==2){
            var check = document.getElementsByName('checkbox' + nameid + '[]');
            var vlist = dvalue.split(',');
            for(var j=0; j<check.length; j++){
                for(var l=0; l<vlist.length; l++){
                    if(check[j].value == vlist[l]) check[j].checked=true;
                }
            }
        }else if(sel == 1) {
            var radio = document.getElementsByName('radio' + nameid + '[]');
            for(var j=0; j<radio.length; j++){
                if(radio[j].value == dvalue) radio[j].checked=true;
            }
        }else if(sel == 3) {
            var selec = document.getElementById('select_' + idx);
            for(var j=0; j<selec.length; j++){
                if(selec.options[j].value == dvalue) selec.options[j].selected=true;
            }
        }
    }
    $(document).keydown(function(e) {
        e = e || window.event;
        var keycode = e.which ? e.which : e.keyCode;
        if (keycode == 38) {
            if (jQuery.trim($("#append").html()) == "") {
                return;
            }
            movePrev();
        } else if (keycode == 40) {
            if (jQuery.trim($("#append").html()) == "") {
                return;
            }
            $("#value17").blur();
            if ($(".item").hasClass("addbg")) {
                moveNext();
            } else {
                $(".item").removeClass('addbg').eq(0).addClass('addbg');
            }
        } else if (keycode == 13) {
            dojob();
        }
    });

    var dojob = function() {
        $("#value17").blur();
    var value = $(".addbg").text();
        $("#value17").val(value);
        $("#append").hide().html("");
    }
});
Date.prototype.format = function(fmt) {
    var o = {
        "M+" : this.getMonth()+1,                 //月份
        "d+" : this.getDate(),                    //日
        "h+" : this.getHours(),                   //小时
        "m+" : this.getMinutes(),                 //分
        "s+" : this.getSeconds(),                 //秒
        "q+" : Math.floor((this.getMonth()+3)/3), //季度
        "S"  : this.getMilliseconds()             //毫秒
    };
    if(/(y+)/.test(fmt)) {
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    for(var k in o) {
        if(new RegExp("("+ k +")").test(fmt)){
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
        }
    }
    return fmt;
}
function my_Search() {
    var validation = true;
    var countFor = document.getElementsByName('count');
    var urlstr = document.getElementById('url').value;
    var input_id1 = document.getElementsByName('input_id1');
    for(var i = 0; i < countFor.length; i++) {
        var idx = input_id1[i].value
        var sel = document.getElementById('select' + idx).value;
        var ul1 = document.getElementById('urlname' + idx).value;
        var nameid = document.getElementById('id_' + idx).value;
        if (sel == 1) {
            var radio = document.getElementsByName('radio' + nameid + '[]');
            var conditions = '';
            for (var j = 0; j < radio.length; j++) {
                if (radio[j].checked) {
                    conditions += radio[j].value;
                    break;
                }
            }
        } else if (sel == 2) {
            var check = document.getElementsByName('checkbox' + nameid + '[]');
            var conditions = '';
            for (var j = 0; j < check.length; j++) {
                if (check[j].checked) {
                    conditions += check[j].value + ',';
                }
            }
            conditions = conditions.slice(0, -1);
        } else if (sel == 3) {
            var selec = document.getElementById('select_' + idx);
            var index = selec.selectedIndex;
            if(index != -1){
            var conditions = selec.options[index].value;
            }
        }else if (sel == 5) {
            var serialNumber = document.getElementById('serialnumber_' + idx).value;
            var conditions = document.getElementById('_easyui_textbox_input' + serialNumber).value;
        } else {
            var conditions = document.getElementById('value' + idx).value;
        }
        if(ul1.toLowerCase() == "shopsku"){
            conditions = escape(conditions);
        }
        if(ul1 == "ShopName"){
            conditions = conditions.replace(/(^\s*)|(\s*$)/g, "")
            conditions = encodeURIComponent(conditions);
        }
		if(ul1 == "ShopName1"){
            conditions = conditions.replace(/(^\s*)|(\s*$)/g, "")
            conditions = encodeURIComponent(conditions);
        }
        if(ul1 == "LargeCategory"){
            conditions = conditions.replace(/(^\s*)|(\s*$)/g, "")
            conditions = encodeURIComponent(conditions);
        }
        if (ul1 == "ShopName_ZY")
        {
            conditions = conditions.replace("/","%2F")
            conditions = conditions.replace(/(^\s*)|(\s*$)/g, "")
        }
        if (ul1 == "LinkUrl")
        {
            conditions = conditions.replace(/\//g,"%2F");
            conditions = conditions.replace(":","%3A");
        }
         if(ul1 == "code"){
             conditions = conditions.replace(/\+/g,"%2B")
        }
        if(ul1 == "sku"){
             conditions = conditions.replace(/\#/g,"%23").replace(/\+/g,"%2B")
        }
        if(ul1 == 'subSKU'){
            conditions = conditions.replace(/\#/g,"%23")
        }
        if(ul1.toLowerCase()  == 'productsku'){
            conditions = escape(conditions);
        }

        if(ul1 == 'SKU'){
            conditions = conditions.replace(/\#/g,"%23")
        }

        if ((conditions != null) && (conditions != "") && (conditions.replace(/(^s*)|(s*$)/g, "").length > 0)) {
            urlstr += ul1 + '=' + conditions + '&';
        }
        
    }


    var countTwo = document.getElementsByName('countTwo');
    var input_id2 = document.getElementsByName('input_id2');
    for(var i = 0; i < countTwo.length; i++) {
        var idx = input_id2[i].value
        var ul1 = document.getElementById('urlname1' + idx).value;
        var ul2 = document.getElementById('urlname2' + idx).value;
        var conditions1 = document.getElementById('value1' + idx).value;
        var conditions2 = document.getElementById('value2' + idx).value;

        var dateT = document.getElementById('date' + idx).value;
        if ((conditions1 != null) && (conditions1 != "") && (conditions1.replace(/(^s*)|(s*$)/g, "").length > 0))
        {
            urlstr += ul1 + '=' + conditions1 + '&';
        }
        if ((conditions2 != null) && (conditions2 != "") && (conditions2.replace(/(^s*)|(s*$)/g, "").length > 0))
        {
            if(dateT==1){
                var endTime = new Date(Date.parse(conditions2));
                endTime.setDate(endTime.getDate()+1);
                conditions2 = endTime.format('yyyy-MM-dd');
            }
            urlstr += ul2 + '=' + conditions2 + '&';

        }
        if(dateT==0){
            if((conditions1 != null)&&(conditions2 != null)&&(conditions1 != '')&&(conditions2 != '')){
                var aa = parseInt(conditions1);
                var bb = parseInt(conditions2);
                if(aa > bb){
                    validation = false;
                    alert('数字输入错误！');
                }
            }
        }else {
            if((conditions1 != null)&&(conditions2 != null)&&(conditions1 != '')&&(conditions2 != '')&&(conditions2<conditions1)){
                validation = false;
                alert('日期输入错误！');
            }
        }
    }
    urlstr = urlstr.slice(0,-1);

    urlstr = urlstr.replace('?&','?');
    if(validation){ 
        if(urlstr.search('/Project/admin/ebayapp/t_online_info_ebay_listing/') != -1 ){        
           urlstr = urlstr.replace(/&Select_flag=\d+/g,'').replace(/Select_flag=\d+&/g,'').replace(/Select_flag=\d+/g,'')
        }
        window.location.href=urlstr;
    }else {
        myReset();
    }
}

function myReset() {
    var countFor = document.getElementsByName('count');
    var countTwo = document.getElementsByName('countTwo');
    var input_id1 = document.getElementsByName('input_id1');
    for(var i = 0; i < countFor.length; i++) {
        var idx = input_id1[i].value
        var sel = document.getElementById('select' + idx).value;
        var nameid = document.getElementById('id_' + idx).value;
        var dvalue1 = document.getElementById('dvalue' + idx).value;
        if (sel == 0) {
            var m = document.getElementById('value' + idx);
            m.value = dvalue1;
        } else if (sel == 2) {
            var check = document.getElementsByName('checkbox' + nameid + '[]');
            var vlist = dvalue1.split(',');
            for (var j = 0; j < check.length; j++) {
                for (var l = 0; l < vlist.length; l++) {
                    if (check[j].value == vlist[l]) {
                        check[j].checked = true;
                        break;
                    }
                }
            }
        } else if (sel == 3) {
            var selec = document.getElementById('select_' + idx);
            for (var j = 0; j < selec.length; j++) {
                if (selec.options[j].value == dvalue1) selec.options[j].selected = true;
            }
        } else if (sel == 5) {
        	  var serialNumber = document.getElementById('serialnumber_' + idx).value;
            var mm = document.getElementById('_easyui_textbox_input' + serialNumber);
            mm.value = dvalue1;
        }else {
            var radio = document.getElementsByName('radio' + nameid + '[]');
            for (var j = 0; j < radio.length; j++) {
                if (radio[j].value == dvalue1) {
                    radio[j].checked = true;
                }
            }
        }
    }

    var input_id2 = document.getElementsByName('input_id2');
    for(var i = 0; i < countTwo.length; i++) {
        var idx = input_id2[i].value
        var dvalue1 = document.getElementById('dvalue1' + idx).value;
        var dvalue2 = document.getElementById('dvalue2' + idx).value;
        var m1 = document.getElementById('value1' + idx);
        var m2 = document.getElementById('value2' + idx);
        m1.value=dvalue1;
        m2.value=dvalue2;
    }
}

function clearAll(){
    var countFor = document.getElementsByName('count');
    var countTwo = document.getElementsByName('countTwo');
    var input_id1 = document.getElementsByName('input_id1');
    for(var i = 0; i < countFor.length; i++) {
        var idx = input_id1[i].value
        var sel = document.getElementById('select' + idx).value;
        var m = document.getElementById('value' + idx);
        var nameid = document.getElementById('id_' + idx).value;
        if (sel == 0) {
            m.value = '';
        } else if (sel == 2) {
            var check = document.getElementsByName('checkbox' + nameid + '[]');
            for (var j = 0; j < check.length; j++) {
                check[j].checked = false;
            }
        } else if (sel == 3) {
            var selec = document.getElementById('select_' + idx);
            for (var j = 0; j < selec.length; j++) {
                if (selec.options[j].value == '') selec.options[j].selected = true;
            }
        } else if (sel == 5) {
            var serialNumber = document.getElementById('serialnumber_' + idx).value;
            var mm = document.getElementById('_easyui_textbox_input' + serialNumber);
            mm.value = '';
        }else {
            var radio = document.getElementsByName('radio' + nameid + '[]');
            for (var j = 0; j < radio.length; j++) {
                if (radio[j].value == '') {
                    radio[j].checked = true;
                }
            }
        }
    }

    var input_id2 = document.getElementsByName('input_id2');
    for(var i = 0; i < countTwo.length; i++) {
        var idx = input_id2[i].value
        var m1 = document.getElementById('value1' + idx);
        var m2 = document.getElementById('value2' + idx);

        m1.value='';
        m2.value='';
    }
}
function searchAll() {
    var uu = document.getElementById('searchAll').value;
    var lastuu = uu.slice(-1);
    if(lastuu == '&'){
        uu = uu.slice(0,-1);
    }
    document.getElementById('btc0').href = uu;
}

function checkNum(obj) {
     //检查是否是非数字值
     if (isNaN(obj.value)) {

         obj.value = "";
     }
     if (obj != null) {
         //检查小数点后是否对于两位
         if (obj.value.toString().split(".").length > 1 && obj.value.toString().split(".")[1].length > 2) {
             alert("小数点后多于两位！");
             obj.value = "";
         }
     }
 }

function getContent(obj) {
    var ShopNameData = document.getElementById("ShopNameData").innerText.replace(/(^\s*)|(\s*$)/g, "").replace("[", '').replace(']', '');
    ShopNameData = unescape(ShopNameData.replace(/\\u/g, '%u'));
    ShopNameData = ShopNameData.split(",");
    var value17 = jQuery.trim($(obj).val());
    if (value17 == "") {
        $("#append").hide().html("");
        return false;
    }
    var html = "";
    for (var i = 0; i < ShopNameData.length; i++) {
        if (ShopNameData[i].indexOf(value17) >= 0) {
            html = html + "<div class='item' onmouseenter='getFocus(this)' onClick='getCon(this);'>" + ShopNameData[i].replace(/'/g, "").replace('u', '') + "</div>"
        }
    }
    if (html != "") {
        $("#append").show().html(html);
    } else {
        $("#append").hide().html("");
    }
}

function getContent2(obj) {
    var SupplierData = document.getElementById("SupplierData").innerText.replace(/(^\s*)|(\s*$)/g, "").replace("[", '').replace(']', '');
    SupplierData = SupplierData.split(",");
    var value12 = jQuery.trim($(obj).val());
    if (value12 == "") {
        $("#append2").hide().html("");
        return false;
    }
    var html = "";
    for (var i = 0; i < SupplierData.length; i++) {
        if (SupplierData[i].indexOf(value12) >= 0) {
            html = html + "<div class='item' onmouseenter='getFocus(this)' onClick='getCon(this);'>" + decodeURIComponent(SupplierData[i]).replace(/'/g, "") + "</div>"
        }
    }
    if (html != "") {
        $("#append2").show().html(html);
    } else {
        $("#append2").hide().html("");
    }
}
function getContent3(obj) {
    var shopNData = document.getElementById("shopNData").innerText.replace(/(^\s*)|(\s*$)/g, "").replace("[",'').replace(']','');
    shopNData = shopNData.split(",");
    var value3 = jQuery.trim($(obj).val());
    if (value3 == "") {
        $("#append3").hide().html("");
        return false;
    }
    var html = "";
    for (var i = 0; i < shopNData.length; i++) {
        if (shopNData[i].indexOf(value3) >= 0) {
            html = html + "<div class='item' onmouseenter='getFocus(this)' onClick='getCon1(this);'>" + shopNData[i].replace(/'/g,"") + "</div>"
        }
    }
    if (html != "") {
        $("#append3").show().html(html);
    } else {
        $("#append3").hide().html("");
    }
}
function getContent4(obj) {
    var Create_manData = document.getElementById("Create_manData").innerText.replace(/(^\s*)|(\s*$)/g, "").replace("[",'').replace(']','');
    Create_manData = Create_manData.split(",");
    var value5 = jQuery.trim($(obj).val());
    if (value5 == "") {
        $("#append4").hide().html("");
        return false;
    }
    var html = "";
    for (var i = 0; i < Create_manData.length; i++) {
        if (Create_manData[i].indexOf(value5) >= 0) {
            html = html + "<div class='item' onmouseenter='getFocus(this)' onClick='getCon4(this);'>" + Create_manData[i].replace(/'/g,"") + "</div>"
        }
    }
    if (html != "") {
        $("#append4").show().html(html);
    } else {
        $("#append4").hide().html("");
    }
}
function getContent5(obj) {
    var shopNameOfficialData = document.getElementById("shopNameOfficialData").innerText.replace(/(^\s*)|(\s*$)/g, "").replace("[",'').replace(']','');
    shopNameOfficialData = shopNameOfficialData.split(",");
    var value1 = jQuery.trim($(obj).val());
    if (value1 == "") {
        $("#append5").hide().html("");
        return false;
    }
    var html = "";
    for (var i = 0; i < shopNameOfficialData.length; i++) {
        if (shopNameOfficialData[i].indexOf(value1) >= 0) {
            html = html + "<div class='item' onmouseenter='getFocus(this)' onClick='getCon5(this);'>" + shopNameOfficialData[i].replace(/'/g,"") + "</div>"
        }
    }
    if (html != "") {
        $("#append5").show().html(html);
    } else {
        $("#append5").hide().html("");
    }
}
function getContent6(obj) {
        var ShNameData = document.getElementById("ShNameData").innerText.replace(/(^\s*)|(\s*$)/g, "").replace("[",'').replace(']','');
        ShNameData = ShNameData.split(",");
        var value1 = jQuery.trim($(obj).val());
        if (value1 == "") {
            $("#append6").hide().html("");
            return false;
        }
        var html = "";
        for (var i = 0; i < ShNameData.length; i++) {
            if (ShNameData[i].indexOf(value1) >= 0) {
                html = html + "<div class='item' onmouseenter='getFocus(this)' onClick='getCon6(this);'>" + ShNameData[i].replace(/'/g,"") + "</div>"
            }
        }
        if (html != "") {
            $("#append6").show().html(html);
        } else {
            $("#append6").hide().html("");
        }
    }
function getFocus(obj) {
    $(".item").removeClass("addbg");
    $(obj).addClass("addbg");
}

function getCon(obj) {
    var value = $(obj).text();
    $("#value17").val(value);
    $("#append").hide().html("");
}
function getCon1(obj) {
    var value = $(obj).text();
    $("#value3").val(value);
    $("#append3").hide().html("");
}
function getCon4(obj) {
    var value = $(obj).text();
    $("#value5").val(value);
    $("#append4").hide().html("");
}
function getCon5(obj) {
    var value = $(obj).text();
    $("#value1").val(value);
    $("#append5").hide().html("");
}
function getCon6(obj) {
        var value = $(obj).text();
        $("#value1").val(value);
        $("#append6").hide().html("");
}
function fideinfunShow() {
    $('.border1').fadeIn();
    $('#show').hide().html();
    $('#hide').show().html();
}

function fideinfunHide() {
    $('.border1').fadeOut('slow');
    $('#show').show().html();
    $('#hide').hide().html();
}

function clickOpt() {
    var LargeCategory1 = document.getElementById("select_19");
    var LargeCategory1_value = LargeCategory1.value;
    var LargeCategory2 = document.getElementById("select_20");
    var LargeCategory2_length = LargeCategory2.options.length;
    var cat_Dic = document.getElementById("cat_Dic").innerText;
    cat_Dic = unescape(cat_Dic.replace(/\\u/g, '%u')).replace(/u/g, '').replace(/'/g, '"');
    var obj = JSON.parse(cat_Dic);
    var myKey = "zy" + LargeCategory1_value.replace(".", "_");

    if (LargeCategory2_length > 0) {
        for (var i = 0; i < LargeCategory2_length; i++) {
            LargeCategory2.options.remove(0);
        }
        addOption('');
    }
    if (LargeCategory1_value != '') {
        var list = obj[myKey];
        if(list!=undefined) {
            // alert(list);
            for (var i = 0; i < list.length; i++) {
                addOption(list[i])
            }
        }
    }
}

function addOption(val) {
    var LargeCategory2 = document.getElementById("select_20");
    var opt = document.createElement('option');
    opt.text = val;
    LargeCategory2.options.add(opt);
}
var html = "";
function sup_ajax() {
    $.ajax({
        url:"/TestAjax/",
        type:"POST",
        data:{
            "supplier":$("#value12").val(),
            "csrfmiddlewaretoken":$('[name="csrfmiddlewaretoken"]').val()
        },
        success:function (data) {
            html = '';
            var dataObj = JSON.parse(data);
            var supplierName = dataObj["msg"];
            if (value12 == "") {
                $("#append2").hide().html("");
                return false;
            }
            for (var i = 0; i < supplierName.length; i++) {
                html = html + "<div class='item' onmouseenter='getFocus(this)' onClick='getCon_sup(this);'>" + supplierName[i].replace(/'/g, "").replace('u', '') + "</div>"
            }
            if (html != "") {
                $("#append2").show().html(html);
            } else {
                $("#append2").hide().html("");
            }
        }
    })
}
function getCon_sup(obj) {
    var value = $(obj).text();
    $("#value12").val(value);
    $("#append2").hide().html("");
}





function to_change_work(id,key,value,type) {
    $.getJSON('/t_work_flow_of_plate_house/update_info/?id='+id+'&key='+key+'&value='+encodeURI(value)+'&type='+type, function(result){
        var spanshow = document.getElementById(id + '_' + key);
        if (result.Code == '1'){
            spanshow.style.color = 'green';
            spanshow.innerText = '修改成功';
        }else if(result.Code == '-2') {
            alert(result.messages);
            spanshow.style.color = 'red';
            spanshow.innerText = '修改失败';
        }
        else {
            alert('处理异常，请联系it人员处理。messages:' + result.messages);
            spanshow.style.color = 'red';
            spanshow.innerText = '修改失败';
            console.log('处理异常，请联系it人员处理。messages:' + result.messages);
        }
    });
}


// 克重审核需要 在输入值的基础上 加上某个值 在更新
function to_change_weight(id,key,value,type,add_v) {
    if (type == 't_sku_weight_examine' && add_v){
        if (parseInt(value) > 0){
            value = parseInt(value) + parseInt(add_v);
        }else if (parseInt(value) == 0){
            value = 0;
        }else {
            alert('输入的测试值无效！');
            return
        }
    }
    var spanshow = document.getElementById(id + '_' + key);
    spanshow.style.color = 'brown';
    spanshow.innerText = '修改中...';
    $.getJSON('/t_work_flow_of_plate_house/update_info/?id='+id+'&key='+key+'&value='+encodeURI(value)+'&type='+type, function(result){
        if (result.Code == '1'){
            spanshow.style.color = 'green';
            spanshow.innerText = '修改成功';
            var spanvalue = document.getElementById(id);
            spanvalue.value = value;
        }else {
            alert('处理异常，请联系it人员处理。messages:' + result.messages);
            spanshow.style.color = 'red';
            spanshow.innerText = '修改失败';
            console.log('处理异常，请联系it人员处理。messages:' + result.messages);
        }
    });
}


function to_lock(f) {
    // f = 1,上锁；f = 0 解锁
    if(f == 1){
        $('#mainbody').addClass('lock');
    }else if (f == 0){
        $('#mainbody').removeClass('lock');
    }

}

