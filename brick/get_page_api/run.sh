#!/bin/bash
nohup ./amazon-proxy-10001 >> amazon-proxy-10001.log &
nohup python amazon-get-10002.py >> amazon-get-10002.log &
nohup python ali1688-proxy-10003.py >> ali1688-proxy-10003.log &
nohup python wish-proxy-10004.py >> wish-proxy-10004.log &
nohup python ebay-proxy-10005.py >> ebay-proxy-10005.log &
nohup python aliexpress-proxy-10006.py >> aliexpress-proxy-10006.log &

