import time
from .api import app
from .tester import tester
from .getter import getter
from multiprocessing import Process
from .logger_proxy import mylogger
from .settings import *
logger=mylogger.get_logger('scheduler')

class sheduler(object):
    def sheduler_test(self,cycle=Tester_cycle):
        test=tester()
        while True:
            logger.info('测试器开始运行')
            test.run()
            time.sleep(cycle)

    def sheduler_get(self,cycle=Getter_cycle):
        get = getter()
        while True:
            logger.info('开始抓取代理')
            get.run()
            time.sleep(cycle)

    def sheduler_api(self):
        app.run(host=Api_host,port=Api_port)

    def run(self):
        logger.info('代理池开始工作')

        if Tester_enabled:
            tester_process = Process(target=self.sheduler_test)
            tester_process.start()

        if Getter_enabled:
            getter_process = Process(target=self.sheduler_get)
            getter_process.start()

        if Api_enabled:
            api_process = Process(target=self.sheduler_api)
            api_process.start()

