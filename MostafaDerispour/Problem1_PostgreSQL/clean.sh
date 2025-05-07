#!/bin/bash

CONTAINER_NAME="my_postgres"

# Stop and remove the PostgreSQL container if it exists
if sudo docker ps -a --filter "name=$CONTAINER_NAME" | grep -q "$CONTAINER_NAME"; then
    echo "Stopping and removing container: $CONTAINER_NAME"
    sudo docker stop "$CONTAINER_NAME" && sudo docker rm "$CONTAINER_NAME"
else
    echo "Container $CONTAINER_NAME does not exist."
fi

echo "Container cleanup completed successfully."
