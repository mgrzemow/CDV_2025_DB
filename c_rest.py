import requests
url_szablon = 'https://api.nbp.pl/api/exchangerates/rates/a/{}/?format=json'
waluta = 'usd'
r = requests.get(url_szablon.format(waluta))
r.raise_for_status()
j = r.json()
print(j['rates'][0]['mid'])

r = requests.get('https://api.nbp.pl/api/exchangerates/tables/a/?format=json')
r.raise_for_status()
j = r.json()
for r in j[0]['rates']:
    print(f'{r["code"]}: {r["mid"]}')

# https://fakestoreapi.com/products
r = requests.get('https://fakestoreapi.com/products')
r.raise_for_status()
j = r.json()
for product in j:
    id = product['id']
    title = product['title']
    price = product['price']
    print(f'{id}, {title}, {price}')