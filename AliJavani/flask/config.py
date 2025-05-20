#config.py
DATABASE_URI = "postgresql://postgres:1234@localhost:5432/ctfdb"
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
