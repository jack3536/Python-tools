# -*- coding:utf-8 -*-
# @ProjectName  :demo
# @FileName     :receiver1.py
# @Time         :20-7-14
# @Author       :EricLin
import pika
import time
import json
from threading import Thread
from functools import wraps


def asyncs(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def callback(ch,method,properties,body):
    print(json.loads(body))
    time.sleep(5)
    print("finish")
    ch.basic_ack(delivery_tag=method.delivery_tag)

@asyncs
def receive():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(credentials=credentials, host="192.168.68.12", port="5672", virtual_host="/"))
    channel = connection.channel()
    channel.exchange_declare("fanout_exchage",exchange_type="fanout",durable=True)
    result = channel.queue_declare("queue",exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(queue_name,exchange="fanout_exchage")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue_name,callback)
    channel.start_consuming()


if __name__ == "__main__":
    receive()




