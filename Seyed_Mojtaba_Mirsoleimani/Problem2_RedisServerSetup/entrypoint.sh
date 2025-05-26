#!/bin/bash

redis-server --appendonly yes --dir /data &

sleep 2

python3 -u subscriber.py &

sleep 1

python3 publisher.py 

wait
