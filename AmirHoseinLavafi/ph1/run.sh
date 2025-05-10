#!/bin/bash

docker rm -f psql
docker run --name psql -e POSTGRES_PASSWORD=123 -it -v datavol:/var/lib/postgresql/data -d postgres
sleep 3
docker exec -it psql psql -U postgres -d postgres
