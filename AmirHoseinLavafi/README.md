## Problem 1: PostgreSQL with Persistent Storage


###  Setup Steps

**Start PostgreSQL with a Docker Volume**

The following script (`run.sh`) first remove any container with specific name and runs a PostgreSQL container using a named Docker volume `datavol` to persist data and in the end, it will run psql command inside the container to write sql commands.

In docker run command, -v is for specifying the volume which was already created using docker volume command. it will mount the volume path to where the container stores database data.

## Problem 2: Redis Server Setup

###  Setup Steps

**Start Redis with a Docker bridge network**

The script first remove any container with specific name and runs a redis container with its port 6379 published to port 6379 of the localhost. Then we run two python programs which one of them listen for messages and one of them sending messgaes using the redis container. the python programs also set a value and retrieve it.

## Problem 3: Container Management with Celery and Redis

###  Setup Steps

**Using Celery for managing containers**

First we run the celery worker and after it's ready we run the script which will start a container using start_container.delay() which will execute start_container from tasks.py. Then using .get() we let the starting process finish and we get the container id for stopping it. we can check that the container is ran using docker ps

Link to videos: https://iutbox.iut.ac.ir/index.php/s/nGQ89abHTFMcKz5



