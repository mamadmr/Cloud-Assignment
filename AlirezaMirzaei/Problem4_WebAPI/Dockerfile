# For dockerizing this part, for the docker-compose based deployment
# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Copy only requirements first for caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Default command (overridden by docker-compose for celery or web)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
