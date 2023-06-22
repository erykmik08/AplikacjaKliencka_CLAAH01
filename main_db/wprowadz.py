import psycopg
import json


def wprowadz_klientow(cur):
    liczba_klientow = int(input("Podaj ile klientow chcesz dodac: "))
    for i in range(liczba_klientow):
            print(f"Klient {i+1}")
            id_klienta = int(input("Unikatowe ID klienta: "))
            imie = input("Imie klienta: ")
            nazwisko = input("Nazwisko klienta: ")
            adres = input("Adres klienta: ")
            cur.execute(f"""insert into klienci values ({id_klienta}, '{imie}', '{nazwisko}', '{adres}')""")
    return


def wprowadz_odczyty(cur):
    liczba_odczytow = int(input("Podaj ile odczytow chcesz dodac: "))
    for i in range(liczba_odczytow):
        print(f"Odczyt {i+1}")
        wartosc = int(input("Wartosc odczytu: "))
        id_klienta = int(input("Unikatowe ID klienta (istniejace w bazie danych): "))
        cur.execute(f"""insert into odczyty (ID_klienta, Wartosc) values ({id_klienta}, {wartosc})""")
    return
    
    
def wprowadz():
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
        wybor = input("Czy chcesz wprowadzic klientow (K/k) czy odczyty?")
        with conn.cursor() as cur:
            if wybor.casefold() == "k":
                wprowadz_klientow(cur)
            else:
                wprowadz_odczyty(cur)
            
        conn.commit()
    except Exception as ex:
        print("Wystapil blad podczas wprowadzania do bazy danych: " + str(ex))
    
    conn.close()
    return


if __name__ == '__main__':
    wprowadz()