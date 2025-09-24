import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Database config
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "1234+-abc"   # use your MySQL root password
DB_NAME = "todo_db"


# Get DB connection
def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To Do List Manager")
        self.root.geometry("700x500")
        self.root.configure(bg="#2c3e50")

        # Title
        tk.Label(root, text="Task Dashboard", font=("Arial", 18, "bold"),
                 bg="#2c3e50", fg="white").pack(pady=10)

        # Task entry
        self.task_entry = tk.Entry(root, width=45, font=("Arial", 12))
        self.task_entry.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root, bg="#2c3e50")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Task", command=self.add_task,
                  bg="#27ae60", fg="white", width=12).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Edit Task", command=self.edit_task,
                  bg="#f39c12", fg="white", width=12).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Mark Done", command=self.mark_done,
                  bg="#2980b9", fg="white", width=12).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Delete Task", command=self.delete_task,
                  bg="#c0392b", fg="white", width=12).grid(row=0, column=3, padx=5)

        # Task list
        self.tree = ttk.Treeview(root, columns=("ID", "Task", "Status", "Created"),
                                 show="headings", height=12)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Created", text="Created At")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Task", width=50)
        self.tree.column("Status", width=100, anchor="center")
        self.tree.column("Created", width=200, anchor="center")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Load tasks from DB
        self.load_tasks()

    # Load tasks
    def load_tasks(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, task, status, created_at FROM tasks")
        rows = cursor.fetchall()
        db.close()

        self.tree.delete(*self.tree.get_children())

        for tid, task, status, created in rows:
            # Use the numeric id as iid
            self.tree.insert("", "end", iid=str(tid), values=(tid, task, status, created))

    # Add task
    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Task cannot be empty")
            return
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
        db.commit()
        db.close()
        self.task_entry.delete(0, tk.END)
        self.load_tasks()
        messagebox.showinfo("Success", "Task added successfully to the database!")

    # Edit task
    def edit_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a task to edit")
            return
        task_id = int(sel[0])  # FIX: cast to integer
        new_task = self.task_entry.get().strip()
        if not new_task:
            messagebox.showwarning("Warning", "Enter new task text")
            return
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE tasks SET task=%s WHERE id=%s", (new_task, task_id))
        db.commit()
        db.close()
        self.task_entry.delete(0, tk.END)
        self.load_tasks()
        messagebox.showinfo("Success", "Task updated successfully!")

    # Mark task as done
    def mark_done(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a task to mark done")
            return
        task_id = int(sel[0])  # FIX: cast to integer
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE tasks SET status='Done' WHERE id=%s", (task_id,))
        db.commit()
        db.close()
        self.load_tasks()
        messagebox.showinfo("Success", "Task marked as Done!")

    # Delete task
    def delete_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a task to delete")
            return
        task_id = int(sel[0])  # FIX: cast to integer
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        db.commit()
        db.close()
        self.load_tasks()
        messagebox.showinfo("Success", "Task deleted successfully!")


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    ToDoApp(root)
    root.mainloop()
