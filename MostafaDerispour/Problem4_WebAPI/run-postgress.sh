sudo docker rm -f ctf_postgress

sudo docker volume create pgdata

sudo docker run -d \
  --name ctf_postgress \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=testpass \
  -e POSTGRES_DB=ctf_database \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:latest
