#!/usr/bin/env python3

import time
import csv
import requests as req
from bs4 import BeautifulSoup as bs

def scrape(url):
    print(f"Attempting to scrape {url}")
    res = req.get(url)
    if res.status_code != 200:
        print(f"Failed to retrieve data from {url} : {res.status_code}")
        return []
    parse = bs(res.text, "html.parser")
    return [element.text.replace('\n', '') for element in parse.find_all('p')]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
urls = [
        "https://en.wikipedia.org/wiki/Dog_grooming",
        "https://en.wikipedia.org/wiki/Cat_behavior",
        "https://en.wikipedia.org/wiki/Appointment_scheduling_software",
]

artifacts = []
for url in urls:
    artifacts.append(scrape(url))
    time.sleep(2)

file_path = "data/dataset.csv"
with open(file_path, mode="w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Content"])
    for url, content in zip(urls, artifacts):
        writer.writerow([url, " ".join(content)])

print(f"Data written to {file_path}")
