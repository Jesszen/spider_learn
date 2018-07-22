
from requests import Request
from config import *

class weixinrequest(Request):
    """
    super().__init__(a,b,c)继承类时，当子类重写init方法，遇到和父类同样的属性。直接显示引用属性
    (a,b,c)中的abc为子类init（）中传入的参数，且传入的参数要与要父类中属性先后顺序一致。

    """
    def __init__(self,url,callback,method='GET',headers=None,need_proxy=False,fail_time=0,timeout=TIMEOUT):
        super(weixinrequest,self).__init__(method,url,headers)#显示调用指定父类init这个三个属性，其他父类属性则相当于丢弃!!这三个属性，要和源码中属性出现的顺序对应
        self.callback=callback
        self.need_proxy=need_proxy
        self.fail_time=fail_time
        self.timeout=timeout



