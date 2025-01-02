import multiprocessing
import os
from datetime import datetime

class Logger:
    def __init__(self):
        # Log dosyalarının dizinini belirliyoruz
        self.log_dir = os.path.join(os.getcwd(), "logs")

        # Eğer log dizini yoksa, oluşturuyoruz
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Log dosyalarının yolları
        self.log_files = {
            'backup': os.path.join(self.log_dir, 'backup_operations_log.txt'),
            'team_operations': os.path.join(self.log_dir, 'team_operations_log.txt'),
            'document_sharing': os.path.join(self.log_dir, 'document_sharing_log.txt'),
            'password_change': os.path.join(self.log_dir, 'password_change_log.txt'),
            'user_operations': os.path.join(self.log_dir, 'user_operations_log.txt'),
            'anormal_davranislar': os.path.join(self.log_dir, 'anormal_davranislar_log.txt'),  # Yeni log dosyası
        }

    def log(self, category, message):
        """Verilen kategoriye ait log dosyasina mesaj yaz."""
        log_file = self.log_files.get(category)
        if log_file:
            with open(log_file, 'a', encoding='utf-8-sig') as file:
                file.write(message + "\n")

    def log_backup_operation(self, source_dir, backup_dir, file_name, success=True):
        """Yedekleme islemi logunu yaz"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Yedekleme islemi
        status = 'Basariyla' if success else 'Basarisiz'
        message = f"Baslangic: {start_time} | Islem: Yedekleme | Durum: {status} | Kaynak: {source_dir} | Hedef: {backup_dir} | Dosya: {file_name}"
        self.log('backup', message)

    def log_team_operation(self, operation, user_id, success=True):
        """Takim islemleri logunu yaz"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 'Basariyla' if success else 'Basarisiz'
        message = f"Baslangic: {start_time} | Islem: {operation} | Durum: {status} | KullanicI DId: {user_id}"
        self.log('team_operations', message)

    def log_document_sharing(self, file_name, user_id, success=True):
        """Dokuman paylasimi islemi logunu yaz"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 'Basariyla' if success else 'Basarisiz'
        message = f"Baslangic: {start_time} | Islem: Paylasim | Durum: {status} | Dosya: {file_name} | KullanicI DId: {user_id}"
        self.log('document_sharing', message)

    def log_password_change(self, user_id, success=True):
        """Parola degistirme islemi logunu yaz"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 'Basariyla' if success else 'Basarisiz'
        message = f"Baslangic: {start_time} | Islem: Parola Degistirme | Durum: {status} | KullanicI DId: {user_id}"
        self.log('password_change', message)

    def log_user_operation(self, operation, user_id, success=True):
        """Kullanici islemleri logunu yaz"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 'Basariyla' if success else 'Basarisiz'
        message = f"Baslangic: {start_time} | Islem: {operation} | Durum: {status} | KullanicI DId: {user_id}"
        self.log('user_operations', message)

    def log_anormal_davranis(self, user_id, behavior_description):
        """Anormal davranış logunu yaz"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"Başlangıç: {start_time} | Anormal Davranış: {behavior_description} | Kullanıcı ID: {user_id}"
        self.log('anormal_davranislar', message)

    def log_anormal_davranis2(self, user_id, behavior_description):
        """Anormal davranış logunu yazmak için bir işlem başlat"""

        def log_task(user_id, behavior_description):
            start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"Başlangıç: {start_time} | Anormal Davranış: {behavior_description} | Kullanıcı ID: {user_id}"
            self.log('anormal_davranislar', message)

        process = multiprocessing.Process(target=log_task, args=(user_id, behavior_description))
        process.start()