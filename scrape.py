#!/usr/bin/env python3

import time
import csv
import re
import requests as req
from bs4 import BeautifulSoup as bs

csv.field_size_limit(10*1024*1024)

def scrape(url):
    print(f"Attempting to scrape {url}")
    res = req.get(url)
    if res.status_code != 200:
        print(f"Failed to retrieve data from {url} : {res.status_code}")
        return []
    parse = bs(res.text, "html.parser")
    return [re.sub(r"[^a-zA-Z0-9\s.,!?'\";:()\-]", '', element.text) for element in parse.find_all('p')]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
urls = [
        "https://en.wikipedia.org/wiki/Dog_grooming",
        "https://en.wikipedia.org/wiki/Cat_behavior",
        "https://en.wikipedia.org/wiki/Appointment_scheduling_software",
        "https://www.gutenberg.org/cache/epub/84/pg84-images.html",
        "https://www.gutenberg.org/cache/epub/1342/pg1342-images.html",
        "https://www.gutenberg.org/cache/epub/1513/pg1513-images.html",
        "https://www.gutenberg.org/cache/epub/2701/pg2701-images.html",
        "https://www.gutenberg.org/cache/epub/25344/pg25344-images.html",
]

artifacts = []
for url in urls:
    artifacts.append(scrape(url))
    time.sleep(2)

file_path = "data/dataset.csv"
with open(file_path, mode="w", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter="|")
    writer.writerow(["URL", "Content"])
    for url, content in zip(urls, artifacts):
        writer.writerow([url, " ".join(content)])

print(f"Data written to {file_path}")
