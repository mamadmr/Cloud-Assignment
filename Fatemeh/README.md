# Setting PostgreSQL Up
## Pull postgres image
docker pull postgres
## Create volume
docker volume create PG-data
## Run the container
docker run --name PS_ctf -e POSTGRES_PASSWORD=1234  -v PG_data:/var/lib/postgresql/data -p 5432:5432 docker.arvancloud.ir/postgres
## Run sell in the container
docker exec -it PS_ctf sh
## Login as default superuser (postgres)
psql -U postgres
## Create database
CREATE DATABASE ctf_db;
## Create table
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    challenge_assigned INT                  
);
## Insert some data
INSERT INTO teams (team_name, challenge_assigned)
VALUES                    
    ('Green Shoes', 1),
    ('Red Hat', 2);
## Retrive data
SELECT * FROM teams
# Explanation
After pulling the PostgreSQL image, I used the following command for creating its container: 

<span style="color:green">**docker run --name PS_ctf -e POSTGRES_PASSWORD=1234  -v PG_data:/var/lib/postgresql/data -p 5432:5432 -d docker. arvancloud.ir/postgres**</span>

<span style="color:red">**--name** </span>indicates the container's name ( PS_ctf)

<span style="color:red">**-e** </span>
sets the environment variables in this container which tells the PostgreSQL "When you initialize the database, create the default superuser postgres with password 1234.”

<span style="color:red">**-v** </span>
mapped a created volume to a specified path in the container

<span style="color:red">**-p** </span>
map port 5432 on the host to port 5432 inside the container (where PostgreSQL listens by default)

<span style="color:red">**-d** </span> run in background

<span style="color:red">**docker. arvancloud.ir/postgres**</span>
: image's name

# Video
https://iutbox.iut.ac.ir/index.php/apps/files/files/12123051?dir=/&openfile=true
