
'''
Problem statement:
https://www.w3resource.com/python-exercises/web-scraping/index.php
2. Write a Python program to download and display the content of robot.txt for en.wikipedia.org.

Solution is made generic to any site and any URL
'''

import argparse
import requests
from bs4 import BeautifulSoup

def parse_command_line():

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', required=True, help="IP or FQDN, for example,"
                                                           "http://en.wikipedia.org)")
    parser.add_argument('-u', '--url', required=True, help="URL path (after trailing '/', for example,"
                                                           " robots.txt)")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_command_line()
    url = "https://" + args.domain + "/" + args.url

    r = requests.get(url)
    text = r.content
    soup = BeautifulSoup(text)
    print(soup.prettify())
