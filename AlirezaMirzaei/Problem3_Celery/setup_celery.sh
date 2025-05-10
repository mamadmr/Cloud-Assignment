#!/bin/bash

echo "Setting up Celery with Redis as message broker..."

# Create directory structure
mkdir -p celery_app

# Install required packages
echo "Installing required Python packages..."
pip install celery redis docker

echo "Creating Celery application structure..."
echo "Celery setup completed!"
