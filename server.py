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


def print_summary():
    while True:
        time.sleep(10)
        total_operations = sum(operation_count.values())
        num_tuples = len(tuple_space)
        if num_tuples > 0:
            total_key_size = sum(len(key) for key in tuple_space)
            total_value_size = sum(len(value) for value in tuple_space.values())
            avg_key_size = total_key_size / num_tuples
            avg_value_size = total_value_size / num_tuples
            avg_tuple_size = (total_key_size + total_value_size) / num_tuples
        else:
            avg_key_size = 0
            avg_value_size = 0
            avg_tuple_size = 0
        print(f"Number of tuples: {num_tuples}")
        print(f"Average tuple size: {avg_tuple_size}")
        print(f"Average key size: {avg_key_size}")
        print(f"Average value size: {avg_value_size}")
        print(f"Total clients connected: {client_count}")
        print(f"Total operations: {total_operations}")
        print(f"Total READs: {operation_count['READ']}")
        print(f"Total GETs: {operation_count['GET']}")
        print(f"Total PUTs: {operation_count['PUT']}")
        print(f"Total errors: {error_count}")


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    summary_thread = threading.Thread(target=print_summary)
    summary_thread.daemon = True
    summary_thread.start()

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    if 50000 <= port <= 59999:
        start_server(port)
    else:
        print("Port should be in the range 50000 - 59999")
