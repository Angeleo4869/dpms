import sqlite3


def get_sqlite3_connect():
    connect = sqlite3.connect("db/dpms.db")
    print("success connect")
    for row in connect.cursor().execute("SELECT * FROM patient"):
        print(row[:])
