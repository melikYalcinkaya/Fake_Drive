import tkinter as tk
from tkinter import messagebox
from GUI_Codes.email_update_page import show_update_email_page  # E-posta güncelleme sayfasını içe aktar
from GUI_Codes.notification_page import show_notification_page
from GUI_Codes.update_username_page import show_update_username_page
from GUI_Codes.update_password_page import show_update_password_page
from GUI_Codes.create_team import show_create_team_page  # create_team.py sayfasını içe aktar
from GUI_Codes.my_team_page import show_my_team_page
from GUI_Codes.my_shared_files_page import show_my_shared_files_page

def show_main_page(user_id):
    """Giriş başarılı olduktan sonra ana sayfa."""
    root = tk.Tk()
    root.title("Ana Sayfa")
    root.geometry("600x400")
    root.resizable(False, False)

    # Hoş geldiniz mesajı
    welcome_label = tk.Label(root, text=f"Hoş Geldiniz! Kullanıcı ID: {user_id}", font=("Arial", 20, "bold"), fg="darkblue")
    welcome_label.pack(pady=50)

    # Takım oluştur butonu
    create_team_button = tk.Button(root, text="Takım Oluştur", command=lambda: show_create_team_page(user_id), width=15, height=2,
                                   font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
    create_team_button.place(x=10, y=10)

    # Bildirimler butonu
    notifications_button = tk.Button(root, text="Bildirimler", command= lambda:view_notifications(user_id), width=15, height=2,
                                     font=("Arial", 12), bg="#FF9800", fg="white", relief="flat")
    notifications_button.place(x=10, y=70)

    # Gelen Dosyalar butonu
    shared_files_button = tk.Button(root, text="Gelen Dosyalar", command=lambda: show_my_shared_files_page(user_id),
                                    width=15, height=2,
                                    font=("Arial", 12), bg="#9C27B0", fg="white", relief="flat")
    shared_files_button.place(x=10, y=190)

    # Ana sayfada "Hesabım" butonu
    account_button = tk.Button(root, text="Hesabım", command=show_account_options, width=9, height=2,
                                font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
    account_button.place(x=500, y=10)

    # Takımım butonu
    my_team_button = tk.Button(root, text="Takımım", command=lambda: show_my_team_page(user_id), width=15, height=2,
                               font=("Arial", 12), bg="#03A9F4", fg="white", relief="flat")
    my_team_button.place(x=10, y=130)

    root.mainloop()


def view_notifications(user_id):
    """Bildirimleri gösterir."""
    #messagebox.showinfo("Bildirimler", "Bildirimler sayfası açılacak.")
    show_notification_page(user_id)

#hesabim butonu
def show_account_options():
    """Hesabım seçeneklerini daha şık şekilde gösterir."""
    account_window = tk.Toplevel()
    account_window.title("Hesap İşlemleri")
    account_window.geometry("400x400")
    account_window.resizable(False, False)  # Pencereyi boyutlandırmayı engelle

    # Başlık
    label_title = tk.Label(account_window, text="Hesap İşlemleri", font=("Arial", 18, "bold"), fg="darkblue")
    label_title.pack(pady=10)

    # Butonlar için bir frame oluştur
    button_frame = tk.Frame(account_window)
    button_frame.pack(pady=10)

    # Kullanıcı adı değiştirme butonu
    def change_username():
        #messagebox.showinfo("İşlem", "Kullanıcı adı değiştirme seçildi.")
        show_update_username_page()
        # Buraya update_username fonksiyonunu çağıran kod eklenebilirrr

    username_button = tk.Button(button_frame, text="Kullanıcı Adını Değiştir", command=change_username, width=25,
                                 height=2, font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
    username_button.grid(row=0, column=0, pady=5)

    # Email değiştirme butonu
    email_button = tk.Button(button_frame, text="E-posta Değiştir", command=show_update_email_page, width=25, height=2,
                              font=("Arial", 12), bg="#2196F3", fg="white", relief="flat")
    email_button.grid(row=1, column=0, pady=5)

    # Şifre değiştirme butonu
    def change_password():
        #messagebox.showinfo("İşlem", "Şifre değiştirme seçildi.")
        show_update_password_page()
        # Buraya request_password_change fonksiyonunu çağıran kod eklenecek


    password_button = tk.Button(button_frame, text="Sifre Degistir", command=change_password, width=25, height=2,
                                 font=("Arial", 12), bg="#FF9800", fg="white", relief="flat")
    password_button.grid(row=2, column=0, pady=5)

    # Kapatma butonu
    close_button = tk.Button(account_window, text="Kapat", command=account_window.destroy, width=25, height=2,
                              font=("Arial", 12), bg="#f44336", fg="white", relief="flat")
    close_button.pack(pady=20)

    # Butonlara üzerine gelindiğinde renk değiştirme efekti
    def on_enter(button, color):
        button.config(bg=color)

    def on_leave(button, color):
        button.config(bg=color)

    # Butonların üzerine gelindiğinde renk değişikliği
    for button in [username_button, email_button, password_button]:
        button.bind("<Enter>", lambda e, b=button: on_enter(b, "#45a049" if b == username_button else "#1976D2" if b == email_button else "#FB8C00"))
        button.bind("<Leave>", lambda e, b=button: on_leave(b, "#4CAF50" if b == username_button else "#2196F3" if b == email_button else "#FF9800"))

    # Ana pencereyi çalıştır
    account_window.mainloop()