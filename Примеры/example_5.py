#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import sqlite3


def sql_fetch(con):
    cursor_obj = con.cursor()
    # cursor_obj.execute("SELECT * FROM employees")
    cursor_obj.execute("SELECT id, name FROM employees")
    [print(row) for row in cursor_obj.fetchall()]


if __name__ == "__main__":
    con = sqlite3.connect("mydatabase.db")
    sql_fetch(con)
    con.close()
