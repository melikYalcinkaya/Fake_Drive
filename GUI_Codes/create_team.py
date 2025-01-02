import tkinter as tk
from tkinter import simpledialog, messagebox
from team_operations import add_team_member  # Daha önce yazdığınız add_team_member fonksiyonunu içe aktar

def show_create_team_page(user_id):
    """Takım oluşturma sayfasını gösterir."""
    create_team_window = tk.Tk()
    create_team_window.title("Takım Oluştur")
    create_team_window.geometry("400x400")
    create_team_window.resizable(False, False)

    # Sayfa başlığı
    title_label = tk.Label(create_team_window, text="Takım Oluştur", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Üye listesi başlığı
    member_list_label = tk.Label(create_team_window, text="Takım Üyeleri", font=("Arial", 12, "bold"))
    member_list_label.pack(pady=5)

    # Üye listesi
    member_listbox = tk.Listbox(create_team_window, width=50, height=10)
    member_listbox.pack(pady=10)

    # Takıma üye ekleme butonu
    add_member_button = tk.Button(create_team_window, text="Takıma Üye Ekle", command=lambda: add_member(create_team_window, member_listbox, user_id), width=20, height=2, font=("Arial", 12), bg="#4CAF50", fg="white")
    add_member_button.pack(pady=10)

    # Ana sayfaya dönme butonu
    back_button = tk.Button(create_team_window, text="Geri", command=create_team_window.destroy, width=10, height=2, font=("Arial", 12), bg="#FF9800", fg="white")
    back_button.pack(pady=10)

    create_team_window.mainloop()


from team_operations import add_team_member, get_username_by_id  # Yeni get_username_by_id fonksiyonu dahil edildi
from team_operations import add_team_member, get_username_by_id  # Yeni get_username_by_id fonksiyonu dahil edildi
from logger import Logger  # Logger sınıfını ekliyoruz


def add_member(create_team_window, member_listbox, user_id):
    """Takıma üye eklemek için kullanıcıdan ID alır ve listeyi günceller."""
    logger = Logger()  # Logger sınıfını oluşturuyoruz
    team_member_id = simpledialog.askstring("Takım Üyesi Ekle",
                                            "Eklemek istediğiniz takım üyesinin kullanıcı ID'sini girin:")

    if team_member_id:
        try:
            # Takım üyesi ID'sini int'e çeviriyoruz
            team_member_id = int(team_member_id)

            # Takıma üye ekleme fonksiyonunu çağırıyoruz
            add_team_member(user_id, team_member_id)

            # Kullanıcının adını almak için get_username_by_id fonksiyonunu çağırıyoruz
            username = get_username_by_id(team_member_id)
            if username:
                # Kullanıcının adını listbox'a ekliyoruz
                member_listbox.insert(tk.END, f"{username} (ID: {team_member_id})")
                messagebox.showinfo("Başarı", f"{username} başarıyla takıma eklendi!")

                # Başarılı ekleme işlemini logluyoruz
                logger.log_team_operation(operation="Üye ekleme", user_id=team_member_id, success=True)
            else:
                messagebox.showerror("Hata", "Kullanıcı adı alınamadı.")
                # Kullanıcı adı alınamama durumunu logluyoruz
                logger.log_team_operation(operation="Üye ekleme (Kullanıcı adı alınamadı)", user_id=team_member_id,
                                          success=False)
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz ID girildi.")
            # Geçersiz ID durumunu logluyoruz
            logger.log_team_operation(operation="Üye ekleme (Geçersiz ID)", user_id=None, success=False)
        except Exception as e:
            messagebox.showerror("Hata", f"Takım üyesi eklenirken hata oluştu: {e}")
            # Genel hata durumunu logluyoruz
            logger.log_team_operation(operation="Üye ekleme", user_id=team_member_id, success=False)
    else:
        messagebox.showwarning("Uyarı", "Takım üyesi ID'si girilmedi.")
        # Kullanıcı herhangi bir ID girmediğinde logluyoruz
        logger.log_team_operation(operation="Üye ekleme (ID girilmedi)", user_id=None, success=False)
