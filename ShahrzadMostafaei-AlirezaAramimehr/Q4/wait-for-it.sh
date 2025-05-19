#!/bin/sh
# wait-for-postgres.sh

set -e

host="postgres"
user="ctf_admin"
db="ctfdb"

until PGPASSWORD=ctf_admin psql -h "$host" -U "$user" -d "$db" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec "$@"
