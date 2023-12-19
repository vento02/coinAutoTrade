#!/bin/bash

. ~ubuntu/.profile 
cd $env_autoTrade_Dir

python3 Tprice_alertBot.py

exit 0

