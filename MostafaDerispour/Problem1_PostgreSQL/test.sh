VOLUME_NAME="pgdata"
CONTAINER_NAME="my_postgres"
DB_USER="admin"
DB_PASSWORD="secret_password"
DB_NAME="mydatabase"
TABLE_NAME="test"

# Create table if it does not exist
TABLE_CHECK="SELECT to_regclass('$TABLE_NAME');"
CREATE_TABLE="CREATE TABLE IF NOT EXISTS $TABLE_NAME (id SERIAL PRIMARY KEY, name VARCHAR(50));"
INSERT_DATA="INSERT INTO $TABLE_NAME (name) VALUES ('Alice'), ('Bob') ON CONFLICT DO NOTHING;"

# Print current table contents
echo "Current contents of table $TABLE_NAME before insertion:"
sudo docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT * FROM $TABLE_NAME;" 

sudo docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "$TABLE_CHECK" | grep -q "$TABLE_NAME" || \
    sudo docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "$CREATE_TABLE" && \
    sudo docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "$INSERT_DATA"

echo "Database setup completed successfully."
