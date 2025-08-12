from fastapi import FastAPI, Depends
from tasks import start_container, stop_container
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://mot:mypassword@localhost:5432/mydb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/assign")
async def assign_challenge(team_id, challenge_id, db=Depends(get_db)):
    image_name = "python:3.12"
    task = start_container.delay(image_name, team_id, challenge_id)
    result = task.get(timeout=20)

    create_table_sql = text("""
    CREATE TABLE IF NOT EXISTS assignments (
        id SERIAL PRIMARY KEY,
        team_id VARCHAR(50),
        challenge_id VARCHAR(50),
        container_id VARCHAR(100),
        container_address VARCHAR(100)
    )
    """)
    db.execute(create_table_sql)

    insert_sql = text("""
    INSERT INTO assignments (team_id, challenge_id, container_id, container_address)
    VALUES (:team_id, :challenge_id, :container_id, :container_address)
    """)
    db.execute(insert_sql, {
        "team_id": team_id,
        "challenge_id": challenge_id,
        "container_id": result['container_id'],
        "container_address": result['container_address']
    })
    db.commit()

    return {"status": "assigned", "container_address": result['container_address']}

@app.post("/remove")
async def remove_challenge(team_id, challenge_id, db=Depends(get_db)):
    query = text("SELECT container_id FROM assignments WHERE team_id=:team_id AND challenge_id=:challenge_id")
    container = db.execute(query, {"team_id": team_id, "challenge_id": challenge_id}).fetchone()
    if not container:
        return {"status": "not found"}

    stop_container.delay(container[0])

    delete_query = text("DELETE FROM assignments WHERE team_id=:team_id AND challenge_id=:challenge_id")
    db.execute(delete_query, {"team_id": team_id, "challenge_id": challenge_id})
    db.commit()

    return {"status": "removed"}
