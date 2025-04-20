# virgio_spider.py
import scrapy
from scrapy.selector import Selector
import time

class VirgioProductLinkSpider(scrapy.Spider):
    name = 'virgio_product_link_spider'
    start_urls = ['https://www.virgio.com/collections/the-party-edit']

    def parse(self, response):
        # Look for main navigation links - let's refine this based on Virgio's structure
        main_nav_links = response.css('nav a::attr(href)').getall()
        for link in main_nav_links:
            absolute_link = response.urljoin(link)
            # Adjust these conditions based on how Virgio organizes categories
            if '/collections/' in absolute_link or '/products/' in absolute_link:
                yield scrapy.Request(absolute_link, callback=self.parse_category_or_product)

        # Also check for category links in other prominent sections of the homepage
        homepage_category_links = response.css('a::attr(href)').getall() # Broader selector
        for link in homepage_category_links:
            absolute_link = response.urljoin(link)
            if '/collections/' in absolute_link or '/products/' in absolute_link:
                yield scrapy.Request(absolute_link, callback=self.parse_category_or_product)

    def parse_category_or_product(self, response):
        # Check if it's a product page based on the URL structure
        if '/products/' in response.url:
            yield {'product_url': response.url}
        else:
            # If it's a category page, look for product links using the HTML structure you provided
            product_links = response.css('a.w-1/2.md\:w-1/4.lg\:px-3.px-0\.5::attr(href)').getall()
            seen_links = set()
            for link in product_links:
                absolute_link = response.urljoin(link).strip()
                if absolute_link not in seen_links:
                    yield {'product_url': absolute_link}
                    seen_links.add(absolute_link)

            # Find and follow pagination links - adjust the selector if needed
            next_page_link = response.css('ul.pagination a[rel="next"]::attr(href)').get()
            if next_page_link:
                yield scrapy.Request(response.urljoin(next_page_link), callback=self.parse_category_or_product)

# Ensure your settings.py file is in the correct location and has the necessary configurations.