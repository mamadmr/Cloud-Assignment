# Use the official PostgreSQL image
FROM postgres:latest

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=dani
ENV POSTGRES_DB=ctf_db

# Expose the default PostgreSQL port
EXPOSE 5432

# Use a volume for persistent data storage
VOLUME ["/var/lib/postgresql/data"]
