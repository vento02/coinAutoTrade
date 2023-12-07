#!/bin/bash

. ~ubuntu/.profile # ~뒤에 이 파일을 실행 할 사용자 입력
cd $env_autoTrade_RSI_Dir

python3 RsiSystemCheck_alertBot.py

exit 0