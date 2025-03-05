# 1. Napisać klasę modelową Ksiazka zawierającą następujące dane:
# - tytul
# - autor
# - rok wydania
# - ilosc stron
# 2. Podłączyć się do bazy sqlite w pamięci i stworzyć strukturę bazy
from sqlalchemy.orm import sessionmaker
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
if __name__ == '__main__':

    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
    metadata = MetaData()
    Base = declarative_base()

    class Ksiazka(Base):
        __tablename__ = "ksiazki"
        id: Mapped[int] = mapped_column(primary_key=True)
        tytul:Mapped[str]
        autor: Mapped[str]
        rok_wydania: Mapped[Optional[int]]
        ilosc_stron: Mapped[Optional[int]]

        def __repr__(self) -> str:
            return f'Ksiazka(id={self.id}, tytul="{self.tytul}", autor="{self.autor}"'

        def __str__(self) -> str:
            return f'Ksiazka(id={self.id}, tytul="{self.tytul}", autor="{self.autor}", rok_wydania={self.rok_wydania}, ilosc_stron={self.ilosc_stron})'

    Base.metadata.create_all(engine)
    k1 = Ksiazka(tytul='Proces', autor='Franz Kafka', rok_wydania=1933, ilosc_stron=221)
    print(k1)

    Session = sessionmaker(bind=engine)
    sesja = Session()
    sesja.add(k1)
    print(k1)
    print(f'Lista nowych, niezapisanych obiektów: {sesja.new}')
    sesja.commit()
    print(f'Lista nowych, niezapisanych obiektów: {sesja.new}')

    print(f'Lista zmodyfikowanych obiektów: {sesja.dirty}')
    k1.ilosc_stron = 333
    print(f'Lista zmodyfikowanych obiektów: {sesja.dirty}')
    sesja.commit()
    print(f'Lista zmodyfikowanych obiektów: {sesja.dirty}')
    for r in sesja.query(Ksiazka).all():
        print(r)
    k2 = sesja.query(Ksiazka).filter_by(tytul='Proces').first()
    print(k2)
    print('Lista skasowanych: ', sesja.deleted)
    sesja.delete(k2)
    print('Lista skasowanych: ', sesja.deleted)
    sesja.commit()
    print('Lista skasowanych: ', sesja.deleted)


