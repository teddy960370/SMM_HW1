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


def html2Json(url : str):
    resp = requests.get(
        url = url,
        cookies = {'over18': '1'},
        verify = True,
        timeout = 3
    )
    
    if resp.status_code == requests.codes.ok:
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        main_content = soup.find(id='main-content')
        base_info = main_content.find_all('div',class_=['article-metaline','article-metaline-right'])
        
        # 文章基本資訊
        author = ''
        title = ''
        date = ''
        
        if base_info:
            author = base_info[0].select('span.article-meta-value')[0].string if base_info[0].select('span.article-meta-value')[0] else author
            title = base_info[2].select('span.article-meta-value')[0].string if base_info[2].select('span.article-meta-value')[0] else title
            date = base_info[3].select('span.article-meta-value')[0].string if base_info[3].select('span.article-meta-value')[0] else date
        
        for info in base_info:
            info.extract()
        
        # 記錄推文，並從主文移除
        pushes = main_content.find_all('div', class_='push')
        for push in pushes:
            push.extract()
    
        # 移除foot資料
        foots = main_content.find_all('span', class_='f2')
        for foot in foots:
            foot.extract()
        
        # 儲存主文章內容
        content = main_content.text.replace('\n', ' ')
        
        return {'author' : author , 'title' : title , 'date' : date , 'content' : content}
    
        # Related Work
        # 1. 時間日期轉換
        # 2. 作者僅保留ID，暱稱移除(因暱稱可替換)
        # 3. 主文移除簽名檔
        # 4. 主文移除防雷內容
        # 5. 標題[好雷]、[負雷]辨識，可當作預測基準
        # 6. 辨識文章主要探討的電影正式名稱

def pttCrawler(broadName : str , keywords : str):
    
    articleList = list()
    
    maxPage = 6
    for page in range(1,maxPage):
        resp = requests.get(
            url = f"https://www.ptt.cc/bbs/{broadName}/search?page="+ str(page) + f"&q={keywords}",
            cookies = {'over18': '1'},
            verify = True,
            timeout = 3
        )
    
        soup = BeautifulSoup(resp.text, 'html.parser')
        divs = soup.find_all("div", class_="r-ent")
        for div in divs:
            href = div.find('a')['href']
            link = 'https://www.ptt.cc' + href
            #article_id = re.sub('\.html', '', href.split('/')[-1])
            articleList.append(html2Json(link))
            
    jsonString = json.dumps(articleList, indent=4, ensure_ascii=False)
    jsonFile = open("data.json", "w", encoding="utf-8")
    jsonFile.write(jsonString)
    jsonFile.close()


def main():
    broadName = 'MOVIE'
    keywords = '心得'
    pttCrawler(broadName,keywords)



if __name__ == "__main__":
    main()