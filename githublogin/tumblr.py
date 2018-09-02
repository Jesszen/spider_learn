from lxml import etree
import requests
import re
from urllib.parse import urlencode
from urllib.request import urlopen
import re
import os
class tumblr():
    def __init__(self):
        self.heads={
            'Referer': 'https://www.tumblr.com/dashboard',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 YaBrowser/18.6.1.770 Yowser/2.5 Safari/537.36',
            'cookie': 'rxx=1tja6pe1nzl.12k4a0ca&v=1; _ga=GA1.2.1287882306.1522321439; yx=o8dqqh9qo4w2b%26o%3D3%26f%3D9a; devicePixelRatio=1.1666666269302368; _gid=GA1.2.2095539574.1532419180; __utmc=189990958; nts=false; __utma=189990958.1287882306.1522321439.1532419180.1532420938.3; __utmb=189990958.0.10.1532420938; __utmz=189990958.1532420938.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; capture=cS5uDcSIP98HVVY6PWOTPGQNrfg; pfp=47QVk5NQq3yot71uFTx15Bx3UOVbSDmwm1dNf7N7; pfs=GBjBzrmzgIiKuhE77m0pV7oKk; pfe=1540197281; pfu=61441918; pfx=4a43a6d221d364d90fd7dd45fe5f0e8f49ba3adce1d488225cd532a2f4935301%230%237254450764; language=%2Cen_US; logged_in=1; documentWidth=1008; pfg=6ac541dc7e626c8cd546ec5f83724f5357f19565bea630fdae9df2b8a1ea56b7%23%7B%22gdpr_is_acceptable_age%22%3A1%2C%22exp%22%3A1563958449%2C%22vc%22%3A%22%22%7D%231213040843; tmgioct=5b56e9312749190373428960'
           }
        self.posturl='https://github.com/session'
        self.session=requests.Session()
    def ping(self):
        k=self.session.get(headers=self.heads,url='https://www.tumblr.com/dashboard')

    def down(self,page):
        k=self.session.get(headers=self.heads,url=page)
        sele=etree.HTML(k.text)
        imgurl=sele.xpath('//img[@class="post_media_photo image"]/@src')
        print(imgurl)
        path='g:/tumbler'
        if not os.path.exists(path):
            os.makedirs(path)
        for url in imgurl:
            imgname=url.split('/')[-1]
            img111=requests.get(url)
            with open('g:/tumbler/%s'%imgname,'wb')as f:
                f.write(img111.content)

    def down2(self,page):
        k=self.session.get(headers=self.heads,url=page)
        sele=etree.HTML(k.text)
        imgurl=sele.xpath('//div[@class="photoset_row photoset_row_1"]/a/@href')
        print(imgurl)
        path='g:/tumbler/xu'
        if not os.path.exists(path):
            os.makedirs(path)
        for url in imgurl:
            imgname=url.split('/')[-1]
            img111=requests.get(url)
            with open('g:/tumbler/xu/%s'%imgname,'wb')as f:
                f.write(img111.content)
m=range(401,434)
z=range(120,800)

for i in m:
   basicurl='https://www.tumblr.com/likes/page/%s'%(i)
   print(basicurl)
   t=tumblr()
   t.down(basicurl)
"""
for i in z:
   basicurl='https://www.tumblr.com/likes/page/%s'%(i)
   print(basicurl)
   t=tumblr()
   t.down2(basicurl)
"""