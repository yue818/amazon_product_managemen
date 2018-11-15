
$('.clearDd').show();
var okSelect = [];
var oClearList = $(".hasBeenSelected .clearList");
var vaksall = [];  // 所有列集
var other_show = [];  //

var flag = 0;
function show_all_col() {
    var list_length = document.getElementById('model_fields_length');
    var length = list_length.value;
    var lastone = document.getElementById(length + '_' + length); // 获取 最后一个 列标签
    // alert('length====='+length);
    if (flag == 0){ // 打开列选择界面
        flag = 1;
        // alert('111111111111111');
        document.getElementById("oSelectList").style.display='';
        var fname = ''; // 为了获取 原有连接
        var vaks = document.getElementsByName('checkbox_name'); // 所有的 check 对象 不包括 show函数的
        for (var v=0;v<vaks.length;v++){
            var midx = vaksall.indexOf(vaks[v].value);
            if (midx == -1){ //排重 并 将所有的列值放到list中
                vaksall.push(vaks[v].value);  // 英文名
            }
            if (!vaks[v].checked){
                fname = vaks[v].value; //
            }
        }
        var fl = 0;
        if (fname == ''){
            fl = 1;
            fname = vaks[0].value;
        }
        var flink = document.getElementById(fname).value;
        // ? _cols=NID.show_Picture.show_SKU.show_SKUName.show_moreInfo.show_kc.Material.show_transportGoods.show_Category.show_Remark &GoodsStatus=3
        var allparama = (flink.split('?').pop()).split('&');
        var flink_param = '';
        for (var all=0;all<allparama.length;all++){
            if (allparama[all].indexOf('_cols=') != -1){
                flink_param = allparama[all].split('=').pop();
                break
            }
        }
        // alert('flink_param==='+flink_param);
        var flinklist = flink_param.split('.');  //原连接 list
        if (fl == 1){
            flinklist.unshift(fname);
        }
        // alert('flinklist==='+flinklist);
        var fnameall = document.getElementsByName('nowshow'); //所有现有的 连接名
        var fnamelist = new Array();
        for (var fn=0;fn<fnameall.length;fn++){
            var idx = fnamelist.indexOf(fnameall[fn].value);
            // if (idx == -1){
            fnamelist.push(fnameall[fn].value);
            if (fnamelist.length==fnameall.length/2){
                break
            }
            // };
        }
        // alert('-------======'+fnamelist);
        var vaksother = [];
        for (var f=0;f<flinklist.length;f++){
            var midx = vaksall.indexOf(flinklist[f]);
            if (midx == -1){
                var other = vaksother.indexOf(flinklist[f]);
                if (other == -1){
                    vaksother.push(flinklist[f]);  // 仅 show 函数  英文
                }
            }
            if (fl != 1 && flinklist[f] == fname){
                flinklist.splice(f,1);
            }
        }
        var newlist = new Array();
        // alert(fnamelist.length + '====' + flinklist.length);
        if (fnamelist.length == flinklist.length){
            for (var n=0;n<flinklist.length;n++){
                newlist.push(flinklist[n] + '|' + fnamelist[n]);

                var fff = vaksother.indexOf(flinklist[n]);
                if (fff != -1){
                    other_show.push(flinklist[n] + '|' + fnamelist[n]);
                //     var br = '';
                //     if (IDD%4 == 0){
                //         br = '</tr><tr>'
                //     }
                //     lastone.insertAdjacentHTML('afterend', '<td id="' + IDD + '_' + IDD + '">'+
                //         '<input id='+ IDD + ' type="checkbox" name="checkbox_name" value="'+ flinklist[n] +'" checked="checked" />'
                //         + '<label onclick="change(' + "'" + flinklist[n] + "','" + IDD +  "','" + fnamelist[n] + "'" + ')"> '
                //         + fnamelist[n] + '</label></td>' + br);
                //     IDD = IDD + 1;
                }
            }
        }
        // alert('---newlist----======'+newlist);
        okSelect = newlist;
        var infor = '';
        show_all(newlist,infor);

    }else {
      flag = 0;
      document.getElementById("oSelectList").style.display='none';
    }
}


// 保存列宽
//function save_col_widths(flag){
    //alert(flag)
    //$("#col_widths").val('0');
    //var url;
    //var page_url = window.location.href;
    //var url_t = page_url.replace(new RegExp('(&_colwidths=([0-9]+[\\.]*[0-9]*\\,)*[0-9]+[\\.]*[0-9]*)|(_colwidths=([0-9]+[\\.]*[0-9]*\\,)*[0-9]+[\\.]*[0-9]*)', 'g'),'');
    //var col_widths = new Array();
    //var t_handle = $('.rc-handle-container').find('.rc-handle');
    //var t_widths = $('.rc-handle-container')[0].style.width;
    // if(flag == '1'){
      //$.each(t_handle, function(idx, val) {
       // if(idx == 0){
        //  col_widths.push((parseFloat(t_handle[idx].style.left)).toFixed(4));
       // }else if(idx != 0 && idx < t_handle.length){
         // col_widths.push((parseFloat(t_handle[idx].style.left) - parseFloat(t_handle[idx-1].style.left)).toFixed(4));
       // }
      //}); 
      //col_widths.push((parseFloat(t_widths) - parseFloat(t_handle[t_handle.length-1].style.left)).toFixed(4));
     // url = url_t + '&_colwidths='+col_widths.join(',');
    // }else if(flag=='2'){
     // url = url_t;
   // }
   // document.getElementById('condition_form').action = "/change_colcol/" + url;
  //  document.getElementById('condition_form').submit();
