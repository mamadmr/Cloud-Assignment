import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe("team_requests")

print("Listening for team requests on channel 'team_requests'...")

for item in pubsub.listen():
    if item['type'] == 'message':
        team_message = item['data']  
        print(f"Received: {team_message}")
        
        team_id = team_message.split()[0]
        status = r.get(f"team:{team_id}:request")
        print(f"Status key for '{team_id}': {status}\n")
