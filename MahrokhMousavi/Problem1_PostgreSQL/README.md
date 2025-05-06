
# Problem 1: PostgreSQL

## 📌 Description

This part of the assignment demonstrates how to:
- Deploy a PostgreSQL container using Docker with persistent storage and a **custom-defined user**.
- Perform basic SQL operations (create database, create table, insert and retrieve data).
- Prove that the data remains available even after stopping and removing the container.

All PostgreSQL data is stored in a Docker-managed volume named `pgdata`, ensuring persistence across container lifecycles.

---

## 🛠️ Steps to Run the Solution

### 1. Create Docker Volume
```bash
docker volume create pgdata
````

### 2. Run PostgreSQL Container with a Custom User

```bash
docker run -d \
  --name my_postgres \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=securepass123 \
  -e POSTGRES_DB=teamdb \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres
```

* `POSTGRES_USER=myuser`: Creates a custom user named `myuser`.
* `POSTGRES_PASSWORD=securepass123`: Sets the password.
* `POSTGRES_DB=teamdb`: Automatically creates a database named `teamdb`.

---

## 🔗 Connect to the PostgreSQL Database

### 3. Access the container and open the psql shell

```bash
docker exec -it my_postgres psql -U myuser -d teamdb
```

### 4. Run SQL Commands

```sql
-- Create a table
CREATE TABLE challenges (
  id SERIAL PRIMARY KEY,
  team_name VARCHAR(50),
  challenge_desc TEXT
);

-- Insert sample data
INSERT INTO challenges (team_name, challenge_desc) VALUES
('Team Alpha', 'Solve the maze problem'),
('Team Beta', 'Implement sorting algorithm');

-- Retrieve data
SELECT * FROM challenges;
```

---

## 🔁 Demonstrate Persistence

* Stop and remove the container:

```bash
docker stop my_postgres
docker rm my_postgres
```

* Re-launch the container with the same volume:

```bash
docker run -d \
  --name my_postgres \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=securepass123 \
  -e POSTGRES_DB=teamdb \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres
```

* Reconnect and verify the data is still there:

```bash
docker exec -it my_postgres psql -U myuser -d teamdb -c "SELECT * FROM challenges;"
```

---

## 💡 Reasoning Behind Decisions

* **Custom user (`myuser`)**: More secure and specific than using the default `postgres` user.
* **Volume (`pgdata`)**: Ensures data persists even if the container is removed or recreated.
* **Direct SQL access inside container**: Simple and direct method for demonstration without needing external tools.

---

## 📷 Screenshots



---

## 🎥 Demonstration Video

Video covers:

* Creating and querying the table
* Restarting the container
* Showing that data persists

📎 [Click here to view the video](https://iutbox.iut.ac.ir/my_link)

---
