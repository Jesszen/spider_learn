import requests
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent,FakeUserAgentError

import aiohttp
import asyncio

from .logger_proxy import mylogger

logger=mylogger.get_logger("utils")

try:
    agent = UserAgent()
except FakeUserAgentError as f:
    logger.exception(f)


def get_page(url,option={}):
    base_headers={
        'User_Agent':agent.random,
        'accept-encoding':'gzip, deflate, sdch',
        'accept-language': 'zh-CN,zh;q=0.8'
          }
    headers=dict(base_headers,**option)
    logger.info('抓取代理 %s'% url)
    try:
        r=requests.get(url,headers=headers)
        logger.info('抓取成功 %s %d'%(url,r.status_code))
        if r.status_code ==200:
            return r.text
    except ConnectionError as c:
        logger.exception(c)
        return None
