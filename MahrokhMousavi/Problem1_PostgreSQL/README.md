
# Problem 1: PostgreSQL

## 📌 Description

This part of the assignment demonstrates how to:

- Deploy a PostgreSQL container using Docker with persistent storage and a custom-defined user.
- Perform basic SQL operations (create database, create table, insert, update, delete, and retrieve data).
- Prove that the data remains available even after stopping and removing the container.

All PostgreSQL data is stored in a Docker-managed volume named `pgdata`, ensuring persistence across container lifecycles.

---

## 🛠️ Steps to Run the Solution

### 1. Create Docker Volume
```bash
docker volume create pgdata
````

* Creates a Docker-managed volume named `pgdata`.
* This volume will store PostgreSQL's data files and ensure they persist even after the container is deleted.

---

### 2. Run PostgreSQL Container with a Custom User

```bash
docker run -d \
  --name my_postgres \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=securepass123 \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres
```

#### 🔍 Explanation of the Command:

* `docker run -d`: Runs the container in detached mode (in the background).
* `--name my_postgres`: Names the container `my_postgres` for easy reference.
* `-e POSTGRES_USER=myuser`: Sets up a custom PostgreSQL user named `myuser` with superuser privileges.
* `-e POSTGRES_PASSWORD=securepass123`: Sets the password for the `myuser` account (required).
* `-v pgdata:/var/lib/postgresql/data`: Mounts the volume `pgdata` to PostgreSQL’s internal data directory, so all data is stored persistently outside the container.
* `-p 5432:5432`: Maps port 5432 of the container (PostgreSQL default) to port 5432 on the host machine, allowing external access from clients like `psql` or pgAdmin.
* `postgres`: Uses the official PostgreSQL Docker image.

---

## 🔗 Connect to the PostgreSQL Database

### 3. Access the container and open the psql shell

```bash
docker exec -it my_postgres psql -U myuser -d postgres
```

### 4. Run SQL Commands

```sql
-- Create a new database
CREATE DATABASE ctf_db;

-- Connect to the new database
\c ctf_db

-- Create a table to store team information
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    challenge_assigned BOOLEAN DEFAULT FALSE
);

-- Insert sample data into the table
INSERT INTO teams (team_name, challenge_assigned)
VALUES 
    ('Red Team', true),
    ('Blue Team', false);

-- Retrieve all records from the table
SELECT * FROM teams;

-- Update a team's challenge assignment status
UPDATE teams
SET challenge_assigned = true
WHERE team_name = 'Blue Team';

-- Delete a team from the table
DELETE FROM teams
WHERE team_name = 'Red Team';
```

---

## 🔁 Demonstrate Persistence

### Stop and remove the container:

```bash
docker stop my_postgres
docker rm my_postgres
```

### Re-launch the container with the same volume:

```bash
docker run -d \
  --name my_postgres \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=securepass123 \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres
```

### Reconnect and verify the data is still there:

```bash
docker exec -it my_postgres psql -U myuser -d ctf_db -c "SELECT * FROM teams;"
```

✅ Your data remains available, proving the volume-based persistence works.

---

## 💡 Reasoning Behind Decisions

* **Custom user (`myuser`)**: Helps avoid default account usage and enforces clearer permission control.
* **Docker volume (`pgdata`)**: Persists data outside the container's filesystem. Ensures the database is not lost if the container is removed.
* **Detached container mode (`-d`)**: Keeps terminal free while the database service runs in the background.
* **Host-to-container port mapping (`-p 5432:5432`)**: Makes PostgreSQL accessible from GUI tools like pgAdmin or the `psql` command on the host system.
* **Official PostgreSQL image**: Clean, secure, and up-to-date.

---

## 🎨 Alternative: Use pgAdmin 4 to Connect to PostgreSQL

1. Download and install pgAdmin 4: [https://www.pgadmin.org/download/](https://www.pgadmin.org/download/)
2. Open pgAdmin and create a new server connection:

   * **Name**: any name (e.g., `Local PostgreSQL`)
   * **Host**: `localhost`
   * **Port**: `5432`
   * **Username**: `myuser`
   * **Password**: `securepass123`
3. Connect and expand `Databases → ctf_db → Schemas → Tables`
4. Use the Query Tool to insert and query data visually

---

## 📷 Screenshots

![pgAdmin Screenshot](https://s6.uupload.ir/files/pdadmin_tj5m.png)


---

## 🎥 Demonstration Video

Video covers:

* Creating and querying the table
* Restarting the container
* Showing that data persists

📎 [Click here to view the video](https://iutbox.iut.ac.ir/index.php/s/cgESb7zbT6t88r9)

---

