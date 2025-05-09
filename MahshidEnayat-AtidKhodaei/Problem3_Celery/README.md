Links to the videos: 
https://iutbox.iut.ac.ir/index.php/s/iDLKHmQHTDiGdyP
https://iutbox.iut.ac.ir/index.php/s/fkQmqGow2HJE2qL

Step 1: Install Docker, Redis and Celery with pip
>pip install celery Redis docker

Step 2: In the celeryconfig.py file, we configureی Celery to use Redis as both the message broker and the result backend
We continue describing each command below:
>broker_url = 'redis://localhost:6379/0'
This setting defines the message broker used by Celery. In this case, Redis is used as the broker, running on localhost and listening on port 6379. The /0 at the end indicates that Redis database number 0 will be used for storing task messages.
** Redis has 16 databases by default (0 to 15). It’s common practice to use separate databases for different purposes. Here, DB 0 is used for task queuing.

result_backend = 'redis://localhost:6379/1'
This setting defines where Celery stores the results of executed tasks. Redis is again used, but this time Redis database number 1 (/1) is used specifically for storing task results.
Using separate Redis databases helps avoid conflicts between queued tasks and stored results:
DB 0 for task messages (broker)
DB 1 for task results (backend)

task_serializer = 'json'
This defines the serialization format used when sending tasks and their arguments.

Step 3:
Startworker.sh file is used to launch the Celery worker. If we run this script in shell and it runs Successfully, it means that we are connected to redis correctly. 
The command we used to run the celery is: celery -A tasks worker --loglevel=info --pool=solo



Step 4: Write celery tasks in tasks.py file
First we define two asynchronous Celery tasks for managing Docker containers:
start_container_task: Launches a container in the background using a specified image, container name, and optional port mapping.
stop_container_task: Stops and removes a container by name, running as a background task.

Step 5: Write Start and Stop Container Functions in docker_utils.py file 
start_ctf_container starts a new Docker container from a specified image. Optionally, it maps ports from the container to the host. The container runs in detached mode (in the background).
stop_ctf_container(...) stops a running Docker container by its name and then removes it completely.

Step 6: Testing
We test the entire system using test.py by starting and stopping multiple containers asynchronously.
- Tasks are executed asynchronously in the background using .delay().
- Return values are stored in Redis and can be accessed later using .get().
- Errors are caught and reported to the user via structured messages.

We wrote 2 programs. First program starts and stops 2 containers. 1 for juice and 1 for pasapple.
The second Program starts and stops 10 containers. 5 for juice and 5 for pasapple. In each program the name and id of the container is printed. Also we can track the state of the containers by "docker ps" command.