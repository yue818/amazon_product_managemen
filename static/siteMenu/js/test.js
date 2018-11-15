$(function () {

    var json = JSON.parse($('#test_list').val());
    var innerText = $('#attention_text').val();

    function tree(data) {
        for (var i = 0; i < data.length; i++) {
            // var data2 = data[i];
            // console.log(data[i]);
            // console.log(data[i].to_url);
            // console.log(data[i].child.length);
            // console.log('-----------------------------');
            if (data[i].icon == "icon-th") {
                var span_input = ''
                if((data[i].selected == "selected")&&(data[i].to_url != "")) {
                    span_input = "<span class='li_selected' style='font-size: 18px'>" + "<strong><a href='"+ data[i].to_url +"' class='a_selected'>" + data[i].name + "</strong></a></span>";
                }else if(data[i].to_url == ""){
                    span_input = "<span style='font-size: 18px'>" + "<strong>" + data[i].name + "</strong></span>";
                } else {
                    span_input = "<span>" + "<strong><a href='"+ data[i].to_url +"'>" + data[i].name + "</strong></a></span>";
                }
                $("#rootUL").append("<li data-name='" + data[i].code + "'>"+ span_input +"</li>");
            } else {
                var children = $("li[data-name='" + data[i].parentCode + "']").children("ul");
                if (children.length == 0) {
                    $("li[data-name='" + data[i].parentCode + "']").append("<ul></ul>")
                }
                // console.log(data[i].to_url);
                var span_input = ''
                if((data[i].selected == "selected")&&(data[i].to_url != "")) {
                    span_input = "<span class='li_selected'>" + "<a href='"+ data[i].to_url +"' class='a_selected'>" + data[i].name + "</a></span>";
                }else if(data[i].to_url == ""){
                    span_input = "<span style='font-size: 14px'>" + "<strong>" + data[i].name + "</strong></span>";
                } else {
                    span_input = "<span>" + "<a href='"+ data[i].to_url +"'>" + data[i].name + "</a></span>";
                }
                $("li[data-name='" + data[i].parentCode + "'] > ul").append(
                    "<li data-name='" + data[i].code + "' class='tree_li'>" +
                    span_input +
                    "</li>")
            }
            for (var j = 0; j < data[i].child.length; j++) {
                var child = data[i].child[j];
                var children = $("li[data-name='" + child.parentCode + "']").children("ul");
                if (children.length == 0) {
                    $("li[data-name='" + child.parentCode + "']").append("<ul></ul>")
                }
                if((child.selected == "selected")&&(child.to_url != "")) {
                  span_input = "<span class='li_selected'>" + "<a href='"+ child.to_url +"' class='a_selected'>" + child.name + "</a></span>";
                }else if(child.to_url == ""){
                  span_input = "<span>" + "<strong>" + child.name + "</strong></span>";
                } else {
                  span_input = "<span>" + "<a href='"+ child.to_url +"'>" + child.name + "</a></span>";
                }
                $("li[data-name='" + child.parentCode + "'] > ul").append(
                    "<li data-name='" + child.code + "' class='tree_li'>" +
                    span_input +
                    "</li>")
                var child2 = data[i].child[j].child;
                tree(child2)
            }
            tree(data[i]);
        }

    }
    tree(json);
    if(innerText != '') {
        if(document.getElementById("pic")&&innerText){
            document.getElementById("pic").innerHTML = innerText;
        }
    }
});