import redis
import json

redisObject = redis.Redis('localhost', 6379, 0)

data = {
    'data1': 'val1',
    'data2': 'val2',
    'data3': 'val3',
    'data4': 'val4'
}

json_data = json.dumps(data)

redisObject.publish('DataFlow', json_data)