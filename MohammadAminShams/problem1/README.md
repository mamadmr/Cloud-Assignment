## 🐳 Setup PostgreSQL with Docker for CTF Project

This guide sets up a PostgreSQL database using Docker, creates a sample `ctf_db` database with a `teams` table, and performs some basic SQL operations.

---

### 📦 Step 1: Create Docker Volume

```bash
docker volume create pgdata
```

This creates a persistent Docker volume named `pgdata` to store PostgreSQL data.

---

### 🐘 Step 2: Pull PostgreSQL Image

```bash
docker pull postgres
```

Fetches the latest official PostgreSQL image from Docker Hub.

---

### 🚀 Step 3: Run PostgreSQL Container

```bash
docker run -d \
  --name postgres-ctf \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:latest
```

This command runs PostgreSQL in a detached container named `postgres-ctf` with:
- Username: `admin`
- Password: `admin`
- Port forwarding: Host `5432` → Container `5432`
- Volume: `pgdata` mounted to store database data

---

### ✅ Step 4: Verify the Container is Running

```bash
docker ps
```

Ensure that the PostgreSQL container is up and running.

---

### 🔐 Step 5: Access the PostgreSQL CLI

```bash
docker exec -it postgres-ctf psql -U admin
```

This opens an interactive PostgreSQL shell as user `admin`.

---

### 🗃️ Step 6: SQL Commands

Run the following SQL commands inside the psql shell:

```sql
-- Create a new database
CREATE DATABASE ctf_db;

-- Connect to the new database
\c ctf_db

-- Create a table named 'teams'
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    challenge_assigned BOOLEAN DEFAULT FALSE
);

-- Insert data into the table
INSERT INTO teams (team_name, challenge_assigned)
VALUES ('Red Team', true), ('Blue Team', false);

-- View all teams
SELECT * FROM teams;

-- Update a team
UPDATE teams
SET challenge_assigned = true
WHERE team_name = 'Blue Team';

-- Delete a team
DELETE FROM teams
WHERE team_name = 'Red Team';

-- Final result
SELECT * FROM teams;
```
