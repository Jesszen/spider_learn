import requests
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent,FakeUserAgentError

import aiohttp
import asyncio

from .logger_proxy import mylogger

logger=mylogger.get_logger("utils")

def get_page(url,option={}):
    try:
        agent=UserAgent()
    except FakeUserAgentError as f:
        logger.exception(f)

    base_headers={
        'User_Agent':agent.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
          }
    header=dict(base_headers,**option)
    logger.info('抓取代理 %s'% url)
    try:
        r=requests.get(url,header=header)
        logger.info('抓取成功 %s %d'%(url,r.status_code))
        if r.status_code ==200:
            return r.text
    except ConnectionError as c:
        logger.exception(c)
        return None
