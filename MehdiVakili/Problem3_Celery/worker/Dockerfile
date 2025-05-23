FROM python:3.10-slim

RUN pip install celery docker redis

WORKDIR /app
COPY tasks.py /app/tasks.py

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
