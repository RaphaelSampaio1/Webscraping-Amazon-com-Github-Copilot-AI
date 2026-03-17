import time
import random
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from openpyxl import Workbook

def scrape_amazon_products(product, pages):
    # Set up Chrome options - removed headless to see automation
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Commented out to show browser
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")  # Maximize window

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load Amazon homepage
        driver.get("https://www.amazon.es/")
        time.sleep(random.uniform(2, 5))  # Random delay

        # Find search box and enter product
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_box.clear()
        search_box.send_keys(product)

        # Submit search
        search_box.submit()
        time.sleep(random.uniform(2, 5))

        all_products = []

        for page in range(pages):
            print(f"Processing page {page + 1}...")
            # Parse current page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            products = soup.find_all('div', {'data-component-type': 's-search-result'})

            print(f"Found {len(products)} product elements on page {page + 1}")

            for product_div in products:
                # Skip sponsored products if possible
                if product_div.find('span', string='Sponsored'):
                    continue

                # Extract title
                title_elem = product_div.find('h2').find('span') if product_div.find('h2') else None
                title = title_elem.text.strip() if title_elem else "N/A"

                # Extract price
                price_whole = product_div.find('span', class_='a-price-whole')
                price_fraction = product_div.find('span', class_='a-price-fraction')
                price = ""
                if price_whole:
                    price += price_whole.text
                if price_fraction:
                    price += price_fraction.text
                if not price:
                    price = "N/A"

                # Extract image URL
                img_elem = product_div.find('img')
                image_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else "N/A"

                # Extract product URL
                link_elem = product_div.find('a', class_='a-link-normal')
                product_url = "https://www.amazon.es" + link_elem['href'] if link_elem and 'href' in link_elem.attrs else "N/A"

                all_products.append({
                    'Description': title,
                    'Price': price,
                    'Image Link': image_url,
                    'Product Link': product_url
                })

            print(f"Extracted {len(all_products)} products so far")

            # Find and click next page if not last page
            if page < pages - 1:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, "Next"))
                    )
                    print("Clicking next page...")
                    next_button.click()
                    # Wait for the next page to load
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
                    )
                    time.sleep(random.uniform(3, 7))  # Longer delay for next page
                except:
                    print(f"No more pages after page {page + 1}")
                    break

        # Save to XLSX
        wb = Workbook()
        ws = wb.active
        ws.title = "Amazon Products"
        ws.append(['Description', 'Price', 'Image Link', 'Product Link'])

        for prod in all_products:
            ws.append([prod['Description'], prod['Price'], prod['Image Link'], prod['Product Link']])

        wb.save(f"{product.replace(' ', '_')}_products.xlsx")
        print(f"Data saved to {product.replace(' ', '_')}_products.xlsx")

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        product = sys.argv[1]
        pages = int(sys.argv[2])
    else:
        product = input("Enter the product to search: ")
        pages = int(input("Enter the number of pages to scrape: "))
    scrape_amazon_products(product, pages)