import argparse
from tasks import stop_container

# Set up argument parser
parser = argparse.ArgumentParser(description='Stop a Docker container.')
parser.add_argument('container_id', help='ID or name of the container to stop')
args = parser.parse_args()

# Stop the container
result = stop_container.delay(args.container_id)
print(result.get(timeout=60))

