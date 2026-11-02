import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import functions


conn = sqlite3.connect("library.db")
functions.create_tables(conn)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM books")
if cursor.fetchone()[0] == 0:
    functions.insert_data(conn)

root = tk.Tk()
root.title("Bibliotēkas datubāze")
root.geometry("900x600")

current_table = tk.StringVar(value="books")
search_var = tk.StringVar()
tree = None


def columns_for(table):
    if table == "books":
        return ["id", "title", "year"]
    if table == "authors":
        return ["id", "name", "birth_year"]
    return ["id", "name", "age"]


def fill(rows):
    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert("", tk.END, values=row)


def refresh():
    table = current_table.get()
    cols = columns_for(table)
    tree["columns"] = cols
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=200)
    fill(functions.get_all(conn, table))


def search():
    table = current_table.get()
    text = search_var.get().strip()
    if not text:
        refresh()
        return
    fill(functions.find_by_name(conn, table, text))


def selected():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Uzmanību", "Izvēlies ierakstu!")
        return None
    return tree.item(sel[0])["values"]


def open_dialog(title, name, value, callback):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("300x150")
    name_var = tk.StringVar(value=name)
    value_var = tk.StringVar(value=value)

    tk.Label(win, text="Nosaukums:").pack(pady=(10, 0))
    tk.Entry(win, textvariable=name_var).pack()
    tk.Label(win, text="Vērtība:").pack(pady=(10, 0))
    tk.Entry(win, textvariable=value_var).pack()

    def save():
        n = name_var.get().strip()
        try:
            v = int(value_var.get())
        except ValueError:
            messagebox.showerror("Kļūda", "Vērtībai jābūt skaitlim!")
            return
        if not n:
            messagebox.showerror("Kļūda", "Nosaukums nedrīkst būt tukšs!")
            return
        callback(n, v)
        win.destroy()

    tk.Button(win, text="Saglabāt", command=save).pack(pady=10)


def add():
    table = current_table.get()

    def do_add(name, value):
        functions.add_record(conn, table, name, value)
        refresh()

    open_dialog("Pievienot ierakstu", "", "", do_add)


def update_name(table, record_id, name):
    column = "title" if table == "books" else "name"
    cursor = conn.cursor()
    cursor.execute("UPDATE " + table + " SET " + column + " = ? WHERE id = ?",
                   (name, record_id))
    conn.commit()


def edit():
    row = selected()
    if not row:
        return
    table = current_table.get()
    record_id, name, value = row[0], row[1], row[2]

    def do_edit(new_name, new_value):
        update_name(table, record_id, new_name)
        functions.update_value(conn, table, record_id, new_value)
        refresh()

    open_dialog("Rediģēt ierakstu", name, value, do_edit)


def delete():
    row = selected()
    if not row:
        return
    if not messagebox.askyesno("Apstiprināt", "Dzēst ierakstu?"):
        return
    functions.delete_record(conn, current_table.get(), row[0])
    refresh()


top = tk.Frame(root)
top.pack(fill=tk.X, padx=10, pady=10)

tk.Label(top, text="Tabula:").pack(side=tk.LEFT)
combo = ttk.Combobox(top, textvariable=current_table,
                     values=functions.TABLES, state="readonly", width=12)
combo.pack(side=tk.LEFT, padx=5)
combo.bind("<<ComboboxSelected>>", lambda e: refresh())

tk.Label(top, text="Meklēt:").pack(side=tk.LEFT, padx=(20, 0))
entry = tk.Entry(top, textvariable=search_var, width=25)
entry.pack(side=tk.LEFT, padx=5)
entry.bind("<Return>", lambda e: search())
tk.Button(top, text="Meklēt", command=search).pack(side=tk.LEFT)
tk.Button(top, text="Rādīt visus", command=refresh).pack(side=tk.LEFT, padx=5)

tree = ttk.Treeview(root, show="headings", selectmode="browse")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

btns = tk.Frame(root)
btns.pack(fill=tk.X, padx=10, pady=10)
tk.Button(btns, text="Pievienot", command=add).pack(side=tk.LEFT)
tk.Button(btns, text="Rediģēt", command=edit).pack(side=tk.LEFT, padx=5)
tk.Button(btns, text="Dzēst", command=delete).pack(side=tk.LEFT)

refresh()
root.mainloop()