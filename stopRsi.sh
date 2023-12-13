#!/bin/bash

PID=$(ps -ef | grep UpbitRsiAutoTrade.py | head -n1 | awk {'print $2'})
echo $(ps -ef | grep UpbitRsiAutoTrade.py | head -n1)
echo $PID
kill -9 $PID
echo "==kill check=="
echo $(ps -ef | grep UpbitRsiAutoTrade.py)
echo "==UpbitRsiAutoTrade Stop=="
echo "[$(date)] ==!UpbitRsiAutoTrade Stop!==" >>./nohup.out
