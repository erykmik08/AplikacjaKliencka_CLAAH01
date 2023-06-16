import sqlite3
import csv

def main():
    while True:
        conn = sqlite3.connect("dane.db")
        cur = conn.cursor()

        print("Wybierz opcje: ")
        print("    q/Q - WYJŚCIE")
        print("    1. Wczytywanie pomiarow")
        print("    2. Wypisz pomiary (w konsoli)")
        print("    3. Wczytaj baze danych do pliku CSV")
        choice = input("Wybor > ")
        
        if choice.casefold() == "q":
            break
        if choice == "1":
            wczytywanie(conn, cur)
        elif choice == "2":
            wypisywanie(cur)
        else:
            generuj_csv(cur)

        conn.close()
    
    
def wczytywanie(conn, cur):
    choice = input("Czy chcesz usunac stara baze danych (jezeli istnieje)? T/N > ")
    if choice.casefold() == "t":
        cur.execute("""drop table if exists pomiary;""")
    cur.execute("""create table if not exists pomiary (id integer primary key autoincrement,
                                                       miejscowosc varchar(30) not null,
                                                       ulica varchar(10) not null,
                                                       nr_domu integer not null,
                                                       nr_mieszkania integer,
                                                       zuzycie integer not null
                                                       );""")
    conn.commit()
    liczba_pomiarow = int(input("Podaj ile odczytow chcesz podac: "))
    
    try:
        for i in range(liczba_pomiarow):
            print(f"Pomiar {i+1}")
            miejscowosc = input("Miejscowosc pomiaru: ")
            ulica = input("Nazwa ulicy: ")
            nr_domu = int(input("Nr domu: "))
            nr_mieszkania = int(input("Nr mieszkania: "))
            zuzycie = int(input("Zuzycie wody: "))
            cur.execute(f"""insert into pomiary (miejscowosc, ulica, nr_domu, nr_mieszkania, zuzycie) values
            ('{miejscowosc}', '{ulica}', {nr_domu}, {nr_mieszkania}, {zuzycie})""")
        conn.commit()    
    except Exception as ex:
        print("Wystapil nieoczekiwany blad podczas wczytywania danych!" + str(ex))
    return


def wypisywanie(cur):
    try:
        cur.execute("SELECT * FROM pomiary")
        print("Krotki w bazie danych: ")
        for pomiar in cur.fetchall():
            print(pomiar)
    except Exception as ex:
        print("Wystapil nieoczekiwany blad podczas wypisywania danych!" + str(ex))
    return


def generuj_csv(cur):
    try:
        cur.execute("SELECT * FROM pomiary")
        with open("pomiary.csv", "w") as plik:
            zapis = csv.writer(plik, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for krotka in cur.fetchall():
                zapis.writerow(krotka)
                #for dana in krotka:
                #    print(str(dana), end=";", file=plik)
                #print(file=plik)
                
    except Exception as ex:
        print("Wystapil nieoczekiwany blad podczas wypisywania danych!" + str(ex))
    return