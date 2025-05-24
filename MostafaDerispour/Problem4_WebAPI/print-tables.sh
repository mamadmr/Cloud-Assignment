#!/bin/bash

CONTAINER_NAME="ctf_postgress"
DB_USER="admin"
DB_NAME="ctf_database"

# Check if container exists and is running
if ! sudo docker ps | grep -q "$CONTAINER_NAME"; then
    echo "Container $CONTAINER_NAME is not running. Please start it first."
    exit 1
fi

echo "Fetching table records from database $DB_NAME..."
echo "----------------------------------------"

# Show records from teams table
echo "Table: teams"
echo "Records:"
sudo docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT * FROM teams;"
echo "----------------------------------------"

# Show records from containers table
echo "Table: containers"
echo "Records:"
sudo docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT * FROM containers;"
echo "----------------------------------------"

echo "Table data fetch completed."
