
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw

conn = sqlite3.connect("bmi_data.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            status TEXT,
            date TEXT)''')
conn.commit()

def calculate_bmi():
name = name_var.get()
weight = weight_var.get()
height = height_var.get()
if not name or not weight or not height:
    messagebox.showwarning("Input Error", "Please fill in all fields")
    return
try:
    weight = float(weight)
    height = float(height) / 100
    bmi = round(weight / (height ** 2), 2)

    if bmi < 18.5:
        status = "Underweight"
    elif 18.5 <= bmi < 25:
        status = "Normal weight"
    elif 25 <= bmi < 30:
        status = "Overweight"
    else:
        status = "Obese"

    result_text.set(f"{name}, your BMI is {bmi} ({status})")

    c.execute("INSERT INTO bmi_history (name, weight, height, bmi, status, date) VALUES (?, ?, ?, ?, ?, ?)",
              (name, weight, height * 100, bmi, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
except ValueError:
    messagebox.showerror("Invalid Input", "Please enter numeric values for weight and height")

def show_history():
history_window = tk.Toplevel(root)
history_window.title("BMI History")
history_window.geometry("700x400")

tree = ttk.Treeview(history_window, columns=("Name", "Weight", "Height", "BMI", "Status", "Date"), show="headings")
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(expand=True, fill=tk.BOTH)

c.execute("SELECT name, weight, height, bmi, status, date FROM bmi_history")
for row in c.fetchall():
    tree.insert("", tk.END, values=row)

def clear_fields():
name_var.set("")
weight_var.set("")
height_var.set("")
result_text.set("")

def clear_history():
confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to clear all history?")
if confirm:
    c.execute("DELETE FROM bmi_history")
    conn.commit()
    messagebox.showinfo("History Cleared", "All BMI history has been deleted.")

def generate_gradient(width, height, color1, color2):
base = Image.new("RGB", (width, height), color1)
top = Image.new("RGB", (width, height), color2)
mask = Image.new("L", (width, height))
mask_data = []
for y in range(height):
    mask_data.extend([int(255 * (y / height))] * width)
mask.putdata(mask_data)
base.paste(top, (0, 0), mask)
return ImageTk.PhotoImage(base)

root = tk.Tk()
root.title("BMI Calculator")
root.attributes("-fullscreen", True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

gradient = generate_gradient(screen_width, screen_height, "#ffb6c1", "#add8e6")
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas_bg = canvas.create_image(0, 0, anchor="nw", image=gradient)

frame = ttk.Frame(root, padding=30)
canvas.create_window(screen_width // 2, screen_height // 2, window=frame)

style = ttk.Style()
style.configure("TLabel", font=("Times New Roman", 14, "bold"))
style.configure("TButton", font=("Segoe UI", 12, "bold"))

name_var = tk.StringVar()
weight_var = tk.StringVar()
height_var = tk.StringVar()
result_text = tk.StringVar()

ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky="e", pady=10)
ttk.Entry(frame, textvariable=name_var, width=35).grid(row=0, column=1, pady=10)

ttk.Label(frame, text="Weight (kg):").grid(row=1, column=0, sticky="e", pady=10)
ttk.Entry(frame, textvariable=weight_var, width=35).grid(row=1, column=1, pady=10)

ttk.Label(frame, text="Height (cm):").grid(row=2, column=0, sticky="e", pady=10)
ttk.Entry(frame, textvariable=height_var, width=35).grid(row=2, column=1, pady=10, )

ttk.Button(frame, text="Calculate BMI", command=calculate_bmi).grid(row=3, column=0, columnspan=2, pady=15)
ttk.Button(frame, text="Show History", command=show_history).grid(row=4, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Clear History", command=clear_history).grid(row=5, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Clear Fields", command=clear_fields).grid(row=6, column=0, columnspan=2, pady=5)

ttk.Label(frame, textvariable=result_text, foreground="black", font=("Segoe UI", 14, "italic")).grid(row=7, column=0, columnspan=2, pady=20)

root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
conn.close()
