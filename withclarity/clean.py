from bs4 import BeautifulSoup
import csv

def extract_diamond_info(html_content):
    diamond_info = []

    soup = BeautifulSoup(html_content, 'html.parser')

    diamond_body = soup.find('div', class_='diamond-body tab-content-container')

    if diamond_body:
        print("Found body")
        diamond_divs = diamond_body.find_all('div', class_='diamond-list no-pair-diamond')

        for div in diamond_divs:
            mobile_info = div.find('div', class_='medium-up--hide diamond-mobile-info')

            if mobile_info:

                data = mobile_info.get_text().split(" ")

                carat = float(data[0].replace("\n", ""))
                cut = data[4].replace("Diamond\n", "")
                color = data[6]
                clarity = data[8]

                price_data = data[9]
                last_index_price = price_data.rfind("$")
                number_index = last_index_price + 1

                while number_index < len(price_data) and (price_data[number_index].isdigit() or price_data[number_index] == ','):
                    number_index += 1

                price = price_data[last_index_price + 1:number_index]
                if price == "":
                    continue
                price = int(price.replace(",", ""))

                price_per_carat = int(price / carat)
                diamond_info.append([price, carat, cut, color, clarity, price_per_carat])

    return diamond_info

def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content

def extract_to_csv(type):

    file_path = f'raw_{type}.html'
    html_content = read_html_file(file_path)
    data = extract_diamond_info(html_content)

    csv_file_name = f'{type}_data.csv'

    with open(csv_file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(['Price ($)', 'Carat', 'Cut', 'Color', 'Clarity', 'Price/Ct'])

        csv_writer.writerows(data)

    print(f'Data has been extracted and saved to {csv_file_name}.')

extract_to_csv("natural")