import tkinter as tk
from tkinter import messagebox
from user_operation import update_email  # E-posta güncelleme fonksiyonunu içe aktar

def show_update_email_page():
    """E-posta güncelleme sayfasını gösterir."""
    email_window = tk.Toplevel()
    email_window.title("E-posta Güncelle")
    email_window.geometry("400x300")

    # Başlık
    label_title = tk.Label(email_window, text="E-posta Güncelle", font=("Arial", 16))
    label_title.pack(pady=10)

    # Kullanıcı ID'si giriş
    label_user_id = tk.Label(email_window, text="Kullanıcı ID:")
    label_user_id.pack(pady=5)
    entry_user_id = tk.Entry(email_window, width=30)
    entry_user_id.pack(pady=5)

    # Yeni e-posta giriş
    label_new_email = tk.Label(email_window, text="Yeni E-posta:")
    label_new_email.pack(pady=5)
    entry_new_email = tk.Entry(email_window, width=30)
    entry_new_email.pack(pady=5)

    # E-posta güncelleme işlemi
    def on_update_email():
        user_id = entry_user_id.get()
        new_email = entry_new_email.get()

        if not user_id or not new_email:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        try:
            user_id = int(user_id)  # Kullanıcı ID'sini tam sayıya çevir
        except ValueError:
            messagebox.showerror("Hata", "Kullanıcı ID geçerli bir sayı olmalıdır.")
            return

        # E-posta güncelleme fonksiyonunu çağır
        update_email(user_id, new_email)
        messagebox.showinfo("Başarılı", "E-posta başarıyla güncellendi.")
        email_window.destroy()

    # Güncelleme butonu
    update_button = tk.Button(email_window, text="Devam Et", command=on_update_email)
    update_button.pack(pady=20)

    # Kapatma butonu
    close_button = tk.Button(email_window, text="Kapat", command=email_window.destroy)
    close_button.pack(pady=10)


