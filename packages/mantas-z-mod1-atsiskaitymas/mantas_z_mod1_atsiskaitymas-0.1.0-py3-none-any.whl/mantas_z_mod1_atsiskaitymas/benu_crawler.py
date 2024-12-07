import requests
from lxml.etree import HTML

def crawl_benu():
    """
    Function reads data from benu website
    :param source: Websites URL
    :return: Data received - titles and prices
    """
    source = "https://www.benu.lt/menesio-top-pasiulymai?vars/gclid/CjwKCAiArva5BhBiEiwA-oTnXX6Umbk0M9UK8rG2G6UbnWgJeXX6HH_C4oWWtSg4vIZXSEvkmGTTPxoCZvgQAvD_BwE"
    response = requests.get(source)
    response.encoding = "utf-8"
    text = response.text
    tree = HTML(text)

    products = tree.xpath("//div[contains(@class, 'bnProductCard bnProductCard--listMobile productItem productItem__wrapCount')]")

    return [{
        "Title": product.xpath(".//h2[contains(@class, 'h3')]/text()")[0].strip(),
        "Price": product.xpath(".//span[contains(@class, 'money_amount')]/text()")[0].strip()
    } for product in products]

    #titles = tree.xpath("//h2[contains(@class, 'h3')]/text()")
    #prices = tree.xpath("//span[contains(@class, 'money_amount')]/text()")

print(crawl_benu())


