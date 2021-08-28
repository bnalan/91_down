#coding=utf-8
import requests
import os
import re
import time
import random
import signal
import threading
import requests.packages.urllib3
from bs4 import BeautifulSoup
#import js2py
from tqdm import tqdm
from urllib.parse import urlparse
from m3u8 import *

requests.packages.urllib3.disable_warnings()


s = requests.session()

class Resturant():
    def __init__(self, url, name,maxpage):
        self.geturl = url
        self.getname = name
        self.getmaxpage = maxpage
#s.keep_alive = False  # 关闭多余连接
#requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数

refererurl = 'http://91porn.com' # 请求头默认地址
proxies = {'http': 'http://127.0.0.1:10809', 'https': 'https://127.0.0.1:10809'} # 代理地址

down1 = Resturant("https://f1105.workarea3.live/v.php?category=tf&viewtype=basic&page=","[本月收藏]",100)
down2 = Resturant("https://f1105.workarea3.live/v.php?category=rf&viewtype=basic&page=","[最近加精]",100)
down3 = Resturant("https://f1105.workarea3.live/v.php?category=top&viewtype=basic&page=","[本月最热]",10)
down4 = Resturant("https://f1105.workarea3.live/v.php?category=hot&viewtype=basic&page=","[当前最热]",10)
down5 = Resturant("https://f1105.workarea3.live/v.php?category=top&m=-1&viewtype=basic&page=","[上月最热]",10)
down6 = Resturant("https://f1105.workarea3.live/v.php?category=md&viewtype=basic&page=","[最近讨论]",100)


dowms = [down5,down4,down3]

fatherpath1 = os.path.dirname(os.path.realpath(__file__))
fatherpath = os.path.join(fatherpath1, 'down')

# 定义随机ip地址
def random_ip():
    a = random.randint(1, 255)
    b = random.randint(1, 255)
    c = random.randint(1, 255)
    d = random.randint(1, 255)
    return (str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))

# 定义请求头
def random_header(url):
    headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'X-Forwarded-For': random_ip(),
            'Content-Type': 'multipart/form-data; session_language=cn_CN',
            'Connection': 'keep-live',
            'Upgrade-Insecure-Requests': '1',                   
            'Referer': url}
    return headers

# 下载除M3U8外的资源
def download_from_url(path,url, title):
    dst = os.path.join(path, title+'.mp4')
    response = s.get(url, headers=random_header(refererurl),proxies=proxies)  # (1)
    file_size = int(response.headers['content-length'])  # (2)
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)  # (3)
    else:
        first_byte = 0
    if first_byte >= file_size:  # (4)
        return file_size
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=dst)
    with(open(dst, 'ab')) as f:
        for chunk in response.iter_content(chunk_size=1024):  # (6)
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    print("----------------下载结束------------------")


# 下载m3u8的资源
def download_from_url_m3u8(path,url, title):
    M3u8Download(url,title,path)
    print("----------------下载结束------------------")


# 爬虫主体
def spider():
    #inputPage = 1
    #inputtitle = 1
    inputdown = 0
    page = 1

    while inputdown < len(dowms):
        while int(page) <= int(dowms[inputdown].getmaxpage):            
            try:
                page_url = dowms[inputdown].geturl + str(page)
                get_page = s.get(url=page_url, headers=random_header(refererurl),proxies=proxies)

                # 利用正则匹配出特征地址
                viewurl = []
                div = BeautifulSoup(get_page.text, "html.parser").find_all("div", class_="well well-sm videos-text-align")
                for i in div:
                    viewurl.append(i.a.attrs["href"])
                resetcount = 1
                index = 0
                while index < len(viewurl):
                    try:
                        url = ''
                        base_req = s.get(url=viewurl[index], headers=random_header(page_url), proxies=proxies)
                        a = re.compile('document.write\(strencode2\("(.*)"').findall(base_req.content.decode('utf-8'))   
                        if len(a) > 0:
                            text = eval(repr(a[0]).replace('%', '\\x'))
                            url = BeautifulSoup(text, "html.parser").source.attrs['src']
                        else:
                            if resetcount <= 10:
                                #print('读取数据空，重试中,重试数量' + str(resetcount))
                                time.sleep(5)
                                resetcount += 1
                                continue
                            elif resetcount >= 10:
                                print(dowms[inputdown].getname +'第'+str(page)+'页数据,共'+str(len(viewurl)) +'条帖子 =>>>> 正在下载第'+str(index+1)+'_读取数据空，重试结束')
                                index += 1
                                resetcount = 1
                                continue
                        res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]")
                        title = BeautifulSoup(base_req.text, "html.parser").title.text.replace(" ", "").replace("\n", "")
                        title = res.sub("", title).replace("Chinesehomemadevideo", "")
                        createtime = BeautifulSoup(base_req.text, "html.parser").find('span', class_="title-yakov").text.replace(" ", "").replace("\n", "").replace("\\", "").replace("/", "").replace('/"', "").replace("*", "")
                        author = BeautifulSoup(base_req.text, "html.parser").find('span', class_="title").text.replace(" ", "").replace("\n", "").replace("\\", "").replace("/", "").replace('/"', "").replace("*", "")
                        # name = createtime + "_" + title + "_" + author
                        name = title + "_" + author
                        videotype = urlparse(url).path.split(".")[1]
                        path = os.path.join(fatherpath, createtime +'_91pron_down')
                        if not os.path.exists(path):
                            os.makedirs(path)

                        dst = os.path.join(path, name+'.mp4')
                        if not os.path.exists(dst) :
                            print('#' * 100)
                            print( dowms[inputdown].getname +'第'+str(page)+'页数据,共'+str(len(viewurl)) +'条帖子 =>>>> 正在下载第'+str(index+1)+'个帖子_'+name)
                            if videotype == "m3u8":
                                download_from_url_m3u8(path,url, name)
                            else:
                                download_from_url(path,url, name)      
                            print('#' * 100 + '\n')
                    except Exception as e:
                        print("Get Value:" + str(e))
                        time.sleep(5)
                        continue
                    resetcount = 1
                    index += 1
                    time.sleep(3)
            except Exception as e:
                print("Get PageInfo:" + str(e))
                time.sleep(5)
                continue
            page += 1
        inputdown += 1
        page = 1
    print("任务完成")

if __name__ == '__main__':
    work_thread = threading.Thread(target=spider)
    work_thread.daemon = True
    work_thread.start()
    signal.signal(signal.SIGINT, quit)
    print("Start Working")
    while True:
        time.sleep(1)