import tkinter as tk
from tkinter import messagebox
from user_operation import add_user  # add_user fonksiyonunu içe aktar
from GUI_Codes.login_page import show_login_page

# Kayıt olma sayfası
def show_registration_page():
    # Ana pencereyi oluştur
    root = tk.Tk()
    root.title("Kayıt Olma Sayfası")
    root.geometry("400x400")

    # Başlık
    label_title = tk.Label(root, text="Kayıt Ol", font=("Arial", 20))
    label_title.pack(pady=10)

    # Email Giriş
    label_email = tk.Label(root, text="Email:")
    label_email.pack(pady=5)
    entry_email = tk.Entry(root, width=30)
    entry_email.pack(pady=5)

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

    # Kayıt ol butonu
    def on_register():
        email = entry_email.get()
        username = entry_username.get()
        password = entry_password.get()

        if not email or not username or not password:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        # Veritabanına kayıt fonksiyonunu çağır
        add_user(username, password, email)
        messagebox.showinfo("Başarılı", "Kayıt başarıyla tamamlandı.")
        root.destroy()  # Kayıt olduktan sonra penceriyi kapat
        # Giriş yap sayfasını açabilirsin
        # show_login_page() gibi bir fonksiyon ekleyebilirsin.

    register_button = tk.Button(root, text="Kayıt Ol", command=on_register)
    register_button.pack(pady=20)

    # Giriş yap butonu
    # Giriş yap butonu
    def on_login():
        root.destroy()  # Kayıt sayfasını kapat
        from GUI_Codes.login_page import show_login_page  # Giriş sayfasını içe aktar
        show_login_page()  # Giriş sayfasını göster

    login_button = tk.Button(root, text="Zaten Hesabınız Var mı? Giriş Yap", command=on_login)
    login_button.pack(pady=10)

    # Ana pencereyi çalıştır
    root.mainloop()


# Kayıt sayfasını göster
#show_registration_page()