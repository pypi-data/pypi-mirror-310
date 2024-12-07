import csv
import threading
from requests import get
from lxml.html import fromstring

def crawl_website(url, output_format, data_container):
    try:
        response = get(url)
        html_content = response.text
        tree = fromstring(html_content)

        products = tree.xpath("//div[contains(@class, 'product-item')]")
        data = []

        for product in products:
            product_name = product.xpath(".//input[@name='productName']/@value")[0]
            product_price = product.xpath(".//input[@name='productPrice']/@value")[0]
            product_brand = product.xpath(".//input[@name='productBrand']/@value")[0]

            product_data = {
                "product_name": product_name,
                "product_price": product_price,
                "product_brand": product_brand
            }
            data.append(product_data)

            print(f"Product Name: {product_name}")
            print(f"Product Price: {product_price}")
            print(f"Product Brand: {product_brand}")

        data_container['data'] = data

        if output_format == "csv":
            save_to_csv(data)
        elif output_format == "dict":
            return data
        else:
            raise ValueError("Unsupported output format. Use 'csv' or 'dict'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def save_to_csv(data, filename="products.csv"):
    if data:
        keys = data[0].keys()
        with open(filename, mode='w',encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data has been saved to {filename}")
    else:
        print("No data to save.")

def web_crawler(url="https://www.gintarine.lt/maistas-ir-papildai-sportininkams", timeout=60, output_format="csv"):
    data_container = {}

    crawl_thread = threading.Thread(target=crawl_website, args=(url, output_format, data_container))
    crawl_thread.start()

    crawl_thread.join(timeout)

    if crawl_thread.is_alive():
        print(f"The web crawling process took too long and was terminated after {timeout} seconds.")
        crawl_thread.join()
    else:
        print("Web crawling completed successfully.")

    if 'data' in data_container:
        return data_container['data']
