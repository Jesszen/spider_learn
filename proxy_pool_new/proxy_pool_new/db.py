import redis
from proxy_pool_new.settings import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,REDIS_KEY
from proxy_pool_new.settings import MAX_SCRORE,MIN_SCORE,INITIAL_SCORE
from proxy_pool_new.error import PoolEmptyerror
from random import choice
import re
from .logger_proxy import mylogger
logger=mylogger.get_logger(name='db')

class RedisClient(object):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        """
        初始化
        :param host: redis 地址
        :param part: redis 端口
        :param password: redis 密码
        decode_responses=True,写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。
        例子：不加，结果前多一个b，    b'hello world'
        """
        self.db = redis.StrictRedis(host= host,port=port,password=password,decode_responses=True)

    def add(self,proxy,intial_socore=INITIAL_SCORE):
        """
        添加代理，至代理池，并设置初始分值
        :param proxy: 获取的单个代理
        :param intial_socore: 初始评分值
        :return:
        """
        if not re.match(r'\d+\.\d*\.\d*\:\d*',proxy):
            logger.info('不符合规范 %s' % proxy)
            return
        if not self.db.zscore()


