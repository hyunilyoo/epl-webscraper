import scrapy
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from scrapy.selector import Selector
from tables_crawler.items import TablesCrawlerItem

class TableSpider(scrapy.Spider):
    name = "Tables"
    allowed_domains = ["premierleague.com"]
    start_urls = ["https://www.premierleague.com/tables"]
    
    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome('/Users/hyunilyoo/Documents/analytics/chromedriver')
        
    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5)
        self.html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        self.selector = Selector(text=self.html)
        self.season_epl = len(self.selector.xpath('//*[@id="mainContent"]/div[2]/div[1]/div[1]/section/div[2]/ul/li'))+1
        
        # Season dropdown
        for i in range(2, self.season_epl):
            time.sleep(5)
            self.browser.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div[1]/div[1]/section/div[2]/div[2]').click()
            time.sleep(3)

            if i < 10: 
                self.browser.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div[1]/div[1]/section/div[2]/ul/li'+f'[{i}]').click()

            elif i >= 10 and i < 19:
                self.browser.execute_script('window.scrollTo(0, 150)')
                self.browser.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div[1]/div[1]/section/div[2]/ul/li'+f'[{i}]').click()

            else:
                self.browser.execute_script('window.scrollTo(0, 330)')
                self.browser.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div[1]/div[1]/section/div[2]/ul/li'+f'[{i}]').click()

            time.sleep(5)
            self.html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
            self.selector = Selector(text=self.html)
            self.rows = self.selector.xpath('//*[@id="mainContent"]/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr[not(@class="expandable")]')

            for row in self.rows:
                self.item = TablesCrawlerItem()
                self.item["club_name"] = row.xpath('./td[3]/a/span[2]/text()')[0].extract()
                self.item["position"] = row.xpath('./td[2]/span[1]/text()')[0].extract()
                self.item["won"] = row.xpath('./td[5]/text()')[0].extract()
                self.item["lost"] = row.xpath('./td[7]/text()')[0].extract()
                self.item["drawn"] = row.xpath('./td[6]/text()')[0].extract()
                self.item["goal"] = row.xpath('./td[8]/text()')[0].extract()
                self.item["goal_against"] = row.xpath('./td[9]/text()')[0].extract()
                self.item["points"] = row.xpath('./td[11]/text()')[0].extract()
                yield self.item
            
        self.browser.quit()

