#!/bin/bash

# linux cron conf
# crontab -e
# SHELL=/bin/bash
# * * * * * cd /opt/OnlineShopAPIProxyServer/ && ./StartShopAPIProxyServer.sh check

Get_Server_PID(){
    server_pid=`ps -ef | grep "Fancyqube_Online_Shop_API_Proxy_Server.py" | grep -v "grep" | awk '{print $2}'`
    echo "$server_pid"
}

# Get_Server_PID
# server_id=`Get_Server_PID`
# echo "[.] This Server Process PID num: $server_id"

Show_Process_info(){
    # 循环输出换行信息
    server_process=`ps -ef | grep "Fancyqube_Online_Shop_API_Proxy_Server.py" | grep -v "grep"`
    if [ -n "$server_process" ]
    then
        echo "[.] Server Process Running"
        echo "$server_process" | while read i
        do
            echo "[.] Server Process Info : $i"
        done
    else
        echo "[.] No Server Process Running."
    fi
}

Server_Exist(){
    Show_Process_info

    server_pid=`ps -ef | grep "Fancyqube_Online_Shop_API_Proxy_Server.py" | grep -v "grep" | awk '{print $2}'`

    if [ -z "$server_pid" ]
    then
        return 2
    else
        return 1
    fi
}

Kill_Server(){
    Show_Process_info

    server_pid=`ps -ef | grep "Fancyqube_Online_Shop_API_Proxy_Server.py" | grep -v "grep" | awk '{print $2}'`

    if [ -z "$server_pid" ]
    then
        echo "[x] No Server Running."
        return 1
    else
        echo "[.] Killing Server, Waiting..."
        kill -9 $server_pid
        if [ "$?" == "0" ]
        then
            echo "[x] Killed Server!"
        else
            echo "[x] Kill Server Exception!"
        fi
        return 2
    fi
}

Start_Server(){
    nohup python Fancyqube_Online_Shop_API_Proxy_Server.py > /dev/null 2>&1 &
    start_res=$?
    if [ "$start_res" == "0" ]
    then
        echo "[.] Run Command Success!"
        return 1
    else
        echo "[.] Run Command Exception!"
        return 2
    fi
}

Start_Option(){
    Kill_Server

    echo "[.] Starting Server..."

    Start_Server

    Server_Exist
    res=$?

    if [ "$res" = "1" -o "$res" = "0" ]
    then
        echo "[.] Start Server OK!"
    else
        echo "[.] Start Server Error! Please Try again."
    fi
}

Check_Option(){
    Server_Exist
    res=$?
    if [ "$res" = "1" -o "$res" = "0" ]
    then
        echo "[.] Server is Running."
    else
        echo "[.] Server is not Running."
        Start_Option
    fi
}

Main(){
    if [ -z "$1" -o "$1" = "start" -o "$1" = "restart" ]
    then
        echo "[x] Start/Restart Fancyqube Online Shop API Proxy Server."
        Start_Option
    elif [ "$1" = "stop" ]
    then
        echo "[x] Stop Fancyqube Online Shop API Proxy Server."
        Kill_Server
    elif [ "$1" = "status" ]
    then
        echo "[x] Status of Fancyqube Online Shop API Proxy Server."
        Show_Process_info
    elif [ "$1" = "check" ]
    then
        echo "[x] Check Fancyqube Online Shop API Proxy Server."
        Check_Option
    else
        echo "[x] Unknow Option! Please Enter Legal Option!"
    fi
    echo "[x] Running Over Exit."
}

Main $1

exit
