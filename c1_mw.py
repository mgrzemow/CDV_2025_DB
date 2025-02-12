# na bazie powyższego przykładu
# napisać kilka funkcji:
# 1. Tworzącą bazę
# 2. Dodającą osobę do bazy
# 3. Wyszukującą osoby - najprościej po imieniu, a co jak więcej kryteriów?
# 4. Usuwającą rekordy po id
import sqlite3


def dodaj_osobe(conn, imie, nazwisko, wiek):
    c = conn.cursor()
    sql = '''
        insert into osoby (imie, nazwisko, wiek) values (?, ?, ?)
        '''
    c.execute(sql, (imie, nazwisko, wiek))


def wyszukaj_osobę(conn, osoba):
    c = conn.cursor()
    sql = '''
    select * from osoby where imie = ?
    '''
    for id, imie, nazwisko, wiek in c.execute(sql, (osoba,)):
        print(id, imie, nazwisko, wiek)


def usun_osobe(conn, osoba):
    c = conn.cursor()
    sql = '''
    select id from osoby where imie = ?
    '''
    c.execute(sql, (osoba,))
    ident = c.fetchone()
    sql = '''
    delete from osoby where id = ?
    '''
    c.execute(sql, (ident[0],))


if __name__ == '__main__':
    with sqlite3.connect(f'baza.db') as conn:
        dodaj_osobe(conn, 'Ala', 'Nowak', 23)
        wyszukaj_osobę(conn, 'Ala')
        usun_osobe(conn, 'Ala')
    print('tu już połączenie jest zamknięte')
