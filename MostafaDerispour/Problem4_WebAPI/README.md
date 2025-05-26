Project Setup Guide
This guide outlines the steps to set up and run the project, including creating a Python environment, installing dependencies, and starting necessary services.
Prerequisites

Python 3.8 or higher
Docker (for running PostgreSQL and Redis containers)
pip (Python package manager)
Git (optional, for cloning the repository)

Setup Instructions

Create and Activate a Python Virtual Environment
Create a virtual environment to isolate project dependencies:
python -m venv venv

Activate the virtual environment:

On Windows:venv\Scripts\activate


On macOS/Linux:source venv/bin/activate




Install Dependencies
Install the required Python packages listed in requirements.txt:
pip install -r requirements.txt


Run PostgreSQL Container
Start the PostgreSQL database using the provided script:
./run-postgres.sh

This script launches a PostgreSQL container using Docker. Ensure Docker is running before executing this command.

Initialize the Database
Create the necessary database tables by running:
./init-db.sh

This script sets up the database schema and any initial data required for the application.

Run Redis Container
Start the Redis server using the provided script:
./run-redis.sh

This script launches a Redis container using Docker, which is used for task queue management.

Run Celery Worker
Start the Celery worker to handle background tasks:
./run-celery.sh

This script sets up the Celery worker, which depends on the Redis container being active.

Run the Web API
Finally, start the web API server:
./run-webapi.sh

This script launches the web API, making the application fully operational and ready to accept requests.


Notes

Ensure all scripts (run-postgres.sh, init-db.sh, run-redis.sh, run-celery.sh, run-webapi.sh) are executable. If not, run:chmod +x *.sh


Verify that Docker is installed and running before executing the scripts that start containers.
If you encounter issues, check the logs for each service (PostgreSQL, Redis, Celery, and the web API) for troubleshooting.

Running the Application
Once all steps are completed, the application should be fully set up and accessible. You can interact with the web API as needed.

# Videos Link
https://iutbox.iut.ac.ir/index.php/s/RpzHAzQbQcokCBL
