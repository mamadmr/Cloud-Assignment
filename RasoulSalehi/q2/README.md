
## Components

1. **Redis Server**: Stores team names and scores, and handles pub/sub messaging
2. **RedisInsight**: Web-based GUI for monitoring Redis data
3. **Publisher**: Python script to update scores and publish notifications
4. **Subscriber**: Python script to display scores and listen for updates

## Docker Compose Configuration

The `docker-compose.yml` file defines two services:

```yaml
version: '3.9'

services:
  redis:
    image: redis
    container_name: redis
    restart: always
    ports:
      - "6379:6379"

  redisinsight:
    image: redis/redisinsight:latest
    container_name: redisinsight
    restart: always
    ports:
      - "5540:5540"
```

### Explanation:

1. **Redis Service**:
   - `image: redis`: Uses the official Redis Docker image
   - `container_name: redis`: Names the container "redis" for easy reference
   - `restart: always`: Automatically restarts if the container stops
   - `ports: - "6379:6379"`: Maps host port 6379 to container port 6379 (default Redis port)

2. **RedisInsight Service**:
   - `image: redis/redisinsight:latest`: Uses the official RedisInsight GUI image
   - `container_name: redisinsight`: Names the container "redisinsight"
   - `restart: always`: Automatically restarts if the container stops
   - `ports: - "5540:5540"`: Maps host port 5540 to container port 5540 (RedisInsight web interface)

## Setup Instructions

1. **Install Docker and Docker Compose** if you haven't already

2. **Start the services**:
   ```bash
   docker-compose up -d
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the publisher** to update scores:
   ```bash
   python publisher.py
   ```

2. **Run the subscriber** to view scores and listen for updates:
   ```bash
   python subscriber.py
   ```

3. **Access RedisInsight** at `http://localhost:5540` to monitor Redis data

## Configuration

- Redis server runs on port 6379
- RedisInsight runs on port 5540
- Default channel name: `ctf_channel`

## Customization

You can modify:
- Team names and scores in `publisher.py`
- Redis connection settings in both Python files
- The pub/sub channel name

## Example Output

**Publisher output**:
```
Scores published and message sent.
```

**Subscriber output**:
```
Team Alpha => 150
Team Beta => 200
Listening for updates on 'ctf_channel'...
🔔 New update received:
Event: score_update
Message: Team scores updated
Scores: {'team1': 'Team Alpha', 'team2': 'Team Beta', 'score1': 150, 'score2': 200}
```

## Cleanup

To stop and remove all containers:
```bash
docker-compose down
```