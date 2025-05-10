======================================= A =======================================


#Celery Initialization


    The Celery class is instantiated with:


        'ctf' (app name).


        broker='redis://localhost:6379/0' (Redis as the message broker).


        backend='redis://localhost:6379/0' (Redis as the result storage).
       


#Task Definition


    The @app.task decorator marks add() as an asynchronous task.


    Workers will execute this function when requested.
   
   
# Run Worker:
celery -A celery_app worker --loglevel=info


# Run tasks.py
python3 tasks.py


# ======================================= B C =======================================




## Files Overview


### 1. celery_app.py
The main Celery configuration file that:
- Creates the Celery app instance
- Sets up broker and backend (typically Redis/RabbitMQ)


### 2. tasks.py
Contains all task definitions that Celery will execute. Example tasks might include:




### 3. test_task.py
A test script that demonstrates how to:
- Call Celery tasks
- Handle task results
- Test task functionality





