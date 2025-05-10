# Problem 2: Redis Server Setup 

## What I Did:

- Deployed a Redis server using Docker.
- Wrote two Python programs (publisher and subscriber) for inter-process communication via Redis.
- Verified Redis server accepts client connections (test client).
- Used RedisInsight to monitor data and pub/sub messages visually.
- Documented and recorded a short demo.

-----
#step1->  pull redis image:

docker pull redis


#step2-> Run Redis Server with Docker :

docker run --name redis-server -p 6379:6379 -d redis


#step3-> Test Redis Client (Manual) :
docker exec -it redis-server redis-cli
SET test "hello"
GET test
exit

#step4-> write and run python codes :
- `publisher.py`: Sends messages and sets key-value data in Redis.
- `subscriber.py`: Reads key-value data and subscribes to messages on a Redis channel.
python subscriber.py
python publisher.py
#step5-> install redisinsight
#step6-> check key-values and subscribe and publish massages

#videos and screenshots :
https://iutbox.iut.ac.ir/index.php/s/HqxwwPcePAEg3HQ

