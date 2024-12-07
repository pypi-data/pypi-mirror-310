import requests
from lxml.etree import HTML

def crawl_gintarine():
    """
    Function reads data from eurovaistine website
    :param source: Websites URL
    :return: Data received - titles and prices
    """
    source = "https://www.gintarine.lt/arbatos"
    response = requests.get(source)
    text = response.text
    tree = HTML(text)

    products = tree.xpath("//div[contains(@class, 'product-item')]")

    return[{
        "Title": product.xpath(".//div[contains(@class, 'product__title')]/a/text()")[0].strip(),
        "Price": product.xpath(".//div[contains(@class, 'product__price')]/span[contains(@class, 'product__price--regular')]/text()")[0].strip()
    } for product in products]

print(crawl_gintarine())