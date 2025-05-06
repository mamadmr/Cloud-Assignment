Problem 1 – PostgreSQL with Persistent Storage using Docker
Setup Command

To run PostgreSQL with persistent data storage using Docker, the following command was used:

docker run --name postgres_ctf -e POSTGRES_USER=ZahraNaderi -e POSTGRES_PASSWORD=zahra -e POSTGRES_DB=ctf_db -v pgdata:/var/lib/postgresql/data -p 5432:5432 -d docker.arvancloud.ir/postgres

• --name postgres_ctf: Names the container postgres_ctf for easier reference
• -e POSTGRES_USER=ZahraNaderi: Sets the default PostgreSQL user
• -e POSTGRES_PASSWORD=zahra: Sets the password for the PostgreSQL user
• -e POSTGRES_DB=ctf_db: Creates a new database named ctf_db
• -v pgdata:/var/lib/postgresql/data: Mounts a Docker volume named pgdata to persist data on disk even if the container is removed
• -p 5432:5432: Maps port 5432 of the host to the container, allowing external connections
• -d docker.arvancloud.ir/postgres: Runs the container in detached mode using the PostgreSQL image from Arvan Cloud (used instead of DockerHub due to access restrictions in Iran)

Video Link
https://iutbox.iut.ac.ir/index.php/s/fKkmP7PHfCDWwYt
