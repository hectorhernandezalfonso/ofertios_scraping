import re
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import date

# Initialize the WebDriver
driver = webdriver.Firefox()

# Load the webpage
driver.get('https://www.alkosto.com/computadores-tablet/c/BI_COMP_ALKOS')


def extract_digits(text):
    return re.sub(r'\D', '', text)


def wait_for_button():
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Mostrar más productos')]")))


data = []  # List to store product data

for _ in range(15):
    load_more_button = wait_for_button()
    driver.execute_script("arguments[0].click();", load_more_button)
    time.sleep(5)  # Wait for 5 seconds before attempting to click again

# Find all <li> elements
li_elements = driver.find_elements(By.CSS_SELECTOR, "li.ais-InfiniteHits-item.product__item.js-product-item.js-algolia-product-click")

# Iterate through each <li> element
for li_element in li_elements:
    # Extract information from the <h3> tag
    h3_element = li_element.find_element(By.CSS_SELECTOR, "h3.product__item__top__title.js-algolia-product-click.js-algolia-product-title")
    product_title = h3_element.text

    # Initialize discount_price to None
    discount_price = None

    # Find the price elements
    try:
        original_price_element = li_element.find_element(By.CSS_SELECTOR, "p.product__price--discounts__old")
        original_price = re.sub(r'\D', '', original_price_element.text)  # Remove non-digits
    except NoSuchElementException:
        original_price = None

    try:
        discount_price_element = li_element.find_element(By.CSS_SELECTOR, "p.product__price--discounts__price")
        discount_price = discount_price_element.text
        discount_price_numeric = extract_digits(discount_price)
    except NoSuchElementException:
        discount_price = None

    # Construct product data dictionary
    product_data = {
        "Nombre": product_title,
        "Precio original": original_price,
        "Precio descuento": discount_price_numeric,
        "Almacen": "Alkosto",
        "Fecha": str(date.today())  # Convert date object to string
    }

    # Append product data to the list
    data.append(product_data)

# Convert list of dictionaries to JSON
json_data = json.dumps(data, indent=4)

# Print or save the JSON data
print(json_data)

# Save JSON data to a file
with open('alkosto_productos.json', 'w') as json_file:
    json_file.write(json_data)

driver.quit()
