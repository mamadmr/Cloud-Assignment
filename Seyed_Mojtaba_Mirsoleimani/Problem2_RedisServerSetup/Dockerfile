FROM python:3.9-slim

RUN apt-get update && apt-get install -y redis-server

RUN pip install redis

WORKDIR /app
COPY . .

RUN chmod +x entrypoint.sh

VOLUME ["/data"]

ENTRYPOINT ["./entrypoint.sh"]
