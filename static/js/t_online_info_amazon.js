var ACTIONSTORTFLAG = 'TortWordsDealWith_amazon';
$(document).ready(function() {
    $('#'+ACTIONSTORTFLAG).attr('onclick', 'TortWordsDealWith_BatchRemarks()');
});


function TortWordsDealWith_BatchRemarks() {
    if (!check_box_num()){
        alert('请选择需要修改的数据！');
        return null;
    }

    $('#id_amazon_tort_remark').modal({backdrop: 'static', keyboard: false});
}


function submit_tort_remark() {
    $('#action').val(ACTIONSTORTFLAG);

    var myform=$('#changelist-form'); //得到form对象
    var tmptext=$('<input name="batch_remark_text">');
    tmptext.attr("value", $('#batch_remark_id').val());
    myform.append(tmptext);

    $('#id_amazon_tort_remark').modal('hide');
    $.do_action(ACTIONSTORTFLAG, '修改侵权词处理标记');
}