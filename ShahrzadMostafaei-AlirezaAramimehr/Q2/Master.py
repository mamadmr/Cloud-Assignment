import redis
import json
from random import randint


class Master:
    def __init__(self, range_max):
        self.range = range_max
        self.secret = self.choose_secret()
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe('guesses')
        self.redis_client.set('range', self.range)  
    def choose_secret(self):
        a = randint(1, self.range)
        b = randint(1, self.range)
        return randint(min(a, b), max(a, b))


    def make_response(self, answer):
        if answer > self.secret:
            return 'H'
        elif answer < self.secret:
            return 'L'
        else:
            return 'Correct'


    def run(self):
        print(f"[Master] Secret number is: {self.secret}")
        for message in self.pubsub.listen():
            if message['type'] != 'message':
                continue


            try:
                data = json.loads(message['data'])
                player = data['player']
                guess = int(data['guess'])
                print(f"[Master] {player} guessed {guess}")


                result = self.make_response(guess)


                self.redis_client.publish('responses', json.dumps({
                    'player': player,
                    'result': result
                }))


                if result == 'Correct':
                    self.redis_client.publish('winner', player)
                    print(f"[Master] 🎉 Winner is {player}")
                    break


            except Exception as e:
                print(f"[Master] Error: {e}")


if __name__ == '__main__':
    max_num = int(input("Max Number: "))
    m = Master(range_max=max_num)
    m.run()



