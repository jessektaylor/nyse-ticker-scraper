import scrapy
import time
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from shutil import which

class NyseSpider(scrapy.Spider):
    name = 'nyse'
    allowed_domains = ['www.eoddata.com/symbols.aspx']
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    start_urls = ['https://www.eoddata.com/stocklist/NYSE/{}.htm'.format(letter) for letter in letters]
        

    def parse(self, response):
        path = which('chromedriver')
        options = webdriver.ChromeOptions()
        # options.add_argument('--no-sandbox')
        options.add_argument('headless')
        options.add_argument('--disable-dev-shm-usage')        
        options.add_argument('window-size=1200x600')
        self.driver = webdriver.Chrome(executable_path=path,options=options)

        print(response.url)
        self.driver.get(response.url) 
        time.sleep(3)
        self.html = self.driver.page_source
        sel  = Selector(text=self.html)
     
        
        rows = sel.xpath('.//table[@class="quotes"]/tbody/tr')
        for row in rows:
            ticker = row.xpath('.//td/a[starts-with(@title,"Display Quote & Chart for NYSE")]/text()').get()
            company_name = row.xpath('.//td[2]/text()').get()
            high = row.xpath('.//td[3]/text()').get()
            low = row.xpath('.//td[4]/text()').get()
            close = row.xpath('.//td[5]/text()').get()
            volume =row.xpath('.//td[6]/text()').get()

            if ticker and company_name and high and low and close and volume:
                object = {'ticker':ticker, 
                        'company_name':company_name,
                        'high':high, 
                        'low':low, 
                        'close':close,
                        'volume':volume
                        }
                yield object