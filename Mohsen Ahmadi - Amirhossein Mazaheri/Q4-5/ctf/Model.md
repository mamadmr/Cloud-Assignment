# CTF Models Documentation

This document explains the Django models used to support a Capture The Flag (CTF) platform using Docker containers to serve challenges dynamically for each team.

---

## 📦 Models Overview

### 1. `Team`

Represents a participating team in the CTF platform.

| Field      | Type              | Description                  |
|------------|-------------------|------------------------------|
| `name`     | CharField (max=100) | Unique name for the team     |

**Example:**

```python
Team(name="CyberHunters")
```

---

### 2. `Challenge`

Represents a single challenge, which is deployed as a Docker container.

| Field            | Type                | Description                                 |
|------------------|---------------------|---------------------------------------------|
| `name`           | CharField (max=100) | Display name of the challenge               |
| `docker_image`   | CharField (max=200) | Docker image name to be used                |
| `internal_port`  | IntegerField        | Port exposed *inside* the container (default: 80) |

**Example:**

```python
Challenge(name="Buffer Overflow", docker_image="ctf/bof:latest", internal_port=1234)
```

---

### 3. `ActiveContainer`

Tracks currently running Docker containers per team/challenge combination.

| Field         | Type               | Description                          |
|---------------|--------------------|--------------------------------------|
| `team`        | ForeignKey(Team)   | Team associated with the container   |
| `challenge`   | ForeignKey(Challenge) | Challenge being run                 |
| `container_id`| CharField(max=100) | Docker container ID                  |
| `host_port`   | IntegerField       | Port exposed on the host machine     |
| `access_url`  | URLField           | Direct URL to access the challenge   |
| `started_at`  | DateTimeField      | Timestamp when the container was started |

---

### 4. `ChallengeHistory`

Logs start/stop events of containers for auditing purposes.

| Field         | Type                 | Description                            |
|---------------|----------------------|----------------------------------------|
| `team`        | ForeignKey(Team)     | Related team                           |
| `challenge`   | ForeignKey(Challenge)| Related challenge                      |
| `container_id`| CharField(max=255)   | ID of the container (unique)           |
| `started_at`  | DateTimeField        | When the container was started         |
| `stopped_at`  | DateTimeField (nullable) | When the container was stopped    |

**Example:**

```python
ChallengeHistory(team=team, challenge=challenge, container_id="abc123", started_at=timezone.now())
```