from threading import Thread

from GUI_Codes.admin_main_page import show_admin_main_page
from GUI_Codes.register_ui import show_registration_page
from GUI_Codes.email_update_page import show_update_email_page
from file_watcher import start_watching

from GUI_Codes.main_page import show_main_page
from logger import Logger
from user_operation import add_user, update_username, update_email, request_password_change
from GUI_Codes import register_ui

if __name__ == "__main__":
    # kullanici bilgilerini elle almak icin

    #username = input("Kullanıcı adı: ")
    #password = input("Parola: ")
    #email = input("E-posta: ")
    #add_user(username, password, email)


    #add_user("Anita Yilmaz","hatayli","anita@gmail.com")
    #add_user("Mauro Icardi","arjantinli","icardi@gmail.com")



    # kullanici adini guncelleme
    #user_id = int(input("Güncellemek istediğiniz kullanıcının ID'si: "))
    #new_username = input("Yeni kullanıcı adı: ")
    #update_username(user_id, new_username)

    #user_id = int(input("Güncellemek istediğiniz kullanıcının ID'si: "))
    #new_email = input("Yeni e-posta adresi: ")
    #update_email(user_id, new_email)

    #user_id = int(input("Parola değiştirme isteği göndermek istediğiniz kullanıcının ID'si: "))
    #request_password_change(user_id)

    # İzleme ve yedekleme dizinlerini tanımla
    source_dir = r"shared_files"
    backup_dir = r"shared_files(copy)"

    # İzleme işlemini bir arka plan thread'inde başlat
    watcher_thread = Thread(target=start_watching, args=(source_dir, backup_dir), daemon=True)
    watcher_thread.start()

    # Arayüzü başlat
    show_registration_page()

