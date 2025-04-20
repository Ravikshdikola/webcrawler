# westside_spider.py
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

class WestsideProductLinkSpiderSelenium(scrapy.Spider):
    name = 'westside_product_link_spider_selenium'
    start_urls = ['https://www.westside.com/collections/duvet-covers-and-comforters']

    def __init__(self):
        # Initialize Selenium WebDriver
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def close(self, spider, reason):
        # Close the WebDriver when the spider finishes
        self.driver.quit()


    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)  # Allow time for JavaScript to render content

        # Get the page source after JavaScript execution
        html = self.driver.page_source
        response_selenium = scrapy.Selector(text=html)

        product_links = response_selenium.css('li.wizzy-result-product > a.wizzy-result-product-item::attr(href)').getall()

        if not product_links:
            self.logger.warning("Selenium did not find product links with the selector.")
        else:
            self.logger.info(f"Selenium found {len(product_links)} product links on {response.url}.")

        seen_links = set()
        for link in product_links:
            absolute_link = response.urljoin(link).strip()
            if absolute_link not in seen_links:
                self.logger.info(f"Found product link (via Selenium): {absolute_link}")
                yield {'product_url': absolute_link}
                seen_links.add(absolute_link)


   
        # After trying all common "next" button selectors, we move on

    # def parse(self, response):
    #     self.driver.get(response.url)
    #     time.sleep(5)  # Allow time for JavaScript to render content

    #     # Get the page source after JavaScript execution
    #     html = self.driver.page_source
    #     response_selenium = scrapy.Selector(text=html)

    #     product_links = response_selenium.css('li.wizzy-result-product > a.wizzy-result-product-item::attr(href)').getall()

    #     if not product_links:
    #         self.logger.warning("Selenium did not find product links with the selector.")
    #     else:
    #         self.logger.info(f"Selenium found {len(product_links)} product links.")

    #     seen_links = set()
    #     for link in product_links:
    #         absolute_link = response.urljoin(link).strip()
    #         if absolute_link not in seen_links:
    #             self.logger.info(f"Found product link (via Selenium): {absolute_link}")
    #             yield {'product_url': absolute_link}
    #             seen_links.add(absolute_link)

    #     # **Handling Pagination with Selenium**
    #     next_page_button_selector = 'ul.pagination li.next a'
    #     while True:
    #         try:
    #             next_button = self.driver.find_element(By.CSS_SELECTOR, next_page_button_selector)
    #             next_button.click()
    #             time.sleep(3)  # Allow time for the next page to load

    #             html = self.driver.page_source
    #             response_selenium = scrapy.Selector(text=html)
    #             new_product_links = response_selenium.css('li.wizzy-result-product > a.wizzy-result-product-item::attr(href)').getall()

    #             if not new_product_links:
    #                 self.logger.warning("Selenium did not find product links on the current page.")
    #             else:
    #                 self.logger.info(f"Selenium found {len(new_product_links)} product links on the next page.")

    #             for link in new_product_links:
    #                 absolute_link = response.urljoin(link).strip()
    #                 if absolute_link not in seen_links:
    #                     self.logger.info(f"Found product link (via Selenium - next page): {absolute_link}")
    #                     yield {'product_url': absolute_link}
    #                     seen_links.add(absolute_link)

    #         except Exception as e:
    #             self.logger.info("No more pagination links found or an error occurred during pagination.")
    #             self.logger.error(f"Pagination error: {e}")
    #             break

# settings.py
BOT_NAME = 'westside_scraper'
SPIDER_MODULES = ['westside_scraper.spiders']
NEWSPIDER_MODULE = 'westside_scraper.spiders'
ROBOTSTXT_OBEY = True
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
DOWNLOAD_DELAY = 3  # Increase download delay for Selenium

# ITEM_PIPELINES = {
#    'westside_scraper.pipelines.WestsideScraperPipeline': 300,
# }