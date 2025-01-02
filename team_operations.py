from mysql_connection import connect_to_database
import mysql
import os
import shutil


# Kullanıcıya takım üyesi ekleme
# user_id = takımı oluşturan kullanıcı
# team_member_id = eklenmek istenen takım üyesi
def add_team_member(user_id, team_member_id):
    """Bir kullanıcıyı takıma ekler."""
    if user_id == team_member_id:
        print("Kendi kendinizi takım üyesi olarak belirleyemezsiniz.")
        return

    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()

            # Aynı üyelik zaten var mı kontrol et
            check_query = """
                SELECT * FROM team_members 
                WHERE user_id = %s AND team_member_id = %s
            """
            cursor.execute(check_query, (user_id, team_member_id))
            if cursor.fetchone():
                print("Bu kullanıcı zaten takım üyesi.")
                return

            # Takım üyesini ekle
            insert_query = """
                INSERT INTO team_members (user_id, team_member_id) 
                VALUES (%s, %s)
            """
            cursor.execute(insert_query, (user_id, team_member_id))
            connection.commit()
            print("Takım üyesi başarıyla eklendi.")

            # Bildirim Gönder
            sender_name = get_username_by_id(user_id)
            message = f"{sender_name} sizi takımına ekledi."
            insert_notification_query = """
                INSERT INTO notifications (user_id, message) VALUES (%s, %s)
            """
            cursor.execute(insert_notification_query, (team_member_id, message))
            connection.commit()
            print("Bildirim gönderildi.")
        except mysql.connector.Error as err:
            print(f"Takım üyesi ekleme hatası: {err}")
        finally:
            connection.close()



# kullanicinin ismini veritabanindan cekiyorum. daha sonra lsitbox icerisinde gosterebilecegim.
def get_username_by_id(user_id):
    """Verilen user_id ile kullanıcı adını döndürür."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT username FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                return result[0]  # username döndürülüyor
            else:
                print("Kullanıcı bulunamadı.")
                return None
        except mysql.connector.Error as err:
            print(f"Kullanıcı adı çekme hatası: {err}")
            return None
        finally:
            connection.close()


def get_team_members(user_id):
    """Verilen user_id'ye ait takım üyelerini döndürür."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT u.username, u.id
                FROM team_members tm
                JOIN users u ON tm.team_member_id = u.id
                WHERE tm.user_id = %s
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            return results  # [(username1, id1), (username2, id2), ...]
        except mysql.connector.Error as err:
            print(f"Takım üyelerini çekme hatası: {err}")
            return []
        finally:
            connection.close()


#bildirim sayfasinda mesaj gonderilecek. takıma sizi katti diye.
def get_notification(user_id):
    """Kullanıcıya ait bildirimleri döndürür, şifre talep cevabını da ekler."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT message, created_at
                FROM notifications
                WHERE user_id = %s
                ORDER BY created_at DESC
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            # Şifre talep cevaplarını da alalım
            password_request_notifications = get_password_request_notifications(user_id)
            results.extend(password_request_notifications)

            return results  # [(message1, date1), (message2, date2), ...]
        except mysql.connector.Error as err:
            print(f"Bildirim çekme hatası: {err}")
            return []
        finally:
            connection.close()


def get_password_request_notifications(user_id):
    """Şifre talep cevaplarını döndürür."""
    # Örnek olarak şifre talep bildirimlerini manuel olarak ekliyoruz.
    # Gerçek uygulamada veritabanında ilgili taleplerin durumlarına göre veri çekebilirsiniz.
    return [("Şifre talebiniz onaylandı.", "2024-12-28")]


def send_password_request_notification(user_id, message):
    """Şifre talep cevabını bildirim olarak ekler."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            insert_query = "INSERT INTO notifications (user_id, message) VALUES (%s, %s)"
            cursor.execute(insert_query, (user_id, message))
            connection.commit()
            print(f"Şifre talep bildirimi gönderildi: {message}")
        except mysql.connector.Error as err:
            print(f"Şifre talep bildirimi gönderme hatası: {err}")
        finally:
            connection.close()


