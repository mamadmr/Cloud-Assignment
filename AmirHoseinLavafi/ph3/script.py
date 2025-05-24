from tasks import start_container, stop_container
import time

result = start_container.delay("bkimminich/juice-shop")
cont_id = result.get(timeout=10)
stop_container.delay(cont_id)

