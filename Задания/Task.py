#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import sqlite3
from pathlib import Path
import argparse
import typing as t


def create_db(database_path: Path) -> None:
    """
    Создать базу данных
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Создать таблицу с информацией о дате рождения
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS birth (
            date_id INTEGER PRIMARY KEY AUTOINCREMENT,
            birth_date INTEGER NOT NULL
        )
        """
    )

    # Создать таблицу с информацией о пользователях
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            user_number TEXT NOT NULL,
            date_id INTEGER NOT NULL,
            FOREIGN KEY(date_id) REFERENCES birth(date_id)
        )
        """
    )
    conn.close()


def display_workers(staff: t.List[t.Dict[str, t.Any]]) -> None:
    """
    Отобразить список работников.
    """
    # Проверить, что список работников не пуст.
    if staff:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "№",
                "Имя",
                "Номер телефона",
                "Дата рождения"
            )
        )
        print(line)

        # Вывести данные о всех сотрудниках
        for idx, user in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>20} |'.format(
                    idx,
                    user.get('name', ''),
                    user.get('number', ''),
                    user.get('year', 0)
                )
            )
            print(line)
    else:
        print("Список работников пуст.")


def add_worker(
    database_path: Path,
    name: str,
    number: str,
    date: int
) -> None:
    """
    Добавить работника в базу данных
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Получить идентификатор должности в базе данных
    # Если такой записи нет, то добавить информацию о новой должности
    cursor.execute(
        """
        SELECT date_id FROM birth WHERE birth_date = ?
        """,
        (date,)
    )
    row = cursor.fetchone()
    if row is None:
        cursor.execute(
            """
            INSERT INTO birth (birth_date) VALUES (?)
            """,
            (date,)
        )
        date_id = cursor.lastrowid

    else:
        date_id = row[0]

    # Добавить информацию о новом работнике
    cursor.execute(
        """
        INSERT INTO users (user_name, date_id, user_number)
        VALUES (?, ?, ?)
        """,
        (name, date_id, number)
    )
    conn.commit()
    conn.close()


def select_all(database_path: Path) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать всех работников.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT users.user_name, birth.birth_date, users.user_number
        FROM users
        INNER JOIN birth ON birth.date_id = users.date_id
        """
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "name": row[0],
            "number": row[1],
            "year": row[2],
        }
        for row in rows
    ]


def select_by_period(
    database_path: Path, pnumber: int
) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать всех пользователей с заданным номером телефона.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT users.user_name, birth.birth_date, users.user_number
        FROM users
        INNER JOIN birth ON birth.date_id = users.date_id
        WHERE users.user_number == ?
        """,
        (pnumber,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "name": row[0],
            "number": row[1],
            "year": row[2],
        }
        for row in rows
    ]


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "--db",
        action="store",
        required=False,
        default=str(Path.home() / "users.db"),
        help="The database file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("workers")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления пользователей.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new worker"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The worker's name"
    )
    add.add_argument(
        "-p",
        "--phone",
        action="store",
        help="The worker's post"
    )
    add.add_argument(
        "-b",
        "--birth",
        action="store",
        type=int,
        required=True,
        help="Birthdate"
    )

    # Создать субпарсер для отображения всех пользователей.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all workers"
    )

    # Создать субпарсер для выбора пользователей.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the workers"
    )
    select.add_argument(
        "-N",
        "--number",
        action="store",
        type=int,
        required=True,
        help="The required phone number"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Получить путь к файлу базы данных.
    db_path = Path(args.db)
    create_db(db_path)

    # Добавить пользователей.
    if args.command == "add":
        add_worker(db_path, args.name, args.phone, args.birth)

    # Отобразить всех рпользователей.
    elif args.command == "display":
        display_workers(select_all(db_path))

    # Выбрать требуемых пользователей.
    elif args.command == "select":
        display_workers(select_by_period(db_path, args.period))
        pass


if __name__ == "__main__":
    main()
