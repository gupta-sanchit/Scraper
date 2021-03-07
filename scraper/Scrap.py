import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
from scraper.pageCount import PageCount


class Scraper:
    def __init__(self):
        self.res = {}
        self.pageCount = 1
        self.url = 'https://www.midsouthshooterssupply.com/dept/reloading/primers'

        self.headers = {"Accept-Language": "en-US, en;q=0.5"}
        res = requests.get(self.url, headers=self.headers)

        self.soup = BeautifulSoup(res.text, "lxml")
        self.number_of_pages()

    def number_of_pages(self):
        p = PageCount(self.soup)
        self.pageCount = p.getCount() if p.getCount() > self.pageCount else self.pageCount

    def scrapPage(self):
        productContainer = self.soup.findAll('div', class_='product')
        resPage = {}
        for one in productContainer:
            div1 = one.find('div', class_='product-description')
            div2 = one.find('div', class_='catalog-item-price')

            productID = div1.find('span', class_='product-id').text
            name = div1.a.text
            brand = div1.find('a', class_='catalog-item-brand').text

            price = div2.find('span', class_='price').text
            status = div2.find('span', class_='status').text

            perPiece = div2.find('div', style='float: left')
            perPiece = perPiece.text.split(" ")[0] if perPiece else 'NA'

            r = {
                'product-id': productID,
                'name': name,
                'price': price,
                'brand': brand,
                'per-piece-price': perPiece,
                'status': status
            }
            resPage[productID] = r
        return resPage

    def getRes(self):

        for i in range(1, self.pageCount + 1):
            if i != 1:
                url = self.url + f"?currentpage={i}"
                res = requests.get(url, headers=self.headers)
                self.soup = BeautifulSoup(res.text, "lxml")

            self.res.update(self.scrapPage())

        return self.res


s = Scraper()
data = s.getRes()

with open('res.json', 'w') as fp:
    json.dump(data, fp, sort_keys=True, indent=4)
