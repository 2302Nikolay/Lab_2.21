#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import sqlite3
import datetime

if __name__ == "__main__":
    con = sqlite3.connect("mydatabase.db")
    cursor_obj = con.cursor()
    cursor_obj.execute(
        """
        CREATE TABLE IF NOT EXISTS assignments(
            id INTEGER, name TEXT, date DATE
            )
        """
    )
    data = [
        (1, "Ridesharing", datetime.date(2017, 1, 2)),
        (2, "Water Purifying", datetime.date(2018, 3, 4)),
    ]
    cursor_obj.executemany("INSERT INTO assignments VALUES(?, ?, ?)", data)
    con.commit()
    con.close()
