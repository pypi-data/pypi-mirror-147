# 爬虫监控程序配置


REGISTER_DB = {
    "engine": "mongo",
    "ip": '192.168.1.2',
    "port": 27017,
    "admin": 'root',
    "passwd": "password",
    "db": "spider-monitor",
    "col": "spider_status",
    "register_field_col": "register_field",
    "array_collection": "array_coll",
    "date_collection":"date_coll"
}
import os

BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR,"log")
################# 自己配置 ###########################
import uuid
SPIDER_TYPE = "xx_spider"
SPIDER_MACHINE = "1号"

# 检测时间间隔 /s
CHECK_INTERVAL = 30

REGISTER_FIELD = {
    "task_count": {
        "type": "SUMMATION",
        "meaning": "任务总数（所有时间）"
    },
    "count": {
        "init": 0,
        "meaning": "本次处理"
    },
    "error": {
        "type": "ARRAY",
        "meaning": "错误"
    },
    "account": {
        "init": "88285028@qq.com",
        "meaning": "账号"
    },

}
