#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import sqlite3


def sql_update(con):
    cursor_obj = con.cursor()
    cursor_obj.execute(
        "UPDATE employees SET name = 'Rogers' where id = 2"
    )
    con.commit()


if __name__ == "__main__":
    con = sqlite3.connect('mydatabase.db')
    sql_update(con)
    con.close()
