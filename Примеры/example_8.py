#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import sqlite3

if __name__ == "__main__":
    con = sqlite3.connect('mydatabase.db')
    cursor_obj = con.cursor()
    cursor_obj.execute(
        "CREATE TABLE IF NOT EXISTS projects(id INTEGER, name TEXT)"
    )
    data = [
        (1, "Ridesharing"),
        (2, "Water Purifying"),
        (3, "Forensics"),
        (4, "Botany")
    ]
    cursor_obj.executemany("INSERT INTO projects VALUES (?, ?)", data)
    con.commit()
    con.close()
