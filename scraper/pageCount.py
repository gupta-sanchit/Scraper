import re


class PageCount:

    def __init__(self, soup):
        self.soup = soup
        self.count = 0

    def getCount(self):
        urls = []
        for link in self.soup.find_all('a', href=re.compile('dept/reloading/primers\?currentpage=[0-9]+$')):
            lk = link['href']
            if lk not in urls:
                urls.append(lk)

        for i in urls:
            c = [int(char) for char in list(i) if char.isdigit()]
            if len(c) != 0:
                c = c[0]
                self.count = c if c > self.count else self.count
        return self.count
