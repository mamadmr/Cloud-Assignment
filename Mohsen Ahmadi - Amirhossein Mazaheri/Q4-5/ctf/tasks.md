# CTF Docker Container Management Tasks

This file contains Celery tasks to manage Docker containers for CTF challenges dynamically assigned to teams. The tasks ensure that each team gets a unique container for a challenge and can stop containers as needed.

---

## Tasks Overview

### `start_challenge_container(team_id, challenge_id)`

- **Purpose:**  
  Starts a Docker container for the given team and challenge if one is not already running.

- **Process:**  
  1. Check if an active container already exists for the team and challenge.  
  2. If yes, return its container ID and access URL without starting a new container.  
  3. If no, start a new Docker container using the challenge's Docker image and map the internal port to a host port.  
  4. Record the container details in the `ActiveContainer` model.  
  5. Log the container start event in `ChallengeHistory`.  
  6. Return the new container ID and access URL.

- **Returns:**  
  - If container exists:  
    ```json
    {
      "message": "Container already running",
      "container_id": "...",
      "url": "http://localhost:port"
    }
    ```
  - If new container started:  
    ```json
    {
      "container_id": "...",
      "url": "http://localhost:port"
    }
    ```

---

### `stop_challenge_container(team_id, challenge_id)`

- **Purpose:**  
  Stops and removes the active Docker container for the specified team and challenge.

- **Process:**  
  1. Retrieve the active container entry for the team and challenge.  
  2. Stop and remove the Docker container using the Docker API.  
  3. Update the `ChallengeHistory` entry with the stop timestamp.  
  4. Delete the `ActiveContainer` record.  
  5. Return a confirmation status.

- **Returns:**  
  ```json
  {
    "status": "stopped"
  }
