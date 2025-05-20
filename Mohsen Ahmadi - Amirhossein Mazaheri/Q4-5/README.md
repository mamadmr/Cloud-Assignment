# CTF Platform Backend

This project is a Django-based backend for a Capture The Flag (CTF) platform that dynamically manages Docker containers per team and challenge. It uses Celery for asynchronous task processing and Docker for container orchestration.

---

## Project Structure

```
Q4-5/
├── core/                    # Django core project settings and configuration
│   ├── __init__.py
│   ├── settings.py          # Django settings file
│   ├── urls.py              # Root URL configurations
│   ├── asgi.py
│   └── wsgi.py
├── ctf/                     # Main application with models, views, tasks, etc.
│   ├── __init__.py
│   ├── admin.py             # Admin site configurations
│   ├── apps.py
│   ├── celery.py            # Celery app configuration
│   ├── models.py            # Database models (Team, Challenge, ActiveContainer, ChallengeHistory)
│   ├── serializers.py       # DRF serializers
│   ├── tasks.py             # Celery tasks for starting/stopping containers
│   ├── urls.py              # Application URLs
│   ├── views.py             # API views for challenge assignment and container management
│   └── migrations/          # Django migrations
├── Dockerfile               # Dockerfile to build the Django app image
├── docker-compose.yml       # Docker Compose configuration for services (web, db, redis, celery)
├── manage.py                # Django management CLI tool
├── requirements.txt         # Python dependencies list
└── README.md                # This file
```

---

## Setup and Running Instructions


### Build and Start Containers

In the root directory (`Q4-5`), run:

```bash
docker-compose up --build
```

This command will:

* Build the Django web application image
* Start the database, Redis, web server, and Celery worker containers
* Run database migrations (if configured)

### Create a Django Superuser

To access the Django admin interface, create a superuser by running:

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to enter a username, email, and password.

### Insert Initial Data into Database

You can insert initial teams, challenges, or other data using Django admin panel or Django shell:

```bash
docker-compose exec web python manage.py shell
```

Then create objects like:

```python
from ctf.models import Team, Challenge

Team.objects.create(name="CyberHunters")
Challenge.objects.create(name="Example Challenge", docker_image="example/image", internal_port=8080)
```

---

## API Endpoints

* **Assign Challenge**: `POST api/assign/`  
  Assigns a challenge to a team and starts the container if not running.

* **Remove Challenge**: `POST api/remove/`  
  Stops and removes the container for a given team and challenge.

* **Active Container Info**: `GET api/container-info/`  
  Returns info about an active container for a team and challenge.

---

## Technologies Used

* Django & Django REST Framework
* Docker & Docker Compose
* Celery with Redis as message broker
* PostgreSQL
* Python 3.11

---

## Notes

* Make sure Docker daemon is running before starting.
* The Celery worker handles container start/stop tasks asynchronously.
* Containers are uniquely mapped with host ports to avoid conflicts.



