import os
import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv

def scrape(type):
    if type == "natural":
        url = "https://www.brilliantearth.com/diamond/shop-all/"
    elif type == "lab":
        url = "https://www.brilliantearth.com/lab-diamonds-search/"
    else:
        print(f"Invalid type: {type}.")
        print("Type must be natural or lab.")
        return False

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    print("-----BrilliantEarth Scraper-----")
    print("Here are the steps to scrape website successfully:")
    print("1. Choose filters in Chrome.")
    print("2. IMPORTANT - Scroll down in the table of all diamonds until no more diamonds load.")
    input("3. Press Enter in the Terminal here.")

    print("Scraping Website...")

    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')

    div_element = soup.find('div', {'id': 'diamonds_search_table', 'class': 'search-table'})

    if div_element:
        inner_html = div_element.decode_contents()
        with open(f"raw_{type}.txt", "w", encoding="utf-8") as file:
            file.write(inner_html)

        print(f"HTML content has been saved to raw_{type}.txt")
    else:
        print("Element not found.")

    driver.quit()

def extract_data_from_div(div):
    price_element = div.find('td', class_='price')
    carat_element = div.find('td', class_='carat')
    cut_element = div.find('td', class_='cut')
    color_element = div.find('td', class_='color')
    clarity_element = div.find('td', class_='clarity')

    if None in (price_element, carat_element, cut_element, color_element, clarity_element):
        return None

    price = price_element.text.strip()
    carat = carat_element.text.strip()
    cut = cut_element.text.strip()
    color = color_element.text.strip()
    clarity = clarity_element.text.strip()

    price = int(price.replace('$', '').replace(',', ''))

    carat = float(carat)

    price_per_carat = int(price / carat)

    return [price, carat, cut, color, clarity, price_per_carat]

def extract_to_csv(type):
    with open(f'raw_{type}.txt', 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    data = []

    divs = soup.find_all('div', class_='inner item')

    for div in divs:
        extracted_data = extract_data_from_div(div)
        if extracted_data:
            data.append(extracted_data)

    csv_file_name = f'{type}_data.csv'

    with open(csv_file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(['Price ($)', 'Carat', 'Cut', 'Color', 'Clarity', 'Price/Ct'])

        csv_writer.writerows(data)

    print(f'Data has been extracted and saved to {csv_file_name}.')

def main():
    
    print("#####################################")
    print("########Initializing Scraping########")
    print("#####################################")
    scrape("natural")
    scrape("lab")
    print("#####################################")
    print("#########Scraping Completed##########")
    print("#####################################")

    print("#####################################")
    print("##########Extracting To CSV##########")
    print("#####################################")

    extract_to_csv("natural")
    extract_to_csv("lab")

    print("#####################################")
    print("########Extraction Completed#########")
    print("#####################################")

if __name__ == "__main__":
    main()