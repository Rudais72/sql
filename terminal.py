# terminal.py — a text menu for working with the database in the terminal.

import sqlite3
import functions

DB_NAME = "for_game.db"


def show_all(conn):
    """Menu option 1: show all records from the chosen table."""
    table = input("Какую таблицу показать (books / authors / readers)?: ")
    rows = functions.get_all(conn, table)
    if not rows:
        print("Таблица пустая или её нет.")
        return
    for row in rows:
        print(row)


def add(conn):
    """Menu option 2: add a new record."""
    table = input("В какую таблицу добавить (books / authors / readers)?: ")
    if table == "books":
        name = input("Название книги: ")
    else:
        name = input("Имя: ")
    value = int(input("Число (год / год рождения / возраст): "))
    functions.add_record(conn, table, name, value)
    print("Запись добавлена!")


def update(conn):
    """Menu option 3: update the number column of a record."""
    table = input("В какой таблице изменить (books / authors / readers)?: ")
    record_id = int(input("id записи: "))
    row = functions.find_by_id(conn, table, record_id)
    if row is None:
        print("Запись не найдена.")
        return
    if table == "books":
        value_name = "year (год издания)"
    elif table == "authors":
        value_name = "birth_year (год рождения)"
    else:
        value_name = "age (возраст)"
    new_value = int(input("Новое значение " + value_name + ": "))
    functions.update_value(conn, table, record_id, new_value)
    print("Запись изменена!")


def delete(conn):
    """Menu option 4: delete a record."""
    table = input("Из какой таблицы удалить (books / authors / readers)?: ")
    record_id = int(input("id записи: "))
    row = functions.find_by_id(conn, table, record_id)
    if row is None:
        print("Запись не найдена.")
        return
    functions.delete_record(conn, table, record_id)
    print("Запись удалена!")


def main():
    """The menu loop: keep showing the options until 0 is chosen."""
    conn = sqlite3.connect(DB_NAME)
    functions.create_tables(conn)

    while True:
        print("\n===== БИБЛИОТЕКА =====")
        print("1 — показать всё")
        print("2 — добавить")
        print("3 — изменить")
        print("4 — удалить")
        print("0 — выход")
        choice = input("Выбери пункт: ")

        if choice == "1":
            show_all(conn)
        elif choice == "2":
            add(conn)
        elif choice == "3":
            update(conn)
        elif choice == "4":
            delete(conn)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Нет такого пункта, попробуй ещё раз.")

    conn.close()


if __name__ == "__main__":
    main()
