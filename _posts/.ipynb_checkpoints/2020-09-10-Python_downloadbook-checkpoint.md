---
title: 使用Python编写脚本抓取小说
date: 2020-09-09 21:29:20
tags: [Python]
---

使用Python脚本抓取小说, 算是第一个成功的程序吧

```
#!/usr/bin/env python
# coding: utf-8

import requests
import re
import time
from bs4 import BeautifulSoup

url = "http://www.biquge.info/22_22197/"
ua = {"User-Agent":"Mozilla/5.0"}
response = requests.get(url, headers=ua)
response.encoding = "utf-8"
html = response.text

soup = BeautifulSoup(html, 'lxml')
title = soup.find('meta', property="og:title").get('content')
#print (title)
fb=open('%s.txt'% title, 'w', encoding='utf-8')

soup_list = soup.select('#list > dl:nth-child(1) > dd > a')
#print (soup_list)

for chapter_info in soup_list:
    try:
        chapter_url = url+"%s" % chapter_info.get('href')
        #print (chapter_url)
        chapter_title = chapter_info.get('title')
        chapter_res = requests.get(chapter_url, headers=ua)
        chapter_res.encoding = "utf-8"
        chapter_html = chapter_res.text
        #print (chapter_html)
        soup_con = BeautifulSoup(chapter_html, 'lxml')
        div = soup_con.find(id='content')
        #print (div)
        chapter_content = div.get_text()
        #print (chapter_content)
        fb.write(chapter_title)
        fb.write('\n')
        fb.write(chapter_content)
        fb.write('\n')
        print (chapter_title, chapter_url)
        time.sleep(3)
    except Exception as err:
        print (chapter_title + "error")
fb.close()

```