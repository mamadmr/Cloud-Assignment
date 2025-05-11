# PostgreSQL Docker Persistence Demo

This repository provides a step-by-step guide to deploy a PostgreSQL server inside a Docker container with persistent storage, perform basic SQL operations, and verify that your data remains intact across container restarts.

## Table of Contents

* [Prerequisites](#prerequisites)
* [Setup](#setup)

  * [1. Create a Docker Volume](#1-create-a-docker-volume)
  * [2. Run the PostgreSQL Container](#2-run-the-postgresql-container)
* [Usage](#usage)

  * [Connecting to the Database](#connecting-to-the-database)
  * [Basic SQL Operations](#basic-sql-operations)
* [Verifying Persistence](#verifying-persistence)
* [Cleanup](#cleanup)
* [Documentation & Demo Video](#documentation--demo-video)

### 1. Create a Docker Volume

A Docker named volume will store all of PostgreSQL's data outside the container filesystem:

```bash
docker volume create postgreSQL_volume
```

### 2. Run the PostgreSQL Container

Use the official PostgreSQL image and mount the volume:

```bash
docker run -d --name postgreSQL_container \
    -v postgreSQL_volume:/var/lib/postgresql/data \
    -e -e POSTGRES_USER=admin \
    -e POSTGRES_PASSWORD=123 \
    -e POSTGRES_DB=mydb \
    postgres:latest
```

* `POSTGRES_USER`, `POSTGRES_PASSWORD` and `POSTGRES_DB` initialize your admin user and default database.
* `-v postgreSQL_volume:/var/lib/postgresql/data` ensures data is persisted in the `postgreSQL_volume` volume.

## Usage

### Connecting to the Database

Open a `psql` shell inside the running container:

```bash
docker exec -it postgreSQL_container psql -u admin -d mydb
```

### Basic SQL Operations

Once inside `psql`, execute the following commands:

1. **Create a new database**

    ```sql
    CREATE DATABASE application;
    \c application
    ```
2. **Create a table**

    ```sql
    CREATE TABLE apps (
        app_id INT,
        app_name VARCHAR(255) NOT NULL,
        description TEXT,
        developer_id INT,
        category_id INT,
        release_date DATE,
        price DECIMAL(6,2) DEFAULT 0.00,
        current_version VARCHAR(20),
        PRIMARY KEY(app_id)
    );
    ```
3. **Insert sample data**

    ```sql
    INSERT INTO apps VALUES
        (1, 'TodoMaster', 'Task management app', 101, 1, '2021-06-15', 0.00, '2.3.1'),
        (2, 'FitLife', 'Workout and health tracking', 102, 2, '2022-01-20', 4.99, '1.8.0'),
        (3, 'PhotoPix', 'Photo editing tool', 103, 3, '2023-03-05', 0.00, '3.0.5');
    ```
4. **Retrieve and display data**

    ```sql
    SELECT * FROM apps;
    ```

You should see:

```text
           | app_id | app_name    | description                   | developer_id | category_id | release_date | price | current_version
--------+-------------+-------------------------------+--------------+-------------+--------------+-------+-----------------
      1 | TodoMaster  | Task management app           |          101 |           1 | 2021-06-15   |  0.00 | 2.3.1
      2 | FitLife     | Workout and health tracking   |          102 |           2 | 2022-01-20   |  4.99 | 1.8.0
      3 | PhotoPix    | Photo editing tool            |          103 |           3 | 2023-03-05   |  0.00 | 3.0.5
```

## Verifying Persistence

1. **Stop and remove** the container:

   ```bash
   docker stop postgreSQL_container
   docker rm postgreSQL_container
   ```
2. **Relaunch** the container (using the same command in [Setup](#2-run-the-postgresql-container)):

   ```bash
   docker run -d \
     --name postgreSQL_container \
     -e POSTGRES_USER=admin \
     -e POSTGRES_PASSWORD=123 \
     -e POSTGRES_DB=mydb \
     -v postgreSQL_volume:/var/lib/postgresql/data \
     postgres:latest
   ```
3. **Reconnect** and run:

   ```bash
   docker exec -it postgreSQL_container psql -U admin -d application -c "SELECT * FROM apps;"
   ```

Your previously inserted rows should still be present, demonstrating that the data persisted across container restarts.

## Cleanup

To remove all resources when you no longer need them:

```bash
# Stop and remove the container
docker stop postgreSQL_container && docker rm postgreSQL_container

# Remove the volume (WARNING: this deletes all stored data)
docker volume rm postgreSQL_volume
```


