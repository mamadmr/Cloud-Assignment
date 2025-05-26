import redis
import json

class ScorePublisher:
    def __init__(self, host='localhost', port=6379, channel='ctf_channel'):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)
        self.channel = channel

    def publish_scores(self, scores):
        for key, value in scores.items():
            self.r.set(key, value)
        message = {
            "event": "score_update",
            "message": "Team scores updated",
            "scores": scores
        }
        self.r.publish(self.channel, json.dumps(message))
        print("Scores published and message sent.")

if __name__ == '__main__':
    scores = {
        "team1": "Team Alpha",
        "team2": "Team Beta",
        "score1": 150,
        "score2": 200
    }
    publisher = ScorePublisher()
    publisher.publish_scores(scores)
