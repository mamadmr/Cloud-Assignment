
# Setting Up a Persistent PostgreSQL Database Using Docker

This guide explains how to set up a PostgreSQL service using Docker Compose, ensuring that data remains persistent across container restarts or deletions.

---

## Prerequisites

- Docker installed
- Docker Compose installed

---

## Project Structure

```
project-root/
├── docker-compose.yml
└── pgdata/           # Directory to store persistent data
```

---

## Step-by-Step Instructions

### 1. Start the PostgreSQL Service

Run the following command in your project directory:

```bash
docker-compose up -d
```

**Explanation:**
- `docker-compose up`: Starts the services defined in the `docker-compose.yml`.
- `-d`: Runs containers in detached (background) mode.

---

### 2. Connect to PostgreSQL Inside the Container

```bash
docker exec -it ctf_db psql -U ctftest -d ctfdb
```

**Explanation:**
- `docker exec`: Runs a command in a running container.
- `-it`: Interactive terminal mode.
- `ctf_db`: Name of the container.
- `psql`: PostgreSQL client.
- `-U ctftest`: Connect as user `ctftest`.
- `-d ctfdb`: Connect to database `ctfdb`.

---

### 3. Sample SQL Commands

```sql
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
```

---

### 4. Exit the `psql` Shell

To exit:

```sql
\q
```

or press `Ctrl+D`.

---

### 5. Test Data Persistence

1. Stop and remove containers:

```bash
docker-compose down
```

**Explanation:** Stops and removes containers, but data remains because it's stored in a volume.

2. Restart containers:

```bash
docker-compose up -d
```

3. Verify data:

```bash
docker exec -it ctf_db psql -U ctftest -d ctfdb -c "SELECT * FROM teams;"
```

**Explanation:** Executes SQL command directly without entering the interactive shell. `-c` specifies the SQL command to run.

---
🎥 [Watch the video](https://iutbox.iut.ac.ir/index.php/s/zDrfM8Hbxp5WXP9)
---

## Conclusion

With this setup, you can run a PostgreSQL database inside Docker with data persistence, ensuring your data survives container restarts or removal.
