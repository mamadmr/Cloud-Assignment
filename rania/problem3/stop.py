from celery_config import stop_container
import sys



stop_container.delay(sys.argv[1])
