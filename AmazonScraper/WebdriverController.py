from selenium import webdriver
from selenium.webdriver.common.by import By

class WebdriverController:

    def __init__(self):
        self.webdriver = webdriver.Firefox()
        self.pageSource = None

    def get(self, url):
        print(url)
        self.webdriver.get(url=url)
        try:
            el = self.webdriver.find_element(By.XPATH, '//*[@id="sp-cc-accept"]')
            el.click()
        except:
            print("There is no cookie to accept :(")
        self.pageSource = self.webdriver.page_source

    def getElementByXPath(self, xpath):
        return self.webdriver.find_element(By.XPATH, xpath)

    def getSource(self): #return source for soup
        return self.pageSource

    def pressButton(self, xpath):
        self.webdriver.find_element(By.XPATH, xpath)


