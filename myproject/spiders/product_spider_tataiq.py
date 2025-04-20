import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
import time

class ProductLinkSpiderSelenium(scrapy.Spider):
    name = 'product_link_spider_selenium'
    start_urls = ['https://www.tatacliq.com/shirts/c-msh1117100?&icid2=regu:nav:main:mnav:m1117100:mulb:best:10:R3']  # Use a category page

    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def close(self, spider):
        self.driver.quit()

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)
        html = self.driver.page_source
        selector = Selector(text=html)

        product_links = selector.css('div.Grid__element div.PlpComponent__base div.ProductModule__base a.ProductModule__aTag::attr(href)').getall()

        for link in product_links:
            absolute_link = response.urljoin(link)
            print(f"Extracted product link: {absolute_link}")  # Print the extracted link
            if '/p-mp' in absolute_link:
                yield {'product_url': absolute_link} # For now, just output the URL

        next_page_link = selector.css('a[rel="next"]::attr(href)').get()
        if next_page_link:
            yield scrapy.Request(response.urljoin(next_page_link), callback=self.parse)

    def is_product_link(self, url):
        return '/p-mp' in url