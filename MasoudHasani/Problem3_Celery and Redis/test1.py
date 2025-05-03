from celery_app import add
result = add.delay(4, 6)
print(result.get(timeout=10))
