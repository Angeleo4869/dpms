import sqlite3


def get_sqlite3_connect():
    return sqlite3.connect("db/dpms.db")

