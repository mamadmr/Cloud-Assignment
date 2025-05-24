sudo docker rm -f my-redis

sudo docker run --name my-redis -p 6379:6379 -d redis