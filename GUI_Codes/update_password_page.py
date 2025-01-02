# update_password_page.py
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from user_operation import request_password_change, get_user_id_by_username
from logger import Logger

# Logger instance
logger = Logger()

# Şifre değiştirme taleplerini takip etmek için bir sözlük
password_change_requests = {}


# Şifre değiştirme talebini takip etme fonksiyonu
def track_password_change_requests(user_id):
    """Kullanıcının şifre değiştirme taleplerini takip eder."""
    current_time = datetime.now()

    if user_id not in password_change_requests:
        password_change_requests[user_id] = []

    # Taleplerin eski tarihli olanlarını temizleyelim (5 dakika önceki taleplerden önceki talepler)
    password_change_requests[user_id] = [timestamp for timestamp in password_change_requests[user_id] if
                                         current_time - timestamp < timedelta(minutes=5)]

    # Yeni talebi ekleyelim
    password_change_requests[user_id].append(current_time)

    # Eğer son 5 dakika içinde 3 veya daha fazla talep yapılmışsa, anormal davranış loguna kaydedelim
    if len(password_change_requests[user_id]) >= 3:
        logger.log_anormal_davranis(user_id, "Çok sık şifre değiştirme talebi")
        messagebox.showwarning("Uyarı", "Çok sık şifre değiştirme talebinde bulundunuz. Lütfen dikkatli olun.")


def submit_password_change_request(entry_username):
    """Parola değiştirme talebini gönderir."""
    username = entry_username.get()  # Kullanıcı adını al
    user_id = get_user_id_by_username(username)  # Kullanıcı ID'sini al

    if user_id:
        # Parola değiştirme talebi gönder
        track_password_change_requests(user_id)  # Şifre değiştirme talebini takip et
        request_password_change(user_id)
        messagebox.showinfo("Başarılı", "Parola değiştirme isteği başarıyla gönderildi.")
    else:
        messagebox.showerror("Hata", "Kullanıcı adı bulunamadı. Lütfen geçerli bir kullanıcı adı girin.")


def show_update_password_page():
    """Parola değiştirme talebini alacak sayfayı gösterir."""
    update_window = tk.Tk()
    update_window.title("Parola Değiştirme Talebi")
    update_window.geometry("400x250")
    update_window.resizable(False, False)

    # Başlık
    label_title = tk.Label(update_window, text="Parola Değiştirme Talebi", font=("Arial", 16, "bold"), fg="darkblue")
    label_title.pack(pady=20)

    # Kullanıcı adı girişi
    label_username = tk.Label(update_window, text="Kullanıcı Adı:", font=("Arial", 12))
    label_username.pack(pady=5)
    entry_username = tk.Entry(update_window, font=("Arial", 12))
    entry_username.pack(pady=5)

    # Talep gönderme butonu
    submit_button = tk.Button(update_window, text="Talep Gönder", font=("Arial", 12),
                              bg="#4CAF50", fg="white", relief="flat", width=15, height=2,
                              command=lambda: submit_password_change_request(entry_username))
    submit_button.pack(pady=20)

    # Pencereyi çalıştır
    update_window.mainloop()

