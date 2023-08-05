from pymongo import MongoClient
from spider_monitor_flow.conf import *
from spider_monitor_flow.utils import *
from similib.mongodb import Mongo

mongo = Mongo(ip="192.168.1.231",port=27017,user=REGISTER_DB["admin"] , passwd=REGISTER_DB["passwd"]).conn

class Register(object):
    col = mongo[REGISTER_DB["db"]][REGISTER_DB["col"]]

    @classmethod
    def insert_or_update(cls, o):
        spider_type = o["spider_type"]
        spider_name = o["spider_name"]
        has_in = cls.col.find_one({"spider_type": spider_type, "spider_name": spider_name})
        if has_in:
            cls.col.update_one({"spider_type": spider_type, "spider_name": spider_name}, {"$set": o})
        else:
            cls.col.insert_one(o)

    @classmethod
    def update_status(cls, spider_type, spider_name, status):
        cls.col.update_one({"spider_type": spider_type, "spider_name": spider_name}, {"$set": {"status": status}})

    @classmethod
    def get_status(cls, spider_type, spider_name):
        res = cls.col.find_one({"spider_type": spider_type, "spider_name": spider_name})
        if res:
            status = res["status"]
            spider_cur_time = res["cur_time"]
            ts = get_cur_timestamp()
            if ts - spider_cur_time > CHECK_INTERVAL + 5:
                status = 1
            return status

    @classmethod
    def get_cur_dict(cls, spider_type, spider_name):
        cur_dict = cls.col.find_one({"spider_type": spider_type, "spider_name": spider_name})
        if not cur_dict:
            return {}
        return cur_dict


class RegisterField(object):
    col = mongo[REGISTER_DB["db"]][REGISTER_DB["register_field_col"]]

    @classmethod
    def insert_or_update(cls, spider_type, spider_field, spider_meaning):
        if cls.check_has_in(spider_type, spider_field):
            cls.col.update_one({"spider_type": spider_type, "spider_field": spider_field},
                               {"$set": {"spider_meaning": spider_meaning}})
        else:
            cls.col.insert_one(
                {"spider_type": spider_type, "spider_field": spider_field, "spider_meaning": spider_meaning})

    @classmethod
    def check_has_in(cls, spider_type, spider_field):
        return cls.col.find_one({"spider_type": spider_type, "spider_field": spider_field})


class ArrayCollection(object):
    col = mongo[REGISTER_DB["db"]][REGISTER_DB["array_collection"]]

    @classmethod
    def add(cls, spider_type, spider_name, spider_field, value):
        if cls.check_has_in(spider_type, spider_name, spider_field, value):
            return
        o = {
            "spider_type": spider_type,
            "spider_name": spider_name,
            "spider_field": spider_field,
            "value": value,
            "datetime": get_cur_timestamp(),
        }
        cls.col.insert_one(o)

    @classmethod
    def check_has_in(cls, spider_type, spider_name, spider_field, value):
        o = {
            "spider_type": spider_type,
            "spider_name": spider_name,
            "spider_field": spider_field,
            "value": value,
        }
        return cls.col.find_one(o)




class DateCollection(object):
    col = mongo[REGISTER_DB["db"]][REGISTER_DB["date_collection"]]

    @classmethod
    def add(cls, spider_type, spider_name, date,num):
        cur_count = cls.check_has_in(spider_type, spider_name, date)
        if cur_count:
            cls.col.update_one({"spider_type": spider_type, "spider_name": spider_name, "date": date},
                               {"$set": {"count": cur_count + num}})
        else:
            cls.col.insert_one({"spider_type": spider_type, "spider_name": spider_name, "date": date, "count": num})



    @classmethod
    def check_has_in(cls, spider_type, spider_name, date):
        o = {
            "spider_type": spider_type,
            "spider_name": spider_name,
            "date": date
        }
        c_res = cls.col.find_one(o)
        if c_res:
            return c_res["count"]


if __name__ == '__main__':
    ArrayCollection.add("wiki爬虫程序","192.168.1.158","error","wiki_error_test2")
