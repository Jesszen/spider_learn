from config import *
from mysql import mysql
from db import RedisQueue
from requestmy import weixinrequest
import requests
from urllib.parse import urlencode
from lxml import etree
import time
import re
from pyquery import PyQuery as pq

class spider(object):
    base_url='http://weixin.sogou.com/weixin'
    headers={
    'Accept': 'image / webp, image / apng, image / *, * / *;q = 0.8',
    'Accept - Encoding': 'gzip, deflate,UTF-8',
    'Accept - Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
    'Connection': 'keep - alive',
    'Host': 'pb.sogou.com',
    'Referer': 'http: // wx.sogou.com /',
    'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 YaBrowser/18.6.1.770 Yowser/2.5 Safari/537.36'
    }
    ruler=re.compile(r'var publish_time = "(\d+.\d+.\d+)')
    keywords='保加利亚妖王'
    session=requests.Session()
    queue=RedisQueue()
    mysql1=mysql()

    def get_proxy(self):
        """
        代理池的web接口获取代理
        :return:
        """
        try:
          response = requests.get(proxy_pool_web)
          if response.status_code == 200:
              print(response.text)
              return response.text
          return None
        except requests.ConnectionError:
            return None

    def start(self):
        """
        初始化
        :return:
        """
        self.session.headers.update(self.headers)
        start_url = self.base_url +'?'+ urlencode({'query':self.keywords,'type':2})#  不如直接formate
        weixin_request= weixinrequest(callback=self.parse_index,url=start_url,need_proxy=False)#构造第一个请求，以我们定义的类呈现
        self.queue.add(weixin_request)#加入队列

    def parse_index(self,response):
        response.encoding='utf-8'
        doc=etree.HTML(response.text)
        url_details=doc.xpath('//div[@class="txt-box"]/h3/a/@href')
        print('开始解析')
        print(url_details)
        #print(response.text)
        for i in url_details:
            #time.sleep(1)
            wei=weixinrequest(url=i,callback=self.parse_detail,need_proxy=True)
            print(wei.url)
            yield wei

        next_page=doc.xpath('//a[@id="sogou_next"]/@href')
        if next_page:
            time.sleep(2)
            url_nex=self.base_url + str(next_page[0])
            wei_nex=weixinrequest(url=url_nex,callback=self.parse_index,need_proxy=False)
            yield wei_nex


    def parse_detail(self,reponse):
        time.sleep(1)
        reponse.encoding='utf-8'
        doc=pq(reponse.text)
        print("细节解析")
        data={
            'titles': doc('#activity-name').text(),
            'contens':doc('#js_content').text(),
            'date': self.ruler.findall(reponse.text)[0],
            'wechat': doc('#js_name').text()
        }
        print(data)
        yield data

    def requesttt(self,wx):
        """

        :param wx: prepare（）方法，转化为prepared request请求
        :return: 响应值，和request.get()得到的reponse差不多
        """
        try:
            if wx.need_proxy:
                proxy=self.get_proxy()
                proxies={
                    'http': 'http://' + proxy,
                    'https': 'https://' + proxy#你需要对 body 或者 header （或者别的什么东西）做一些额外处理，，，，prepare（）
                }
                return self.session.send(wx.prepare(),timeout=wx.timeout,allow_redirects=True,proxies=proxies) #.prepare()方法，把weixinrequest中封装的参数，进行预处理，结束后，send（）出去，得到reaponse
            return self.session.send(wx.prepare(),timeout=wx.timeout,allow_redirects=True)
        except (requests.ConnectionError,requests.ConnectTimeout) as e:
            print(e.args)

    def error(self,wx):
        wx.fail_time=wx.fail_time +1
        print('request failed %s times %s '%(wx.fail_time,wx.url))
        if wx.fail_time <= Max_failed_time:
            self.queue.add(wx)
    def scheduler(self):
        while not self.queue.empty():
            wx=self.queue.pop()
            callback=wx.callback
            print('schedule %s'% wx.url)
            rseponse=self.requesttt(wx)
            if rseponse and rseponse.status_code in Valid_statues:
                print('zhix')
                results = list(callback(rseponse))
                if results:
                    for result in results:
                        if isinstance(result,weixinrequest):
                            self.queue.add(result)
                        if isinstance(result,dict):
                            self.mysql1.insert('articles',result)
                else:
                    self.error(wx)
            else:
              self.error(wx)

    def run(self):
        self.start()
        self.scheduler()


if __name__=='__main__':
    Spider1=spider()
    Spider1.run()











