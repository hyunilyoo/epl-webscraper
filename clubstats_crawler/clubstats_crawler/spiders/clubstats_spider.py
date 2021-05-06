import scrapy
import time
from selenium import webdriver
from scrapy.selector import Selector
from clubstats_crawler.items import ClubstatsCrawlerItem

class ClubSpider(scrapy.Spider):
    name = 'Clubstats'
    allowed_domains = ['premierleague.com']
    start_urls = ['https://www.premierleague.com/clubs']

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome('/Users/hyunilyoo/Documents/analytics/chromedriver')

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5)
        self.clubnames = []
        self.name = None
        self.season_club = None

        # Seasons for EPL
        self.html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        self.selector = Selector(text=self.html)
        self.season_epl = len(self.selector.xpath('//*[@id="mainContent"]/div[2]/div/section/div[1]/ul/li'))+1

        for i in range(1, self.season_epl):
            time.sleep(3)

            # Filter by Season
            self.browser.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div/section/div[1]/div[2]').click()
            time.sleep(3)
            # Seasons in the dropdown menu
            self.browser.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div/section/div[1]/ul/li'+str([i])).click()

            # Number of teams
            for j in range(1, 21):
                time.sleep(3)
                self.html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
                self.selector = Selector(text=self.html)
                self.name = self.selector.xpath('//*[@id="mainContent"]/div[2]/div/div/div[1]/div/ul/li'+str([j])+'/a/div[3]/div[2]/h4/text()')[0].extract()
                if self.name not in self.clubnames:
                    self.clubnames.append(self.name)

                    # Into Club
                    self.browser.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div/div/div[1]/div/ul/li'+str([j])+'/a/div[3]/div[3]/span').click()
                    time.sleep(3)

                    # navigate to stats
                    self.browser.find_element_by_xpath('//*[@id="mainContent"]/nav/ul/li[5]/a').click()
                    time.sleep(3)

                    self.html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
                    self.selector = Selector(text=self.html)
                    self.season_club = len(self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/section/div[1]/ul/li'))+1

                    # navigate to dropdown menu for seasons in the club
                    for k in range(2, self.season_club):
                        self.browser.find_element_by_xpath('//*[@id="mainContent"]/div[3]/div/div/section/div[1]/div[2]').click()
                        time.sleep(3)

                        if k < 10:
                            self.browser.find_element_by_xpath('//*[@id="mainContent"]/div[3]/div/div/section/div[1]/ul/li'+f'[{k}]').click()
                            time.sleep(5)

                        elif k >= 10 and k < 19:
                            self.browser.execute_script('window.scrollTo(0, 150)')
                            time.sleep(3)
                            self.browser.find_element_by_xpath('//*[@id="mainContent"]/div[3]/div/div/section/div[1]/ul/li'+f'[{k}]').click()
                            time.sleep(5)

                        else:
                            self.browser.execute_script('window.scrollTo(0, 330)')
                            time.sleep(3)
                            self.browser.find_element_by_xpath('//*[@id="mainContent"]/div[3]/div/div/section/div[1]/ul/li'+f'[{k}]').click()
                            time.sleep(5)

                        self.html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
                        self.selector = Selector(text=self.html)

                        self.item = ClubstatsCrawlerItem()
                        self.item["club_name"] = self.selector.xpath('//*[@id="mainContent"]/header/div[2]/div/div/div[2]/h1/text()')[0].extract()
                        self.item["goal_per_match"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[1]/div/div[3]/span/span/text()')[0].extract()
                        self.item["shot_on_target"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[1]/div/div[5]/span/span/text()')[0].extract()
                        self.item["shooting_accuracy"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[1]/div/div[6]/span/span/text()')[0].extract()
                        self.item["big_chance_created"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[1]/div/div[8]/span/span/text()')[0].extract()
                        self.item["pass_per_game"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[2]/div/div[3]/span/span/text()')[0].extract()
                        self.item["pass_accuracy"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[2]/div/div[4]/span/span/text()')[0].extract()
                        self.item["cross"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[2]/div/div[5]/span/span/text()')[0].extract()
                        self.item["cross_accuracy"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[2]/div/div[6]/span/span/text()')[0].extract()
                        self.item["goal_conceded_per_match"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[3]/div/div[4]/span/span/text()')[0].extract()
                        self.item["tackle_success"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[3]/div/div[7]/span/span/text()')[0].extract()
                        self.item["clearance"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[3]/div/div[10]/span/span/text()')[0].extract()
                        self.item["aerial_battles"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[3]/div/div[12]/span/span/text()')[0].extract()
                        self.item["interceptions"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/ul/li[3]/div/div[9]/span/span/text()')[0].extract()
                        self.item["season"] = self.selector.xpath('//*[@id="mainContent"]/div[3]/div/div/section/div[1]/div[2]/text()')[0].extract()
                        yield self.item

                    # Back to the request url
                    self.browser.get(response.url)

        self.browser.quit()

