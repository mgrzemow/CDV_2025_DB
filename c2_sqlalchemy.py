from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from faker import Faker
import random

# Inicjalizacja bazy danych
engine = create_engine("sqlite:///baza.db", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Definicja tabel
class Osoba(Base):
    __tablename__ = "osoby"

    id = Column(Integer, primary_key=True, autoincrement=True)
    imie = Column(String, nullable=False)
    nazwisko = Column(String, nullable=False)
    wiek = Column(Integer)

    zamowienia = relationship("Zamowienie", back_populates="klient", cascade="all, delete-orphan")


class Zamowienie(Base):
    __tablename__ = "zamowienia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kwota = Column(Float)
    klient_id = Column(Integer, ForeignKey("osoby.id"))

    klient = relationship("Osoba", back_populates="zamowienia")


# Funkcje operacyjne
def stworz_baze():
    """Tworzy strukture bazy danych."""
    Base.metadata.drop_all(engine)  # Usuwa stare tabele
    Base.metadata.create_all(engine)  # Tworzy nowe tabele
    print("Baza danych zostala utworzona.")


def uzupelnij_osoby(liczba_rekordow=10):
    """Uzupelnia tabele osoby losowymi danymi."""
    fake = Faker("pl_PL")
    with Session() as sesja:
        osoby = [Osoba(imie=fake.first_name(), nazwisko=fake.last_name(), wiek=fake.random_int(min=0, max=120)) for _ in
                 range(liczba_rekordow)]
        sesja.add_all(osoby)
        sesja.commit()
    print(f"{liczba_rekordow} rekordow zostalo dodanych do tabeli osoby.")


def uzupelnij_zamowienia(liczba_rekordow=20):
    """Uzupelnia tabele zamowienia losowymi danymi."""
    with Session() as sesja:
        klienci = sesja.query(Osoba.id).all()
        klienci_ids = [k[0] for k in klienci]

        if not klienci_ids:
            print("Brak klientow w bazie! Najpierw uzupelnij tabele osoby.")
            return

        zamowienia = [Zamowienie(kwota=round(random.uniform(-100, 1000), 2), klient_id=random.choice(klienci_ids)) for _
                      in range(liczba_rekordow)]
        sesja.add_all(zamowienia)
        sesja.commit()
    print(f"{liczba_rekordow} rekordow zostalo dodanych do tabeli zamowienia.")


def wyszukaj_osobe(imie=None, nazwisko=None):
    """Wyszukuje osoby po imieniu, nazwisku lub obu jednoczesnie."""
    with Session() as sesja:
        zapytanie = sesja.query(Osoba)
        if imie:
            zapytanie = zapytanie.filter(Osoba.imie == imie)
        if nazwisko:
            zapytanie = zapytanie.filter(Osoba.nazwisko == nazwisko)
        return zapytanie.all()


def wyszukaj_zamowienia_po_kliencie(klient_id):
    """Wyszukuje zamowienia po ID klienta."""
    with Session() as sesja:
        return sesja.query(Zamowienie).filter(Zamowienie.klient_id == klient_id).all()


def usun_osobe_po_id(osoba_id):
    """Usuwa osobe o podanym ID (zamowienia usuwaja sie automatycznie)."""
    with Session() as sesja:
        osoba = sesja.query(Osoba).filter(Osoba.id == osoba_id).first()
        if osoba:
            sesja.delete(osoba)
            sesja.commit()
            print(f"Osoba o ID {osoba_id} zostala usunieta.")
        else:
            print(f"Osoba o ID {osoba_id} nie istnieje.")


# Przykladowe uzycie
if __name__ == "__main__":
    stworz_baze()
    uzupelnij_osoby(10)
    uzupelnij_zamowienia(20)

    # Wyszukaj osoby
    print("Wyniki wyszukiwania dla imienia 'Jan':", wyszukaj_osobe(imie="Jan"))
    print("Wyniki wyszukiwania dla nazwiska 'Kowalski':", wyszukaj_osobe(nazwisko="Kowalski"))
    print("Wyniki wyszukiwania dla imienia 'Jan' i nazwiska 'Kowalski':",
          wyszukaj_osobe(imie="Jan", nazwisko="Kowalski"))

    # Wyszukaj zamowienia klienta o ID 1
    print("Zamowienia klienta o ID 1:", wyszukaj_zamowienia_po_kliencie(1))

    # Usun osobe o ID 1
    usun_osobe_po_id(1)
