import mysql.connector

def connect_to_database():
    """MySQL veritabanına bağlanır ve bağlantı nesnesini döner."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your password",
            database="database name"
        )
        print("Veritabanına başarılı bir şekilde bağlandı.")
        return connection
    except mysql.connector.Error as err:
        print(f"Veritabanı bağlantı hatası: {err}")
        return None
