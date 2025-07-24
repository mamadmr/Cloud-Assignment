# Problem 1: PostgreSQL

### Step 1: Create a Docker Volume for Persistent Storage
To ensure that PostgreSQL data persists even after container restarts, we will create a Docker volume. The volume will be mounted to the PostgreSQL container to store its data.

```bash
docker volume create postgres_data
```

### Step 2: Run PostgreSQL in a Docker Container
Now that we have a volume for persistent storage, we will run the PostgreSQL container. The following command will set up a PostgreSQL container with environment variables for user credentials, expose the necessary port, and mount the volume for persistent data storage.

```bash
docker run --name my_postgres -e POSTGRES_USER=Sara -e POSTGRES_PASSWORD=password -p 5432:5432 -v postgres_data:/var/lib/postgresql/data -d postgres
```

### Step3: Connect to PostgreSQL
Once the container is running, we need to connect to PostgreSQL using the following command:

```bash
docker exec -it my_postgres psql -U Sara
```

### Step 4: Create a Database and Table and Insert Data
Inside the PostgreSQL interactive session, create a new database and a table to store team information for the CTF competition

```sql
CREATE DATABASE ctf_database;
\c ctf_database

CREATE TABLE teams (
id SERIAL PRIMARY KEY,
team_name VARCHAR(100),
challenge_name VARCHAR(100)
);

INSERT INTO teams (team_name, challenge_name) VALUES ('Team Sara', 'Java To-Do Challenge');
INSERT INTO teams (team_name, challenge_name) VALUES ('Team Moti', 'OWASP Juice Shop');
```

### Step 5: Verify Data Insertion
To verify that the data has been inserted correctly, run the following query:

```sql
SELECT \* FROM teams;

id | team_name | challenge_name
----+-----------+----------------------
1 | Team sara | Java To-Do Challenge
2 | Team moti | OWASP Juice Shop
(2 rows)
```

### Step 6: Test Data Persistence
The next step is to test whether the data persists even after stopping and removing the container. Follow these steps:

```bash
docker stop my_postgres

docker rm my_postgres

docker run --name my_postgres -e POSTGRES_USER=Sara -e POSTGRES_PASSWORD=password -p 5432:5432 -v postgres_data:/var/lib/postgresql/data -d postgres

docker exec -it my_postgres psql -U Sara -d ctf_database
```

```sql
SELECT \* FROM teams;
```

## Video report avalable at https://iutbox.iut.ac.ir/index.php/s/KpDzCLLR88NjWtS