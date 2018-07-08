"""
在Python中，异常也是对象，可对它进行操作。
所有异常都是基类Exception的成员。所有异常都从基类Exception继承，而且都在exceptions模块中定义
"""


class PoolEmptyerror(Exception):
    def __init__(self):
        Exception.__init__(self)
    def __str__(self):
        return repr('代理池已经枯竭')
