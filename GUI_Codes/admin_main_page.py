import tkinter as tk
from tkinter import messagebox

from GUI_Codes.password_requests_page import show_password_request_page
from logger import Logger
from mysql_connection import connect_to_database

# Kullanıcı eklemek için fonksiyon
def add_user():
    def on_add_user():
        logger = Logger()  # Logger sınıfını oluşturuyoruz

        username = entry_username.get()
        password = entry_password.get()
        email = entry_email.get()

        if not username or not password or not email:
            messagebox.showerror("Hata", "Kullanıcı adı, şifre ve e-posta adresini girin.")
            # Eksik bilgi log mesajı
            logger.log_user_operation(operation="Kullanıcı ekleme (eksik bilgi)", user_id=None, success=False)
            return

        try:
            connection = connect_to_database()
            cursor = connection.cursor()

            # Kullanıcıyı veritabanına ekle
            query = "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, email))
            connection.commit()

            # Başarılı işlem
            messagebox.showinfo("Başarılı", "Kullanıcı başarıyla eklendi.")
            logger.log_user_operation(operation="Kullanıcı ekleme", user_id=username, success=True)
            add_user_window.destroy()  # Pencereyi kapat
        except Exception as e:
            # Hata log mesajı
            error_message = f"Kullanıcı eklenirken hata oluştu: {e}"
            messagebox.showerror("Hata", error_message)
            logger.log_user_operation(operation="Kullanıcı ekleme", user_id=username, success=False)
        finally:
            if connection:
                connection.close()

    # Kullanıcı ekleme penceresi
    add_user_window = tk.Toplevel()
    add_user_window.title("Kullanıcı Ekle")
    add_user_window.geometry("300x250")

    # Kullanıcı adı
    label_username = tk.Label(add_user_window, text="Kullanıcı Adı:")
    label_username.pack(pady=5)
    entry_username = tk.Entry(add_user_window)
    entry_username.pack(pady=5)

    # Şifre
    label_password = tk.Label(add_user_window, text="Şifre:")
    label_password.pack(pady=5)
    entry_password = tk.Entry(add_user_window, show="*")
    entry_password.pack(pady=5)

    # E-posta
    label_email = tk.Label(add_user_window, text="E-posta:")
    label_email.pack(pady=5)
    entry_email = tk.Entry(add_user_window)
    entry_email.pack(pady=5)

    # Ekle butonu
    add_button = tk.Button(add_user_window, text="Ekle", command=on_add_user)
    add_button.pack(pady=20)


# Kullanıcı silmek için fonksiyon
def delete_user():
    def on_delete_user():
        user_id = entry_user_id.get()

        if not user_id:
            messagebox.showerror("Hata", "Kullanıcı ID'sini girin.")
            return

        try:
            connection = connect_to_database()
            cursor = connection.cursor()

            # Kullanıcıyı veritabanından sil
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Başarılı", "Kullanıcı başarıyla silindi.")
                delete_user_window.destroy()
            else:
                messagebox.showerror("Hata", "Kullanıcı bulunamadı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Kullanıcı silinirken hata oluştu: {e}")
        finally:
            if connection:
                connection.close()

    delete_user_window = tk.Toplevel()
    delete_user_window.title("Kullanıcı Sil")
    delete_user_window.geometry("300x200")

    label_user_id = tk.Label(delete_user_window, text="Kullanıcı ID:")
    label_user_id.pack(pady=5)
    entry_user_id = tk.Entry(delete_user_window)
    entry_user_id.pack(pady=5)

    delete_button = tk.Button(delete_user_window, text="Sil", command=on_delete_user)
    delete_button.pack(pady=20)


# Kullanıcılara limit verme fonksiyonu
def set_user_limit():
    def on_set_limit():
        user_id = entry_user_id.get()
        limit = combo_limit.get()

        if not user_id or not limit:
            messagebox.showerror("Hata", "Kullanıcı ID'si ve limit seçimi yapın.")
            return

        try:
            connection = connect_to_database()
            cursor = connection.cursor()

            # Kullanıcı limitini güncelle
            query = "UPDATE users SET `limit` = %s WHERE id = %s"
            cursor.execute(query, (limit, user_id))
            connection.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Başarılı", "Kullanıcının limiti başarıyla güncellendi.")
            else:
                messagebox.showerror("Hata", "Belirtilen ID'ye sahip kullanıcı bulunamadı.")

            set_limit_window.destroy()  # Pencereyi kapat
        except Exception as e:
            messagebox.showerror("Hata", f"Limit ayarlanırken hata oluştu: {e}")
        finally:
            if connection:
                connection.close()

    # Limit belirleme penceresi
    set_limit_window = tk.Toplevel()
    set_limit_window.title("Kullanıcıya Limit Ver")
    set_limit_window.geometry("300x200")

    # Kullanıcı ID girişi
    label_user_id = tk.Label(set_limit_window, text="Kullanıcı ID:")
    label_user_id.pack(pady=5)
    entry_user_id = tk.Entry(set_limit_window)
    entry_user_id.pack(pady=5)

    # Limit seçimi
    label_limit = tk.Label(set_limit_window, text="Limit Seçin:")
    label_limit.pack(pady=5)
    combo_limit = tk.StringVar()
    limit_dropdown = tk.OptionMenu(set_limit_window, combo_limit, "50GB", "100GB")
    limit_dropdown.pack(pady=5)

    # Kaydet butonu
    set_button = tk.Button(set_limit_window, text="Kaydet", command=on_set_limit)
    set_button.pack(pady=20)


# Ana pencereyi oluştur
def show_admin_main_page():
    root = tk.Tk()
    root.title("Admin Paneli")
    root.geometry("400x300")

    label_title = tk.Label(root, text="Sistem Yöneticisi Paneli", font=("Arial", 20))
    label_title.pack(pady=10)

    button_add_user = tk.Button(root, text="Kullanıcı Ekle", command=add_user)
    button_add_user.pack(pady=10)

    button_delete_user = tk.Button(root, text="Kullanıcı Sil", command=delete_user)
    button_delete_user.pack(pady=10)

    button_set_limit = tk.Button(root, text="Kullanıcılara Limit Ver", command=set_user_limit)
    button_set_limit.pack(pady=10)

    # Şifre değişim talepleri butonu
    password_requests_button = tk.Button(
        root,
        text="Şifre Değişim Talepleri",
        font=("Arial", 12),
        bg="#4CAF50",
        fg="white",
        relief="flat",
        width=20,
        height=2,
        command=show_password_request_page  # Yeni sayfayı çağıracak
    )
    password_requests_button.pack(pady=20)

    root.mainloop()

