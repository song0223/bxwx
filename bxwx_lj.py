import requests
import threading
import os
from bs4 import BeautifulSoup
from time import sleep, ctime

bxwx_url = 'http://www.bxwx9.org/bsort/0/1.htm'
novel = requests.get(bxwx_url)
novel.encoding = 'gb2312'
novel_html = novel.text

soup = BeautifulSoup(novel_html, 'html.parser')
title = soup.select('.odd a')  #获取小说链接

def cj(con):
    href = con['href']
    x_id = href.split('/')[5].rstrip('.html')
    href = href.replace('www.bxwx9.org/binfo', 'txt.bxwxtxt.com/packdown/fulltxt')
    href = href.replace('htm', 'txt?14')  # 处理链接变成小说下载链接
    r = requests.get(href)
    path = 'D:\mbxwxs\\'
    if os.path.exists(path) == False:
        os.makedirs(path)

    os.chdir(path)  #切换到上面创建的文件夹
    r_title = con.text + '_' + x_id + '.txt'
    with open(r_title, "wb") as code:
        code.write(r.content)

threads = []
for con in title:
    t = threading.Thread(target=cj, args=(con,))
    threads.append(t)

if __name__ == '__main__':
    #启动线程
    for i in range(len(title)):
        threads[i].start()
    for i in range(len(title)):
        threads[i].join()

    #主线程
    print('采集完成:%s' %ctime())

