# -*- coding: utf-8 -*-

from  lxml import etree
import re
from .utils import get_page
from random import choice
from pyquery import PyQuery as pq

from .logger_proxy import mylogger
logger=mylogger.get_logger('crawler')


class proxy_mataclass(type):
    """
    定义元类
    """
    def __new__(cls, name,bases,attrs):
        count=0
        attrs['__crawlfunc__']=[]
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__crawlfunc__'].append(k)
                count +=1
        attrs['__crawlcount__']=count
        return type.__new__(cls,name,bases,attrs)

class crawler(object,metaclass=proxy_mataclass):
    """
    metaclas取自定的元类。
    第一：元类的attrs参数，收录自定义类的所有属性。
    第二：我们自定义的这个proxy mataclass，的attrs属性，额外添加了两个属性，一个是’__crawlfunc__'属性，其对应的值为列表，用来存储包含crawl_字段的所有属性名称。
          另一个额外的属性是"__crawlcount__",对应的值，存储了crawlfunc属性的个数。
    """
    def get_crawler(self,callback):
        proxies=[]
        for proxy in eval('self.{}()'.format(callback)):
            logger.info('成功获取代理')
            proxies.append(proxy)
        return proxies


    def crawl_daili666(self,page_count=800):

        url='http://www.66ip.cn/{}.html'
        urls=[url.format(page) for page in range(page_count)]
        for u in urls:
            logger.info('begain crawl %s'%u)
            html=get_page(u)
            if html:
                doc=etree.HTML(html)#解析网页地址
                ip=doc.xpath('//div[@align="center"]//table//tr[position()>1]//td[1]/text()')
                prot=doc.xpath('//div[@align="center"]//table//tr[position()>1]//td[2]/text()')
                ip_address=list(zip(ip,prot))#元组列表
                for ip,port in ip_address:
                    yield  ':'.join([ip,port])#join的对象只能数字符型，此外join只接受一个参数，可以是列表，元组，字典，所以此处要用【】列表








