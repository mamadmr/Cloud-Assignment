from celery_config import start_container

import sys

start_container.delay(sys.argv[1])

