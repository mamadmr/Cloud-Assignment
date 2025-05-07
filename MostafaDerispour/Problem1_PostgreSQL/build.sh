sudo docker volume create pgdata

sudo docker run -d \
  --name my_postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=testpass \
  -e POSTGRES_DB=mydatabase \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:latest
