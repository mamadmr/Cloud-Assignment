import argparse
from tasks import start_container

# Set up argument parser
parser = argparse.ArgumentParser(description='Start a Docker container from an image.')
parser.add_argument('image_name', help='Name of the Docker image')
parser.add_argument('container_name', help='Name to assign to the container')
args = parser.parse_args()

# Start the container
result = start_container.delay(args.image_name, args.container_name)
print(result.get(timeout=60))


# bkimminich/juice-shop
# pasapples/apjctf-todo-java-app:latest 
