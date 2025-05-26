# Problem 1: Setup PostgreSQL with Docker for CTF Project

---

### Step 1: Create Docker Volume

```bash
docker volume create pgdata
```

This creates a persistent Docker volume named `pgdata` for PostgreSQL DB.

---

### Step 2: Run PostgreSQL Container

```bash
docker run -d \
  --name postgres-ctf \
  -e POSTGRES_USER=ctfer \
  -e POSTGRES_PASSWORD=ctfword \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres
```

This command runs PostgreSQL in a detached container with:
- Username: `ctfer`
- Password: `ctfword`
- Port forwarding: Host `5432` → Container `5432`
- Volume: `pgdata` mounted to store database

---

### Step 3: access the postgresql cli

```bash
docker exec -it postgres-ctf psql -U ctfer
```

This opens an interactive PostgreSQL cli as `ctfer`.

---

### Step 4: SQL Commands

Run the following SQL commands inside the psql cli:

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
