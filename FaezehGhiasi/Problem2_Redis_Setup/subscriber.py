import redis

r = redis.Redis(host='localhost', port=6379)


team1 = r.get('team1').decode()
team2 = r.get('team2').decode()
score1 = r.get('score1').decode()
score2 = r.get('score2').decode()

print(f'Team1: {team1}, Score: {score1}')
print(f'Team2: {team2}, Score: {score2}')


pubsub = r.pubsub()
pubsub.subscribe('ctf_channel')

print('Waiting for new messages...')
for message in pubsub.listen():
    if message['type'] == 'message':
        print('New message:', message['data'].decode())
        break
