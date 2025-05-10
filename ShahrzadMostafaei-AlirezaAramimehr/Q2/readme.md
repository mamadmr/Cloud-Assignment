# This command make a container with name of 'redis-container' and map host port 6379 to container port 6379
1- docker run --name redis-container -p 6379:6379 -d docker.arvancloud.ir/redis:latest


# Opens an interactive Bash shell inside the redis-container
2- docker exec -it redis-container /bin/bash


# Inside a container
3- redis-cli


# set a Key and its Value
4- SET <Key> <'Value'>           Set name 'Admin'


# Get Value of a Key
5- Get <Key>                 Get name


# ============================ Connect via localhost ============================


# Install redis-cli
1- sudo apt install redis-tools


# Connect to the redis-container
2- redis-cli -h localhost -p 6379


# Now we are connect to redis-container
3- Get name     # We except to see 'admin'


# =============================== Connect via Lan ===============================


1- Install redis-cli on my windows from this link 'https://github.com/tporadowski/redis/releases'


2- Add it to PATH


# Install verification
3- redis-cli --version


# Get IP address of my Ubuntu which my container is run
4- ip a


# Inside my redis-cli (windows)
5- redis-cli -h <Ubuntu IP> -p 6379


# Now we are connect to redis-container
6- Get name     # We except to see 'admin





