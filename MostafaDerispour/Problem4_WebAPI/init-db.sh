#!/bin/bash

VOLUME_NAME="pgdata"
CONTAINER_NAME="ctf_postgress"
DB_USER="admin"
DB_PASSWORD="secret_password"
DB_NAME="ctf_database"
TABLE_NAME="test"

# Check if container exists and is running
if ! sudo docker ps | grep -q "$CONTAINER_NAME"; then
    echo "Container $CONTAINER_NAME is not running. Please start it first."
    exit 1
fi

sudo docker cp init.sql "$CONTAINER_NAME":/init.sql

# Check if database exists
echo "Checking if database $DB_NAME exists..."
DB_CHECK="SELECT 1 FROM pg_database WHERE datname='$DB_NAME';"
if ! sudo docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d postgres -c "$DB_CHECK" | grep -q 1; then
    echo "Database $DB_NAME does not exist. Creating it..."
    sudo docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME;"
else
    echo "Database $DB_NAME exists."
fi

# Execute the init.sql file in the database
echo "Executing init.sql in database $DB_NAME..."
sudo docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -f /init.sql

echo "Database initialization completed successfully."