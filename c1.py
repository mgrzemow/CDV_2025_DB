# na bazie powyższego przykładu
# napisać kilka funkcji:
# 1. Tworzącą bazę
# 2. Dodającą osobę do bazy
# 3. Wyszukującą osoby - najprościej po imieniu, a co jak więcej kryteriów?
# 4. Usuwającą rekordy po id
import sqlite3
# jak wypełnić danymi
import faker

f = faker.Faker('PL_pl')
print(f.first_name())
print(f.last_name())
print(f.email())
print(f.pyint(18, 89))


# standard funckji:
def szukaj_czlowieka(cursor, imie):
    ...

# if __name__ == '__main__':
#     with sqlite3.connect('test.db') as conn:
#         cursor = conn.cursor()
#         for r in szukaj_czlowieka(cursor, 'Jan'):
#             print(r)
    