Link to the video: https://iutbox.iut.ac.ir/index.php/s/WLw6yypdo6pyB7M

Step 1: Running a redis container with the command below
>docker run --name redis-ctf -p 6379:6379 -d redis
To ensure that the container is running we execute 'docker ps'

Step 2: Create python program
We have a Publisher.py which does 2 things
1. Create a key-value pair and set it in the redis. Then it Sleeps for 5 seconds to allow the subscriber to run and listen to the channel which we want to publish message in.
2. Publishes about 3 messages in channel1.
We have also a Subscriber.py which does 2 things
1. Get the value of the team:pink which is stored in redis by publisher
2. Listen to channel1 and print all the messages received from channel.

Step 3: In the browser part of the Redis Insight we can see the key-values 
For Example:


And in Pub/Sub part we can see the messages published by publisher.
For Example:
