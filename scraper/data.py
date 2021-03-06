import requests
from bs4 import BeautifulSoup
from pprint import pprint
from scraper.pageCount import PageCount

url = 'https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1'
headers = {"Accept-Language": "en-US, en;q=0.5"}
res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.text, "lxml")

productContainer = soup.findAll('div', class_='product')
res = {}
for one in productContainer:
    price = one.find('span', class_='price').text
    name = one.find('div', class_='product-description').a.text
    productID = one.find('span', class_='product-id').text
    status = one.find('span', class_='status').text
    brand = one.find('a', class_='catalog-item-brand').text

    perPiece = one.find('div', style='float: left')
    perPiece = perPiece.text.split(" ")[0] if perPiece else 'NA'

    r = {
        'product-id': productID,
        'name': name,
        'price': price,
        'brand': brand,
        'per-piece-price': perPiece,
        'status': status
    }
    res[productID] = r
pprint(res)

# forRating = one.find('div', class_='catalog-item-price').find_next_sibling()['id']


p = PageCount(soup)
print("Page Count ==>", p.getCount())
