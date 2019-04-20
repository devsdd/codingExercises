
'''
Problem statement:
https://www.w3resource.com/python-exercises/web-scraping/index.php
3. Write a Python program to get the number of datasets currently listed on data.gov.
'''

import requests
from bs4 import BeautifulSoup


r = requests.get("https://www.data.gov/")
rawWebPage = r.content

soup = BeautifulSoup(rawWebPage, "html.parser")
link = soup.find('a', {'href': '/metrics'})
print(link.text)