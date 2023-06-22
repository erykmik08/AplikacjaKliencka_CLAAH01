import psycopg
import json
import csv


def importuj_klientow(cur):
    nazwa = input("Podaj nazwe pliku csv z klientami (z rozszerzeniem): ")
    with open(nazwa, "r") as plik:
        lista = []
        reader = csv.reader(plik, delimiter=";")
        for line in reader:
            lista.append(line)
        cur.executemany("""INSERT INTO klienci VALUES (%s, %s, %s, %s)""", lista)
    return


def importuj_odczyty(cur):
    nazwa = input("Podaj nazwe pliku csv z odczytami (z rozszerzeniem): ")
    with open(nazwa, "r") as plik:
        lista = []
        reader = csv.reader(plik, delimiter=";")
        for line in reader:
            lista.append(line)
        cur.executemany("""INSERT INTO odczyty VALUES (%s, %s, %s, %s)""", lista)
    return
    
    
def importuj():
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
            importuj_klientow(cur)
            importuj_odczyty(cur)
        conn.commit()
    except Exception as ex:
        print("Wystapil blad podczas importowania bazy danych: " + str(ex))
    
    conn.close()
    return


if __name__ == '__main__':
    importuj()