import redis
import json
from random import randint
from threading import Thread


class Slave:
    def __init__(self, name):
        self.name = 'Player_' + name
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.range_max = int(self.redis_client.get('range'))  
        self.a = 1
        self.b = self.range_max
        self.answer = None
        self.found = False


    def choose_answer(self):
        self.answer = randint(self.a, self.b)


    def send_guess(self):
        self.redis_client.publish('guesses', json.dumps({
            'player': self.name,
            'guess': self.answer
        }))
        print(f"[{self.name}] Guessed {self.answer}")


    def handle_response(self):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe('responses')
        try:
            for message in pubsub.listen():
                if message['type'] != 'message':
                    continue
                try:
                    data = json.loads(message['data'])
                    if data['player'] != self.name:
                        continue
                   
                    result = data['result']
                    print(f"[{self.name}] Server says: {result}")


                    if result == 'H':
                        self.b = self.answer - 1
                    elif result == 'L':
                        self.a = self.answer + 1
                    elif result == 'Correct':
                        print(f"[{self.name}] 🎉 I won!")
                        self.found = True
                        return


                    if not self.found:
                        self.choose_answer()
                        self.send_guess()


                except Exception as e:
                    print(f"[{self.name}] Error: {e}")
        finally:
            pubsub.close()


    def listen_for_winner(self):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe('winner')
        try:
            for message in pubsub.listen():
                if message['type'] != 'message':
                    continue
                winner = message['data']
                if winner != self.name:
                    print(f"[{self.name}] 😢 {winner} won the game.")
                return
        finally:
            pubsub.close()


    def run(self):
        self.choose_answer()
        self.send_guess()
        self.handle_response()


if __name__ == '__main__':
    name = input("Name: ")
    s = Slave(name)
    s.run()



