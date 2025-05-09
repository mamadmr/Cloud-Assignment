import redis
import sys

if len(sys.argv) != 2:
    print("Usage: python requester.py <team_id>")
    sys.exit(1)

team_id = sys.argv[1]
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

r.set(f"team:{team_id}:request", "joined")

message = f"{team_id} requests to join"
r.publish("team_requests", message)

print(f"Sent request: {message}")
