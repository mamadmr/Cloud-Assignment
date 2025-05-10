# Cloud Assignment

Problem 1: Deploy a PostgreSQL Container with Persistent Storage
1.Created a Docker volume:
	docker volume create pgdata
2.Ran PostgreSQL container with environment variables and volume mount:
	docker run --name postgres-container \
        	-e POSTGRES_USER=myuser \
        	-e POSTGRES_PASSWORD=mypassword \
        	-e POSTGRES_DB=mydatabase \
                -v pgdata:/var/lib/postgresql/data \
        	-p 5432:5432 \
                -d postgres
3.Connected to the database using:
	docker exec -it postgres-container psql -U myuser -d mydatabase
4.Ran basic SQL operations:
	CREATE TABLE teams (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
        );

---------------
	INSERT INTO teams (name) VALUES ('Team Alpha'), ('Team Beta');
---------------
	SELECT * FROM teams;
5.Stopped and removed container:
	docker stop postgres-container
	docker rm postgres-container
6.re-ran steps 2,3 again and ran this basic SQL operation again for checking :
	SELECT * FROM teams;
 


