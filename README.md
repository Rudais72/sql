# Library

A study project. It is a simple "Library" database on Python.
It has three tables:

- **books** (a book title and the year it was published)
- **authors** (a name and the year of birth)
- **readers** (a name and the age)

## Project files

- `app.py` — the main file, we start the project with it
- `main.py` — creates the database `for_game.db` and fills it with data
- `functions.py` — functions: show, find, add, update, delete
- `terminal.py` — the console menu (1 — show all, 2 — add, 3 — update, 4 — delete, 0 — exit)

## How to install and run (Mac / Linux)

You need Python 3 (it is already installed on most computers).

1. Open the terminal and go to the project folder:

```bash
cd path/to/sql_danielsR
```

2. Run the project:

```bash
python3 app.py
```

First the database `for_game.db` will be created with books, authors and readers.
Then the menu will open — just type a number and follow the hints.

## How to download and run on Windows

1. **Install Python.**
   Go to https://www.python.org/downloads/ and download the installer.
   While installing, be sure to check the box **"Add Python to PATH"**.

2. **Download the project from GitHub.**
   Open the project page, press the green **Code** button, then **Download ZIP**.
   Unpack the archive to any folder, for example `C:\Projects\sql_danielsR`.

   (You can also use Git:
   ```
   git clone the-link-to-the-repository
   ```
   )

3. **Open the command line.**
   Press `Win + R`, type `cmd` and press Enter.

4. **Go to the project folder:**

```
cd C:\Projects\sql_danielsR
```

5. **Run the project:**

```
python app.py
```

If it says that `python` is not found — try `py app.py`.
Then just type the number of the menu option and press Enter.

## Good to know

- The database is stored in the file `for_game.db`, it appears in the folder by itself.
- All the data is just a file, you can copy it and move it somewhere.
- If you want to reset the database — delete `for_game.db` and run the project again.
