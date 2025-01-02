from watchdog.events import FileSystemEventHandler
import shutil
import os
import time
from watchdog.observers import Observer
from logger import Logger
from datetime import datetime

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, source_dir, backup_dir):
        self.source_dir = source_dir #kaynak dizin ;)
        self.backup_dir = backup_dir #hedef dizin
        self.logger = Logger()  # Logger nesnesini başlatıyoruz

    def on_created(self, event):
        if not event.is_directory:
            self.backup_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.backup_file(event.src_path)

    def backup_file(self, src_path):
        try:
            # Yedekleme işleminin başlangıç zamanını al
            start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Dosyanın yedeğini oluştur
            relative_path = os.path.relpath(src_path, self.source_dir)
            backup_path = os.path.join(self.backup_dir, relative_path)

            os.makedirs(os.path.dirname(backup_path), exist_ok=True)  # Hedef dizini oluştur
            shutil.copy2(src_path, backup_path)  # Dosyayı kopyala (metadata dahil)

            # Yedekleme başarıyla gerçekleşti, log yazıyoruz
            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # İşlem bitiş zamanı
            self.logger.log_backup_operation(self.source_dir, self.backup_dir, src_path, success=True)
            print(f"Dosya yedeklendi: {src_path} -> {backup_path}")
        except Exception as e:
            # Hata durumunda log yazıyoruz
            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # İşlem bitiş zamanı
            self.logger.log_backup_operation(self.source_dir, self.backup_dir, src_path, success=False)
            print(f"Yedekleme sırasında hata oluştu: {e}")

# start_watching fonksiyonunun doğru şekilde tanımlanması
def start_watching(source_dir, backup_dir):
    print(f"Baslangic: {source_dir} izleniyor ve {backup_dir} dizinine kopyalanacak.")
    event_handler = FileEventHandler(source_dir, backup_dir)
    observer = Observer()
    observer.schedule(event_handler, path=source_dir, recursive=True)
    observer.start()
    print("Dosya izleme baslatildi...")
    try:
        while True:
            time.sleep(1)  # Burada 'time' modülünün sleep fonksiyonu kullanılıyor datetime degil
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
