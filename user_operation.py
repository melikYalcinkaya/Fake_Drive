import hashlib
import mysql
import datetime
from datetime import timedelta

import logger
from mysql_connection import connect_to_database

# add user
def add_user(username, password, email):
    """Yeni bir kullanıcı ekler."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            query = "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password_hash, email))
            connection.commit()
            print("Kullanıcı başarıyla eklendi.")
        except mysql.connector.Error as err:
            print(f"Kullanıcı ekleme hatası: {err}")
        finally:
            connection.close()

# kullanicidan yeni kullanici ismi alacagiz eger veri tabaninda zaten
# boyle bir isim kayıtlı degil ise (unique) ismi degistirecegim.
def update_username(user_id, new_username):
    """Kullanıcı adını günceller."""
    from mysql_connection import connect_to_database  # Bağlantıyı al
    from logger import Logger  # Logger sınıfını import ediyoruz

    logger = Logger()  # Logger nesnesini başlatıyoruz
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()

            # Benzersizlik kontrolü
            check_query = "SELECT id FROM users WHERE username = %s"
            cursor.execute(check_query, (new_username,))
            if cursor.fetchone():
                print("Bu kullanıcı adı zaten kullanılıyor. Lütfen farklı bir ad seçin.")
                logger.log_user_operation("username_update", user_id, success=False)
                return

            # Güncelleme işlemi
            update_query = "UPDATE users SET username = %s WHERE id = %s"
            cursor.execute(update_query, (new_username, user_id))
            connection.commit()
            print("Kullanıcı adı başarıyla güncellendi.")
            logger.log_user_operation("username_update", user_id, success=True)
        except mysql.connector.Error as err:
            print(f"Kullanıcı adı güncelleme hatası: {err}")
            logger.log_user_operation("username_update", user_id, success=False)
        finally:
            connection.close()

# user tablosundaki kisinin id'sini cekmek icin fonksiyonum.
def get_user_id_by_username(username):
    """Kullanıcı adından kullanıcı ID'sini döner."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()

            # Kullanıcı adı ile ID'yi getiren sorgu
            query = "SELECT id FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result:
                return result[0]  # İlk sütun (id) döndürülür
            else:
                print("Bu kullanıcı adıyla eşleşen bir kullanıcı bulunamadı.")
                return None
        except mysql.connector.Error as err:
            print(f"Kullanıcı ID'sini getirme hatası: {err}")
            return None
        finally:
            connection.close()


# email'i guncelleme
def update_email(user_id, new_email):
    """Kullanıcının e-posta adresini günceller."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()

            # Güncelleme sorgusu
            update_query = "UPDATE users SET email = %s WHERE id = %s"
            cursor.execute(update_query, (new_email, user_id))
            connection.commit()

            if cursor.rowcount > 0:
                print("E-posta adresi başarıyla güncellendi.")
            else:
                print("E-posta adresi güncellenemedi. Kullanıcı ID'si bulunamadı veya gmail zaten var.")
        except mysql.connector.Error as err:
            print(f"E-posta güncelleme hatası: {err}")
        finally:
            connection.close()


# sifre guncelleme talebi
def request_password_change(user_id):
    """Kullanıcı için parola değiştirme isteği oluşturur."""
    from mysql_connection import connect_to_database  # Bağlantıyı al
    from logger import Logger  # Logger sınıfını import ediyoruz

    logger = Logger()  # Logger nesnesini başlatıyoruz
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()

            # Aynı kullanıcı için zaten bekleyen bir istek var mı kontrol et
            check_query = "SELECT * FROM password_requests WHERE user_id = %s AND status = 'pending'"
            cursor.execute(check_query, (user_id,))
            if cursor.fetchone():
                print("Bu kullanıcı için zaten bekleyen bir parola değiştirme isteği var.")
                logger.log_password_change(user_id, success=False)
                return

            # Yeni parola değiştirme isteği oluştur
            insert_query = "INSERT INTO password_requests (user_id) VALUES (%s)"
            cursor.execute(insert_query, (user_id,))
            connection.commit()
            print("Parola değiştirme isteği başarıyla oluşturuldu.")
            logger.log_password_change(user_id, success=True)
        except mysql.connector.Error as err:
            print(f"Parola değiştirme isteği oluşturma hatası: {err}")
            logger.log_password_change(user_id, success=False)
        finally:
            connection.close()


# user_operation.py
from logger import Logger  # Logger sınıfını ekliyoruz
import hashlib


def check_user_credentials(username, password):
    """Kullanıcı adı ve şifreyi doğrular ve kullanıcı ID'sini döner."""
    logger = Logger()  # Logger sınıfını oluşturuyoruz
    connection = connect_to_database()

    if connection:
        try:
            cursor = connection.cursor()
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            query = "SELECT id FROM users WHERE username = %s AND password_hash = %s"
            cursor.execute(query, (username, password_hash))
            result = cursor.fetchone()

            if result:
                user_id = result[0]
                # Başarılı giriş logu
                logger.log_user_operation(operation="Giriş doğrulama", user_id=user_id, success=True)
                return user_id  # Kullanıcı ID'sini döndür
            else:
                # Başarısız giriş logu
                logger.log_user_operation(operation="Giriş doğrulama (Geçersiz kullanıcı adı/şifre)", user_id=None,
                                          success=False)
                return None
        except Exception as e:
            # Hata durumunu logla
            logger.log_user_operation(operation="Giriş doğrulama (Hata)", user_id=None, success=False)
            print(f"Hata: {e}")
            return None
        finally:
            connection.close()
    else:
        # Bağlantı kurulamazsa logla
        logger.log_user_operation(operation="Giriş doğrulama (Bağlantı hatası)", user_id=None, success=False)
    return None


