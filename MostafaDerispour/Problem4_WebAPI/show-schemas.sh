#!/bin/bash

CONTAINER_NAME="ctf_postgress"
DB_USER="admin"
DB_NAME="ctf_database"

# Check if container exists and is running
if ! sudo docker ps | grep -q "$CONTAINER_NAME"; then
    echo "Container $CONTAINER_NAME is not running. Please start it first."
    exit 1
fi

echo "Fetching table schemas from database $DB_NAME..."
echo "----------------------------------------"

# Show teams table schema
echo "Table: teams"
echo "Schema:"
sudo docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "\d+ teams"
echo "----------------------------------------"

# Show containers table schema
echo "Table: containers"
echo "Schema:"
sudo docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "\d+ containers"
echo "----------------------------------------"

# Show all foreign key relationships
echo "Foreign Key Relationships:"
echo "----------------------------------------"
sudo docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "
SELECT
    tc.table_schema, 
    tc.constraint_name, 
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM 
    information_schema.table_constraints AS tc 
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
      AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY';"

echo "Schema display completed." 