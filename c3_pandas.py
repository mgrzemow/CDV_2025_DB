import pandas
# uwagna DSN
# https://docs.sqlalchemy.org/en/20/core/engines.html
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///baza.db")
with engine.connect() as polaczenie:
    # df = pd.read_sql_table("osoby", con=polaczenie)
    df = pd.read_sql('select * from osoby', con=polaczenie)
    print(df)
    df.to_sql('osoby2', con=polaczenie, if_exists='replace')
    