#sifreyi degismek isteyenleri alip admin panelinde gosterecegım
def fetch_password_requests():
    """Şifre değişim taleplerini veritabanından çeker."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT pr.id, u.username, u.email, pr.status 
                FROM password_requests pr
                JOIN users u ON pr.user_id = u.id
                WHERE pr.status = 'pending'
            """
            cursor.execute(query)
            requests = cursor.fetchall()
            return requests  # Talepleri döndür
        except Exception as e:
            print(f"Şifre değişim taleplerini çekerken hata: {e}")
            return []
        finally:
            connection.close()
    return []



#veritabaninda talepin durumunu guncelleyecegiz.
def update_password_request_status(request_id, status):
    """Şifre değişim talebini onaylar veya reddeder."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()

            # Durum ve işlem tarihi güncelleme sorgusu
            query = """
                UPDATE password_requests
                SET status = %s, processed_at = %s
                WHERE id = %s
            """
            processed_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(query, (status, processed_at, request_id))
            connection.commit()

            if cursor.rowcount > 0:
                print(f"Talep ID: {request_id}, durum: {status} olarak güncellendi.")
            else:
                print(f"Talep ID: {request_id} güncellenemedi. Geçersiz ID olabilir.")
        except Exception as e:
            print(f"Şifre talep güncelleme hatası: {e}")
        finally:
            connection.close()


def send_request_notifications():
    """Kullanıcılara talep durumu bildirimi gönderir."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()

            # Durumu "accepted" veya "rejected" olan talepleri alıyoruz
            query = """
                SELECT pr.id, pr.user_id, pr.status, u.username 
                FROM password_requests pr
                JOIN users u ON pr.user_id = u.id
                WHERE pr.status IN ('accepted', 'rejected')
            """
            cursor.execute(query)
            requests = cursor.fetchall()

            for request in requests:
                request_id, user_id, status, username = request
                message = ""

                # Duruma göre mesaj belirleme
                if status == "accepted":
                    message = "Talebiniz onaylandı"
                elif status == "rejected":
                    message = "Talebiniz reddedildi"

                # Bildirim veritabanına ekleniyor
                insert_query = "INSERT INTO notification (user_id, message, created_at) VALUES (%s, %s, NOW())"
                cursor.execute(insert_query, (user_id, message))
                connection.commit()

                print(f"Kullanıcı {username} için bildirim gönderildi: {message}")

        except mysql.connector.Error as err:
            print(f"Bildirimi gönderme hatası: {err}")
        finally:
            connection.close()


# Kullanıcı giriş denemelerinin ve parola değiştirme taleplerinin sayısı
failed_login_attempts = {}
password_change_requests = {}

from datetime import datetime  # doğru içe aktarma

# Logger sınıfını içeri aktarın
from logger import Logger

# Logger sınıfını başlatın
logger = Logger()

def track_failed_login(user_id):
    now = datetime.now()
    if user_id not in failed_login_attempts:
        failed_login_attempts[user_id] = []
    failed_login_attempts[user_id].append(now)

    # Başarısız giriş denemelerinin sayısını kontrol et
    recent_attempts = [t for t in failed_login_attempts[user_id] if now - t < timedelta(minutes=10)]
    if len(recent_attempts) >= 3:
        # logger'ı burada kullanın
        logger.log_anormal_davranis(user_id, "Üçüncü başarısız giriş denemesi")
        # Kullanıcıya uyarı gösterilebilir

def track_password_change(user_id):
    now = datetime.now()
    if user_id not in password_change_requests:
        password_change_requests[user_id] = []
    password_change_requests[user_id].append(now)

    # Sürekli parola değiştirme taleplerini kontrol et
    recent_requests = [t for t in password_change_requests[user_id] if now - t < timedelta(minutes=10)]
    if len(recent_requests) >= 3:
        # logger'ı burada kullanın
        logger.log_anormal_davranis(user_id, "Sürekli parola değiştirme talebi")
        # Kullanıcıya uyarı gösterilebilir
