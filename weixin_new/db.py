import redis
from pickle import dumps, loads
from requestmy import weixinrequest
from config import *


class RedisQueue():
    """
    反爬虫，我们把需要爬去的request（默认的，包含url，headers，mehtod请求方式get，等等
            我们又新加了几个属性，是否需要代理，爬取失败次数，该请求的回调等）
    重点！！！每定义方法都要return 对应的结果
    """
    def __init__(self,host=Redis_host,password=Redis_password,port=REdis_port):
        self.db=redis.StrictRedis(port=port,host=host,password=password)

    def add(self,request):
        """
        向队列添加符合weixinrequest的信心
        redis的列表形式添加
        :param request:
        :return:
        """
        if isinstance(request,weixinrequest):
            return self.db.rpush(Redis_key,dumps(request))#向队列添加序列化的request  因为redis的列表只接受字符串形式，而我们的weixinrequest类似字典的结构
        else:                                             #如果db.lpush列表Redis_key不存在，则新建一个名称Redis_key的空列表
            return False

    def pop(self):
        """
         从redis队列中取出请求
        :return:
        """
        if self.db.llen(Redis_key):#这个列表名Redis_key是从config引用过来的
            return loads(self.db.lpop(Redis_key)) #从队列头部第一个元素值，并在列表中删除该元素值
        else:
            return False

    def clear(self):
        self.db.delete(Redis_key)#删除列表

    def empty(self):
        return self.db.llen(Redis_key) == 0#返回列表是否为空

if __name__ == '__main__':
     ba = RedisQueue()
     u='http://www.badu.com'
     w=weixinrequest(url=u,need_proxy=True,callback='hello')
     ba.add(w)
     request=ba.pop() #我们从队列中取数出来，要求pop方法必须含有return语句，否则就是空
     print(request)
     print(request.url)
     print(request.callback)
