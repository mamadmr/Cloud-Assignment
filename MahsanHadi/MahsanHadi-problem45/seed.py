from app.database import SessionLocal
from app.models import Team, Challenge

db = SessionLocal()

teams = [
    Team(id=1, name="Team One"),
    Team(id=2, name="Team Two")
]

challenges = [
    Challenge(id=101, name="Nginx Challenge", image_name="nginx"),
    Challenge(id=102, name="Redis Challenge", image_name="redis")
]

db.add_all(teams + challenges)
db.commit()
db.close()

print("Sample data inserted.")