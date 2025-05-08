FROM python:3.11-slim

WORKDIR /app
RUN pip install celery redis docker psycopg2-binary
RUN apt-get update
RUN apt-get install -y postgresql-client


COPY . /app

#CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]