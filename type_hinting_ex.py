import random

# hintowanie typów wartości zwracanych i parametrów
def cos_zwracam(n: int) -> int | float | str:
    return random.choice([12, 33.5, 'ala'][:n])

def cos_zwracam_bez_hintow(n):
    return random.choice([12, 33.5, 'ala'][:n])

# hintowanie zmiennych
x : int | float | str = cos_zwracam_bez_hintow(2)

# hintowanie typów klas:
class Klasa:
    atr1 : str = 'asdasd'

# da się programowo dostać do informacji otype hintach
import typing
print(typing.get_type_hints(cos_zwracam))
# zaawansowane narzędzia potrafią z tego korzystać żeby automatycznie generować kod
# dobre źródło type hintingu:
# https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html