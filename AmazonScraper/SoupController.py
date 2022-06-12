import bs4
import WebdriverController

class SoupController:
    def __init__(self):
        self.WC = WebdriverController.WebdriverController()

    def getThatSoup(self, url):
        self.WC.get(url=url)
        self.soup = bs4.BeautifulSoup(self.WC.pageSource, features="html.parser")
        return self.soup

    def getLinks(self):
        self.getThatSoup("https://www.amazon.de/s?k=isomatte&crid=IT7HEBYSO3WC&sprefix=isomatt%2Caps%2C165&ref=nb_sb_noss_2")
        bigDiv = self.soup.find_all("div", {"class": "s-matching-dir sg-col-16-of-20 sg-col sg-col-8-of-12 sg-col-12-of-16"})
        self.links = []
        try:
            elements = bigDiv[0].find_all_next("h2", {"class": "a-size-mini a-spacing-none a-color-base s-line-clamp-2"})
            for e in elements:
                nextLinks = e.find_all_next("a", {"class": "a-link-normal"})
                for l in nextLinks:
                    linkUrl = l["href"]
                    self.links.append(linkUrl)

            self.links = set([link for link in self.links if "/s" not in link[:2]  and "https" not in link[:5] and "#" not in link[:1]])
        except:
            print("No divs")
        return self.links

    def goInThatLinks(self):
        print(f"Number of items to scan: {len(self.links)}")
        for link in self.links:
            self.WC.get("https://www.amazon.de" + link)
            soup = bs4.BeautifulSoup(self.WC.pageSource, features="html.parser")
            itemParameters = soup.find_all("span", {"class": "a-size-base a-text-bold"})
            otherParams = soup.find_all("th", {"class" : "a-color-secondary a-size-base prodDetSectionEntry"})
            print("firstParams: ", itemParameters)
            print("secondParam: ", otherParams)
            newAmazonItem = {}

            for param in itemParameters:
                paramName = param.getText()
                if (param is not None):
                    parent = param.findParent("tr", { "class": "a-spacing-small"})
                    if (parent):
                        paramValues = parent.find_all("td", {"class": "a-span9"})
                        paramValue = [b.getText() for b in paramValues][0]
                        newAmazonItem[paramName] = paramValue

            table1 = soup.find_all("table", {"id": "productDetails_detailBullets_sections1"})
            table1Value = self.tableToObject(table1[0])
            for i in table1Value.keys():
                print(f"try to set, {i}1")
                a = table1Value[i]
                newAmazonItem[i] = table1Value[i]

            table2 = soup.find_all("table", {"id": "productDetails_techSpec_section_1"})
            table2Value = self.tableToObject(table2[0])

            for i in table2Value.keys():
                a = table2Value[i]
                newAmazonItem[i] = a

            print(newAmazonItem)
            print("Scanning next...")
            #brands = [brand.findParent("div", { "class": "a-spacing-small"}) for brand in brands if "Marke" in brand.getText()]

            # print(brands)
        self.WC.webdriver.close()

    def tableToObject(self, table):
        ths = table.find_all("th")
        tds = table.find_all("td")

        tableObject = {}
        for (name, value) in zip(ths, tds):
            newName = name.getText().replace(" ", "")

            tableObject[newName] = value.getText()

        print("TableObject:", tableObject)
        return tableObject


sc = SoupController()
soup = sc.getThatSoup(
    "https://www.amazon.de/s?k=isomatte&crid=IT7HEBYSO3WC&sprefix=isomatt%2Caps%2C165&ref=nb_sb_noss_2")
links = sc.getLinks()
sc.goInThatLinks()
#print(links)