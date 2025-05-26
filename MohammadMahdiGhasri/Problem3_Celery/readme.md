This is for using in python
pip install celery docker

This command is used to setup a celery worker
py -3.10 -m celery -A celery_docker_ctf worker --loglevel=info --pool=solo

-m celery:
The -m flag tells Python to run the celery module as a script.

-A celery_docker_ctf:
The -A (or --app) option specifies the Celery application instance to use.
celery_docker_ctf is the name of the Python module or package where the Celery app is defined.

worker:
This is the Celery subcommand that starts a worker process.

--loglevel=info:
Sets the logging level for the worker to info.
Celery will output logs at the "info" level or higher.

--pool=solo:
Specifies the concurrency model for the worker.
The solo pool means the worker runs in a single-threaded mode, processing one task at a time.

Then we use 
py -3.10 celery_remove_container.py
and
py -3.10 celery_create_container.py

to create and remove containers using nginx image, with Unique names, IP address and port number.
