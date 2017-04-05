import requests
import re
from bs4 import BeautifulSoup

bxwx_url = 'http://www.bxwx9.org/bsort/0/1.htm'
novel = requests.get(bxwx_url)
novel.encoding = 'gb2312'
novel_html = novel.text

soup = BeautifulSoup(novel_html, 'html.parser')
title = soup.select('.odd a')  #获取小说链接
for con in title:
    href = con['href']
    href = href.replace('binfo','b')
    href = href.replace('.htm','/index.html')  #处理链接变成小说阅读页链接
    novel_one = requests.get(href)  #获取小说章节
    href_id = href.split('/')
    novel_one.encoding = 'gb2312'

    novel_soup = BeautifulSoup(novel_one.text,'html.parser')
    chapter = novel_soup.select('#TabCss dl dd')
    new_chapter = {}
    new_chapter[href_id[5]] = {}
    for cha in chapter:
        if cha.find('a') != None:
            cha_href = cha.select_one('a')['href'].rstrip('.html')
            new_chapter[href_id[5]][cha_href] = cha

    items = new_chapter[href_id[5]].items()
    cha_list = sorted(items, key=lambda d: d[0])  #章节排序
    cha_title = novel_soup.select_one('#title').text.rstrip(' 全集下载')  #标题
    cha_info = novel_soup.select_one('#info a').text  #作者

    path = str(cha_title).strip()  #去掉空格
    fp = open("D:\mzitu\\"+path + ".txt", 'w+', encoding='utf-8')

    for key,value in cha_list:
        list_href = value.select_one('a')['href']
        list_href = href.replace('index.html',list_href)
        list_content = requests.get(list_href)
        list_content.encoding = 'gb2312'
        list_soup = BeautifulSoup(list_content.text,'html.parser')
        contents = list_soup.select_one('#content')
        l_title = '没有'
        if list_soup.select_one('#title'):
            l_title = list_soup.select_one('#title').text  #标题
        fp.writelines(l_title+'\n')
        l_contents = contents.get_text().lstrip('天才壹秒��住『笔下文学 』，�槟�提供精彩小�f���x。')  #内容
        fp.writelines(l_contents + '\n')

    fp.close()
    #print(fp)
    #print(href)
    #print(cha_list)


