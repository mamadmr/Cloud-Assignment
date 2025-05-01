import psycopg2
from psycopg2 import sql

DB_NAME = "newdb"
USER = "postgres"
PASSWORD = "ERFAN1234"
PORT = 15432
try:
    conn = psycopg2.connect(
        host="localhost",
        port=PORT,
        database="postgres",
        user=USER,
        password=PASSWORD

    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
    exists = cur.fetchone()

    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(DB_NAME)
        ))
        print(f"Database '{DB_NAME}' created.")
    else:
        print(f"Database '{DB_NAME}' already exists.")

    cur.close()
    conn.close()

    conn = psycopg2.connect(
        host="localhost",
        port=PORT,
        database=DB_NAME,
        user=USER,
        password=PASSWORD
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
    """)
    while (1):
        print("1. Insert data")
        print("2. Select data")
        print("3. Exit")
        option = int(input())
        if (option == 1):
            try:
                name = input("name: ")
                cur.execute("INSERT INTO test_table (name) VALUES (%s);",
                            (name,))
                conn.commit()
            except Exception as e:
                print("Error:", e)

        elif (option == 2):
            cur.execute("SELECT * FROM test_table;")
            rows = cur.fetchall()
            for row in rows:
                print(row)
        elif (option == 3):
            print("Exiting...")
            exit(0)
            cur.close()
            conn.close()


except Exception as e:
    print("Error:", e)
