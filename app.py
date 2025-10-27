import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

tree = None
title_entr = None
year_entr = None
rating_entr = None
selected_id = None

def setup_db():
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title NVARCHAR,
            year INTEGER,
            rating FLOAT
        )
    ''')
    conn.commit()
    conn.close()

def add_movie(title, year, rating):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO movies (title, year, rating) VALUES (?, ?, ?)", (title, year, rating))
    conn.commit()
    conn.close()

def update_movie(movie_id, title, year, rating):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE movies SET title=?, year=?, rating=? WHERE id=?", (title, year, rating, movie_id))
    conn.commit()
    conn.close()

def delete_movie(movie_id):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id=?", (movie_id,))
    conn.commit()
    conn.close()

def get_all_movies():
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    conn.close()
    return movies

def load_movies():
    for item in tree.get_children():
        tree.delete(item)
    movies = get_all_movies()
    for movie in movies:
        tree.insert('', tk.END, values=movie)

def on_add_movie():
    global selected_id
    title = title_entr.get()
    year = year_entr.get()
    rating = rating_entr.get()

    if title and year and rating:
        try:
            add_movie(title, int(year), float(rating))
            load_movies()
            clear_entries()
        except ValueError:
            messagebox.showerror("Ошибка", "Год и рейтинг должны быть числами")
    else:
        messagebox.showwarning("Предупреждение", "Заполните все поля")

def on_update_movie():
    global selected_id
    if selected_id:
        title = title_entr.get()
        year = year_entr.get()
        rating = rating_entr.get()

        if title and year and rating:
            try:
                update_movie(selected_id, title, int(year), float(rating))
                load_movies()
                clear_entries()
            except ValueError:
                messagebox.showerror("Ошибка", "Год и рейтинг должны быть числами")
        else:
            messagebox.showwarning("Предупреждение", "Заполните все поля")
    else:
        messagebox.showwarning("Предупреждение", "Выберите фильм для обновления")

def on_delete_movie():
    global selected_id
    if selected_id:
        result = messagebox.askyesno("Подтверждение", "Точно хотите удалить выбранный фильм?")
        if result:
            delete_movie(selected_id)
            load_movies()
            clear_entries()
        else:
            messagebox.showwarning("Предупреждение", "Удаление отменено")
    else:
        messagebox.showwarning("Предупреждение", "Выберите фильм для удаления")

def clear_entries():
    global selected_id
    selected_id = None
    title_entr.delete(0, tk.END)
    year_entr.delete(0, tk.END)
    rating_entr.delete(0, tk.END)

def on_select(event):
    global selected_id
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        values = item['values']
        if values:
            selected_id = values[0]
            title_entr.delete(0, tk.END)
            title_entr.insert(0, values[1])
            year_entr.delete(0, tk.END)
            year_entr.insert(0, values[2])
            rating_entr.delete(0, tk.END)
            rating_entr.insert(0, values[3])


if __name__ == "__main__":
    setup_db()
