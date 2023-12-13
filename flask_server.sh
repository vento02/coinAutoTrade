#!/bin/bash

nohup python3 -u flask_server.py &

tail -f ./nohup.out