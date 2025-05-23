from time import sleep

import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

values = ["team-red", "team-blue", "team-green"]

for value in values:
    r.delete(value)

for value in values:
    sleep(2)

    r.set(value, "assigned")

    print(f"Assigned {value}")

    r.publish("team-updates", f"{value}/added")


r.publish("team-updates", "close")
