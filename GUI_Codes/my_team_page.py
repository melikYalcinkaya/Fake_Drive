import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from team_operations import get_team_members
from file_operations import share_file
import tkinter as tk
from tkinter import filedialog, messagebox
from team_operations import get_team_members
from file_operations import share_file


def show_my_team_page(user_id):
    """Takım üyelerini gösteren sayfa ve toplu dosya paylaşımı yapar."""

    def share_file_with_team():
        """Tüm takım üyelerine dosya paylaşımı yap."""
        from logger import Logger  # Logger sınıfını içe aktarıyoruz
        logger = Logger()  # Logger sınıfından bir nesne oluşturuyoruz

        # Takım üyelerini kontrol et
        if not team_members:
            messagebox.showwarning("Uyarı", "Takımda üye bulunamadı.")
            logger.log_team_operation(operation="file_sharing", user_id=user_id, success=False)
            return

        # Dosya seçme
        file_path = filedialog.askopenfilename(title="Dosya Seç", filetypes=[("Tüm Dosyalar", "*.*")])
        if not file_path:
            return  # Dosya seçilmediyse işlemi iptal et

        # Dosyayı tüm üyelerle paylaş
        try:
            for username, member_id in team_members:
                # Her kullanıcı için hedef dizini belirle
                user_folder = f"shared_files/user_{member_id}"  # Örneğin: shared_files/1

                # Hedef klasörü oluştur (eğer yoksa)
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)

                # Dosya yolunu oluştur
                file_name = os.path.basename(file_path)
                target_path = os.path.join(user_folder, file_name)

                # Dosyayı kullanıcının klasörüne kopyala
                shutil.copy(file_path, target_path)

                # Veritabanına paylaşım kaydını ekle
                share_file(sender_id=user_id, receiver_id=member_id, local_path=target_path)

                # Başarılı paylaşım için log yaz
                logger.log_document_sharing(file_name=file_name, user_id=member_id, success=True)

            messagebox.showinfo("Başarılı", "Dosya tüm takım üyeleriyle başarıyla paylaşıldı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya paylaşımında bir hata oluştu: {e}")

            # Hata durumunda log yaz
            logger.log_document_sharing(file_name=os.path.basename(file_path), user_id=user_id, success=False)

    team_window = tk.Toplevel()
    team_window.title("Takımım")
    team_window.geometry("400x500")
    team_window.resizable(False, False)

    # Başlık
    title_label = tk.Label(team_window, text="Takım Üyelerim", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Üye listesi başlığı
    member_list_label = tk.Label(team_window, text="Üyeler:", font=("Arial", 12, "bold"))
    member_list_label.pack(pady=5)

    # Üye listesi
    member_listbox = tk.Listbox(team_window, width=50, height=15)
    member_listbox.pack(pady=10)

    # Veritabanından üyeleri çek
    team_members = get_team_members(user_id)
    if team_members:
        for username, member_id in team_members:
            member_listbox.insert(tk.END, f"{username} (ID: {member_id})")
    else:
        member_listbox.insert(tk.END, "Takımda henüz üye yok.")

    # Tüm Takıma Dosya Paylaş Butonu
    share_button = tk.Button(team_window, text="Dosya Paylaş", command=share_file_with_team,
                             width=25, height=2, font=("Arial", 12), bg="#4CAF50", fg="white")
    share_button.pack(pady=10)

    # Kapatma Butonu
    close_button = tk.Button(team_window, text="Kapat", command=team_window.destroy, width=15, height=2,
                             font=("Arial", 12), bg="#f44336", fg="white")
    close_button.pack(pady=10)