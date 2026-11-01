# main.py — creates the for_game.db database, the tables and fills them with data.
# A demonstration of the functions from functions.py.

import sqlite3
import functions

DB_NAME = "for_game.db"


def run():
    """Recreates the database, tables and data, then shows a demo."""
    # If the database already exists — start over so the data is not duplicated
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS books")
    cursor.execute("DROP TABLE IF EXISTS authors")
    cursor.execute("DROP TABLE IF EXISTS readers")
    conn.commit()

    # Create the tables
    functions.create_tables(conn)

    # Fill the tables with data
    functions.insert_data(conn)

    print("База данных", DB_NAME, "создана и заполнена!")

    # --- Demo of the functions ---

    print("\nВсе книги:")
    for row in functions.get_all(conn, "books"):
        print(row)

    print("\nКнига с id = 3:")
    print(functions.find_by_id(conn, "books", 3))

    print("\nПоиск книги по названию 'мир':")
    for row in functions.find_by_name(conn, "books", "мир"):
        print(row)

    print("\nДобавляем книгу 'Мёртвые души' (1842):")
    functions.add_record(conn, "books", "Мёртвые души", 1842)

    print("\nМеняем год издания (year) у книги с id = 1 на 1994:")
    functions.update_value(conn, "books", 1, 1994)

    print("\nМеняем возраст (age) у читателя с id = 2 на 20:")
    functions.update_value(conn, "readers", 2, 20)

    print("\nУдаляем книгу с id = 5:")
    functions.delete_record(conn, "books", 5)

    print("\nКниги после изменений:")
    for row in functions.get_all(conn, "books"):
        print(row)

    print("\nЧитатели после изменений:")
    for row in functions.get_all(conn, "readers"):
        print(row)

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    run()
