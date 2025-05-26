# Command Explainations

```bash
sudo docker volume create pgdata
```

* **`sudo`**: Runs the command with superuser privileges.
* **`docker volume create`**: Creates a new Docker-managed volume.
* **`pgdata`**: The name of the volume to be created.

---

```bash
sudo docker run -d \
  --name my_postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=testpass \
  -e POSTGRES_DB=mydatabase \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:latest
```

* **`sudo`**: Runs the command with superuser privileges.
* **`docker run -d`**: Runs the container in detached mode.
* **`--name my_postgres`**: Assigns a custom name to the container.
* **`-e POSTGRES_USER=admin`**: Sets the database admin username.
* **`-e POSTGRES_PASSWORD=testpass`**: Sets the password for the admin user.
* **`-e POSTGRES_DB=mydatabase`**: Creates a default database on startup.
* **`-v pgdata:/var/lib/postgresql/data`**: Mounts the Docker volume to the PostgreSQL data directory.
* **`-p 5432:5432`**: Exposes the PostgreSQL port to the host.
* **`postgres:latest`**: Specifies the Docker image to use.

# Videos Link
https://iutbox.iut.ac.ir/index.php/s/RpzHAzQbQcokCBL
