run the whole service:
docker-compose up --build

requests:

POST http://localhost:8000/assign
Content-Type: application/json

{
  "team_id": 2,
  "challenge_id": 102
}

POST http://localhost:8000/remove
Content-Type: application/json

{
  "team_id": 1,
  "challenge_id": 101
}