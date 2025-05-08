#server.py
import socket
import threading
import time
from collections import defaultdict

# 元组空间
tuple_space = {}
# 操作计数器
operation_count = defaultdict(int)
# 错误计数器
error_count = 0
# 客户端连接计数器
client_count = 0

def handle_client(client_socket):
    global tuple_space, operation_count, error_count
    global client_count
    client_count += 1
try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            size = int(data[:3])
            command = data[3]
            key = data[4:].split(' ')[0]
            value = data[4 + len(key):].strip() if command == 'P' else None