from mysql_connection import connect_to_database
import mysql.connector
  # Yeni eklediğimiz fonksiyonu içe aktar

def send_file_to_team(user_id, file_path, team_members):
    """Dosyayı takım üyeleriyle paylaşır."""
    file_name = file_path.split('/')[-1]  # Dosya adını al

    for member in team_members:
        member_id = member[1]  # Üye ID'si

        # Dosyayı fiziksel olarak paylaş
        share_file_with_user(file_path, member_id,user_id)

        # Dosya paylaşımını veritabanına kaydet
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                insert_query = """
                    INSERT INTO shared_files (sender_id, receiver_id, file_path, shared_date) 
                    VALUES (%s, %s, %s, NOW())
                """
                cursor.execute(insert_query, (user_id, member_id, file_path))

                connection.commit()
                print(f"Dosya {file_name} {member_id} kullanıcısına gönderildi ve veritabanına kaydedildi.")
            except mysql.connector.Error as err:
                print(f"Dosya kaydetme hatası: {err}")
            finally:
                connection.close()

        # Bildirim gönderme işlemi
        send_file_notification(member_id, user_id, file_name)


def get_shared_files(user_id):
    """Verilen user_id'ye ait paylaşılan dosyaları döndürür."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT file_name, file_path
                FROM shared_files
                WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            return results  # [(file_name1, file_path1), (file_name2, file_path2), ...]
        except mysql.connector.Error as err:
            print(f"Paylaşılan dosyaları çekme hatası: {err}")
            return []
        finally:
            connection.close()

def send_file_notification(member_id, sender_id, file_name):
    """Dosya gönderildiğinde bildirimi veritabanına kaydeder."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            message = f"{get_username_by_id(sender_id)} size şu dosyayı yolladı: {file_name}"
            insert_query = "INSERT INTO notifications (user_id, message) VALUES (%s, %s)"
            cursor.execute(insert_query, (member_id, message))
            connection.commit()
            print(f"Bildirim gönderildi: {message}")
        except mysql.connector.Error as err:
            print(f"Bildirim gönderme hatası: {err}")
        finally:
            connection.close()


import os
import shutil
import mysql.connector
from datetime import datetime

import os
import shutil
import mysql.connector

def share_file_with_user(file_path, receiver_id, sender_id):
    """
    Paylaşılan dosyayı ilgili kullanıcının klasörüne taşır ve veritabanına kaydeder.
    """
    # Ana shared_files dizinini kontrol et ve oluştur
    base_directory = "shared_files"
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    # Kullanıcıya ait alt dizini kontrol et ve oluştur
    user_directory = os.path.join(base_directory, f"user_{receiver_id}")
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)

    # Dosyayı yeni dizine taşı
    try:
        file_name = os.path.basename(file_path)
        target_path = os.path.join(user_directory, file_name)  # Dosya yeni dizine taşınıyor

        # Hedef dizini ve yolu kontrol et
        print(f"Dosya hedef yolu: {target_path}")

        # Dosya kopyalanıyor
        shutil.copy(file_path, target_path)
        print(f"{file_name} dosyası {user_directory} dizinine kopyalandı.")

        # Veritabanına kaydet
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                insert_query = """
                    INSERT INTO shared_files (sender_id, receiver_id, file_path, shared_date) 
                    VALUES (%s, %s, %s, NOW())
                """
                cursor.execute(insert_query, (sender_id, receiver_id, target_path))
                connection.commit()
                print(f"Paylaşım veritabanına kaydedildi: {file_name}")
            except mysql.connector.Error as err:
                print(f"Veritabanına kaydetme hatası: {err}")
            finally:
                connection.close()

    except Exception as e:
        print(f"Dosya taşıma sırasında hata oluştu: {e}")
