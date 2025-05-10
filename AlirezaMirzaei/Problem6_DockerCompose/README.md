# PostgreSQL Container with Automatic Schema Initialization

This document explains how to set up a PostgreSQL container that automatically initializes with your database schema and sample data when it starts.

## How It Works

PostgreSQL's official Docker image looks for initialization scripts in the `/docker-entrypoint-initdb.d/` directory. Any `.sql`, `.sql.gz`, or `.sh` files in this directory will be executed in alphabetical order when the container is first initialized.

## Setup Instructions

### 1. Create the SQL Initialization Script

Create a file named `init-db.sql` with your database schema and sample data:

```sql
-- Create a new database
CREATE DATABASE ctf_db;

-- Connect to the newly created database
\connect ctf_db;

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
    ('Blue Team', false),
    ('Green Team', false);

-- Update a team's challenge assignment status
UPDATE teams
SET challenge_assigned = true
WHERE team_name = 'Blue Team';

-- Delete a team from the table
DELETE FROM teams
WHERE team_name = 'Red Team';

-- Insert an additional row as requested
INSERT INTO teams (team_name, challenge_assigned)
VALUES ('Yellow Team', true);

-- Final state of the table
SELECT * FROM teams;
```

### 2. Create a Bash Script to Run the Container

Create a file named `setup-postgres.sh`:

```bash
#!/bin/bash

# Create volume for PostgreSQL data persistence
docker volume create postgres_data

# Run PostgreSQL container with initialization
docker run --name postgres_ctf \
  -e POSTGRES_PASSWORD=secretpassword \
  -d \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  -v $(pwd)/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql \
  postgres:latest

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to initialize..."
sleep 5

# Verify container is running
docker ps -a | grep postgres_ctf

echo "PostgreSQL container initialized with your database schema!"
```

### 3. Make the Script Executable and Run It

```bash
chmod +x run-postgres.sh
./setup-postgres.sh
```

## Important Notes

1. **First-Time Initialization Only**: The initialization scripts only run when the container is first created and the data volume is empty. If you stop and restart the container, the scripts will not run again.

2. **Checking Initialization Results**: You can check if your initialization worked by connecting to the database:

   ```bash
   docker exec -it postgres_ctf psql -U postgres -d ctf_db -c "SELECT * FROM teams;"
   ```

3. **For Re-initialization**: If you need to rerun the initialization, you must remove both the container and the volume:

   ```bash
   docker stop postgres_ctf
   docker rm postgres_ctf
   docker volume rm postgres_data
   ./setup-postgres.sh
   ```

## Demonstration

When you run the setup script:

1. A Docker volume named `postgres_data` is created for data persistence
2. The PostgreSQL container starts with the initialization script mounted
3. PostgreSQL automatically executes the initialization script
4. The database, tables, and sample data are created

After the container initialization, your database will contain:
- A database named `ctf_db`
- A table named `teams` with:
  - Blue Team (challenge_assigned = true)
  - Green Team (challenge_assigned = false)
  - Yellow Team (challenge_assigned = true)
- The Red Team row was deleted as per your SQL script

## For Docker Compose Integration

For Docker Compose later on, we will place our initialization script in a directory and map it in the services section:

```yaml
services:
  postgres:
    image: postgres:latest
    environment:
      POSTGRES_PASSWORD: somepassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres-init:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

Then we place our `init-db.sql` file in the `./postgres-init` directory to initialize the db.