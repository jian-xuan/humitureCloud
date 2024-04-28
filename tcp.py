import socket
import threading
import time

def handle_connection(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        data = data.decode()
        print(data)
        time.sleep(0.1)
    conn.close()

def danController():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
    tcp_socket.bind(('0.0.0.0', 8080))
    tcp_socket.listen(5)
    print('等待连接 ......')

    while True:
        conn, addr = tcp_socket.accept()
        print('连接成功： ', addr)
        thread = threading.Thread(target=handle_connection, args=(conn,))
        thread.start()

danController()