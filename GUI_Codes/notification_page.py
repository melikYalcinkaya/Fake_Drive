import tkinter as tk
from team_operations import get_notification  # Bildirimleri almak için get_notification fonksiyonu
def show_notification_page(user_id):
    """Bildirimler sayfasını açar."""
    notification_window = tk.Toplevel()
    notification_window.title("Bildirimler")
    notification_window.geometry("400x300")
    notification_window.resizable(False, False)

    # Başlık
    lbl_title = tk.Label(notification_window, text="Bildirimleriniz", font=("Arial", 16), fg="darkblue")
    lbl_title.pack(pady=10)

    # Bildirimleri Gösteren Listbox
    listbox = tk.Listbox(notification_window, width=50, height=15)
    listbox.pack(pady=10)

    # Bildirimleri Yükle
    notifications = get_notification(user_id)
    if notifications:
        for message, added_date in notifications:
            listbox.insert(tk.END, f"{message} ({added_date})")
    else:
        listbox.insert(tk.END, "Henüz bir bildiriminiz yok.")

    # Kapat Butonu
    close_button = tk.Button(notification_window, text="Kapat", command=notification_window.destroy,
                              font=("Arial", 12), bg="#f44336", fg="white", relief="flat")
    close_button.pack(pady=10)

    # Pencereyi çalıştır
    notification_window.mainloop()
