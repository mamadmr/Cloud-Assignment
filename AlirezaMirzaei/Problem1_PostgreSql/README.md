# My PostgreSQL Container Setup

This here is a quick way to spin up a PostgreSQL database with my schema and sample data already loaded, so here’s exactly how I did it for this assignment:

1. **Write the initialization script**

   In my project root I created an `init-db.sql` file containing everything I wanted PostgreSQL to run on first boot:

   - Create the database and initialize it.
   - Create necessary tables (teams).
   - Insert value into the tables and initialize them with the data necessary.
   - Some changes to the database and confirmations that are in the container log after running the container.

2. **Create my startup script**

   I wrote `setup-postgres.sh` so I could reproduce this on any machine:

   - The script runs the docker container using the username and credentials provided plainly, this could be parameterized or given as a docker secret but seeing as this is a local installation with no need to access the internet i made it more simple.
   - Then the script initializes, fills and updates the database using the file `init-db.sql`.
   - Then the container status is checked via the command `pg_isready` in a loop.

3. **Verify the result**

   After running `chmod +x setup-postgres.sh` and `./setup-postgres.sh`, I double-checked the container to be running:

   ```
   docker exec -it postgres_ctf \
   psql -U postgres -d ctf_db \
   -c "SELECT * FROM teams;"
   ```

   This should output the final data in the database after any change we make to the `teams` table

4. **Tearing down for a fresh start**

   Whenever I want to start over, I simply do:

   ```
   docker stop postgres_ctf && docker rm postgres_ctf
   docker volume rm postgres_data
   ./setup-postgres.sh
   ```
