from spider_monitor_flow.conf import LOG_DIR
import logging
import os
import time
import sys


class LogGen(object):
    loggers = {}

    def __init__(self):
        self.dir = LOG_DIR
        self.create_dir()

    def create_dir(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir, exist_ok=True)

    def create_logger(self, name):
        # 创建一个日志对象
        logger = logging.getLogger(name)
        # 设置logger等级
        logger.setLevel(logging.INFO)
        # 设置时间
        log_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        # 设置存放日志文件的目录
        log_name = '{}/{}.logs'.format(self.dir, name)
        # 创建存储文件对象
        file_obj = logging.FileHandler(log_name)
        # 设置文件logger等级
        file_obj.setLevel(logging.INFO)
        # 设置日志格式化信息
        formatter = logging.Formatter('%(asctime)s %(message)s')
        # 设置控制台终端显示输出日志信息（类似于print在终端打印输出）
        console_obj = logging.StreamHandler(sys.stdout)
        # 设置终端日志输出等级信息
        console_obj.setLevel(logging.INFO)
        # 设置文件日志输出格式化信息
        file_obj.setFormatter(formatter)
        # 设置终端日志输出格式化信息
        console_obj.setFormatter(formatter)
        # 设置文件日志事件加入进去
        logger.addHandler(file_obj)
        # 设置终端日志事件加入进去
        logger.addHandler(console_obj)
        return logger

    def get_logger(self, name):
        if name not in self.loggers:
            self.loggers[name] = self.create_logger(name)
        return self.loggers[name]


logger_manage = LogGen()

running_log = logger_manage.get_logger("runging")