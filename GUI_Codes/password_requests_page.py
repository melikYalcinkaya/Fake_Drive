from tkinter import *
from tkinter import messagebox
from user_operation import fetch_password_requests, update_password_request_status

def handle_accept_request(request_id, container, request_frame):
    """Talebi onaylar."""
    update_password_request_status(request_id, "accepted")
    messagebox.showinfo("Başarılı", "Talep onaylandı.")
    container.destroy()
    refresh_request_list(request_frame)

def handle_reject_request(request_id, container, request_frame):
    """Talebi reddeder."""
    update_password_request_status(request_id, "rejected")
    messagebox.showinfo("Başarılı", "Talep reddedildi.")
    container.destroy()
    refresh_request_list(request_frame)

def refresh_request_list(frame):
    """Listeyi günceller."""
    # Önceki öğeleri temizle
    for widget in frame.winfo_children():
        widget.destroy()

    requests = fetch_password_requests()
    if not requests:
        label = Label(frame, text="Onay bekleyen talep yok.", font=("Arial", 12))
        label.pack(pady=10)
    else:
        for request in requests:
            create_request_row(frame, request)

def create_request_row(frame, request):
    """Her kullanıcı için bir satır oluşturur."""
    container = Frame(frame, pady=5)
    container.pack(fill="x", pady=5)

    lbl_info = Label(
        container,
        text=f"ID: {request[0]}, Kullanıcı: {request[1]}, Email: {request[2]}",
        font=("Arial", 12),
    )
    lbl_info.pack(side=LEFT, padx=10)

    btn_accept = Button(
        container,
        text="Onayla",
        font=("Arial", 10),
        bg="green",
        fg="white",
        command=lambda: handle_accept_request(request[0], container, frame),
    )
    btn_accept.pack(side=RIGHT, padx=5)

    btn_reject = Button(
        container,
        text="Reddet",
        font=("Arial", 10),
        bg="red",
        fg="white",
        command=lambda: handle_reject_request(request[0], container, frame),
    )
    btn_reject.pack(side=RIGHT, padx=5)

def show_password_request_page():
    """Şifre talep sayfasını gösterir."""
    window = Tk()
    window.title("Şifre Değişiklik Talepleri")
    window.geometry("600x400")

    label_title = Label(window, text="Şifre Değişiklik Talepleri", font=("Arial", 16, "bold"))
    label_title.pack(pady=10)

    # Taleplerin gösterileceği çerçeve
    request_frame = Frame(window)
    request_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Talepleri yükle
    refresh_request_list(request_frame)

    window.mainloop()
