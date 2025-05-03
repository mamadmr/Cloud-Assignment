docker volume create pgdata

docker pull postgres

docker run -d \
  --name postgres-ctf \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:latest

docker ps

docker exec -it postgres-ctf psql -U admin

# then execute sql commands below

CREATE DATABASE ctf_db;
\c ctf_db
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    challenge_assigned BOOLEAN DEFAULT FALSE
);
INSERT INTO teams (team_name, challenge_assigned) VALUES ('Red Team', true), ('Blue Team', false);
SELECT * FROM teams;
UPDATE teams SET challenge_assigned = true WHERE team_name = 'Blue Team';
DELETE FROM teams WHERE team_name = 'Red Team';
SELECT * FROM teams;