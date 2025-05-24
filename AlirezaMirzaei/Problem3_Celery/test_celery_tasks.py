#!/usr/bin/env python3
"""
Script to test Celery tasks for container management
"""

import sys
import time
import json
from celery_app.tasks import start_container, stop_container, get_container_status


def print_response(title, response):
    """Print task response in a formatted way"""
    print(f"\n===== {title} =====")
    print(json.dumps(response, indent=2))
    print("=" * (len(title) + 12))


def main():
    """Test Celery container management tasks"""
    if len(sys.argv) < 3:
        print("Usage: python test_celery_tasks.py <challenge_name> <team_id>")
        print("  challenge_name: 'todo-app' or 'juice-shop'")
        print("  team_id: Team identifier (e.g., 'team1')")
        sys.exit(1)

    challenge_name = sys.argv[1]
    team_id = sys.argv[2]

    print(
        f"Testing Celery tasks with challenge '{challenge_name}' for team '{team_id}'..."
    )

    # First, check container status before starting anything
    print("\nChecking initial container status...")
    status = get_container_status.delay(
        team_id=team_id, challenge_name=challenge_name
    ).get()
    print_response("Initial Status", status)

    # Start container
    print("\nStarting container...")
    start_result = start_container.delay(challenge_name, team_id).get()
    print_response("Start Container Result", start_result)

    if start_result.get("status") != "success":
        print("Failed to start container. Exiting.")
        sys.exit(1)

    container_id = start_result["container"]["id"]

    # Wait a moment and check container status
    print("\nWaiting for container to fully start...")
    time.sleep(5)

    status = get_container_status.delay(container_id=container_id).get()
    print_response("Container Status After Start", status)

    # Let the user see the running container
    input("\nPress Enter to stop the container...")

    # Stop container
    print("\nStopping container...")
    stop_result = stop_container.delay(container_id).get()
    print_response("Stop Container Result", stop_result)

    # Check final status
    time.sleep(2)
    status = get_container_status.delay(container_id=container_id).get()
    print_response("Final Container Status", status)

    print("\nTest completed!")


if __name__ == "__main__":
    main()
