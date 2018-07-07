import logging.config
import  os
import datetime
import logging.handlers


class mylogger(object):
    log_path = os.path.join(os.curdir,'logs')

    if not os.path.exists(log_path):
        os.mkdir(log_path)

    log_name = datetime.datetime.now().strftime('%y-%m-%d') + '.log'

    logger_conf_path =os.path.join(os.curdir,'logging.conf')

    @staticmethod
    def init_log_conf():
        """
        #读取logging配置信息
        :return:
        """
        logging.config.fileConfig(mylogger.logger_conf_path)

    @staticmethod
    def get_logger(name=''):
        mylogger.init_log_conf()
        return logging.getLogger(name)


