# admin_login_page.py
import tkinter as tk
from tkinter import messagebox

from GUI_Codes.admin_main_page import show_admin_main_page


# Admin girişi sayfası
def show_admin_login_page():
    root = tk.Tk()
    root.title("Admin Girişi")
    root.geometry("400x300")

    # Başlık
    label_title = tk.Label(root, text="Admin Girişi", font=("Arial", 20))
    label_title.pack(pady=10)

    # Kullanıcı Adı Giriş
    label_username = tk.Label(root, text="Kullanıcı Adı:")
    label_username.pack(pady=5)
    entry_username = tk.Entry(root, width=30)
    entry_username.pack(pady=5)

    # Şifre Giriş
    label_password = tk.Label(root, text="Şifre:")
    label_password.pack(pady=5)
    entry_password = tk.Entry(root, width=30, show="*")
    entry_password.pack(pady=5)

    # Admin girişi doğrulama işlemi
    def on_admin_login():
        username = entry_username.get()
        password = entry_password.get()

        if username == "Melik Yalcinkaya" and password == "Melik2121.":  # Admin kullanıcı adı ve şifresi
            messagebox.showinfo("Başarılı", "Admin girişi başarılı!")
            root.destroy()  # Giriş başarılı olduğunda pencereyi kapat
            show_admin_main_page()  # Admin ana sayfasına yönlendir
        else:
            messagebox.showerror("Hata", "Admin kullanıcı adı veya şifresi hatalı.")

    # Giriş yap butonu
    login_button = tk.Button(root, text="Giriş Yap", command=on_admin_login)
    login_button.pack(pady=20)

    root.mainloop()
