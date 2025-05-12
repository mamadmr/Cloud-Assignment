# Problem 3: Celery-Based Docker Container Management

This guide explains how to set up and use the Celery-based system for managing CTF challenge containers in the `Problem3_Celery` folder.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)
- [Running the System](#running-the-system)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Cleanup](#cleanup)

---

## Overview

This solution uses **Celery** (with Redis as a broker) and the **Docker SDK for Python** to start and stop challenge containers asynchronously.  
You can trigger container operations by running simple Python scripts.

---

## Prerequisites

- **Linux** OS
- **Docker** installed and running
- **Python 3.6+**
- **pip** (Python package manager)
- **Redis** server (can be run via Docker)

---

## Setup Instructions

1. **Install Python dependencies:**

   ```bash
   pip install celery docker python-dotenv
   ```

2. **Start a Redis server** (if not already running):

   ```bash
   ddocker run -d -p 6379:6379 --name ctf_redis_db -e REDIS_PASSWORD=12345678 redis:alpine
   (i did use the redis container which i create in question 2)
   ```

---

## Configuration

- Edit the `.env` file to set your desired configuration (Redis URL, default image, DB password, etc.).
- Make sure the Docker network specified in `.env` (default: `ctf-network`) exists, or create it:

  ```bash
  docker network create ctf-network
  ```

---

## Running the System

1. **Start the Celery worker:**

   ```bash
   celery -A conf worker --loglevel=info
   ```

   - If you see permission errors, make sure you are in the `docker` group or run with `sudo` (not recommended for regular use).

2. **Start a challenge container:**

   In a new terminal (with the same environment):

   ```bash
   python3 start.py
   ```

3. **Stop a challenge container:**

   In a new terminal:

   ```bash
   python3 end.py
   ```

---

## Usage

- **start.py**: Triggers a Celery task to start a new challenge container.
- **end.py**: Triggers a Celery task to stop and remove the challenge container.

Check the output of the Celery worker terminal for task results and error messages.

**desierd output**
<img src="./../../shots/q3/Screenshot from 2025-05-12 15-19-42.png" width="400" alt="">
<img src="./../../shots/q3/Screenshot from 2025-05-12 15-20-27.png" width="400" alt="">
---


## Notes

- You can adjust the maximum number of containers, image name, and other settings in the `.env` file.
- For production, consider securing your Redis instance and using more robust error handling.

---


