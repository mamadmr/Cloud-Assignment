Link to the video: https://iutbox.iut.ac.ir/index.php/s/KGz5DJnGHfF9mFT

### PostgreSQL with Persistent Storage:

Step 1: Create a Docker Volume
In the terminal we run this command to create a volume to store persistant data:
>docker volume create pgdata

Step 2: Run PostgreSQL Container
In terminal we run this command:
>docker run --name postgres-ctf -e POSTGRES_USER=ctfuser -e POSTGRES_PASSWORD=ctfpass -e POSTGRES_DB=ctfdb -v pgdata:/var/lib/postgresql/data -p 5432:5432 -d postgres:latest 

In the command above, we create a new container from the latest official PostgreSQL image and give it the name postgres-ctf.
We set environment variables using the -e flag to define:
a default user (ctfuser)
a password (ctfpass)
and a default database (ctfdb) that will be automatically created at startup.
The -v flag mounts a Docker volume named pgdata to the PostgreSQL data directory inside the container (/var/lib/postgresql/data) to ensure data persistence.
The -p flag maps port 5432 on the host to port 5432 on the container, allowing external access to the PostgreSQL server.
The -d flag runs the container in detached mode, meaning it runs in the background.

step 3: Connect to the database
With the command below, we execute the psql command inside the container to interact with the PostgreSQL database as the user ctfuser, connecting to the ctfdb database
>docker exec -it postgres-ctf psql -U ctfuser -d ctfdb

Step 4: Run command to create a table and insert data into it
>CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    challenge_assigned BOOLEAN DEFAULT FALSE
);

>INSERT INTO teams (team_name, challenge_assigned)
VALUES 
    ('Red Team', true),
    ('Blue Team', false);

Then we run the command below to retrieve all the record from the database:
>SELECT * FROM teams;

Step 5: Stop and remove the container
>docker stop postgres-ctf
>docker rm postgres-ctf

Step 6: Aqain run the container to see of the data is still available
>docker run --name postgres-ctf -e POSTGRES_USER=ctfuser -e POSTGRES_PASSWORD=ctfpass -e POSTGRES_DB=ctfdb -v pgdata:/var/lib/postgresql/data -p 5432:5432 -d postgres:latest
>docker exec -it postgres-ctf psql -U ctfuser -d ctfdb
>SELECT * FROM teams;

By running these command, we will see that the data is still available in the database even if the container is stoped and removed.
