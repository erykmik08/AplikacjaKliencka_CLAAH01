import psycopg
import json

def buduj():
    # Odczytaj plik JSON
    with open("database_creds.json", "r") as json_file:
        dane = json.loads(json_file.read())
    # Polacz sie z baza danych
    conn = psycopg.connect(dbname=dane["db_name"],
                            user=dane["user_name"],
                            password=dane["password"],
                            host=dane["host_name"],
                            port=dane["port_number"]
                           )
    try:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS klienci (
                                    ID_klienta INTEGER PRIMARY KEY,
                                    Imie VARCHAR(20) NOT NULL,
                                    Nazwisko VARCHAR(20) NOT NULL,
                                    Adres VARCHAR(60) NOT NULL
                                );

                                CREATE TABLE IF NOT EXISTS odczyty (
                                    ID_odczytu SERIAL PRIMARY KEY,
                                    Wartosc INTEGER NOT NULL,
                                    Data_odczytu DATE DEFAULT (date('now')) NOT NULL,
                                    ID_klienta INTEGER NOT NULL,
                                    FOREIGN KEY (ID_klienta) REFERENCES klienci (ID_klienta) ON DELETE CASCADE
                                );""")
        conn.commit()
    except Exception as ex:
        print("Wystapil blad podczas tworzenia bazy danych: " + str(ex))
    
    conn.close()
    return


if __name__ == '__main__':
    buduj()