import requests
import json
import csv
import time
from mantas_z_mod1_atsiskaitymas.gintarine_crawler import crawl_gintarine
from mantas_z_mod1_atsiskaitymas.benu_crawler import crawl_benu

def crawl(source: str, time_limit: int = 60, data_format: str = "json"):
    """
    Function read website date and returns it in desired formats.

    :param source: Takes websites URL from which read data.
    :param time_limit: Time limit in seconds. After the certain time function stops working.
    :param data_format: Data return format. Can be json, csv, dict.
    :return: Data is formated in desired format.
    """
    start_time = time.time()

    if "gintarine" in source:
        data = crawl_gintarine()
    elif "benu" in source:
        data = crawl_benu()
    else:
        raise ValueError("Neturime prieigos prie šios svetainės.")

    if time.time() - start_time > time_limit:
        raise TimeoutError("Funkcijos veikimo laikas baigėsi.")

    if data_format == "json":
        return json.dumps(data, indent=4, ensure_ascii=False)
    elif data_format == "csv":
        with open("data_csv.csv", "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Title", "Price"])
            writer.writeheader()
            writer.writerows(data)
        return "CSV failas 'data_csv.csv' sukurtas sėkmingai"
    elif data_format == "list":
        return data
    else:
        raise ValueError("Toks formatamas yra nepalaikomas.")