//}



function go_url_page() {
    var ids = document.getElementsByName('allshow');

    var rellist = new Array();
    for (var rl=0;rl<ids.length;rl++){
        var idx = rellist.indexOf(ids[rl].value);
        if (idx == -1){
           rellist.push(ids[rl].value);
        };
    } 

   // var col_widths = new Array()
    //var col_dict = new Array();
    //$('#idTableFixed thead tr th').each(function (index, obj) {
      //  col = $("#idTableFixed thead tr th input:hidden:eq("+index+")").val();
        //col_width = $("#idTableFixed thead tr th:eq("+index+")").width(); 
        //col_widths.push(col_width.toFixed(0))
    //})
    
    // var t_handle = $('.rc-handle-container').find('.rc-handle');
    //var t_widths = $('.rc-handle-container')[0].style.width
    // var t_width = ''
    //$.each(t_handle, function(idx, val) {
     // if(idx == 0){
       // col_widths.push((parseFloat(t_handle[idx].style.left)).toFixed(4))
      // }else if(idx != 0 && idx < t_handle.length){
        //col_widths.push((parseFloat(t_handle[idx].style.left) - parseFloat(t_handle[idx-1].style.left)).toFixed(4))   
     // }
    //}); 
    //col_widths.push((parseFloat(t_widths) - parseFloat(t_handle[t_handle.length-1].style.left)).toFixed(4))
        
    var linkname = document.getElementsByName('checkbox_name')[0].value;

    var flink = document.getElementById(linkname).value;
    var linkval = flink.split('?').pop();
    var lastval = linkval.split('&');

    var oldparm = new Array();
    for (var t = 0; t < lastval.length;t++){
      if (lastval[t].indexOf('_cols=') == -1){
          oldparm.push(lastval[t])
      }
    }
    var url = '?_cols=' + rellist.join('.')  // +'&_colwidths='+col_widths.join(',');
    if (oldparm.length >= 1){
        // window.location.href= '?' + oldparm.join('&') + '&_cols=' + rellist.join('.');
        document.getElementById('param').value = oldparm.join('&');
    }
    // alert('---------'+url);
    document.getElementById('condition_form').action = "/change_colcol/" + url;
    document.getElementById('condition_form').submit();
    // if (oldparm.length < 1){
    //   window.location.href= '?_cols=' + rellist.join('.');
    // }else{
    //   window.location.href= '?' + oldparm.join('&') + '&_cols=' + rellist.join('.');
    // }
}
// 以上是 打开显示框和代码处理部分

function change(name,id,verbose_name) {
    var show_idx = other_show.indexOf(name + '|' + verbose_name);
    var check = document.getElementById(id);
    if(show_idx == -1){
        var infor = '';
        if (check.checked){
            check.checked = false;
            var idx = okSelect.indexOf(name + '|' + verbose_name);
            if (idx != -1){
                okSelect.splice(idx,1);
            }
        }else {
            check.checked = true;
            var idx = okSelect.indexOf(name + '|' + verbose_name);
            if (idx == -1){
                okSelect.push(name + '|' + verbose_name);
            }
        }
        show_all(okSelect,infor);
    }else {
        alert('函数显示不允许删除！！！');
        if (check.checked) {
            check.checked = true;
        }else {
            check.checked = false;
        }
    }
};

function show_all(okSelect,infor) {
    for (var i = 0; i < okSelect.length; i++) {
        var vals = okSelect[i].split('|');
        infor += '<div class="selectedInfor selectedShow" ' +
            'ondragover="allowDrop(event)" draggable="true" ondragstart="to_drag(event,this)" ondrop="to_drop(event,this,)">' +
            '<input type="hidden" name="allshow" readonly="readonly" value="' + vals[0] + '">' +
            '<span style="font-size:5px">' + vals[1] + '</span><em onclick="' +
            "delsome('"+ okSelect[i] +"')" +
            '"></em></div>';
    }
    oClearList.html(infor);
}


function delsome(flag) {
    var show_idx = other_show.indexOf(flag);
    if(show_idx == -1) {
        var idxx = okSelect.indexOf(flag);
        var allcheck = document.getElementsByName('checkbox_name');
        if (idxx != -1) {
            okSelect.splice(idxx, 1);
            for (var al = 0; al < allcheck.length; al++) {
                var val = flag.split('|')[0];
                if (allcheck[al].value == val) {
                    if (allcheck[al].checked) {
                        allcheck[al].checked = false;
                    }
                }
            }
        }
        var infor = '';
        show_all(okSelect, infor);
    }else {
        alert('函数显示不允许删除！！！')
    }
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
}

function to_drop(ev,divdom)
{
    ev.preventDefault();
    if(srcdiv[0] == $(divdom).parent()[0] && domdiv != divdom){
        $(divdom).before(domdiv);
    }
    srcdiv = null;
    domdiv = null;
}