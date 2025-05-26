# Problem 1: PostgreSQL Database Setup

This project sets up a PostgreSQL database environment using Docker Compose.
It provides a ready-to-use PostgreSQL server along with a lightweight web-based management tool (Adminer).

## Services

- **PostgreSQL**: A containerized PostgreSQL server.
- **Adminer**: A web-based UI for managing the PostgreSQL database.

## How to Use

To start the database services, open your terminal in the project directory and run the following command:

```bash
docker compose up --build
```

After the services are running:

- Access Adminer by visiting [http://localhost:8080](http://localhost:8080) in your web browser.
- Connect to the PostgreSQL server and manage your databases and tables through the Adminer interface.

## Data Persistence

The PostgreSQL service uses a Docker volume to ensure that database data persists across container restarts.
Even if you stop and restart the containers, the database data will not be lost.

## How to Stop the Services

To stop and remove the running containers, use the following command:

```bash
docker compose down
```

Note: The data volume created for PostgreSQL will not be deleted automatically when you bring the containers down.
You need to manually remove the volume if you wish to delete the stored data completely.

## Requirements

- Docker must be installed.
- Docker Compose must be installed.
- Port 8080 must be available and not used by another service.

## Screenshots 📸


![image](https://github.com/user-attachments/assets/b65173ba-fd61-45fa-8fc3-96591fadb9a4)


![image](https://github.com/user-attachments/assets/a12d0be0-e5c3-4d9b-9880-3563e319a543)




