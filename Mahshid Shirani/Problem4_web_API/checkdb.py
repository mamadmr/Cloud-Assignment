from database import SessionLocal, Container

db = SessionLocal()
for row in db.query(Container).all():
    print(row.team_id, row.challenge_id, row.container_id, row.host_port)
db.close()
