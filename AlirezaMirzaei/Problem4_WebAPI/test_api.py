#!/usr/bin/env python3
"""
A more complete test script for the CTF Challenge Manager API,
including Celery connectivity check and assign/remove flows.
"""

import os
import time
import argparse
import requests

# Load .env if present
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_URL", "http://localhost:8000")

# Check Celery broker connection
from celery_app import celery_app

ping = celery_app.control.ping(timeout=1)
if not ping:
    print("[!] Celery broker not reachable. Ping returned:", ping)
    exit(1)
print("[+] Celery broker reachable:", ping)


def assign(team_id: int, challenge_id: int) -> dict:
    url = f"{BASE_URL}/assign"
    resp = requests.post(url, json={"team_id": team_id, "challenge_id": challenge_id})
    if resp.ok:
        data = resp.json()
        print(f"[+] Assigned: {data}")
        return data
    else:
        print(f"[!] Assign failed {resp.status_code}: {resp.text}")
        exit(1)


def remove(team_id: int, challenge_id: int) -> dict:
    url = f"{BASE_URL}/remove"
    resp = requests.post(url, json={"team_id": team_id, "challenge_id": challenge_id})
    if resp.ok:
        data = resp.json()
        print(f"[+] Removed: {data}")
        return data
    else:
        print(f"[!] Remove failed {resp.status_code}: {resp.text}")
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CTF API Tester")
    parser.add_argument("--team", type=int, default=1, help="Team ID to use")
    parser.add_argument(
        "--challenge", type=int, default=2, help="Challenge ID to assign/remove"
    )
    parser.add_argument(
        "--wait", type=int, default=10, help="Seconds to wait before removal"
    )
    args = parser.parse_args()

    result = assign(args.team, args.challenge)
    print(f"[.] Waiting {args.wait} seconds before removal...")
    time.sleep(args.wait)
    remove(args.team, args.challenge)
