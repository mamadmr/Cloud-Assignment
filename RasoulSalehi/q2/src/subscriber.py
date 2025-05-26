import redis
import json

class ScoreSubscriber:
    def __init__(self, host='localhost', port=6379, channel='ctf_channel'):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)
        self.channel = channel

    def show_scores(self):
        team1 = self.r.get('team1')
        team2 = self.r.get('team2')
        score1 = self.r.get('score1')
        score2 = self.r.get('score2')

        print(f"{team1} => {score1}")
        print(f"{team2} => {score2}")

    def listen_for_updates(self):
        pubsub = self.r.pubsub()
        pubsub.subscribe(self.channel)
        print(f"Listening for updates on '{self.channel}'...")
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                print("🔔 New update received:")
                print(f"Event: {data['event']}")
                print(f"Message: {data['message']}")
                print("Scores:", data['scores'])
                break

if __name__ == '__main__':
    subscriber = ScoreSubscriber()
    subscriber.show_scores()
    subscriber.listen_for_updates()
