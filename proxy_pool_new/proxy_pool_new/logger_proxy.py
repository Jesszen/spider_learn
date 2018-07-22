import logging.config
import  os
import datetime
import logging.handlers
import yaml
import logging

import concurrent_log_handler
"""
class mylogger(object):
    log_path = os.path.join(os.curdir,'logs')

    if not os.path.exists(log_path):
        os.mkdir(log_path)

    log_name = datetime.datetime.now().strftime('%y-%m-%d') + '.log'

    logger_conf_path =os.path.join(os.curdir,'logging.conf')

    @staticmethod
    def init_log_conf():
        logging.config.fileConfig(mylogger.logger_conf_path)

    @staticmethod
    def get_logger(name=''):
        mylogger.init_log_conf()
        return logging.getLogger(name)


"""
log_name = datetime.datetime.now().strftime('%y-%m-%d') + '.log'


class mylogger(object):
    log_path = os.path.join(os.curdir,'logs')
    if not os.path.exists(log_path):
        os.mkdir(log_path)


    logger_conf_path =os.path.join(os.curdir,'logging.yaml')
    with open(logger_conf_path,'r') as log_conf:
        dict_yaml=yaml.load(log_conf)
    @staticmethod
    def init_log():
        logging.config.dictConfig(mylogger.dict_yaml)
    @staticmethod
    def get_logger(name=''):
        mylogger.init_log()
        return logging.getLogger(name)


class myloggerhander_r(logging.handlers.RotatingFileHandler):
    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename("%s.%d" % (self.baseFilename, i))
                dfn = self.rotation_filename("%s.%d" % (self.baseFilename,
                                                        i + 1))
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.rotation_filename(self.baseFilename + ".1")
            #改写
            if not os.path.exists(dfn):
                try:
                    self.rotate(self.baseFilename, dfn)
                except FileNotFoundError:
                    # 这里会出异常：未找到日志文件，原因是其他进程对该日志文件重命名了，忽略即可，当前日志不会丢失
                    pass
            """
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
           """
        if not self.delay:
            self.stream = self._open()

