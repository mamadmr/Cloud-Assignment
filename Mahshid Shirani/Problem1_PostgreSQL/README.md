Section A: Deploy a PostgreSQL Container with Persistent Storage

    Create a Docker volume to store PostgreSQL data persistently:

    docker volume create pgdata

    Run a PostgreSQL container with the following configuration:

    docker run -d
    --name my_postgres
    -e POSTGRES_USER=myuser
    -e POSTGRES_PASSWORD=mypass
    -e POSTGRES_DB=mydb
    -v pgdata:/var/lib/postgresql/data
    -p 5432:5432
    postgres

Explanation:

    Environment variables set up the username, password, and initial database.

    The -v flag attaches the pgdata volume to the PostgreSQL data directory, ensuring data is not lost if the container is removed.

    The -p flag maps port 5432 on the host to the container, allowing external connections.

Section B: Perform Basic Database Operations

    Connect to the PostgreSQL container using the psql CLI:

    docker exec -it my_postgres psql -U myuser -d mydb

    Execute the following SQL commands inside the PostgreSQL shell:

    a. Create a table:

    CREATE TABLE students (id SERIAL PRIMARY KEY, name VARCHAR(50), age INT);

    b. Insert data:

    INSERT INTO students (name, age) VALUES ('Alice', 22), ('Bob', 25);

    c. Retrieve and display the data:

    SELECT * FROM students;

Section C: Verifying Persistence

    Stop and remove the container:

    docker stop my_postgres
    docker rm my_postgres

    Re-run the container using the same volume:

    docker run -d
    --name my_postgres
    -e POSTGRES_USER=myuser
    -e POSTGRES_PASSWORD=mypass
    -e POSTGRES_DB=mydb
    -v pgdata:/var/lib/postgresql/data
    -p 5432:5432
    postgres

    Reconnect to the database and verify the data is still present:

    docker exec -it my_postgres psql -U myuser -d mydb
    SELECT * FROM students;

The output should confirm that the previously inserted records (e.g., Alice and Bob) are still available, proving that the Docker volume preserved the data.


