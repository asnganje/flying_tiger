# 🕷️ E-Commerce Web Scraper

A Python web scraper built with **Scrapy and Playwright** for extracting product data from JavaScript-driven e-commerce websites.

## 🚀 Features

* Scrapes dynamically rendered products
* Handles JavaScript-based pagination
* Uses CSS selectors for data extraction
* Exports products to **Excel**
* Supports **Google Sheets** export
* Automatically adds product serial numbers
* Formats Excel headers

## 🛠️ Tech Stack

* Python
* Scrapy
* Playwright
* OpenPyXL
* Google Sheets API
* uv

## 📊 Live Output

View the scraped product data in Google Sheets:

👉 [View Scraped Products](https://docs.google.com/spreadsheets/d/1kBAOs9LYdHMDFP-bl-HAUwS6BBEo_n4okoYROIpPoMc/edit?usp=drive_link)

## ▶️ Run

Install dependencies:

```bash
uv sync
```

Install Playwright browsers:

```bash
uv run playwright install
```

Run the spider:

```bash
uv run scrapy crawl ftigerspider
```

## ⚠️ Responsible Scraping

Respect the target website's Terms of Service, `robots.txt`, and applicable rate limits when using this tool.
