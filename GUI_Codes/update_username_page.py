import tkinter as tk
from tkinter import messagebox
from mysql_connection import connect_to_database  # Veritabanı bağlantısı için


def update_username(user_id, new_username):
    """Kullanıcı adını günceller."""
    from logger import Logger  # Logger sınıfını içe aktarıyoruz
    logger = Logger()  # Logger sınıfından bir nesne oluşturuyoruz

    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()

            # Kullanıcı adı benzersiz mi kontrol et
            check_query = "SELECT id FROM users WHERE username = %s"
            cursor.execute(check_query, (new_username,))
            if cursor.fetchone():
                messagebox.showerror("Hata", "Bu kullanıcı adı zaten kullanılıyor. Lütfen farklı bir ad seçin.")
                logger.log_user_operation(operation="username_update", user_id=user_id, success=False)
                return

            # Kullanıcı adını güncelle
            update_query = "UPDATE users SET username = %s WHERE id = %s"
            cursor.execute(update_query, (new_username, user_id))
            connection.commit()
            messagebox.showinfo("Başarılı", "Kullanıcı adı başarıyla güncellendi.")
            logger.log_user_operation(operation="username_update", user_id=user_id, success=True)
        except Exception as e:
            messagebox.showerror("Hata", f"Kullanıcı adı güncellenirken bir hata oluştu: {e}")
            logger.log_user_operation(operation="username_update", user_id=user_id, success=False)
        finally:
            connection.close()
    else:
        messagebox.showerror("Hata", "Veritabanı bağlantısı sağlanamadı.")
        logger.log_user_operation(operation="username_update", user_id=user_id, success=False)


def show_update_username_page():
    """Kullanıcı adı güncelleme sayfasını gösterir."""
    update_window = tk.Toplevel()
    update_window.title("Kullanıcı Adı Güncelle")
    update_window.geometry("400x300")
    update_window.resizable(False, False)  # Boyutlandırmayı engelle

    # Başlık
    label_title = tk.Label(update_window, text="Kullanıcı Adı Güncelle", font=("Arial", 16, "bold"), fg="darkblue")
    label_title.pack(pady=20)

    # Kullanıcı ID girişi
    label_user_id = tk.Label(update_window, text="Kullanıcı ID:", font=("Arial", 12))
    label_user_id.pack(pady=5)
    entry_user_id = tk.Entry(update_window, font=("Arial", 12))
    entry_user_id.pack(pady=5)

    # Yeni kullanıcı adı girişi
    label_new_username = tk.Label(update_window, text="Yeni Kullanıcı Adı:", font=("Arial", 12))
    label_new_username.pack(pady=5)
    entry_new_username = tk.Entry(update_window, font=("Arial", 12))
    entry_new_username.pack(pady=5)

    # Güncelle butonu
    def handle_update():
        user_id = entry_user_id.get().strip()
        new_username = entry_new_username.get().strip()

        if not user_id or not new_username:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
            return

        if not user_id.isdigit():
            messagebox.showerror("Hata", "Kullanıcı ID yalnızca sayılardan oluşmalıdır.")
            return

        # Kullanıcı adını güncelle
        update_username(int(user_id), new_username)

    update_button = tk.Button(update_window, text="Güncelle", command=handle_update, font=("Arial", 12),
                               bg="#4CAF50", fg="white", relief="flat", width=15, height=2)
    update_button.pack(pady=20)

    # Pencereyi çalıştır
    update_window.mainloop()
