import shutil
import os

import mysql

from mysql_connection import connect_to_database

def share_file(sender_id, receiver_id, local_path):
    """Dosyayı sunucuya yükler ve paylaşır."""
    # Sunucudaki hedef dizin
    server_directory = "shared_files/"
    if not os.path.exists(server_directory):
        os.makedirs(server_directory)

    # Dosya adı ve hedef path
    file_name = os.path.basename(local_path)
    server_path = os.path.join(server_directory, file_name)

    # Dosya boyutu kontrolü (100 MB)
    max_size = 100 * 1024 * 1024  # 100 MB
    if os.path.getsize(local_path) > max_size:
        print("Dosya çok büyük. Lütfen daha küçük bir dosya yükleyin.")
        return

    # Dosya formatı kontrolü
    allowed_extensions = ['.txt', '.pdf', '.jpg', '.png']
    file_extension = os.path.splitext(file_name)[1].lower()
    if file_extension not in allowed_extensions:
        print("Geçersiz dosya formatı. Lütfen uygun bir dosya formatı seçin.")
        return

    # Dosyayı sunucuya kopyala
    try:
        shutil.copy(local_path, server_path)
        print(f"Dosya {server_path} konumuna başarıyla yüklendi.")
    except FileNotFoundError:
        print("Dosya bulunamadı. Lütfen geçerli bir dosya yolu girin.")
        return
    except shutil.Error as e:
        print(f"Dosya yükleme hatası: {e}")
        return

    # Veritabanına paylaşımı kaydet
    max_retries = 3
    for attempt in range(max_retries):
        try:
            connection = connect_to_database()
            break
        except mysql.connector.Error as err:
            if attempt < max_retries - 1:
                print("Veritabanı bağlantısı başarısız. Yeniden deniyorum...")
                continue
            else:
                print("Veritabanına bağlanılamadı.")
                return

    if connection:
        try:
            cursor = connection.cursor()

            # Takım üyeliği kontrolü
            check_query = """
                SELECT * FROM team_members 
                WHERE user_id = %s AND team_member_id = %s 
            """
            cursor.execute(check_query, (sender_id, receiver_id))
            if not cursor.fetchone():
                print("Bu kullanıcı sizin takım üyeniz değil. Dosya paylaşımı yapılamaz.")
                return

            # Veritabanına paylaşımı kaydet
            insert_query = """
                INSERT INTO shared_files (sender_id, receiver_id, file_path) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (sender_id, receiver_id, server_path))
            connection.commit()
            print("Dosya başarıyla paylaşıldı ve veritabanına kaydedildi.")
        except mysql.connector.Error as err:
            print(f"Dosya paylaşımı hatası: {err}")
        finally:
            connection.close()