import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

FILE = "expenses.csv"
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])
    df.to_csv(FILE, index=False)

def add_expense(date, category, description, amount):
    df = pd.read_csv(FILE)
    new_expense = {"Date": date, "Category": category, "Description": description, "Amount": amount}
    df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
    df.to_csv(FILE, index=False)

def view_expenses():
    df = pd.read_csv(FILE)
    if df.empty:
        messagebox.showinfo("Expenses", "No rows saved yet.")
        return
    top = tk.Toplevel(root)
    top.title("Saved Expenses")
    top.geometry("640x360")
    cols = ["Date","Category","Description","Amount"]
    tree = ttk.Treeview(top, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
    tree.column("Date", width=110, anchor="center")
    tree.column("Category", width=140, anchor="w")
    tree.column("Description", width=300, anchor="w")
    tree.column("Amount", width=90, anchor="e")
    vsb = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
    tree.configure(yscroll=vsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)
    for _, r in df.iterrows():
        tree.insert("", tk.END, values=(r["Date"], r["Category"], r["Description"], r["Amount"]))

def normalize_date(s):
    s = s.strip().replace("/", "-")
    fmts = ["%m-%d-%Y", "%Y-%m-%d", "%m-%d-%y", "%d-%m-%Y"]
    for f in fmts:
        try:
            d = datetime.strptime(s, f)
            return d.strftime("%m-%d-%Y")
        except ValueError:
            pass
    raise ValueError("Use a valid date like 03-21-2025")

def on_add():
    try:
        d = normalize_date(date_var.get())
        amt = float(amount_var.get().strip())
    except ValueError as e:
        messagebox.showerror("Invalid input", str(e))
        return
    add_expense(d, category_var.get().strip(), description_var.get().strip(), amt)
    date_var.set(""); category_var.set(""); description_var.set(""); amount_var.set("")
    messagebox.showinfo("Saved", "Expense added.")

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("520x220")
try:
    ttk.Style().theme_use("clam")
except:
    pass
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)

date_var = tk.StringVar()
category_var = tk.StringVar()
description_var = tk.StringVar()
amount_var = tk.StringVar()

pad = dict(sticky="ew", padx=8, pady=6)

tk.Label(root, text="Date (MM-DD-YYYY)").grid(row=0, column=0, sticky="w", padx=8, pady=6)
tk.Entry(root, textvariable=date_var, width=24).grid(row=0, column=1, **pad)

tk.Label(root, text="Category").grid(row=1, column=0, sticky="w", padx=8, pady=6)
tk.Entry(root, textvariable=category_var, width=24).grid(row=1, column=1, **pad)

tk.Label(root, text="Description").grid(row=2, column=0, sticky="w", padx=8, pady=6)
tk.Entry(root, textvariable=description_var, width=24).grid(row=2, column=1, **pad)

tk.Label(root, text="Amount").grid(row=3, column=0, sticky="w", padx=8, pady=6)
tk.Entry(root, textvariable=amount_var, width=24).grid(row=3, column=1, **pad)

ttk.Button(root, text="Add", command=on_add).grid(row=4, column=0, padx=8, pady=8, sticky="w")
ttk.Button(root, text="View", command=view_expenses).grid(row=4, column=1, padx=8, pady=8, sticky="e")

root.mainloop()
