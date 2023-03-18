# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 21:04:39 2023

@author: ted
"""

from bs4 import BeautifulSoup
import time
import requests
import json
import re
import codecs
from six import u
import pandas as pd


def pttCrawler(broadName : str , keywords : str):
    for page in range(1,6):
        resp = requests.get(
            url = f"https://www.ptt.cc/bbs/{broadName}/search?page="+ str(page) + f"&q={keywords}",
            cookies = {'over18': '1'},
            verify = True,
            timeout = 3
        )
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    divs = soup.find_all("div", "r-ent")      
    for div in divs:      
      href = div.find('a')['href']
      link = 'https://www.ptt.cc' + href
      article_id = re.sub('\.html', '', href.split('/')[-1])
      #parse_article(link, article_id, dataset)


def main():
    pttCrawler("MOVIE","天能")



if __name__ == "__main__":
    main()