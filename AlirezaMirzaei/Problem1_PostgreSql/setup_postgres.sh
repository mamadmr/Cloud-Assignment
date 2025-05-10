#!/bin/bash

# Create volume for PostgreSQL data persistence
docker volume create postgres_data

# Run PostgreSQL container with initialization
docker run --name postgres_ctf \
  -e POSTGRES_USERNAME=ctfadmin \
  -e POSTGRES_PASSWORD=s#cr#tpasssswithasalt \
  -d \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  -v $(pwd)/initdb.sql:/docker-entrypoint-initdb.d/init-db.sql \
  postgres:14-alpine

# 3. Wait until Postgres is actually ready
echo "Waiting for PostgreSQL to initialize…"
until docker exec postgres_ctf pg_isready -U postgres >/dev/null 2>&1; do
  sleep 1
done

echo "PostgreSQL container initialized with our database schema and data!"
