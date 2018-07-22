import asyncio
import aiohttp
from .db import RedisClient
import time
import sys
from .settings import *
from .logger_proxy import mylogger
logger=mylogger.get_logger('test')
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError

class tester(object):
    def __init__(self):
        self.redis=RedisClient()
    async def test_single_proxy(self,proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)  #下一句with  as  session:前后文管理器,with结束，session会话结束
        async with aiohttp.ClientSession(connector=conn) as session:#aiohttp则是基于asyncio实现的HTTP框架;这里要引入一个类，aiohttp.ClientSession.
                                                                      # 首先要建立一个session对象，然后用该session对象去打开网页
               try:
                   if isinstance(proxy,bytes):
                       proxy=proxy.decode('utf-8')#将bytes对象解码成字符串，默认使用utf-8进行解码。防止数据库提取的proxy是bytes格式。
                   real_proxy = 'http://' + proxy
                   logger.info('正在测试代理')
                   async with session.get(Test_url,proxy=real_proxy,timeout=15,allow_redirects=False) as response:
                       if response.status in VALID_STATUS_CODES:
                           self.redis.max(proxy)# 将可用代理分值设为100
                           logger.info('proxy is enable %s' %proxy)
                       else:
                           self.redis.decrease(proxy)
                           logger.info('请求响应码不合适 %s %s'%(response.status,proxy))
               except (ConnectionError,ClientError,TimeoutError,ArithmeticError):
                   self.redis.decrease(proxy)
                   logger.info('代理请求失败 %s'%proxy)
    def run(self):
        """
        测试主函数
        :return:
        """
        logger.info('测试器开始运行')
        try:
            count=self.redis.count()
            logger.info('当前剩余 %d 个代理'%count)
            for i in range(0,count,Batch_test_size):#所有代理，按照批次检测的个数，分段
                start = i
                stop=min(i+Batch_test_size,count)
                logger.info('正在检测第 %s 到%s之间的代理'%(start + 1,stop))
                test_proxies = self.redis.batch(start=start,stop=stop)
                loop = asyncio.get_event_loop()#asyncio实现并发，就需要多个协程组成列表来完成任务【创建多个协程的列表，然后将这些协程注册到事件循环中】，
                                               # 每当有任务阻塞的时候就await，然后其他协程继续工作，所以下面是协程列表；
                                               # 所谓的并发：多个任务需要同时进行；
                tasks=[self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))#asyncio.wait(tasks)接受一个列表
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            logger.exception('测试发生错误 %s'%e)












