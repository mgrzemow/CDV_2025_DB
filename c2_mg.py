import sqlite3
from faker import Faker
import random

# standard dbapi2.0


def stworz_baze(kursor):
    """Tworzy tabele osoby i zamowienia. Jesli istnieja, usuwa je przed stworzeniem nowych."""
    kursor.execute("DROP TABLE IF EXISTS zamowienia")
    kursor.execute("DROP TABLE IF EXISTS osoby")

    kursor.execute("""
        CREATE TABLE osoby (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imie TEXT NOT NULL,
            nazwisko TEXT NOT NULL,
            wiek INTEGER
        )
    """)

    kursor.execute("""
        CREATE TABLE zamowienia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kwota REAL,
            klient_id INTEGER,
            FOREIGN KEY (klient_id) REFERENCES osoby(id) ON DELETE CASCADE
        )
    """)

    print("Baza danych zostala utworzona.")


def uzupelnij_osoby(kursor, liczba_rekordow=10):
    """Uzupelnia tabele osoby losowymi danymi."""
    fake = Faker("pl_PL")
    dane = [(fake.first_name(), fake.last_name(), fake.random_int(min=0, max=120)) for _ in range(liczba_rekordow)]
    kursor.executemany("INSERT INTO osoby (imie, nazwisko, wiek) VALUES (?, ?, ?)", dane)
    print(f"{liczba_rekordow} rekordow zostalo dodanych do tabeli osoby.")


def uzupelnij_zamowienia(kursor, liczba_rekordow=20):
    """Uzupelnia tabele zamowienia losowymi danymi."""
    kursor.execute("SELECT id FROM osoby")
    klienci = [wiersz[0] for wiersz in kursor.fetchall()]

    if not klienci:
        print("Brak klientow w bazie! Najpierw uzupelnij tabele osoby.")
        return

    dane = [(round(random.uniform(-100, 1000), 2), random.choice(klienci)) for _ in range(liczba_rekordow)]
    kursor.executemany("INSERT INTO zamowienia (kwota, klient_id) VALUES (?, ?)", dane)
    print(f"{liczba_rekordow} rekordow zostalo dodanych do tabeli zamowienia.")


def wyszukaj_osobe(kursor, imie=None, nazwisko=None):
    """Wyszukuje osoby po imieniu, nazwisku lub obu jednoczesnie."""
    zapytanie = "SELECT * FROM osoby WHERE 1=1"
    parametry = []

    if imie:
        zapytanie += " AND imie = ?"
        parametry.append(imie)
    if nazwisko:
        zapytanie += " AND nazwisko = ?"
        parametry.append(nazwisko)

    kursor.execute(zapytanie, tuple(parametry))
    return kursor.fetchall()


def wyszukaj_zamowienia_po_kliencie(kursor, klient_id):
    """Wyszukuje zamowienia po ID klienta."""
    kursor.execute("SELECT * FROM zamowienia WHERE klient_id = ?", (klient_id,))
    return kursor.fetchall()


def usun_osobe_po_id(kursor, osoba_id):
    """Usuwa osobe o podanym ID (zamowienia usuwaja sie automatycznie)."""
    kursor.execute("DELETE FROM osoby WHERE id = ?", (osoba_id,))
    print(f"Osoba o ID {osoba_id} zostala usunieta.")


# Przykladowe uzycie z menedzerem kontekstu:
if __name__ == "__main__":
    with sqlite3.connect("baza.db") as polaczenie:
        kursor = polaczenie.cursor()

        stworz_baze(kursor)  # Tworzy tabele
        uzupelnij_osoby(kursor, 10)  # Dodaje 10 klientow
        uzupelnij_zamowienia(kursor, 20)  # Dodaje 20 zamowien

        # Wyszukaj osoby po imieniu "Jan"
        wyniki = wyszukaj_osobe(kursor, imie="Jan")
        print("Wyniki wyszukiwania dla imienia 'Jan':", wyniki)

        # Wyszukaj osoby po nazwisku "Kowalski"
        wyniki = wyszukaj_osobe(kursor, nazwisko="Kowalski")
        print("Wyniki wyszukiwania dla nazwiska 'Kowalski':", wyniki)

        # Wyszukaj osoby po imieniu "Jan" i nazwisku "Kowalski"
        wyniki = wyszukaj_osobe(kursor, imie="Jan", nazwisko="Kowalski")
        print("Wyniki wyszukiwania dla imienia 'Jan' i nazwiska 'Kowalski':", wyniki)

        # Wyszukaj zamowienia klienta o ID 1
        zamowienia = wyszukaj_zamowienia_po_kliencie(kursor, 1)
        print("Zamowienia klienta o ID 1:", zamowienia)

        # Usun osobe o ID 1 (zamowienia tej osoby usuna sie automatycznie)
        usun_osobe_po_id(kursor, 1)
