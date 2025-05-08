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

            if command == 'R':
                operation_count['READ'] += 1
                if key in tuple_space:
                    result = f"{len(f'OK ({key}, {tuple_space[key]}) read'):03d}OK ({key}, {tuple_space[key]}) read"
                else:
                    result = f"{len(f'ERR {key} does not exist'):03d}ERR {key} does not exist"
                    error_count += 1
            elif command == 'G':
                operation_count['GET'] += 1
                if key in tuple_space:
                    value = tuple_space.pop(key)
                    result = f"{len(f'OK ({key}, {value}) removed'):03d}OK ({key}, {value}) removed"
                else:
                    result = f"{len(f'ERR {key} does not exist'):03d}ERR {key} does not exist"
                    error_count += 1
            elif command == 'P':
                operation_count['PUT'] += 1
                if key not in tuple_space:
                    tuple_space[key] = value
                    result = f"{len(f'OK ({key}, {value}) added'):03d}OK ({key}, {value}) added"
                else:
                    result = f"{len(f'ERR {key} already exists'):03d}ERR {key} already exists"
                    error_count += 1
            else:
                result = f"{len('ERR Invalid command'):03d}ERR Invalid command"
                error_count += 1

client_socket.send(result.encode())
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()
