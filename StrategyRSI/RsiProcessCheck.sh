#!/bin/bash

. ~ubuntu/.profile # ~뒤에 이 파일을 실행 할 사용자 입력
cd $env_autoTrade_RSI_Dir

PID1=$(ps -ef | grep UpbitRsiAutoTrade.py | grep -v "grep" | awk {'print $2'} | head -n1)

ReStartup=0 # 재기동 여부

if [ -z $PID1 ]; then
  python3 RsiProcessCheck_alertBot.py dead
  sleep 1
  nohup python3 -u UpbitRsiAutoTrade.py 2>&1 &
  sleep 1
  python3 RsiProcessCheck_alertBot.py restart
  ReStartup=1
else
  python3 RsiProcessCheck_alertBot.py ok
fi

sleep 3

if [ $ReStartup -eq 1 ]; then
  PID1=$(ps -ef | grep UpbitRsiAutoTrade.py | grep -v "grep" | awk {'print $2'} | head -n1)

  if [ -z $PID1 ]; then
    python3 RsiProcessCheck_alertBot.py fail
  else
    python3 RsiProcessCheck_alertBot.py ok
  fi
fi

exit 0