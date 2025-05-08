``` docker run -d --name rds -p 6390:6379 redis:7.0```

The explaination is the same as before
Int the first client program I set 5 keys to a value and then publish hello followe by an integer to a channel then in the second programm I retrieve all the key and values and then listen to the channel for incoming messages
Using redis insight will be explained in the recorded video

