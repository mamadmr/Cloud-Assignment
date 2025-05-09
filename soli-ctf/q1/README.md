
---

## PostgreSQL Service with Docker Compose

This project provides a Docker Compose configuration to set up a PostgreSQL database service for the **soli-ctf** environment.

### Features
- Runs the latest version of PostgreSQL.
- Persistent data storage using Docker volumes.
- Configurable database credentials.
- Automatically restarts in case of failure.

### Configuration Details

#### Docker Compose Version
- **Version**: `3.9`

#### Services Provided
1. **PostgreSQL Database**
   - **Image**: `postgres:latest`
   - **Container Name**: `postgres-soli-ctf`
   - **Environment Variables**:
     - `POSTGRES_USER`: `ctf_soli`  
       (Default database username)
     - `POSTGRES_PASSWORD`: `ctf_soli_pass`  
       (Default database password)
     - `POSTGRES_DB`: `ctf_soli_db`  
       (Default database name)
   - **Volumes**:
     - `solipg`: Persists data at `/var/lib/postgresql/data`.
   - **Ports**:
     - Exposed on `5432` (host) → `5432` (container).
   - **Restart Policy**: `always` (Ensures service availability).

#### Volumes
- **solipg**: Stores PostgreSQL data persistently, so database data remains intact even if the container is removed.

### How to Use

1. **Install Docker and Docker Compose**  
   Ensure you have Docker and Docker Compose installed on your system.

2. **Start the Services**  
   Run the following command in the directory containing the `docker-compose.yml` file:
   ```bash
   docker-compose up -d
   ```
   This will start the PostgreSQL service in detached mode.

3. **Access the Database**  
   Connect to the database using any PostgreSQL client with the following credentials:
   - **Host**: `localhost`
   - **Port**: `5432`
   - **Username**: `ctf_soli`
   - **Password**: `ctf_soli_pass`
   - **Database**: `ctf_soli_db`

4. **Stop the Services**  
   To stop the services, run:
   ```bash
   docker-compose down
   ```

5. **Persistent Data**  
   The database data is stored in the `solipg` volume. To remove the volume, use:
   ```bash
   docker-compose down -v
   ```

### Notes
- This configuration is ideal for local development and testing.
- For production use, ensure you secure sensitive credentials and configure proper networking.

--- 

Feel free to modify this based on additional project requirements or details!
