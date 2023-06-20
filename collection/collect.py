import sqlite3
import csv

""" Aplikacja do mobilnego zbierania informacji o klientach i odczytów ich domowych liczników.
    
    Funkcja main() stanowi główne ciało programu i umożliwia wybranie przez użytkownika różnych funkcji.
    Możliwe jest tworzenie, usuwanie, wyswietlanie oraz modyfikacja bazy danych zapisanej przy użyciu sqlite3.
    Zebrane dane mogą być zapisane do plików csv - klienci.csv oraz odczyty.csv.
    
    Każdy odczyt jest powiązany z unikalnym ID klienta w bazie danych.
"""


def main():
    while True:
        try:
            conn = sqlite3.connect("baza_danych.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON;")

            print("Wybierz opcje: ")
            print("    q/Q - WYJŚCIE")
            print("    1. Usun dotychczasowa baze danych")
            print("    2. Dodaj klientow")
            print("    3. Dodaj odczyty")
            print("    4. Wypisz odczyty")
            print("    5. Zapisz dane do pliku CSV")
            choice = input("Wybor > ")

            if choice.casefold() == "q":
                break
            elif choice == "1":
                usun_db(conn, cur)
            elif choice == "2":
                dodaj_klientow(conn, cur)
            elif choice == "3":
                dodaj_odczyty(conn, cur)
            elif choice == "4":
                wypisz(cur)
            elif choice == "5":
                zapisz_csv(cur)
            else:
                print("Nie znaleziono takiej opcji!")

            conn.close()
        except Exception as ex:
            print("Wystapil blad! " + str(ex))

            
def usun_db(conn, cur):
    try:
        choice = input("Czy chcesz usunac stara baze danych (jezeli istnieje)? T/N > ")
        if choice.casefold() == "t":
            cur.executescript("""drop table if exists klienci;
                                 drop table if exists odczyty""")
        conn.commit()
    except Exception as ex:
        print("Wystapil blad podczas usuwania bazy danych: " + str(ex))
    return

    
def stworz_db(conn, cur):
    try:
        cur.executescript("""CREATE TABLE IF NOT EXISTS klienci (
                                ID_klienta INTEGER PRIMARY KEY,
                                Imie VARCHAR(20) NOT NULL,
                                Nazwisko VARCHAR(20) NOT NULL,
                                Adres VARCHAR(60) NOT NULL
                            );

                            CREATE TABLE IF NOT EXISTS odczyty (
                                ID_odczytu INTEGER PRIMARY KEY AUTOINCREMENT,
                                Wartosc INTEGER NOT NULL,
                                Data_odczytu DATE DEFAULT (date('now')) NOT NULL,
                                ID_klienta INTEGER NOT NULL,
                                FOREIGN KEY (ID_klienta) REFERENCES klienci (ID_klienta) ON DELETE CASCADE
                            );""")
        conn.commit()
    except Exception as ex:
        print("Wystapil blad podczas tworzenia bazy danych: " + str(ex))
    return


def dodaj_klientow(conn, cur):
    # Utwórz bazę danych (klienci + odczyty), jeżeli jeszcze nie istnieje
    stworz_db(conn, cur)
    liczba_klientow = int(input("Podaj ile klientow chcesz dodac: "))
    try:
        for i in range(liczba_klientow):
            print(f"Klient {i+1}")
            id_klienta = int(input("Unikatowe ID klienta: "))
            imie = input("Imie klienta: ")
            nazwisko = input("Nazwisko klienta: ")
            adres = input("Adres klienta: ")
            cur.execute(f"""insert into klienci values ({id_klienta}, '{imie}', '{nazwisko}', '{adres}')""")
        conn.commit()    
    except Exception as ex:
        print("Wystapil nieoczekiwany blad podczas wczytywania klientow! " + str(ex))
    return


def dodaj_odczyty(conn, cur):
    try:
        wybor = input("Czy chcesz pomocniczno wyswietlic liste zapisanych klientow? (T/t) ")
        if wybor.casefold() == "t":
            cur.execute("select * from klienci")
            print("ID\tImie\tNazwisko\tAdres")
            for klient in cur.fetchall():
                for atrybut in klient:
                    print(str(atrybut) + "\t", end="")
                print()
                
        liczba_odczytow = int(input("Podaj ile odczytow chcesz dodac: "))
        for i in range(liczba_odczytow):
            print(f"Odczyt {i+1}")
            wartosc = int(input("Wartosc odczytu: "))
            id_klienta = int(input("Unikatowe ID klienta (istniejace w bazie danych): "))
            cur.execute(f"""insert into odczyty (ID_klienta, Wartosc) values ({id_klienta}, {wartosc})""")
        conn.commit()    
    except Exception as ex:
        print("Wystapil blad podczas wczytywania odczytow! " + str(ex))
    return


def wypisz(cur):
    try:
        cur.execute("""SELECT klienci.ID_klienta, klienci.Adres, odczyty.Wartosc, odczyty.Data_odczytu FROM klienci, odczyty
                       WHERE klienci.ID_klienta = odczyty.ID_klienta""")
        print("ID klienta\tAdres\tWartosc\tData odczytu")
        for odczyt in cur.fetchall():
            for atrybut in odczyt:
                print(str(atrybut) + "\t", end="")
            print()
    except Exception as ex:
        print("Wystapil nieoczekiwany blad podczas wypisywania danych! " + str(ex))
    return


def zapisz_csv(cur):
    try:
        cur.execute("SELECT * FROM klienci")
        with open("klienci.csv", "w") as plik:
            zapis = csv.writer(plik, delimiter=';')
            for krotka in cur.fetchall():
                zapis.writerow(krotka)
        cur.execute("SELECT * FROM odczyty")
        with open("odczyty.csv", "w") as plik:
            zapis = csv.writer(plik, delimiter=';')
            for krotka in cur.fetchall():
                zapis.writerow(krotka)       
    except Exception as ex:
        print("Wystapil nieoczekiwany blad podczas wypisywania danych!" + str(ex))
    return