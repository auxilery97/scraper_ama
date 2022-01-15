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
        for link in self.links:
            self.WC.get("https://www.amazon.de" + link)
            soup = bs4.BeautifulSoup(self.WC.pageSource, features="html.parser")
            itemParameters = soup.find_all("span", {"class": "a-size-base a-text-bold"})
            print(itemParameters)
            newAmazonItem = {}

            for param in itemParameters:
                paramName = param.getText()
                if (param is not None):
                    parent = param.findParent("tr", { "class": "a-spacing-small"})
                    if (parent):
                        paramValues = parent.find_all("td", {"class": "a-span9"})
                        paramValue = [b.getText() for b in paramValues][0]
                        newAmazonItem[paramName] = paramValue
            print(newAmazonItem)
            #brands = [brand.findParent("div", { "class": "a-spacing-small"}) for brand in brands if "Marke" in brand.getText()]

            # print(brands)
        self.WC.webdriver.close()


sc = SoupController()
soup = sc.getThatSoup("https://www.amazon.de/s?k=isomatte&crid=IT7HEBYSO3WC&sprefix=isomatt%2Caps%2C165&ref=nb_sb_noss_2")
links = sc.getLinks()
sc.goInThatLinks()
#print(links)