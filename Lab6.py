import tkinter as tk
from tkinter import messagebox
import sqlite3

# --- Функции для работы с базой данных ---

def create_database():
    """Создает базу данных и таблицу пользователей, если они не существуют."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password, window):
    """Регистрирует нового пользователя в базе данных."""
    if not username or not password:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
        return

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Успех", "Пользователь успешно зарегистрирован")
        window.destroy()  # Закрыть окно регистрации
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Имя пользователя уже существует")
    finally:
        conn.close()

def login_user(username, password):
    """Проверяет данные пользователя при авторизации."""
    if not username or not password:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
        return

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Успех", "Авторизация прошла успешно")
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

# --- Функции для создания графического интерфейса ---

def open_registration_window():
    """Открывает окно регистрации."""
    registration_window = tk.Toplevel(root)
    registration_window.title("Регистрация")

    username_label = tk.Label(registration_window, text="Имя пользователя:")
    username_label.pack()

    username_entry = tk.Entry(registration_window)
    username_entry.pack()

    password_label = tk.Label(registration_window, text="Пароль:")
    password_label.pack()

    password_entry = tk.Entry(registration_window, show="*")
    password_entry.pack()

    register_button = tk.Button(registration_window, text="Зарегистрироваться", command=lambda: register_user(username_entry.get(), password_entry.get(), registration_window))
    register_button.pack()

# --- Создание главного окна ---

create_database()  # Создаем базу данных при запуске

root = tk.Tk()
root.title("Авторизация")

username_label = tk.Label(root, text="Имя пользователя:")
username_label.pack()

username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Пароль:")
password_label.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="Войти", command=lambda: login_user(username_entry.get(), password_entry.get()))
login_button.pack()

register_button = tk.Button(root, text="Регистрация", command=open_registration_window)
register_button.pack()

root.mainloop()