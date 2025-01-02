import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql_connection import connect_to_database

import tkinter as tk
from mysql_connection import connect_to_database

def show_my_shared_files_page(user_id):
    """Paylaşılan dosyaları görüntüleme sayfası."""
    shared_files_window = tk.Toplevel()
    shared_files_window.title("Gelen Paylaşılan Dosyalar")
    shared_files_window.geometry("400x400")
    shared_files_window.resizable(False, False)

    # Başlık
    title_label = tk.Label(shared_files_window, text="Paylaşılan Dosyalarım", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Dosya listesi
    files_listbox = tk.Listbox(shared_files_window, width=50, height=15)
    files_listbox.pack(pady=10)

    # Veritabanından dosyaları çek
    connection = None
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Kullanıcıya gelen dosyaları sorgula
        query = """
            SELECT file_path, shared_date, sender_id 
            FROM shared_files 
            WHERE receiver_id = %s
            ORDER BY shared_date DESC
        """
        cursor.execute(query, (user_id,))
        shared_files = cursor.fetchall()

        if shared_files:
            for file_path, shared_date, sender_id in shared_files:
                files_listbox.insert(tk.END, f"Gönderen: {sender_id}, Tarih: {shared_date}, Dosya: {file_path}")
        else:
            files_listbox.insert(tk.END, "Henüz paylaşılmış dosya yok.")
    except Exception as e:
        files_listbox.insert(tk.END, f"Hata: {str(e)}")
    finally:
        if connection:
            connection.close()

    # Kapatma butonu
    close_button = tk.Button(shared_files_window, text="Kapat", command=shared_files_window.destroy, width=15, height=2,
                              font=("Arial", 12), bg="#f44336", fg="white")
    close_button.pack(pady=10)

    shared_files_window.mainloop()