# Hint: SQL Commands for Question 1

```sql
-- Create a new database
CREATE DATABASE ctf_db;


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
```
