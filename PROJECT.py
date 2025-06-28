from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("data_entry.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_to_db(time, name):
    conn = sqlite3.connect("data_entry.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entries (time, name) VALUES (?, ?)", (time, name))
    conn.commit()
    conn.close()

def update_db(entry_id, time, name):
    conn = sqlite3.connect("data_entry.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE entries SET time = ?, name = ? WHERE id = ?", (time, name, entry_id))
    conn.commit()
    conn.close()

def delete_from_db(entry_id):
    conn = sqlite3.connect("data_entry.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect("data_entry.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- GUI SETUP ---
top = Tk()
top.geometry("600x550")
top.title('Data Entry Table with Database')

# Entry widgets
Label(top, text="Enter Timing:").pack(pady=5)
time_entry = Entry(top, width=30)
time_entry.pack()

Label(top, text="Enter Name:").pack(pady=5)
name_entry = Entry(top, width=30)
name_entry.pack()

# Treeview Table
columns = ("ID", "Time", "Name")
table = ttk.Treeview(top, columns=columns, show="headings", selectmode="browse")
table.heading("ID", text="ID")
table.heading("Time", text="Time")
table.heading("Name", text="Name")
table.column("ID", width=50, anchor='center')
table.pack(pady=20)

# Scrollbar
scrollbar = ttk.Scrollbar(top, orient=VERTICAL, command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)

selected_item_id = None

# Add to table & database
def add_to_table():
    time = time_entry.get().strip()
    name = name_entry.get().strip()
    if time and name:
        insert_to_db(time, name)
        refresh_table()
        time_entry.delete(0, END)
        name_entry.delete(0, END)
    else:
        messagebox.showwarning("Input Error", "Both fields are required.")

# Delete selected row
def delete_selected():
    global selected_item_id
    selected = table.selection()
    if selected:
        item = table.item(selected)
        entry_id = item["values"][0]
        delete_from_db(entry_id)
        refresh_table()
        time_entry.delete(0, END)
        name_entry.delete(0, END)
        selected_item_id = None

# Select row into entry fields
def select_row():
    global selected_item_id
    selected = table.selection()
    if selected:
        item = table.item(selected)
        selected_item_id = item["values"][0]
        time_entry.delete(0, END)
        name_entry.delete(0, END)
        time_entry.insert(0, item["values"][1])
        name_entry.insert(0, item["values"][2])

# Modify selected row
def modify_selected():
    global selected_item_id
    if selected_item_id:
        time = time_entry.get().strip()
        name = name_entry.get().strip()
        if time and name:
            update_db(selected_item_id, time, name)
            refresh_table()
            time_entry.delete(0, END)
            name_entry.delete(0, END)
            selected_item_id = None
        else:
            messagebox.showwarning("Input Error", "Both fields are required.")

# Refresh table from database
def refresh_table():
    for row in table.get_children():
        table.delete(row)
    for row in fetch_all():
        table.insert("", END, values=row)

# Buttons
add_btn = Button(top, text="Add to Table", width=20, height=1, font=("Arial", 12, "bold"),
                 bg="#4CAF50", fg="white", cursor="hand2", command=add_to_table)
add_btn.pack(pady=5)

select_btn = Button(top, text="Select Row", width=20, height=1, font=("Arial", 12, "bold"),
                    bg="#2196F3", fg="white", cursor="hand2", command=select_row)
select_btn.pack(pady=5)

modify_btn = Button(top, text="Modify Selected", width=20, height=1, font=("Arial", 12, "bold"),
                    bg="#FFC107", fg="black", cursor="hand2", command=modify_selected)
modify_btn.pack(pady=5)

delete_btn = Button(top, text="Delete Selected", width=20, height=1, font=("Arial", 12, "bold"),
                    bg="#F44336", fg="white", cursor="hand2", command=delete_selected)
delete_btn.pack(pady=5)

# Initialize DB and load entries
init_db()
refresh_table()

# Optional: auto-select row on click
table.bind("<<TreeviewSelect>>", lambda e: select_row())

top.mainloop()
