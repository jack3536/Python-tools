# -*- coding:utf-8 -*-
# @ProjectName  :demo
# @FileName     :publisher.py
# @Time         :20-7-14
# @Author       :EricLin
import pika
import json
msg = {
  "messageType":"2",
  "data":{
    "accessToken":"ceca20fb6xx",
    "appCode":"syscode",
    "expireTime":"2020-11-22 13:00:00",
    "phone":"1835xxxxxxxx"
}
}

def publish():
    credentials = pika.PlainCredentials("admin","passwd")
    connection = pika.BlockingConnection(pika.ConnectionParameters(credentials=credentials,host="192.168.68.175",port=5672,virtual_host="/"))
    channel = connection.channel()
    #定义交换机名称和类型
    channel.exchange_declare("fanout_exchage","fanout")

    channel.basic_publish(exchange="fanout_exchage",routing_key="",body=json.dumps(msg))

    connection.close()


if __name__ == "__main__":
    publish()
