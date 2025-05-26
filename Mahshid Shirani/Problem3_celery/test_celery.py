from celery_application import app

@app.task
def ping():
    return 'pong'
