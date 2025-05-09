## Problem 1: PostgreSQL

IUTBox link:
<br />
[https://iutbox.iut.ac.ir/index.php/s/f74MfCTo7LRCokG](https://iutbox.iut.ac.ir/index.php/s/f74MfCTo7LRCokG)
<br />

To create a database that holds the records when container is removed we should use docker volumes
we used a named volume that is managed by docker itself, to create a named volume, run following command:
```bash
docker volume create db_data
```
after creating a volume we run the database container:
```bash
docker run -d \
    --name ctf_db \ 
    -e POSTGRES_USER=admin 
    -e POSTGRES_PASSWORD=admin \
    -v db_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:17-alpine3.21
```
flag "-v" binds the previously created named volume to the path which postgres stores its records
and in case of removing the container the records are persisted in a volume and if we run the
same command again we have access to the records that was created before removing the container.
<br />

we can connect to the databse using psql with the following command:
<br />
(psql should be installed separately)
```bash
psql -h localhost -p 5432 -U admin
```
the port and username depends on what we fed to the container.
<br />
<br />

after connecting we should create a new databse:
```sql
create database ctf_db;

\c ctf_db
```
create a new table and add some records:

```sql
create table teams (
    id serial primary key,
    team_name varchar(100) not null,
    challenge_assigned boolean default false
);

insert into teams (team_name) values ('Red Team'), ('Blue Team');
```
we can check created records with:
```sql
select * from teams;
```
to ensure that the records are persisted, we must remove the container and then run it:
```bash
docker remove -f ctf_db
```
after revoming and running again if we connect to the databse and run:
```sql
select * from teams;
```
we must see the previously created records
