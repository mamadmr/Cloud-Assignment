from flask import Flask, request, jsonify
from tasks import start_container, stop_container
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

# Database connection settings (adjust as needed)
DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_PORT = "5432"
DB_NAME = os.environ.get("POSTGRES_DB", "ctf_db")
DB_USER = os.environ.get("POSTGRES_USER", "admin")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "dani")


def get_db_conn():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


def get_image_name(challenge_id):
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT image_name FROM challenges WHERE id = %s", (challenge_id,)
            )
            row = cur.fetchone()
            return row["image_name"] if row else None


def get_container_id(team_id, challenge_id):
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT container_id FROM team_challenges WHERE team_id = %s AND challenge_id = %s AND container_id IS NOT NULL",
                (team_id, challenge_id),
            )
            row = cur.fetchone()
            return row["container_id"] if row else None


@app.route("/assign-container", methods=["POST"])
def assign_container():
    data = request.json
    team_id = data["team_id"]
    challenge_id = data["challenge_id"]
    image_name = get_image_name(challenge_id)
    if not image_name:
        return jsonify({"error": "Challenge not found"}), 404

    # Start container asynchronously
    result = start_container.delay(team_id, challenge_id, image_name)
    # Wait for task to finish (or use a callback/webhook for production)
    container_info = result.get(timeout=30)
    container_id = container_info["container_id"]
    address = container_info["address"]

    # Store assignment in DB
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO team_challenges (team_id, challenge_id, container_id, address)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (team_id, challenge_id) DO UPDATE
                SET container_id = EXCLUDED.container_id, address = EXCLUDED.address, assigned_at = CURRENT_TIMESTAMP
                """,
                (team_id, challenge_id, container_id, address),
            )
            conn.commit()

    return (
        jsonify({"message": "Container started successfully", "address": address}),
        200,
    )


@app.route("/remove-container", methods=["DELETE"])
def remove_container():
    data = request.json
    team_id = data["team_id"]
    challenge_id = data["challenge_id"]
    container_id = get_container_id(team_id, challenge_id)
    if not container_id:
        return jsonify({"error": "No active container found"}), 404

    # Stop container asynchronously
    stop_container.delay(container_id)

    # Remove assignment from DB
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE team_challenges SET container_id = NULL, address = NULL WHERE team_id = %s AND challenge_id = %s",
                (team_id, challenge_id),
            )
            conn.commit()

    return jsonify({"message": "Remove task submitted"}), 202


@app.route("/active-containers", methods=["GET"])
def active_containers():
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM team_challenges WHERE container_id IS NOT NULL")
            rows = cur.fetchall()
            return jsonify(rows), 200
