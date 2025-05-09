## Problem 3: Celery and Redis

IUTBox link:
<br />
[https://iutbox.iut.ac.ir/index.php/s/f74MfCTo7LRCokG](https://iutbox.iut.ac.ir/index.php/s/f74MfCTo7LRCokG)
<br />

We need to run a redis container to integrate with celery:
```bash
docker run -d \
    --name task_broker \
    -p 6379:6379 \
    redis:7.4-alpine
```
we exposed the port to be accessible from outside.

then we need to make a virtual environment to install celery python package:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U "celery[redis]" docker
```
we also need docker package to work with docker with python


### Redis Integration
To make celery use redis as its broker we only have to feed the proper string for celery's broker:
```bash
redis://host:port/0
```
in our case:
```bash
redis://localhost:6379/0
```
by setting this url as celery's broker we enabled redis integration.
<br />
Also we need to use redis for celery's backend which is used for storing tasks return value:
```bash
redis://host:port/1
```
in our case:
```bash
redis://localhost:6379/1
```
now celery work fully with redis.

### Running Celery Worker Process
We must run celery worker process to handle tasks:
```bash
celery -A tasks worker --loglevel=inf
```
which also shows celery logs and if anything goes wrong we can observe by looking at output of this command.


### About Tasks
There are two tasks, one for starting ctf container and the other one for stopping and removing
the container.
We used docker python package to work with docker daemon, start task first pulls the "bkimminich/juice-shop"
image then run a container named ctf_container and then return the container id to the main.py and run the 
stop task after 10 seconds we can observe the docker processes in this 10 seconds window via:
```bash
docker ps
```
after a couple of seconds we can see ctf_container process and after about 10 seconds if we run the command
again the ctf_container is removed from the list which shows that tasks ran successfully.
