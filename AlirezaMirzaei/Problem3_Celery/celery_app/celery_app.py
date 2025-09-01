#!/usr/bin/env python3
"""
Main Celery application file
"""

from celery import Celery

# Create Celery app
app = Celery("container_manager")

# Load configuration from config file
app.config_from_object("celery_app.celery_config")

# Auto-discover tasks in specified modules
app.autodiscover_tasks(["celery_app.tasks"])

if __name__ == "__main__":
    app.start()
