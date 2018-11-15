function removeOptions(selectObj)
    {
        if (typeof selectObj != 'object')
        {
            selectObj = document.getElementById(selectObj);
        }
        // 原有选项计数
        var len = selectObj.options.length;
        for (var i=0; i < len; i++) 
        {
            // 移除当前选项
            selectObj.options[0] = null;
        }
    }
 
    function setSelectOption(selectObj, optionList, firstOption, selected) 
    {
        if (typeof selectObj != 'object')
        {
            selectObj = document.getElementById(selectObj);
        }
        // 清空选项
        removeOptions(selectObj);
        // 选项计数
        var start = 0;
        // 如果需要添加第一个选项
        if (firstOption)
        {
            selectObj.options[0] = new Option(firstOption, '');
            // 选项计数从 1 开始
            start ++;
        }
        var len = optionList.length;
        for (var i=0; i < len; i++) 
        {
            // 设置 option
            selectObj.options[start] = new Option(optionList[i], optionList[i]);
            // 选中项
            if(selected == optionList[i])  
            {
                selectObj.options[start].selected = true;
            }
            // 计数加 1
            start ++;
        }
    }
    
    function changeCatagory1()
    {
        subCata = getSubcata([catagory1.options[catagory1.selectedIndex].value]);
        setSelectOption('p2cname', subCata, 'All', 'All');
        setSelectOption('p3cname', [], 'All', 'All'); 
        setSelectOption('p4cname', [], 'All', 'All'); 
        setSelectOption('p5cname', [], 'All', 'All'); 
    }
    
    
    function changeCatagory2()
    {
        subCata = getSubcata([catagory1.options[catagory1.selectedIndex].value, catagory2.options[catagory2.selectedIndex].value]);
        setSelectOption('p3cname', subCata, 'All', 'All');       
        setSelectOption('p4cname', [], 'All', 'All');    
        setSelectOption('p5cname', [], 'All', 'All'); 
    }
    
    function changeCatagory3()
    {
        subCata = getSubcata([catagory1.options[catagory1.selectedIndex].value, catagory2.options[catagory2.selectedIndex].value, catagory3.options[catagory3.selectedIndex].value]);
        setSelectOption('p4cname', subCata, 'All', 'All');    
        setSelectOption('p5cname', [], 'All', 'All');
    }
    
    function changeCatagory4()
    {
        subCata = getSubcata([catagory1.options[catagory1.selectedIndex].value, catagory2.options[catagory2.selectedIndex].value, catagory3.options[catagory3.selectedIndex].value, catagory4.options[catagory4.selectedIndex].value]);
        setSelectOption('p5cname', subCata, 'All', 'All');
    }
    
    function initCatagory()
    {
        var request = new XMLHttpRequest();
        jsonData = '{}';
        request.onreadystatechange = function()
        {
            if (request.readyState == 4 && request.status == 200)
            {
                jsonData = request.responseText;
                infos = JSON.parse(jsonData)
                allCatagory = infos;
                initSelectByValue()
            }
        }
        request.open("GET", "/static/searchnav/"+platform_name+"_catagory_"+department_desc+".json");
        request.send();
    }


    function getSubcata(obj)
    {
        currList = allCatagory;
        //lv1 catagory
        for(var t = 0; t<obj.length; t++)
        {
            currList = findList(obj[t], currList)
        }
        return convert(currList)
    }
    
    function findList(str, currList)
    {
        for(var i=0;i<currList.length;i++)
        {
            if(str == currList[i]['title'])
            {
                if(currList[i]['value'])
                {
                    return currList[i]['value']
                }
                else
                {
                    return []  
                }
                
            }
        }
        return [] 
    }

    function convert(dictArr)
    {
        result = [];
        for(var i=0; i<dictArr.length; i++)
        {
            result[i] = dictArr[i].title
        }
        return result
    }
    
    function getSearch()
    {   
        values = [catagory1.options[catagory1.selectedIndex].value, catagory2.options[catagory2.selectedIndex].value, catagory3.options[catagory3.selectedIndex].value, catagory4.options[catagory4.selectedIndex].value, catagory5.options[catagory5.selectedIndex].value]        
        
        sourceurl = window.location.href
        
        for(var i = 0;i< values.length; i++)
        {
            if(values[i] == ''||values[i] == 'All' )
            {
                values[i] = ''
            }
            sourceurl = changeParam(sourceurl, "_p_"+ cata_desc + (i+1), escape(values[i]));
        } 
        
        window.location.href=sourceurl
    }
    
    function changeParam(sourceurl,pname,pvalue)
    {
        var newUrl="";
        var reg = new RegExp(pname +"=([^&]*)");
        var namedValue = sourceurl.match(reg);

        namedValueStr = pname+"="+pvalue
        
        if(namedValue != null)
        {
            if(pvalue == '')
            {
                newUrl = sourceurl.replace("&"+namedValue[0],'').replace(namedValue[0],'')
            }
            else
            {
                newUrl = sourceurl.replace(namedValue[0],namedValueStr); 
            }
        }
        else
        {
            if(pvalue == '')
            {
                newUrl = sourceurl
            }
            else if(sourceurl.match("[\?]"))
            {
                newUrl = sourceurl + "&" + namedValueStr;
            }
            else
            {
                newUrl = sourceurl + "?" + namedValueStr;
            }
        }
        return newUrl
    }
    
    
    function cleared()
    {
        setSelectOption('p1cname', getSubcata([]), 'All', 'All');
        setSelectOption('p2cname', [], 'All', 'All');
        setSelectOption('p3cname', [], 'All', 'All'); 
        setSelectOption('p4cname', [], 'All', 'All'); 
        setSelectOption('p5cname', [], 'All', 'All'); 
    }
    
    function initSelectByValue()
    {   
        var para=window.location.search;                
        
        cata1 = getQueryString(para, '_p_'+cata_desc+'1');
        cata2 = getQueryString(para, '_p_'+cata_desc+'2');
        cata3 = getQueryString(para, '_p_'+cata_desc+'3');
        cata4 = getQueryString(para, '_p_'+cata_desc+'4');
        cata5 = getQueryString(para, '_p_'+cata_desc+'5');
        
        setSelectOption('p1cname', getSubcata([]), 'All', cata1); 
        changeCatagory1();
       
        if(cata2 != null)
        {    
            setSelectOption('p2cname', getSubcata([cata1]), 'All', cata2);   
            changeCatagory2();
            if(cata3 != null)
            {
                setSelectOption('p3cname', getSubcata([cata1, cata2]), 'All', cata3);   
                changeCatagory3();
                if(cata4 != null)
                {
                    setSelectOption('p4cname', getSubcata([cata1, cata2, cata3]), 'All', cata4);   
                    changeCatagory4();
                    
                    if(cata5 != null)
                    {
                        setSelectOption('p5cname', getSubcata([cata1, cata2, cata3,cata4]), 'All', cata5);   
                    }
                }
            }
        }
        
    }
    
    function getQueryString(paraPart,pname) 
    {
        var reg = new RegExp(pname+"=([^&]*)");
        var namedValue = paraPart.match(reg);
        if (namedValue != null) 
        {
            return unescape(namedValue[1]).replace(/\+/g,' ');
        }
        return null;  
    }     
    
    function refreshCatagory()
    {
        //initCatagory()
    }
    
    allCatagory = []
    catagory1 = document.getElementById('p1cname');
    catagory2 = document.getElementById('p2cname');
    catagory3 = document.getElementById('p3cname');
    catagory4 = document.getElementById('p4cname');
    catagory5 = document.getElementById('p5cname');
    cata_department_info = document.getElementById("cata_department_desc");
    platform_name=cata_department_info.getAttribute("cata_of_platform");
    department_desc=cata_department_info.getAttribute("cata_department_desc");
    cata_desc = 'cata'
    if(platform_name == 'amazon')
    {
        cata_desc = 'group'
    }    
    initCatagory()