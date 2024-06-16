from datetime import datetime
import pandas as pd
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import urllib.parse
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from models.new_product import NewProduct

load_dotenv()
BASE_URL = "https://www.staples.ca"
API_KEY = os.getenv("PROXY_API_KEY")

# Proxy
def get_proxy_url(url):
    payload = {"api_key": API_KEY, "url": url}
    query_string = urllib.parse.urlencode(payload)
    proxy_url = f"https://proxy.scrapeops.io/v1/?{query_string}"
    return proxy_url

page_url = f"{BASE_URL}/collections/cleaning-wipes-liquids-sprays-9326?configure%5Bfilters%5D=tags%3A%22en_CA%22&configure%5BruleContexts%5D%5B0%5D=logged-out&page=2&sortBy=shopify_products"

def fetch_product_data(product_url, ua):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            permissions=["geolocation"],
            storage_state=None,
            user_agent=ua,
        )
        product_page = context.new_page()            
        product_page.goto(get_proxy_url(product_url))
        product_page.screenshot(path=f"{product_url}.png")
        time.sleep(1)

        try:
            product_page.click('button:has-text("Cancel")', timeout=500)
        except Exception as _:
            pass

        product_data = NewProduct()
        try:
            rating_point_element = product_page.query_selector('.product-information__link__reviews')
            rating_point = len(rating_point_element.query_selector_all(".icon.icon--star-filled")) + (0.5 if rating_point_element.query_selector(".icon.icon--star-filled-half") else 0)
        except Exception as e:
            rating_point = "0"

        try:
            rating_count_element = product_page.query_selector('.product-information__link__reviews')
            rating_count = rating_count_element.query_selector_all("span")[-1].text_content() if rating_count_element else "0"
        except Exception as e:
            rating_count = "0"

        try:
            stock_string = product_page.query_selector(".product-bopis-accordion__content.product-bopis-accordion__content--open > p").text_content()
            match = re.search(r'\b\d+\b', stock_string)
            stock_number = int(match.group())
            stock_level = "In stock" if stock_number > 0 else "Out of stock"
        except Exception as e:
            stock_level = "Out of stock"

        product_data.product_link = product_url
        product_data.product_name = product_page.query_selector('h1.product-title').query_selector(":scope > *").text_content().strip() if product_page.query_selector('h1.product-title') else None
        product_data.brand = product_page.query_selector('div.product-tile__brand-name').text_content().strip() if product_page.query_selector('div.product-tile__brand-name') else None
        product_data.category = product_page.query_selector(".breadcrumbs__list").text_content() if product_page.query_selector(".breadcrumbs__list") else None
        product_data.regular_price = product_page.query_selector('.mini-commerce-summary__price.money.pre-money').text_content().strip() if product_page.query_selector('.mini-commerce-summary__price.money.pre-money') else None
        product_data.discounted_price = product_page.query_selector('span.product-tile__sale-price').text_content().strip() if product_page.query_selector('span.product-tile__sale-price') else None
        product_data.size = None
        product_data.color = None
        product_data.flavor = None
        product_data.weight = None
        product_data.description = product_page.query_selector(".product-details__content").text_content() if product_page.query_selector(".product-details__content") else None
        product_data.average_rating = rating_point
        product_data.num_reviews = rating_count
        product_data.image_link = [item.get_attribute("src") for item in product_page.query_selector_all('.thumbnail-slider__thumb.thumbnail-slider__image')]
        product_data.sku = product_page.query_selector('.product-property').inner_text().split("Model")[0].replace("Item: ", "") if product_page.query_selector(".product-property") else None
        product_data.upc = None
        product_data.mfr_number = product_page.query_selector('.product-property').inner_text().split("Model:")[1] if product_page.query_selector(".product-property") else None
        product_data.stock_level = stock_level
        product_data.sold_by_3rd_party = 0
        product_data.shipped_by = None
        product_data.data_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        product_data.data_year_month = datetime.now().strftime('%Y-%m')
        product_data.retailer_code = None

        product_page.close()
        browser.close()
        return product_data

def collect_data(page_url=page_url, max_items=10):
    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/69.0.3497.100 Safari/537.36"
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            permissions=["geolocation"],
            storage_state=None,
            user_agent=ua,
        )
        page = context.new_page()
        page.goto(get_proxy_url(page_url))

        time.sleep(3)
        page.screenshot(path="main.png")

        try:
            page.click('button:has-text("Cancel")', timeout=500)
        except Exception as _:
            pass

        # Get current timestamp
        data_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_year_month = datetime.now().strftime('%Y-%m')

        # Define a list to store product information
        products = []

        # Get product URLs on the page
        product_elements = page.query_selector_all('.product-thumbnail__title.product-link')
        product_urls = [BASE_URL + product_element.get_attribute('href') for product_element in product_elements[:max_items]]

        browser.close()

        # Use ThreadPoolExecutor to fetch product data concurrently
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(fetch_product_data, url, ua) for url in product_urls]
            for future in as_completed(futures):
                try:
                    product_data = future.result()
                    products.append(product_data)
                    print(f"Products crawled: {len(products)}")
                except Exception as e:
                    print(f"Error fetching product data: {e}")

        # Define the order of headers
        headers = [
            'PRODUCT_LINK', 'PRODUCT_NAME', 'BRAND', 'CATEGORY', 'REGULAR_PRICE', 'DISCOUNTED_PRICE', 
            'SIZE', 'COLOR', 'FLAVOR', 'WEIGHT', 'DESCRIPTION', 'AVERAGE_RATING', 'NUM_REVIEWS', 
            'IMAGE_LINK', 'SKU', 'UPC', 'MFR_NUMBER', 'STOCK_LEVEL', 'SOLD_BY_3RD_PARTY', 
            'SHIPPED_BY', 'DATA_TIMESTAMP', 'DATA_YEAR_MONTH', 'RETAILER_CODE'
        ]

        # Convert to DataFrame and save to CSV
        df = pd.DataFrame([vars(product) for product in products], columns=headers)
        csv_file_path = "output/staplesca.csv"
        df.to_csv(csv_file_path, index=False)

        print(f"Data successfully saved to '{csv_file_path}'.")

        return products

if __name__ == "__main__":
    collect_data()
