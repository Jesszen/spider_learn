# -*- coding: utf-8 -*-

from .db import RedisClient
from .crawler import crawler
from .logger_proxy import mylogger
logger=mylogger.get_logger('getter')
POOL_UPPER_THRESHOLD=1000

class getter(object):
    def __init__(self):
        self.redis=RedisClient()
        self.crawl=crawler()

    def is_over_threshold(self):
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        logger.info('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawl.__crawlcount__):
                callback=self.crawl.__crawlfunc__[callback_label]
                proxies=self.crawl.get_crawler(callback)#可迭代对象
                for proxy in proxies:
                    self.redis.add(proxy)
