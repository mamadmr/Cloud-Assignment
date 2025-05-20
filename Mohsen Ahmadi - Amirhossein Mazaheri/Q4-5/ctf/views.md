# CTF Challenge Management API Views

This module defines Django REST Framework API views for managing CTF challenge Docker containers assigned to teams.

---

## API Views Overview

### `AssignChallenge`

- **Endpoint:** POST `api/assign/`  
- **Purpose:**  
  Assigns a challenge to a team by starting a Docker container for that challenge (if not already running).  
- **Process:**  
  1. Validate the `team_id` and `challenge_id` from the request.  
  2. Check if an active container already exists for this team and challenge.  
  3. If yes, return container details with status 200.  
  4. If no, enqueue a Celery task to start a new container and return task info with status 202.

---

### `RemoveChallenge`

- **Endpoint:** POST `api/remove/`  
- **Purpose:**  
  Stops and removes a Docker container assigned to a team for a challenge by enqueuing a Celery task.  
- **Process:**  
  1. Accept `team_id` and `challenge_id` from the request.  
  2. Enqueue Celery task to stop the container.  
  3. Return task info with status 202.

---

### `ActiveContainerInfo`

- **Endpoint:** GET `api/container-info/`  
- **Purpose:**  
  Returns information about an active Docker container for a team and challenge.  
- **Process:**  
  1. Retrieve `team_id` and `challenge_id` from query parameters.  
  2. Fetch the matching `ActiveContainer` record.  
  3. Return container details or 404 if not found.

---