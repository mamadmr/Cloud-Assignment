import redis

r = redis.Redis(host='localhost', port=6379)

r.set('team3', 'CTF3')
r.set('team4', 'CTF4')

r.publish('ctf_channel', 'Challenge started for Team 1')
print("Sent data and published message.")
