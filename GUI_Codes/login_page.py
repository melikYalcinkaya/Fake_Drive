# login_page.py
import tkinter as tk
from tkinter import messagebox

from GUI_Codes.admin_login_page import show_admin_login_page
from user_operation import check_user_credentials, track_failed_login, \
    failed_login_attempts  # track_failed_login fonksiyonunu içe aktar
from GUI_Codes.main_page import show_main_page  # Ana sayfa fonksiyonunu içe aktar


# Giriş yapma sayfası
def show_login_page():
    # Ana pencereyi oluştur
    root = tk.Tk()
    root.title("Giriş Yap")
    root.geometry("400x300")

    # Başlık
    label_title = tk.Label(root, text="Giriş Yap", font=("Arial", 20))
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

    # Giriş yap butonu
    def on_login():
        username = entry_username.get()
        password = entry_password.get()

        if not username or not password:
            messagebox.showerror("Hata", "Lütfen kullanıcı adı ve şifre alanlarını doldurun.")
            return

        # Kullanıcı doğrulama işlemi ve kullanıcı ID'sini al
        user_id = check_user_credentials(username, password)

        if user_id:
            messagebox.showinfo("Başarılı", "Giriş başarılı!")
            root.destroy()  # Giriş başarılı olduğunda pencereyi kapat
            show_main_page(user_id)  # Ana sayfaya doğru user_id ile yönlendir
        else:
            # Başarısız giriş denemesi, track_failed_login fonksiyonunu çağır
            track_failed_login(user_id)

            # 3. yanlış deneme olduğu durumda ekrana mesaj göster
            failed_attempts = failed_login_attempts.get(user_id, [])
            if len(failed_attempts) >= 3:  # 3. başarısız giriş
                messagebox.showerror("Hata", "Şifrenizi yanlış girdiniz. Üçüncü başarısız giriş denemesi!")

            messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı.")

    login_button = tk.Button(root, text="Giriş Yap", command=on_login)
    login_button.pack(pady=20)

    # Admin girişi butonu
    def on_admin_login():
        root.destroy()
        show_admin_login_page()  # Admin giriş sayfasına yönlendir

    admin_button = tk.Button(root, text="Admin Girişi", command=on_admin_login)
    admin_button.pack(pady=10)

    # Ana pencereyi çalıştır
    root.mainloop()
