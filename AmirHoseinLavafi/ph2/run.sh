#!/bin/bash

docker rm -f redisc
docker run --name redisc -d -p 127.0.0.1:6379:6379 redis

