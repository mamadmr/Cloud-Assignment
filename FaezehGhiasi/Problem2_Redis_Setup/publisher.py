import redis

r = redis.Redis(host='localhost', port=6379)

r.set('team1', 'Team Alpha')
r.set('team2', 'Team Beta')
r.set('score1', 100)
r.set('score2', 100)

r.publish('ctf_channel', 'Scores have been updated!')
print('Data set and message published!')
