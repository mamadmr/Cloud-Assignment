This docker-compose.yml file sets up a multi-container environment for a Django-based CTF (Capture the Flag) management system 
using the following services:

    web: Runs the Django application. On container startup, it applies database migrations and then starts the development server on port 8000.

    celery: A Celery worker to handle asynchronous background tasks. It shares the application codebase with the web container and connects to Redis as a broker.

    postgres: A PostgreSQL database instance configured with user ctf_admin and database ctfdb, exposed on port 55432.

    redis: A Redis service that functions as the Celery message broker.

All containers are connected via a shared Docker network named ctf-net, allowing them to communicate with each other using their
service names.

How to Run:
1- docker-compose up --build

2- Access the web API at:
	http://localhost:8000/api/add-user
	http://localhost:8000/api/start-container
	http://localhost:8000/api/remove-container
	http://localhost:8000/api/stop-container

