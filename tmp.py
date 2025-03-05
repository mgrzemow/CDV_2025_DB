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

    engine = create_engine("sqlite+pysqlite:///tmp.db", echo=True)
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
    k2 = Ksiazka(tytul='Proces2', autor='Franz Kafka', rok_wydania=1933, ilosc_stron=221)

    Session = sessionmaker(bind=engine)
    sesja = Session()
    sesja.add(k1)
    input('stop')
    sesja.flush()
    sesja.add(k2)
    input('stop')
    sesja.commit()

