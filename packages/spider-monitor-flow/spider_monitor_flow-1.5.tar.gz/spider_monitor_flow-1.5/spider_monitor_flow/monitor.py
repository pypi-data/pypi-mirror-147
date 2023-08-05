
from spider_monitor_flow.model import *
from spider_monitor_flow.exceptions import *
import time
from spider_monitor_flow.log import running_log

import signal




@singleton
class Monitor(object):
    name = "爬虫监测程序"
    def __init__(self,TYPE=None,MACHINE=None):
        self.TYPE = TYPE
        self.MACHINE = MACHINE
        self.status = None
        self.one_invoke_add = 0
        self.check_status()
        self.start_time = get_cur_timestamp()
        self.register_fields = {}
        self.register_props = []
        self.array_props = []
        self._init_register_fields()
        self.send_register()

    def check_status(self):
        status = Register.get_status(SPIDER_TYPE, SPIDER_MACHINE)
        if status == 0:
            self.log("此机器名已被占用，并正在运行中")
            exit()

    def _init_register_fields(self):
        old_register = Register.get_cur_dict(SPIDER_TYPE, SPIDER_MACHINE)
        fields = {
            "start_time": self.start_time,
            "status": 0,
            "spider_type": SPIDER_TYPE,
            "spider_name": SPIDER_MACHINE,
        }
        if self.TYPE:
            fields["spider_type"] = self.TYPE
        if self.MACHINE:
            fields["spider_name"] = self.MACHINE
        for k, v in REGISTER_FIELD.items():
            RegisterField.insert_or_update(SPIDER_TYPE, k, v["meaning"])
            self.register_props.append(k)
            if v.get("type") == "SUMMATION":
                fields[k] = old_register.get(k, 0)
                continue
            if v.get("type") == "ARRAY":
                self.array_props.append(k)
                fields[k] = "array"
                continue
            fields[k] = v["init"]
        self.register_fields = fields

    def send_register(self):
        try:
            self.register_fields["cur_time"] = get_cur_timestamp()
            Register.insert_or_update(self.register_fields)
            if self.one_invoke_add:
                num = self.one_invoke_add
                self.one_invoke_add = 0
                DateCollection.add(SPIDER_TYPE,SPIDER_MACHINE,get_cur_date(),num)
        except Exception as e:
            self.log(self.name+str(e),file=False)

    def hold_and_send_register(self):
        while self.status:
            self.send_register()
            time.sleep(CHECK_INTERVAL)
        self.log("爬虫监测程序退出",file=False)

    def run(self):
        self.log("爬虫监测程序启动",file=False)
        self.status = True
        pool.submit(self.hold_and_send_register)

    def set(self, prop, value):
        if prop not in self.register_props:
            raise NotValueProp()
        self.register_fields[prop] = value

    def push(self, prop, value):
        try:
            if prop not in self.array_props:
                raise NotValueProp()
            return ArrayCollection.add(SPIDER_TYPE, SPIDER_MACHINE, prop, value)
        except Exception as e:
            self.log(self.name+str(e),file=False)

    def count_add(self):
        self.log("计数加1",file=False)
        self.increase_summation("task_count")
        self.increase_summation("count")
        self.one_invoke_add += 1


    def increase_summation(self, field):
        self.set(field, self.register_fields[field] + 1)

    def update_status(self, status):
       self.register_fields["status"] = status

    def log(self, msg,file = True):
        if file:
            running_log.warning("{}   {}".format(get_cur_date(), msg))
        print("\033[1;31;40m{}\033[0m".format(msg))

    def my_handler(self,signum, frame):
        self.status = False
        self.log("程序被强制中止,正在释放监测进程，最多{}秒后自动退出".format(CHECK_INTERVAL), file=False)
        exit()
    def set_signal(self):
        signal.signal(signal.SIGINT, self.my_handler)







# 设置相应信号处理的handler


