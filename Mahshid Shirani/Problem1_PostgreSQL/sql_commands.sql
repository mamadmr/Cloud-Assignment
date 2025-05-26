-- (a) Create a table
CREATE TABLE students (id SERIAL PRIMARY KEY, name VARCHAR(50), age INT);

-- (b) Insert some data
INSERT INTO students (name, age) VALUES ('Alice', 22), ('Bob', 25);

-- (c) Retrieve the data
SELECT * FROM students;
