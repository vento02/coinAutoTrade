#!/bin/bash

. ~ubuntu/.profile
cd $env_autoTrade_Dir

python3 BalanceCheck.py

exit 0