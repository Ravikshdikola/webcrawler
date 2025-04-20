import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
import time

class NykaaProductLinkSpider(scrapy.Spider):
    name = 'nykaa_product_link_spider'
    start_urls = ['https://www.nykaa.com/makeup/face/face-concealer/c/234']

    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def close(self, spider):
        self.driver.quit()

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(10)  # Increased wait time

        html = self.driver.page_source
        selector = Selector(text=html)

        # Updated CSS selector based on the inspected HTML
        product_links = selector.css('a.css-qlopj4::attr(href)').getall()

        for link in product_links:
            absolute_link = response.urljoin(link)
            print(f"Extracted product link: {absolute_link}")
            yield {'product_url': absolute_link}

        next_page_link = selector.css('a[rel="next"]::attr(href)').get()
        if next_page_link:
            yield scrapy.Request(response.urljoin(next_page_link), callback=self.parse)

    def is_product_link(self, url):
        return '/p/' in url # Updated product link identifier for Nykaa