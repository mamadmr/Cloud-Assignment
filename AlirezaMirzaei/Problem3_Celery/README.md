# Celery Container Management Documentation

This document outlines the setup of Celery with Redis for managing Docker containers for CTF challenge environments intended to run in this assignment, per team.

## Overview

The system uses Celery with Redis as a message broker to asynchronously manage Docker containers for CTF challenges. This allows for efficient background processing of container management tasks without blocking the main application.

## Components

1. **Redis**: Message broker for Celery
2. **Celery**: Distributed task queue system
3. **Docker Python SDK**: For interacting with Docker containers
4. **CTF Challenge Containers**:
   - Java To-Do App (`pasapples/apjctf-todo-java-app:latest`)
   - OWASP Juice Shop (`bkimminich/juice-shop`)

## Directory Structure

```
.
├── celery_app/
│   ├── __init__.py
│   ├── celery_app.py      # Main Celery application
│   ├── celery_config.py   # Celery configuration
│   └── tasks.py           # Container management tasks
├── run-celery-worker.sh   # Script to run Celery worker
├── run-celery-test.sh     # Script to test tasks
├── setup-celery.sh        # Setup script
└── test_celery_tasks.py   # Task testing script
```

## Setup Process

### 1. Prerequisites

Before setting up Celery, ensure:

- Redis server is running (The part before this)
- Docker is installed and running
- Python 3.x is installed with pip
- Install the requirements and setup data folder with running the file `setup-celery.sh`.

### 2. Celery Configuration

The Celery configuration uses Redis as both the message broker and result backend:

- Broker URL: `redis://localhost:6379/0`
- Result backend: `redis://localhost:6379/1`
- Task serialization: JSON
- Result expiration: 1 day
- These configs are saved as variables in the celery_config.py and are accessed by the main celery app trying to run the celery agent

### 3. Task Implementation

The implementation includes three main tasks:

1. **Start Container Task**: Creates and starts a Docker container for a specific CTF challenge
2. **Stop Container Task**: Stops a running Docker container
3. **Get Container Status Task**: Retrieves the status of containers

Each task implements error handling and retry mechanisms for robustness.

### 4. Container Management Features

- **Team Isolation**: Containers are named with team IDs to ensure separation
- **Challenge Types**: Supports both Java To-Do App and OWASP Juice Shop challenges
- **Port Mapping**: Automatically maps container ports to host ports
- **Status Checking**: Provides detailed status information about running containers
- **Error Handling**: Gracefully handles errors with detailed logging

## Usage Instructions

### Starting the Celery Worker

Run the Celery worker to process tasks:

```bash
./run-celery-worker.sh
```

### Testing Container Management

To test starting and stopping containers:

```bash
./run-celery-test.sh [challenge-name] [team-id]
```

Example:

```bash
./run-celery-test.sh todo-app team1
```

## Monitoring

You can monitor Celery and Redis activity:

1. **Celery Worker Logs**: Show task execution, success, and failures
2. **Redis Monitor**: Use `redis-cli monitor` to see message broker activity
3. **Docker Container List**: Use `docker ps` to verify container states

## Error Handling

The system handles various error scenarios:

- Connection failures to Redis or Docker
- Container not found errors
- API errors from Docker
- Task execution failures

All errors are logged with detailed information and tasks implement retry mechanisms with exponential backoff.

## Integration Points

This Celery setup integrates with:

1. **Redis Server**: Used as message broker and result backend
2. **Docker Engine**: For container management
3. **Web Application**: Can call these tasks to provision CTF environments

### End. The video links:
https://iutbox.iut.ac.ir/index.php/s/oLbwink98GPyA36
