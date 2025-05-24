-- Create a new database
CREATE DATABASE ctf_db;

-- Connect to the newly created database
\connect ctf_db;

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
    ('Blue Team', false),
    ('Green Team', false);

-- This is just to verify the data was inserted
-- The output will show in the container logs
SELECT * FROM teams;

-- Update a team's challenge assignment status
UPDATE teams
SET challenge_assigned = true
WHERE team_name = 'Blue Team';

-- Delete a team from the table
DELETE FROM teams
WHERE team_name = 'Red Team';

-- Insert an additional row as requested
INSERT INTO teams (team_name, challenge_assigned)
VALUES ('Yellow Team', true);

-- Final state of the table
SELECT * FROM teams;