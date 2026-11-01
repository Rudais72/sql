# functions.py — functions for working with the "Library" database.

import sqlite3

# --- SQL queries that create the tables ---

def create_tables(conn):
    """Creates the three tables: books, authors, readers."""
    cursor = conn.cursor()
    # books: value was renamed to year (the publication year)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER
        )
    """)
    # authors: value was renamed to birth_year (the year of birth)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birth_year INTEGER
        )
    """)
    # readers: value was renamed to age (the age)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        )
    """)
    conn.commit()


# --- Data: books ---

BOOKS = [
    ("Мастер и Маргарита", 1967),
    ("Евгений Онегин", 1833),
    ("Война и мир", 1869),
    ("Преступление и наказание", 1866),
    ("Anna Karenina", 1878),
    ("Отцы и дети", 1862),
    ("Капитанская дочка", 1836),
    ("Собачье сердце", 1987),
]

# --- Data: authors ---

AUTHORS = [
    ("Михаил Булгаков", 1891),
    ("Александр Пушкин", 1799),
    ("Лев Толстой", 1828),
    ("Фёдор Достоевский", 1821),
    ("Иван Тургенев", 1818),
    ("Николай Гоголь", 1809),
    ("Антон Чехов", 1860),
    ("Максим Горький", 1868),
]

# --- Data: readers ---

READERS = [
    ("Иван Петров", 17),
    ("Мария Смирнова", 19),
    ("Алексей Соколов", 21),
    ("Ольга Кузнецова", 18),
    ("Дмитрий Волков", 20),
    ("Анна Новикова", 22),
    ("Сергей Морозов", 25),
    ("Екатерина Зайцева", 16),
    ("Павел Белов", 30),
]


def insert_data(conn):
    """Adds the initial data to all three tables."""
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO books (title, year) VALUES (?, ?)", BOOKS)
    cursor.executemany("INSERT INTO authors (name, birth_year) VALUES (?, ?)", AUTHORS)
    cursor.executemany("INSERT INTO readers (name, age) VALUES (?, ?)", READERS)
    conn.commit()


# --- Functions for main.py ---

# Only these table names are allowed here:
# if something else is passed, the function returns an empty answer.
TABLES = ["books", "authors", "readers"]

# Which number column each table has (after renaming value)
VALUE_COLUMNS = {
    "books": "year",          # the publication year of the book
    "authors": "birth_year",  # the year of birth of the author
    "readers": "age",         # the age of the reader
}


def get_all(conn, table):
    """Returns all records from a table."""
    if table not in TABLES:
        print("Нет такой таблицы:", table)
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM " + table)
    return cursor.fetchall()


def find_by_id(conn, table, record_id):
    """Finds one record by its id."""
    if table not in TABLES:
        print("Нет такой таблицы:", table)
        return None
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM " + table + " WHERE id = ?", (record_id,))
    return cursor.fetchone()


def find_by_name(conn, table, name):
    """Finds records by the book title or the author/reader name."""
    if table not in TABLES:
        print("Нет такой таблицы:", table)
        return []
    cursor = conn.cursor()
    # for books we search in the title column, for the rest — in name
    if table == "books":
        column = "title"
    else:
        column = "name"
    cursor.execute("SELECT * FROM " + table + " WHERE " + column + " LIKE ?",
                   ("%" + name + "%",))
    return cursor.fetchall()


def add_record(conn, table, name, value):
    """Adds a new record to a table."""
    if table not in TABLES:
        print("Нет такой таблицы:", table)
        return
    cursor = conn.cursor()
    # pick the right name of the number column: year, birth_year or age
    value_column = VALUE_COLUMNS[table]
    if table == "books":
        cursor.execute("INSERT INTO books (title, " + value_column + ") "
                       "VALUES (?, ?)", (name, value))
    else:
        cursor.execute("INSERT INTO " + table + " (name, " + value_column + ") "
                       "VALUES (?, ?)", (name, value))
    conn.commit()


def update_value(conn, table, record_id, new_value):
    """Updates the number column of a record by its id.

    In books it is year, in authors — birth_year, in readers — age.
    """
    if table not in TABLES:
        print("Нет такой таблицы:", table)
        return
    cursor = conn.cursor()
    value_column = VALUE_COLUMNS[table]
    cursor.execute("UPDATE " + table + " SET " + value_column + " = ? WHERE id = ?",
                   (new_value, record_id))
    conn.commit()


def delete_record(conn, table, record_id):
    """Deletes a record by its id."""
    if table not in TABLES:
        print("Нет такой таблицы:", table)
        return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM " + table + " WHERE id = ?", (record_id,))
    conn.commit()
