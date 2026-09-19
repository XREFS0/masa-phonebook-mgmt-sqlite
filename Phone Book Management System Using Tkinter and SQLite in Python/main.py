"""
Developed by MASA
All Rights Reserved.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("phonebook.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT
)
""")
conn.commit()


def add_contact():
    add_btn.state(["!disabled"])
    update_btn.state(["disabled"])
    if name_var.get() == "" or phone_var.get() == "":
        messagebox.showwarning("Required", "Name and Phone are required")
        return
    cursor.execute(
        "INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
        (name_var.get(), phone_var.get(), email_var.get(), address_var.get()),
    )
    conn.commit()
    clear_fields()
    fetch_contacts()


def fetch_contacts():
    for row in contact_table.get_children():
        contact_table.delete(row)
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    for index, row in enumerate(rows):
        tag = "even" if index % 2 == 0 else "odd"
        contact_table.insert("", tk.END, values=row, tags=(tag,))


def clear_fields():
    name_var.set("")
    phone_var.set("")
    email_var.set("")
    address_var.set("")

    add_btn.state(["!disabled"])
    update_btn.state(["disabled"])


def select_contact(event):
    selected = contact_table.focus()
    if not selected:
        return
    values = contact_table.item(selected, "values")
    name_var.set(values[1])
    phone_var.set(values[2])
    email_var.set(values[3])
    address_var.set(values[4])

    add_btn.state(["disabled"])
    update_btn.state(["!disabled"])


def update_contact():
    if "disabled" not in add_btn.state():
        messagebox.showwarning("Edit Mode", "Double-click a row to edit before updating")
        return

    selected = contact_table.focus()
    if not selected:
        messagebox.showwarning("Select", "Select a contact to update")
        return
    contact_id = contact_table.item(selected, "values")[0]
    cursor.execute(
        "UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
        (name_var.get(), phone_var.get(), email_var.get(), address_var.get(), contact_id),
    )
    conn.commit()
    fetch_contacts()
    clear_fields()


def delete_contact():
    selected = contact_table.focus()
    if not selected:
        messagebox.showwarning("Select", "Select a contact to delete")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
    if not confirm:
        return

    contact_id = contact_table.item(selected, "values")[0]
    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    fetch_contacts()
    clear_fields()


root = tk.Tk()
root.title("MASA - Phone Book Management System")
root.geometry("1000x520")
root.configure(bg="#f4f6f8")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="white",
    foreground="#333333",
    rowheight=28,
    fieldbackground="white",
    font=("Segoe UI", 10),
)

style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e9ecef", foreground="#333333")

style.map("Treeview", background=[("selected", "#0d6efd")], foreground=[("selected", "white")])

style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
address_var = tk.StringVar()

header = ttk.Label(root, text="Phone Book Management System", style="Header.TLabel")
header.pack(pady=10)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

form_frame = ttk.LabelFrame(main_frame, text="Contact Details", padding=10)
form_frame.pack(side="left", fill="y", padx=5)

labels = ["Name", "Phone", "Email", "Address"]
vars = [name_var, phone_var, email_var, address_var]

for i, (label, var) in enumerate(zip(labels, vars)):
    ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w", pady=6)
    ttk.Entry(form_frame, textvariable=var, width=30).grid(row=i, column=1, pady=6)

btn_frame = ttk.Frame(form_frame)
btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

buttons = [
    ("Add", add_contact),
    ("Update", update_contact),
    ("Delete", delete_contact),
    ("Clear", clear_fields),
]

add_btn = ttk.Button(btn_frame, text="Add", width=12, command=add_contact)
add_btn.pack(side="left", padx=4)

update_btn = ttk.Button(btn_frame, text="Update", width=12, command=update_contact)
update_btn.state(["disabled"])
update_btn.pack(side="left", padx=4)
ttk.Button(btn_frame, text="Delete", width=12, command=delete_contact).pack(side="left", padx=4)
ttk.Button(btn_frame, text="Clear", width=12, command=clear_fields).pack(side="left", padx=4)

table_frame = ttk.LabelFrame(main_frame, text="Saved Contacts", padding=10)
table_frame.pack(side="right", fill="both", expand=True)

cols = ("ID", "Name", "Phone", "Email", "Address")
contact_table = ttk.Treeview(table_frame, columns=cols, show="headings")

contact_table.heading("ID", text="ID")
contact_table.heading("Name", text="Full Name")
contact_table.heading("Phone", text="Phone Number")
contact_table.heading("Email", text="Email")
contact_table.heading("Address", text="Address")

contact_table.column("ID", width=0, stretch=False)
contact_table.column("Name", width=160, anchor="w")
contact_table.column("Phone", width=120, anchor="center")
contact_table.column("Email", width=180, anchor="w")
contact_table.column("Address", width=220, anchor="w")

contact_table.tag_configure("odd", background="#f8f9fa")
contact_table.tag_configure("even", background="white")

vsb = ttk.Scrollbar(table_frame, orient="vertical", command=contact_table.yview)
hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=contact_table.xview)

contact_table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

contact_table.pack(side="top", fill="both", expand=True)
hsb.pack(side="bottom", fill="x")
vsb.pack(side="right", fill="y")


contact_table.bind("<Double-1>", select_contact)  # Double-click to populate fields & lock Add

fetch_contacts()

root.mainloop()
