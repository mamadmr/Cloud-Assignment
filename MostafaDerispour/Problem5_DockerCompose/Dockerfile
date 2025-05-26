FROM python:3.10-slim

# Install python deps for celery (optional, adjust as needed)
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .