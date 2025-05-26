using virtual environment:
python3 -m venv venv
source venv/bin/activate

requirements:
pip install fastapi uvicorn celery redis sqlalchemy psycopg2-binary

run celery worker:
celery -A app.tasks worker --loglevel=info

run api:
uvicorn app.main:app --reload

checking database in psql:
docker exec -it my_postgres psql -U postgres -d ctf_db

add sample record to database(optional):
python3 seed.py

postman requests:
http://localhost:8000/remove
http://localhost:8000/assign

postman request json body:
{
  "team_id": 1,
  "challenge_id": 101
}