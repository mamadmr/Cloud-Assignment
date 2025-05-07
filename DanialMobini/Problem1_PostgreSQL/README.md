## (a)

```bash
docker build [OPTIONS] PATH 
docker build -t postgres_ctf .
```

- `build` : Build an image from a Dockerfile.

- OPTIONS
  `-t` or `--tag` : Name and Optionally a tag in the 'name:tag' format. If you omit the tag, it defaults to 'latest'.

- PATH
  `.` : The path to the Dockerfile.

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
docker run -d --name postgres_ctf_danial -p 5432:5432 -v postgres_data:/var/lib/postgresql/data postgres_ctf
```

- `run` : Run a command in a new container.

- OPTIONS
  `-d` or `--detach` : Run container in detached mode (in the background).
  `--name` : Assign a name to the container.
  `-p` : Publish a container's port to the host.
  `-v` : Bind mount a volume.

## (b)

```bash
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
docker exec -it postgres_ctf_danial bash
```

- `exec` : Run a command in a running container.
-
- OPTIONS
  `-i` OR `--interactive` : Keep STDIN open even if not attached.
  `-t` OR `--tty` : Allocate a pseudo-TTY.

- `be03881a03521190f94fec53cc3efd4c93c4fbe83e63b65e593dabc278855e33` : The container ID.
- `bash` : The command to run inside the container.

```bash
psql -h localhost -U admin -d ctf_db
```

```sql
-- Create a table to store team information
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    challenge_assigned BOOLEAN DEFAULT FALSE
);

-- Insert sample data into the table
INSERT INTO teams (team_name, challenge_assigned)
VALUES 
    ('Red Team', true),
    ('Blue Team', false);

-- Retrieve all records from the table
SELECT * FROM teams;

-- Update a team's challenge assignment status
UPDATE teams
SET challenge_assigned = true
WHERE team_name = 'Blue Team';

-- Delete a team from the table
DELETE FROM teams
WHERE team_name = 'Red Team';

-- Output:
CREATE TABLE

INSERT 0 2
 id | team_name | challenge_assigned 
----+-----------+--------------------
  1 | Red Team  | t
  2 | Blue Team | f
(2 rows)

UPDATE 1

DELETE 1

```

## (c)

### (i)

اول یک داکر فایل ساختم که در آن دیتا بیس و یوزر ایجاد می شد و به آن یک والیوم اختصاص دادم

### (ii)


