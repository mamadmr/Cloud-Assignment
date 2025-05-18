POST http://localhost:50000/assign-container/
This endpoint creates a container and assings that container to the relevant challenge and team, which must be specified in the body that is sent with the request.

GET http://localhost:50000/active-containers/
We can fetch the information about active containers using this endpoint.

DELETE http://localhost:50000/remove-container/teamID/challengeID
Using this endpoint, we can remove containers assigned to teams and challenges.


This SQL code was used to create the table in postgresql
CREATE TABLE team_challenges (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    team_id VARCHAR(255) NOT NULL,
    challenge_id VARCHAR(255) NOT NULL,
    container_name VARCHAR(255) NOT NULL UNIQUE,
    container_id VARCHAR(255),
    ip_address VARCHAR(45),
    host_port VARCHAR(10)
);


First, we should set up a celery worker using this command
py -3.10 -m celery -A celery_docker_ctf worker --loglevel=info --pool=solo


Use this command to run the APIs using challenge_management.py file
py -3.10 -m uvicorn challenge_management:app --port 50000 --reload

Now, you can test the APIs using postman.


Link of the video
https://iutbox.iut.ac.ir/index.php/s/RwG6zZjtAxrJpGx