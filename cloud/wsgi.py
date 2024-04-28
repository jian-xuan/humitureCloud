"""
WSGI config for cloud project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import socket
import time
import threading

from django.utils import timezone

from index import models
from index.self import  dev



# 全局变量 是温湿度的开关
def handle_connection(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        data = data.decode()
        tem = 1
        if(dev.auto is True):
            if(tem>40) :
                conn.send("t0".encode())
            else:
                conn.send("t1".encode())
        print(data)
        time.sleep(0.1)
    conn.close()


def danController():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接服务器
    server_addr = ('192.168.4.1', 8080)
    tcp_socket.connect(server_addr)
    print("连接成功")
    dev.conn = tcp_socket
    while True :
        data = tcp_socket.recv(1024)
        #print(data.decode())
        tem = data.decode()[2:6]
        hum = data.decode()[9:13]
        tOpen = data.decode()[14:15]
        models.DevInfo.objects.create(ip='192.168.4.1',tem=tem,hum=hum,tOpen=tOpen,receive_time=timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("收到数据："+data.decode())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloud.settings')

application = get_wsgi_application()

class MyThread(threading.Thread):
    def run(self):
        danController()

t = MyThread()
t.start()