import redis
from proxy_pool_new.settings import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,REDIS_KEY
from proxy_pool_new.settings import MAX_SCRORE,MIN_SCORE,INITIAL_SCORE
from proxy_pool_new.error import PoolEmptyerror
from random import choice
import re
from .logger_proxy import mylogger
logger=mylogger.get_logger(name='db')

class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: redis 地址
        :param part: redis 端口
        :param password: redis 密码
        decode_responses=True,写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。
        例子：不加，结果前多一个b，    b'hello world'
        """
        self.db = redis.StrictRedis(host= host, port=port, password=password, decode_responses=True)

    def add(self,proxy,score=INITIAL_SCORE):#score  已经又默认值，如果不特别指定
        """
        添加代理，至代理池，并设置初始分值
        :param proxy: 获取的单个代理
        :param intial_socore: 初始评分值
        :return:
        """
        if not re.match('\d+\.\d*\.\d*\.\d+\:\d*',proxy):
            logger.info('不符合规范 %s' % proxy)
            return
        if not self.db.zscore(REDIS_KEY,proxy):
            logger.info('代理添加到数据库')
            #语法 zscore(key,member),key为有序集合名，member为有序集合的键名，返回值为member对应的值，若不存在，返回nil
            return self.db.zadd(REDIS_KEY,score,proxy)#语法zadd(key,score,member),key有序集合名，scrore默认分值，proxy为member值

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数的代理，如果不存在，则按照排名顺序获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCRORE,MAX_SCRORE)
        #语法 zrangebyscore（key，min_score,max_score) y有序集合名，最低分，最高分、、、、返回有序集中指定分数区间内的所有的成员
        if len(result):#最高非空，则len（）为真，执行
            return  choice(result)#语法random.choice(seq),seq为一个列表，集合或者元组；返回值为seq的一个随机数。
        else:
            result = self.db.zrevrange(REDIS_KEY,0,100)# zvreverange(key,start,end)  ,Redis Zrevrange 命令返回有序集中，指定区间内的成员。其中成员的位置按分数值递减(从大到小)来排列。
            # 除此之外和ZRANGE命令一样，此处返回值数量是100个。即最高分至最低分数排序的，前101个代理
            #0,100  指的是redis数据库的下标！！！
            try:
                if len(result):
                    return choice(result)
            except PoolEmptyerror as e:
                logger.exception(e)      #记录异常

    def decrease(self,proxy):
        """
        代理值减一分，分数小于最小值，则对应的代理，删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY,proxy)
        if score and score>MIN_SCORE:
            logger.info('代理 %s 当前分数 %d 减一' %(proxy,score))
            return self.db.zincrby(REDIS_KEY,proxy,-1) #为有序集合，member对应的值减1
        else:
            logger.info('代理 %s 当前分数 %d 移除'%(proxy,score))
            return self.db.zrem(REDIS_KEY,proxy)#删除指定的键值对

    def exists(self,proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 返回是否存在
        """
        return not self.db.zscore(REDIS_KEY,proxy) == None

    def max(self,proxy):
        """
        将代理的分值设为最大值
        :param proxy: 代理
        :return: 设置最大值
        """
        logger.info('代理 %s 可设置最大值 %d' %(proxy,MAX_SCRORE))
        return self.db.zadd(REDIS_KEY,MAX_SCRORE,proxy)

    def count(self):
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部有效代理
        :return:
        """
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCRORE)
    def batch(self,start,stop):
        """
        批量获取代理
        :param start:
        :param stop:
        :return:
        """
        return self.db.zrevrange(REDIS_KEY,start,stop)


if __name__ =='__main__':
    conn=RedisClient()
    result = conn.batch(680,688)
    print(result)








