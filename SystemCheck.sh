#!/bin/bash

. ~ubuntu/.profile 
cd $env_autoTrade_Dir

python3 SystemCheck_alertBot.py

exit 0

