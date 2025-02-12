import sqlite3

if __name__ == '__main__':
    with sqlite3.connect('test.db') as conn:
        # poczytać o kursorach typu dict, często DictCursor
        # one zwracają dane w postaci słowników:
        # {
        #     'imie': 'Ala',
        #     'nazwisko': 'Kowalska',
        #     'wiek': 23
        # }

        c = conn.cursor()
        sql_drop = 'drop table if exists osoby'
        c.execute(sql_drop)

        create_table = '''
        create table osoby (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imie text,
        nazwisko text,
        wiek integer
        )
        '''

        c.execute(create_table)

        sql_insert = f"""
        insert into osoby (imie, nazwisko, wiek) values 
        (?, ?, ?)
        """

        c.execute(sql_insert, ('Jan', 'Kowalski', 23))
        print('Dodano Jan Kowalski o id', c.lastrowid)
        c.execute(sql_insert, ('Ala', 'Nowak', 32))
        print('Dodano Ala Nowak o id', c.lastrowid)
        c.execute(sql_insert, ('Paweł', 'Kowalski', 33))
        print('Dodano Paweł Kowalski o id', c.lastrowid)

        sql_select  = '''
        select * from osoby
        where nazwisko = ?
        '''

        for id, imie, nazwisko, wiek in c.execute(sql_select, ('Kowalski',)):
            print(imie, nazwisko, wiek)

        # conn.commit()
        # conn.rollback()
