FROM python:3.11-slim

WORKDIR /app
RUN pip install celery redis docker
COPY . /app


CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]