'''Example on how to copy data from one database to the other'''
import sqlite3

SCHEMA_SQL = "CREATE TABLE people (name TEXT, id INT)"
INSERT_SQL = "INSERT INTO people VALUES (?, ?)"
GET_SQL = "SELECT * FROM people"
COUNT = 100

def setup_dbs():
    "Setup source and destination databases, create schema and populate source"
    src = sqlite3.connect(":memory:")
    dest = sqlite3.connect(":memory:")
    for conn in (src, dest):
        cursor = conn.cursor()
        cursor.executescript(SCHEMA_SQL)
        conn.commit()

    cursor = src.cursor()
    for i in range(COUNT):
        cursor.execute(INSERT_SQL, ("name%d" % i, i))
    src.commit()

    return src, dest


def copy_table(src, dest):
    "Copy data from src to dest (both on people table)"
    src_cursor = src.cursor()
    src_cursor.execute(GET_SQL)
    dest_cursor = dest.cursor()
    # src_cursor is a generator of rows, so we can use it as parameter to
    # executemany
    dest_cursor.executemany(INSERT_SQL, src_cursor)
    dest.commit()

def main():
    src, dest = setup_dbs()
    copy_table(src, dest)

    cursor = dest.cursor()
    cursor.execute("SELECT COUNT(*) FROM people")
    value = cursor.fetchone()[0]
    if value == COUNT:
        print("All data copied")
    else:
        print("BUMMER")

if __name__ == "__main__":
    main()
