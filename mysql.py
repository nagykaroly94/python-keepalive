import os # Fájlkezeléshez 
import subprocess # Parancssor futtatásához Pythonból (a titkosított fájl dekódolása).
import configparser # INI fájlok beolvasásához és feldolgozásához.
import mysql.connector # MySQL adatbázis kapcsolatok kezeléséhez.
import threading # Több szál létrehozásához (hogy párhuzamosan tudjon több adatbázis kapcsolódni).
import time # Időzítéshez (pl. alvási időszak beállítása a kapcsolatok életben tartása során).

# Dekódolt konfigurációs fájl neve
DECRYPTED_CONFIG_FILE = 'config.ini'

# Dekódolja a titkosított konfigurációs fájlt
def decrypt_config():
    try:
        subprocess.run(['gpg', '--decrypt', '--output', DECRYPTED_CONFIG_FILE, 'config.ini.gpg'], check=True)
    except subprocess.CalledProcessError as e: # Ha a dekódolás közben hibára fut akkor kilép és hibaüzenetet ad.
        print(f"Error decrypting config file: {e}")
        exit(1)

# MySQL kapcsolat életben tartása
def keep_alive(host, user, password, database):
    connection = mysql.connector.connect(
        host=host, # Az adatbázis szerver címe.
        user=user, # Az adatbázis felhasználóneve.
        password=password, # Az adatbázis felhasználó jelszava.
        database=database # Az adatbázis neve.
    )
    while True:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1;")
            time.sleep(300)  # Folyamatosan (5 percenként) egy egyszerű SQL lekérdezést futtat le, hogy a kapcsolat ne szakadjon meg inaktivitás miatt.
        except mysql.connector.Error as err: # Ha hiba lép fel (pl. kapcsolat megszakad), akkor újra próbálkozik a kapcsolódással háromszor, 5 másodperces késleltetéssel.
            print(f"Error: {err}")
            connection.reconnect(attempts=3, delay=5)

# Fő program
def main():
    # Dekódolja a konfigurációs fájlt
    decrypt_config()

    # Be olvassa a konfigurációs fájlt
    config = configparser.ConfigParser()
    config.read(DECRYPTED_CONFIG_FILE)

    # Adatbázis kapcsolatok paraméterei. A program felvan készítve arra, hogy akármennyi adatbázist tudjon kezelni. A lista bármeddig bővíthető.
    # Fontos megjegyezni, hogy a config.ini fájlban benne kell lennie minden szükséges adatnak.
    connections = [
        {"host": "hosztnev1", "user": config['database1']['user'], "password": config['database1']['password'], "database": "adatbazis1"},
        {"host": "hosztnev2", "user": config['database2']['user'], "password": config['database2']['password'], "database": "adatbazis2"},
        {"host": "hosztnev3", "user": config['database3']['user'], "password": config['database3']['password'], "database": "adatbazis3"},
        {"host": "hosztnev4", "user": config['database4']['user'], "password": config['database4']['password'], "database": "adatbazis4"},
        {"host": "hosztnev5", "user": config['database5']['user'], "password": config['database5']['password'], "database": "adatbazis5"},
        {"host": "hosztnev6", "user": config['database6']['user'], "password": config['database6']['password'], "database": "adatbazis6"}
    ]

    # Szálak létrehozása és indítása
    threads = []
    for conn_params in connections:
        thread = threading.Thread(target=keep_alive, args=(conn_params["host"], conn_params["user"], conn_params["password"], conn_params["database"]))
        threads.append(thread)
        thread.start()

    # Threadek futtatásának biztosítása
    for thread in threads:
        thread.join()

    # Dekódolt konfigurációs fájl törlése a biztonság érdekében
    os.remove(DECRYPTED_CONFIG_FILE)

if __name__ == "__main__":
    main()