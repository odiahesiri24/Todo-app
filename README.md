# 📝 To-Do List Manager (Tkinter + MySQL)

A simple **desktop To-Do List Manager** built with **Python Tkinter** for the GUI and **MySQL** as the database.  
This app allows you to add, edit, mark as done, and delete tasks with persistent storage.

---

## 🚀 Features
- Add new tasks to your list
- Edit existing tasks
- Mark tasks as **Done**
- Delete tasks permanently
- Stores tasks in **MySQL database**
- Simple, clean GUI using Tkinter

---

## 📦 Requirements
Make sure you have the following installed:

- Python 3.x  
- Tkinter (comes pre-installed with Python)  
- `mysql-connector-python`  

Install MySQL connector with:
`bash`
`pip install mysql-connector-python`

## 🗄️ Database Setup

Before running the app, create the database and table in MySQL:

-- Create database
`CREATE DATABASE IF NOT EXISTS todo_db;`

`USE todo_db;`

-- Create tasks table
`CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);`

## ⚡ Running the App

Clone this repository:

`git clone https://github.com/your-username/todo-tkinter-mysql.git
cd todo-tkinter-mysql`


Update database credentials in the script:

`DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_mysql_password"
DB_NAME = "todo_db"`


Run the app:

`python app.py`






