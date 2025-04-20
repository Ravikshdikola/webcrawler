
# 🕷️ #Product Link Crawler using Scrapy

This repository contains custom **Scrapy-based web crawlers** designed to extract **product page URLs** from multiple e-commerce websites. Each spider is tailored to the site's HTML structure for efficient and accurate data collection.



project overview :
mycrawler/
├── spiders/
│   ├── product_spider_virgo.py
│   ├── product_spider_westside.py
│   ├── product_spider_tataiq.py
│   └── product_spider_nyaka.py
├── items.py
├── pipelines.py
├── settings.py




---

## 🧩 Spiders Overview

### `virgio_spider.py`
- **Target**: [Virgio.com](https://www.virgio.com/)
- **Highlights**:
  - Starts from the "Party Edit" collection
  - Extracts links to product and category pages
  - Handles pagination
  - Outputs unique product page URLs

### `westside_spider.py`
- **Target**: [Westside](https://www.westside.com/)
- **Highlights**:
  - Crawls through categories and subcategories
  - Extracts links to product pages

### `tataiq_spider.py`
- **Target**: Tata iQ product catalog (or a similar platform)
- **Highlights**:
  - Navigates category/product hierarchies
  - Handles nested product structures

### `nykaa_spider.py`
- **Target**: [Nykaa](https://www.nykaa.com/)
- **Highlights**:
  - Extracts product links from various beauty categories
  - Handles product variants and pagination

---

## 💾 Output Format

Each spider yields a JSON-like dictionary:
```json
{
  "product_url": "https://example.com/products/product-name"
}


## for running it :
syntax : scrapy  crawl  <name described in each webcrawler file  -o  <output file where you want to save output it should be in json format>
scrapy crawl virgio_product_link_spider -o virgio_links.json
