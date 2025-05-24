"""
Celery configuration file
"""

# Broker settings
broker_url = "redis://localhost:6379/0"

# Result backend settings
result_backend = "redis://localhost:6379/1"

# Task serialization format
task_serializer = "json"

# Result serialization format
result_serializer = "json"

# Accepted content types
accept_content = ["json"]

# Task result expires in 1 day
result_expires = 86400

# Enable task events for monitoring
worker_send_task_events = True
task_send_sent_event = True

# Logging
worker_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
worker_task_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s"
