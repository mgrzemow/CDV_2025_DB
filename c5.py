# 1. Napisać klasę modelową Ksiazka zawierającą następujące dane:
# - tytul
# - autor
# - rok wydania
# - ilosc stron
# 2. Podłączyć się do bazy sqlite w pamięci i stworzyć strukturę bazy
# 3. Dodaj klasę Autor powiązaną relacją one-to-many

from sqlalchemy.orm import sessionmaker, relationship
from typing import Optional, List
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import MetaData, select
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
if __name__ == '__main__':

    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    metadata = MetaData()
    Base = declarative_base()


    class Autor(Base):
        __tablename__ = "autorzy"
        id: Mapped[int] = mapped_column(primary_key=True)
        imie_nazwisko: Mapped[str]
        ksiazki: Mapped[List["Ksiazka"]] = relationship(back_populates="autor")

        def __repr__(self) -> str:
            return f'Autor(id={self.id}, imie_nazwisko="{self.imie_nazwisko}")'


    class Ksiazka(Base):
        __tablename__ = "ksiazki"
        id: Mapped[int] = mapped_column(primary_key=True)
        tytul:Mapped[str]
        rok_wydania: Mapped[Optional[int]]
        ilosc_stron: Mapped[Optional[int]]
        autor_id: Mapped[int] = mapped_column(ForeignKey("autorzy.id"))
        autor: Mapped["Autor"] = relationship(back_populates="ksiazki")

        def __repr__(self) -> str:
            return f'Ksiazka(id={self.id}, tytul="{self.tytul}", autor="{self.autor}")'

        def __str__(self) -> str:
            return f'Ksiazka(id={self.id}, tytul="{self.tytul}", autor="{self.autor}", rok_wydania={self.rok_wydania}, ilosc_stron={self.ilosc_stron})'




    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sesja = Session()

    a1 = Autor(imie_nazwisko='Franz Kafka')
    k1 = Ksiazka(tytul='Proces', autor=a1, rok_wydania=1933, ilosc_stron=221)
    k2 = Ksiazka(tytul='Proces2', autor=a1, rok_wydania=1933, ilosc_stron=222)
    sesja.add_all([a1, k1, k2])
    sesja.commit()
    k3 = Ksiazka(tytul='Proces3', rok_wydania=1933, ilosc_stron=222)
    a1.ksiazki.append(k3)
    sesja.commit()
    print(a1.ksiazki[1].autor.ksiazki)
    stmt = select(Ksiazka).where(Ksiazka.autor_id == 1)
    print(stmt)
    # uwaga - jednoelementowa krotka
    print(sesja.execute(stmt).first())

    # jak łatwiej:
    print(sesja.execute(stmt).scalars().first())
    print(sesja.scalars(stmt).first())
